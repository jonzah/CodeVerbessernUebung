from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import zeiterfassung.functions as functions
import json
import csv
from django.core.files.storage import FileSystemStorage
from datetime import date, datetime, time, timedelta




ablzDatei = "/home/ubuntu/myproject/static/ablz.json"






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
