# RUN: python3 motion_sensor.py
# RUN DISCORD BOT: bot.run(bot_token)


import RPi.GPIO as GPIO
import time
import subprocess
import os

import RPi.GPIO as GPIO
import time
import subprocess
import discord
from discord.ext import commands
import dotenv
import os

dotenv.load_dotenv()
#bot_token = "BOT_TOKEN"
bot_token = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='!')


def snimi_sliku():
    subprocess.run(["fswebcam", "-r", "1280x720", "--no-banner", putanja_slike])


@bot.command()
async def capture(ctx):
    snimi_sliku(ctx)
    with open(putanja_slike, "rb") as file:
        picture = discord.File(file)
        await ctx.send(file=picture)




# Postavi GPIO način rada
GPIO.setmode(GPIO.BCM)

# Onemogući GPIO upozorenja
GPIO.setwarnings(False)

# Odredi GPIO pin koji je povezan sa PIR senzorom
pir_pin = 17

# Postavi GPIO pin
GPIO.setup(pir_pin, GPIO.IN)

# Postavi putanju za spremanje slike
putanja_slike = "/tmp/slika.jpg"

# Postavi vremenski razmak između detekcija u sekundama
vremenski_razmak = 5

# Inicijalno postavi vrijeme zadnje detekcije na nulu
zadnja_detekcija = 0

# Provjeri postoji li datoteka i stvori je ako ne postoji
if not os.path.isfile(putanja_slike):
    open(putanja_slike, 'w').close()

# Funkcija za snimanje slike s USB kamere
def snimi_sliku():
    subprocess.run(["fswebcam", "-r", "1280x720", "--no-banner", putanja_slike])

try:
    while True:
        if GPIO.input(pir_pin):
            trenutno_vrijeme = time.time()
            if trenutno_vrijeme - zadnja_detekcija >= vremenski_razmak:
                print("Detektirano kretanje!")
                snimi_sliku()
                print("Slika je snimljena.")
                zadnja_detekcija = trenutno_vrijeme
        else:
            print("Nema detektiranog kretanja.")
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()
