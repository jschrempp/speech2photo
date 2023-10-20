"""
Test the GPIO pins on the Raspberry Pi by blinking an LED


sudo apt-get install python3-rpi.gpio
pip install rpi.gpio

"""

import RPi.GPIO as GPIO
import time

# Set the pin numbering mode to BCM
GPIO.setmode(GPIO.BOARD)

# Set up pin 8 as an output
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

while True: # Run forever
    if GPIO.input(10) == GPIO.HIGH:
        print("Button was pushed!")

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
