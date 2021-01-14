import sys
import spotipy as spotipy
import spotipy.util as util
import json
import time
import logging
import board
import urllib
import busio
import os
from writeToDisplay import *
import threading


def getImageUrl(currentSong): 
    with open("../logs/log.json", 'w+') as temp:
        temp.write(json.dumps(currentSong, indent=4))
    images = currentSong["item"]["album"]["images"]
    url = images[-1]['url']
    return url

def saveImage(url):
    albumCover = urllib.request.urlopen(url)
    with open ("../images/album_cover.jpg", 'wb') as temp:
        temp.write(albumCover.read())

def getAlbumInfo(currentSong):
    albumName = currentSong["item"]["album"]["name"]
    artistName = currentSong["item"]["artists"][0]["name"]
    return(artistName + " - " + albumName)

def update_screen(disp: adafruit_ssd1306.SSD1306_I2C, album: str):
    screen_thread = threading.Thread(target=writeAlbumTitle, name=f"{album.split(':')[0]}Thread", args=(disp, album, ))
    screen_thread.start()

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print('Usage %s Username ' % (sys.argv[0],))
    sys.exit()

scope = 'user-read-currently-playing'

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='../logs/songInfo.log',level=logging.INFO)

token = spotipy.util.prompt_for_user_token(
    username, scope, redirect_uri='http:/127.0.0.1/callback:8080')

if token:
    try:
        sp = spotipy.Spotify(auth=token)
        currentId = ""
        screenIsClear = True
        albumThreadStop = threading.Event()
        while True:
            currentSong = sp.currently_playing()
            if currentSong is not None and currentSong['currently_playing_type'] is not 'ad':
                try:
                    screenIsClear = False
                    songId = str(currentSong["item"]["id"])
                    if songId != currentId:
                        albumThreadStop.set()
                        currentId = songId
                        imageUrl = getImageUrl(currentSong)
                        saveImage(imageUrl)
                        songName = currentSong["item"]["name"]
                        os.system("sudo ../scripts/showImage.sh")
                        clearDisplay(disp)
                        albumThreadStop.clear()
                        screen_thread = threading.Thread(target=writeAlbumTitle, name=f"{songName}Thread", args=(disp, songName, getAlbumInfo(currentSong), albumThreadStop))
                        screen_thread.start()
                        print(songName)
                        print(getAlbumInfo(currentSong))
                        logging.info(f"{songName}:\t{getAlbumInfo(currentSong)}")
                except TypeError as error:
                    albumThreadStop.set()
                    os.system("sudo ../scripts/clearScreen.sh")
                    time.sleep(5)
            else:
                print("No song playing")
                if not screenIsClear:
                    clearDisplay(disp)
                    screenIsClear = True
                defaultScreen(disp)
                os.system("sudo ../scripts/showImage.sh")
            time.sleep(10)
    except TypeError as error:
        mos.system("sudo ../scripts/showImage.sh")
        clearDisplay(disp)
    except KeyboardInterrupt as error:
        albumThreadStop.set()
        os.system("sudo ../scripts/clearScreen.sh")
        clearDisplay(disp)
        sys.exit()

else:
    print("Can't get token for", username)
