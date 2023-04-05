import json
import csv
from datetime import datetime, time
from operator import itemgetter

jsonDatei = "/home/ubuntu/myproject/static/inhalte.json"
csvDatei = "/home/ubuntu/myproject/static/inhalte.csv"
ablzDatei = "/home/ubuntu/myproject/static/ablz.json"


def makeDict(nummer, modul, starttime, endtime, comment):
    eintragDict = {
        "Nummer": nummer,
        "Modul": modul,
        "Startzeit": starttime,
        "Endzeit": endtime,
        "Kommentar": comment
    }
    return eintragDict


def jsonAuslesen():
    with open (jsonDatei, "r") as data:
        listeMitDictionaries = json.loads(data.read())
    return listeMitDictionaries


def neuerInhaltJson(inhalt):
    ergebnis = jsonAuslesen()
    with open (jsonDatei, "w") as datei:
        ergebnis.append(inhalt)
        datei.write(json.dumps(ergebnis))


def makeCSV(inhalt):
    with open (jsonDatei, "r") as datei:
        dictionaries = json.loads(datei.read())
    
    inhalt = ""

    for eintrag in dictionaries:
        neueZeile = f"{eintrag['Nummer']}, {eintrag['Modul']}, {eintrag['Startzeit']}, {eintrag['Endzeit']}, {eintrag['Kommentar']}\n"
        inhalt += neueZeile

    with open(csvDatei, "w", encoding="utf-8")as datei:
        datei.write(inhalt)



def zeitErrechnen(startzeitEingabe, endzeitEingabe):

    t1 = datetime.strptime(startzeitEingabe, "%H:%M")

    t2 = datetime.strptime(endzeitEingabe, "%H:%M")

    delta = t2 - t1

    delta = datetime.strptime(str(delta), "%H:%M:%S")


    return delta.strftime("%H:%M")



def moduleSortieren():
    with open(jsonDatei, "r")as datei:
        inhalt = json.loads(datei.read())

    sortierteListe = sorted(inhalt, key=itemgetter('Modul'))
    listeMitMustereintrag = []

    for eintrag in sortierteListe:
        if eintrag["Modul"] == "x":
            listeMitMustereintrag.append(eintrag)
    
    for eintrag in sortierteListe:
        if eintrag["Modul"] != "x":
            listeMitMustereintrag.append(eintrag)

    counter = 1

    for eintrag in listeMitMustereintrag:
        if eintrag["Nummer"] != "x":
            eintrag["Nummer"] = counter
            counter += 1


    with open(jsonDatei, "w")as datei:
        datei.write(json.dumps(listeMitMustereintrag))



#ABLZ

def makeDictABLZ(date, noah, noahx, jonas, jonasx, fabi, fabix, till, tillx, tom, tomx, sesmoms, sesmomsx, chris, chrisx, richy, richyx, robin, robinx, lukas, lukasx, marlon, marlonx):
    ergebnis = {
        "Datum": date,
        "Noah": noah, 
        "Noahx": noahx, 
        "Jonas": jonas, 
        "Jonasx":jonasx, 
        "Fabi": fabi, 
        "Fabix": fabix, 
        "Till": till, 
        "Tillx": tillx, 
        "Tom": tom, 
        "Tomx": tomx, 
        "Sesmoms": sesmoms, 
        "Sesmomsx": sesmomsx, 
        "Chris": chris, 
        "Chrisx": chrisx, 
        "Richy": richy, 
        "Richyx": richyx,
        "Robin": robin, 
        "Robinx": robinx,
        "Lukas": lukas, 
        "Lukasx": lukasx,
        "Marlon": marlon, 
        "Marlonx": marlonx
    }
    return ergebnis


def jsonAuslesenAblz():
    with open (ablzDatei, "r") as data:
        listeMitDictionaries = json.loads(data.read())
    return listeMitDictionaries


def neuerInhaltAblz(inhalt):
    ergebnisAblz = jsonAuslesenAblz()
    
    with open (ablzDatei, "w") as datei:
        ergebnisAblz.append(inhalt)
        datei.write(json.dumps(ergebnisAblz))

def prozent():

    aktuellerInhalt = jsonAuslesenAblz()

    varNoah = 0
    varNoahx = 0
    varJonas = 0
    varJonasx = 0
    varFabi = 0 
    varFabix = 0
    varTill = 0 
    varTillx = 0
    varTom = 0 
    varTomx = 0 
    varSesmoms = 0
    varSesmomsx = 0 
    varChris = 0
    varChrisx = 0
    varRichy = 0
    varRichyx = 0
    

    dictAlle = {}
    
    for eintrag in aktuellerInhalt:
        if len(aktuellerInhalt) > 1:
            if eintrag["Datum"] != "XX.XX.XXXX":

                if eintrag["Noah"] != "0":
                    varNoah += int(eintrag["Noah"])
                    varNoahx += int(eintrag["Noahx"])

                if eintrag["Jonas"] != "0":
                    varJonas += int(eintrag["Jonas"])
                    varJonasx += int(eintrag["Jonasx"])

                if eintrag["Fabi"] != "0":
                    varFabi += int(eintrag["Fabi"])
                    varFabix += int(eintrag["Fabix"])

                if eintrag["Till"] != "0":
                    varTill += int(eintrag["Till"])
                    varTillx += int(eintrag["Tillx"])

                if eintrag["Tom"] != "0":
                    varTom += int(eintrag["Tom"])
                    varTomx += int(eintrag["Tomx"])
                
                if eintrag["Sesmoms"] != "0":   
                    varSesmoms += int(eintrag["Sesmoms"])
                    varSesmomsx += int(eintrag["Sesmomsx"])

                if eintrag["Chris"] != "0":
                    varChris += int(eintrag["Chris"])
                    varChrisx += int(eintrag["Chrisx"])

                if eintrag["Richy"] != "0":
                    varRichy += int(eintrag["Richy"])
                    varRichyx += int(eintrag["Richyx"])
                



                if varNoah != 0:
                    dictAlle["NoahPr"] = round(((varNoahx / varNoah)*100),2)
                else:
                    dictAlle["NoahPr"] = 0.0

                if varJonas != 0: 
                    dictAlle["JonasPr"] = round(((varJonasx / varJonas)*100),2)
                else:
                    dictAlle["JonasPr"] = 0.0

                if varFabi != 0:
                    dictAlle["FabiPr"] = round(((varFabix / varFabi)*100),2)
                else:
                    dictAlle["FabiPr"] = 0.0

                if varTill != 0:   
                    dictAlle["TillPr"] = round(((varTillx / varTill)*100),2)
                else:
                    dictAlle["TillPr"] = 0.0
                
                if varTom != 0:
                    dictAlle["TomPr"] = round(((varTomx / varTom)*100),2)
                else:
                    dictAlle["TomPr"] = 0.0
                
                if varSesmoms != 0:
                    dictAlle["SesmomsPr"] = round(((varSesmomsx / varSesmoms)*100),2)
                else:
                    dictAlle["SesmomsPr"] = 0.0
                
                if varChris != 0:
                    dictAlle["ChrisPr"] = round(((varChrisx / varChris)*100),2)
                else:
                    dictAlle["ChrisPr"] = 0.0
                
                if varRichy != 0:
                    dictAlle["RichyPr"] = round(((varRichyx / varRichy)*100),2)
                else:
                    dictAlle["RichyPr"] = 0.0

    return dictAlle