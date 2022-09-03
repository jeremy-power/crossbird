import os
import logging
from db import *
from messages import *
from bot_functions import *

def define_commands(tree, interaction):

    # enter wordle command
    @tree.command(name = "wordle", description = "Submit your wordle score for the day!")
    async def wordle(interaction: interaction, score: int):
        await create_wordle_score_from_message(score, interaction)
        #implement validation on time here
    
# async def start_trivia(param_array, message, client):
#     question_amount = param_array[0]
#     await play_trivia(question_amount, message, client)

async def display_averages(param_array, message, client):
    average_string = await build_crossword_averages(client, message)
    await custom_message(client, message, average_string)

async def display_wordle_averages(param_array, message, client):
    average_string = await build_wordle_averages(client, message)
    await custom_message(client, message, average_string)

async def display_top_scores(param_array, message, client):
    top_scores_string = await build_top_scores_string(client, message)
    await custom_message(client, message, top_scores_string)

async def display_personal_best(param_array, message, client):
    pb_string = await build_personal_best_string(client, message)
    await custom_message(client, message, pb_string)

async def display_time(param_array, message, client):
    await time_message(client, message, date_scrape())
    

async def display_scores_today(param_array, message, client):
    score_string = await build_score_string(client, message, date_scrape())
    await custom_message(client, message, score_string)

async def display_wordles_today(param_array, message, client):
    score_string = await build_wordle_string(client, message, get_wordle_date())
    await custom_message(client, message, score_string)

async def display_streaks(param_array, message, client):
    streak_string = await build_streak_string(message,client)
    await custom_message(client, message, streak_string)

async def display_scores_yesterday(param_array, message, client):
    score_string = await build_score_string(client, message, date_scrape() - datetime.timedelta(days=1))
    await custom_message(client, message, score_string)

async def display_link(param_array, message, client):
    await where_message(client, message)

async def display_help(param_array, message, client):
    await help_message(client, message)

async def display_rules(param_array, message, client):
    await rules_message(client, message)

async def display_streak(param_array, message, client):
    discord_id = message.author.id
    streak = get_streak(discord_id)
    await streak_message(client, message, streak)


# async def enter_crossword_command(param_array, message, client):
#     time = param_array[0]
#     await create_score_from_message(time, message, client, False)
#     #implement validation on time here

# async def enter_archive_command(param_array, message, client):
#     time = param_array[0]
#     #implement validation on time here
#     await create_score_from_message(time, message, client, True)

# async def enter_both_command(param_array, message, client):
#     try:
#         time = param_array[0]
#         await create_score_from_message(time, message, client, False)
#         time = param_array[1]
#         await create_score_from_message(time, message, client, True)
#     except Exception as e:
#         logging.warning(e)
#         await output_error(client, message)

# async def create_score_from_message(time, message, client, isArchive):
#     try:
#         time = time_to_number(str(time)) #Calls a function to convert "hh:mm:ss" to integer seconds
#         score_entered = enter_score(message.author.id, message.author.display_name,time,date_scrape(), isArchive) #Attempts to actual enter the score into the database
#         if score_entered == 1:
#             streak = get_streak(message.author.id)
#             await success_message(client, message, time, isArchive, streak)
#         else:
#             await score_error(client, message)
#     except Exception as e:
#         logging.warning(e)
#         await output_error(client, message)


async def create_wordle_score_from_message(score, interaction):
    try:
        score_entered = enter_wordle_score(interaction.user.id, interaction.user.display_name, score, get_wordle_date())
        if score_entered == 1:
            streak = get_wordle_streak(interaction.user.id)
            await wordle_success_message(interaction, score, streak)
        else:
            await score_error(interaction)
    except Exception as e:
        logging.warning(e)
        await output_error(interaction)