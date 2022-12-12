import discord
from discord.ext import commands
import time
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
BOT_MEMBER_ID = os.getenv('BOT_MEMBER_ID')
bot = commands.Bot(intents=discord.Intents.default(), command_prefix = "!")

@bot.event
async def on_ready():
    print("Bot is ready!")
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    BOT_MEMBER_ID = bot.user.id
    print('------')

@bot.command()
async def ping(ctx):
    ping_ = bot.latency
    ping =  round(ping_ * 1000)
    await ctx.send(f"my ping is {ping}ms")

@bot.event
async def on_voice_state_update(member, before, after):
    if str(member.id) == BOT_MEMBER_ID:
        #Bot moving. Discard
        return
    files = os.listdir(os.curdir+"/clips")
    users = []
    for file in files:
        if file[-3:] == "mp3":
            users.append(file[:-4])
    if str(member.id) not in users:
        print(member.name + ' (' + str(member.id) + ') doesnt have a clip')
        return

    # grab the user who sent the command
    voice_channel = after.channel

    # only play music if user is in a voice channel
    if voice_channel != None and before.channel != after.channel:
        # grab user's voice channel
        channel_name = voice_channel.name
        print(member.name + ' (' + str(member.id) + ') joined channel: '+ channel_name)
        # create StreamPlayer
        # check if bot is in here
        # if it is then wait
        try:
            vc= await voice_channel.connect()
        except discord.errors.ClientException:
            print("BOT ALREADY PLAYING")
            return
        try:
            print(str(member.id) + '.mp3')
            vc.play(discord.FFmpegPCMAudio('clips/' + str(member.id) + '.mp3'), after=lambda e: print('done playing. Error? ', e))
            while vc.is_playing():
                await asyncio.sleep(.1)
            # disconnect after the player has finished
            vc.stop()
        except Exception as e:
            print("RAN INTO AN ERROR: ")
            print(e)
        await vc.disconnect()
    elif before.channel == after.channel:
        print(member.name + ' changed state.')
    else:
        print(member.name + ' left a channel.')


if __name__ == "__main__" :
    bot.run(DISCORD_TOKEN)
