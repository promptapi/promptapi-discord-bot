#promptapi.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()
PROMPT_KEY = os.getenv('PROMPTAPI_KEY')

def bad_words(message):
    #This bot using Prompt API - Bad Words API
    #Visit promptapi.com to create a free account
    url = "https://api.promptapi.com/bad_words?censor_character=*"
    payload = message.encode("utf-8")
    headers = {"apikey": PROMPT_KEY}
    response = requests.request("POST", url, headers=headers, data = payload)
    data = response.json()
        
    #check if json data returning an error or message.
    #for ex. api key error or bad formatted text
    if 'message' in data:
        return data['message']
    #check if data not contains any bad word.
    elif data['bad_words_total'] == 0:
        return "Perfect! No bad words."
    #check if data containts a bad word.
    elif data['bad_words_total'] > 0:
        return f'Warning: {message} is a bad word. Original: {data["bad_words_list"][0]["word"]}'.format(message)
    #check if it returns a generic error.
    else:
    	return "Unknown error"