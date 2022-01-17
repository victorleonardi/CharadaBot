from distutils import command
import discord
import os
from discord.ext import commands

token_bot = os.environ['token']

client = commands.Bot(command_prefix="!")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run(token_bot)
