import asyncio
from bot_functions import seconds_to_minutes
async def output_error(client, message):
    msg = "Hello {0.author.mention}, I didn't understand that.".format(message)
    msg = msg.format(message)
    msg = await message.channel.send(msg)
    await asyncio.sleep(3) 
    await msg.delete()
    
async def score_error(client, message):
    msg = 'Hello {0.author.mention}, something went wrong and we could not record your score.'
    msg = msg.format(message)
    msg = await message.channel.send(msg)
    await asyncio.sleep(3) 
    await msg.delete()
    
async def success_message(client, message, time, isArchive, streak):
    if time > 60:
        time_string = seconds_to_minutes(time)
    else:
        time_string = str(time)+' seconds'
    if isArchive or streak <= 1:
        msg = 'Hello {0.author.mention}, we have logged your crossword score of ' + time_string + '.'
    else:
        msg = 'Hello {0.author.mention}, we have logged your crossword score of ' + time_string + ', your current streak is '+str(streak)+'!'
    msg = msg.format(message)
    msg = await message.channel.send(msg)

async def wordle_success_message(client, message, score, streak):
    if streak <= 1:
        msg = 'Hello {0.author.mention}, we have logged your Wordle score of ' + score + ' guesses.'
    else:
        msg = 'Hello {0.author.mention}, we have logged your Wordle score of ' + score + ' guesses, your current streak is ' + str(streak) + '!'
    msg = msg.format(message)
    msg = await message.channel.send(msg)

async def streak_message(client, message, streak):
    msg = '{0.author.mention}, your current streak is '+str(streak)+'!'
    msg = msg.format(message)
    msg = await message.channel.send(msg)

async def help_message(client, message):
    msg = """```!crossword, !c x:xx - Saves your time for today\'s crossword.
!archive, !a x:xx   - Saves your time for today\'s archive crossword.
!both, !b c:cc a:aa - Saves your time for both crosswords at once.
!wordle, !w x       - Saves your score for today\'s Wordle.
!streak             - Displays your current streak of completing the regular crossword on consecutive days.
!where, !nyt        - Provides a link to the New York Times Crosswords. Archive is in bottom right corner.
!scores             - Creates a table with the crossword scores of the day.
!wscores            - Creates a table with the wordle scores of the day.
!joel               - Displays the current crossword day.
!topscores          - Displays how many times each person (not nick) had the #1 score for the day.
!pb                 - Displays your personal best score.
!averages           - Displays average score and total number of crosswords.
```"""
    msg = msg.format(message)
    msg = await message.channel.send(msg)

async def rules_message(client, message):
    msg = """```nick can use check
bohan can record 10s scores
```"""
    msg = msg.format(message)
    msg = await message.channel.send(msg)

async def where_message(client, message):
    msg = 'https://www.nytimes.com/crosswords https://www.nytimes.com/games/wordle/index.html'
    msg = msg.format(message)
    msg = await message.channel.send(msg)

async def no_scores(client, message):
    msg = 'Sorry, there are no scores yet today!'
    msg = msg.format(message)
    msg = await message.channel.send(msg)
    
async def custom_message(client, message, custom_string):
    msg = custom_string
    msg = msg.format(message)
    msg = await message.channel.send(msg)

async def time_message(client, message, date):
    msg = date.strftime("%B %-d, %Y")
    msg = msg.format(message)
    msg = await message.channel.send(msg)
