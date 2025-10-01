# This example shows you a simple, non-interrupt way of reading Pico Display's buttons with a loop that checks to see if buttons are pressed.
# If you have a Display Pack 2.0" or 2.8" use DISPLAY_PICO_DISPLAY_2 instead of DISPLAY_PICO_DISPLAY

import time
from machine import Pin
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P4
from pimoroni import RGBLED

# We're only using a few colours so we can use a 4 bit/16 colour palette and save RAM!
display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, pen_type=PEN_P4, rotate=0)

display.set_backlight(0.5)
display.set_font("bitmap8")

button_a = Pin(12, Pin.IN, Pin.PULL_UP)
button_b = Pin(13, Pin.IN, Pin.PULL_UP)
button_x = Pin(14, Pin.IN, Pin.PULL_UP)
button_y = Pin(15, Pin.IN, Pin.PULL_UP)

# Set up the RGB LED For Display Pack and Display Pack 2.0":
led = RGBLED(6, 7, 8)

# For Display Pack 2.8" uncomment the line below and comment out the line above:
# led = RGBLED(26, 27, 28)

WHITE = display.create_pen(255, 255, 255)
BLACK = display.create_pen(0, 0, 0)
CYAN = display.create_pen(0, 255, 255)
MAGENTA = display.create_pen(255, 0, 255)
YELLOW = display.create_pen(255, 255, 0)
GREEN = display.create_pen(0, 255, 0)


# sets up a handy function we can call to clear the screen
def clear():
    display.set_pen(BLACK)
    led.set_rgb(0, 0, 0)
    display.clear()
    display.update()


# set up
clear()

while True:
    # button logic is reversed as we're using pull-ups
    if button_a.value() == 0:                             # if a button press is detected then...
        clear()                                           # clear to black
        display.set_pen(WHITE)                            # change the pen colour
        led.set_rgb(255, 255, 255)                        # set the LED colour to match
        display.text("Button A pressed", 10, 10, 240, 4)  # display some text on the screen
        display.update()                                  # update the display
        time.sleep(1)                                     # pause for a sec
        clear()                                           # clear to black again
    elif button_b.value() == 0:
        clear()
        display.set_pen(CYAN)
        led.set_rgb(0, 255, 255)
        display.text("Button B pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    elif button_x.value() == 0:
        clear()
        display.set_pen(MAGENTA)
        led.set_rgb(255, 0, 255)
        display.text("Button X pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    elif button_y.value() == 0:
        clear()
        display.set_pen(YELLOW)
        led.set_rgb(255, 255, 0)
        display.text("Button Y pressed", 10, 10, 240, 4)
        display.update()
        time.sleep(1)
        clear()
    else:
        display.set_pen(GREEN)
        led.set_rgb(0, 255, 0)
        display.text("Press any button!", 10, 10, 240, 4)
        display.update()
    time.sleep(0.1)  # this number is how frequently the Pico checks for button presses
