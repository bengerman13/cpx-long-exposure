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


def focus(pin):
    try:
        pin.value = True
        time.sleep(1) # try *real* hard to focus
    except:
        pass
    finally:
        pin.value = False


def main():
    exposure_time = TIMER_INCREMENT_LONG
    cpx.red_led = False

    cpx.detect_taps = 1
    shutter = digitalio.DigitalInOut(board.D10)
    shutter.switch_to_output(value=False)
    af = digitalio.DigitalInOut(board.A4)
    af.switch_to_output(value=False)

    state = State()
    cpx.pixels[0:NUM_PIXELS] = state.colors()
    while True:
        if cpx.button_a and not cpx.button_b:
            if not state.lock:
                state.lock = True
                cpx.pixels[0:NUM_PIXELS] = state.increase_timer()
        else:
            state.lock = False
        if cpx.button_b and not cpx.button_a:
            focus(af)
            time.sleep(0.25) # pause for shake
            while state.clicks > 0:
                shutter.value = True
                if cpx.switch:
                    cpx.pixels.brightness = PIXEL_ON
                else:
                    cpx.pixels.brightness = PIXEL_OFF
                time.sleep(exposure_time)
                cpx.pixels[0:NUM_PIXELS] = state.decrease_timer()
                shutter.value = False
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
