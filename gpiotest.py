"""
Test the GPIO pins on the Raspberry Pi by blinking an LED


sudo apt-get install python3-rpi.gpio

"""

import RPi.GPIO as GPIO
import time

# Set the pin numbering mode to BCM
GPIO.setmode(GPIO.BOARD)

# Set up pin 8 as an output
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

# Blink the LED 5 times
for i in range(25):
    # Turn the LED on
    GPIO.output(8, GPIO.HIGH)
    # Wait for 1 second
    time.sleep(1)
    # Turn the LED off
    GPIO.output(8, GPIO.LOW)
    # Wait for 1 second
    time.sleep(1)

# Clean up the GPIO pins
GPIO.cleanup()
