# python3 motion_sensor_discord.py

import discord
from discord.ext import commands
import os
import dotenv
import RPi.GPIO as GPIO
import time
import subprocess

# Učitajte token bota iz .env datoteke
dotenv.load_dotenv()
bot_token = os.getenv("DISCORD_TOKEN")


# Postavite GPIO način rada
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
pir_pin = 17
GPIO.setup(pir_pin, GPIO.IN)

putanja_slike = "/tmp/slika.jpg"
vremenski_razmak = 5
zadnja_detekcija = 0

# Funkcija za snimanje slike s USB kamere
def snimi_sliku():
    subprocess.run(["fswebcam", "-r", "1280x720", "--no-banner", putanja_slike])

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

target_channel_id = 1122952677765173430 # ID ciljnog kanala

@bot.command()
async def capture(ctx):
    target_channel = bot.get_channel(target_channel_id)
    if GPIO.input(pir_pin):
        trenutno_vrijeme = time.time()
        if trenutno_vrijeme - zadnja_detekcija >= vremenski_razmak:
            snimi_sliku()
            with open(putanja_slike, "rb") as file:
                picture = discord.File(file)
                zadnja_detekcija = trenutno_vrijeme
                await target_channel.send("Detektirano kretanje!")
                await target_channel.send(file=picture)
            
    else:
        print("Upozorenje! Nema detekcije kretanja.")
        await ctx.send("Nema detektiranog kretanja.")

@bot.event
async def on_ready():
    print(f'Bot je prijavljen kao {bot.user.name}')

bot.run(bot_token, reconnect=True)