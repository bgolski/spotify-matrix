import time
import subprocess
 
from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

def clearDisplay(disp: adafruit_ssd1306.SSD1306_I2C):
    # Clear display.
    disp.fill(0)
    disp.show()

def writeAlbumTitle(disp: adafruit_ssd1306.SSD1306_I2C, album: str):
    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    width = disp.width
    height = disp.height
    image = Image.new("1", (width, height))
    font = ImageFont.load_default()
    
    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)
    
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    
    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = 0
    top = padding
    bottom = height - padding
    # Move left to right keeping track of the current x position for drawing shapes.
    x = 0
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
 
    draw.text(((width / 2), top), album, font=font, fill=255)
 
    # Display image.
    disp.image(image)
    disp.show()
