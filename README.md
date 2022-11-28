# Stream-Recorder

### Description:
Stream Recorder plays and records video streams.

### Features:
- Supports standard m3u files.
- Create your own playlists.
- Add streams to favorites list.
- Select streams from play history.
- Timer shots once, daily or weekly.
- Create your own download command lines.
- Use youtube-dl or yt-dlp for more downloads.
- Media Player freely selectable (splayer.conf).
- User Agent freely selectable (useragent.conf).
- Color and font size are changeable.
- Directories can be customized.
- Language in English and German.
- and much more ...

![alt text](https://github.com/sc44/Stream-Recorder/blob/main/screenshot.png)

### Download manager:

Currently, the two download managers youtube-dl and yt-dlp can be integrated, provided they are also installed. 
They can also be used to record streams and videos which are not normally available. It should be noted that a few 
channels can only recorded without embedded download manager.

If you use download manager in expert mode, you can create your own download command lines. In schedule the 
desired line number must then be entered. So each stream can be recorded with its required command.

### Channel hopping:

With some media players you can also surf through the channel list e.g. Celluloid, SMPlayer and umpv. If you pull 
the main window very small, so that only the station names can be seen and then position the media player window 
next to it (not overlapping), you can do channel-hopping, start a recording if you want and then continue surfing. 

With the left and right arrow key it is possible to go back and forward in the play history. 
The TV feeling is perfect if you are owner of a USB remote control.

### Additional information:

As the program name suggests, this is a stream recorder. The fact that you can also use it to download videos is 
just a nice side effect. Streams are broadcast at specific times like TV, therefore a schedule with a timer is 
installed. In addition, streams run endless if they are not stopped, so sometime hard disk will overflow. 
For this reason the recordings must be stopped by user or timer.

On the other hand, videos can be recorded at any time and do not have to be terminated. However, this results in "dead" 
entries in the recording list. These do not further disturb and after end of recording they can be ignored or deleted.

### Arch Linux install:

https://aur.archlinux.org/packages/streamrecorder

### Requirements:

- python3
- python3-tk (tkinter)
- ffmpeg (ffplay)
- optional additional media player
- optional youtube-dl and yt-dlp

### Tested with:

- Windows 11
- Arch Linux 
- Linux-Mint

### License:
This project is licensed under the GNU GPL3 - see the LICENSE file for details
