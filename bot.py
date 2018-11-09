__author__ = "Jeremy Power and Logan Groves"

# Work with Python 3.6
import discord
import logging
from bot_functions import *
from db import *
from messages import *
from commands import *
TOKEN = get_token()
client = discord.Client()
command_dict = define_commands()
from threading import Timer

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
    update_joel_date(date_scrape())
    t = Timer(60.0, check_joel_day)
    t.start()
client.run(TOKEN)