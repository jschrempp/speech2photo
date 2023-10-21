import RPi.GPIO as GPIO
import threading
import time
from queue import Queue

# Set the pin numbering mode to BCM
GPIO.setmode(GPIO.BOARD)

# Set up pin 8 as an output
GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW)

# Define a function to blink the LED
def blink_led(q):
    print("Blinking LED")
    # initialize the blink time
    onTime = 0
    offTime = 1000  # a long time

    while True:
        # Get the blink time from the queue
        blink_time = q.get()

        if blink_time[0] == -1:
            # stop blinking
            print("Blink time -1: ", blink_time)
            GPIO.output(8, GPIO.LOW)
            onTime = 0
            offTime = 1000
        else:
            print("Blink time: ", blink_time)
            onTime = blink_time[0]
            offTime = blink_time[1]

        print("in blink cycle"  )
        # Turn the LED on
        GPIO.output(8, GPIO.HIGH)
        # Wait for blink_time seconds
        time.sleep(onTime)
        # Turn the LED off
        GPIO.output(8, GPIO.LOW)
        # Wait for blink_time seconds
        time.sleep(offTime)

# Create a new thread to blink the LED
q = Queue()
led_thread1 = threading.Thread(target=blink_led, args=(q,),daemon=True)
led_thread1.start()

# Continue running the main thread
blink_times = [0.2, 2]
while True:
    blink_times[0] += 0.2
    q.put(blink_times)
    # Wait for 10 seconds
    time.sleep(10)
    # Generate a random blink time between 0.5 and 2 seconds
    #blink_time = 5
    #q.put(blink_time)
    # put one message with two values in the queue



# Stop the LED thread
q.put(None)
led_thread1.join()

# Clean up the GPIO pins
GPIO.cleanup()
