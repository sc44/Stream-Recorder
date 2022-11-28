#! /usr/bin/env python3
#
#  StreamRecorder v1.50 - Update: 25.11.2022
#
###############################################################################################################

import tkinter as tk
import tkinter.filedialog as fdialog
import tkinter.colorchooser as chooser
import tkinter.messagebox as message
import platform
import locale
import os
import signal
import subprocess
import time
import datetime
import urllib.request
import urllib.error

###############################################################################################################

if platform.system() == "Windows":    WINDOWS = True
else:                                 WINDOWS = False
print(platform.platform())
print("Python Version " + platform.python_version())

Name = [""]
Land = [""]
Sprache = [""]
Gruppe = [""]
URL = [""]

PufNr = [0]
Puffer = [""]
sPuffer = [""]
recPID = [0]
recName = [""]
recStart = [""]
recEnde = [""]
altName = [""]
altLink = [""]
altPos = 0

StatusAnzahl = 0
StatusAufnahmen = 0
StatusBeendete = 0
StatusFehler = 0

Wochentag = [0,0,0,0,0,0,0,0] 
WochenText = "-------"
Suchbereich = 0
Suchbegriff = ""

HauptGeo = "770x875+500+50"
Vordergrund = "#ffffcc"
Hintergrund = "#000066"
FensterVG = "#000000"
FensterHG = "#ffff88"
FontM = "Helvetica "
SizeM = "11"
SizeL = "10"
if WINDOWS:  SizeL = "11"
Gebiet = "de"
pAktiv = 0
uaAktiv = 0

m3uDatei = ""
m3uMerker = ""
startDatei = ""

if WINDOWS:
    confVerzeichnis = os.path.dirname(os.path.abspath(__file__)) + "/"
    cacheVerzeichnis = os.path.dirname(os.path.abspath(__file__)) + "/"
else:
    confVerzeichnis = os.path.expanduser("~") + "/.config/srecorder/"
    cacheVerzeichnis = os.path.expanduser("~") + "/.cache/srecorder/"

recVerzeichnis = os.path.expanduser("~") + "/Videos/"
m3uVerzeichnis = os.path.expanduser("~") + "/Downloads/"

confDatei = confVerzeichnis + "srecorder.conf"
cmdDatei = confVerzeichnis + "scomand.conf"
playerDatei = confVerzeichnis + "splayer.conf"
uaDatei = confVerzeichnis + "useragent.conf"
protDatei = cacheVerzeichnis + "protocol"
schedDatei = cacheVerzeichnis + "schedule"

cmdxListe = ["","","","","","","","",""]

if WINDOWS:
    cmdListe = [ \
    'ffmpeg -i "link" -c copy "file" 2> nul',
    'for /f %a in (\'youtube-dl -g -f best --no-playlist "link"\') do ffmpeg -i %a -c copy "file" 2> nul',
    'for /f %a in (\'yt-dlp -g -f b --no-playlist "link"\') do ffmpeg -i %a -c copy "file" 2> nul',
    'for /f %a in (\'youtube-dl -g -f best --no-playlist "link"\') do ffmpeg -user_agent "uagent" -i %a -c copy "file" 2> nul',
    'for /f %a in (\'yt-dlp -g -f b --no-playlist "link"\') do ffmpeg -user_agent "uagent" -i %a -c copy "file" 2> nul',
    '',
    'yt-dlp -F "link"',
    'yt-dlp "link" -P "file".dir',
    './srecorder.bat "link"' ]
else:
    cmdListe = [ \
    'ffmpeg -i "link" -c copy "file" 2> /dev/null',
    'ffmpeg -i $(youtube-dl -g -f best --no-playlist "link") -c copy "file" 2> /dev/null',
    'ffmpeg -i $(yt-dlp -g -f b --no-playlist "link") -c copy "file" 2> /dev/null',
    'ffmpeg -user_agent "uagent" -i $(youtube-dl -g -f best --no-playlist "link") -c copy "file" 2> /dev/null',
    'ffmpeg -user_agent "uagent" -i $(yt-dlp -g -f b --no-playlist "link") -c copy "file" 2> /dev/null',
    '',
    'yt-dlp -F "link"      # List available formats of video or playlist.',
    'yt-dlp "link" -P "file".dir      # Download video or playlist into path.',
    './srecorder.sh "link"      # Run a bash script.' ]

if WINDOWS:
    pListe = [ \
    'FFplay                  "C:/Program Files/ffmpeg/bin/ffplay.exe" "URL[Nr]"',
    'FFplay  1280x720        "C:/Program Files/ffmpeg/bin/ffplay.exe" -x 1280 -y 720 -window_title ffplay "URL[Nr]" 2> NUL',
    'Windows Media Player    "C:/Program Files/Windows Media Player/wmplayer.exe" "URL[Nr]"',
    'VLC  Media Player       "C:/Program Files/VideoLAN/VLC/vlc.exe" "URL[Nr]"',
    'MPV  Media Player       "C:/Program Files (x86)/MPV/mpvnet.exe" "URL[Nr]"',
    'SMPlayer                "C:/Program Files/SMPlayer/smplayer.exe" "URL[Nr]"',
    'SMPlayer  1480x1020     "C:/Program Files/SMPlayer/smplayer.exe" "URL[Nr]" -size 1480 1020',
    'SMPlayer  Windows-GUI   "C:/Program Files/SMPlayer/smplayer.exe" "URL[Nr]" -mpcgui',
    'Zoom  Video Player      "C:/Program Files (x86)/Zoom Player/zplayer.exe" "URL[Nr]"',
    'Pot  Media Player       "C:/Program Files/DAUM/PotPlayer/PotPlayerMini64.exe" "URL[Nr]"',
    'KM  Media Player        "C:/Program Files/KMPlayer/KMPlayer.exe" "URL[Nr]"',
    'GOM  Media Player       "C:/Program Files (x86)/GOM/GOMPlayer/GOM.exe" "URL[Nr]"',
    'Real  Media Player      "C:/Program Files (x86)/Real/RealPlayer/realplayer.exe" "URL[Nr]"' ]
else:
    pListe = [ \
    'FFplay                  ffplay "URL[Nr]"',
    'FFplay  1280x720        ffplay -x 1280 -y 720 -window_title ffplay "URL[Nr]" 2> /dev/null',
    'SMPlayer                smplayer "URL[Nr]"',
    'SMPlayer  1480x1020     smplayer "URL[Nr]" -size 1480 1020',
    'SMPlayer  Windows-GUI   smplayer "URL[Nr]" -mpcgui',
    'MPV  Media Player       mpv "URL[Nr]"',
    'MPV  (UMPV) one Inst.   umpv "URL[Nr]"',
    'Celluloid  (Gnome-MPV)  celluloid "URL[Nr]"',
    'Gnome-MPlayer           gnome-mplayer "URL[Nr]"',
    'VLC  Media Player       vlc "URL[Nr]" 2> /dev/null',
    'SVLC  simple Interface  svlc  "URL[Nr]" 2> /dev/null',
    'CVLC  without Interface cvlc "URL[Nr]"',
    'FFmpeg | mpv            ffmpeg -i "URL[Nr]" -c copy -f mpegts - | mpv -',
    'FFmpeg > /dev/nul | mpv ffmpeg -i "URL[Nr]" -c:v copy -c:a copy -f mpegts - 2> /dev/null | mpv -' ]

uaListe = [ \
'Windows 10 / Chrome 107       Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
'Windows 10 / Chrome 107 Win64 Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
'Windows 10 / Chrome 107 WOW64 Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
'Windows 10 / Edge 107         Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.42',
'Windows 10 / Firefox 107      Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:107.0) Gecko/20100101 Firefox/107.0',
'Windows 10 / IExplorer 11     Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Windows 6.1 / Firefox 52      Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
'Windows 6.1 / IExplorer 11    Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Linux / Chrome 72             Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
'Linux / Firefox 107           Mozilla/5.0 (X11; Linux x86_64; rv:107.0) Gecko/20100101 Firefox/107.0',
'Linux / Ubuntu Server         Apache/2.4.34 (Ubuntu) OpenSSL/1.1.1 (internal dummy connection)',
'Linux / Debian Server         Apache/2.4.25 (Debian) (internal dummy connection)',
'Linux / Thunderstorm          Thunderstorm/1.0 (Linux)',
'Linux / Wget                  Wget/1.12 (linux-gnu)',
'Google Bot                    Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
'Google Bot / Safari           Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; Googlebot/2.1; +http://www.google.com/bot.html) Safari/537.36',
'Mac OS X / Safari 16          Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
'Mac OS X / Firefox 107        Mozilla/5.0 (Macintosh; Intel Mac OS X 13.0; rv:107.0) Gecko/20100101 Firefox/107.0',
'Android Tablet / Chrome 75    Mozilla/5.0 (Linux; Android 9.0; SAMSUNG-SM-T377A Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Mobile Safari/537.36',
'Android Tablet / Firefox 67   Mozilla/5.0 (Android 9.0; Tablet; rv:67.0) Gecko/67.0 Firefox/67.0',
'Android Phone / Chrome 75     Mozilla/5.0 (Linux; Android 9.0; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Mobile Safari/537.36',
'Android Phone / Firefox 67    Mozilla/5.0 (Android 9.0; Mobile; rv:67.0) Gecko/67.0 Firefox/67.0',
'iPhone / Safari 12            Mozilla/5.0 (iPhone; CPU OS 10_14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/14E304 Safari/605.1.15',
'iPad / Safari 12              Mozilla/5.0 (iPad; CPU OS 10_14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/605.1.15',
'n.a.                          ' ]

cListe = ["AE","AR","ARAB","AT","AU","BR","BY","CA","CH","CL","CN","CZ","DE","EC","EG","ES","ET","FR","GR","HK","HU","JP","KR","KW",\
          "IN","INT","IR","IT","MA","MD","MN","MO","MX","MY","NL","PL","PS","PY","RO","RU","SA","SAS","SE","TW","UA","UK","US","XK"]

gListe = ["Allgemein","Comedy","Bildung","Business","Documentary","Doku","Education","Entertainment","Family","Filme","Gaming",\
          "General","Gesundheit","Hobby","Kids","Kinder","Kultur","Lifestyle","Local","Movies","Music","Musik","Nachrichten","Natur",\
          "News","Politik","Regional","Religion","Religious","Serie","Shop","Spiel","Sport","Technik","Travel","Unterhaltung","XXX"]

Woerterbuch = { \
"de" : {"Datei":" Datei ","Suchen":" Suchen ","Favoriten":" Favoriten ","Aufnahme":" Aufnahme ","Schedule":" Schedule ",
        "Hilfe":" Hilfe ","Öffnen":"  Öffnen ","Bearbeiten":"  Bearbeiten ","Player":"  Player auswählen ","Info":"  Info ",
        "UserAgent":"  User-Agent ändern ","Einstellungen":"  Einstellungen ","Beenden":"  Beenden ","nNamen":"  Nach Namen ",
        "nLand":"  Nach Land ","nGruppe":"  Nach Gruppe ","Alle":"  Alle anzeigen ","Anzeigen":"  Anzeigen ","Über":"  Über ",
        "Hinzufügen":"  Hinzufügen ","Entfernen":"  Entfernen ","Zurück":"  Zurück ","Stoppen":"  Anzeigen / Stoppen ",
        "AlleStop":"  Alle beenden ","Protokoll":"  Protokoll anzeigen ","Tastatur":"  Tastatur ","sDatei":"Start-Playlist:",
        "Schrift Menü":"Schriftgröße des Menüs auswählen: ", "Schrift Liste":"Schriftgröße der Playlist auswählen: ",
        "VGfarbe":"Vordergrundfarbe einstellen","HGfarbe":"Hintergrundfarbe einstellen","FFschema":"Fensterfarbschema auswählen",
        "pVerzeichnis":" Playlist-Verzeichnis:","rVerzeichnis":" Aufnahme-Verzeichnis:","Laufende Aufnahmen":"Laufende Aufnahmen",
        "Speichern":"Speichern","Abbrechen":"Abbrechen","Datei speichern":" Speichern mit <Ctrl+S> oder <Doppelklick-Rechts> ",
        "Aufnahme stoppen":" Aufnahme stoppen mit <Doppelklick-Links>","Deutsch":"  Deutsch  ","Englisch":"  Englisch ","hinzu":" hinzugefügt",
        "wirklich beenden":" Sollen wirklich alle Aufnahmen beendet werden?  ","Player prüfen":"   Keine Überprüfung der Player-Installation",
        "SuchSpeich":"  Suche speichern","kein Suchfilter":" Zuerst einen Suchfilter setzen.  ","Begriff auswählen":"Suchbegriff auswählen:",
        "Sender speichern":"Ausgewählte Sender speichern unter:","Eingeben":"  Neuer Stream","Gruppe":"Gruppe:","Land":"Land:",
        "Sprache":"Sprache:","Youtube an":"   youtube-dl beim Programmstart einbinden","Beendet Timer":"Beendet von Timer      - ",
        "einbinden als":" als Download-Manager einbinden","einbinden keinen":"Keinen Download-Manager einbinden","Unbenannt":"Unbenannt",
        "Kein Sender":" Kein Sender ausgewählt.  ","nicht gefunden":" nicht gefunden.  ","wirklich entfernen":" wirklich entfernen?  ",
        "Zeilenumbruch":"   Keinen Zeilenumbruch in Datei Bearbeiten","Protokoll aus":"   Keine Meldungen ins Protokoll schreiben",
        "Fenster anders":"   Meldung bei Änderung der Fenstergröße", "Experten Modus":"   Download-Manager im Experten-Modus",
        "Eintrag entfernen":"Eintrag entfernen mit <Doppelklick-Links> oder <Entf> Taste","Begriff eingeben":"Suchbegriff eingeben:",
        "Mo":"Mo","Di":"Di","Mi":"Mi","Do":"Do","Fr":"Fr","Sa":"Sa","So":"So","Gestartet Schedule":"Start von Timer    - ",
        "Gestartet Benutzer":"Start von Benutzer - ","Beendet Benutzer":"Beendet von Benutzer   - ","Manager":"  Download-Manager",
        "Groesse Fenster":"Die Größe/Position des Hauptfensters wurde geändert.  \n\n  Sollen die neuen Koordinaten gespeichert werden?  ",
        "Entwickelt":" ++++ Entwickelt von Woodstock & sc44 ++++ Dieses Programm wird unter den Bedingungen der GNU General Public License veröffentlicht, Copyright (C) 2022."},

"en" : {"Datei":" File ","Suchen":" Search ","Favoriten":" Favorites ","Aufnahme":" Recording ","Schedule":" Schedule ",
        "Hilfe":" Help ","Öffnen":"  Open ","Bearbeiten":"  Edit ","Player":"  Player ","Info":"  Info ",
        "UserAgent":"  User-Agent ","Einstellungen":"  Settings ","Beenden":"  Exit ","nNamen":"  Name ",
        "nLand":"  Country ","nGruppe":"  Category ","Alle":"  List all ","Anzeigen":"  Display ","Über":"  About ",
        "Hinzufügen":"  Add ","Entfernen":"  Delete ","Zurück":"  Back ","Stoppen":"  Disp / Stop ","Unbenannt":"Unnamed",
        "AlleStop":"  Stop all ","Protokoll":"  Protocol ","Tastatur":"  Keyboard ","FFschema":" Select window color scheme ",
        "Schrift Menü":"Set the font size of the menu: ", "Schrift Liste":"Set the font size of the playlist: ",
        "VGfarbe":"     Set foreground color     ","HGfarbe":"    Set background color    ","sDatei":"Start playlist:",
        "pVerzeichnis":" Playlist directory:","rVerzeichnis":" Recording directory:","Laufende Aufnahmen":"Active recordings",
        "Speichern":"    Save    ","Abbrechen":"     Exit     ","Datei speichern":" Save file with <Ctrl+S> or <Right Double Click> ",
        "Aufnahme stoppen":" Stop recording with <Left Double Click>","Deutsch":"  German  ","Englisch":"  English  ",
        "wirklich beenden":" Are you sure you want to stop all recordings?  ","Player prüfen":"   No verification of player installation",
        "SuchSpeich":"  Save search","kein Suchfilter":" First set a search filter.  ","Begriff auswählen":"Select a search term:",
        "Sprache":"Language:","Youtube an":"   Include youtube-dl at program start","Beendet Timer":"Terminated by timer    - ",
        "einbinden als":" include as download manager","einbinden keinen":"Do not include any download manager","hinzu":" added",
        "Sender speichern":"Selected channels save as:","Eingeben":"  New stream","Gruppe":"Group:","Land":"Country:",
        "Kein Sender":" No channel selected.  ","nicht gefunden":" not found.  ","wirklich entfernen":" really remove?  ",
        "Zeilenumbruch":"   Don't wrap lines in the file edit window ","Protokoll aus":"   Don't write any messages in the logfile",
        "Fenster anders":"   Message when changing the window size", "Experten Modus":"   Set download manager to expert mode",
        "Eintrag entfernen":"Remove entry with <Left Double Click> or <Del> key","Begriff eingeben":"Enter a search term:",
        "Mo":"Mon","Di":"Tue","Mi":"Wed","Do":"Thu","Fr":"Fri","Sa":"Sat","So":"Sun","Gestartet Schedule":"Started by timer   - ",
        "Gestartet Benutzer":"Started by user    - ","Beendet Benutzer":"Terminated by user     - ","Manager":"  Download manager",
        "Groesse Fenster":"The size/position of main window has changed.  \n\n  Do you want to save the new coordinates?  ",
        "Entwickelt":" +++++ Developed by Woodstock & sc44 +++++ This program is published under the terms of the GNU General Public License, Copyright (C) 2022."} }  

###############################################################################################################

Master = tk.Tk()
Master.title("Stream Recorder v1.5")
Master.option_add("*Dialog.msg.font", "Helvetica 11")        # Messagebox Schriftart
Master.option_add("*Dialog.msg.wrapLength", "50i")           # Messagebox Zeilenumbruch

if WINDOWS:    Bildchen = "./srecorder.png"
else:          Bildchen = "/usr/share/icons/hicolor/128x128/apps/srecorder.png"
if os.path.isfile(Bildchen):    Master.iconphoto(False, tk.PhotoImage(file=Bildchen))

if locale.getlocale()[0][0:2] == "de":    Gebiet = "de"
else:                                     Gebiet = "en"

GebietButton = tk.StringVar()                # Gebietsschema
Statustext = tk.StringVar()                  # Statuszeile
Lauftext = tk.StringVar()                    # Laufschrift
Zeilenumbruch = tk.IntVar()                  # Zeilenumbruch an/aus
Zeilenumbruch.set(1)                         # default = keinen Zeilenumbruch
ProtMeldAus = tk.IntVar()                    # Protokollmeldungen an/aus
ProtMeldAus.set(0)                           # default = Protokoll schreiben
FensterAnders = tk.IntVar()                  # Fensterabfrage an/aus
FensterAnders.set(1)                         # default = Abfrage anzeigen
PlayerPruefen = tk.IntVar()                  # Player-Installation prüfen
PlayerPruefen.set(0)                         # default = überprüfen
ExpertenModus = tk.IntVar()                  # Experten-Modus an/aus
ExpertenModus.set(0)                         # default = Standard-Modus
youtube_dl = tk.IntVar()                     # Nummer der Kommandozeile
youtube_dl.set(0)                            # default = 1.Zeile
ZeichenLand = tk.StringVar()                 # Suche nach Land
ZeichenLand.set(cListe[12])                  # default = "DE"
ZeichenGruppe = tk.StringVar()               # Suche nach Gruppe
ZeichenGruppe.set(gListe[0])                 # default = "Movies"

recPID.clear()                               # Aufnahme-PID, -Name, -Startzeit, -Endezeit löschen
recName.clear()
recStart.clear()
recEnde.clear()
altName.clear()                              # vorher gesehene Sender (History-Liste) löschen
altLink.clear()

###############################################################################################################

def Schreibe_confDatei():

    with open(confDatei, "w", encoding="utf-8") as Datei:
        Datei.write("m3u=" + m3uVerzeichnis + "\n")
        Datei.write("records=" + recVerzeichnis + "\n")
        Datei.write("start=" + startDatei + "\n")
        Datei.write("geometry=" + HauptGeo + "\n")
        Datei.write("fg=" + Vordergrund + "\n")
        Datei.write("bg=" + Hintergrund + "\n")
        Datei.write("fg2=" + FensterVG + "\n")
        Datei.write("bg2=" + FensterHG + "\n")
        Datei.write("size1=" + SizeM + "\n")
        Datei.write("size2=" + SizeL + "\n")
        Datei.write("language=" + Gebiet + "\n")
        Datei.write("player=" + str(pAktiv) + "\n")    
        Datei.write("uagent=" + str(uaAktiv) + "\n")    
        Datei.write("youtube=" + str(youtube_dl.get()) + "\n")
        Datei.write("nowrap=" + str(Zeilenumbruch.get()) + "\n")
        Datei.write("noprot=" + str(ProtMeldAus.get()) + "\n")
        Datei.write("winchng=" + str(FensterAnders.get()) + "\n")
        Datei.write("nocheck=" + str(PlayerPruefen.get()) + "\n")
        Datei.write("expert=" + str(ExpertenModus.get()) + "\n")
        Datei.close()

###############################################################################################################

if not os.path.isdir(confVerzeichnis):
    os.makedirs(confVerzeichnis)
if not os.path.isdir(cacheVerzeichnis):
    os.makedirs(cacheVerzeichnis)

if os.path.isfile(confDatei):                # wenn Konfigurationsdatei existiert dann laden
    with open(confDatei, "r", encoding="utf-8") as Datei:
        Puffer.clear() 
        for Zeile in Datei:
            Puffer.append(Zeile)
        Datei.close()
        for i in range(len(Puffer)):
            if Puffer[i][0:4] == "m3u=":       m3uVerzeichnis = Puffer[i][4:].rstrip()
            if Puffer[i][0:8] == "records=":   recVerzeichnis = Puffer[i][8:].rstrip()
            if Puffer[i][0:6] == "start=":     startDatei = Puffer[i][6:].rstrip()
            if Puffer[i][0:9] == "geometry=":  HauptGeo = Puffer[i][9:].rstrip()
            if Puffer[i][0:3] == "fg=":        Vordergrund = Puffer[i][3:10]
            if Puffer[i][0:3] == "bg=":        Hintergrund = Puffer[i][3:10]
            if Puffer[i][0:4] == "fg2=":       FensterVG = Puffer[i][4:11]
            if Puffer[i][0:4] == "bg2=":       FensterHG = Puffer[i][4:11]
            if Puffer[i][0:6] == "size1=":     SizeM = Puffer[i][6:8]
            if Puffer[i][0:6] == "size2=":     SizeL = Puffer[i][6:8]
            if Puffer[i][0:9] == "language=":  Gebiet = Puffer[i][9:11]
            if Puffer[i][0:7] == "player=":    pAktiv = int(Puffer[i][7:])    
            if Puffer[i][0:7] == "uagent=":    uaAktiv = int(Puffer[i][7:])    
            if Puffer[i][0:8] == "youtube=":   youtube_dl.set(int(Puffer[i][8:9])) 
            if Puffer[i][0:7] == "nowrap=":    Zeilenumbruch.set(int(Puffer[i][7:8]))    
            if Puffer[i][0:7] == "noprot=":    ProtMeldAus.set(int(Puffer[i][7:8]))    
            if Puffer[i][0:8] == "winchng=":   FensterAnders.set(int(Puffer[i][8:9]))    
            if Puffer[i][0:8] == "nocheck=":   PlayerPruefen.set(int(Puffer[i][8:9]))    
            if Puffer[i][0:7] == "expert=":    ExpertenModus.set(int(Puffer[i][7:8]))    

Schreibe_confDatei()                         # Neue Konfigurationsdatei schreiben  

TxT = Woerterbuch[Gebiet]                    # Zeiger auf aktuelle Sprache

Master.geometry(HauptGeo)                    # Hauptfenstergrösse und Position einstellen

if os.path.isfile(playerDatei):              # wenn Player-Datei existiert dann laden
    with open(playerDatei, "r", encoding="utf-8") as Datei:
        pListe.clear() 
        for Zeile in Datei:
            pListe.append(Zeile.rstrip())
        Datei.close()
else:                                        # sonst neue Player-Datei erstellen
    with open(playerDatei, "w", encoding="utf-8") as Datei:
        for i in range(len(pListe)):
            Datei.write(pListe[i] + "\n")
        Datei.close()

if os.path.isfile(uaDatei):                  # wenn User-Agent-Datei existiert dann laden
    with open(uaDatei, "r", encoding="utf-8") as Datei:
        uaListe.clear() 
        for Zeile in Datei:
            uaListe.append(Zeile.rstrip())
        Datei.close()
else:                                        # sonst neue User-Agent-Datei erstellen
    with open(uaDatei, "w", encoding="utf-8") as Datei:
        for i in range(len(uaListe)):
            Datei.write(uaListe[i] + "\n")
        Datei.close()

if os.path.isfile(cmdDatei):                 # wenn Kommandozeilen-Datei existiert dann laden
    with open(cmdDatei, "r", encoding="utf-8") as Datei:
        for i, Zeile in enumerate(Datei, 0):
            cmdxListe[i] = Zeile.rstrip()    # Kommandoliste Experten-Modus
        Datei.close()
else:                                        # sonst neue Kommandozeilen-Datei erstellen
    with open(cmdDatei, "w", encoding="utf-8") as Datei:
        for i in range(len(cmdListe)):
            cmdxListe[i] = cmdListe[i]       # Kommandoliste Experten-Modus
            Datei.write(cmdListe[i] + "\n")
        Datei.close()

if not os.path.isdir(m3uVerzeichnis):
    os.makedirs(m3uVerzeichnis)
if not os.path.isdir(recVerzeichnis):
    os.makedirs(recVerzeichnis)

if PlayerPruefen.get() == 0:
    if WINDOWS:
        if not os.path.isfile("c:/Program Files/ffmpeg/bin/ffmpeg.exe"):
            message.showwarning("Stream Recorder", "\n FFmpeg" + TxT["nicht gefunden"])
    else:
        if not os.path.isfile("/usr/bin/ffmpeg") and not os.path.isfile("/usr/local/bin/ffmpeg"):
            message.showwarning("Stream Recorder", "\n FFmpeg" + TxT["nicht gefunden"])

###############################################################################################################

def Datei_Oeffnen(event=None):

    global Puffer, m3uDatei, m3uMerker

    if not m3uMerker == "":
        m3uMerke2 = m3uDatei
        m3uDatei = fdialog.askopenfilename(initialdir=m3uVerzeichnis, filetypes=[("Playlists","*.m3u *.m3u8"),("Alle Dateien","*")])
        if m3uDatei == ():  m3uDatei = m3uMerke2
        else:               m3uMerker = m3uMerke2
    else:                                               # wenn m3uMerker == "" (nur einmal beim Programmstart)
        m3uDatei = m3uMerker = startDatei
        if not os.path.isfile(m3uDatei):                # wenn startDatei nicht existiert
            m3uDatei = m3uMerker = fdialog.askopenfilename(initialdir=m3uVerzeichnis, filetypes=[("Playlists","*.m3u *.m3u8"),("Alle Dateien","*")])

    if not m3uDatei == ():
        if os.path.isfile(m3uDatei):
            with open(m3uDatei, "r", encoding="utf-8") as Datei:
                Puffer.clear() 
                for Zeile in Datei:
                    if not (Zeile == "\n" or Zeile[0:11] == "#EXTVLCOPT:"):    # Leerzeile und User Agent überspringen
                        Puffer.append(Zeile)
                Datei.close()
            Alle_Anzeigen()

###############################################################################################################

def Datei_Bearbeiten(event=None):

    def Datei_Speichern(event):

        Datei = fdialog.asksaveasfile(parent=Fenster, mode="w", initialdir=m3uVerzeichnis, filetypes = [("Playlists","*.m3u *.m3u8"),("Alle Dateien","*")])
        if Datei:
            Datei.write(Text_Fenster.get("1.0", tk.END + "-1c"))     # ohne letztes LF !!
            Puffer.clear()
            with open(m3uDatei, "r", encoding="utf-8") as Datei:
                for Zeile in Datei:
                    if not (Zeile == "\n" or Zeile[0:11] == "#EXTVLCOPT:"):    # Leerzeile und User Agent überspringen
                        Puffer.append(Zeile)
                Datei.close()
            Alle_Anzeigen()
            Fenster.destroy()

    if not os.path.isfile(m3uDatei):
        message.showwarning("Stream Recorder", "\n" + m3uDatei + TxT["nicht gefunden"])
    else:
        Fenster = tk.Toplevel(Master)
        Fenster.title(m3uDatei)
        Fenster.wm_attributes("-topmost", True)
        Fenster.grab_set()

        Scroll_Vertikal = tk.Scrollbar(Fenster, width=14)
        Scroll_Horizont = tk.Scrollbar(Fenster, width=14, orient="horizontal")
        Text_Fenster = tk.Text(Fenster, width=120, height=34, pady=10, padx=10, yscrollcommand = Scroll_Vertikal.set, xscrollcommand = Scroll_Horizont.set)
        if Zeilenumbruch.get() == 1:  umbruch = "none"
        else                       :  umbruch = "char"
        Text_Fenster.config(foreground=FensterVG, background=FensterHG, font="Consolas 10", wrap=umbruch, undo="TRUE")
        Zeile_Info = tk.Label(Fenster, font="Helvetica 10", text=TxT["Datei speichern"])
        Scroll_Vertikal.config(command = Text_Fenster.yview)
        Scroll_Horizont.config(command = Text_Fenster.xview)
        Zeile_Info.pack(side="bottom", fill="x", padx=2, pady=0)
        Scroll_Vertikal.pack(side="right", fill="y", padx=1, pady=1)
        Scroll_Horizont.pack(side="bottom", fill="x", padx=1, pady=1)
        Text_Fenster.pack(fill="both", padx=2, pady=2, expand=True)
        with open(m3uDatei, "r", encoding="utf-8") as Datei:
            Text_Fenster.insert("1.0", Datei.read())
            Datei.close()

        Text_Fenster.focus_set()
        Text_Fenster.bind("<Control-Key-s>", Datei_Speichern)
        Text_Fenster.bind("<Double-Button-3>", Datei_Speichern)
        Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))


###############################################################################################################

def Listen_Loeschen():

    global PufNr, Name, Land, Sprache, Gruppe, URL

    PufNr.clear()
    Name.clear()
    Land.clear()
    Sprache.clear()
    Gruppe.clear()
    URL.clear()

###############################################################################################################

def Zeilenpuffer_Auswerten(i):

    global PufNr, Name, Land, Sprache, Gruppe, URL

    x = Puffer[i].find(",")
    if x == -1:
        Name.append("---")
    else:
        Name.append(Puffer[i][x+1:].rstrip())    # Namen (ohne LF)
    x = Puffer[i].find("tvg-country=")
    y = Puffer[i].find('"', x+13)
    if x == -1:
        Land.append("---")
    else:
        Land.append(Puffer[i][x+13:y])           # Land
    x = Puffer[i].find("tvg-language=")
    y = Puffer[i].find('"', x+14)
    if x == -1:
        Sprache.append("---")
    else:
        Sprache.append(Puffer[i][x+14:y])        # Sprache
    x = Puffer[i].find("group-title=")
    y = Puffer[i].find('"', x+13)
    if x == -1:
        Gruppe.append("---")
    else:
        Gruppe.append(Puffer[i][x+13:y])         # Gruppe

    URL.append(Puffer[i+1].rstrip())             # URL (ohne LF)

    PufNr.append(int((i+1)/2))                   # Nummer

###############################################################################################################

def Liste_Anzeigen(event=None):

    global StatusAnzahl

    Listen_Box.delete(0, tk.END) 
    for i in range(len(Name)):
        Listen_Box.insert(tk.END, "{:6d}    {:40.39s} {:8.7s} {:17.16s} {:14.14s}".format(PufNr[i], Name[i], Land[i], Sprache[i], Gruppe[i]))
    Listen_Box.selection_set(0)            # Scrollbalken auf ersten Eintrag setzen
    StatusAnzahl = len(Name)
    Statusleiste_Anzeigen("")

###############################################################################################################

def Listenende_Anzeigen():

    global StatusAnzahl

    Listen_Box.delete(0, tk.END) 
    for i in range(len(Name)):
        Listen_Box.insert(tk.END, "{:6d}    {:40.39s} {:8.7s} {:17.16s} {:14.14s}".format(PufNr[i], Name[i], Land[i], Sprache[i], Gruppe[i]))
    Listen_Box.activate("end")
    Listen_Box.selection_set("end")        # Scrollbalken auf letzten Eintrag setzen
    Listen_Box.see("end")
    StatusAnzahl = len(Name)
    Statusleiste_Anzeigen("")
    return "break"                         # eingebautes <Ende> in tk.Listbox verhindern

###############################################################################################################

def Alle_Anzeigen(event=None):

    global Suchbereich, Suchbegriff

    Listen_Loeschen()
    for i in range(1, len(Puffer)-1, 2):
        Zeilenpuffer_Auswerten(i)
    Liste_Anzeigen()
    Suchbereich = 0
    Suchbegriff = ""

###############################################################################################################

def Suche_Namen():

    def Namen_Anzeigen(event=None):

        global Suchbereich, Suchbegriff

        Suchbegriff = Eingabefeld.get()
        Suchbereich = 1
        Fenster.destroy()
        Listen_Loeschen()
        for i in range(1, len(Puffer)-1, 2):
            x = Puffer[i].find(",")
            if Suchbegriff.lower() in Puffer[i][x+1:].rstrip().lower():
                Zeilenpuffer_Auswerten(i)
        Liste_Anzeigen()

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Suchen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    Fenstertext = tk.Label(Fenster, text=TxT["Begriff eingeben"], font="Helvetica 12")
    Eingabefeld = tk.Entry(Fenster, bd=4, width=15, font="Helvetica 11")
    Fenstertext.pack(pady=20)
    Eingabefeld.pack(padx=50)
    tk.Label(Fenster).pack(pady=8)
    Eingabefeld.focus_set()
    Eingabefeld.bind("<Return>", Namen_Anzeigen)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Suche_Sender(b):

    def Sender_Anzeigen(event=None):

        global Suchbereich, Suchbegriff

        if b == 2:
            Suchbegriff = ZeichenLand.get()
            Suchstelle = "tvg-country="
        else:
            Suchbegriff = ZeichenGruppe.get()
            Suchstelle = "group-title="
        Suchbereich = b
        Fenster.destroy()
        Listen_Loeschen()
        for i in range(1, len(Puffer)-1, 2):
            x = Puffer[i].find(Suchstelle)
            y = Puffer[i].find('"', x+13)
            if Puffer[i][x+13:y].find(Suchbegriff) != -1:
                Zeilenpuffer_Auswerten(i)
        Liste_Anzeigen()

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Suchen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    if b == 2:    FensterMenu = tk.OptionMenu(Fenster, ZeichenLand, *cListe, command=Sender_Anzeigen)
    else:         FensterMenu = tk.OptionMenu(Fenster, ZeichenGruppe, *gListe, command=Sender_Anzeigen)
    FensterMenu.config(bd=3, width=13, font="Helvetica 11")
    Fenstertext = tk.Label(Fenster, text=TxT["Begriff auswählen"], font="Helvetica 12")
    Fenstertext.pack(pady=20)
    FensterMenu.pack(padx=50)
    tk.Label(Fenster).pack(pady=8)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Suche_Speichern():

    def Datei_Speichern(event=None):

        with open(Eingabefeld.get(), "w", encoding="utf-8") as Datei:
            Datei.write("#EXTM3U\n")
            for i in range(1, len(Puffer)-1, 2):
                if Suchbereich == 1:                    # nach Namen durchsuchen
                    x = Puffer[i].find(",")
                    if Suchbegriff in Puffer[i][x+1:].rstrip():
                        Datei.write(Puffer[i])
                        Datei.write(Puffer[i+1])
                if Suchbereich == 2:                    # nach Land durchsuchen
                    x = Puffer[i].find("tvg-country=")
                    y = Puffer[i].find('"', x+13)
                    if Puffer[i][x+13:y] == Suchbegriff:
                        Datei.write(Puffer[i])
                        Datei.write(Puffer[i+1])
                if Suchbereich == 3:                    # nach Gruppe durchsuchen
                    x = Puffer[i].find("group-title=")
                    y = Puffer[i].find('"', x+13)
                    if Puffer[i][x+13:y] == Suchbegriff:
                        Datei.write(Puffer[i])
                        Datei.write(Puffer[i+1])
            Datei.close()
        Fenster.destroy()


    if Suchbereich == 0:
        message.showwarning(TxT["Suchen"], "\n" + TxT["kein Suchfilter"])
    else:
        Fenster = tk.Toplevel(Master)
        Fenster.title(TxT["Suchen"])
        Fenster.wm_attributes("-topmost", True)
        Fenster.grab_set()

        Fenstertext = tk.Label(Fenster, text=TxT["Sender speichern"], font="Helvetica 12")
        Eingabefeld = tk.Entry(Fenster, bd=4, width=52, font="Helvetica 11")
        ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Speichern"], font="Helvetica 11", command=Datei_Speichern)
        ButtonAbbrechen = tk.Button(Fenster, bd=3, text=TxT["Abbrechen"], font="Helvetica 11", command=Fenster.destroy)
        Fenstertext.pack(pady=20)
        Eingabefeld.pack(padx= 40)
        ButtonSpeichern.pack(pady=20, ipadx=23, expand=True, side="left", padx=40)
        ButtonAbbrechen.pack(pady=20, ipadx=20, expand=True, side="left", anchor="w")

        dName = os.path.basename(m3uDatei)              # Vorgabe für Dateinamen erstellen
        Basis = os.path.splitext(dName)[0]
        m3uNeu = m3uVerzeichnis + Basis + "_" + Suchbegriff + ".m3u"

        Eingabefeld.insert(0, m3uNeu)
        Eingabefeld.focus_set()
        Eingabefeld.bind("<Return>", Datei_Speichern)
        ButtonSpeichern.bind("<Return>", Datei_Speichern)
        ButtonAbbrechen.bind("<Return>", lambda event: Fenster_Schliessen(Fenster))
        Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Favoriten_Anzeigen(event=None):

    global Puffer, m3uDatei, m3uMerker
    
    if not os.path.isfile(m3uVerzeichnis + "favoriten.m3u"):
        message.showwarning("Stream Recorder", "\n" + m3uVerzeichnis + "favoriten.m3u" + TxT["nicht gefunden"])
    else:
        if not m3uDatei == m3uVerzeichnis + "favoriten.m3u":    
            m3uMerker = m3uDatei
        m3uDatei = m3uVerzeichnis + "favoriten.m3u"
        Puffer.clear()
        with open(m3uDatei, "r", encoding="utf-8") as Datei:
            for Zeile in Datei:
                if not (Zeile == "\n" or Zeile[0:11] == "#EXTVLCOPT:"):    # Leerzeile und User Agent überspringen
                    Puffer.append(Zeile)
            Datei.close()
        Alle_Anzeigen()

###############################################################################################################

def Favoriten_Hinzufuegen(event=None):

    if Listen_Box.curselection():
        Nr = Listen_Box.curselection()[0]           # Index des markierten Senders
        i = PufNr[Nr]                               # Sendernummer laden (Pufferposition * 2 - 1)
        FavName = m3uVerzeichnis + "favoriten.m3u"
        if not os.path.isfile(FavName):             # wenn Favoriten-Datei nicht existiert
            with open(FavName, "w", encoding="utf-8") as Datei:
                Datei.write("#EXTM3U\n")            #  dann 1. Zeile schreiben (Dateikennung)
                Datei.close()
        with open(FavName, "a", encoding="utf-8") as Datei:    # 2 Zeilen an favoriten.m3u anhängen
            Datei.write(Puffer[i*2-1])              #  Beschreibung  
            Datei.write(Puffer[i*2])                #  URL
            Datei.close()

        Fenster = tk.Toplevel(Master)               # Meldefenster 2 Sek. anzeigen
        Fenster.title(TxT["Favoriten"])
        Fenster.wm_attributes("-topmost", True)
        Fenster.grab_set()
        Fenstertext = tk.Label(Fenster, text=Name[Nr] + TxT["hinzu"], font="Helvetica 12")
        Fenstertext.pack(ipadx=50, pady=30)
        Fenster.after(2000, Fenster.destroy)

###############################################################################################################

def Favoriten_Bearbeiten(event=None):

    def Eintrag_Speichern(event=None):
  
        i = PufNr[Nr]                               # Puffer "#EXTINF" Zeile = PufNr * 2 - 1
        Name[i-1] = EingabeName.get()
        Land[i-1] = EingabeLand.get()
        Sprache[i-1] = EingabeSprache.get()
        Gruppe[i-1] = EingabeGruppe.get()
        Puffer[i*2-1] = '#EXTINF:-1 tvg-country="' + EingabeLand.get() + '" tvg-language="' + EingabeSprache.get() + \
                        '" group-title="' + EingabeGruppe.get() + '",' + EingabeName.get() + '\n'

        FavName = m3uVerzeichnis + "favoriten.m3u"
        with open(FavName, "w", encoding="utf-8") as Datei:    # Favoriten-Datei neu schreiben (überschreiben)
            for i in range(0, len(Puffer)):
                Datei.write(Puffer[i])
            Datei.close()
        Favoriten_Anzeigen()
        Listen_Box.selection_clear(0)
        Listen_Box.selection_set(Nr)
        Listen_Box.activate(Nr)
        Listen_Box.see(Nr)
        Fenster.destroy()


    if Listen_Box.curselection():
        Nr = Listen_Box.curselection()[0]           # Index des markierten Senders
    else:
        message.showwarning(TxT["Favoriten"], "\n" + TxT["Kein Sender"])
        return
 
    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Favoriten"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()
    
    TextName =    tk.Label(Fenster, text="Name:", font="Helvetica 11")
    TextGruppe =  tk.Label(Fenster, text=TxT["Gruppe"], font="Helvetica 11")
    TextLand =    tk.Label(Fenster, text=TxT["Land"], font="Helvetica 11")
    TextSprache = tk.Label(Fenster, text=TxT["Sprache"], font="Helvetica 11")
    EingabeName =    tk.Entry(Fenster, bd=3, width=53, font="Helvetica 11")
    EingabeGruppe =  tk.Entry(Fenster, bd=3, width=11, font="Helvetica 11")
    EingabeLand =    tk.Entry(Fenster, bd=3, width=4, font="Helvetica 11")
    EingabeSprache = tk.Entry(Fenster, bd=3, width=12, font="Helvetica 11")
    ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Speichern"], font="Helvetica 11", command=Eintrag_Speichern)
    ButtonAbbrechen = tk.Button(Fenster, bd=3, text=TxT["Abbrechen"], font="Helvetica 11", command=Fenster.destroy)

    tk.Label(Fenster).grid(row=0, column=0)
    TextName.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    EingabeName.grid(row=1, column=2, columnspan=5, padx=1, pady=10, sticky="w")
    tk.Label(Fenster).grid(row=1, column=7, padx=15)
    TextGruppe.grid(row=2, column=1, padx=20, pady=6, sticky="w")
    EingabeGruppe.grid(row=2, column=2, padx=1, pady=6)
    TextLand.grid(row=2, column=3, padx=20, pady=6, sticky="w")
    EingabeLand.grid(row=2, column=4, padx=1, pady=6)
    TextSprache.grid(row=2, column=5, padx=20, pady=6, sticky="w")
    EingabeSprache.grid(row=2, column=6, padx=1, pady=6)
    ButtonSpeichern.grid(row=4, column=2, columnspan=3, pady=12, ipadx=23, sticky="w")
    ButtonAbbrechen.grid(row=4, column=4, columnspan=3, pady=12, ipadx=20)
    tk.Label(Fenster).grid(row=5, column=0)

    i = PufNr[Nr]                                   # Puffer "#EXTINF" Zeile = PufNr * 2 - 1
    EingabeGruppe.insert(0, Gruppe[i-1])
    EingabeLand.insert(0, Land[i-1])
    EingabeSprache.insert(0, Sprache[i-1])
    EingabeName.insert(0, Name[i-1])
    EingabeName.select_range(0, tk.END)
    EingabeName.focus_set()

    ButtonSpeichern.bind("<Return>", Eintrag_Speichern)
    ButtonAbbrechen.bind("<Return>", lambda event: Fenster_Schliessen(Fenster))
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Favoriten_Entfernen(event=None):

    global Puffer

    if Listen_Box.curselection() and os.path.basename(m3uDatei) == "favoriten.m3u":
        Nr = Listen_Box.curselection()[0]           # Index des markierten Senders
        if message.askyesno("Stream Recorder", "\n" + Name[Nr] + TxT["wirklich entfernen"]):
            Puffer.pop(Nr*2+2)                      # URL löschen
            Puffer.pop(Nr*2+1)                      # Beschreibung löschen
            with open(m3uDatei, "w", encoding="utf-8") as Datei:    # Favoriten-Datei neu schreiben (überschreiben)
                for i in range(0, len(Puffer)):
                    Datei.write(Puffer[i])
                Datei.close()
            Alle_Anzeigen()
            Listen_Box.selection_clear(0)
            Listen_Box.selection_set(Nr)            # Scrollbalken einen Eintrag weiter
            Listen_Box.activate(Nr)
            Listen_Box.see(Nr)
            Listen_Box.index(0)

###############################################################################################################

def Favoriten_Eingeben(event=None):

    def Eintrag_Hinzufuegen(event=None):

        FavName = m3uVerzeichnis + "favoriten.m3u"
        if not os.path.isfile(FavName):             # wenn keine Favoriten-Datei gefunden
            with open(FavName, "w", encoding="utf-8") as Datei:
                Datei.write("#EXTM3U\n")            # 1.Zeile schreiben (Header)
                Datei.close()
        with open(FavName, "a", encoding="utf-8") as Datei:
            Datei.write('#EXTINF:-1 tvg-country="' + EingabeLand.get())    #  Land  
            Datei.write('" tvg-language="' + EingabeSprache.get())         #  Sprache  
            Datei.write('" group-title="' + EingabeGruppe.get())           #  Gruppe  
            Datei.write('",' + EingabeName.get())                          #  Name  
            Datei.write('\n' + EingabeLink.get() + '\n')                   #  URL
            Datei.close()
        Favoriten_Anzeigen()
        Listenende_Anzeigen()
        Fenster.destroy()


    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Favoriten"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    TextName =    tk.Label(Fenster, text="Name:", font="Helvetica 11")
    TextGruppe =  tk.Label(Fenster, text=TxT["Gruppe"], font="Helvetica 11")
    TextLand =    tk.Label(Fenster, text=TxT["Land"], font="Helvetica 11")
    TextSprache = tk.Label(Fenster, text=TxT["Sprache"], font="Helvetica 11")
    TextLink =    tk.Label(Fenster, text="Link:", font="Helvetica 11")
    EingabeName =    tk.Entry(Fenster, bd=3, width=53, font="Helvetica 11")
    EingabeGruppe =  tk.Entry(Fenster, bd=3, width=11, font="Helvetica 11")
    EingabeLand =    tk.Entry(Fenster, bd=3, width=4, font="Helvetica 11")
    EingabeSprache = tk.Entry(Fenster, bd=3, width=12, font="Helvetica 11")
    EingabeLink =    tk.Entry(Fenster, bd=3, width=53, font="Helvetica 11")
    ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Speichern"], font="Helvetica 11", command=Eintrag_Hinzufuegen)
    ButtonAbbrechen = tk.Button(Fenster, bd=3, text=TxT["Abbrechen"], font="Helvetica 11", command=Fenster.destroy)

    tk.Label(Fenster).grid(row=0, column=0)
    TextName.grid(row=1, column=1, padx=20, pady=10, sticky="w")
    EingabeName.grid(row=1, column=2, columnspan=5, padx=1, pady=10, sticky="w")
    tk.Label(Fenster).grid(row=1, column=7, padx=15)
    TextGruppe.grid(row=2, column=1, padx=20, pady=6, sticky="w")
    EingabeGruppe.grid(row=2, column=2, padx=1, pady=6)
    TextLand.grid(row=2, column=3, padx=20, pady=6, sticky="w")
    EingabeLand.grid(row=2, column=4, padx=1, pady=6)
    TextSprache.grid(row=2, column=5, padx=20, pady=6, sticky="w")
    EingabeSprache.grid(row=2, column=6, padx=1, pady=6)
    TextLink.grid(row=3, column=1, padx=20, pady=10, sticky="w")
    EingabeLink.grid(row=3, column=2, columnspan=5, padx=1, pady=10, sticky="w")
    ButtonSpeichern.grid(row=4, column=2, columnspan=3, pady=6, ipadx=23, sticky="w")
    ButtonAbbrechen.grid(row=4, column=4, columnspan=3, pady=6, ipadx=20)
    tk.Label(Fenster).grid(row=5, column=0)

    EingabeName.insert(0, TxT["Unbenannt"])
    EingabeName.select_range(0, tk.END)
    EingabeName.focus_set()
    EingabeLink.insert(0, "https://")
    ButtonSpeichern.bind("<Return>", Eintrag_Hinzufuegen)
    ButtonAbbrechen.bind("<Return>", lambda event: Fenster_Schliessen(Fenster))
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Favoriten_Zurueck(event=None):

    global Puffer, m3uDatei, m3uMerker

    aktuelle = m3uDatei             # aktuelle Datei merken
    m3uDatei = m3uMerker            # vorherige Datei neu laden
    m3uMerker = aktuelle

    if os.path.isfile(m3uDatei):
        with open(m3uDatei, "r", encoding="utf-8") as Datei:
            Puffer.clear()
            for Zeile in Datei:
                if not (Zeile == "\n" or Zeile[0:11] == "#EXTVLCOPT:"):    # Leerzeile und User Agent überspringen
                    Puffer.append(Zeile)
            Datei.close()
        Alle_Anzeigen()

###############################################################################################################

def Favoriten_Hochschieben(event=None):

    if Listen_Box.curselection() and os.path.basename(m3uDatei) == "favoriten.m3u":

        Nr = Listen_Box.curselection()[0]           # Index des markierten Senders
        if Nr >= 1:
            i = PufNr[Nr]                           # Sendernummer laden (Pufferposition * 2 - 1)
            Puffer[i*2-3], Puffer[i*2-1] = Puffer[i*2-1], Puffer[i*2-3]
            Puffer[i*2-2], Puffer[i*2] = Puffer[i*2], Puffer[i*2-2]

            with open(m3uDatei, "w", encoding="utf-8") as Datei:    # Favoriten.m3u neu schreiben
                for i in range(0, len(Puffer), 1):
                    Datei.write(Puffer[i])
                Datei.close()

            Favoriten_Anzeigen()
            Listen_Box.selection_clear(0)
            Listen_Box.selection_set(Nr-1)          # Scrollbalken eine Zeile zurück
            Listen_Box.activate(Nr-1)
            Listen_Box.see(Nr-1)

    return "break"                                      # eingebautes <Alt-Hoch> in tk.Listbox verhindern

###############################################################################################################

def Favoriten_Runterschieben(event=None):

    if Listen_Box.curselection() and os.path.basename(m3uDatei) == "favoriten.m3u":

        Nr = Listen_Box.curselection()[0]           # Index des markierten Senders
        if Nr < len(Puffer)/2-2:
            i = PufNr[Nr]                           # Sendernummer laden (Pufferposition * 2 - 1)
            Puffer[i*2+2], Puffer[i*2] = Puffer[i*2], Puffer[i*2+2]
            Puffer[i*2+1], Puffer[i*2-1] = Puffer[i*2-1], Puffer[i*2+1]

            with open(m3uDatei, "w", encoding="utf-8") as Datei:    # Favoriten.m3u neu schreiben
                for i in range(0, len(Puffer), 1):
                    Datei.write(Puffer[i])
                Datei.close()

            Favoriten_Anzeigen()
            Listen_Box.selection_clear(0)
            Listen_Box.selection_set(Nr+1)          # Scrollbalken auf nächste Zeile
            Listen_Box.activate(Nr+1)
            Listen_Box.see(Nr+1)

    return "break"                                      # eingebautes <Alt-Runter> in tk.Listbox verhindern

###############################################################################################################

def Player_Auswaehlen(event=None):

    def Player_Laden(event):

        global pAktiv

        Nr = int(Player_Liste.curselection()[0])         # Index pListe
        if PlayerPruefen.get() == 1:                     # wenn keine Prüfung
            pAktiv = Nr                                  # neuer aktiver Player-Index
            Schreibe_confDatei()
            Fenster.destroy()
        else:
            if WINDOWS:
                x = pListe[Nr][25:].find('"')
                player = pListe[Nr][25:25+x]             # Programmpfad des Player
                if os.path.isfile(player):    gefunden = True
                else:                         gefunden = False
            else:
                x = pListe[Nr][24:].find(' ')
                player = pListe[Nr][24:24+x]             # Programmname des Player
                if os.path.isfile("/usr/bin/" + player) or os.path.isfile("/usr/local/bin/" + player):    gefunden = True
                else:                                                                                     gefunden = False

            if gefunden:
                pAktiv = Nr                              # neuer aktiver Player-Index
                Schreibe_confDatei()
                Fenster.destroy()
            else:
                message.showwarning("Stream Recorder", "\n " + player + TxT["nicht gefunden"], parent=Fenster)
                Player_Liste.selection_clear(Nr)
                Player_Liste.selection_set(pAktiv)       # Scrollbalken auf aktiven Player
                Player_Liste.activate(pAktiv)

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Player"])
    Fenster.wm_attributes("-topmost", True)
    #Fenster.wait_visibility()
    time.sleep(0.3)                                      # grab failed (rechte Maustaste!!)
    Fenster.grab_set()

    Player_Liste = tk.Listbox(Fenster, width=25, height=18, selectborderwidth=2)
    Player_Liste.config(foreground=FensterVG, background=FensterHG, font="Helvetica 11")
    Player_Liste.pack(fill="both", padx=3, pady=3, expand=True)
    Player_Liste.delete(0, tk.END) 
    for i in range(len(pListe)):
        Player_Liste.insert(tk.END, "    " + pListe[i][0:24])
    Player_Liste.selection_set(pAktiv)                   # Scrollbalken auf aktiven Player
    Player_Liste.activate(pAktiv)
    Player_Liste.focus_set()
    Player_Liste.bind("<Return>", Player_Laden)
    Player_Liste.bind("<Double-Button-1>", Player_Laden)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def User_Agent_Aendern(event=None):

    def UserAgent_Laden(event):

        global uaAktiv

        Nr = int(UserAgent_Liste.curselection()[0])      # Index uaListe
        uaAktiv = Nr                                     # neuer aktiver UserAgent-Index
        Schreibe_confDatei()
        Fenster.destroy()

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["UserAgent"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    UserAgent_Liste = tk.Listbox(Fenster, width=31, height=26, selectborderwidth=2)
    UserAgent_Liste.config(foreground=FensterVG, background=FensterHG, font="Helvetica 11")
    UserAgent_Liste.pack(fill="both", padx=3, pady=3, expand=True)
    UserAgent_Liste.delete(0, tk.END) 
    for i in range(len(uaListe)):
        UserAgent_Liste.insert(tk.END, "    " + uaListe[i][0:30])
    UserAgent_Liste.selection_set(uaAktiv)               # Scrollbalken auf aktiven User-Agent
    UserAgent_Liste.activate(uaAktiv)
    UserAgent_Liste.focus_set()
    UserAgent_Liste.bind("<Return>", UserAgent_Laden)
    UserAgent_Liste.bind("<Double-Button-1>", UserAgent_Laden)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Download_Manager(event=None):

    def Kommando_Speichern(event=None):

        if ExpertenModus.get() == 1:
            for i in range(len(cmdxListe)):              # Kommando-Liste neu laden
                cmdxListe[i] = EingabeZeile[i].get()
            with open(cmdDatei, "w", encoding="utf-8") as Datei:    # Kommando-Datei neu schreiben
                for i in range(9):
                    Datei.write(EingabeZeile[i].get() + "\n")
                Datei.close()

        Schreibe_confDatei()                             # youtube_dl speichern (aktive Kommandozeile)
        Fenster.destroy()


    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Manager"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    if ExpertenModus.get() == 1:
        Fenster.geometry("630x380")    
        EingabeZeile1 = tk.Entry(Fenster, bd=3, width=130, font="Helvetica 11")
        EingabeZeile2 = tk.Entry(Fenster, bd=3, width=130, font="Helvetica 11")
        EingabeZeile3 = tk.Entry(Fenster, bd=3, width=130, font="Helvetica 11")
        EingabeZeile4 = tk.Entry(Fenster, bd=3, width=130, font="Helvetica 11")
        EingabeZeile5 = tk.Entry(Fenster, bd=3, width=130, font="Helvetica 11")
        EingabeZeile6 = tk.Entry(Fenster, bd=3, width=130, font="Helvetica 11")
        EingabeZeile7 = tk.Entry(Fenster, bd=3, width=130, font="Helvetica 11")
        EingabeZeile8 = tk.Entry(Fenster, bd=3, width=130, font="Helvetica 11")
        EingabeZeile9 = tk.Entry(Fenster, bd=3, width=130, font="Helvetica 11")
        EingabeZeile = [EingabeZeile1, EingabeZeile2, EingabeZeile3, EingabeZeile4, EingabeZeile5, EingabeZeile6, EingabeZeile7, EingabeZeile8, EingabeZeile9]

        tk.Label(Fenster).grid(row=0,column=0, pady=1)
        for i in range(9):
            tk.Label(Fenster).grid(row=i+1,column=0, padx=6, pady=6)
            tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=youtube_dl, value=i).grid(row=i+1, column=1, padx=7)
            tk.Label(Fenster, text=str(i+1), font="Helvetica 9").grid(row=i+1,column=2, ipadx=5)
            EingabeZeile[i].grid(row=i+1, column=3, padx=0)
            EingabeZeile[i].insert(0, cmdxListe[i][0:])
            tk.Label(Fenster).grid(row=i+1,column=4, padx=9)
        Fenster.grid_columnconfigure(3, weight=1, minsize=480)    # Breite Eingabefeld flexibel machen
        x1, x2 = 110, 30    # Button X-Position und Breite
    else:
        if youtube_dl.get() > 2:    youtube_dl.set(0)
        RadioZeile1 = tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=2, variable=youtube_dl, value=2)
        RadioZeile2 = tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=2, variable=youtube_dl, value=1)
        RadioZeile3 = tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=2, variable=youtube_dl, value=0)
        RadioZeile = [RadioZeile1, RadioZeile2, RadioZeile3]
        TextZeile1 = tk.Label(Fenster, text="yt-dlp" + TxT["einbinden als"], font="Helvetica 11")
        TextZeile2 = tk.Label(Fenster, text="youtube-dl" + TxT["einbinden als"], font="Helvetica 11")
        TextZeile3 = tk.Label(Fenster, text=TxT["einbinden keinen"], font="Helvetica 11")
        TextZeile = [TextZeile1, TextZeile2, TextZeile3]

        tk.Label(Fenster).grid(row=0,column=0, pady=2)
        for i in range(3):
            tk.Label(Fenster).grid(row=i+1,column=0, padx=5, pady=6)
            RadioZeile[i].grid(row=i+1, column=1, padx=25, pady=6)
            TextZeile[i].grid(row=i+1, column=2, padx=0, pady=6,sticky="w")
            tk.Label(Fenster).grid(row=i+1,column=3, padx=15, pady=6)
        x1, x2 = 48, 17    # Button X-Position und Breite

    ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Speichern"], font="Helvetica 11", command=Kommando_Speichern)
    ButtonAbbrechen = tk.Button(Fenster, bd=3, text=TxT["Abbrechen"], font="Helvetica 11", command=Fenster.destroy)
    ButtonSpeichern.grid(row=10, column=0, padx=x1, pady=15, ipadx=x2+3, columnspan=5,sticky="w")
    ButtonAbbrechen.grid(row=10, column=0, padx=x1, pady=15, ipadx=x2, columnspan=5,sticky="e")
    ButtonSpeichern.bind("<Return>", Kommando_Speichern)
    ButtonAbbrechen.bind("<Return>", lambda event: Fenser_Schliessen(Fenster))
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Stream_Anschauen(event=None):

    global altName, altLink, altPos

    if Listen_Box.curselection():
        Nr = Listen_Box.curselection()[0]                  # Index des markierten Senders
        cmdStrg = pListe[pAktiv][24:].replace("URL[Nr]", URL[Nr])    # Kommandostring zusammenbauen
        cmdStrg = cmdStrg.replace("uagent", uaListe[uaAktiv][30:])   # User-Agent in Kommandozeile einbauen
        try:                                               # URL prüfen
            urllib.request.urlopen(urllib.request.Request(URL[Nr], headers={"User-Agent": uaListe[uaAktiv][30:]}), timeout=5)
        except urllib.error.HTTPError as err:
            meldung = str(err.code) + ":  " + str(err.reason)
            Statusleiste_Anzeigen(meldung)
        except urllib.error.URLError as err:
            meldung = str(err.reason)
            Statusleiste_Anzeigen(meldung)
        except:
            Statusleiste_Anzeigen("Unexpected error")
        else:                                              # wenn URL gültig
            Statusleiste_Anzeigen(Name[Nr])
            proc = subprocess.Popen(cmdStrg, shell=True)   # Player starten
            altName.append(Name[Nr])                       # History speichern
            altLink.append(URL[Nr])
            altPos = len(altName)-1
            Master.focus_force()
            Listen_Box.focus_set()                         # Focus zurück auf Programmliste

###############################################################################################################

def Stream_Aufnehmen(event=None):

    def protDatei_Schreiben(text, name):

        if not ProtMeldAus.get():  
            with open(protDatei, "a", encoding="utf-8") as Datei:
                Datei.write(time.strftime("%d.%m.%y %H:%M > ") + text +  name + "\n")
                Datei.close()

    global recPID, recStart, recEnde, recName, StatusAufnahmen, StatusFehler

    if Listen_Box.curselection():
        Nr = Listen_Box.curselection()[0]                  # Index des markierten Senders
        try:                                               # URL prüfen
            urllib.request.urlopen(urllib.request.Request(URL[Nr], headers={"User-Agent": uaListe[uaAktiv][30:]}), timeout=5)
        except urllib.error.HTTPError as err:
            StatusFehler += 1
            meldung = str(err.code) + ":  " + str(err.reason)
            Statusleiste_Anzeigen(meldung)
            protmeld = "HTTP error: " + str(err.code) + "        - "
            protDatei_Schreiben(protmeld, Name[Nr])
        except urllib.error.URLError as err:
            StatusFehler += 1
            meldung = str(err.reason)
            Statusleiste_Anzeigen(meldung)
            protDatei_Schreiben("URL error: " + meldung[0:11].ljust(11) + " - ", Name[Nr])
        except:
            StatusFehler += 1
            Statusleiste_Anzeigen("Unexpected error")
            protDatei_Schreiben("Unexpected error       - ", Name[Nr])
        else:                                              # wenn URL gültig
            Statusleiste_Anzeigen(Name[Nr])
            for n in range(1, 1000):                       # Namen der Aufnahme festlegen (..._001 bis ..._999)
                Dateiname = Name[Nr] + "_" + str(n).zfill(3) + ".ts" 
                if not os.path.isfile(recVerzeichnis + Dateiname):   break   # wenn Dateiname nicht existiert dann übernehmen

            if ExpertenModus.get() == 1:
                cmdStrg = cmdxListe[youtube_dl.get()][0:]
            else:          # Standard-Modus
                if youtube_dl.get() > 2:    youtube_dl.set(0)
                cmdStrg = cmdListe[youtube_dl.get()][0:]

            cmdStrg = cmdStrg.replace("link", URL[Nr])                        # Link der Aufnahme in Kommandozeile einbauen
            cmdStrg = cmdStrg.replace("uagent", uaListe[uaAktiv][30:])        # User-Agent in Kommandozeile einbauen
            cmdStrg = cmdStrg.replace("file", recVerzeichnis + Dateiname)     # Namen der Aufnahme in Kommandozeile einbauen
            print(cmdStrg)

            if WINDOWS:    proc = subprocess.Popen(cmdStrg, shell=True)
            else:          proc = subprocess.Popen(cmdStrg, shell=True, preexec_fn=os.setsid)
            #print(proc.pid)

            if proc.pid:
                recPID.append(proc.pid)                  # Aufnahme: PID speichern     
                recStart.append(time.strftime("%H%M"))   # Aufnahme: Startzeit speichern                          
                recEnde.append("9999")                   # Aufnahme: Endezeit speichern                          
                recName.append(Name[Nr])                 # Aufnahme: Namen speichern
                StatusAufnahmen = len(recPID)
                Statusleiste_Anzeigen(Name[Nr])
                protDatei_Schreiben("[" + str(youtube_dl.get()+1) + "] " + TxT["Gestartet Benutzer"], Name[Nr])

###############################################################################################################

def Aufnahme_Stoppen(event=None):

    def Aufnahme_Beenden(event):

        global recPID, recStart, recEnde, recName, StatusAufnahmen, StatusBeendete

        if Record_Liste.curselection():
            Nr = int(Record_Liste.curselection()[0])     # Index Aufnahmeliste
            Kill_PID(Nr, 1)
            recPID.pop(Nr)                               # Aufnahme: PID löschen
            recStart.pop(Nr)                             # Aufnahme: Startzeit löschen
            recEnde.pop(Nr)                              # Aufnahme: Endezeit löschen
            recName.pop(Nr)                              # Aufnahme: Namen löschen
            Record_Liste.delete(Nr)                      # Listeneintrag löschen
            StatusAufnahmen = len(recPID)
            StatusBeendete += 1
            Statusleiste_Anzeigen("")

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Laufende Aufnahmen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()
    Zeile_Titel = tk.Label(Fenster, anchor="w", text="PID       Start      Stop       Name", font="Helvetica 11")
    Record_Liste = tk.Listbox(Fenster, width=60, height=15)
    Record_Liste.config(foreground=FensterVG, background=FensterHG, font="Consolas 10")
    Zeile_Info = tk.Label(Fenster, font="Helvetica 10", text=TxT["Aufnahme stoppen"])
    Zeile_Info.pack(side="bottom", fill="x", padx=3, pady=2)
    Zeile_Titel.pack(side="top", fill="x", padx=22, pady=2)
    Record_Liste.pack(fill="both", padx=3, pady=1, expand=True)

    if len(recName) > 0:                                 # wenn mind. 1 Aufnahme
        Record_Liste.delete(0, tk.END) 
        for i in range(len(recName)):
            Record_Liste.insert(tk.END, "{:6d} - {:4s} - {:4s} - {:40s}".format(recPID[i], recStart[i], recEnde[i], recName[i]))
        Record_Liste.selection_set(0)
        Record_Liste.focus_set()                          # Markierung auf ersten Eintrag setzen
        Record_Liste.bind("<Return>", Aufnahme_Beenden)
        Record_Liste.bind("<Double-Button-1>", Aufnahme_Beenden)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Kill_PID(i, b):

    if WINDOWS:
        try:
            subprocess.Popen("taskkill /F /PID  {pid} /T".format(pid=recPID[i]))
        except:
            pass
    else: 
        try:
            os.killpg(int(recPID[i]), signal.SIGTERM)
        except:
            pass
    if not ProtMeldAus.get():  
        with open(protDatei, "a", encoding="utf-8") as Datei:
            if b == 1:    MeldeText = TxT["Beendet Benutzer"]
            else:         MeldeText = TxT["Beendet Timer"]
            Datei.write(time.strftime("%d.%m.%y %H:%M > ") + MeldeText + recName[i] + "\n")
            Datei.close()

###############################################################################################################

def Alle_Beenden():

    global recPID, recStart, recEnde, recName, StatusAufnahmen, StatusBeendete

    if message.askyesno("Stream Recorder", "\n" + TxT["wirklich beenden"]):
        for i in range(len(recPID)):
            Kill_PID(i, 1)
        StatusAufnahmen = 0
        StatusBeendete += len(recPID)
        Statusleiste_Anzeigen("")
        recPID.clear()
        recStart.clear()
        recEnde.clear()
        recName.clear()

###############################################################################################################

def Schedule_Starten():

    def protDatei_Schreiben(text, name):

        if not ProtMeldAus.get():  
            with open(protDatei, "a", encoding="utf-8") as Datei:
                Datei.write(time.strftime("%d.%m.%y %H:%M > ") + text +  name + "\n")
                Datei.close()

    global sPuffer, recPID, recStart, recEnde, recName, StatusAufnahmen, StatusBeendete, StatusFehler

    sPuffer.clear()     # Schedule-Puffer löschen   (1. Zeile = Tage + Start + Ende + Rec + * + Name + LF  /  2. Zeile = URL + LF)

    if os.path.isfile(schedDatei):
        with open(schedDatei, "r", encoding="utf-8") as Datei:            # Schedule-Datei in Puffer laden
            for Zeile in Datei:
                    sPuffer.append(Zeile)
            Datei.close()

    #---------- Nächste Aufnahme(n) starten ----------

    Aktuelle = int(time.strftime("%H%M"))                                 # aktuelle Uhrzeit holen (SSMM)
    w = datetime.datetime.today().weekday()                               # aktuellen Wochentag holen (0-6)

    for i in range(len(sPuffer)-2, -2, -2):                               # vom Ende her durchsuchen!!
        Startzeit = int(sPuffer[i][8:10] + sPuffer[i][11:13])             # Startzeit holen (SSMM)

        if Startzeit == Aktuelle and sPuffer[i][w] == "x":                # wenn Uhrzeit und Wochentag stimmen
            try:                                                          # URL prüfen
                urllib.request.urlopen(urllib.request.Request(sPuffer[i+1].rstrip(), headers={"User-Agent": uaListe[uaAktiv][30:]}), timeout=5)
            except urllib.error.HTTPError as err:
                StatusFehler += 1
                Statusleiste_Anzeigen("")
                protmeld = "HTTP error: " + str(err.code) + "        - "
                protDatei_Schreiben(protmeld, sPuffer[i][24:].rstrip())
            except urllib.error.URLError as err:
                StatusFehler += 1
                Statusleiste_Anzeigen("")
                meldung = str(err.reason)
                protDatei_Schreiben("URL error: " + meldung[0:11].ljust(11) + " - ", sPuffer[i][24:].rstrip())
            except:
                StatusFehler += 1
                Statusleiste_Anzeigen("")
                protDatei_Schreiben("Unexpected error       - ", sPuffer[i][24:].rstrip())
            else:                                                         # wenn URL gültig
                for n in range(1, 1000):                                  # Namen der Aufnahme festlegen (..._001 bis ..._999)
                    Dateiname = sPuffer[i][24:].rstrip() + "_" + str(n).zfill(3) + ".ts"
                    if not os.path.isfile(recVerzeichnis + Dateiname):   break

                cmdNr = int(sPuffer[i][20])-1
                if ExpertenModus.get() == 1:
                    cmdStrg = cmdxListe[cmdNr][0:]
                else:    # Standard-Modus
                    if cmdNr > 2:    cmdNr = 0
                    cmdStrg = cmdListe[cmdNr][0:]

                cmdStrg = cmdStrg.replace("link", sPuffer[i+1].rstrip())         # Link der Aufnahme in Kommandozeile einbauen
                cmdStrg = cmdStrg.replace("uagent", uaListe[uaAktiv][30:])       # User-Agent in Kommandozeile einbauen
                cmdStrg = cmdStrg.replace("file", recVerzeichnis + Dateiname)    # Namen der Aufnahme in Kommandozeile einbauen
                #print(cmdStrg)

                if WINDOWS:    proc = subprocess.Popen(cmdStrg, shell=True)
                else:          proc = subprocess.Popen(cmdStrg, shell=True, preexec_fn=os.setsid)
                #print(proc.pid)

                if proc.pid:
                    recPID.append(proc.pid)                               # Aufnahme: PID speichern
                    recStart.append(time.strftime("%H%M"))                # Aufnahme: Startzeit speichern
                    recEnde.append(sPuffer[i][14:16] + sPuffer[i][17:19]) # Aufnahme: Endezeit (SSMM) speichern
                    recName.append(sPuffer[i][24:].rstrip())              # Aufnahme: Namen (ohne LF) speichern
                    StatusAufnahmen = len(recPID)
                    Statusleiste_Anzeigen("")
                    if ExpertenModus.get() == 1:   protDatei_Schreiben("[" + str(cmdNr+1) + "] " + TxT["Gestartet Schedule"], sPuffer[i][24:].rstrip())
                    else:                          protDatei_Schreiben("[" + str(youtube_dl.get()+1) + "] " + TxT["Gestartet Schedule"], sPuffer[i][24:].rstrip())

            #---------- Wenn Einmal-Aufnehmen ---------

            if sPuffer[i][22] == " ":
                z = list(sPuffer[i])
                z[w] = "-"                                                # Wochentag in Puffer deaktivieren
                sPuffer[i] = "".join(z)

                if sPuffer[i][0:7] == "-------":                          # wenn keine Wochentage mehr gültig
                    sPuffer.pop(i+1)                                      # URL-Zeile löschen
                    sPuffer.pop(i)                                        # Text-Zeile löschen 

                with open(schedDatei, "w", encoding="utf-8") as Datei:                      # Schedule neu schreiben
                    for i in range(len(sPuffer)):
                        Datei.write(sPuffer[i])
                    Datei.close()

    #---------- Nächste Aufnahme(n) beenden ----------

    for i in range(len(recEnde)-1, -1, -1):            # vom Ende her durchsuchen (Löschfehler vermeiden)
        Endezeit = int(recEnde[i])
        if Endezeit == Aktuelle:
            Kill_PID(i, 2)
            recPID.pop(i)                              # Aufnahme: PID löschen
            recStart.pop(i)                            # Aufnahme: Startzeit löschen
            recEnde.pop(i)                             # Aufnahme: Endezeit löschen
            recName.pop(i)                             # Aufnahme: Namen löschen
            StatusAufnahmen = len(recPID)
            StatusBeendete += 1
            Statusleiste_Anzeigen("")

    if int(time.strftime("%S")) < 55:                  # Minutensprung verhindern
        Master.after(60000, Schedule_Starten)
    else:
        Master.after(20000, Schedule_Starten)

###############################################################################################################

def Protokoll_Anzeigen(event=None):

    if not os.path.isfile(protDatei):
        message.showwarning("Stream Recorder", "\n" + protDatei + TxT["nicht gefunden"])
    else:
        Fenster = tk.Toplevel(Master)
        Fenster.title(TxT["Protokoll"])
        Fenster.wm_attributes("-topmost", True)
        Fenster.grab_set()
        Scroll_Balken = tk.Scrollbar(Fenster, width=14)
        Text_Fenster = tk.Text(Fenster, width=77, height=30, pady=10, padx=10, yscrollcommand=Scroll_Balken.set)
        Text_Fenster.config(foreground=FensterVG, background=FensterHG, font="Consolas 10", wrap="none")
        Scroll_Balken.config(command = Text_Fenster.yview)
        Scroll_Balken.pack(side="right", fill="y", padx=1, pady=1)
        Text_Fenster.pack(fill="both", padx=2, pady=2, expand=True)
        with open(protDatei, "r", encoding="utf-8") as Datei:
            Text_Fenster.configure(state="normal")
            Text_Fenster.delete(1.0, tk.END)
            #for Zeile in Datei:                          # von oben nach unten anzeigen
            #    Text_Fenster.insert(1.0, Zeile)
            Text_Fenster.insert(tk.END, Datei.read())
            Text_Fenster.see(tk.END)                     # das Ende der Datei anzeigen
            Text_Fenster.configure(state="disabled")
            Datei.close()
        Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Schedule_Anzeigen(event=None):

    global sPuffer

    def Eintrag_Entfernen(event=None):

        if Sched_Liste.curselection():
            Nr = Sched_Liste.curselection()[0]           # Index des markierten Senders
            if message.askyesno("Stream Recorder", "\n" + sPuffer[Nr*2][24:].rstrip() + TxT["wirklich entfernen"], parent=Fenster):
                sPuffer.pop(Nr*2)                        # Beschreibung löschen
                sPuffer.pop(Nr*2)                        # URL löschen
                with open(schedDatei, "w", encoding="utf-8") as Datei:    # Schedule-Datei neu schreiben (überschreiben)
                    for i in range(0, len(sPuffer)):
                        Datei.write(sPuffer[i])
                    Datei.close()
                Sched_Liste.delete(0, tk.END)
                for i in range(0, len(sPuffer)-1, 2):    # Schedule-Liste neu anzeigen
                    Sched_Liste.insert(tk.END, " {:s}".format(sPuffer[i].rstrip()))
                Sched_Liste.selection_set(Nr-1)          # Scrollbalken einen Eintrag zurück
                Sched_Liste.activate(Nr-1)
                Sched_Liste.see(Nr-1)

    if not os.path.isfile(schedDatei):
        message.showwarning("Stream Recorder", "\n" + schedDatei + TxT["nicht gefunden"])
    else:
        Fenster = tk.Toplevel(Master)
        Fenster.title(TxT["Schedule"])
        Fenster.wm_attributes("-topmost", True)
        #Fenster.grab_set()

        Sched_Liste = tk.Listbox(Fenster, width=60, height=20, yscrollcommand=Scroll_Balken.set)
        Sched_Liste.config(bg=FensterHG, fg=FensterVG, font="Consolas "+SizeL)
        Zeile_Info = tk.Label(Fenster, font="Helvetica 10", text=TxT["Eintrag entfernen"])
        Zeile_Info.pack(side="bottom", fill="x", padx=3, pady=2)
        Sched_Liste.pack(fill="both", padx=3, pady=3, expand=True)

        with open(schedDatei, "r", encoding="utf-8") as Datei:
            sPuffer.clear()
            for Zeile in Datei:
                sPuffer.append(Zeile)
            Datei.close()
        if len(sPuffer) > 0:                        # wenn mind. 1 Eintrag
            for i in range(0, len(sPuffer)-1, 2):
                Sched_Liste.insert(tk.END, " {:s}".format(sPuffer[i].rstrip()))
            Sched_Liste.selection_set(0)
            Sched_Liste.activate(0)
            Sched_Liste.focus_set()
            Sched_Liste.bind("<Delete>", Eintrag_Entfernen)
            Sched_Liste.bind("<Double-Button-1>", Eintrag_Entfernen)

        Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Schedule_Hinzufuegen(event=None):

    def Eintrag_Speichern(event=None):

        global WochenText

        wt = list(WochenText)                      # Wochentage-String zusammenbauen
        for i in range(0, 7, 1):
            if Wochentag[i].get():    wt[i] = "x"  
            else:                     wt[i] = "-"
        WochenText = "".join(wt)

        Start = varStart.get()
        Ende = varEnde.get()
  
        if ExpertenModus.get() == 1:   Rec = varRec.get()    # Kommandozeilen-Nummer
        else:                          Rec = str(youtube_dl.get()+1)

        if Wiederholung.get():    Einmal = "-"     # Dauer-Aufnahme
        else:                     Einmal = " "     # Einmal-Aufnahme

        with open(schedDatei, "a", encoding="utf-8") as Datei:
            Datei.write(WochenText + " " + Start + " " + Ende + " " + Rec + " " + Einmal + " " + Name[Nr] + "\n")
            Datei.write(URL[Nr] + "\n")
            Datei.close()
        Fenster.destroy()

#----------------------------------------------------------------

    global Wochentag

    if Listen_Box.curselection():
        Nr = Listen_Box.curselection()[0]          # Index des markierten Senders
    else:
        message.showwarning(TxT["Schedule"], "\n" + TxT["Kein Sender"])
        return
 
    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Schedule"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    SenderName = tk.Label(Fenster, text=Name[Nr][0:56], font="Helvetica 12")

    for i in range(0, 7, 1):                       # Checkboxen Mo-So löschen
        Wochentag[i] = tk.IntVar()
        Wochentag[i].set(0)
    i = datetime.datetime.today().weekday()        # aktuellen Wochentag setzen
    Wochentag[i].set(1)

    TextMo = tk.Label(Fenster, text=TxT["Mo"], font="Helvetica 9")
    TextDi = tk.Label(Fenster, text=TxT["Di"], font="Helvetica 9")
    TextMi = tk.Label(Fenster, text=TxT["Mi"], font="Helvetica 9")
    TextDo = tk.Label(Fenster, text=TxT["Do"], font="Helvetica 9")
    TextFr = tk.Label(Fenster, text=TxT["Fr"], font="Helvetica 9")
    TextSa = tk.Label(Fenster, text=TxT["Sa"], font="Helvetica 9")
    TextSo = tk.Label(Fenster, text=TxT["So"], font="Helvetica 9")
    TextTag = [TextMo, TextDi, TextMi, TextDo, TextFr, TextSa, TextSo]
    TextStart = tk.Label(Fenster, text="Start", font="Helvetica 9")
    TextEnde = tk.Label(Fenster, text="Stop", font="Helvetica 9")
    TextRec = tk.Label(Fenster, text="Rec", font="Helvetica 9")
    BoxMo = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[0])
    BoxDi = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[1])
    BoxMi = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[2])
    BoxDo = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[3])
    BoxFr = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[4])
    BoxSa = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[5])
    BoxSo = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[6])

    ZeitListe = list(range(24*60))    # Variablenliste für Uhrzeit
    for i in range(24*60):
        zeit = datetime.datetime.now() + datetime.timedelta(minutes=i)
        ZeitListe[i] = zeit.strftime("%H:%M")
    RecListe = list(range(1,10,1))    # Variablenliste für Kommandozeile
    varStart = tk.StringVar()
    varEnde = tk.StringVar()
    varRec = tk.StringVar()
    BoxStart = tk.Spinbox(Fenster, values=ZeitListe, textvariable=varStart, repeatdelay=100,repeatinterval=10, bd=3, width=5, font="Helvetica 11")
    BoxEnde = tk.Spinbox(Fenster, values=ZeitListe, textvariable=varEnde, repeatdelay=100,repeatinterval=10, bd=3, width=5, font="Helvetica 11")
    BoxRec = tk.Spinbox(Fenster, values=RecListe, textvariable=varRec, repeatdelay=100,repeatinterval=80, bd=3, width=2, font="Helvetica 11")
    varStart.set(ZeitListe[1])
    varEnde.set(ZeitListe[2])
    varRec.set(RecListe[youtube_dl.get()])

    Wiederholung = tk.IntVar()        # Einmal-Aufnahme setzen (default)
    Wiederholung.set(0)
    Radio9 = tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wiederholung, value=1, text=" ∞  ", font="Helvetica 11")
    Radio1 = tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wiederholung, value=0, text=" ①  ", font="Helvetica 11")
    ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Speichern"], font="Helvetica 11", command=Eintrag_Speichern)
    ButtonAbbrechen = tk.Button(Fenster, bd=3, text=TxT["Abbrechen"], font="Helvetica 11", command=Fenster.destroy)

    TextTag = [TextMo, TextDi, TextMi, TextDo, TextFr, TextSa, TextSo]    # Variablenliste für Wochentage
    BoxTag = [BoxMo, BoxDi, BoxMi, BoxDo, BoxFr, BoxSa, BoxSo]

    SenderName.grid(row=0, column=2, padx=0, pady=20, columnspan=13)
    tk.Label(Fenster).grid(row=1, column=1, padx=10)
    for i in range (7):
        TextTag[i].grid(row=1, column=i+2, padx=2, pady=2)
    TextStart.grid(row=1, column=9, padx=30, pady=2)
    TextEnde.grid(row=1, column=10, padx=0, pady=2)
    TextRec.grid(row=1, column=11, padx=25, pady=2)
    Radio9.grid(row=1, column=12, padx=2, pady=2)
    tk.Label(Fenster).grid(row=1, column=13, padx=10)
    tk.Label(Fenster).grid(row=2, column=1, padx=10)
    for i in range (7):
        BoxTag[i].grid(row=2, column=i+2, padx=1, pady=2)
    BoxStart.grid(row=2, column=9, padx=30, pady=2)
    BoxEnde.grid(row=2, column=10, padx=0, pady=2)
    BoxRec.grid(row=2, column=11, padx=25, pady=2)
    Radio1.grid(row=2, column=12, padx=2, pady=2)
    tk.Label(Fenster).grid(row=2, column=13, padx=10)
    ButtonSpeichern.grid(row=3, column=4, padx=15, pady=25, ipadx=33, columnspan=5)
    ButtonAbbrechen.grid(row=3, column=9, padx=0, pady=25, ipadx=30, columnspan=4)
    if ExpertenModus.get() == 0:    BoxRec.config(state='disabled')       # wenn Standard-Modus
    ButtonSpeichern.bind("<Return>", Eintrag_Speichern)
    ButtonAbbrechen.bind("<Return>", lambda event: Fenster_Schliessen(Fenster))
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Schedule_Bearbeiten(event=None):

    def Schedule_Speichern(event):

        with open(schedDatei, "w", encoding="utf-8") as Datei:
            Datei.write(Text_Fenster.get("1.0", tk.END + "-1c"))          # ohne letztes LF !!
            Datei.close()
        Fenster.destroy()   

    if not os.path.isfile(schedDatei):
        message.showwarning("Stream Recorder", "\n" + schedDatei + TxT["nicht gefunden"])
    else:
        Fenster = tk.Toplevel(Master)
        Fenster.title(TxT["Schedule"])
        Fenster.wm_attributes("-topmost", True)
        Fenster.grab_set()

        Scroll_Vertikal = tk.Scrollbar(Fenster, width=14)
        Scroll_Horizont = tk.Scrollbar(Fenster, width=14, orient="horizontal")
        Text_Fenster = tk.Text(Fenster, width=76, height=30, pady=10, padx=10, yscrollcommand = Scroll_Vertikal.set, xscrollcommand = Scroll_Horizont.set)
        if Zeilenumbruch.get() == 1:  umbruch = "none"
        else                       :  umbruch = "char"
        Text_Fenster.config(foreground=FensterVG, background=FensterHG, font="Consolas 10", wrap=umbruch, undo="TRUE")
        Zeile_Info = tk.Label(Fenster, font="Helvetica 10", text=TxT["Datei speichern"])
        Scroll_Vertikal.config(command = Text_Fenster.yview)
        Scroll_Horizont.config(command = Text_Fenster.xview)
        Zeile_Info.pack(side="bottom", fill="x", padx=2, pady=0)
        Scroll_Vertikal.pack(side="right", fill="y", padx=1, pady=1)
        Scroll_Horizont.pack(side="bottom", fill="x", padx=1, pady=1)
        Text_Fenster.pack(fill="both", padx=2, pady=2, expand=True)

        with open(schedDatei, "r", encoding="utf-8") as Datei:
            Text_Fenster.insert("1.0", Datei.read())
            Datei.close()

        Text_Fenster.focus_set()
        Text_Fenster.bind("<Control-Key-s>", Schedule_Speichern)
        Text_Fenster.bind("<Double-Button-3>", Schedule_Speichern)
        Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Einstellungen(event=None):

    def Farbe_Aktivieren():

        Menuleiste.config(activebackground=Hintergrund, activeforeground=Vordergrund)
        Menu_Datei.config(activebackground=Hintergrund, activeforeground=Vordergrund)
        Menu_Suchen.config(activebackground=Hintergrund, activeforeground=Vordergrund)
        Menu_Favoriten.config(activebackground=Hintergrund, activeforeground=Vordergrund)
        Menu_Aufnahme.config(activebackground=Hintergrund, activeforeground=Vordergrund)
        Menu_Schedule.config(activebackground=Hintergrund, activeforeground=Vordergrund)
        Listen_Box.config(bg=Hintergrund, fg=Vordergrund)

    def Vordergrund_Einstellen():

        global Vordergrund

        Farbe = chooser.askcolor(parent=Fenster, color=Vordergrund, title = "Vordergrund")[1]
        if Farbe:
            Vordergrund = Farbe
        Farbe_Aktivieren()

    def Hintergrund_Einstellen():

        global Hintergrund

        Farbe = chooser.askcolor(parent=Fenster, color=Hintergrund, title = "Hintergrund")[1]
        if Farbe:
            Hintergrund = Farbe
        Farbe_Aktivieren()

    def Fensterfarbschema():

        VG = ["#ffffff", "#ffffff", "#ffffff", "#ffffff", "#ffffff", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000", "#000000"]
        HG = ["#000000", "#222222", "#550000", "#003300", "#000055", "#eeeeee", "#bbbbbb", "#55bbff", "#ffaa66", "#ffff88", "#00ffee", "#ffaaff"]
        Farben = ["            weiss - schwarz", "            weiss - grau", "            weiss - rot", "            weiss - grün",
                  "            weiss - blau", "        schwarz - weiss", "        schwarz - grau", "        schwarz - blau",
                  "        schwarz - orange", "        schwarz - gelb", "        schwarz - cyan", "        schwarz - lila"]

        def Schema_Aktivieren(event):

            global FensterVG, FensterHG

            Nr = int(Farben_Liste.curselection()[0])
            FensterVG = VG[Nr]
            FensterHG = HG[Nr]
            Fenster2.destroy()

        Fenster2 = tk.Toplevel(Fenster)
        Fenster2.title("Schema")
        Fenster2.wm_attributes("-topmost", True)
        Fenster2.grab_set()

        Farben_Liste = tk.Listbox(Fenster2, width=22, height=12, font="Helvetica 13")
        Farben_Liste.pack(side="left", fill="y", padx=10, pady=10)
        for name in Farben:
            Farben_Liste.insert(tk.END, name)
        for i in range(12):
            Farben_Liste.itemconfig(i, fg=VG[i], bg=HG[i])
        Farben_Liste.bind("<Double-Button-1>", Schema_Aktivieren)

    def Einstellungen_Speichern(event=None):

        global m3uVerzeichnis, recVerzeichnis, startDatei, SizeM, SizeL, Gebiet, TxT
  
        if EingabeM3uVerz.get()[-1] == "/":  m3uVerzeichnis = EingabeM3uVerz.get()
        else:                                m3uVerzeichnis = EingabeM3uVerz.get() + "/" 
        if not os.path.isdir(m3uVerzeichnis):
            os.makedirs(m3uVerzeichnis)
        if EingabeRecVerz.get()[-1] == "/":  recVerzeichnis = EingabeRecVerz.get()
        else:                                recVerzeichnis = EingabeRecVerz.get() + "/" 
        if not os.path.isdir(recVerzeichnis):
            os.makedirs(recVerzeichnis)
        startDatei = EingabeStartDat.get()

        if varSizeM.get().isdecimal():
            SizeM = varSizeM.get()[0:2]
        if varSizeL.get().isdecimal():
            SizeL = varSizeL.get()[0:2]
        Gebiet = GebietButton.get()
        TxT = Woerterbuch[Gebiet]
        Listen_Box.config(font="Consolas "+SizeL)

        Schreibe_confDatei()

        Menuleiste.entryconfigure(1, label=TxT["Datei"], font=FontM+SizeM)
        Menuleiste.entryconfigure(2, label=TxT["Suchen"], font=FontM+SizeM)
        Menuleiste.entryconfigure(3, label=TxT["Favoriten"], font=FontM+SizeM)
        Menuleiste.entryconfigure(4, label=TxT["Aufnahme"], font=FontM+SizeM)
        Menuleiste.entryconfigure(5, label=TxT["Schedule"], font=FontM+SizeM)
        Menuleiste.entryconfigure(6, label=TxT["Hilfe"], font=FontM+SizeM)
        Menu_Datei.entryconfigure(0, label=TxT["Öffnen"], font=FontM+SizeM)
        Menu_Datei.entryconfigure(1, label=TxT["Bearbeiten"], font=FontM+SizeM)
        Menu_Datei.entryconfigure(3, label=TxT["Player"], font=FontM+SizeM)
        Menu_Datei.entryconfigure(4, label=TxT["UserAgent"], font=FontM+SizeM)
        Menu_Datei.entryconfigure(5, label=TxT["Einstellungen"], font=FontM+SizeM)
        Menu_Datei.entryconfigure(7, label=TxT["Beenden"], font=FontM+SizeM)
        Menu_Suchen.entryconfigure(0, label=TxT["nNamen"], font=FontM+SizeM)
        Menu_Suchen.entryconfigure(1, label=TxT["nLand"], font=FontM+SizeM)
        Menu_Suchen.entryconfigure(2, label=TxT["nGruppe"], font=FontM+SizeM)
        Menu_Suchen.entryconfigure(4, label=TxT["SuchSpeich"], font=FontM+SizeM)
        Menu_Suchen.entryconfigure(6, label=TxT["Alle"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(0, label=TxT["Anzeigen"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(1, label=TxT["Hinzufügen"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(2, label=TxT["Bearbeiten"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(3, label=TxT["Entfernen"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(5, label=TxT["Eingeben"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(7,label=TxT["Zurück"], font=FontM+SizeM)
        Menu_Aufnahme.entryconfigure(0, label=TxT["Stoppen"], font=FontM+SizeM)
        Menu_Aufnahme.entryconfigure(1, label=TxT["AlleStop"], font=FontM+SizeM)
        Menu_Aufnahme.entryconfigure(3, label=TxT["Manager"], font=FontM+SizeM)
        Menu_Aufnahme.entryconfigure(5, label=TxT["Protokoll"], font=FontM+SizeM)
        Menu_Schedule.entryconfigure(0, label=TxT["Anzeigen"], font=FontM+SizeM)
        Menu_Schedule.entryconfigure(1, label=TxT["Hinzufügen"], font=FontM+SizeM)
        Menu_Schedule.entryconfigure(3, label=TxT["Bearbeiten"], font=FontM+SizeM)
        Menu_Hilfe.entryconfigure(0, label=TxT["Tastatur"], font=FontM+SizeM)
        Menu_Hilfe.entryconfigure(2, label=TxT["Über"], font=FontM+SizeM)

        Fenster.destroy()

#-----------------------------------------------------

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Einstellungen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    RadioDeutsch = tk.Radiobutton(Fenster, relief="raised", bd=3, variable=GebietButton, value="de", text=TxT["Deutsch"], font="Helvetica 11")
    RadioEnglish = tk.Radiobutton(Fenster, relief="raised", bd=3, variable=GebietButton, value="en", text=TxT["Englisch"], font="Helvetica 11")
    GebietButton.set(Gebiet)
    CheckZUmbruch = tk.Checkbutton(Fenster, bd=3, text=TxT["Zeilenumbruch"], font="Helvetica 11", variable=Zeilenumbruch)
    CheckProtokoll = tk.Checkbutton(Fenster, bd=3, text=TxT["Protokoll aus"], font="Helvetica 11", variable=ProtMeldAus)
    CheckGroesse = tk.Checkbutton(Fenster, bd=3, text=TxT["Fenster anders"], font="Helvetica 11", variable=FensterAnders)
    CheckPlayer = tk.Checkbutton(Fenster, bd=3, text=TxT["Player prüfen"], font="Helvetica 11", variable=PlayerPruefen)
    CheckExperten = tk.Checkbutton(Fenster, bd=3, text=TxT["Experten Modus"], font="Helvetica 11", variable=ExpertenModus)

    TextSizeM = tk.Label(Fenster, text=TxT["Schrift Menü"], font="Helvetica 11")
    TextSizeL = tk.Label(Fenster, text=TxT["Schrift Liste"], font="Helvetica 11")
    SizeListe = list(range(5,26,1))
    varSizeM = tk.StringVar()
    varSizeL = tk.StringVar()
    BoxSizeM = tk.Spinbox(Fenster, values=SizeListe, textvariable=varSizeM, repeatdelay=100,repeatinterval=100, bd=4, width=3, font="Helvetica 11")
    BoxSizeL = tk.Spinbox(Fenster, values=SizeListe, textvariable=varSizeL, repeatdelay=100,repeatinterval=100, bd=4, width=3, font="Helvetica 11")
    varSizeM.set(SizeM)
    varSizeL.set(SizeL)

    ButtonVorderg = tk.Button(Fenster, bd=3, text=TxT["VGfarbe"], font="Helvetica 11", command=Vordergrund_Einstellen)
    ButtonHinterg = tk.Button(Fenster, bd=3, text=TxT["HGfarbe"], font="Helvetica 11", command=Hintergrund_Einstellen)
    ButtonSchema = tk.Button(Fenster, bd=3, text=TxT["FFschema"], font="Helvetica 11", command=Fensterfarbschema)
    TextM3uVerz = tk.Label(Fenster, text=TxT["pVerzeichnis"], font="Helvetica 10")
    EingabeM3uVerz = tk.Entry(Fenster, bd=4, width=38, font="Helvetica 11")
    EingabeM3uVerz.insert(0, m3uVerzeichnis)
    TextRecVerz = tk.Label(Fenster, text=TxT["rVerzeichnis"], font="Helvetica 10")
    EingabeRecVerz = tk.Entry(Fenster, bd=4, width=38, font="Helvetica 11")
    EingabeRecVerz.insert(0, recVerzeichnis)
    TextStartDat = tk.Label(Fenster, text=TxT["sDatei"], font="Helvetica 10")
    EingabeStartDat = tk.Entry(Fenster, bd=4, width=38, font="Helvetica 11")    
    EingabeStartDat.insert(0, startDatei)

    ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Speichern"], font="Helvetica 11", command=Einstellungen_Speichern)
    ButtonAbbrechen = tk.Button(Fenster, bd=3, text=TxT["Abbrechen"], font="Helvetica 11", command=Fenster.destroy)

    RadioDeutsch.grid(row=1, column=0, padx=25, pady=20, ipadx=12, ipady=3, sticky="e")
    RadioEnglish.grid(row=1, column=1, padx=25, pady=20, ipadx=12, ipady=3, sticky="w")
    CheckZUmbruch.grid(row=2, column=0, columnspan=2, pady=1, ipadx=50, sticky="w")
    CheckProtokoll.grid(row=3, column=0, columnspan=2, pady=1, ipadx=50, sticky="w")
    CheckGroesse.grid(row=4, column=0, columnspan=2, pady=1, ipadx=50, sticky="w")
    CheckPlayer.grid(row=5, column=0, columnspan=2, pady=1, ipadx=50, sticky="w")
    CheckExperten.grid(row=6, column=0, columnspan=2, pady=1, ipadx=50, sticky="w")
    TextSizeM.grid(row=7, column=0, columnspan=2, pady=7, ipadx=60, sticky="w")
    BoxSizeM.grid(row=7, column=1, padx=62, pady=7, sticky="e")
    TextSizeL.grid(row=8, column=0, columnspan=2, pady=0, ipadx=60, sticky="w")
    BoxSizeL.grid(row=8, column=1, padx=62, pady=0, sticky="e")
    ButtonVorderg.grid(row=9, column=0, columnspan=2, padx=50, pady=14, ipadx=57)
    ButtonHinterg.grid(row=10, column=0, columnspan=2, padx=50, pady=0, ipadx=59)
    ButtonSchema.grid(row=11, column=0, columnspan=2, padx=50, pady=14, ipadx=47)
    TextM3uVerz.grid(row=12, column=0, columnspan=2, pady=0)
    EingabeM3uVerz.grid(row=13, column=0, columnspan=2, pady=7)
    TextRecVerz.grid(row=14, column=0, columnspan=2, pady=0)
    EingabeRecVerz.grid(row=15, column=0, columnspan=2, pady=7)
    TextStartDat.grid(row=16, column=0, columnspan=2, pady=0)
    EingabeStartDat.grid(row=17, column=0, columnspan=2, pady=7)
    ButtonSpeichern.grid(row=18, column=0, padx=22, pady=18, ipadx=15, sticky="e")
    ButtonAbbrechen.grid(row=18, column=1, padx=22, pady=18, ipadx=12, sticky="w")
    tk.Label(Fenster).grid(row=19, column=0)

    ButtonSpeichern.bind("<Return>", Einstellungen_Speichern)
    ButtonAbbrechen.bind("<Return>", lambda event: Fenster_Schliessen(Fenster))
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Hilfe_Tastatur(event=None):

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Tastatur"])
    Fenster.wm_attributes("-topmost", True)
    #Fenster.grab_set()
    Text_Fenster = tk.Text(Fenster, width=42, height=41, pady=10, padx=10)
    Text_Fenster.config(foreground=FensterVG, background=FensterHG, font="Consolas 10", wrap="none")
    Text_Fenster.pack(fill="both", padx=3, pady=3, expand=True)
    Text_Fenster.configure(state="normal")
    Text_Fenster.delete("1.0", tk.END)
    if Gebiet == "de":
        Text_Fenster.insert(tk.END, "\n   Stream auswählen:      <Pfeiltasten↑↓>")
        Text_Fenster.insert(tk.END, "\n   Vorheriger Stream:     <Pfeiltasten←→>")
        Text_Fenster.insert(tk.END, "\n   Stream anschauen:      <Eingabetaste>")
        Text_Fenster.insert(tk.END, "\n   Stream aufnehmen:      <Leertaste>\n")
        Text_Fenster.insert(tk.END, "\n   Tastaturbelegung:      <F1>")
        Text_Fenster.insert(tk.END, "\n   Vorherige Playliste:   <F2>")
        Text_Fenster.insert(tk.END, "\n   Alle anzeigen:         <F3>")
        Text_Fenster.insert(tk.END, "\n   Zu Favoriten hinzu:    <F4>")
        Text_Fenster.insert(tk.END, "\n   Player auswählen:      <F5>")
        Text_Fenster.insert(tk.END, "\n   User-Agent auswählen:  <F6>")
        Text_Fenster.insert(tk.END, "\n   Download-Manager:      <F7>")
        Text_Fenster.insert(tk.END, "\n   Neue Timer-Aufnahme:   <F8>")
        Text_Fenster.insert(tk.END, "\n   Einstellungen:         <F9>")
        Text_Fenster.insert(tk.END, "\n   Menü öffnen:           <F10>\n")
        Text_Fenster.insert(tk.END, "\n   Aufnahme stoppen:      <Strg+T>")
        Text_Fenster.insert(tk.END, "\n   Protokoll anzeigen:    <Strg+P>")
        Text_Fenster.insert(tk.END, "\n   Favoriten anzeigen:    <Strg+F>")
        Text_Fenster.insert(tk.END, "\n   Favoriten bearbeiten:  <Strg+A>")
        Text_Fenster.insert(tk.END, "\n   Neuen Stream eingeben: <Strg+N>")
        Text_Fenster.insert(tk.END, "\n   Neue Playlist öffnen:  <Strg+O>")
        Text_Fenster.insert(tk.END, "\n   Playliste bearbeiten:  <Strg+E>")
        Text_Fenster.insert(tk.END, "\n   Schedule anzeigen:     <Strg+S>")
        Text_Fenster.insert(tk.END, "\n   Schedule bearbeiten:   <Strg+D>")
        Text_Fenster.insert(tk.END, "\n   Programm beenden:      <Strg+Q>\n")
        Text_Fenster.insert(tk.END, "\n   Favorit hochschieben:  <Alt+↑>")
        Text_Fenster.insert(tk.END, "\n   Favorit runterschieb:  <Alt+↓>")
        Text_Fenster.insert(tk.END, "\n   Blättern seitenweise:  <Bild↑/Bild↓>")
        Text_Fenster.insert(tk.END, "\n   Zum Anfang springen:   <Pos1>")
        Text_Fenster.insert(tk.END, "\n   Zum Ende springen:     <Ende>")
        Text_Fenster.insert(tk.END, "\n   Favoriten entfernen:   <Entf>")
        Text_Fenster.insert(tk.END, "\n   Fenster schließen:     <Esc>\n")
        Text_Fenster.insert(tk.END, "\n   Stream auswählen:      <Linksklick>")
        Text_Fenster.insert(tk.END, "\n   Stream anschauen:      <Doppelklick>")
        Text_Fenster.insert(tk.END, "\n   Stream aufnehmen:      <Mittelklick>")
        Text_Fenster.insert(tk.END, "\n   Player auswählen:      <Rechtsklick>\n")
    else:
        Text_Fenster.insert(tk.END, "\n   Select stream:         <Arrow Keys ↑↓>")
        Text_Fenster.insert(tk.END, "\n   Previous streams:      <Arrow Keys ←→>")
        Text_Fenster.insert(tk.END, "\n   View stream:           <Return>")
        Text_Fenster.insert(tk.END, "\n   Record stream:         <Spacebar>\n")
        Text_Fenster.insert(tk.END, "\n   Keyboard shortcuts:    <F1>")
        Text_Fenster.insert(tk.END, "\n   Previous playlist:     <F2>")
        Text_Fenster.insert(tk.END, "\n   Search filter off:     <F3>")
        Text_Fenster.insert(tk.END, "\n   Add to favorites:      <F4>")
        Text_Fenster.insert(tk.END, "\n   Select player:         <F5>")
        Text_Fenster.insert(tk.END, "\n   Select user agent:     <F6>")
        Text_Fenster.insert(tk.END, "\n   Download manager:      <F7>")
        Text_Fenster.insert(tk.END, "\n   Set new timer:         <F8>")
        Text_Fenster.insert(tk.END, "\n   Settings:              <F9>")
        Text_Fenster.insert(tk.END, "\n   Open file menu:        <F10>\n")
        Text_Fenster.insert(tk.END, "\n   Terminate recording:   <Ctrl+T>")
        Text_Fenster.insert(tk.END, "\n   View protocol:         <Ctrl+P>")
        Text_Fenster.insert(tk.END, "\n   View favorites:        <Ctrl+F>")
        Text_Fenster.insert(tk.END, "\n   Edit favorite:         <Ctrl+A>")
        Text_Fenster.insert(tk.END, "\n   Enter new stream:      <Ctrl+N>")
        Text_Fenster.insert(tk.END, "\n   Open new playlist:     <Ctrl+O>")
        Text_Fenster.insert(tk.END, "\n   Edit playlist:         <Ctrl+E>")
        Text_Fenster.insert(tk.END, "\n   View schedule:         <Ctrl+S>")
        Text_Fenster.insert(tk.END, "\n   Edit schedule:         <Ctrl+D>")
        Text_Fenster.insert(tk.END, "\n   Quit program:          <Ctrl+Q>\n")
        Text_Fenster.insert(tk.END, "\n   Move favorite up:      <Alt+Up>")
        Text_Fenster.insert(tk.END, "\n   Move favorite down:    <Alt+Down>")
        Text_Fenster.insert(tk.END, "\n   Scroll page:           <PgUp/PgDn>")
        Text_Fenster.insert(tk.END, "\n   Go to top:             <Home>")
        Text_Fenster.insert(tk.END, "\n   Go to end:             <End>")
        Text_Fenster.insert(tk.END, "\n   Delete favorite:       <Del>")
        Text_Fenster.insert(tk.END, "\n   Close windows:         <Esc>\n")
        Text_Fenster.insert(tk.END, "\n   Select stream:         <Left Click>")
        Text_Fenster.insert(tk.END, "\n   View stream:           <Double Click>")
        Text_Fenster.insert(tk.END, "\n   Record stream:         <Middle Click>")
        Text_Fenster.insert(tk.END, "\n   Select player:         <Right Click>\n")
    Text_Fenster.configure(state="disabled")
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Hilfe_Ueber():

    def Laufzeile():

        ende = { "de":152, "en":139 }  
        if Laufzeile.Zaehler < ende[Gebiet]:
            Laufzeile.Zeichenkette = Laufzeile.Zeichenkette[1:] + Laufzeile.Zeichenkette[0]
            Lauftext.set(Laufzeile.Zeichenkette[0:43])
            Laufzeile.Zaehler += 1
            Fenster.after(70, Laufzeile)

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Über"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()
    if os.path.isfile(Bildchen):
        Hilfe_Ueber.Icon = tk.PhotoImage(file=Bildchen)
        Grafik = tk.Label(Fenster, image=Hilfe_Ueber.Icon)
        Grafik.pack(pady=20)
    else:
        tk.Label(Fenster).pack()
    Zeile1 = tk.Label(Fenster, text="Stream Recorder", font="Helvetica 18 bold")
    Zeile2 = tk.Label(Fenster, text="Version 1.5", font="Helvetica 12")
    Laufzeile.Zeichenkette = TxT["Entwickelt"]
    Lauftext.set(Laufzeile.Zeichenkette[0:43])
    Zeile3 = tk.Label(Fenster, textvariable=Lauftext, font="Helvetica 12")
    Zeile1.pack(padx=120, pady=10) 
    Zeile2.pack(pady=10) 
    Zeile3.pack(pady=20)
    tk.Label(Fenster).pack()
    Laufzeile.Zaehler = 0
    Fenster.after(1500, Laufzeile)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Vorheriger_Stream(i, event=None):

    global altPos

    if (i == -1 and altPos > 0) or (i == 1 and altPos < len(altName)-1):
        altPos += i
        cmdStrg = pListe[pAktiv][24:].replace("URL[Nr]", altLink[altPos])    # Kommandozeile zusammenbauen
        Statusleiste_Anzeigen(altName[altPos])
        subprocess.Popen(cmdStrg, shell=True)      # Player starten
        Master.focus_force()
        Listen_Box.focus_set()                     # Focus zurück auf Programmliste
    return "break"               # eingebaute <Pfeiltaste> in tk.Listbox verhindern

###############################################################################################################

def Programm_Beenden(event=None):

    global HauptGeo

    if FensterAnders.get() == 1:
        Master.update_idletasks()    # update Fensterwerte
        NeuGeo = str(Master.winfo_width()) + "x" + str(Master.winfo_height()) + "+" + str(Master.winfo_x()) + "+50"
        if not NeuGeo == HauptGeo:
            if message.askokcancel("Stream Recorder", "\n" + TxT["Groesse Fenster"]):
                HauptGeo = NeuGeo
                Schreibe_confDatei()

    if StatusAufnahmen == 0:
        Master.destroy()
    else:
        if message.askokcancel("Stream Recorder", "\n" + TxT["wirklich beenden"]):
            for i in range(len(recPID)):
                try:
                    os.killpg(int(recPID[i]), signal.SIGTERM)
                except:
                    pass
                if not ProtMeldAus.get():  
                    with open(protDatei, "a", encoding="utf-8") as Datei:
                        Datei.write(time.strftime("%d.%m.%y %H:%M > ") + TxT["Beendet Benutzer"] + recName[i] + "\n")
                        Datei.close()
            Master.destroy()

###############################################################################################################

def Statusleiste_Anzeigen(text):

    global Statustext

    Statustext.set(" {:10d}  | {:6d}  | {:6d}  | {:6d}  |   {:s}".format(StatusAnzahl, StatusAufnahmen, StatusBeendete, StatusFehler, text))

###############################################################################################################

def Fenster_Schliessen(fenster):

    fenster.destroy()

###############################################################################################################

Menuleiste = tk.Menu(Master, activebackground=Hintergrund, activeforeground=Vordergrund, font=FontM+SizeM)
Menu_Datei = tk.Menu(Menuleiste, tearoff=0, activebackground=Hintergrund, activeforeground=Vordergrund, font=FontM+SizeM)
Menu_Suchen = tk.Menu(Menuleiste, tearoff=0, activebackground=Hintergrund, activeforeground=Vordergrund, font=FontM+SizeM)
Menu_Favoriten = tk.Menu(Menuleiste, tearoff=0, activebackground=Hintergrund, activeforeground=Vordergrund, font=FontM+SizeM)
Menu_Aufnahme = tk.Menu(Menuleiste, tearoff=0, activebackground=Hintergrund, activeforeground=Vordergrund, font=FontM+SizeM)
Menu_Schedule = tk.Menu(Menuleiste, tearoff=0, activebackground=Hintergrund, activeforeground=Vordergrund, font=FontM+SizeM)
Menu_Hilfe = tk.Menu(Menuleiste, tearoff=0, activebackground=Hintergrund, activeforeground=Vordergrund, font=FontM+SizeM)

Menu_Datei.add_command(label=TxT["Öffnen"], command=Datei_Oeffnen, accelerator=" <Strg+O> ")
Menu_Datei.add_command(label=TxT["Bearbeiten"], command=Datei_Bearbeiten)
Menu_Datei.add_separator()
Menu_Datei.add_command(label=TxT["Player"], command=Player_Auswaehlen, accelerator=" <F5> ")
Menu_Datei.add_command(label=TxT["UserAgent"], command=User_Agent_Aendern)
Menu_Datei.add_command(label=TxT["Einstellungen"], command=Einstellungen, accelerator=" <F9> ")
Menu_Datei.add_separator()
Menu_Datei.add_command(label=TxT["Beenden"], command=Programm_Beenden, accelerator=" <Strg+Q> ")

Menu_Suchen.add_command(label=TxT["nNamen"], command=Suche_Namen)
Menu_Suchen.add_command(label=TxT["nLand"], command=lambda: Suche_Sender(2))
Menu_Suchen.add_command(label=TxT["nGruppe"], command=lambda: Suche_Sender(3))
Menu_Suchen.add_separator()
Menu_Suchen.add_command(label=TxT["SuchSpeich"], command=Suche_Speichern)
Menu_Suchen.add_separator()
Menu_Suchen.add_command(label=TxT["Alle"], command=Alle_Anzeigen, accelerator=" <F3> ")

Menu_Favoriten.add_command(label=TxT["Anzeigen"], command=Favoriten_Anzeigen, accelerator=" <Strg+F> ")
Menu_Favoriten.add_command(label=TxT["Hinzufügen"], command=Favoriten_Hinzufuegen, accelerator=" <F4> ")
Menu_Favoriten.add_command(label=TxT["Bearbeiten"], command=Favoriten_Bearbeiten)
Menu_Favoriten.add_command(label=TxT["Entfernen"], command=Favoriten_Entfernen, accelerator=" <Entf> ")
Menu_Favoriten.add_separator()
Menu_Favoriten.add_command(label=TxT["Eingeben"], command=Favoriten_Eingeben)
Menu_Favoriten.add_separator()
Menu_Favoriten.add_command(label=TxT["Zurück"], command=Favoriten_Zurueck, accelerator=" <F2> ")

Menu_Aufnahme.add_command(label=TxT["Stoppen"], command=Aufnahme_Stoppen, accelerator=" <Strg+T> ")
Menu_Aufnahme.add_command(label=TxT["AlleStop"], command=Alle_Beenden)
Menu_Aufnahme.add_separator()
Menu_Aufnahme.add_command(label=TxT["Manager"], command=Download_Manager, accelerator=" <F7> ")
Menu_Aufnahme.add_separator()
Menu_Aufnahme.add_command(label=TxT["Protokoll"], command=Protokoll_Anzeigen, accelerator=" <Strg+P> ")

Menu_Schedule.add_command(label=TxT["Anzeigen"], command=Schedule_Anzeigen, accelerator=" <Strg+S> ")
Menu_Schedule.add_command(label=TxT["Hinzufügen"], command=Schedule_Hinzufuegen, accelerator=" <F8> ")
Menu_Schedule.add_separator()
Menu_Schedule.add_command(label=TxT["Bearbeiten"], command=Schedule_Bearbeiten)

Menu_Hilfe.add_command(label=TxT["Tastatur"], command=Hilfe_Tastatur, accelerator=" <F1> ")
Menu_Hilfe.add_separator()
Menu_Hilfe.add_command(label=TxT["Über"], command=Hilfe_Ueber)

Menuleiste.add_cascade(label=TxT["Datei"], menu=Menu_Datei, underline=1)
Menuleiste.add_cascade(label=TxT["Suchen"], menu=Menu_Suchen, underline=1)
Menuleiste.add_cascade(label=TxT["Favoriten"], menu=Menu_Favoriten, underline=3)
Menuleiste.add_cascade(label=TxT["Aufnahme"], menu=Menu_Aufnahme, underline=1)
Menuleiste.add_cascade(label=TxT["Schedule"], menu=Menu_Schedule, underline=2)
Menuleiste.add_cascade(label=TxT["Hilfe"], menu=Menu_Hilfe, underline=1)

Scroll_Balken = tk.Scrollbar(Master, width=14)
Listen_Box = tk.Listbox(Master, width=90, yscrollcommand=Scroll_Balken.set)
Statusleiste = tk.Label(Master, textvariable=Statustext, relief="sunken", anchor="w", font="Helvetica 11")
Master.config(menu=Menuleiste)
Scroll_Balken.config(command=Listen_Box.yview)
Listen_Box.config(bg=Hintergrund, fg=Vordergrund, font="Consolas "+SizeL)
Statusleiste.pack(side="bottom", fill="x", padx=2, pady=1)
Scroll_Balken.pack(side="right", fill="y", padx=1, pady=1)
Listen_Box.pack(fill="both", padx=2, pady=1, expand=True)

Listen_Box.bind("<Double-Button-1>", Stream_Anschauen)
Listen_Box.bind("<Button-2>", Stream_Aufnehmen)
Listen_Box.bind("<Button-3>", Player_Auswaehlen)
Listen_Box.bind("<Home>", Liste_Anzeigen)
Listen_Box.bind("<End>", lambda event: Listenende_Anzeigen())       # eingebaute <Ende-Taste> in tk.Listbox umgehen
Listen_Box.bind("<Left>", lambda event: Vorheriger_Stream(-1))      # eingebaute <Pfeiltaste> in tk.Listbox umgehen
Listen_Box.bind("<Right>", lambda event: Vorheriger_Stream(1))      # eingebaute <Pfeiltaste> in tk.Listbox umgehen
Listen_Box.bind("<Return>", Stream_Anschauen)
Listen_Box.bind("<space>", Stream_Aufnehmen)
Listen_Box.bind("<Delete>", Favoriten_Entfernen)
Listen_Box.bind("<F1>", Hilfe_Tastatur)
Listen_Box.bind("<F2>", Favoriten_Zurueck)
Listen_Box.bind("<F3>", Alle_Anzeigen)
Listen_Box.bind("<F4>", Favoriten_Hinzufuegen)
Listen_Box.bind("<F5>", Player_Auswaehlen)
Listen_Box.bind("<F6>", User_Agent_Aendern)
Listen_Box.bind("<F7>", Download_Manager)
Listen_Box.bind("<F8>", Schedule_Hinzufuegen)
Listen_Box.bind("<F9>", Einstellungen)
Listen_Box.bind("<Control-Key-t>", Aufnahme_Stoppen)
Listen_Box.bind("<Control-Key-p>", Protokoll_Anzeigen)
Listen_Box.bind("<Control-Key-f>", Favoriten_Anzeigen)
Listen_Box.bind("<Control-Key-a>", Favoriten_Bearbeiten)
Listen_Box.bind("<Control-Key-n>", Favoriten_Eingeben)
Listen_Box.bind("<Control-Key-o>", Datei_Oeffnen)
Listen_Box.bind("<Control-Key-e>", Datei_Bearbeiten)
Listen_Box.bind("<Control-Key-s>", Schedule_Anzeigen)
Listen_Box.bind("<Control-Key-d>", Schedule_Bearbeiten)
Listen_Box.bind("<Control-Key-q>", Programm_Beenden)
Listen_Box.bind("<Alt-Key-Up>", lambda event: Favoriten_Hochschieben())        # eingebaute <Alt-Hoch-Taste> in tk.Listbox umgehen
Listen_Box.bind("<Alt-Key-Down>", lambda event: Favoriten_Runterschieben())    # eingebaute <Alt-Runter-Taste> in tk.Listbox umgehen

#-----------------------------------------------------

Schedule_Starten()      # Schedule einmal pro Minute nach Terminen durchsuchen

Datei_Oeffnen()         # StartDatei laden oder Playlist auswählen

Master.protocol("WM_DELETE_WINDOW", Programm_Beenden)

Master.mainloop()

###############################################################################################################

