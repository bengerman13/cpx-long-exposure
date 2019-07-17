# cpx-long-exposure

## DISCLAIMER
I am not an electrical engineer, or any kind of expert. This was a series of lucky guesses, and a little 
bit of thinking on my part. It has not damaged my camera, but I cannot guarantee it will not damage yours.
Use with caution!

## What it do?

Takes long exposures on a Canon camera using a Circuit Playground Express (CPX) and a cannibalized
remote, similar to the RS-60E3.

## How do I use it?

First, wire it up (obviously), but you probably want to know what you'll get before that:

Press the `A` button to increase exposure time. As you click, you'll see the LEDs change colors
 to indicate how many time increments you've added. In "normal mode", exposure is increased 30 seconds
per click. In "demo mode", exposure is increased in 0.5 second steps.

Press the `B` button to take a picture. The camera with then attempt for one second to focus, wait for
a quarter second, then take the picture. The LEDs then count down to give some indication how much time is left.

Tap to switch between "normal mode" and "demo mode". The red led by the USB port indicates you're in "demo mode"

Toggle the switch to turn off the lights.

## How do I wire it up?

You'll need:
- 2 SPST (single pole/single throw) relays suitable for 3.3v DC. We'll call one the `focus relay` and the other the `shutter relay`
- a 2.5mm TRS connector. I took mine out of a broken, off-brand RS-60E3. These are also called stereo connectors, but they're a 
size smaller than the one your phone has
- a little bit of extra wire, I used 24 AWG, but I'm not an expert

### Shutter relay
A3 on the CPX goes to the positive side of the shutter relay's coil.
GND on the CPX (there are three GNDs, they all work) goes to the negative side of the shutter relay coil.
The one relay contact is connected to the wire leading to TRS connector sleeve (closest to the pigtail), the other leads to the 
TRS connector tip.

### Focus relay
A4 on the CPX goes to the positive side of the focus relay coil.
GND on the CPX goes to the negative side of the relay's coil.
The one relay contact is connected to the wire leading to TRS connector ring (middle), the other leads to the 
TRS connector tip.

Something like this:
```
                      +---------------------------+
A3 -------------------|+ coil               coil -|--------- GND
                      |       SHUTTER RELAY       |
barrel sleeve --------|- contact         contact +|--------- barrel tip
                      +---------------------------+

                      +---------------------------+
A4 -------------------|+ coil               coil -|--------- GND
                      |        FOCUS RELAY        |
barrel sleeve --------|- contact         contact +|--------- barrel ring
                      +---------------------------+
```
_barrel sleeve_ means the segment of the barrel connector closest to the pigtail
_barrel ring_ means the segment of the barrel connector between the bottom and the tip
_barrel tip_ means the end of the barrel connector farthest from the pigtail

## How do I program it?
Just copy `code.py` to your Circuit Playground Express. This assumes you already have already installed 
CircuitPython on your device

