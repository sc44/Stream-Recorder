#! /usr/bin/env python3
#
#  StreamRecorder v1.45 extend - Update: 23.02.2022
#
###############################################################################################################

import tkinter as tk
import tkinter.filedialog as fdialog
import tkinter.colorchooser as chooser
import tkinter.messagebox as message
import os
import subprocess
import signal
import time
import datetime
import locale
import urllib.request
import urllib.error

###############################################################################################################

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

Wochentag = [0,0,0,0,0,0,0,0] 
WochenText = "-------"
Suchbereich = 0
Suchbegriff = ""

StatusAnzahl = 0
StatusAufnahmen = 0
StatusBeendete = 0
StatusFehler = 0

HauptGeo = "770x875"
Vordergrund = "#ffffcc"
Hintergrund = "#000066"
FensterVG = "#000000"
FensterHG = "#ffff88"
FontM = "Helvetica "
SizeM = "11"
SizeL = "10"
Gebiet = "de"

m3uDatei = ""
m3uMerker = ""
startDatei = ""

recVerzeichnis = os.path.expanduser("~") + "/Videos/"
m3uVerzeichnis = os.path.expanduser("~") + "/Downloads/"
confVerzeichnis = os.path.expanduser("~") + "/.config/srecorder/"
cacheVerzeichnis = os.path.expanduser("~") + "/.cache/srecorder/"

protDatei = os.path.expanduser("~") + "/.cache/srecorder/protocol.txt"
schedDatei = os.path.expanduser("~") + "/.cache/srecorder/schedule.txt"
confDatei = os.path.expanduser("~") + "/.config/srecorder/srecorder.conf"
keyDatei = os.path.expanduser("~") + "/.config/srecorder/keyboard.conf"
playerDatei = os.path.expanduser("~") + "/.config/srecorder/splayer.conf"
uaDatei = os.path.expanduser("~") + "/.config/srecorder/useragent.conf"
cmdDatei = os.path.expanduser("~") + "/.config/srecorder/scomand.conf"

keyListe = [ \
"View stream:          <Return>",
"Record stream:        <space>",
"Keyboard shortcuts:   <F1>",
"Previous playlist:    <F2>",
"Search filter off:    <F3>",
"Select player:        <F4>",
"Select user agent:    <F5>",
"Download manager:     <F6>",
"Settings:             <F7>",
"Enter new stream:     <F8>",
"Set new timer:        <F9>",
"Terminate recording:  <Control-Key-t>",
"View protocol:        <Control-Key-p>",
"View favorites:       <Control-Key-f>",
"Add to favorites:     <Control-Key-a>",
"Open new playlist:    <Control-Key-o>",
"Edit playlist:        <Control-Key-e>",
"View schedule:        <Control-Key-s>",
"Edit schedule:        <Control-Key-d>",
"Quit program:         <Control-Key-q>" ]

pListe = [ \
'FFplay                  ffplay "URL[Nr]"',
'FFplay  1280x720        ffplay -x 1280 -y 720 -window_title ffplay "URL[Nr]"',
'SMPlayer                smplayer "URL[Nr]"',
'SMPlayer  1280x720      smplayer "URL[Nr]" -size 1280 870',
'SMPlayer  Windows-GUI   smplayer "URL[Nr]" -mpcgui',
'MPV  Media Player       mpv "URL[Nr]"',
'MPV  (UMPV) one Inst.   umpv "URL[Nr]"',
'Celluloid  (Gnome-MPV)  celluloid "URL[Nr]"',
'MPlayer                 mplayer "URL[Nr]"',
'MPlayer  1280x720       mplayer "URL[Nr]" -geometry 1280x720',
'Gnome-MPlayer           gnome-mplayer "URL[Nr]"',
'VLC  Media Player       vlc "URL[Nr]"',
'SVLC  simple Interface  svlc  "URL[Nr]"',
'CVLC  without Interface cvlc "URL[Nr]"',
'FFmpeg | mpv            ffmpeg -i "URL[Nr]" -c:v copy -c:a copy -f mpegts - | mpv -',
'FFmpeg > /dev/nul | mpv ffmpeg -i "URL[Nr]" -c:v copy -c:a copy -f mpegts - 2> /dev/null | mpv -' ]

uaListe = [ \
'Windows 10 / Chrome 75        Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Safari/537.36',
'Windows 10 / Chrome 64 Edge   Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36 Edge/18.17763',
'Windows 10 / Firefox 86       Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0',
'Windows 10 / Firefox 60 ESR   Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:60.7) Gecko/20100101 Firefox/60.7',
'Windows 6.1 / Firefox 52      Mozilla/5.0 (Windows NT 6.1; rv:52.0) Gecko/20100101 Firefox/52.0',
'Windows 6.1 / IE 11           Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
'Linux / Firefox 67            Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0',
'Mac OS X / Safari 12          Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Safari/605.1.15',
'Android Phone / Chrome 75     Mozilla/5.0 (Linux; Android 9.0; Z832 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Mobile Safari/537.36',
'Android Phone / Firefox 67    Mozilla/5.0 (Android 9.0; Mobile; rv:67.0) Gecko/67.0 Firefox/67.0',
'Android Tablet / Chrome 75    Mozilla/5.0 (Linux; Android 9.0; SAMSUNG-SM-T377A Build/NMF26X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.80 Mobile Safari/537.36',
'Android Tablet / Firefox 67   Mozilla/5.0 (Android 9.0; Tablet; rv:67.0) Gecko/67.0 Firefox/67.0',
'iPhone / Safari 12.1.1        Mozilla/5.0 (iPhone; CPU OS 10_14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/14E304 Safari/605.1.15',
'iPad / Safari 12.1.1          Mozilla/5.0 (iPad; CPU OS 10_14_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.1.1 Mobile/15E148 Safari/605.1.15',
'Google Bot                    Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)' ]

cmdListe = [ \
'ffmpeg -i "link" -c:v copy -c:a copy "file" 2> /dev/null',
'ffmpeg -i $(youtube-dl -g -f best --no-playlist "link") -c:v copy -c:a copy "file" 2> /dev/null',
'ffmpeg -i $(yt-dlp -g -f b --no-playlist "link") -c:v copy -c:a copy "file" 2> /dev/null',
'yt-dlp -F "link"      # List available formats of video or playlist.',
'yt-dlp "link" -P "file".dir      # Download video or playlist into path.' ]

Woerterbuch = { \
"de" : {"Datei":" Datei ","Suchen":" Suchen ","Favoriten":" Favoriten ","Aufnahme":" Aufnahme ","Schedule":" Schedule ",
        "Hilfe":" Hilfe ","??ffnen":"  ??ffnen ","Bearbeiten":"  Bearbeiten ","Player":"  Player ausw??hlen ","Info":"  Info ",
        "UserAgent":"  User-Agent ??ndern ","Einstellungen":"  Einstellungen ","Beenden":"  Beenden ","nNamen":"  Nach Namen ",
        "nLand":"  Nach Land ","nGruppe":"  Nach Gruppe ","Alle":"  Alle anzeigen ","Anzeigen":"  Anzeigen ","??ber":"  ??ber ",
        "Hinzuf??gen":"  Hinzuf??gen ","Entfernen":"  Entfernen ","Zur??ck":"  Zur??ck ","Stoppen":"  Anzeigen / Stoppen ",
        "AlleStop":"  Alle beenden ","Protokoll":"  Protokoll anzeigen ","Tastatur":"  Tastatur ","sDatei":"Start-Playlist:",
        "Schrift Men??":"Schriftgr????e des Men??s eingeben: ", "Schrift Liste":"Schriftgr????e der Playlist eingeben: ",
        "VGfarbe":"Vordergrundfarbe einstellen","HGfarbe":"Hintergrundfarbe einstellen","FFschema":"Fensterfarbschema ausw??hlen",
        "pVerzeichnis":" Playlist-Verzeichnis:","rVerzeichnis":" Aufnahme-Verzeichnis:","Laufende Aufnahmen":"Laufende Aufnahmen",
        "Speichern":"Speichern","Abbrechen":"Abbrechen","Datei speichern":" Speichern mit <Ctrl+S> oder <Doppelklick-Rechts> ",
        "Aufnahme stoppen":" Aufnahme stoppen mit <Doppelklick-Links>","Deutsch":"  Deutsch  ","Englisch":"  Englisch ",
        "wirklich beenden":" Sollen wirklich alle Aufnahmen beendet werden?  ","wirklich entfernen":" wirklich entfernen?  ",
        "SuchSpeich":"  Suche speichern","kein Suchfilter":" Zuerst einen Suchfilter setzen.  ","Unbenannt":"Unbenannt",
        "Sender speichern":"Ausgew??hlte Sender speichern unter:","Eingeben":"  Neuer Stream","Gruppe":"Gruppe:","Land":"Land:",
        "Sprache":"Sprache:","Youtube an":"   youtube-dl beim Programmstart einbinden","Beendet Schedule":"Beendet von Timer      - ",
        "Kein Sender":" Kein Sender ausgew??hlt.  ","nicht installiert":" nicht installiert.  ","nicht gefunden":" nicht gefunden.  ",
        "Zeilenumbruch":"   Keinen Zeilenumbruch in Datei Bearbeiten","Protokoll aus":"   Keine Meldungen ins Protokoll schreiben",
        "Mo":"Mo","Di":"Di","Mi":"Mi","Do":"Do","Fr":"Fr","Sa":"Sa","So":"So","Gestartet Schedule":"Start von Timer    - ",
        "Gestartet Benutzer":"Start von Benutzer - ","Beendet Benutzer":"Beendet von Benutzer   - ","Manager":"  Download-Manager",
        "Groesse Fenster":"Die Gr????e des Hauptfensters wurde ge??ndert.  \n\nSoll die neue Gr????e gespeichert werden?  ",
        "Entwickelt":" ++++ Entwickelt von Woodstock & sc44 ++++ Dieses Programm wird unter den Bedingungen der GNU General Public License ver??ffentlicht, Copyright (C) 2022."},

"en" : {"Datei":" File ","Suchen":" Search ","Favoriten":" Favorites ","Aufnahme":" Recording ","Schedule":" Schedule ",
        "Hilfe":" Help ","??ffnen":"  Open ","Bearbeiten":"  Edit ","Player":"  Player ","Info":"  Info ",
        "UserAgent":"  User-Agent ","Einstellungen":"  Settings ","Beenden":"  Exit ","nNamen":"  Name ",
        "nLand":"  Country ","nGruppe":"  Category ","Alle":"  List all ","Anzeigen":"  Display ","??ber":"  About ",
        "Hinzuf??gen":"  Add ","Entfernen":"  Delete ","Zur??ck":"  Back ","Stoppen":"  Disp / Stop ",
        "AlleStop":"  Stop all ","Protokoll":"  Protocol ","Tastatur":"  Keyboard ","FFschema":" Select window color scheme ",
        "Schrift Men??":"Set the font size of the menu: ", "Schrift Liste":"Set the font size of the playlist: ",
        "VGfarbe":"     Set foreground color     ","HGfarbe":"    Set background color    ","sDatei":"Start playlist:",
        "pVerzeichnis":" Playlist directory:","rVerzeichnis":" Recording directory:","Laufende Aufnahmen":"Active recordings",
        "Speichern":"    Save    ","Abbrechen":"     Exit     ","Datei speichern":" Save file with <Ctrl+S> or <Right double click> ",
        "Aufnahme stoppen":" Stop recording with <Left double click>","Deutsch":"  German  ","Englisch":"  English  ",
        "wirklich beenden":" Are you sure you want to stop all recordings?  ","wirklich entfernen":" really remove?  ",
        "SuchSpeich":"  Save search","kein Suchfilter":" First set a search filter.  ","Unbenannt":"Unnamed",
        "Sprache":"Language:","Youtube an":"   Include youtube-dl at program start","Beendet Schedule":"Terminated by timer    - ",
        "Sender speichern":"Selected channels save as:","Eingeben":"  New stream","Gruppe":"Group:","Land":"Country:",
        "Kein Sender":" No channel selected.  ","nicht installiert":" not installed.  ","nicht gefunden":" not found.  ",
        "Zeilenumbruch":"   Don't wrap lines in the file edit window ","Protokoll aus":"   Don't write any messages in the logfile",
        "Mo":"Mon","Di":"Tue","Mi":"Wed","Do":"Thu","Fr":"Fri","Sa":"Sat","So":"Sun","Gestartet Schedule":"Started by timer   - ",
        "Gestartet Benutzer":"Started by user    - ","Beendet Benutzer":"Terminated by user     - ","Manager":"  Set download",
        "Groesse Fenster":"The size of main window has been changed.  \n\nDo you want to save the new size?  ",
        "Entwickelt":" +++++ Developed by Woodstock & sc44 +++++ This program is published under the terms of the GNU General Public License, Copyright (C) 2022."} }  

###############################################################################################################

Master = tk.Tk()
Master.title("Stream Recorder v1.45 ext")
Master.option_add("*Dialog.msg.font", "Helvetica 11")        # Messagebox Schriftart
Master.option_add("*Dialog.msg.wrapLength", "50i")           # Messagebox Zeilenumbruch

if os.path.isfile("/usr/share/icons/hicolor/128x128/apps/srecorder.png"):
    Master.iconphoto(False, tk.PhotoImage(file="/usr/share/icons/hicolor/128x128/apps/srecorder.png"))

GebietButton = tk.StringVar()                # Gebietsschema
Statustext = tk.StringVar()                  # Statuszeile
Lauftext = tk.StringVar()                    # Laufschrift
Zeilenumbruch = tk.IntVar()                  # Zeilenumbruch an/aus
ProtMeldAus = tk.IntVar()                    # Protokollmeldungen an/aus
youtube_dl = tk.IntVar()                     # Nummer der Kommandozeile

if locale.getlocale()[0][0:2] == "de":  Gebiet = "de"
else:                                   Gebiet = "en"
youtube_dl.set(0)
Zeilenumbruch.set(1)    
ProtMeldAus.set(0)

recPID.clear()                               # Aufnahme: PID, Name, Startzeit, Endezeit l??schen
recName.clear()
recStart.clear()
recEnde.clear()
altName.clear()                              # vorher geschaute Sender
altLink.clear()

###############################################################################################################

def Schreibe_confDatei():

    with open(confDatei, "w") as Datei:
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
        Datei.write("youtube=" + str(youtube_dl.get()) + "\n")
        Datei.write("nowrap=" + str(Zeilenumbruch.get()) + "\n")
        Datei.write("noprot=" + str(ProtMeldAus.get()) + "\n")
        Datei.close()

###############################################################################################################

if not os.path.isdir(confVerzeichnis):       # Verzeichnisse erstellen wenn nicht vorhanden
    os.makedirs(confVerzeichnis)
if not os.path.isdir(cacheVerzeichnis):
    os.makedirs(cacheVerzeichnis)

if os.path.isfile(confDatei):                # wenn Konfigurationsdatei existiert dann laden
    with open(confDatei, "r") as Datei:
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
            if Puffer[i][0:8] == "youtube=":   youtube_dl.set(int(Puffer[i][8:9])) 
            if Puffer[i][0:7] == "nowrap=":    Zeilenumbruch.set(int(Puffer[i][7:8]))    
            if Puffer[i][0:7] == "noprot=":    ProtMeldAus.set(int(Puffer[i][7:8]))    

Schreibe_confDatei()                         # Neue Konfigurationsdatei schreiben  

TxT = Woerterbuch[Gebiet]                    # Zeiger auf aktuelle Sprache

Master.geometry(HauptGeo)                    # Hauptfenstergr??sse einstellen

if os.path.isfile(playerDatei):              # wenn Player-Datei existiert dann laden
    with open(playerDatei, "r") as Datei:
        pListe.clear() 
        for Zeile in Datei:
            pListe.append(Zeile.rstrip())
        Datei.close()
else:                                        # sonst neue Player-Datei erstellen
    with open(playerDatei, "w") as Datei:
        for i in range(len(pListe)):
            Datei.write(pListe[i] + "\n")
        Datei.close()
cmdPlayer = pListe[0][24:]                   # Player-Kommandozeile (default = 1.Zeile)

if os.path.isfile(uaDatei):                  # wenn User-Agent-Datei existiert dann laden
    with open(uaDatei, "r") as Datei:
        uaListe.clear() 
        for Zeile in Datei:
            uaListe.append(Zeile.rstrip())
        Datei.close()
else:                                        # sonst neue User-Agent-Datei erstellen
    with open(uaDatei, "w") as Datei:
        for i in range(len(uaListe)):
            Datei.write(uaListe[i] + "\n")
        Datei.close()
UserAgent = uaListe[0][30:]                  # User-Agent-Eintrag (defaut = 1.Zeile)

if os.path.isfile(cmdDatei):                 # wenn Aufnahmeprogramm-Datei existiert dann laden
    with open(cmdDatei, "r") as Datei:
        cmdListe.clear() 
        for Zeile in Datei:
            cmdListe.append(Zeile.rstrip())
        Datei.close()
else:                                        # sonst neue Aufnahmeprogramm-Datei erstellen
    with open(cmdDatei, "w") as Datei:
        for i in range(5):
            Datei.write(cmdListe[i] + "\n")
        Datei.close()

if os.path.isfile(keyDatei):                 # wenn Tastaturbelegungsdatei existiert dann laden
    with open(keyDatei, "r") as Datei:
        keyListe.clear() 
        for Zeile in Datei:
            keyListe.append(Zeile.rstrip())
        Datei.close()
else:                                        # sonst neue Tastaturbelegungsdatei erstellen
    with open(keyDatei, "w") as Datei:
        for i in range(len(keyListe)):
            Datei.write(keyListe[i] + "\n")
        Datei.close()

if not os.path.isdir(m3uVerzeichnis):        # Verzeichnisse erstellen wenn nicht vorhanden
    os.makedirs(m3uVerzeichnis)
if not os.path.isdir(recVerzeichnis):
    os.makedirs(recVerzeichnis)
if not os.path.isfile("/usr/bin/ffmpeg") and not os.path.isfile("/usr/local/bin/ffmpeg"):
    message.showwarning("Stream Recorder", "\n FFmpeg" + TxT["nicht installiert"])

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
            with open(m3uDatei, "r") as Datei:
                Puffer.clear() 
                for Zeile in Datei:
                    if not (Zeile == "\n" or Zeile[0:11] == "#EXTVLCOPT:"):    # Leerzeile und User Agent ??berspringen
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
            with open(m3uDatei, "r") as Datei:
                for Zeile in Datei:
                    if not (Zeile == "\n" or Zeile[0:11] == "#EXTVLCOPT:"):
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
        Text_Fenster.config(foreground=FensterVG, background=FensterHG, font="Monospace 10", wrap=umbruch, undo="TRUE")
        Zeile_Info = tk.Label(Fenster, font="Helvetica 10", text=TxT["Datei speichern"])
        Scroll_Vertikal.config(command = Text_Fenster.yview)
        Scroll_Horizont.config(command = Text_Fenster.xview)
        Zeile_Info.pack(side="bottom", fill="x", padx=2, pady=0)
        Scroll_Vertikal.pack(side="right", fill="y", padx=1, pady=1)
        Scroll_Horizont.pack(side="bottom", fill="x", padx=1, pady=1)
        Text_Fenster.pack(fill="both", padx=2, pady=2)
        with open(m3uDatei, "r") as Datei:
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
    Listen_Box.selection_set(0)
    Listen_Box.focus_set()                # Scrollbalken auf ersten Eintrag setzen
    StatusAnzahl = len(Name)
    Statusleiste_Anzeigen("")

###############################################################################################################

def Listenende_Anzeigen():

    global StatusAnzahl

    Listen_Box.delete(0, tk.END) 
    for i in range(len(Name)):
        Listen_Box.insert(tk.END, "{:6d}    {:40.39s} {:8.7s} {:17.16s} {:14.14s}".format(PufNr[i], Name[i], Land[i], Sprache[i], Gruppe[i]))
    Listen_Box.activate("end")
    Listen_Box.selection_set("end")
    Listen_Box.focus_set()                # Scrollbalken auf letzten Eintrag setzen
    Listen_Box.see("end")
    StatusAnzahl = len(Name)
    Statusleiste_Anzeigen("")
    return "break"                        # eingebautes <Ende> in tk.Listbox verhindern

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

        Suchbereich = 1
        Suchbegriff = Eingabefeld.get()
        Fenster.destroy()
        Listen_Loeschen()
        for i in range(1, len(Puffer)-1, 2):            # Puffer durchsuchen
            x = Puffer[i].find(",")
            if Suchbegriff in Puffer[i][x+1:].rstrip():
                Zeilenpuffer_Auswerten(i)
        Liste_Anzeigen()

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Suchen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    Fenstertext = tk.Label(Fenster, text=TxT["nNamen"]+":", font="Helvetica 12")
    Eingabefeld = tk.Entry(Fenster, bd=4, width=12, font="Helvetica 11")
    ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Anzeigen"], font="Helvetica 11", command=Namen_Anzeigen)
    Fenstertext.pack(pady=20)
    Eingabefeld.pack(padx=50)
    ButtonSpeichern.pack(pady=30, ipadx=4)

    Eingabefeld.insert(0, "")
    Eingabefeld.focus_set()
    Eingabefeld.bind("<Return>", Namen_Anzeigen)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Suche_Land():

    def Land_Anzeigen(event=None):

        global Suchbereich, Suchbegriff

        Suchbereich = 2
        Suchbegriff = Eingabefeld.get()
        Fenster.destroy()
        Listen_Loeschen()
        for i in range(1, len(Puffer)-1, 2):            # Puffer durchsuchen
            x = Puffer[i].find("tvg-country=")
            y = Puffer[i].find('"', x+13)
            if Puffer[i][x+13:y] == Suchbegriff:
                Zeilenpuffer_Auswerten(i)
        Liste_Anzeigen()

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Suchen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    Fenstertext = tk.Label(Fenster, text=TxT["nLand"]+":", font="Helvetica 12")
    Eingabefeld = tk.Entry(Fenster, bd=4, width=12, font="Helvetica 11")
    ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Anzeigen"], font="Helvetica 11", command=Land_Anzeigen)
    Fenstertext.pack(pady=20)
    Eingabefeld.pack(padx=50)
    ButtonSpeichern.pack(pady=30, ipadx=4)

    Eingabefeld.insert(0, "DE")
    Eingabefeld.focus_set()
    Eingabefeld.bind("<Return>", Land_Anzeigen)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Suche_Gruppe():

    def Gruppe_Anzeigen(event=None):

        global Suchbereich, Suchbegriff

        Suchbereich = 3
        Suchbegriff = Eingabefeld.get()
        Fenster.destroy()
        Listen_Loeschen()
        for i in range(1, len(Puffer)-1, 2):            # Puffer durchsuchen
            x = Puffer[i].find("group-title=")
            if Puffer[i][x+13:x+16] == Suchbegriff[0:3]:
                Zeilenpuffer_Auswerten(i)
        Liste_Anzeigen()

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Suchen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    Fenstertext = tk.Label(Fenster, text=TxT["nGruppe"]+":", font="Helvetica 12")
    Eingabefeld = tk.Entry(Fenster, bd=4, width=12, font="Helvetica 11")
    ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Anzeigen"], font="Helvetica 11", command=Gruppe_Anzeigen)
    Fenstertext.pack(pady=20)
    Eingabefeld.pack(padx=50)
    ButtonSpeichern.pack(pady=30, ipadx=4)

    Eingabefeld.insert(0, "Music")
    Eingabefeld.focus_set()
    Eingabefeld.bind("<Return>", Gruppe_Anzeigen)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Suche_Speichern():

    def Datei_Speichern(event=None):

        with open(Eingabefeld.get(), "w") as Datei:
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
                    if Puffer[i][x+13:x+16] == Suchbegriff[0:3]:
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
        Fenstertext.pack(pady=25)
        Eingabefeld.pack(padx= 40)
        ButtonSpeichern.pack(pady=25, ipadx=23, expand=True, side="left", padx=40)
        ButtonAbbrechen.pack(pady=25, ipadx=20, expand=True, side="left", anchor="w")

        dName = os.path.basename(m3uDatei)              # Vorgabe f??r Dateinamen erstellen
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
        m3uMerker = m3uDatei
        m3uDatei = m3uVerzeichnis + "favoriten.m3u"
        Puffer.clear()
        with open(m3uDatei, "r") as Datei:
            for Zeile in Datei:
                if not (Zeile == "\n" or Zeile[0:11] == "#EXTVLCOPT:"):
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
            with open(FavName, "w") as Datei:
                Datei.write("#EXTM3U\n")            #  dann 1. Zeile schreiben (Dateikennung)
                Datei.close()
        with open(FavName, "a") as Datei:           # 2 Zeilen an favoriten.m3u anh??ngen
            Datei.write(Puffer[i*2-1])              #  Beschreibung  
            Datei.write(Puffer[i*2])                #  URL
            Datei.close()

###############################################################################################################

def Favoriten_Eingeben(event=None):

    def Eintrag_Hinzufuegen(event=None):

        FavName = m3uVerzeichnis + "favoriten.m3u"
        if not os.path.isfile(FavName):             # wenn keine Favoriten-Datei gefunden
            with open(FavName, "w") as Datei:
                Datei.write("#EXTM3U\n")            # 1.Zeile schreiben (Header)
                Datei.close()
        with open(FavName, "a") as Datei:
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
    Fenster.title(TxT["Eingeben"])
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
    TextGruppe.grid(row=2, column=1, padx=20, pady=10, sticky="w")
    EingabeGruppe.grid(row=2, column=2, padx=1, pady=10)
    TextLand.grid(row=2, column=3, padx=20, pady=10, sticky="w")
    EingabeLand.grid(row=2, column=4, padx=1, pady=10)
    TextSprache.grid(row=2, column=5, padx=20, pady=10, sticky="w")
    EingabeSprache.grid(row=2, column=6, padx=1, pady=10)
    TextLink.grid(row=3, column=1, padx=20, pady=10, sticky="w")
    EingabeLink.grid(row=3, column=2, columnspan=5, padx=1, pady=10, sticky="w")
    ButtonSpeichern.grid(row=4, column=2, columnspan=3, pady=10, ipadx=23, sticky="w")
    ButtonAbbrechen.grid(row=4, column=4, columnspan=3, pady=10, ipadx=20)
    tk.Label(Fenster).grid(row=5, column=0)

    EingabeName.insert(0, TxT["Unbenannt"])
    EingabeName.select_range(0, tk.END)
    EingabeName.focus_set()
    EingabeLink.insert(0, "https://")
    ButtonSpeichern.bind("<Return>", Eintrag_Hinzufuegen)
    ButtonAbbrechen.bind("<Return>", lambda event: Fenster_Schliessen(Fenster))
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))


###############################################################################################################

def Favoriten_Entfernen():

    global Puffer

    if m3uDatei == m3uVerzeichnis + "favoriten.m3u":
        Nr = Listen_Box.curselection()[0]           # Index des markierten Senders
        if message.askyesno("Stream Recorder", "\n" + Name[Nr] + TxT["wirklich entfernen"]):
            Puffer.pop(Nr*2+2)                      # URL l??schen
            Puffer.pop(Nr*2+1)                      # Beschreibung l??schen
            with open(m3uDatei, "w") as Datei:      # Favoriten-Datei neu schreiben (??berschreiben)
                for i in range(0, len(Puffer)):
                    Datei.write(Puffer[i])
                Datei.close()
            Alle_Anzeigen()
            Listen_Box.selection_clear(0)
            Listen_Box.selection_set(Nr-1)          # Scrollbalken einen Eintrag zur??ck
            Listen_Box.activate(Nr-1)
            Listen_Box.focus_set()
            Listen_Box.see(Nr-1)

###############################################################################################################

def Favoriten_Zurueck(event=None):

    global Puffer, m3uDatei, m3uMerker

    aktuelle = m3uDatei                             # aktuelle Datei merken
    m3uDatei = m3uMerker                            # vorherige Datei neu laden
    m3uMerker = aktuelle

    if os.path.isfile(m3uDatei):
        with open(m3uDatei, "r") as Datei:
            Puffer.clear()
            for Zeile in Datei:
                if not (Zeile == "\n" or Zeile[0:11] == "#EXTVLCOPT:"):    # Leerzeile und User Agent ??berspringen
                    Puffer.append(Zeile)
            Datei.close()
        Alle_Anzeigen()

###############################################################################################################

def Player_Auswaehlen(event=None):

    def Player_Laden(event):

        global cmdPlayer

        Nr = int(Player_Liste.curselection()[0])         # Index pListe
        x = pListe[Nr][24:].find(" ")
        player = pListe[Nr][24:24+x]                     # Player-Programmname
        if os.path.isfile("/usr/bin/" + player) or os.path.isfile("/usr/local/bin/" + player):
            cmdPlayer = pListe[Nr][24:]
            Fenster.destroy()
        else:
            message.showwarning("Stream Recorder", "\n " + player + TxT["nicht installiert"], parent=Fenster)
            cmdPlayer = pListe[0][24:]

    Fenster = tk.Toplevel(Master)
    Fenster.title("Player")
    Fenster.wm_attributes("-topmost", True)
    #Fenster.wait_visibility()
    time.sleep(0.3)                                      # wegen rechter Maustaste, sonst grab failed !!
    Fenster.grab_set()

    Player_Liste = tk.Listbox(Fenster, width=25, height=20, selectborderwidth=2)
    Player_Liste.config(foreground=FensterVG, background=FensterHG, font="Helvetica 11")
    Player_Liste.pack(fill="both", padx=3, pady=3)
    Player_Liste.delete(0, tk.END) 
    for i in range(len(pListe)):
        Player_Liste.insert(tk.END, "    " + pListe[i][0:24])
        if pListe[i][24:] == cmdPlayer:
            aktiv = i
    Player_Liste.activate(aktiv)
    Player_Liste.selection_set(aktiv)                    # Scrollbalken auf aktiven Player
    Player_Liste.focus_set()
    Player_Liste.bind("<Return>", Player_Laden)
    Player_Liste.bind("<Double-Button-1>", Player_Laden)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def User_Agent_Aendern(event=None):

    def UserAgent_Laden(event):

        global UserAgent

        Nr = int(UserAgent_Liste.curselection()[0])      # Index uaListe
        UserAgent = uaListe[Nr][30:]
        Fenster.destroy()

    Fenster = tk.Toplevel(Master)
    Fenster.title("User-Agent")
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    UserAgent_Liste = tk.Listbox(Fenster, width=30, height=20, selectborderwidth=2)
    UserAgent_Liste.config(foreground=FensterVG, background=FensterHG, font="Helvetica 11")
    UserAgent_Liste.pack(fill="both", padx=3, pady=3)
    UserAgent_Liste.delete(0, tk.END) 
    for i in range(len(uaListe)):
        UserAgent_Liste.insert(tk.END, "    " + uaListe[i][0:30])
        if uaListe[i][30:] == UserAgent:
            aktiv = i
    UserAgent_Liste.activate(aktiv)
    UserAgent_Liste.selection_set(aktiv)                 # Scrollbalken auf aktiven User-Agent
    UserAgent_Liste.focus_set()
    UserAgent_Liste.bind("<Return>", UserAgent_Laden)
    UserAgent_Liste.bind("<Double-Button-1>", UserAgent_Laden)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Download_Manager(event=None):

    def Kommando_Speichern(event=None):

        cmdListe.clear()                            # Kommando-Liste neu laden
        for i in range(5):
            cmdListe.append(EingabeZeile[i].get())
        with open(cmdDatei, "w") as Datei:          # Kommando-Datei schreiben
            for i in range(5):
                Datei.write(EingabeZeile[i].get() + "\n")
            Datei.close()
        Schreibe_confDatei()                        # Konfigurationsdatei schreiben  
        Fenster.destroy()


    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Manager"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    EingabeZeile1 = tk.Entry(Fenster, bd=3, width=70, font="Helvetica 11")
    EingabeZeile2 = tk.Entry(Fenster, bd=3, width=70, font="Helvetica 11")
    EingabeZeile3 = tk.Entry(Fenster, bd=3, width=70, font="Helvetica 11")
    EingabeZeile4 = tk.Entry(Fenster, bd=3, width=70, font="Helvetica 11")
    EingabeZeile5 = tk.Entry(Fenster, bd=3, width=70, font="Helvetica 11")
    EingabeZeile = [EingabeZeile1, EingabeZeile2, EingabeZeile3, EingabeZeile4, EingabeZeile5]

    tk.Label(Fenster).grid(row=0,column=0, pady=2, columnspan=4)
    for i in range(5):
        tk.Label(Fenster).grid(row=i+1,column=0, padx=10, pady=6)
        tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=youtube_dl, value=i).grid(row=i+1, column=1, padx=7, pady=6)
        tk.Label(Fenster, text=str(i+1), font="Helvetica 9").grid(row=i+1,column=2, ipadx=5, pady=6)
        EingabeZeile[i].grid(row=i+1, column=3, padx=0, pady=6)
        EingabeZeile[i].insert(0, cmdListe[i][0:])
        tk.Label(Fenster).grid(row=i+1,column=4, padx=15, pady=6)

    ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Speichern"], font="Helvetica 11", command=Kommando_Speichern)
    ButtonAbbrechen = tk.Button(Fenster, bd=3, text=TxT["Abbrechen"], font="Helvetica 11", command=Fenster.destroy)
    ButtonSpeichern.grid(row=8, column=0, padx=105, pady=20, ipadx=43, columnspan=4,sticky="w")
    ButtonAbbrechen.grid(row=8, column=0, padx=105, pady=20, ipadx=40, columnspan=4,sticky="e")
    ButtonSpeichern.bind("<Return>", Kommando_Speichern)
    ButtonAbbrechen.bind("<Return>", lambda event: Fenster_Schliessen(Fenster))
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Stream_Anschauen(event=None):

    x = cmdPlayer.find(" ")
    player = cmdPlayer[0:x]                              # Player-Programmname
    if not os.path.isfile("/usr/bin/" + player) and not os.path.isfile("/usr/local/bin/" + player):
        message.showwarning("Stream Recorder", "\n" + player + TxT["nicht installiert"])
        return

    global altName, altLink, altPos

    if Listen_Box.curselection():
        Nr = Listen_Box.curselection()[0]                # Index des markierten Senders
        cmdStrg = cmdPlayer.replace("URL[Nr]", URL[Nr])  # Kommandostring zusammenbauen
        try:                                             # URL pr??fen
            urllib.request.urlopen(urllib.request.Request(URL[Nr], headers={"User-Agent": UserAgent}), timeout=5)
        except urllib.error.HTTPError as err:
            meldung = str(err.code) + ":  " + str(err.reason)
            Statusleiste_Anzeigen(meldung)
        except urllib.error.URLError as err:
            meldung = str(err.reason)
            Statusleiste_Anzeigen(meldung)
        except:
            Statusleiste_Anzeigen("Unexpected error")
        else:                                            # wenn URL g??ltig
            Statusleiste_Anzeigen(Name[Nr])
            subprocess.Popen(cmdStrg, shell=True)        # Player starten
            altName.append(Name[Nr])                     # Namen speichern
            altLink.append(URL[Nr])                      # Link speichern
            altPos = len(altName)-1                      # Position auf Letzten
            Master.focus_force()
            Listen_Box.focus_set()                       # Focus zur??ck auf Programmliste

###############################################################################################################

def Stream_Aufnehmen(event=None):

    def protDatei_Schreiben(text, name):

        if not ProtMeldAus.get():  
            with open(protDatei, "a") as Datei:
                Datei.write(time.strftime("%d.%m.%y %H:%M > ") + text +  name + "\n")
                Datei.close()

    global recPID, recStart, recEnde, recName, StatusAufnahmen, StatusFehler

    if Listen_Box.curselection():
        Nr = Listen_Box.curselection()[0]                # Index des markierten Senders
        try:                                             # URL pr??fen
            urllib.request.urlopen(urllib.request.Request(URL[Nr], headers={"User-Agent": UserAgent}), timeout=5)
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
        else:                                            # wenn URL g??ltig
            Statusleiste_Anzeigen(Name[Nr])
            for n in range(1, 1000):                     # Namen der Aufnahme festlegen (..._001 bis ..._999)
                Dateiname = Name[Nr] + "_" + str(n).zfill(3) + ".ts" 
                if not os.path.isfile(recVerzeichnis + Dateiname):   break   # wenn Dateiname nicht existiert dann ??bernehmen
            cmdStrg = cmdListe[youtube_dl.get()][0:]
            cmdStrg = cmdStrg.replace("link", URL[Nr])                        # Link der Aufnahme in Kommandozeile einbauen
            cmdStrg = cmdStrg.replace("file", recVerzeichnis + Dateiname)     # Namen der Aufnahme in Kommandozeile einbauen
            print(cmdStrg)
            proc = subprocess.Popen(cmdStrg, shell=True, preexec_fn=os.setsid)
            print(proc.pid)
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

        Nr = int(Record_Liste.curselection()[0])         # Index Aufnahmeliste
        try:
            os.killpg(int(recPID[Nr]), signal.SIGTERM)   # Aufnahme stoppen
        except:
            pass
        if not ProtMeldAus.get():  
            with open(protDatei, "a") as Datei:
                Datei.write(time.strftime("%d.%m.%y %H:%M > ") + TxT["Beendet Benutzer"] + recName[Nr] + "\n")
                Datei.close()
        recPID.pop(Nr)                                   # Aufnahme: PID l??schen
        recStart.pop(Nr)                                 # Aufnahme: Startzeit l??schen
        recEnde.pop(Nr)                                  # Aufnahme: Endezeit l??schen
        recName.pop(Nr)                                  # Aufnahme: Namen l??schen
        Record_Liste.delete(Nr)                          # Listeneintrag l??schen
        StatusAufnahmen = len(recPID)
        StatusBeendete += 1
        Statusleiste_Anzeigen("")

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Laufende Aufnahmen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()
    Zeile_Titel = tk.Label(Fenster, anchor="w", text="PID       Start      Stop       Name", font="Helvetica 11")
    Record_Liste = tk.Listbox(Fenster, width=60, height=15)
    Record_Liste.config(foreground=FensterVG, background=FensterHG, font="Monospace 10")
    Zeile_Info = tk.Label(Fenster, font="Helvetica 10", text=TxT["Aufnahme stoppen"])
    Zeile_Info.pack(side="bottom", fill="x", padx=3, pady=2)
    Zeile_Titel.pack(side="top", fill="x", padx=22, pady=2)
    Record_Liste.pack(fill="both", padx=3, pady=1)

    if len(recName) != 0:                  # wenn mind. 1 Aufnahme dann Liste erstellen
        Record_Liste.delete(0, tk.END) 
        for i in range(len(recName)):
            Record_Liste.insert(tk.END, "{:6d} - {:4s} - {:4s} - {:40s}".format(recPID[i], recStart[i], recEnde[i], recName[i]))
        Record_Liste.selection_set(0)
        Record_Liste.focus_set()           # Markierung auf ersten Eintrag setzen
        Record_Liste.bind("<Return>", Aufnahme_Beenden)
        Record_Liste.bind("<Double-Button-1>", Aufnahme_Beenden)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Alle_Beenden():

    global recPID, recStart, recEnde, recName, StatusAufnahmen, StatusBeendete

    if message.askyesno("Stream Recorder", "\n" + TxT["wirklich beenden"]):
        for i in range(len(recPID)):
            try:
                os.killpg(int(recPID[i]), signal.SIGTERM)
            except:
                pass
            if not ProtMeldAus.get():  
                with open(protDatei, "a") as Datei:
                    Datei.write(time.strftime("%d.%m.%y %H:%M > ") + TxT["Beendet Benutzer"] + recName[i] + "\n")
                    Datei.close()
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
            with open(protDatei, "a") as Datei:
                Datei.write(time.strftime("%d.%m.%y %H:%M > ") + text +  name + "\n")
                Datei.close()

    global sPuffer, recPID, recStart, recEnde, recName, StatusAufnahmen, StatusBeendete, StatusFehler

    sPuffer.clear()     # Schedule-Puffer l??schen   (1. Zeile = Tage + Start + Ende + * + Name + LF  /  2. Zeile = URL + LF)

    if os.path.isfile(schedDatei):
        with open(schedDatei, "r") as Datei:          # Schedule-Datei in Puffer laden
            for Zeile in Datei:
                    sPuffer.append(Zeile)
            Datei.close()

    #---------- N??chste Aufnahme(n) starten ----------

    Aktuelle = int(time.strftime("%H%M"))                                 # aktuelle Uhrzeit holen (SSMM)
    w = datetime.datetime.today().weekday()                               # aktuellen Wochentag holen (0-6)

    for i in range(len(sPuffer)-2, -2, -2):                               # vom Ende her durchsuchen (L??schfehler vermeiden)
        Startzeit = int(sPuffer[i][8:10] + sPuffer[i][11:13])             # Startzeit holen (SSMM)

        if Startzeit == Aktuelle and sPuffer[i][w] == "x":                # wenn Uhrzeit und Wochentag stimmen
            try:                                                          # URL pr??fen
                urllib.request.urlopen(urllib.request.Request(sPuffer[i+1].rstrip(), headers={"User-Agent": UserAgent}), timeout=5)
            except urllib.error.HTTPError as err:
                StatusFehler += 1
                Statusleiste_Anzeigen("")
                protmeld = "HTTP error: " + str(err.code) + "        - "
                protDatei_Schreiben(protmeld, sPuffer[i][22:].rstrip())
            except urllib.error.URLError as err:
                StatusFehler += 1
                Statusleiste_Anzeigen("")
                meldung = str(err.reason)
                protDatei_Schreiben("URL error: " + meldung[0:11].ljust(11) + " - ", sPuffer[i][22:].rstrip())
            except:
                StatusFehler += 1
                Statusleiste_Anzeigen("")
                protDatei_Schreiben("Unexpected error       - ", sPuffer[i][22:].rstrip())
            else:                                                         # wenn URL g??ltig
                for n in range(1, 1000):                                  # Namen der Aufnahme festlegen (..._001 bis ..._999)
                    Dateiname = sPuffer[i][22:].rstrip() + "_" + str(n).zfill(3) + ".ts"
                    if not os.path.isfile(recVerzeichnis + Dateiname):   break
                cmdNr = int(sPuffer[i][20])
                if cmdNr == 0:   cmdNr = 4
                elif cmdNr > 5:  cmdNr -= 6 
                else:            cmdNr -= 1
                cmdStrg = cmdListe[cmdNr][0:]
                cmdStrg = cmdStrg.replace("link", sPuffer[i+1].rstrip())          # Link der Aufnahme in Kommandozeile einbauen
                cmdStrg = cmdStrg.replace("file", recVerzeichnis + Dateiname)     # Namen der Aufnahme in Kommandozeile einbauen
                #print(cmdStrg)
                proc = subprocess.Popen(cmdStrg, shell=True, preexec_fn=os.setsid)
                #print(proc.pid)
                if proc.pid:
                    recPID.append(proc.pid)                               # Aufnahme: PID speichern
                    recStart.append(time.strftime("%H%M"))                # Aufnahme: Startzeit speichern
                    recEnde.append(sPuffer[i][14:16] + sPuffer[i][17:19]) # Aufnahme: Endezeit (SSMM) speichern
                    recName.append(sPuffer[i][22:].rstrip())              # Aufnahme: Namen (ohne LF) speichern
                    StatusAufnahmen = len(recPID)
                    Statusleiste_Anzeigen("")
                    protDatei_Schreiben("[" + str(cmdNr+1) + "] " + TxT["Gestartet Schedule"], sPuffer[i][22:].rstrip())

            #---------- Wenn Einmal-Aufnehmen (*) ----------

            if int(sPuffer[i][20]) > 5 or int(sPuffer[i][20]) == 0:
                z = list(sPuffer[i])
                z[w] = "-"                                                # Wochentag in Puffer deaktivieren
                sPuffer[i] = "".join(z)

                if sPuffer[i][0:7] == "-------":                          # wenn keine Wochentage mehr g??ltig
                    sPuffer.pop(i+1)                                      # URL-Zeile l??schen
                    sPuffer.pop(i)                                        # Text-Zeile l??schen 

                with open(schedDatei, "w") as Datei:                      # schedule.txt neu schreiben
                    for i in range(len(sPuffer)):
                        Datei.write(sPuffer[i])
                    Datei.close()

    #---------- N??chste Aufnahme(n) beenden ----------

    for i in range(len(recEnde)-1, -1, -1):            # vom Ende her durchsuchen (L??schfehler vermeiden)
        Endezeit = int(recEnde[i])
        if Endezeit == Aktuelle:
            try:
                os.killpg(int(recPID[i]), signal.SIGTERM)
            except:
                pass
            protDatei_Schreiben(TxT["Beendet Schedule"], recName[i])
            recPID.pop(i)                              # Aufnahme: PID l??schen
            recStart.pop(i)                            # Aufnahme: Startzeit l??schen
            recEnde.pop(i)                             # Aufnahme: Endezeit l??schen
            recName.pop(i)                             # Aufnahme: Namen l??schen
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
        Text_Fenster = tk.Text(Fenster, width=72, height=30, pady=10, padx=10, yscrollcommand=Scroll_Balken.set)
        Text_Fenster.config(foreground=FensterVG, background=FensterHG, font="Monospace 10", wrap="none")
        Scroll_Balken.config(command = Text_Fenster.yview)
        Scroll_Balken.pack(side="right", fill="y", padx=1, pady=1)
        Text_Fenster.pack(fill="both", padx=2, pady=2)
        with open(protDatei, "r") as Datei:
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

    if not os.path.isfile(schedDatei):
        message.showwarning("Stream Recorder", "\n" + schedDatei + TxT["nicht gefunden"])
    else:
        Fenster = tk.Toplevel(Master)
        Fenster.title("Schedule")
        Fenster.wm_attributes("-topmost", True)
        Fenster.grab_set()

        Scroll_Balken = tk.Scrollbar(Fenster, width=14)
        Text_Fenster = tk.Text(Fenster, width=55, height=25, pady=10, padx=10, yscrollcommand=Scroll_Balken.set)
        Text_Fenster.config(foreground=FensterVG, background=FensterHG, font="Monospace 10", wrap="none")
        Scroll_Balken.config(command = Text_Fenster.yview)
        Scroll_Balken.pack(side="right", fill="y", padx=1, pady=1)
        Text_Fenster.pack(fill="both", padx=2, pady=2)

        with open(schedDatei, "r") as Datei:
            Text_Fenster.configure(state="normal")
            Text_Fenster.delete("1.0", tk.END)
            for Zeile in Datei:
                if not Zeile[0:4] == "http":                 # URL nicht anzeigen 
                    Text_Fenster.insert(tk.END, Zeile)
            Text_Fenster.yview(tk.END)                       # das Ende der Datei anzeigen
            Text_Fenster.configure(state="disabled")
            Datei.close()
        Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Schedule_Hinzufuegen(event=None):

    def Eintrag_Speichern(event=None):

        global WochenText

        if int(BoxRec.get()) >= 1 and int(BoxRec.get()) <= 5:    # nur 1-5 akzeptieren
 
            wt = list(WochenText)                      # Wochentage-String zusammenbauen
            for i in range(0, 7, 1):
                if Wochentag[i].get():    wt[i] = "x"  
                else:                     wt[i] = "-"
            WochenText = "".join(wt)

            Start = BoxStart.get()
            Ende = BoxEnde.get()

            if Wiederholung.get() == 1:   
                Rec = BoxRec.get()                     # wenn Dauer-Aufnahme (1-5)
            else:
                Rec = str(int(BoxRec.get())+5)         # wenn Einmal-Aufnahme (6-9,0)
                if Rec == "10":   Rec = "0"

            Nr = Listen_Box.curselection()[0]
            with open(schedDatei, "a") as Datei:
                Datei.write(WochenText + " " + Start + " " + Ende + " " + Rec + " " + Name[Nr] + "\n")
                Datei.write(URL[Nr] + "\n")
                Datei.close()
            Fenster.destroy()

#----------------------------------------------------

    global Wochentag

    if Listen_Box.curselection():
        Nr = Listen_Box.curselection()[0]              # Index des markierten Senders
    else:
        message.showwarning("Schedule", "\n" + TxT["Kein Sender"])
        return
 
    Fenster = tk.Toplevel(Master)
    Fenster.title("Schedule")
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    for i in range(0, 7, 1):
        Wochentag[i] = tk.IntVar()                     # Checkboxen Mo-So auf Null setzen
        Wochentag[i].set(0)

    Wiederholung = tk.IntVar()                         # Einmal-Aufnehmen setzen (default)
    Wiederholung.set(0)

    i = datetime.datetime.today().weekday()            # aktuellen Wochentag setzen
    Wochentag[i].set(1)

    ProgName = tk.Label(Fenster, text=Name[Nr][0:56], font="Helvetica 12")
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
    BoxStart = tk.Entry(Fenster, exportselection=0, relief="sunken", bd=3, width=5, font="Helvetica 11")
    BoxEnde = tk.Entry(Fenster, exportselection=0, relief="sunken", bd=3, width=5, font="Helvetica 11")
    BoxRec = tk.Entry(Fenster, exportselection=0, relief="sunken", bd=3, width=2, font="Helvetica 11")
    Radio9 = tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wiederholung, value=1, text=" ???  ", font="Helvetica 11")
    Radio1 = tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wiederholung, value=0, text=" ???  ", font="Helvetica 11")
    ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Speichern"], font="Helvetica 11", command=Eintrag_Speichern)
    ButtonAbbrechen = tk.Button(Fenster, bd=3, text=TxT["Abbrechen"], font="Helvetica 11", command=Fenster.destroy)

    TextTag = [TextMo, TextDi, TextMi, TextDo, TextFr, TextSa, TextSo]     # Variablenliste f??r Wochentage
    BoxTag = [BoxMo, BoxDi, BoxMi, BoxDo, BoxFr, BoxSa, BoxSo]

    ProgName.grid(row=0, column=2, padx=0, pady=20, columnspan=13)
    tk.Label(Fenster).grid(row=1, column=1, padx=10)
    for i in range (7):
        TextTag[i].grid(row=1, column=i+2, padx=2, pady=4)
    TextStart.grid(row=1, column=9, padx=30, pady=4)
    TextEnde.grid(row=1, column=10, padx=0, pady=4)
    TextRec.grid(row=1, column=11, padx=25, pady=4)
    Radio9.grid(row=1, column=12, padx=2, pady=4)
    tk.Label(Fenster).grid(row=1, column=13, padx=10)
    tk.Label(Fenster).grid(row=2, column=1, padx=10)
    for i in range (7):
        BoxTag[i].grid(row=2, column=i+2, padx=1, pady=4)
    BoxStart.grid(row=2, column=9, padx=30, pady=4)
    BoxEnde.grid(row=2, column=10, padx=0, pady=4)
    BoxRec.grid(row=2, column=11, padx=25, pady=4)
    Radio1.grid(row=2, column=12, padx=2, pady=4)
    tk.Label(Fenster).grid(row=2, column=13, padx=10)
    ButtonSpeichern.grid(row=3, column=4, padx=15, pady=20, ipadx=23, columnspan=5)
    ButtonAbbrechen.grid(row=3, column=9, padx=0, pady=20, ipadx=20, columnspan=4)
    tk.Label(Fenster).grid(row=4, column=1, padx=10)

    BoxStart.insert(0, time.strftime("%H:%M"))
    BoxEnde.insert(0, time.strftime("%H:%M"))
    BoxRec.insert(0, youtube_dl.get()+1)
    ButtonSpeichern.bind("<Return>", Eintrag_Speichern)
    ButtonAbbrechen.bind("<Return>", lambda event: Fenster_Schliessen(Fenster))
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Schedule_Bearbeiten(event=None):

    def Schedule_Speichern(event):

        with open(schedDatei, "w") as Datei:
            Datei.write(Text_Fenster.get("1.0", tk.END + "-1c"))       # ohne letztes LF !!
            Datei.close()
        Fenster.destroy()   

    if not os.path.isfile(schedDatei):
        message.showwarning("Stream Recorder", "\n" + schedDatei + TxT["nicht gefunden"])
    else:
        Fenster = tk.Toplevel(Master)
        Fenster.title("Schedule")
        Fenster.wm_attributes("-topmost", True)
        Fenster.grab_set()

        Scroll_Vertikal = tk.Scrollbar(Fenster, width=14)
        Scroll_Horizont = tk.Scrollbar(Fenster, width=14, orient="horizontal")
        Text_Fenster = tk.Text(Fenster, width=76, height=30, pady=10, padx=10, yscrollcommand = Scroll_Vertikal.set, xscrollcommand = Scroll_Horizont.set)
        if Zeilenumbruch.get() == 1:  umbruch = "none"
        else                       :  umbruch = "char"
        Text_Fenster.config(foreground=FensterVG, background=FensterHG, font="Monospace 10", wrap=umbruch, undo="TRUE")
        Zeile_Info = tk.Label(Fenster, font="Helvetica 10", text=TxT["Datei speichern"])
        Scroll_Vertikal.config(command = Text_Fenster.yview)
        Scroll_Horizont.config(command = Text_Fenster.xview)
        Zeile_Info.pack(side="bottom", fill="x", padx=2, pady=0)
        Scroll_Vertikal.pack(side="right", fill="y", padx=1, pady=1)
        Scroll_Horizont.pack(side="bottom", fill="x", padx=1, pady=1)
        Text_Fenster.pack(fill="both", padx=2, pady=2)

        with open(schedDatei, "r") as Datei:
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
        Farben = ["            weiss - schwarz", "            weiss - grau", "            weiss - rot", "            weiss - gr??n",
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

        if EingabeSizeM.get().isdecimal():
            SizeM = EingabeSizeM.get()[0:2]
        if EingabeSizeL.get().isdecimal():
            SizeL = EingabeSizeL.get()[0:2]
        Gebiet = GebietButton.get()
        TxT = Woerterbuch[Gebiet]
        Listen_Box.config(font="Monospace "+SizeL)

        Schreibe_confDatei()

        Menuleiste.entryconfigure(1, label=TxT["Datei"], font=FontM+SizeM)
        Menuleiste.entryconfigure(2, label=TxT["Suchen"], font=FontM+SizeM)
        Menuleiste.entryconfigure(3, label=TxT["Favoriten"], font=FontM+SizeM)
        Menuleiste.entryconfigure(4, label=TxT["Aufnahme"], font=FontM+SizeM)
        Menuleiste.entryconfigure(5, label=TxT["Schedule"], font=FontM+SizeM)
        Menuleiste.entryconfigure(6, label=TxT["Hilfe"], font=FontM+SizeM)
        Menu_Datei.entryconfigure(0, label=TxT["??ffnen"], font=FontM+SizeM)
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
        Menu_Favoriten.entryconfigure(1, label=TxT["Hinzuf??gen"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(2, label=TxT["Eingeben"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(4, label=TxT["Entfernen"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(6,label=TxT["Zur??ck"], font=FontM+SizeM)
        Menu_Aufnahme.entryconfigure(0, label=TxT["Stoppen"], font=FontM+SizeM)
        Menu_Aufnahme.entryconfigure(1, label=TxT["AlleStop"], font=FontM+SizeM)
        Menu_Aufnahme.entryconfigure(3, label=TxT["Manager"], font=FontM+SizeM)
        Menu_Aufnahme.entryconfigure(5, label=TxT["Protokoll"], font=FontM+SizeM)
        Menu_Schedule.entryconfigure(0, label=TxT["Anzeigen"], font=FontM+SizeM)
        Menu_Schedule.entryconfigure(1, label=TxT["Hinzuf??gen"], font=FontM+SizeM)
        Menu_Schedule.entryconfigure(3, label=TxT["Bearbeiten"], font=FontM+SizeM)
        Menu_Hilfe.entryconfigure(0, label=TxT["Tastatur"], font=FontM+SizeM)
        Menu_Hilfe.entryconfigure(2, label=TxT["??ber"], font=FontM+SizeM)

        Fenster.destroy()

#-----------------------------------------------------

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Einstellungen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    RadioDeutsch = tk.Radiobutton(Fenster, relief="raised", bd=3, variable=GebietButton, value="de", text=TxT["Deutsch"], font="Helvetica 11")
    RadioEnglish = tk.Radiobutton(Fenster, relief="raised", bd=3, variable=GebietButton, value="en", text=TxT["Englisch"], font="Helvetica 11")
    CheckZUmbruch = tk.Checkbutton(Fenster, bd=3, text=TxT["Zeilenumbruch"], font="Helvetica 11", variable=Zeilenumbruch)
    CheckProtokoll = tk.Checkbutton(Fenster, bd=3, text=TxT["Protokoll aus"], font="Helvetica 11", variable=ProtMeldAus)
    TextSizeM = tk.Label(Fenster, text=TxT["Schrift Men??"], font="Helvetica 11")
    EingabeSizeM = tk.Entry(Fenster, bd=4, width=4, font="Helvetica 11")
    TextSizeL = tk.Label(Fenster, text=TxT["Schrift Liste"], font="Helvetica 11")
    EingabeSizeL = tk.Entry(Fenster, bd=4, width=4, font="Helvetica 11")
    ButtonVorderg = tk.Button(Fenster, bd=3, text=TxT["VGfarbe"], font="Helvetica 11", command=Vordergrund_Einstellen)
    ButtonHinterg = tk.Button(Fenster, bd=3, text=TxT["HGfarbe"], font="Helvetica 11", command=Hintergrund_Einstellen)
    ButtonSchema = tk.Button(Fenster, bd=3, text=TxT["FFschema"], font="Helvetica 11", command=Fensterfarbschema)
    TextM3uVerz = tk.Label(Fenster, text=TxT["pVerzeichnis"], font="Helvetica 10")
    EingabeM3uVerz = tk.Entry(Fenster, bd=4, width=38, font="Helvetica 11")
    TextRecVerz = tk.Label(Fenster, text=TxT["rVerzeichnis"], font="Helvetica 10")
    EingabeRecVerz = tk.Entry(Fenster, bd=4, width=38, font="Helvetica 11")
    TextStartDat = tk.Label(Fenster, text=TxT["sDatei"], font="Helvetica 10")
    EingabeStartDat = tk.Entry(Fenster, bd=4, width=38, font="Helvetica 11")    
    ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Speichern"], font="Helvetica 11", command=Einstellungen_Speichern)
    ButtonAbbrechen = tk.Button(Fenster, bd=3, text=TxT["Abbrechen"], font="Helvetica 11", command=Fenster.destroy)

    RadioDeutsch.grid(row=1, column=0, padx=25, pady=20, ipadx=12, ipady=3, sticky="e")
    RadioEnglish.grid(row=1, column=1, padx=25, pady=20, ipadx=12, ipady=3, sticky="w")
    CheckZUmbruch.grid(row=2, column=0, columnspan=2, pady=1, ipadx=50, sticky="w")
    CheckProtokoll.grid(row=3, column=0, columnspan=2, pady=10, ipadx=50, sticky="w")
    TextSizeM.grid(row=4, column=0, columnspan=2, pady=4, ipadx=60, sticky="w")
    EingabeSizeM.grid(row=4, column=1, padx=62, pady=4, sticky="e")
    TextSizeL.grid(row=5, column=0, columnspan=2, pady=4, ipadx=60, sticky="w")
    EingabeSizeL.grid(row=5, column=1, padx=62, pady=4, sticky="e")
    ButtonVorderg.grid(row=6, column=0, columnspan=2, padx=50, pady=14, ipadx=57)
    ButtonHinterg.grid(row=7, column=0, columnspan=2, padx=50, pady=4, ipadx=59)
    ButtonSchema.grid(row=8, column=0, columnspan=2, padx=50, pady=14, ipadx=47)
    TextM3uVerz.grid(row=9, column=0, columnspan=2, pady=1)
    EingabeM3uVerz.grid(row=10, column=0, columnspan=2, pady=8)
    TextRecVerz.grid(row=11, column=0, columnspan=2, pady=1)
    EingabeRecVerz.grid(row=12, column=0, columnspan=2, pady=8)
    TextStartDat.grid(row=13, column=0, columnspan=2, pady=1)
    EingabeStartDat.grid(row=14, column=0, columnspan=2, pady=8)
    ButtonSpeichern.grid(row=15, column=0, padx=22, pady=20, ipadx=15, sticky="e")
    ButtonAbbrechen.grid(row=15, column=1, padx=22, pady=20, ipadx=12, sticky="w")
    tk.Label(Fenster).grid(row=16, column=0)

    GebietButton.set(Gebiet)
    EingabeSizeM.insert(0, SizeM)
    EingabeSizeL.insert(0, SizeL)
    EingabeM3uVerz.insert(0, m3uVerzeichnis)
    EingabeRecVerz.insert(0, recVerzeichnis)
    EingabeStartDat.insert(0, startDatei)
    ButtonSpeichern.bind("<Return>", Einstellungen_Speichern)
    ButtonAbbrechen.bind("<Return>", lambda event: Fenster_Schliessen(Fenster))
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Hilfe_Tastatur(event=None):

    if not os.path.isfile(keyDatei):
        message.showwarning("Stream Recorder", "\n" + keyDatei + " nicht gefunden.  ")
    else:
        Fenster = tk.Toplevel(Master)
        Fenster.title(TxT["Tastatur"])
        Fenster.wm_attributes("-topmost", True)
        Fenster.grab_set()
        Text_Fenster = tk.Text(Fenster, width=44, height=37, pady=10, padx=10)
        Text_Fenster.config(foreground=FensterVG, background=FensterHG, font="Monospace 10", wrap="none")
        Text_Fenster.pack(fill="both", padx=3, pady=3)

        with open(keyDatei, "r") as Datei:
            Text_Fenster.configure(state="normal")
            Text_Fenster.delete("1.0", tk.END)
            Text_Fenster.insert(tk.END, "\n   Select stream:        <Arrow Keys ??????>")
            Text_Fenster.insert(tk.END, "\n   Previous streams:     <Arrow Keys ??????>\n")
            for i, Zeile in enumerate(Datei):
                Text_Fenster.insert(tk.END, "   " + Zeile)
                if i == 1:   Text_Fenster.insert(tk.END, "\n")
                if i == 10:  Text_Fenster.insert(tk.END, "   Open windows menu:    <F10>\n\n")
            Text_Fenster.insert(tk.END, "\n   Scroll page:          <PgUp/PgDn>\n")
            Text_Fenster.insert(tk.END, "   Go to top:            <Home>\n")
            Text_Fenster.insert(tk.END, "   Go to end:            <End>\n")
            Text_Fenster.insert(tk.END, "   Close windows:        <Esc>\n\n")
            Text_Fenster.insert(tk.END, "   Select stream:    <left click>\n")
            Text_Fenster.insert(tk.END, "   View stream:      <left double-click>\n")
            Text_Fenster.insert(tk.END, "   Record stream:    <middle mouse-click>\n")
            Text_Fenster.insert(tk.END, "   Select player:    <right click>\n")
            Text_Fenster.configure(state="disabled")
            Datei.close()
        Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Hilfe_Ueber():

    def Einblenden():

        if Einblenden.Transparenz <= 80: 
            Einblenden.Transparenz += 1
            Fenster.wm_attributes("-alpha", Einblenden.Transparenz / 70)
            Fenster.after(40, Einblenden)
        else:
            Einblenden.Zeichenkette = Einblenden.Zeichenkette[1:] + Einblenden.Zeichenkette[0]
            Lauftext.set(Einblenden.Zeichenkette[0:43])
            Fenster.after(100, Einblenden)

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["??ber"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()
    if os.path.isfile("/usr/share/icons/hicolor/128x128/apps/srecorder.png"):
        Hilfe_Ueber.Icon = tk.PhotoImage(file="/usr/share/icons/hicolor/128x128/apps/srecorder.png")
        Grafik = tk.Label(Fenster, image=Hilfe_Ueber.Icon)
        Grafik.pack(pady=20)
    else:
        tk.Label(Fenster).pack()
    Zeile1 = tk.Label(Fenster, text="Stream Recorder", font="Helvetica 18 bold")
    Zeile2 = tk.Label(Fenster, text="Version 1.45 ext", font="Helvetica 12")
    Einblenden.Zeichenkette = TxT["Entwickelt"]
    Lauftext.set(Einblenden.Zeichenkette[0:43])
    Zeile3 = tk.Label(Fenster, textvariable=Lauftext, font="Helvetica 12")
    Zeile1.pack(padx=110, pady=10) 
    Zeile2.pack(pady=10) 
    Zeile3.pack(pady=20)
    tk.Label(Fenster).pack()
    Fenster.wait_visibility()
    Einblenden.Transparenz = -1
    Einblenden()
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))


###############################################################################################################

def Vorheriger_Stream(i, event=None):

    global altPos

    if (i == -1 and altPos > 0) or (i == 1 and altPos < len(altName)-1):
        altPos += i
        cmdStrg = cmdPlayer.replace("URL[Nr]", altLink[altPos])    # Kommandozeile zusammenbauen
        Statusleiste_Anzeigen(altName[altPos])
        subprocess.Popen(cmdStrg, shell=True)                      # Player starten
        Master.focus_force()
        Listen_Box.focus_set()                                     # Focus zur??ck auf Programmliste
    return "break"               # eingebaute <Pfeiltaste> in tk.Listbox verhindern

###############################################################################################################

def Programm_Beenden(event=None):

    global HauptGeo

    NeuGeo = str(Master.winfo_width()) + "x" + str(Master.winfo_height())
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
                    with open(protDatei, "a") as Datei:
                        Datei.write(time.strftime("%d.%m.%y %H:%M > ") + TxT["Beendet Benutzer"] + recName[i] + "\n")
                        Datei.close()
            Master.destroy()

###############################################################################################################

def Statusleiste_Anzeigen(text):

    global Statustext

    Statustext.set(" {:10d}  | {:6d}  | {:6d}  | {:6d}  |   {:s} ".format(StatusAnzahl, StatusAufnahmen, StatusBeendete, StatusFehler, text))

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

Menu_Datei.add_command(label=TxT["??ffnen"], command=Datei_Oeffnen, accelerator=" <Ctrl+O> ")
Menu_Datei.add_command(label=TxT["Bearbeiten"], command=Datei_Bearbeiten)
Menu_Datei.add_separator()
Menu_Datei.add_command(label=TxT["Player"], command=Player_Auswaehlen, accelerator=" <F4> ")
Menu_Datei.add_command(label=TxT["UserAgent"], command=User_Agent_Aendern)
Menu_Datei.add_command(label=TxT["Einstellungen"], command=Einstellungen, accelerator=" <F7> ")
Menu_Datei.add_separator()
Menu_Datei.add_command(label=TxT["Beenden"], command=Programm_Beenden, accelerator=" <Ctrl+Q> ")

Menu_Suchen.add_command(label=TxT["nNamen"], command=Suche_Namen)
Menu_Suchen.add_command(label=TxT["nLand"], command=Suche_Land)
Menu_Suchen.add_command(label=TxT["nGruppe"], command=Suche_Gruppe)
Menu_Suchen.add_separator()
Menu_Suchen.add_command(label=TxT["SuchSpeich"], command=Suche_Speichern)
Menu_Suchen.add_separator()
Menu_Suchen.add_command(label=TxT["Alle"], command=Alle_Anzeigen, accelerator=" <F3> ")

Menu_Favoriten.add_command(label=TxT["Anzeigen"], command=Favoriten_Anzeigen, accelerator=" <Ctrl+F> ")
Menu_Favoriten.add_command(label=TxT["Hinzuf??gen"], command=Favoriten_Hinzufuegen)
Menu_Favoriten.add_command(label=TxT["Eingeben"], command=Favoriten_Eingeben, accelerator=" <F8> ")
Menu_Favoriten.add_separator()
Menu_Favoriten.add_command(label=TxT["Entfernen"], command=Favoriten_Entfernen)
Menu_Favoriten.add_separator()
Menu_Favoriten.add_command(label=TxT["Zur??ck"], command=Favoriten_Zurueck, accelerator=" <F2> ")

Menu_Aufnahme.add_command(label=TxT["Stoppen"], command=Aufnahme_Stoppen, accelerator=" <Ctrl+A> ")
Menu_Aufnahme.add_command(label=TxT["AlleStop"], command=Alle_Beenden)
Menu_Aufnahme.add_separator()
Menu_Aufnahme.add_command(label=TxT["Manager"], command=Download_Manager, accelerator=" <F6> ")
Menu_Aufnahme.add_separator()
Menu_Aufnahme.add_command(label=TxT["Protokoll"], command=Protokoll_Anzeigen, accelerator=" <Ctrl+P> ")

Menu_Schedule.add_command(label=TxT["Anzeigen"], command=Schedule_Anzeigen, accelerator=" <Ctrl+S> ")
Menu_Schedule.add_command(label=TxT["Hinzuf??gen"], command=Schedule_Hinzufuegen, accelerator=" <F9> ")
Menu_Schedule.add_separator()
Menu_Schedule.add_command(label=TxT["Bearbeiten"], command=Schedule_Bearbeiten)

Menu_Hilfe.add_command(label=TxT["Tastatur"], command=Hilfe_Tastatur, accelerator=" <F1> ")
Menu_Hilfe.add_separator()
Menu_Hilfe.add_command(label=TxT["??ber"], command=Hilfe_Ueber)

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
Listen_Box.config(bg=Hintergrund, fg=Vordergrund, font="Monospace "+SizeL)
Statusleiste.pack(side="bottom", fill="x", padx=2, pady=1)
Scroll_Balken.pack(side="right", fill="y", padx=1, pady=1)
Listen_Box.pack(fill="both", padx=2, pady=1, expand=True)

Listen_Box.bind("<Double-Button-1>", Stream_Anschauen)
Listen_Box.bind("<Button-2>", Stream_Aufnehmen)
Listen_Box.bind("<Button-3>", Player_Auswaehlen)
Listen_Box.bind("<Home>", Liste_Anzeigen)
Listen_Box.bind("<End>", lambda event: Listenende_Anzeigen())     # eingebaute <Ende-Taste> in tk.Listbox umgehen
Listen_Box.bind("<Left>", lambda event: Vorheriger_Stream(-1))    # eingebaute <Pfeiltaste> in tk.Listbox umgehen
Listen_Box.bind("<Right>", lambda event: Vorheriger_Stream(1))    # eingebaute <Pfeiltaste> in tk.Listbox umgehen
Listen_Box.bind(keyListe[0][22:], Stream_Anschauen)
Listen_Box.bind(keyListe[1][22:], Stream_Aufnehmen)
Listen_Box.bind(keyListe[2][22:], Hilfe_Tastatur)
Listen_Box.bind(keyListe[3][22:], Favoriten_Zurueck)
Listen_Box.bind(keyListe[4][22:], Alle_Anzeigen)
Listen_Box.bind(keyListe[5][22:], Player_Auswaehlen)
Listen_Box.bind(keyListe[6][22:], User_Agent_Aendern)
Listen_Box.bind(keyListe[7][22:], Download_Manager)
Listen_Box.bind(keyListe[8][22:], Einstellungen)
Listen_Box.bind(keyListe[9][22:], Favoriten_Eingeben)
Listen_Box.bind(keyListe[10][22:], Schedule_Hinzufuegen)
Listen_Box.bind(keyListe[11][22:], Aufnahme_Stoppen)
Listen_Box.bind(keyListe[12][22:], Protokoll_Anzeigen)
Listen_Box.bind(keyListe[13][22:], Favoriten_Anzeigen)
Listen_Box.bind(keyListe[14][22:], Favoriten_Hinzufuegen)
Listen_Box.bind(keyListe[15][22:], Datei_Oeffnen)
Listen_Box.bind(keyListe[16][22:], Datei_Bearbeiten)
Listen_Box.bind(keyListe[17][22:], Schedule_Anzeigen)
Listen_Box.bind(keyListe[18][22:], Schedule_Bearbeiten)
Listen_Box.bind(keyListe[19][22:], Programm_Beenden)

#-----------------------------------------------------

Schedule_Starten()      # Schedule einmal pro Minute nach Terminen durchsuchen

Datei_Oeffnen()         # StartDatei laden oder Playlist ausw??hlen

Master.protocol("WM_DELETE_WINDOW", Programm_Beenden)

Master.mainloop()

###############################################################################################################

