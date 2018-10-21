import asyncio
async def output_error(client, message):
    msg = "Hello {0.author.mention}, I didn't understand that.".format(message)
    msg = msg.format(message)
    msg = await client.send_message(message.channel, msg)
    await asyncio.sleep(3) 
    await client.delete_message(msg)
    
async def score_error(client, message):
    msg = 'Hello {0.author.mention}, something went wrong and we could not record your score.'
    msg = msg.format(message)
    msg = await client.send_message(message.channel, msg)
    await asyncio.sleep(3) 
    await client.delete_message(msg)
    
async def success_message(client, message, time):
    msg = 'Hello {0.author.mention}, we have logged your score of '+str(time)+' seconds.'
    msg = msg.format(message)
    await client.send_message(message.channel, msg)

async def streak_message(client, message, streak):
    msg = '{0.author.mention}, your current streak is '+str(streak)+'!'
    msg = msg.format(message)
    await client.send_message(message.channel, msg)

async def help_message(client, message):
    msg = """```!crossword, !c x:xx - Saves your time for today\'s crossword.
!archive, !a x:xx   - Saves your time for today\'s archive crossword.
!both, !b c:cc a:aa - Saves your time for both crosswords at once.
!streak             - Displays your current streak of completing the regular crossword on consecutive days.
!where, !nyt        - Provides a link to the New York Times Crosswords. Archive is in bottom right corner.
!scores             - Creates a table with the scores of the day.
```"""
    msg = msg.format(message)
    await client.send_message(message.channel, msg)

async def where_message(client, message):
    msg = 'https://www.nytimes.com/crosswords'
    msg = msg.format(message)
    await client.send_message(message.channel, msg)

async def no_scores(client, message):
    msg = 'Sorry, there are no scores yet today!'
    msg = msg.format(message)
    await client.send_message(message.channel, msg)
    
async def score_message(client, message, score_string):
    msg = score_string
    msg = msg.format(message)
    await client.send_message(message.channel, msg)