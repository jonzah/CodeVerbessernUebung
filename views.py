from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import zeiterfassung.functions as functions
import json
import csv
from django.core.files.storage import FileSystemStorage
from datetime import date, datetime, time, timedelta



jsonDatei = "/home/ubuntu/myproject/static/inhalte.json"
csvDatei = "/home/ubuntu/myproject/static/inhalte.csv"
ablzDatei = "/home/ubuntu/myproject/static/ablz.json"



def zeiterfassung(request):

    nummer = None

    with open (jsonDatei, "r") as data:
        listeMitDictionaries = json.loads(data.read())
        counter = 0
        for eintrag in listeMitDictionaries:
            counter +=1

    
    #hinzufügen
    if request.POST:
        if len(request.POST) > 3 and request.POST["aktion"] == "hinzufügen":
            modulEingabe = request.POST["modul"]
            startzeitEingabe = request.POST["startzeit"]
            endzeitEingabe = request.POST["endzeit"]
            commentEingabe = request.POST["kommentar"]

            ergebnis = functions.makeDict(counter, modulEingabe, startzeitEingabe, endzeitEingabe, commentEingabe,)

            functions.neuerInhaltJson(ergebnis)

            functions.moduleSortieren()

            functions.makeCSV(jsonDatei)


            return HttpResponseRedirect("../zeiterfassung")


        #löschen
        if len(request.POST) == 3 and request.POST["aktion"] == "löschen":

            nummer = int(request.POST["nr"])

            if isinstance(nummer, int):

                with open (jsonDatei, "r") as data:
                    listeMitDictionaries = json.loads(data.read())

                counter = 0
                neuerCounter = 1

                for eintrag in listeMitDictionaries:
                    counter += 1

                    if eintrag["Nummer"] == int(nummer):
                        listeMitDictionaries.pop(counter -1)

                for eintrag in listeMitDictionaries:
                    if eintrag["Nummer"] != "x":
                        eintrag["Nummer"] = neuerCounter
                        neuerCounter += 1

                    with open (jsonDatei, "w") as data2:
                            neueListe = json.dumps(listeMitDictionaries)
                            data2.write(neueListe)
                
                functions.moduleSortieren()

                functions.makeCSV(jsonDatei)
                    
                return HttpResponseRedirect("../zeiterfassung")



        #hochladen
        if request.POST["aktion"] == "hochladen":
            
            folder='/home/ubuntu/myproject/files'

            if request.method == 'POST' and request.FILES['fileToUpload']:
                myfile = request.FILES['fileToUpload']
                fs = FileSystemStorage(location=folder) 
                filename = fs.save(myfile.name, myfile)
                file_url = fs.url(filename)


                if filename.endswith('.json'):
                    with open(f"/home/ubuntu/myproject/files/{myfile}", "r") as importedFileJSON:
                        importierterInhalt = json.loads(importedFileJSON.read())

                    listeMitMustereintragJSON = [{"Nummer": "x", "Modul": "x", "Startzeit": "xx:xx", "Endzeit": "xx:xx", "Kommentar": "x"}]

                    for eintrag in importierterInhalt:
                        listeMitMustereintragJSON.append(eintrag)

                    with open(jsonDatei, "w") as content:
                        content.write(json.dumps(listeMitMustereintragJSON))
                    
                    functions.moduleSortieren()

                    functions.makeCSV(jsonDatei)
                    

                

                if filename.endswith('.csv'):
                    with open(f"/home/ubuntu/myproject/files/{myfile}") as importedFileCSV:
                        reader = csv.reader(importedFileCSV, delimiter=",")

                        listeMitMustereintragCSV = [{"Nummer": "x", "Modul": "x", "Startzeit": "xx:xx", "Endzeit": "xx:xx", "Kommentar": "x"}]

                        for row in reader:
                            dict = {}
                            dict["Nummer"] = row[0]
                            dict["Modul"] = row[1]
                            dict["Startzeit"] = row[2]
                            dict["Endzeit"] = row[3]
                            dict["Kommentar"] = row[4]

                            listeMitMustereintragCSV.append(dict)
                        
                    with open(jsonDatei, "w")as content:
                        content.write(json.dumps(listeMitMustereintragCSV))
                    
                    functions.moduleSortieren()
                    
                    functions.makeCSV(jsonDatei)

                
            return HttpResponseRedirect("../zeiterfassung")



    with open(jsonDatei, "r")as datei:

        inhalt = json.loads(datei.read())

    listeSoftwareEngineering = []
    listeSysteme = []
    listeInformatik = []

    
    zeitSoftwareEngineering = datetime(year=2022,month=1, day=1, hour=0, minute=0, second=0)
    zeitInformatik = datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0)
    zeitSysteme = datetime(year=2022, month=1, day=1, hour=0, minute=0, second=0)

    for eintrag in inhalt:

        if eintrag["Modul"] == "1.1.2":
            listeInformatik.append(eintrag)
        
        if eintrag["Modul"] == "1.3.1":
            listeSysteme.append(eintrag)
        
        if eintrag["Modul"] == "1.5.1":
            listeSoftwareEngineering.append(eintrag)
    

    for eintrag in listeInformatik:
            delta = functions.zeitErrechnen(eintrag["Startzeit"], eintrag["Endzeit"]).split(":")
            zeitInformatik = zeitInformatik + timedelta(hours= int(delta[0]), minutes= int(delta[1]))
               

    for eintrag in listeSoftwareEngineering:
            delta = functions.zeitErrechnen(eintrag["Startzeit"], eintrag["Endzeit"]).split(":")
            zeitSoftwareEngineering = zeitSoftwareEngineering + timedelta(hours= int(delta[0]), minutes= int(delta[1]))

    for eintrag in listeSysteme:
            delta = functions.zeitErrechnen(eintrag["Startzeit"], eintrag["Endzeit"]).split(":")
            zeitSysteme = zeitSysteme + timedelta(hours= int(delta[0]), minutes= int(delta[1]))

    listeMitZeiten = [zeitInformatik.strftime("%H:%M hour(s)"), zeitSysteme.strftime("%H:%M hour(s)"), zeitSoftwareEngineering.strftime("%H:%M hour(s)")]

    


                
    return render(request, 'zeiterfassung/meineTemplate.html', {"Liste": functions.jsonAuslesen, "Zeiten": listeMitZeiten})


                






#FallstudienBerichte

def fallstudie0322(request):
    return render(request, 'Fallstudie0322/Fallstudienbericht.html')

def fallstudie0922(request):
    return render(request, 'Fallstudie0922/Fallstudienbericht0922.html')


#privat

def ablz(request):

    if request.POST:
        if request.POST["aktion"] == "add":
            date = request.POST["date"]

            noah = request.POST["noah"]
            noahx = request.POST["noahx"]

            jonas = request.POST["jonas"]
            jonasx = request.POST["jonasx"]

            fabi = request.POST["fabi"]
            fabix = request.POST["fabix"]

            till = request.POST["till"]
            tillx = request.POST["tillx"]

            tom = request.POST["tom"]
            tomx = request.POST["tomx"]

            sesmoms = request.POST["sesmoms"]
            sesmomsx = request.POST["sesmomsx"]

            chris = request.POST["chris"]
            chrisx = request.POST["chrisx"]

            richy = request.POST["richy"]
            richyx = request.POST["richyx"]

            robin = request.POST["robin"]
            robinx = request.POST["robinx"]

            lukas = request.POST["lukas"]
            lukasx = request.POST["lukasx"]

            marlon = request.POST["marlon"]
            marlonx = request.POST["marlonx"]

            result = functions.makeDictABLZ(date, noah, noahx, jonas, jonasx, fabi, fabix, till, tillx, tom, tomx, sesmoms, sesmomsx, chris, chrisx, richy, richyx, robin, robinx, lukas, lukasx, marlon, marlonx)
            
            functions.neuerInhaltAblz(result)

            return HttpResponseRedirect("../arschbolzeliste")



        if request.POST["aktion"] == "löschen":

            datum = request.POST["datumL"]
            counter = 0

            if datum != "XX.XX.XXXX":

                with open (ablzDatei, "r") as data:
                    listeMitDictionaries = json.loads(data.read())


                for eintrag in listeMitDictionaries:

                    if eintrag["Datum"] == datum:
                        listeMitDictionaries.remove(listeMitDictionaries[counter])

                        with open (ablzDatei, "w") as data:
                            data.write(json.dumps(listeMitDictionaries))
                    
                    counter +=1


            return HttpResponseRedirect("../arschbolzeliste")


    return render(request, 'ablz/ablz.html', {"Daten": functions.jsonAuslesenAblz, "Erg": functions.prozent})


'''[{
    "Datum": "XX.XX.XXXX",
    "Noah": "X", 
    "Noahx": "X", 
    "Jonas": "X", 
    "Jonasx":"X", 
    "Fabi": "X", 
    "Fabix": "X", 
    "Till": "X", 
    "Tillx": "X", 
    "Tom": "X", 
    "Tomx": "X", 
    "Sesmoms": "X", 
    "Sesmomsx": "X", 
    "Chris": "X", 
    "Chrisx": "X", 
    "Richy": "X", 
    "Richyx": "X",
    "Robin": "X",
    "Robinx": "X",
    "Lukas": "X",
    "Lukasx": "X",
    "Marlon": "X",
    "Marlonx": "X",
}]'''