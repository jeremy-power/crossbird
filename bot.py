__author__ = "Jeremy Power and Logan Groves"

# Work with Python 3.6
import logging
from bot_functions import *
from db import *
from messages import *
from commands import *
from timer import *
import discord
TOKEN = process.env.BOT_TOKEN
client = discord.Client()
command_dict = define_commands()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    if message.author == client.user:
        return
    # breaks the user's message into parts
    command = message.content.split(" ")[0]
    command_params = message.content.split(" ")[1:]

    if(command.startswith('!')):
        try:
            await command_dict[command](command_params, message, client)
        except KeyError as e:
            pass
        except Exception as e:
            await output_error(client, message)
            logging.warning(e)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    # update_joel_date(date_scrape())
    # rt = RepeatedTimer(10, check_joel_day)
    # rt.start()
client.run(TOKEN)