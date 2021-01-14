from board import SCL, SDA
import busio
import sys
import time
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

def clearDisplay(disp: adafruit_ssd1306.SSD1306_I2C):
    # Clear display.
    disp.fill(0)
    disp.show()

def writeAlbumTitle(disp: adafruit_ssd1306.SSD1306_I2C, songName: str, artistAndAlbumName: str, albumThreadStop):
    try:
        # Initialize display.
        clearDisplay(disp)
        WIDTH = disp.width
        HEIGHT = disp.height

        scrollingName = False
        scrollingAlbum = False

        img = Image.new("1", (WIDTH, HEIGHT))

        drawSong = ImageDraw.Draw(img)
        drawAlbum = ImageDraw.Draw(img)

        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)

        songNameX, songNameY = drawSong.textsize(songName, font)
        albumInfoX, albumInfoY = drawAlbum.textsize(artistAndAlbumName, font)

        if (songNameX > 100):
            scrollingName = True
        if (albumInfoX > 100):
            scrollingAlbum = True

        text_x = disp.width
        text_y = (HEIGHT - songNameY) / 2

        t_start = time.time()

        while not albumThreadStop.is_set():
            x = (time.time() - t_start) * 50
            x %= (songNameX + WIDTH)
            y = (time.time() - t_start) * 50
            y %= (albumInfoX + WIDTH)
            drawSong.rectangle((0, 0, WIDTH, (HEIGHT / 2)), (0))
            drawAlbum.rectangle((0,(HEIGHT / 2), WIDTH, HEIGHT), (0))
            if scrollingName:
                drawSong.text((int(text_x - x), (text_y / 2)), songName, font=font, fill=(255))
            else:
                drawSong.text((((WIDTH / 2) - (songNameX / 2)), (text_y / 2)), songName, font=font, fill=255)

            if scrollingAlbum:   
                drawAlbum.text((int(text_x - y), (text_y * 2)), artistAndAlbumName, font=font, fill=255)
            else:
                drawAlbum.text((((WIDTH / 2) - (albumInfoX / 2)), (text_y * 2)), "hello", font=font, fill=255)
            disp.image(img)
            disp.show()
        clearDisplay(disp)
    except KeyboardInterrupt as error:
        clearDisplay(disp)
        sys.exit()


def defaultScreen(disp: adafruit_ssd1306.SSD1306_I2C):
    width = 128
    height = 64
    image = Image.open("../images/SpotifyCode.jpg")
    image_r = image.resize((width,height), Image.BICUBIC)
    image_bw = image_r.convert("1")

    for x in range(width):
            for y in range(height):
                    disp.pixel(x,y,bool(int(image_bw.getpixel((x,y)))))
    
    disp.show()