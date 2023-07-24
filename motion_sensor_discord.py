# python3 motion_sensor_discord.py

import os
import RPi.GPIO as GPIO
import time
import subprocess
import asyncio
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

# Gmail account credentials
gmail_user = 'motion.detector2023@gmail.com'
gmail_password = 'motiondetector18'

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pir_pin = 17
GPIO.setup(pir_pin, GPIO.IN)

putanja_slike = "/tmp/slika.jpg"
vremenski_razmak = 5
zadnja_detekcija = 0

def snimi_sliku():
    result = subprocess.run(
        ["fswebcam", "-r", "1280x720", "--no-banner", putanja_slike],
        capture_output=True,
        text=True,
        
    )
    if result.returncode == 0:
        print("Slika snimljena.")
    else:
        print("Greška prilikom snimanja slike:")
        print(result.stderr)

def posalji_email():
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = 'nikolina.lekaj.tkt99@gmail.com'  # recipient's email address
    msg['Subject'] = 'Detektirano kretanje!'
    body = "Detektirano je kretanje. Pogledaj priloženu sliku."
    msg.attach(MIMEText(body, 'plain'))
    with open(putanja_slike, "rb") as file:
        img = MIMEImage(file.read(), name=os.path.basename(putanja_slike))
        msg.attach(img)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, msg['To'], msg.as_string())
        server.quit()
        print("Slika poslana na email.")
    except Exception as e:
        print(f"Greška prilikom slanja emaila: {e}")

async def motion_detection():
    global zadnja_detekcija
    while True:
        if GPIO.input(pir_pin):
            print("Detektiran pokret.")
            trenutno_vrijeme = time.time()
            if trenutno_vrijeme - zadnja_detekcija >= vremenski_razmak:
                snimi_sliku()
                posalji_email()
                zadnja_detekcija = trenutno_vrijeme
        else:
            print("Nema detekcije.")
        await asyncio.sleep(1)

async def main():
    await motion_detection()

if __name__ == "__main__":
    asyncio.run(main())