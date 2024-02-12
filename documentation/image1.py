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
WIDTH, HEIGHT, MARGIN, FRAMES = 4096, 2048, 256, 1
FONT_PATH = "fonts/FGGrotesk-Regular.ttf"
FONT_LICENSE = "OFL v1.1"
AUXILIARY_FONT = "Helvetica"
AUXILIARY_FONT_SIZE = 48

BIG_TEXT = "AFont.Garden™"
BIG_TEXT_SIDE_MARGIN = MARGIN * 1
BIG_TEXT_BOTTOM_MARGIN = MARGIN * 5

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
    text(BIG_TEXT, (BIG_TEXT_SIDE_MARGIN, BIG_TEXT_BOTTOM_MARGIN))

    fontSize(410)
    # text(BIG_TEXT, (BIG_TEXT_SIDE_MARGIN, BIG_TEXT_BOTTOM_MARGIN - (MARGIN * 1.5)))

    fontSize(280)
    # text(BIG_TEXT, (BIG_TEXT_SIDE_MARGIN, BIG_TEXT_BOTTOM_MARGIN - (MARGIN * 2.5)))

    fontSize(230)
    text(BIG_TEXT, (BIG_TEXT_SIDE_MARGIN, BIG_TEXT_BOTTOM_MARGIN - (MARGIN * 3.5)))

    fontSize(60)
    # text(BIG_TEXT, (BIG_TEXT_SIDE_MARGIN, BIG_TEXT_BOTTOM_MARGIN - (MARGIN * 3.25)))

    fontSize(50)
    text(
        BIG_TEXT, (BIG_TEXT_SIDE_MARGIN, BIG_TEXT_BOTTOM_MARGIN - (MARGIN * 4))
    )  # 3.375


# Build and save the image
if __name__ == "__main__":
    draw_background()
    draw_main_text()
    # Save output, using the "--output" flag location
    saveImage(args.output)
    # Print done in the terminal
    print("DrawBot: Done")
