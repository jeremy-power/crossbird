__author__ = "Jeremy Power and Logan Groves"

# Work with Python 3.6
import discord
import logging
from bot_functions import *
from db import *
from messages import *
from commands import *
from timer import *
TOKEN = get_token()
intents = discord.Intents.default()
intents.message_content = True

class aclient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.synced = False

    async def on_ready(self):
        await self.wait_until_ready()
        if not self.synced:
            await tree.sync()
            self.synced = True
        print(f"We have logged in as {self.user}.")

client = aclient()
tree = discord.app_commands.CommandTree(client)
command_dict = define_commands(tree, discord.Interaction)

client.run(TOKEN)