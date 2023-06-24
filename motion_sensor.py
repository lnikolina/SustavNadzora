# RUN: python3 motion_sensor.py

import RPi.GPIO as GPIO
import time

# Postavi GPIO način rada
GPIO.setmode(GPIO.BCM)

# Onemogući GPIO upozorenja
GPIO.setwarnings(False)

# Odredi GPIO pin koji je povezan sa PIR senzorom
pir_pin = 17

# Postavi GPIO pin
GPIO.setup(pir_pin, GPIO.IN)

try:
    while True:
        if GPIO.input(pir_pin):
            print("Detektirano kretanje!")
        else:
            print("Nema detektiranog kretanja.")
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()

