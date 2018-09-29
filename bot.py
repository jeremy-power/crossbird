# Work with Python 3.6
import discord
from bot_functions import *
from db import *

with open('token.txt') as f:
    read_data = f.read()
f.closed
TOKEN = read_data

client = discord.Client()


def enter_score(discord_id, discord_name, score, date, isArchive):
    #find the user by their discord ID
    user = select_user_by_id(discord_id)
    #if user doesn't exist yet, create one
    if len(user) == 0:
        create_user(discord_id, discord_name)
    #otherwise if their name has changed, update it
    elif user[0]['DiscordName'] != discord_name:
        update_name(discord_id, discord_name)
    #make sure user exists now
    user = select_user_by_id(discord_id)
    if len(user) != 0:
        #if it does, add the score
        create_score(discord_id, score, date, isArchive)
        return 1
    else:
        return 0

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself

    if message.author == client.user:
        return

    if message.content.startswith('!crossword'):
        time = str(message.content).split("!crossword ",1)
        time = time[1]
        #try:
        time = time_to_number(str(time))
        score_entered = enter_score(message.author.id, message.author.name,time,date_scrape(), False)
        if score_entered == 1:
            msg = 'Hello {0.author.mention}, we have logged your score of '+str(time)+' seconds.'
            msg = msg.format(message)
            await client.send_message(message.channel, msg)
        else:
            msg = 'Hello {0.author.mention}, we have already logged a score for you, today. Please play again, tomorrow.'
            msg = msg.format(message)
            await client.send_message(message.channel, msg)
        #except:
        #    msg = "Hello {0.author.mention}, I didn't understand that.".format(message)
        #    await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)