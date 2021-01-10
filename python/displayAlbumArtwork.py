#!/usr/bin/env python

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
import os

def displayAlbumArtwork(matrix: RGBMatrix):
    with open('../images/album_cover.jpg', 'rb') as image_file:
        image = Image.open(image_file)

        # Make image fit screen.
        image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
        matrix.SetImage(image.convert('RGB'))
    # os.system("../showImage.sh")
    # os.system("sudo ../led-image-viewer --led-rows=64 --led-cols=64 --led-slowdown-gpio=4 /home/pi/Developer/spotify-matrix/images/album_cover.jpg")
