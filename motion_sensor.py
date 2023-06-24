import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Konfiguracija PIR senzora pokreta
PIR_PIN = 17
GPIO.setup(PIR_PIN, GPIO.IN)

# Konfiguracija LED diode
LED_PIN = 18
GPIO.setup(LED_PIN, GPIO.OUT)

try:
    while True:
        if GPIO.input(PIR_PIN):
            print("Detektirano kretanje!")
            GPIO.output(LED_PIN, GPIO.HIGH)  # Uključi LED
            time.sleep(1)  # LED uključena 1 sekundu
            GPIO.output(LED_PIN, GPIO.LOW)  # Isključi LED
        time.sleep(0.1)  # Kratka pauza kako bi se izbjeglo pretjerano otkrivanje

except KeyboardInterrupt:
    GPIO.cleanup()
