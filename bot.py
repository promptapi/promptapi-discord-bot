# bot.py
import os
import discord
import promptapi
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
        
    if message.content.startswith('!badwords'):
        #split the !badwords part
        bad_word_split = message.content.split('!badwords')
        bad_word = bad_word_split[1]
        
        prompt_response = promptapi.bad_words(bad_word)
        await message.channel.send(prompt_response)

@client.event
async def on_ready():
    print('Botname:')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)