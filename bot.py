# Work with Python 3.6
import discord
from bot_functions import *

with open('token.txt') as f:
    read_data = f.read()
f.closed
TOKEN = read_data

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    if message.content.startswith('!crossword'):
        time = str(message.content).split("!crossword ",1)
        time = time[1]
        try:
            time = time_to_number(str(time))
            msg = 'Hello {0.author.mention}, we have logged your score of '+str(time)+' seconds.'
            msg = msg.format(message)
            await client.send_message(message.channel, msg)
        except:
            msg = "Hello {0.author.mention}, I didn't understand that.".format(message)
            await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)