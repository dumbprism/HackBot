import os
import discord
from dotenv import load_dotenv
import requests

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# Define intents
intents = discord.Intents.default()

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    print("Message received:", message.content)  # Debug print statement

    if message.author == client.user:
        return
    
    if message.content.startswith('/hello') or message.content.startswith('/start'):
        await message.channel.send('Hello how can I help you today!')

    if message.content.startswith('/help'):
        await message.channel.send('These are the following commands that you can use:\n'
                                   '1. /on -- to fetch online hackathons\n'
                                   '2. /off -- to fetch online hackathons\n'
                                   '3. /loc -- Enter the city that you are present in\n'
                                   '4. /start (or) /hello -- starting me')
        
    #ONline hackathon fetching 

    if message.content.startswith('/on'):
        response = requests.get("https://devpost.com/api/hackathons/featured_hackathons")
        hackathons = response.json().get("hackathons", [])
        

        if not hackathons:
            await message.channel.send("No online hackathons found.")
        else:
            for hackathon in hackathons:
                title = hackathon.get("title", "No title available")
                url = hackathon.get("url", "No URL available")
                submission_period_dates = hackathon.get("submission_period_dates", "No submission period dates available")
                await message.channel.send(f'Title: {title}\nURL: {url}\nSubmission Period Dates: {submission_period_dates}')


    if message.content.startswith('/off'):
        response_off = requests.get("https://devpost.com/api/hackathons/")
        hackathons_off = response_off.json().get("hackathons", [])
        

        if not hackathons_off:
            await message.channel.send("No offline hackathons found.")
        else:
            for hackathon in hackathons_off:
                title = hackathon.get("title", "No title available")
                url = hackathon.get("url", "No URL available")
                submission_period_dates = hackathon.get("submission_period_dates", "No submission period dates available")
                await message.channel.send(f'Title: {title}\nURL: {url}\nSubmission Period Dates: {submission_period_dates}')
        
        if message.content.startswith('/loc'):
            await message.channel.send('fetching ')



   

client.run(TOKEN)
