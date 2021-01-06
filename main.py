import sys
import spotipy as spotipy
import spotipy.util as util
import json
import time
import logging
import urllib
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from displayAlbumArtwork import displayAlbumArtwork
import busio
from writeToDisplay import *

# Create the I2C interface.
i2c = busio.I2C(SCL, SDA)

# Create the SSD1306 OLED class.
# The first two parameters are the pixel width and pixel height.  Change these
# to the right size for your display!
disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

# Configure RGB matrix
options = RGBMatrixOptions()
options.rows = 64
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.gpio_slowdown = 2
options.hardware_mapping = 'regular'  # If you have an Adafruit HAT: 'adafruit-hat'

matrix = RGBMatrix(options = options)


if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print('Usage %s Username ' % (sys.argv[0],))
    sys.exit()

scope = 'user-read-currently-playing'

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='songInfo.log',level=logging.INFO)

token = spotipy.util.prompt_for_user_token(
    username, scope, redirect_uri='http:/127.0.0.1/callback:8080')

def getImageUrl(currentSong): 
    with open("log.json", 'w+') as temp:
        temp.write(json.dumps(currentSong, indent=4))
    images = currentSong["item"]["album"]["images"]
    url = images[-1]['url']
    return url

def saveImage(url):
    albumCover = urllib.request.urlopen(url)
    with open ("album_cover.jpg", 'wb') as temp:
        temp.write(albumCover.read())

def getAlbumInfo(currentSong):
    albumName = currentSong["item"]["album"]["name"]
    artistName = currentSong["item"]["artists"][0]["name"]
    return(albumName + " - " + artistName)


if token:
    try:
        sp = spotipy.Spotify(auth=token)
        currentId = ""
        while True:
            currentSong = sp.currently_playing()
            if type(currentSong) is not None:
                songId = str(currentSong["item"]["id"])
                if songId != currentId:
                    currentId = songId
                    imageUrl = getImageUrl(currentSong)
                    saveImage(imageUrl)
                    songName = currentSong["item"]["name"]
                    displayAlbumArtwork(matrix)
                    clearDisplay(disp)
                    writeAlbumTitle(disp, songName)
                    print(songName)
                    print(getAlbumInfo(currentSong))
                    logging.info(f"{songName}:\t{getAlbumInfo(currentSong)}")
            else:
                print("No song playing")
            time.sleep(5)
    except TypeError as error:
        print(error)
        sys.exit()

else:
    print("Can't get token for", username)

