# Packages.
## Packages default to Python.
from os import scandir
## Packages that have to be installed through the package manager.
from discord import Message
from colorama import Fore, Style
from discord.ext import commands
## Packages on this machine.
from config import cluster, prefix

__version__ = "v1.0.0"

async def get_prefix(message : Message) -> str:
    """Get the prefix for a server.

    Args:
        message (discord.Message): The message to check.

    Returns:
        str: The prefix that will work for the server.
    """

    if message.guild:
        prefix_document = await cluster.servers.prefixes.find_one({"_id": message.guild.id})
        if prefix_document:
            return prefix_document["prefix"]
    return prefix

def get_commands(bot : commands.AutoShardedBot, directory : str) -> None:
    """Load all commands in a directory.

    Args:
        bot (commands.AutoShardedBot): Our bot.
        directory (str): The directory to load commands from.
    """

    # For every file / sub-directory in the provided directory continue
    # if it's cache otherwise attempt to load extension or use recursion.
    for entry in scandir(directory):
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
