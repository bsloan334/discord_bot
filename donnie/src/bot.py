import discord
from discord.ext import commands
import os

# Set the command prefix
command_prefix = "!"

# Initialize the bot
intents = discord.Intents.default()
bot = commands.Bot(command_prefix=command_prefix, intents=intents)

# Load cogs
cogs_dir = "src/cogs"
for filename in os.listdir(cogs_dir):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

# Run the bot with the token
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)