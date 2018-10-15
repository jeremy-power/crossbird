import os
import logging
from db import *
from messages import *
from bot_functions import *

def define_commands():
    command_dict = {'!crossword' : enter_crossword_command,
                    '!c' : enter_crossword_command,
                    '!archive' : enter_archive_command,
                    '!a' : enter_archive_command,
                    '!both' : enter_both_command,
                    '!b' : enter_both_command,
                    '!streak' : display_streak,
                    '!how' : display_help,
                    '!where' : display_link,
                    '!nyt' : display_link}
    return command_dict

async def display_link(param_array, message, client):
    await where_message(client, message)

async def display_help(param_array, message, client):
    await help_message(client, message)

async def display_streak(param_array, message, client):
    discord_id = message.author.id
    streak = get_streak(discord_id)
    await streak_message(client, message, streak)


async def enter_crossword_command(param_array, message, client):
    time = param_array[0]
    await create_score_from_message(time, message, client, False)
    #implement validation on time here

async def enter_archive_command(param_array, message, client):
    time = param_array[0]
    #implement validation on time here
    await create_score_from_message(time, message, client, True)

async def enter_both_command(param_array, message, client):
    try:
        time = param_array[0]
        await create_score_from_message(time, message, client, False)
        time = param_array[1]
        await create_score_from_message(time, message, client, True)
    except Exception as e:
        logging.warning(e)
        await output_error(client, message)