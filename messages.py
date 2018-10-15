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