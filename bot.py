# bot.py
import os
import random
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN  = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    # diasble bot self reply
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)

@client.event
async def on_ready():
    print('Botname:')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)