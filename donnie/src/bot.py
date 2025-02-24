import discord
from discord.ext import commands
import os

CHANNEL_ID = 1342321534185767018

friends = [358779943632502785]

VOICE_CHANNEL_ID = 1342321534185767019





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
    print("Hello, Im really bad")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hello, Im really bad")


@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)

    await ctx.send(f"Result: {result}")



@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and after.channel.id == VOICE_CHANNEL_ID and not before.self_mute and after.self_mute:
        # User has started speaking
        print(f'{member.name} is speaking')
        voice_client = discord.utils.get(bot.voice_clients, guild=member.guild)
        if voice_client and not voice_client.is_playing():


            # Play a sound or speak a message
            source = discord.FFmpegPCMAudio ("C:/Users/erikh/dev/discord_bot/thornberry.mp3")
            voice_client.play(source, after=lambda e: print("player error: %s" % e) if e else None)







@bot.event
async def on_voice_state_update(member, before, after):
    channel = after.channel
    bot_connection = member.guild.voice_client

    if channel and member.id in friends:
        if bot_connection:
            await bot_connection.move_to(channel)
        else:
            await channel.connect()

    if not channel and bot_connection:
        await bot_connection.disconnect()




    



# Run the bot with the token
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)