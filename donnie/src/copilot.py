import discord
from discord.ext import commands
import os
import numpy as np
import pyaudio

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

    # Initialize PyAudio
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    try:
        while True:
            data = stream.read(1024)
            if detect_voice(data):
                print(f'{ctx.author.name} is speaking')
                # You can add additional actions here, such as playing a sound
                source = discord.FFmpegPCMAudio("../assets/donnie.mp3")
                voice_client.play(source, after=lambda e: print("Player error: %s" % e) if e else None)
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        p.terminate()

# Run the bot with the token
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)