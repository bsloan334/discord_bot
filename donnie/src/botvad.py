import discord
from discord.ext import commands
import os
import numpy as np

CHANNEL_ID = 1342321534185767018

friends = [358779943632502785]

VOICE_CHANNEL_ID = 1342321534185767019

# Voice activity detection threshold
VAD_THRESHOLD = 0.05

# Set the command prefix
command_prefix = "!"

# Initialize the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=command_prefix, intents=intents)
intents.guilds = True
intents.voice_states = True




# Load cogs
# cogs_dir = "src/cogs"
# for filename in os.listdir(cogs_dir):
#    if filename.endswith(".py"):
#        bot.load_extension(f"cogs.{filename[:-3]}")






@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}')

@bot.event
async def on_voice_state_update(member, before, after):
    bot_connection = member.guild.voice_client

    # First event logic: Join or move to the same channel as a friend
    if after.channel and member.id in friends:
        if bot_connection:
            await bot_connection.move_to(after.channel)
        else:
            await after.channel.connect()

    # Second event logic: Disconnect if the bot is alone in the channel
    if not after.channel and bot_connection:
        await bot_connection.disconnect()

    # Third event logic: Trigger when a user unmutes
    if after.channel and after.channel.id == VOICE_CHANNEL_ID and before.self_mute and not after.self_mute:
        print(f'{member.name} is speaking')
        voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
        if voice_client and not voice_client.is_playing():
            source = discord.FFmpegPCMAudio("../assets/donnie.mp3")
            voice_client.play(source, after=lambda e: print("Player error: %s" % e) if e else None)

# Voice activity detection
def detect_voice(data):
    # Convert the data to a numpy array
    audio_data = np.frombuffer(data, dtype=np.int16)
    # Calculate the RMS (Root Mean Square) of the audio data
    rms = np.sqrt(np.mean(audio_data**2))
    return rms > VAD_THRESHOLD

@bot.command()
async def start_vad(ctx):
    voice_client = ctx.voice_client
    if not voice_client:
        await ctx.send('Bot is not connected to a voice channel.')
        return

    stream = voice_client.stream()
    async for data in stream:
        if detect_voice(data):
            print(f'{ctx.author.name} is speaking')
            # You can add additional actions here, such as playing a sound
            source = discord.FFmpegPCMAudio("../assets/donnie.mp3")
            voice_client.play(source, after=lambda e: print("Player error: %s" % e) if e else None)


# Run the bot with the token
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)