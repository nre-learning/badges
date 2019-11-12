# NRE Labs Badge Code

import time
import board
import neopixel
import displayio
from digitalio import DigitalInOut
import adafruit_imageload
from gamepadshift import GamePadShift

pixel_pin = board.D8
num_pixels = 5

pixels = neopixel.NeoPixel(pixel_pin, num_pixels,
                           brightness=0.1, auto_write=False)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)


def color_chase(color, wait):
    for i in range(num_pixels):
        pixels[i] = color
        time.sleep(wait)
        pixels.write()
        time.sleep(0.5)


def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            rc_index = (i * 256 // num_pixels) + j
            pixels[i] = wheel(rc_index & 255)
        pixels.write()

def blackout():
    for i in range(num_pixels):
        pixels[i] = OFF
        pixels.write()

OFF = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)


display = board.DISPLAY

# Open the file
with open("/nrelabs-pixels.bmp", "rb") as bitmap_file:
 
    # Setup the file as the bitmap data source
    bitmap = displayio.OnDiskBitmap(bitmap_file)

    # Create a sprite (tilegrid)
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=displayio.ColorConverter())

    # Create a Group to hold the TileGrid
    group = displayio.Group()

    # Add the TileGrid to the Group
    group.append(tile_grid)

    # Add the Group to the Display
    display.show(group)

    show_rainbow = False
    blackout()

    pad = GamePadShift(DigitalInOut(board.BUTTON_CLOCK),
                    DigitalInOut(board.BUTTON_OUT),
                    DigitalInOut(board.BUTTON_LATCH))

    # Button Constants
    BUTTON_LEFT = 128
    BUTTON_UP = 64
    BUTTON_DOWN = 32
    BUTTON_RIGHT = 16
    BUTTON_SEL = 8
    BUTTON_START = 4
    BUTTON_A = 2
    BUTTON_B = 1

    while True:
        buttons = pad.get_pressed()
        if (buttons & BUTTON_START) > 0:
            if show_rainbow:
                show_rainbow = False
                blackout()
            else:
                show_rainbow = True


            # Wait for button to be released
            while buttons != 0:
                buttons = pad.get_pressed()
                time.sleep(0.1)

        if show_rainbow:
            rainbow_cycle(0)
        else:
            time.sleep(0.1)
