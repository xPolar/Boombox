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

# FIXME: Code is stolen from discord.py's master branch (1.7 currently), local code is on discord.py 1.6.0, once discord.py 1.7.0 is released switch to discord.utils.remove_markdown.

_MARKDOWN_ESCAPE_COMMON = r'^>(?:>>)?\s|\[.+\]\(.+\)'
_MARKDOWN_STOCK_REGEX = r'(?P<markdown>[_\\~|\*`]|%s)' % _MARKDOWN_ESCAPE_COMMON
_URL_REGEX = r'(?P<url><[^: >]+:\/[^ >]+>|(?:https?|steam):\/\/[^\s<]+[^<.,:;\"\'\]\s])'

def remove_markdown(text, *, ignore_links=True):
    """A helper function that removes markdown characters.
    .. versionadded:: 1.7
    
    .. note::
            This function is not markdown aware and may remove meaning from the original text. For example,
            if the input contains ``10 * 5`` then it will be converted into ``10  5``.
    
    Parameters
    -----------
    text: :class:`str`
        The text to remove markdown from.
    ignore_links: :class:`bool`
        Whether to leave links alone when removing markdown. For example,
        if a URL in the text contains characters such as ``_`` then it will
        be left alone. Defaults to ``True``.
    Returns
    --------
    :class:`str`
        The text with the markdown special characters removed.
    """

    def replacement(match):
        groupdict = match.groupdict()
        return groupdict.get('url', '')

    regex = _MARKDOWN_STOCK_REGEX
    if ignore_links:
        regex = '(?:%s|%s)' % (_URL_REGEX, regex)
    return re.sub(regex, replacement, text, 0, re.MULTILINE)