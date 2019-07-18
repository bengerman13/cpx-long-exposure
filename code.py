import time
from adafruit_circuitplayground.express import cpx

import digitalio
import board

TIMER_INCREMENT_SHORT = 0.5
TIMER_INCREMENT_LONG = 30

PIXEL_ON = 0.004
PIXEL_OFF = 0

RED = (255, 0, 0)
BLUE = (0,0,255)
GREEN = (0, 255, 0)

MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

WHITE = (255, 255, 255)

COLORS = [WHITE, BLUE, CYAN, GREEN, YELLOW, RED, MAGENTA]

NUM_PIXELS = len(cpx.pixels)


class State:

    def __init__(self):
        self.lock = False
        self.clicks = 0

    def increase_timer(self):
        self.clicks += 1
        return self.colors()

    def decrease_timer(self):
        self.clicks -= 1
        return self.colors()

    def colors(self):
        base_color = self.clicks // NUM_PIXELS
        base_color = base_color % len(COLORS)
        next_color = base_color + 1
        next_color = next_color % len(COLORS)
        base_color = COLORS[base_color]
        next_color = COLORS[next_color]
        num_next_color = self.clicks % NUM_PIXELS 
        color_state = [base_color] * NUM_PIXELS
        if num_next_color:
            color_state[0:num_next_color] = [next_color] * num_next_color
        return color_state

class hold_down:

    def __init__(self, pin):
        self.pin = pin

    def __enter__(self):
        self.pin.value = True

    def __exit__(self, *exc):
        self.pin.value = False

def focus(pin):
    with hold_down(pin):
        time.sleep(1) # try *real* hard to focus
    time.sleep(0.25) # pause for shake

def main():
    exposure_time = TIMER_INCREMENT_LONG
    cpx.red_led = False

    cpx.detect_taps = 1

    # the pin for the shutter button
    shutter = digitalio.DigitalInOut(board.D10)
    shutter.switch_to_output(value=False)

    # the pin for the autofocus button
    af = digitalio.DigitalInOut(board.A4)
    af.switch_to_output(value=False)

    state = State()
    cpx.pixels[0:NUM_PIXELS] = state.colors()
    while True:
        if cpx.button_a:
            if not state.lock:
                state.lock = True
                cpx.pixels[0:NUM_PIXELS] = state.increase_timer()
        else:
            state.lock = False
        if cpx.button_b:
            with hold_down(shutter):
                while state.clicks > 0:
                    if cpx.switch:
                        cpx.pixels.brightness = PIXEL_ON
                    else:
                        cpx.pixels.brightness = PIXEL_OFF
                    if cpx.button_a:
                        state.lock = True
                        state.clicks = 0
                        cpx.pixels[0:NUM_PIXELS] = state.colors()
                        break # give a way to bail other than yanking the cord from the camera
                    time.sleep(exposure_time)
                    cpx.pixels[0:NUM_PIXELS] = state.decrease_timer()
        if cpx.tapped:
            if exposure_time == TIMER_INCREMENT_SHORT:
                exposure_time = TIMER_INCREMENT_LONG
                cpx.red_led = False
            else:
                exposure_time = TIMER_INCREMENT_SHORT
                cpx.red_led = True
        if cpx.switch:
            cpx.pixels.brightness = PIXEL_ON
        else:
            cpx.pixels.brightness = PIXEL_OFF
       
if __name__ == "__main__":
    main()
