# BEGIN: qv5z7j8d6p3m
import RPi.GPIO as GPIO
import threading
import time

# Set the pin numbering mode to BCM
GPIO.setmode(GPIO.BOARD)

# Set up pin 8 as an output
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

# Define a function to blink the LED
def blink_led(blink_time):
    print("Blinking LED with time: " + str(blink_time))
    while True:
        # Turn the LED on
        GPIO.output(8, GPIO.HIGH)
        # Wait for blink_time seconds
        time.sleep(blink_time)
        # Turn the LED off
        GPIO.output(8, GPIO.LOW)
        # Wait for blink_time seconds
        time.sleep(blink_time)

# Create a new thread to blink the LED
blink_time = 1
led_thread = threading.Thread(target=blink_led, args=(blink_time,),daemon=True)
led_thread.start()

# Continue running the main thread
while True:
    # Wait for 60 seconds
    time.sleep(10)
    # Generate a random blink time between 0.5 and 2 seconds
    blink_time = 5
    # Restart the LED thread with the new blink time
    led_thread = threading.Thread(target=blink_led, args=(blink_time,),daemon=True)
    led_thread.start()

# END: qv5z7j8d6p3m
