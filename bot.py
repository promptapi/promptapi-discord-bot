# bot.py
import os
import discord
import re
from bin_checker import get_bin
from scraper import Scraper

EXISTING_PROMPTAPI_TOKEN = os.environ.get('PROMPTAPI_TOKEN')
EXISTING_DISCORD_TOKEN = os.environ.get('DISCORD_TOKEN')

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
        os.environ['PROMPTAPI_TOKEN'] = EXISTING_PROMPTAPI_TOKEN
        bin_code_stripped = message.content.strip('!bincheck ')
        regex = r'\d{6}'
        bin_code = re.search(regex, bin_code_stripped)
        if bin_code:
            bin_information = get_bin(int(bin_code.group()))
            if bin_information.get('error', False):
                response = f'Error: {bin_information["error"]}'
                await message.channel.send(response)
            else:
                response = f'Bank name: {bin_information["bank_name"]} - Country: {bin_information["country"]} - URL: {bin_information["url"]} - Type: {bin_information["type"]} - Scheme: {bin_information["scheme"]} - BIN: {bin_information["bin"]}'
                await message.channel.send(response)
        else:
            await message.channel.send('Please enter the first six digit of a credit card. Ex: 424201')
            
    if message.content.startswith('!getusd'):
        os.environ['PROMPTAPI_TOKEN'] = EXISTING_PROMPTAPI_TOKEN
        bin_code_stripped = message.content.strip('!getusd ')
        url = 'https://kur.doviz.com/serbest-piyasa/amerikan-dolari'
        scraper = Scraper(url)
        fetch_params = dict(selector='div.col span.value')
        response = scraper.get(params=fetch_params)
        if response.get('error', None):
    	    await message.channel.send(response)
        else:
            usd = re.findall(r'[-+]?\d*\,\d+|\d+', f'{response["result"]["data"]}')
            if usd:
                await message.channel.send(f'Buying: {usd[0]} - Selling: {usd[1]} Source: {url}')
            else:
                await message.channel.send('Site can not scraped or can not find any element with the given css selector.')
                
@client.event
async def on_ready():
    print('Bot Name:')
    print(client.user.name)
    print(client.user.id)
    print('Bot started...')

client.run(EXISTING_DISCORD_TOKEN)
