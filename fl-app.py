#!/usr/bin/python3

from flask import request
from flask_api import FlaskAPI
import board
import threading
import neopixel
import time

num_points = 150

RED = (255, 0, 0)
YELLOW = (255, 150, 0)
GREEN = (0, 255, 0)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
PURPLE = (180, 0, 255)
WHITE = (255, 255, 255)
OFF = (0, 0, 0)

LEDS = {"red":RED,"yellow":YELLOW,"green":GREEN,"cyan":CYAN,"blue":BLUE,"purple":PURPLE,"white":WHITE,"off":OFF}

pixel_pin = board.D18

num_pixels = 9

ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False, pixel_order=ORDER)
pixels.fill(OFF)
pixels.show()
state = 0

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

app = FlaskAPI(__name__)
@app.before_first_request
def activate_job():
    def run_job():
        global state
        while True:
            for x in range(num_points):
                if state == 0:
                    bright = 0
                elif state == 1:
                    bright = 0.3
                else:
                    bright = 0.3 * (1.0 - abs((2.0*(x/num_points))-1.0))
                #print(pwm,"\n")
                pixels.brightness = bright
                pixels.show()
                time.sleep(0.01)

    thread = threading.Thread(target=run_job)
    thread.start()

@app.route('/', methods=["GET"])
def api_root():
    return {
           "led_url": request.url + "led/<color>/",
             "led_url_POST": {"state": "(0 | 1)"}
                 }

@app.route('/led/<color>/', methods=["GET", "POST"])
def api_leds_control(color):
    global state
    if request.method == "POST":
        if color in LEDS:
            state = int(request.data.get("state"))
            pixels.fill(LEDS[color])
            pixels.show()
    return {color: color}

if __name__ == "__main__":
    app.run()
