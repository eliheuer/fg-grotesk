# This script is meant to be run from the root level
# of your font's git repository. For example, from a Unix terminal:
# $ git clone my-font
# $ cd my-font
# $ python3 documentation/image1.py --output documentation/image1.png

import argparse

# Import moduels from the Python Standard Library: https://docs.python.org/3/library/
import subprocess
import sys

# Import moduels from external python packages: https://pypi.org/
from drawbot_skia.drawbot import *
from fontTools.misc.fixedTools import floatToFixedToStr
from fontTools.ttLib import TTFont

# Constants, these are the main "settings" for the image
WIDTH, HEIGHT, MARGIN, FRAMES = 4096, 4096, 512, 1
FONT_PATH = "fonts/FGGrotesk-Regular.ttf"
FONT_LICENSE = "OFL v1.1"
AUXILIARY_FONT = "Helvetica"
AUXILIARY_FONT_SIZE = 48

GRID_VIEW = True  # Toggle this for a grid overlay
GRID_VIEW = False  # Toggle this for a grid overlay

# Handel the "--output" flag
# For example: $ python3 documentation/image1.py --output documentation/image1.png
parser = argparse.ArgumentParser()
parser.add_argument("--output", metavar="PNG", help="where to write the PNG file")
args = parser.parse_args()

# Load the font with the parts of fonttools that are imported with the line:
# from fontTools.ttLib import TTFont
# Docs Link: https://fonttools.readthedocs.io/en/latest/ttLib/ttFont.html
ttFont = TTFont(FONT_PATH)

# Constants that are worked out dynamically
MY_URL = subprocess.check_output("git remote get-url origin", shell=True).decode()
MY_HASH = subprocess.check_output("git rev-parse --short HEAD", shell=True).decode()
FONT_NAME = ttFont["name"].getDebugName(4)
FONT_VERSION = "v%s" % floatToFixedToStr(ttFont["head"].fontRevision, 16)


# Draws a grid
def grid():
    stroke(1, 0, 0, 0.75)
    strokeWidth(2)
    STEP_X, STEP_Y = 0, 0
    INCREMENT_X, INCREMENT_Y = MARGIN / 2, MARGIN / 2
    rect(MARGIN, MARGIN, WIDTH - (MARGIN * 2), HEIGHT - (MARGIN * 2))
    for x in range(61):
        polygon((MARGIN + STEP_X, MARGIN), (MARGIN + STEP_X, HEIGHT - MARGIN))
        STEP_X += INCREMENT_X
    for y in range(29):
        polygon((MARGIN, MARGIN + STEP_Y), (WIDTH - MARGIN, MARGIN + STEP_Y))
        STEP_Y += INCREMENT_Y
    polygon((WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    polygon((0, HEIGHT / 2), (WIDTH, HEIGHT / 2))


# Draws a display grid
def display_grid():
    fill(None)
    stroke(1, 1, 1, 1)
    strokeWidth(12)
    STEP_X, STEP_Y = 0, 0
    INCREMENT_X, INCREMENT_Y = MARGIN / 2, MARGIN / 2
    rect(MARGIN, MARGIN, WIDTH - (MARGIN * 2), HEIGHT - (MARGIN * 3))
    for x in range(12):
        polygon((MARGIN + STEP_X, MARGIN), (MARGIN + STEP_X, HEIGHT - MARGIN * 2))
        STEP_X += INCREMENT_X
    for y in range(11):
        polygon((MARGIN, MARGIN + STEP_Y), (WIDTH - MARGIN, MARGIN + STEP_Y))
        STEP_Y += INCREMENT_Y
    #polygon((WIDTH / 2, 0), (WIDTH / 2, HEIGHT))
    #polygon((0, HEIGHT / 2), (WIDTH, HEIGHT / 2))


# Remap input range to VF axis range
# This is useful for animation
# (E.g. sinewave(-1,1) to wght(100,900))
def remap(value, inputMin, inputMax, outputMin, outputMax):
    inputSpan = inputMax - inputMin  # FIND INPUT RANGE SPAN
    outputSpan = outputMax - outputMin  # FIND OUTPUT RANGE SPAN
    valueScaled = float(value - inputMin) / float(inputSpan)
    return outputMin + (valueScaled * outputSpan)


# Draw the page/frame and a grid if "GRID_VIEW" is set to "True"
def draw_background():
    newPage(WIDTH, HEIGHT)
    fill(0)
    rect(-2, -2, WIDTH + 2, HEIGHT + 2)
    if GRID_VIEW:
        grid()
    else:
        pass


# Draw main text
def draw_main_text():
    fill(1)
    stroke(None)
    font(FONT_PATH)

    fontSize(547)
    fontSize(564)
    fontSize(560)
    fontSize(562)
    fontSize(564)
    fontSize(578.75)
    #fontSize(552)
    #text("Font.Garden", (1*MARGIN, (6*MARGIN)+24))
    text("Font.Garden", (0.92*MARGIN, (6*MARGIN)+58))

# Draw rects
def draw_rects():
    fill(1)
    stroke(None)
#    rect(1*MARGIN, 1*MARGIN, 0.5*MARGIN, 0.5*MARGIN)
#    rect(2*MARGIN, 1*MARGIN, 0.5*MARGIN, 0.5*MARGIN)
#    rect(3*MARGIN, 1*MARGIN, 0.5*MARGIN, 0.5*MARGIN)
#    rect(4*MARGIN, 1*MARGIN, 0.5*MARGIN, 0.5*MARGIN)
#    rect(5*MARGIN, 1*MARGIN, 0.5*MARGIN, 0.5*MARGIN)
#    rect(6*MARGIN, 1*MARGIN, 0.5*MARGIN, 0.5*MARGIN)

# Build and save the image
if __name__ == "__main__":
    draw_background()
    draw_main_text()
    display_grid()
    draw_rects()
    # Save output, using the "--output" flag location
    saveImage(args.output)
    # Print done in the terminal
    print("DrawBot: Done")
