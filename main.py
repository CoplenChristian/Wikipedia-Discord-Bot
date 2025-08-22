import discord
from discord.ext import commands
import random
import wikipediaapi
import os
import requests
import json

# Create a Wikipedia API client
wiki_wiki = wikipediaapi.Wikipedia('en')

# Replace 'YOUR_DISCORD_BOT_TOKEN' with your own bot token
TOKEN = ''

# File to store the sent titles
SENT_TITLES_FILE = 'sent_titles.txt'

# Define the required intents
intents = discord.Intents.default()
intents.messages = True

# Create a bot instance
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    # Check if the sent titles file exists, and create it if not
    if not os.path.exists(SENT_TITLES_FILE):
        with open(SENT_TITLES_FILE, 'w') as file:
            pass


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

    # Check if the sent titles file exists, and create it if not
    if not os.path.exists(SENT_TITLES_FILE):
        with open(SENT_TITLES_FILE, 'w') as file:
            pass


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check if the message is in the "masterdebaters" channel
    if message.channel.name == 'masterdebaters':
        if message.content == '!wiki':
            await message.channel.send("Looking for american event or figure that fits criteria, this may take a while")
            # Read the sent titles from the file
            with open(SENT_TITLES_FILE, 'r') as file:
                sent_titles = file.read().splitlines()

            # Get a random Wikipedia page (filtered for American historical events and figures)
            random_page = None
            while random_page is None or random_page['title'] in sent_titles or not is_american_historical_page(random_page):
                random_page = get_random_wikipedia_page()
                print(random_page)

            # Retrieve the page title and description
            title = random_page['title']
            description = random_page['description']

            # Store the sent title in the file
            with open(SENT_TITLES_FILE, 'a') as file:
                file.write(title + '\n')

            # Send the title and description in the channel
            response = f'**Title:** {title}\n\n{description}'
            await message.channel.send(response)

        if message.content == "!purge":
            await message.channel.purge()

    await bot.process_commands(message)


def get_random_wikipedia_page():
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'query',
        'list': 'random',
        'format': 'json',
        'rnnamespace': '0',
        'rnlimit': '1'
    }

    response = requests.get(url, params=params)
    data = response.json()
    random_page = data['query']['random'][0]

    page_title = random_page['title']
    page = wiki_wiki.page(page_title)

    description = page.summary

    return {'title': page_title, 'description': description}


def is_american_historical_page(page):
    title = page['title'].lower()
    description = page['description'].lower()

    # Check if the page falls under an American historical category
    if 'american history' in page.get('categories', []):
        return True

    # Check if the page is related to American historical events or figures
    american_keywords = ['united states', 'american', 'usa']
    if any(keyword in title or keyword in description for keyword in american_keywords):
        return True

    return False



bot.run(TOKEN)
