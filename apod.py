import requests
import asyncio
import discord
from discord.ext import commands
from datetime import datetime, time, timedelta

# set bot command prefix to $
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix="$", intents=intents)

# time to post image
WHEN = time(22, 0, 0) # 3:00PM (22, 0, 0)

# when bot programmed starts running
@bot.event
async def on_ready():
    # print statement
    print("Bot is online")
    # go to function
    await background_task()

# checks the time
async def background_task():
    # current time
    now = datetime.utcnow()
    # make sure loop doesn't start after {WHEN} as then it will send immediately the first time as negative seconds will make the sleep yield instantly
    if now.time() > WHEN:
        # get tomorrow time
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        # seconds until tomorrow (midnight)
        seconds = (tomorrow - now).total_seconds()
        # sleep until tomorrow and then the loop will start
        await asyncio.sleep(seconds)
    # infinite loop
    while True:
        # you can do now() or a specific timezone if that matters, but I'll leave it with utcnow
        now = datetime.utcnow()
        # 3:00 PM today (in UTC)
        target_time = datetime.combine(now.date(), WHEN)
        seconds_until_target = (target_time - now).total_seconds()
        # sleep until we hit the target time
        await asyncio.sleep(seconds_until_target)
        # call the helper function that sends the message
        await send_daily_images()
        # get tomorrow time
        tomorrow = datetime.combine(now.date() + timedelta(days=1), time(0))
        # seconds until tomorrow (midnight)
        seconds = (tomorrow - now).total_seconds()
        # sleep until tomorrow and then the loop will start a new iteration
        await asyncio.sleep(seconds)

# sends NASA astronomy picture of the day images on a daily basis at a set time
async def send_daily_images():
    # wait until set time
    await bot.wait_until_ready()

    # list of channels (from various different Discord servers) the bot will be posting the images in (you will need to supply your own channel IDs)
    channels_to_send = []
    # a loop that will go through each channel listed above and send images
    for channel_id in channels_to_send:
        # store channel id
        channel = bot.get_channel(channel_id)
        #await channel.send("NASA")

        # get image information from NASA API (need to get your own key)
        r = requests.get("")
        # set in json
        res = r.json()
        # check if API has copyright
        if "copyright" in res:
            # set title, url, and description
            em = discord.Embed(title=res['title'], url=res['hdurl'], description=res['explanation'], color=discord.Color.blue())
            # set author
            em.set_author(name=res['copyright'])
            # set image
            em.set_image(url=res['hdurl'])
        # if API does not have copyright
        else:
            # set title, url, and description
            em = discord.Embed(title=res['title'], url=res['hdurl'], description=res['explanation'], color=discord.Color.blue())
            # set author
            em.set_author(name='Public Domain')
            # set image
            em.set_image(url=res['hdurl'])

        # send embed to channel
        await channel.send(embed=em)


if __name__ == '__main__':
    # bot token (need to generate your own)
    TOKEN = ""
    bot.run(TOKEN)