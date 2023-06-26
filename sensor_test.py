import RPi.GPIO as GPIO
import time

# Set up GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pir_pin = 17
GPIO.setup(pir_pin, GPIO.IN)

# Main loop
try:
    while True:
        if GPIO.input(pir_pin):
            print("Motion detected")
        else:
            print("No motion detected")
        time.sleep(1)  # Wait for 1 second before checking again

except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()