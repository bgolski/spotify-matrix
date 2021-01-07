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

# def writeAlbumTitle(disp: adafruit_ssd1306.SSD1306_I2C, album: str):
#     # Create blank image for drawing.
#     # Make sure to create image with mode '1' for 1-bit color.
#     width = disp.width
#     height = disp.height
#     image = Image.new("1", (width, height))
#     # font = ImageFont.load_default()
#     font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 3)
#     # Get drawing object to draw on image.
#     draw = ImageDraw.Draw(image)
#     w, h = draw.textsize(album.encode('utf-8', 'ignore'))
#     print(w,h)
#     # Draw a black filled box to clear the image.
#     draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
#     # Draw some shapes.
#     # First define some constants to allow easy resizing of shapes.
#     padding = 0
#     top = padding
#     bottom = height - padding
#     # Move left to right keeping track of the current x position for drawing shapes.
#     x = 0
#     # Draw a black filled box to clear the image.
#     draw.rectangle((0, 0, width, height), outline=0, fill=0)
#     draw.text(((width-w)/2,(height-h)/2), album.encode('utf-8', 'ignore'), fill="white")
#     # draw.text(((width / 2), top), album.encode('utf-8', 'ignore'), font=font, fill=255)
 
#     # Display image.
#     disp.image(image)
#     disp.show()

def writeAlbumTitle(disp: adafruit_ssd1306.SSD1306_I2C, message: str, albumThreadStop):
    try:
        # Initialize display.
        clearDisplay(disp)

        WIDTH = disp.width
        HEIGHT = disp.height


        img = Image.new("1", (WIDTH, HEIGHT))

        draw = ImageDraw.Draw(img)
        

        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)

        size_x, size_y = draw.textsize(message, font)

        text_x = disp.width
        text_y = (HEIGHT - size_y) / 2

        t_start = time.time()

        while not albumThreadStop.is_set():
            x = (time.time() - t_start) * 50
            x %= (size_x + disp.width)
            draw.rectangle((0, 0, disp.width, 80), (0))
            draw.text((int(text_x - x), text_y), message, font=font, fill=(255))
            disp.image(img)
            disp.show()
        clearDisplay(disp)
    except:
        print(sys.exc_info())
