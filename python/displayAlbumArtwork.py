#!/usr/bin/env python

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

def displayAlbumArtwork(matrix: RGBMatrix):
    with open('../images/album_cover.jpg', 'rb') as image_file:
        image = Image.open(image_file)

        # Make image fit our screen.
        image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
        matrix.SetImage(image.convert('RGB'))