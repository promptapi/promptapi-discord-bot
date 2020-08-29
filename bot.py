# bot.py
import os
import discord
from bin_checker import get_bin

MY_PROMPTAPI_TOKEN = os.environ.get('PROMPTAPI_TOKEN')
MY_DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_message(message):
    # diasble bot self reply
    if message.author == client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await message.channel.send(msg)
        
    if message.content.startswith('!bincheck'):
        os.environ['PROMPTAPI_TOKEN'] = MY_PROMPTAPI_TOKEN
        bin_code_split = message.content.split('!bincheck')
        bin_code = bin_code_split[1]
        bin_information = get_bin(int(bin_code))
        if bin_information.get('error', False):
            response = f'Error: {bin_information["error"]}'
            await message.channel.send(response)
        else:
            response = f'Bank name: {bin_information["bank_name"]} - Country: {bin_information["country"]} - URL: {bin_information["url"]} - Type: {bin_information["type"]} - Scheme: {bin_information["scheme"]} - BIN: {bin_information["bin"]}'
            await message.channel.send(response)

@client.event
async def on_ready():
    print('Bot Name:')
    print(client.user.name)
    print(client.user.id)
    print('Bot started...')

client.run(MY_DISCORD_TOKEN)
