# Work with Python 3.6
import discord
from bot_functions import *

with open('token.txt') as f:
    read_data = f.read()
f.closed
TOKEN = read_data

client = discord.Client()

def create_user(userid):
    ADD_USER_TO_DATABASE
    return

def enter_score(userid, score, date):
    user_found = 0
    for i in DATABASE_OF_USERS:
        if userid == 1:
            user_found = 1
    if user_found = 0:
        ADD_USER_TO_DATABASE
    else:
        if NO_ENTRY_FOR_GIVEN_DATE_YET:
            ADD_ENTRY_WITH_ID_SCORE_DATE
            return(1)
        else:
            return(0)

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
            score_entered = enter_score(message.author.id,time,date_scrape())
            if score_entered == 1:
                msg = 'Hello {0.author.mention}, we have logged your score of '+str(time)+' seconds.'
                msg = msg.format(message)
                await client.send_message(message.channel, msg)
            else:
                msg = 'Hello {0.author.mention}, we have already logged a score for you, today. Please play again, tomorrow.'
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