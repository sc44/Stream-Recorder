#! /usr/bin/env python3
#
#  StreamRecorder - Version: 1.40 - letzte Änderungen: 25.01.2022
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
rpDatei = os.path.expanduser("~") + "/.config/srecorder/recprog.conf"

keyListe = [ \
"View stream:          <Return>",
"Record stream:        <space>",
"Keyboard shortcuts:   <F1>",
"Previous playlist:    <F2>",
"Search filter off:    <F3>",
"Select player:        <F4>",
"Select user agent:    <F5>",
"Select record prog:   <F6>",
"Settings:             <F7>",
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

rpListe = [ \
'*ffmpeg -i "link" -c:v copy -c:a copy "file" 2> /dev/null',
' ffmpeg -i $(yt-dlp -g "link") -c:v copy -c:a copy "file" 2> /dev/null',
' ffmpeg -i $(youtube-dl -g "link") -c:v copy -c:a copy "file" 2> /dev/null',
' ', ' ', ' ', ' ' ]

Woerterbuch = { \
"de" : {"Datei":" Datei ","Suchen":" Suchen ","Favoriten":" Favoriten ","Aufnahme":" Aufnahme ","Schedule":" Schedule ",
        "Hilfe":" Hilfe ","Öffnen":"  Öffnen ","Bearbeiten":"  Bearbeiten ","Player":"  Player auswählen ","Info":"  Info ",
        "UserAgent":"  User-Agent ändern ","Einstellungen":"  Einstellungen ","Beenden":"  Beenden ","Namen":"  Nach Namen ",
        "Land":"  Nach Land ","Gruppe":"  Nach Gruppe ","Alle":"  Alle anzeigen ","Anzeigen":"  Anzeigen ","Über":"  Über ",
        "Hinzufügen":"  Hinzufügen ","Entfernen":"  Entfernen ","Zurück":"  Zurück ","Stoppen":"  Anzeigen / Stoppen ",
        "AlleStop":"  Alle beenden ","Protokoll":"  Protokoll anzeigen ","Tastatur":"  Tastatur ","sDatei":"Start-Playlist:",
        "Schrift Menü":"Schriftgröße des Menüs eingeben: ", "Schrift Liste":"Schriftgröße der Playlist eingeben: ",
        "VGfarbe":"Vordergrundfarbe einstellen","HGfarbe":"Hintergrundfarbe einstellen","FFschema":"Fensterfarbschema auswählen",
        "pVerzeichnis":" Playlist-Verzeichnis:","rVerzeichnis":" Aufnahme-Verzeichnis:","Laufende Aufnahmen":"Laufende Aufnahmen",
        "Speichern":"Speichern","Abbrechen":"Abbrechen","Datei speichern":" Speichern mit <Strg+S> oder <Doppelklick-Rechts> ",
        "Aufnahme stoppen":" Aufnahme stoppen mit <Doppelklick-Links>","Deutsch":"  Deutsch  ","Englisch":"  Englisch ",
        "wirklich beenden":" Sollen wirklich alle Aufnahmen beendet werden?  ","wirklich entfernen":" wirklich entfernen?  ",
        "Kein Sender":" Kein Sender ausgewählt.  ","nicht installiert":" nicht installiert.  ","nicht gefunden":" nicht gefunden.  ",
        "Zeilenumbruch":"   Keinen Zeilenumbruch in Datei Bearbeiten","Protokoll aus":"   Keine Meldungen ins Protokoll schreiben",
        "Mo":"Mo","Di":"Di","Mi":"Mi","Do":"Do","Fr":"Fr","Sa":"Sa","So":"So","Gestartet Schedule":"Gestartet von Timer    - ",
        "Beendet Schedule":"Beendet von Timer      - ","Alle stoppen":"Alle Aufnahmen von Benutzer beendet.","Strg":" <Strg+",
        "Gestartet Benutzer":"Gestartet von Benutzer - ","Beendet Benutzer":"Beendet von Benutzer   - ","Rec Prog":"  Aufnahme Programme ",
        "Groesse Fenster":"Die Größe des Hauptfensters wurde geändert.  \n\nSoll die neue Größe gespeichert werden?  ",
        "Entwickelt":" ++++ Entwickelt von Woodstock & sc44 ++++ Dieses Programm wird unter den Bedingungen der GNU General Public License veröffentlicht, Copyright (C) 2021."},

"en" : {"Datei":" File ","Suchen":" Search ","Favoriten":" Favorites ","Aufnahme":" Recording ","Schedule":" Schedule ",
        "Hilfe":" Help ","Öffnen":"  Open ","Bearbeiten":"  Edit ","Player":"  Player ","Info":"  Info ",
        "UserAgent":"  User-Agent ","Einstellungen":"  Settings ","Beenden":"  Exit ","Namen":"  Name ",
        "Land":"  Country ","Gruppe":"  Category ","Alle":"  List all ","Anzeigen":"  Display ","Über":"  About ",
        "Hinzufügen":"  Add ","Entfernen":"  Delete ","Zurück":"  Back ","Stoppen":"  Disp / Stop ",
        "AlleStop":"  Stop all ","Protokoll":"  Protocol ","Tastatur":"  Keyboard ","FFschema":" Select window color scheme ",
        "Schrift Menü":"Set the font size of the menu: ", "Schrift Liste":"Set the font size of the playlist: ",
        "VGfarbe":"     Set foreground color     ","HGfarbe":"    Set background color    ","sDatei":"Start playlist:",
        "pVerzeichnis":" Playlist directory:","rVerzeichnis":" Recording directory:","Laufende Aufnahmen":"Active recordings",
        "Speichern":"    Save    ","Abbrechen":"     Exit     ","Datei speichern":" Save file with <Ctrl+S> or <Right double click> ",
        "Aufnahme stoppen":" Stop recording with <Left double click>","Deutsch":"  German  ","Englisch":"  English  ",
        "wirklich beenden":" Are you sure you want to stop all recordings?  ","wirklich entfernen":" really remove?  ",
        "Kein Sender":" No channel selected.  ","nicht installiert":" not installed.  ","nicht gefunden":" not found.  ",
        "Zeilenumbruch":"   Don't wrap lines in the file edit window ","Protokoll aus":"   Don't write any messages in the logfile",
        "Mo":"Mon","Di":"Tue","Mi":"Wed","Do":"Thu","Fr":"Fri","Sa":"Sat","So":"Sun","Gestartet Schedule":"Started by timer       - ",
        "Beendet Schedule":"Terminated by timer    - ","Alle stoppen":"All recordings terminated by user.","Strg":" <Ctrl+",
        "Gestartet Benutzer":"Started by user        - ","Beendet Benutzer":"Terminated by user     - ","Rec Prog":"  Record programs ",
        "Groesse Fenster":"The size of main window has been changed.  \n\nDo you want to save the new size?  ",
        "Entwickelt":" +++++ Developed by Woodstock & sc44 +++++ This program is published under the terms of the GNU General Public License, Copyright (C) 2021."} }  

###############################################################################################################

Master = tk.Tk()
Master.title("Stream Recorder v1.40")
Master.option_add("*Dialog.msg.font", "Helvetica 11")        # Messagebox Schriftart
Master.option_add("*Dialog.msg.wrapLength", "50i")           # Messagebox Zeilenumbruch

if os.path.isfile("/usr/share/icons/hicolor/128x128/apps/srecorder.png"):
    Master.iconphoto(False, tk.PhotoImage(file="/usr/share/icons/hicolor/128x128/apps/srecorder.png"))

GebietButton = tk.StringVar()                # Gebietsschema
Statustext = tk.StringVar()                  # Statuszeile
Lauftext = tk.StringVar()                    # Laufschrift
Zeilenumbruch = tk.IntVar()                  # Zeilenumbruch an/aus
ProtMeldAus = tk.IntVar()                    # Protokollmeldungen an/aus
RecProgNr = tk.IntVar()                      # Nummer Aufnahmeprogramm

recPID.clear()                               # Aufnahme: PID, Name, Startzeit, Endezeit löschen
recName.clear()
recStart.clear()
recEnde.clear()
altName.clear()                              # vorher geschaute Sender
altLink.clear()

if not os.path.isdir(confVerzeichnis):       # Verzeichnisse erstellen wenn nicht vorhanden
    os.makedirs(confVerzeichnis)
if not os.path.isdir(cacheVerzeichnis):
    os.makedirs(cacheVerzeichnis)

if os.path.isfile(confDatei):                # wenn Konfigurationsdatei existiert dann laden
    with open(confDatei, "r") as Datei:
        Puffer.clear() 
        for Zeile in Datei:            Puffer.append(Zeile)
        Datei.close()
    m3uVerzeichnis = Puffer[0][4:].rstrip()
    recVerzeichnis = Puffer[1][8:].rstrip()
    startDatei = Puffer[2][6:].rstrip()
    HauptGeo = Puffer[3][9:].rstrip()
    Vordergrund = Puffer[4][3:10]
    Hintergrund = Puffer[5][3:10]
    FensterVG = Puffer[6][4:11]
    FensterHG = Puffer[7][4:11]
    SizeM = Puffer[8][6:8]
    SizeL = Puffer[9][6:8]
    Gebiet = Puffer[10][9:11]
    Zeilenumbruch.set(int(Puffer[11][7:8]))    
    ProtMeldAus.set(int(Puffer[12][7:8]))    
else:                                        # sonst neue Konfigurationsdatei erstellen
    if locale.getlocale()[0][0:2] == "de":  Gebiet = "de"
    else:                                   Gebiet = "en"
    Zeilenumbruch.set(1)    
    ProtMeldAus.set(0)    
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
        Datei.write("nowrap=" + "1\n")
        Datei.write("noprot=" + "0\n")
        Datei.close()
TxT = Woerterbuch[Gebiet]                    # Zeiger auf aktuelle Sprache

Master.geometry(HauptGeo)                    # Hauptfenstergrösse

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

if os.path.isfile(rpDatei):                  # wenn Aufnahmeprogramm-Datei existiert dann laden
    with open(rpDatei, "r") as Datei:
        rpListe.clear() 
        for Zeile in Datei:
            rpListe.append(Zeile.rstrip())
        Datei.close()
else:                                        # sonst neue Aufnahmeprogramm-Datei erstellen
    with open(rpDatei, "w") as Datei:
        for i in range(len(rpListe)):
            Datei.write(rpListe[i] + "\n")
        Datei.close()
for i in range(len(rpListe)):                # Nummer des aktiven Aufnahmeprogramms setzen
    if rpListe[i][0:1] == "*":
        RecProgNr.set(i)

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
if not os.path.isfile("/usr/bin/ffmpeg"):
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
            Datei.close()
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

    Listen_Loeschen()
    for i in range(1, len(Puffer)-1, 2):
        Zeilenpuffer_Auswerten(i)
    Liste_Anzeigen()

###############################################################################################################

def Suche_Namen():

    def Namen_Anzeigen(event=None):

        Eingabe = Eingabefeld.get()
        Fenster.destroy()
        Listen_Loeschen()
        for i in range(1, len(Puffer)-1, 2):            # Puffer durchsuchen
            x = Puffer[i].find(",")
            if Eingabe in Puffer[i][x+1:].rstrip():     # wenn gefunden
                Zeilenpuffer_Auswerten(i)
        Liste_Anzeigen()

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Suchen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    Fenstertext = tk.Label(Fenster, text=TxT["Namen"]+":", font="Helvetica 12")
    Eingabefeld = tk.Entry(Fenster, bd=4, width=10, font="Helvetica 11")
    Button_Speichern = tk.Button(Fenster, bd=2, text=TxT["Anzeigen"], font="Helvetica 11", command=Namen_Anzeigen)
    Fenstertext.pack(pady=20)
    Eingabefeld.pack(pady=1)
    Button_Speichern.pack(padx=50, pady=25, ipadx=4)
    tk.Label(Fenster).pack()

    Eingabefeld.insert(0, "")
    Eingabefeld.focus_set()
    Eingabefeld.bind("<Return>", Namen_Anzeigen)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Suche_Land():

    def Land_Anzeigen(event=None):

        Eingabe = Eingabefeld.get()
        Fenster.destroy()
        Listen_Loeschen()
        for i in range(1, len(Puffer)-1, 2):            # Puffer durchsuchen
            x = Puffer[i].find("tvg-country=")
            y = Puffer[i].find('"', x+13)
            if Puffer[i][x+13:y] == Eingabe:            # wenn gefunden
                Zeilenpuffer_Auswerten(i)
        Liste_Anzeigen()

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Suchen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    Fenstertext = tk.Label(Fenster, text=TxT["Land"]+":", font="Helvetica 12")
    Eingabefeld = tk.Entry(Fenster, bd=4, width=10, font="Helvetica 11")
    Button_Speichern = tk.Button(Fenster, bd=2, text=TxT["Anzeigen"], font="Helvetica 11", command=Land_Anzeigen)
    Fenstertext.pack(pady=20)
    Eingabefeld.pack(pady=1)
    Button_Speichern.pack(padx=50, pady=25, ipadx=4)
    tk.Label(Fenster).pack()

    Eingabefeld.insert(0, "DE")
    Eingabefeld.focus_set()
    Eingabefeld.bind("<Return>", Land_Anzeigen)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Suche_Gruppe():

    def Gruppe_Anzeigen(event=None):

        Eingabe = Eingabefeld.get()
        Fenster.destroy()
        Listen_Loeschen()
        for i in range(1, len(Puffer)-1, 2):            # Puffer durchsuchen
            x = Puffer[i].find("group-title=")
            if Puffer[i][x+13:x+16] == Eingabe[0:3]:    # wenn gefunden
                Zeilenpuffer_Auswerten(i)
        Liste_Anzeigen()

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Suchen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    Fenstertext = tk.Label(Fenster, text=TxT["Gruppe"]+":", font="Helvetica 12")
    Eingabefeld = tk.Entry(Fenster, bd=4, width=10, font="Helvetica 11")
    Button_Speichern = tk.Button(Fenster, bd=2, text=TxT["Anzeigen"], font="Helvetica 11", command=Gruppe_Anzeigen)
    Fenstertext.pack(pady=20)
    Eingabefeld.pack(pady=1)
    Button_Speichern.pack(padx=50, pady=25, ipadx=4)
    tk.Label(Fenster).pack()

    Eingabefeld.insert(0, "Music")
    Eingabefeld.focus_set()
    Eingabefeld.bind("<Return>", Gruppe_Anzeigen)
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Favoriten_Anzeigen(event=None):

    global Puffer, m3uDatei, m3uMerker
    
    if not os.path.isfile(m3uVerzeichnis + "favoriten.m3u"):
        message.showwarning("Stream Recorder", "\n" + m3uVerzeichnis + "favoriten.m3u" + TxT["nicht gefunden"])
    else:
        m3uMerker = m3uDatei
        m3uDatei = m3uVerzeichnis + "favoriten.m3u"
        with open(m3uDatei, "r") as Datei:
            Puffer.clear()
            for Zeile in Datei:
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
        with open(FavName, "a") as Datei:           # 2 Zeilen an favoriten.m3u anhängen
            Datei.write(Puffer[i*2-1])              #  Beschreibung  
            Datei.write(Puffer[i*2])                #  URL
            Datei.close()

###############################################################################################################

def Favoriten_Entfernen():

    global Puffer
    
    if m3uDatei == m3uVerzeichnis + "favoriten.m3u":
        Nr = Listen_Box.curselection()[0]           # Index des markierten Senders
        if message.askyesno("Stream Recorder", "\n" + Name[Nr] + TxT["wirklich entfernen"]):
            Puffer.pop(Nr*2+2)                      # URL löschen
            Puffer.pop(Nr*2+1)                      # Beschreibung löschen
            with open(m3uDatei, "w") as Datei:      # Favoriten-Datei neu schreiben (überschreiben)
                for i in range(0, len(Puffer)):
                    Datei.write(Puffer[i])
                Datei.close()
            Alle_Anzeigen()                         # gesamten Puffer neu anzeigen

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
                if not (Zeile == "\n" or Zeile[0:11] == "#EXTVLCOPT:"):    # Leerzeile und User Agent überspringen
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
    time.sleep(0.2)                                      # wegen rechter Maustaste, sonst grab failed !!
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

def Aufnahme_Programm(event=None):

    def Rec_Prog_Speichern(event=None):

        for i in range(len(rpListe)):
            rpListe[i] = " " + rpEingabe[i].get()
        z = list(rpListe[RecProgNr.get()])
        z[0] = "*"
        rpListe[RecProgNr.get()] ="".join(z)
        with open(rpDatei, "w") as Datei:
            for i in range(len(rpListe)):
                if RecProgNr.get() == i:  Datei.write("*")
                else:                     Datei.write(" ")
                Datei.write(rpEingabe[i].get() + "\n")
            Datei.close()
        Fenster.destroy()


    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Rec Prog"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    rpEingabe1 = tk.Entry(Fenster, bd=2, width=55, font="Helvetica 11")
    rpEingabe2 = tk.Entry(Fenster, bd=2, width=55, font="Helvetica 11")
    rpEingabe3 = tk.Entry(Fenster, bd=2, width=55, font="Helvetica 11")
    rpEingabe4 = tk.Entry(Fenster, bd=2, width=55, font="Helvetica 11")
    rpEingabe5 = tk.Entry(Fenster, bd=2, width=55, font="Helvetica 11")
    rpEingabe6 = tk.Entry(Fenster, bd=2, width=55, font="Helvetica 11")
    rpEingabe7 = tk.Entry(Fenster, bd=2, width=55, font="Helvetica 11")
    rpEingabe = [rpEingabe1, rpEingabe2, rpEingabe3, rpEingabe4, rpEingabe5, rpEingabe6, rpEingabe7]

    for i in range(len(rpListe)):                # aktuelle Kommandozeilen einfügen
        rpEingabe[i].insert(0, rpListe[i][1:])

    rpRadio1 = tk.Radiobutton(Fenster, variable=RecProgNr, value=0)
    rpRadio2 = tk.Radiobutton(Fenster, variable=RecProgNr, value=1)
    rpRadio3 = tk.Radiobutton(Fenster, variable=RecProgNr, value=2)
    rpRadio4 = tk.Radiobutton(Fenster, variable=RecProgNr, value=3)
    rpRadio5 = tk.Radiobutton(Fenster, variable=RecProgNr, value=4)
    rpRadio6 = tk.Radiobutton(Fenster, variable=RecProgNr, value=5)
    rpRadio7 = tk.Radiobutton(Fenster, variable=RecProgNr, value=6)
    rpRadio = [rpRadio1, rpRadio2, rpRadio3, rpRadio4, rpRadio5, rpRadio6, rpRadio7]

    for i in range(len(rpListe)):                # aktive Kommandozeile setzen
        if rpListe[i][0:1] == "*":
            RecProgNr.set(i)

    tk.Label(Fenster).grid(row=0,column=0, pady=2, columnspan=3)
    for i in range(len(rpListe)):
        rpRadio[i].grid(row=i+1, column=0, padx=10, pady=4)
        rpEingabe[i].grid(row=i+1, column=1, padx=0, pady=4)
        tk.Label(Fenster).grid(row=i+1,column=2, padx=15, pady=4)

    butSpeichern = tk.Button(Fenster, bd=2, text=TxT["Speichern"], font="Helvetica 11", command=Rec_Prog_Speichern)
    butAbbrechen = tk.Button(Fenster, bd=2, text=TxT["Abbrechen"], font="Helvetica 11", command=Fenster.destroy)
    butSpeichern.grid(row=8, column=0, padx=95, pady=20, ipadx=18, columnspan=3,sticky="w")
    butAbbrechen.grid(row=8, column=0, padx=85, pady=20, ipadx=15, columnspan=3,sticky="e")
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
        try:                                             # URL prüfen
            urllib.request.urlopen(urllib.request.Request(URL[Nr], headers={"User-Agent": UserAgent}), timeout=5)
        except urllib.error.HTTPError as err:
            meldung = str(err.code) + ":  " + str(err.reason)
            Statusleiste_Anzeigen(meldung)
        except urllib.error.URLError as err:
            meldung = str(err.reason)
            Statusleiste_Anzeigen(meldung)
        except:
            Statusleiste_Anzeigen("Unexpected error")
        else:                                            # wenn URL gültig
            Statusleiste_Anzeigen(Name[Nr])
            subprocess.Popen(cmdStrg, shell=True)        # Player starten
            altName.append(Name[Nr])                     # Namen speichern
            altLink.append(URL[Nr])                      # Link speichern
            altPos = len(altName)-1                      # Position auf Letzten
            Master.focus_force()
            Listen_Box.focus_set()                       # Focus zurück auf Programmliste

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
        try:                                             # URL prüfen
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
        else:                                            # wenn URL gültig
            Statusleiste_Anzeigen(Name[Nr])
            for n in range(1, 1000):                     # Namen der Aufnahme festlegen (..._001 bis ..._999)
                Dateiname = Name[Nr] + "_" + str(n).zfill(3) + ".ts" 
                if not os.path.isfile(recVerzeichnis + Dateiname):                  # wenn Dateiname nicht existiert dann übernehmen
                    break
            cmdRecProg = rpListe[RecProgNr.get()][1:]
            cmdRecProg = cmdRecProg.replace("link", URL[Nr])                        # Link der Aufnahme in Kommandozeile einbauen
            cmdRecProg = cmdRecProg.replace("file", recVerzeichnis + Dateiname)     # Namen der Aufnahme in Kommandozeile einbauen
            try:
                altpid = int(subprocess.check_output(["pidof", "-s", "ffmpeg"]))
            except:
                altpid = 0
            subprocess.Popen(cmdRecProg, shell=True)
            if not rpListe[RecProgNr.get()][1:7] == "ffmpeg":
                Statusleiste_Anzeigen(rpListe[RecProgNr.get()][1:])
            else:
                pid = 0
                time.sleep(3)            # PID-Fehler bei yt-dlp abfangen !!
                for x in range(14):
                    time.sleep(0.5)      # 0,5 Sek. x 14 Durchläufe = max. 7 Sek.
                    try:
                        pid = int(subprocess.check_output(["pidof", "-s", "ffmpeg"]))
                        if not pid == altpid:   break
                    except:
                        pass
                recPID.append(pid)                       # Aufnahme: PID speichern     
                recStart.append(time.strftime("%H%M"))   # Aufnahme: Startzeit speichern                          
                recEnde.append("9999")                   # Aufnahme: Endezeit speichern                          
                recName.append(Name[Nr])                 # Aufnahme: Namen speichern
                StatusAufnahmen = len(recPID)
                protDatei_Schreiben(TxT["Gestartet Benutzer"], Name[Nr])
                Statusleiste_Anzeigen(Name[Nr])

###############################################################################################################

def Aufnahme_Stoppen(event=None):

    def Aufnahme_Beenden(event):

        global recPID, recStart, recEnde, recName, StatusAufnahmen, StatusBeendete

        Nr = int(Record_Liste.curselection()[0])         # Index Aufnahmeliste
        try:
            os.kill(int(recPID[Nr]), signal.SIGTERM)     # Aufnahme stoppen
        except:
            pass
        if not ProtMeldAus.get():  
            with open(protDatei, "a") as Datei:
                Datei.write(time.strftime("%d.%m.%y %H:%M > ") + TxT["Beendet Benutzer"] + recName[Nr] + "\n")
                Datei.close()
        recPID.pop(Nr)                                   # Aufnahme: PID löschen
        recStart.pop(Nr)                                 # Aufnahme: Startzeit löschen
        recEnde.pop(Nr)                                  # Aufnahme: Endezeit löschen
        recName.pop(Nr)                                  # Aufnahme: Namen löschen
        Record_Liste.delete(Nr)                          # Listeneintrag löschen
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
        subprocess.Popen('killall ffmpeg', shell=True)
        if not ProtMeldAus.get():  
            with open(protDatei, "a") as Datei:
                Datei.write(time.strftime("%d.%m.%y %H:%M > ") + TxT["Alle stoppen"] + "\n")
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

    sPuffer.clear()     # Schedule-Puffer löschen   (1. Zeile = Tage + Start + Ende + * + Name + LF  /  2. Zeile = URL + LF)

    if os.path.isfile(schedDatei):
        with open(schedDatei, "r") as Datei:          # Schedule-Datei in Puffer laden
            for Zeile in Datei:
                    sPuffer.append(Zeile)
            Datei.close()

    #---------- Nächste Aufnahme(n) starten ----------

    Aktuelle = int(time.strftime("%H%M"))                                 # aktuelle Uhrzeit holen (SSMM)
    w = datetime.datetime.today().weekday()                               # aktuellen Wochentag holen (0-6)

    for i in range(len(sPuffer)-2, -2, -2):                               # vom Ende her durchsuchen (Löschfehler verhindern)
        Startzeit = int(sPuffer[i][8:10] + sPuffer[i][11:13])             # Startzeit holen (SSMM)

        if Startzeit == Aktuelle and sPuffer[i][w] == "x":                # wenn Uhrzeit und Wochentag stimmen
            try:                                                          # URL prüfen
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
            else:                                                         # wenn URL gültig
                for n in range(1, 1000):                                  # Namen der Aufnahme festlegen (..._001 bis ..._999)
                    Dateiname = sPuffer[i][22:].rstrip() + "_" + str(n).zfill(3) + ".ts"
                    if not os.path.isfile(recVerzeichnis + Dateiname):
                        break
                cmdRecProg = rpListe[RecProgNr.get()][1:]
                cmdRecProg = cmdRecProg.replace("link", sPuffer[i+1].rstrip())          # Link der Aufnahme in Kommandozeile einbauen
                cmdRecProg = cmdRecProg.replace("file", recVerzeichnis + Dateiname)     # Namen der Aufnahme in Kommandozeile einbauen
                try:
                    altpid = int(subprocess.check_output(["pidof", "-s", "ffmpeg"]))
                except:
                    altpid = 0
                subprocess.Popen(cmdRecProg, shell=True)
                pid = 0
                time.sleep(3)            # PID-Fehler bei yt-dlp abfangen !!
                for x in range(14):
                    time.sleep(0.5)      # 0,5 Sek. x 14 Durchläufe = max. 7 Sek.
                    try:
                        pid = int(subprocess.check_output(["pidof", "-s", "ffmpeg"]))
                        if not pid == altpid:   break
                    except:
                        pass
                recPID.append(pid)                                        # Aufnahme: PID speichern
                recStart.append(time.strftime("%H%M"))                    # Aufnahme: Startzeit speichern
                recEnde.append(sPuffer[i][14:16] + sPuffer[i][17:19])     # Aufnahme: Endezeit (SSMM) speichern
                recName.append(sPuffer[i][22:].rstrip())                  # Aufnahme: Namen (ohne LF) speichern
                StatusAufnahmen = len(recPID)
                Statusleiste_Anzeigen("")
                protDatei_Schreiben(TxT["Gestartet Schedule"], sPuffer[i][22:].rstrip())

            #---------- Wenn Einmal-Aufnehmen (*) ----------

            if sPuffer[i][20] == "*":
                z = list(sPuffer[i])
                z[w] = "-"                                                # Wochentag in Puffer deaktivieren
                sPuffer[i] = "".join(z)

                if sPuffer[i][0:7] == "-------":                          # wenn keine Wochentage mehr gültig
                    sPuffer.pop(i+1)                                      # URL-Zeile löschen
                    sPuffer.pop(i)                                        # Text-Zeile löschen 

                with open(schedDatei, "w") as Datei:                      # schedule.txt neu schreiben
                    for i in range(len(sPuffer)):
                        Datei.write(sPuffer[i])
                    Datei.close()

    #---------- Nächste Aufnahme(n) beenden ----------

    for i in range(len(recEnde)-1, -1, -1):            # vom Ende her durchsuchen (Löschfehler verhindern)
        Endezeit = int(recEnde[i])
        if Endezeit == Aktuelle:
            try:
                os.kill(int(recPID[i]), signal.SIGTERM)
            except:
                pass
            protDatei_Schreiben(TxT["Beendet Schedule"], recName[i])
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
        Text_Fenster = tk.Text(Fenster, width=72, height=30, pady=10, padx=10, yscrollcommand=Scroll_Balken.set)
        Text_Fenster.config(foreground=FensterVG, background=FensterHG, font="Monospace 10", wrap="none")
        Scroll_Balken.config(command = Text_Fenster.yview)
        Scroll_Balken.pack(side="right", fill="y", padx=1, pady=1)
        Text_Fenster.pack(fill="both", padx=2, pady=2)
        with open(protDatei, "r") as Datei:
            Text_Fenster.configure(state="normal")
            Text_Fenster.delete(1.0, tk.END)
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

        wt = list(WochenText)
        for i in range(0, 7, 1):
            if Wochentag[i].get():    wt[i] = "x"  
            else:                     wt[i] = "-"
        WochenText = "".join(wt)

        Start = BoxStart.get()
        Ende = BoxEnde.get()

        if Wiederholung.get():    Einmal = "-"
        else:                     Einmal = "*"

        Nr = Listen_Box.curselection()[0]
        with open(schedDatei, "a") as Datei:
            Datei.write(WochenText + " " + str(Start) + " " + str(Ende) + " " + Einmal + " " + Name[Nr] + "\n")
            Datei.write(str(URL[Nr] + "\n"))
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

    Wiederholung = tk.IntVar()                         # Einmal-Aufnehmen setzen
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
    BoxMo = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[0])
    BoxDi = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[1])
    BoxMi = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[2])
    BoxDo = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[3])
    BoxFr = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[4])
    BoxSa = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[5])
    BoxSo = tk.Checkbutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wochentag[6])
    BoxStart = tk.Entry(Fenster, exportselection=0, relief="sunken", bd=3, width=5, font="Helvetica 11")
    BoxEnde = tk.Entry(Fenster, exportselection=0, relief="sunken", bd=3, width=5, font="Helvetica 11")
    Radio9 = tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wiederholung, value=1, text=" ∞  ", font="Helvetica 11")
    Radio1 = tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=3, variable=Wiederholung, value=0, text=" ①  ", font="Helvetica 11")
    ButtonSpeichern = tk.Button(Fenster, bd=3, text=TxT["Speichern"], font="Helvetica 11", command=Eintrag_Speichern)
    ButtonAbbrechen = tk.Button(Fenster, bd=3, text=TxT["Abbrechen"], font="Helvetica 11", command=Fenster.destroy)

    TextTag = [TextMo, TextDi, TextMi, TextDo, TextFr, TextSa, TextSo]     # Variablenliste für Wochentage
    BoxTag = [BoxMo, BoxDi, BoxMi, BoxDo, BoxFr, BoxSa, BoxSo]

    ProgName.grid(row=0, column=2, padx=0, pady=20, columnspan=13)
    tk.Label(Fenster).grid(row=1, column=1, padx=10)
    for i in range (7):
        TextTag[i].grid(row=1, column=i+2, padx=2, pady=4)
    TextStart.grid(row=1, column=9, padx=30, pady=4)
    TextEnde.grid(row=1, column=10, padx=0, pady=4)
    tk.Label(Fenster).grid(row=1, column=11, padx=10)
    Radio9.grid(row=1, column=12, padx=2, pady=4)
    tk.Label(Fenster).grid(row=1, column=13, padx=10)
    tk.Label(Fenster).grid(row=2, column=1, padx=10)
    for i in range (7):
        BoxTag[i].grid(row=2, column=i+2, padx=1, pady=4)
    BoxStart.grid(row=2, column=9, padx=30, pady=4)
    BoxEnde.grid(row=2, column=10, padx=0, pady=4)
    tk.Label(Fenster).grid(row=2, column=11, padx=10)
    Radio1.grid(row=2, column=12, padx=2, pady=4)
    tk.Label(Fenster).grid(row=2, column=13, padx=10)
    ButtonSpeichern.grid(row=3, column=4, padx=10, pady=20, ipadx=8, columnspan=5)
    ButtonAbbrechen.grid(row=3, column=9, padx=0, pady=20, ipadx=8, columnspan=3)
    tk.Label(Fenster).grid(row=4, column=1, padx=10)

    BoxStart.insert(0, time.strftime("%H:%M"))
    BoxEnde.insert(0, time.strftime("%H:%M"))
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

    def Einstellungen_Speichern():

        global m3uVerzeichnis, recVerzeichnis, startDatei, SizeM, SizeL,Gebiet, TxT
  
        if m3uEingabe.get()[-1] == "/":  m3uVerzeichnis = m3uEingabe.get()
        else:                            m3uVerzeichnis = m3uEingabe.get() + "/" 
        if not os.path.isdir(m3uVerzeichnis):
            os.makedirs(m3uVerzeichnis)
        if recEingabe.get()[-1] == "/":  recVerzeichnis = recEingabe.get()
        else:                            recVerzeichnis = recEingabe.get() + "/" 
        if not os.path.isdir(recVerzeichnis):
            os.makedirs(recVerzeichnis)
        startDatei = startEingabe.get()

        if SizeMEingabe.get().isdecimal():
            SizeM = SizeMEingabe.get()[0:2]
        if SizeLEingabe.get().isdecimal():
            SizeL = SizeLEingabe.get()[0:2]
        Gebiet = GebietButton.get()
        TxT = Woerterbuch[Gebiet]
        Listen_Box.config(font="Monospace "+SizeL)

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
        Menu_Suchen.entryconfigure(0, label=TxT["Namen"], font=FontM+SizeM)
        Menu_Suchen.entryconfigure(1, label=TxT["Land"], font=FontM+SizeM)
        Menu_Suchen.entryconfigure(2, label=TxT["Gruppe"], font=FontM+SizeM)
        Menu_Suchen.entryconfigure(4, label=TxT["Alle"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(0, label=TxT["Anzeigen"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(1, label=TxT["Hinzufügen"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(3, label=TxT["Entfernen"], font=FontM+SizeM)
        Menu_Favoriten.entryconfigure(5,label=TxT["Zurück"], font=FontM+SizeM)
        Menu_Aufnahme.entryconfigure(0, label=TxT["Stoppen"], font=FontM+SizeM)
        Menu_Aufnahme.entryconfigure(1, label=TxT["AlleStop"], font=FontM+SizeM)
        Menu_Aufnahme.entryconfigure(3, label=TxT["Rec Prog"], font=FontM+SizeM)
        Menu_Aufnahme.entryconfigure(5, label=TxT["Protokoll"], font=FontM+SizeM)
        Menu_Schedule.entryconfigure(0, label=TxT["Anzeigen"], font=FontM+SizeM)
        Menu_Schedule.entryconfigure(1, label=TxT["Hinzufügen"], font=FontM+SizeM)
        Menu_Schedule.entryconfigure(3, label=TxT["Bearbeiten"], font=FontM+SizeM)
        Menu_Hilfe.entryconfigure(0, label=TxT["Tastatur"], font=FontM+SizeM)
        Menu_Hilfe.entryconfigure(2, label=TxT["Über"], font=FontM+SizeM)

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
            Datei.write("nowrap=" + str(Zeilenumbruch.get()) + "\n")
            Datei.write("noprot=" + str(ProtMeldAus.get()) + "\n")
            Datei.close()
        Fenster.destroy()

#-----------------------------------------------------

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Einstellungen"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()

    Radio_Deutsch = tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=2, variable=GebietButton, value="de", text=TxT["Deutsch"], font="Helvetica 11")
    Radio_English = tk.Radiobutton(Fenster, relief="raised", overrelief="sunken", bd=2, variable=GebietButton, value="en", text=TxT["Englisch"], font="Helvetica 11")
    Check_StartBild = tk.Checkbutton(Fenster, bd=2, text=TxT["Zeilenumbruch"], font="Helvetica 11", variable=Zeilenumbruch)
    Check_Protokoll = tk.Checkbutton(Fenster, bd=2, text=TxT["Protokoll aus"], font="Helvetica 11", variable=ProtMeldAus)
    SizeMText = tk.Label(Fenster, text=TxT["Schrift Menü"], font="Helvetica 11")
    SizeLText = tk.Label(Fenster, text=TxT["Schrift Liste"], font="Helvetica 11")
    SizeMEingabe = tk.Entry(Fenster, bd=4, width=4, font="Helvetica 11")
    SizeLEingabe = tk.Entry(Fenster, bd=4, width=4, font="Helvetica 11")
    Button_Vorderg = tk.Button(Fenster, bd=2, text=TxT["VGfarbe"], font="Helvetica 11", command=Vordergrund_Einstellen)
    Button_Hinterg = tk.Button(Fenster, bd=2, text=TxT["HGfarbe"], font="Helvetica 11", command=Hintergrund_Einstellen)
    Button_Standard = tk.Button(Fenster, bd=2, text=TxT["FFschema"], font="Helvetica 11", command=Fensterfarbschema)
    m3uText = tk.Label(Fenster, text=TxT["pVerzeichnis"], font="Helvetica 10")
    m3uEingabe = tk.Entry(Fenster, bd=4, width=38, font="Helvetica 11")
    recText = tk.Label(Fenster, text=TxT["rVerzeichnis"], font="Helvetica 10")
    recEingabe = tk.Entry(Fenster, bd=4, width=38, font="Helvetica 11")
    startText = tk.Label(Fenster, text=TxT["sDatei"], font="Helvetica 10")
    startEingabe = tk.Entry(Fenster, bd=4, width=38, font="Helvetica 11")    
    Button_Speichern = tk.Button(Fenster, bd=2, text=TxT["Speichern"], font="Helvetica 11", command=Einstellungen_Speichern)
    Button_Abbrechen = tk.Button(Fenster, bd=2, text=TxT["Abbrechen"], font="Helvetica 11", command=Fenster.destroy)

    Radio_Deutsch.grid(row=1, column=0, padx=25, pady=20, ipadx=12, ipady=3, sticky="e")
    Radio_English.grid(row=1, column=1, padx=25, pady=20, ipadx=12, ipady=3, sticky="w")
    Check_StartBild.grid(row=2, column=0, columnspan=2, pady=1, ipadx=50, sticky="w")
    Check_Protokoll.grid(row=3, column=0, columnspan=2, pady=10, ipadx=50, sticky="w")
    SizeMText.grid(row=4, column=0, columnspan=2, pady=4, ipadx=60, sticky="w")
    SizeMEingabe.grid(row=4, column=1, padx=62, pady=4, sticky="e")
    SizeLText.grid(row=5, column=0, columnspan=2, pady=4, ipadx=60, sticky="w")
    SizeLEingabe.grid(row=5, column=1, padx=62, pady=4, sticky="e")
    Button_Vorderg.grid(row=6, column=0, columnspan=2, padx=50, pady=14, ipadx=57)
    Button_Hinterg.grid(row=7, column=0, columnspan=2, padx=50, pady=4, ipadx=59)
    Button_Standard.grid(row=8, column=0, columnspan=2, padx=50, pady=14, ipadx=47)
    m3uText.grid(row=9, column=0, columnspan=2, pady=1)
    m3uEingabe.grid(row=10, column=0, columnspan=2, pady=8)
    recText.grid(row=11, column=0, columnspan=2, pady=1)
    recEingabe.grid(row=12, column=0, columnspan=2, pady=8)
    startText.grid(row=13, column=0, columnspan=2, pady=1)
    startEingabe.grid(row=14, column=0, columnspan=2, pady=8)
    Button_Speichern.grid(row=15, column=0, padx=20, pady=20, ipadx=12, sticky="e")
    Button_Abbrechen.grid(row=15, column=1, padx=20, pady=20, ipadx=12, sticky="w")
    tk.Label(Fenster).grid(row=16, column=0)

    GebietButton.set(Gebiet)
    SizeMEingabe.insert(0, SizeM)
    SizeLEingabe.insert(0, SizeL)
    m3uEingabe.insert(0, m3uVerzeichnis)
    recEingabe.insert(0, recVerzeichnis)
    startEingabe.insert(0, startDatei)
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
        Text_Fenster = tk.Text(Fenster, width=44, height=36, pady=10, padx=10)
        Text_Fenster.config(foreground=FensterVG, background=FensterHG, font="Monospace 10", wrap="none")
        Text_Fenster.pack(fill="both", padx=3, pady=3)

        with open(keyDatei, "r") as Datei:
            Text_Fenster.configure(state="normal")
            Text_Fenster.delete("1.0", tk.END)
            Text_Fenster.insert(tk.END, "\n   Select stream:        <Arrow Keys ↑↓>")
            Text_Fenster.insert(tk.END, "\n   Previous streams:     <Arrow Keys ←→>\n")
            for i, Zeile in enumerate(Datei):
                Text_Fenster.insert(tk.END, "   " + Zeile)
                if i == 1:  Text_Fenster.insert(tk.END, "\n")
                if i == 9:  Text_Fenster.insert(tk.END, "\n")
            Text_Fenster.insert(tk.END, "\n   Scroll page:          <PgUp/PgDn>\n")
            Text_Fenster.insert(tk.END, "   Go to top:            <Home>\n")
            Text_Fenster.insert(tk.END, "   Go to end:            <End>\n")
            Text_Fenster.insert(tk.END, "   Close windows:        <Esc>\n\n")
            Text_Fenster.insert(tk.END, "   Select stream:    <left click>\n")
            Text_Fenster.insert(tk.END, "   View stream:      <left double-click>\n")
            Text_Fenster.insert(tk.END, "   Record stream:    <middle mouse-click>\n")
            Text_Fenster.insert(tk.END, "   Select player:    <right click>\n\n")
            Text_Fenster.configure(state="disabled")
            Datei.close()
        Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))

###############################################################################################################

def Hilfe_Ueber():

    def Einblenden():

        if Einblenden.Transparenz <= 80: 
            Einblenden.Transparenz += 1
            #Fenster.wm_attributes("-alpha", Einblenden.Transparenz / 70)
            Fenster.wm_attributes("-alpha", 1)
            Fenster.after(50, Einblenden)
        else:
            Einblenden.Zeichenkette = Einblenden.Zeichenkette[1:] + Einblenden.Zeichenkette[0]
            Lauftext.set(Einblenden.Zeichenkette[0:43])
            Fenster.after(100, Einblenden)

    Fenster = tk.Toplevel(Master)
    Fenster.title(TxT["Über"])
    Fenster.wm_attributes("-topmost", True)
    Fenster.grab_set()
    if os.path.isfile("/usr/share/icons/hicolor/128x128/apps/srecorder.png"):
        Hilfe_Ueber.Icon = tk.PhotoImage(file="/usr/share/icons/hicolor/128x128/apps/srecorder.png")
        Grafik = tk.Label(Fenster, image=Hilfe_Ueber.Icon)
        Grafik.pack(pady=20)
    else:
        tk.Label(Fenster).pack()
    Zeile1 = tk.Label(Fenster, text="Stream Recorder", font="Helvetica 18 bold")
    Zeile2 = tk.Label(Fenster, text="Version 1.40", font="Helvetica 12")
    Einblenden.Zeichenkette = TxT["Entwickelt"]
    Lauftext.set(Einblenden.Zeichenkette[0:43])
    Zeile3 = tk.Label(Fenster, textvariable=Lauftext, font="Helvetica 12")
    Zeile1.pack(padx=100, pady=10) 
    Zeile2.pack(pady=10) 
    Zeile3.pack(pady=20)
    tk.Label(Fenster).pack()
    #Fenster.wait_visibility()
    Einblenden.Transparenz = 50
    Einblenden()
    Fenster.bind("<Escape>", lambda event: Fenster_Schliessen(Fenster))


###############################################################################################################

def Vorheriger_Stream(i, event=None):

    global altPos

    if (i == -1 and altPos > 0) or (i == 1 and altPos < len(altName)-1):
        altPos += i
        cmdStrg = cmdPlayer.replace("URL[Nr]", altLink[altPos])    # Kommandostring zusammenbauen
        Statusleiste_Anzeigen(altName[altPos])
        subprocess.Popen(cmdStrg, shell=True)                      # Player starten
        Master.focus_force()
        Listen_Box.focus_set()                                     # Focus zurück auf Programmliste
    return "break"               # eingebaute <Pfeiltaste> in tk.Listbox verhindern

###############################################################################################################

def Programm_Beenden(event=None):

    NeuGeo = str(Master.winfo_width()) + "x" + str(Master.winfo_height())
    if not NeuGeo == HauptGeo:
        if message.askokcancel("Stream Recorder", "\n" + TxT["Groesse Fenster"]):
            with open(confDatei, "w") as Datei:
                Datei.write("m3u=" + m3uVerzeichnis + "\n")
                Datei.write("records=" + recVerzeichnis + "\n")
                Datei.write("start=" + startDatei + "\n")
                Datei.write("geometry=" + NeuGeo + "\n")
                Datei.write("fg=" + Vordergrund + "\n")
                Datei.write("bg=" + Hintergrund + "\n")
                Datei.write("fg2=" + FensterVG + "\n")
                Datei.write("bg2=" + FensterHG + "\n")
                Datei.write("size1=" + SizeM + "\n")
                Datei.write("size2=" + SizeL + "\n")
                Datei.write("language=" + Gebiet + "\n")
                Datei.write("nowrap=" + str(Zeilenumbruch.get()) + "\n")
                Datei.write("noprot=" + str(ProtMeldAus.get()) + "\n")
                Datei.close()

    if StatusAufnahmen == 0:
        Master.destroy()
    else:
        if message.askokcancel("Stream Recorder", "\n" + TxT["wirklich beenden"]):
            subprocess.Popen('killall ffmpeg', shell=True)
            if not ProtMeldAus.get():  
                with open(protDatei, "a") as Datei:
                    Datei.write(time.strftime("%d.%m.%y %H:%M > ") + "Alle Aufnahmen vom Benutzer beendet.\n")
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

Menu_Datei.add_command(label=TxT["Öffnen"], command=Datei_Oeffnen, accelerator=TxT["Strg"]+"O> ")
Menu_Datei.add_command(label=TxT["Bearbeiten"], command=Datei_Bearbeiten)
Menu_Datei.add_separator()
Menu_Datei.add_command(label=TxT["Player"], command=Player_Auswaehlen, accelerator=" <F4> ")
Menu_Datei.add_command(label=TxT["UserAgent"], command=User_Agent_Aendern)
Menu_Datei.add_command(label=TxT["Einstellungen"], command=Einstellungen, accelerator=" <F7> ")
Menu_Datei.add_separator()
Menu_Datei.add_command(label=TxT["Beenden"], command=Programm_Beenden, accelerator=TxT["Strg"]+"Q> ")

Menu_Suchen.add_command(label=TxT["Namen"], command=Suche_Namen)
Menu_Suchen.add_command(label=TxT["Land"], command=Suche_Land)
Menu_Suchen.add_command(label=TxT["Gruppe"], command=Suche_Gruppe)
Menu_Suchen.add_separator()
Menu_Suchen.add_command(label=TxT["Alle"], command=Alle_Anzeigen, accelerator=" <F3> ")

Menu_Favoriten.add_command(label=TxT["Anzeigen"], command=Favoriten_Anzeigen, accelerator=TxT["Strg"]+"F> ")
Menu_Favoriten.add_command(label=TxT["Hinzufügen"], command=Favoriten_Hinzufuegen)
Menu_Favoriten.add_separator()
Menu_Favoriten.add_command(label=TxT["Entfernen"], command=Favoriten_Entfernen)
Menu_Favoriten.add_separator()
Menu_Favoriten.add_command(label=TxT["Zurück"], command=Favoriten_Zurueck, accelerator=" <F2> ")

Menu_Aufnahme.add_command(label=TxT["Stoppen"], command=Aufnahme_Stoppen, accelerator=TxT["Strg"]+"A> ")
Menu_Aufnahme.add_command(label=TxT["AlleStop"], command=Alle_Beenden)
Menu_Aufnahme.add_separator()
Menu_Aufnahme.add_command(label=TxT["Rec Prog"], command=Aufnahme_Programm, accelerator=" <F6> ")
Menu_Aufnahme.add_separator()
Menu_Aufnahme.add_command(label=TxT["Protokoll"], command=Protokoll_Anzeigen, accelerator=TxT["Strg"]+"P> ")

Menu_Schedule.add_command(label=TxT["Anzeigen"], command=Schedule_Anzeigen, accelerator=TxT["Strg"]+"S> ")
Menu_Schedule.add_command(label=TxT["Hinzufügen"], command=Schedule_Hinzufuegen, accelerator=" <F9> ")
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
Listen_Box.bind(keyListe[7][22:], Aufnahme_Programm)
Listen_Box.bind(keyListe[8][22:], Einstellungen)
Listen_Box.bind(keyListe[9][22:], Schedule_Hinzufuegen)
Listen_Box.bind(keyListe[10][22:], Aufnahme_Stoppen)
Listen_Box.bind(keyListe[11][22:], Protokoll_Anzeigen)
Listen_Box.bind(keyListe[12][22:], Favoriten_Anzeigen)
Listen_Box.bind(keyListe[13][22:], Favoriten_Hinzufuegen)
Listen_Box.bind(keyListe[14][22:], Datei_Oeffnen)
Listen_Box.bind(keyListe[15][22:], Datei_Bearbeiten)
Listen_Box.bind(keyListe[16][22:], Schedule_Anzeigen)
Listen_Box.bind(keyListe[17][22:], Schedule_Bearbeiten)
Listen_Box.bind(keyListe[18][22:], Programm_Beenden)

#-----------------------------------------------------

Schedule_Starten()      # Schedule einmal pro Minute nach Terminen durchsuchen

Datei_Oeffnen()         # StartDatei laden oder Playlist auswählen

Master.protocol("WM_DELETE_WINDOW", Programm_Beenden)

Master.mainloop()

###############################################################################################################

