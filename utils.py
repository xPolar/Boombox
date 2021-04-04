# Packages.
## Packages default to Python.
import os, re
from bson.int64 import Int64
## Packages that have to be installed through the package manager.
import discord
from colorama import Fore, Style
from discord.ext import commands
## Packages on this machine.
import config

__version__ = "v1.0.0"

async def get_prefix(message : discord.Message) -> str:
    """Get the prefix for a server.

    Args:
        message (discord.Message): The message to check.

    Returns:
        str: The prefix that will work for the server.
    """

    if message.guild:
        document = await config.cluster.servers.prefixes.find_one({"_id": Int64(message.guild.id)})
        if document:
            return document["prefix"]
    return config.prefix

def get_commands(bot : commands.AutoShardedBot, directory : str) -> None:
    """Load all commands in a directory.

    Args:
        bot (commands.AutoShardedBot): Our bot.
        dir (str): The directory to load commands from.
    """

    for entry in os.scandir(directory):
        if entry.name == "__pycache__":
            continue
        if entry.is_dir() and entry.name:
            get_commands(bot, entry.path)
        else:
            try:
                bot.load_extension(entry.path.replace(".\\", "").replace("./", "").replace("\\", ".").replace("/", ".").replace(".py", ""))
            except Exception as e:
                print(e)
            else:
                print(f"{Style.BRIGHT}{Fore.GREEN}[SUCCESS]{Fore.WHITE} Loaded Cog: {entry.path}")