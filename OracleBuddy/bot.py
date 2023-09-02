from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("SECRET_KEY") 
CHANNEL_ID = 1146839044328792104
MAX_SESSION_TIME_MINUTES = 30


@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
session = Session()


@bot.event
async def on_ready():
    print("Hey! Oracle bot is ready!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Hey! Oracle bot is ready!")


@tasks.loop(minutes=MAX_SESSION_TIME_MINUTES, count=2)
async def break_reminder():
    if break_reminder.current_loop == 0:
        return
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send(f"**Take a break!** You've been studying for {MAX_SESSION_TIME_MINUTES} minutes. ")


# Start Session
@bot.command()
async def start(ctx):
    if session.is_active:
        await ctx.send("A session is already active!")
        return

    session.is_active = True
    session .start_time = ctx.message.created_at.timestamp()
    human_readable_time = ctx.message.created_at.strftime('%H:%M:%S')
    break_reminder.start()
    await ctx.send(f"New session started at {human_readable_time}")


# End Session
@bot.command()
async def stop(ctx):
    if not session.is_active:
        await ctx.stop("No session is active")
        return

    session.is_active = False
    stop_time = ctx.message.created_at.timestamp()
    duration = stop_time - session.start_time
    human_readable_duration = str(datetime.timedelta(seconds=duration))
    break_reminder.stop()
    await ctx.send(f"Session ended after {human_readable_duration}")


# Addition
@bot.command()
async def add(ctx, *arr):
    result = 0
    for i in arr:
        result += int(i)
    await ctx.send(f"{result}")


# Subtraction
@bot.command()
async def subtract(ctx, *arr):
    result = int(arr[0])  # Initialize result with the first element
    for i in arr[1:]:     # Loop through the rest of the elements
        result -= int(i)
    await ctx.send(f"Result: {result}")


bot.run(BOT_TOKEN)
