import requests
import os
import discord
import random

keyCatGif = "YOUR KEY"
token = "YOUR TOKEN"
openaiKey = "YOUR KEY"


def getCatGif():
    r = requests.get(
        'https://api.thecatapi.com/v1/images/search?mime_types=gif', headers={'x-api-key': keyCatGif})
    if r.status_code == 200:
        gif = r.json()
        if type(gif) == list:
            gif = gif[0]['url']
            return gif
    else:
        print('Error:', r.status_code)


def getCatStory():
    thingList = ["story", "prose", "poem", "article", "sonnet"]
    catList = ["persian", "himalayan", "ragdoll",
               "main coon", "siamese", "birman", "siberian"]
    query = "Write a " + \
        random.choice(thingList) + " about a " + \
        random.choice(catList) + " cat, that is 50 words in length"

    h = {"Content-Type": "application/json",
         "Authorization": "Bearer " + openaiKey}
    d = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": query}],
        "temperature": 0.7
    }
    r = requests.post(
        url="https://api.openai.com/v1/chat/completions", headers=h, json=d)
    if r.status_code == 200:
        data = r.json()
        text = data["choices"][0]["message"]["content"]
        print(text)
        return text
    else:
        print('Error:', r.status_code)


class MyClient(discord.Client):
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(client))

    async def on_message(self, message):
        if message.author == client.user:
            print(f'Logged on as {self.user}!')

        if message.content.startswith('gif'):
            catGif = getCatGif()
            await message.channel.send(catGif)

        if message.content.startswith('story'):
            catStory = getCatStory()
            await message.channel.send(catStory)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(token)
