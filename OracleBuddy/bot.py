from discord.ext import commands, tasks
import discord
from dataclasses import dataclass
import datetime
import os
from dotenv import load_dotenv
import random
from discord.ext import commands
from discord import app_commands
import aiohttp
load_dotenv()

BOT_TOKEN = os.getenv("SECRET_KEY")
API_KEY = os.getenv("API_KEY")
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

# Embedded Message


@bot.command()
async def embed(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author

    name = member.display_name
    pfp = member.display_avatar

    embed = discord.Embed(title="This is my embed",
                          description="It's a very cool embed", colour=discord.Colour.random())
    embed.set_author(name=f"{name}", url="", icon_url="")
    embed.set_thumbnail(url=f"{pfp}")
    embed.add_field(name="This is 1 field", value="This field is just a value")
    embed.add_field(name="This is 2 field",
                    value="This field is inline true", inline=True)
    embed.add_field(name="This is 3 field",
                    value="This field is inline false", inline=False)
    embed.set_footer(text=f"{name} Made this embed")

    await ctx.send(embed=embed)

# Define and create your abot instance


@bot.command(aliases=['8ball', '8b'])
async def eightball(ctx, *, question):
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]

    await ctx.send(f':8ball: Question: {question}\n:8ball: Answer: {random.choice (responses)} ')


@bot.event
async def on_member_join(member):
    # Define a list of random emojis
    emojis = ["🎉", "👋", "🌟", "🎊", "🥳", "👏"]

    # Randomly select an emoji from the list
    random_emoji = random.choice(emojis)

    # Create a customized welcome message with the selected emoji
    welcome_message = f"{random_emoji} Welcome to the server, {member.mention} {random_emoji}"

    # Create an embed for the welcome message
    welcome_embed = discord.Embed(
        title="New Member Alert!",
        description=welcome_message,
        color=discord.Color.blue()
    )

    # Send the welcome message to the designated channel
    # Replace with your channel ID
    channel = bot.get_channel(1146839044328792104)
    await channel.send(embed=welcome_embed)


@bot.command()
async def weather(ctx: commands.Context, *, city):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": API_KEY,
        "q": city
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as res:
            data = await res.json()

            location = data["location"]["name"]
            temp_c = data["current"]["temp_c"]
            temp_f = data["current"]["temp_f"]
            humidity = data["current"]["humidity"]
            wind_kph = data["current"]["wind_kph"]
            wind_mph = data["current"]["wind_mph"]
            condition = data["current"]["condition"]["text"]
            image_url = "http:" + data["current"]["condition"]["icon"]

            embed = discord.Embed(
                title=f"Weather for {location}", description=f"The condition in `{location}` is `{condition}` ")
            embed.add_field(name="Temperature",
                            value=f"C: `{temp_c}` | F:`{temp_f}`")
            embed.add_field(name="Humidity", value=f"`{humidity}`")
            embed.add_field(name="Wind Speed",
                            value=f"KPH: `{wind_kph}` | MPH:`{wind_mph}`")

            embed.set_thumbnail(url=image_url)

            await ctx.send(embed=embed)


# Run both bots
bot.run(BOT_TOKEN)
