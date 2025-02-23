import discord
from discord.ext import commands
import os

CHANNEL_ID = 1342321534185767018

# Set the command prefix
command_prefix = "!"

# Initialize the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=command_prefix, intents=intents)


# Load cogs
# cogs_dir = "src/cogs"
# for filename in os.listdir(cogs_dir):
#    if filename.endswith(".py"):
#        bot.load_extension(f"cogs.{filename[:-3]}")


@bot.event
async def on_ready():
    print("Hello, Im really bad")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello, Im really bad")


@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)

    await ctx.send(f"Result: {result}")



    



# Run the bot with the token
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)