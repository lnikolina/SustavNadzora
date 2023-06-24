# RUN DISCORD BOT: bot.run(bot_token)

import discord
from discord.ext import commands
import os
import dotenv

dotenv.load_dotenv()

bot_token = os.getenv("DISCORD_TOKEN")
bot = commands.Bot(command_prefix='!')

@bot.command()
async def capture(ctx):
    putanja_slike = "/tmp/slika.jpg"
    with open(putanja_slike, "rb") as file:
        picture = discord.File(file)
        await ctx.send(file=picture)

bot.run(bot_token)