# Packages
## Packages that are default to Python.
import datetime, traceback
from asyncio import sleep
## Packages that need to be installed through PyPi.
import aiohttp, discord
from colorama import Fore, Style, init
from discord.ext import commands
## Packages on this machine.
import config
from utils import get_prefix as gp, get_commands

# Initialize colorama
init()

async def get_prefix(bot, message):
    """Returns the bot's prefix.

    Args:
        bot (commands.AutoShardedBot): The bot object.
        message (discord.Message): Message object.

    Returns:
        str: The prefix the bot will accept.
    """
    return commands.when_mentioned_or(await gp(message))(bot, message)

intents = discord.Intents.default()
intents.members = True
bot = commands.AutoShardedBot(activity = discord.Game(f"with {config.prefix}help"), command_prefix = get_prefix, case_insensitive = True, intents = intents, status = discord.Status.online)

# bot.remove_command("help")
bot.load_extension("jishaku")

try:
    get_commands(bot, ".\cogs")
except:
    get_commands(bot, "./cogs")

async def owner(ctx):
    """Checks if a user is allowed to run the restart.

    Args:
        ctx (discord.py's context object): Context object.

    Returns:
        bool: Wether the user is one of the bot's owners.
    """

    return ctx.author.id in config.ownerids

@bot.event
async def on_command_error(ctx, error):
    """Whenever a command has an error the following function will be executed.

    Args:
        ctx (commands.Context): Discord's context object.
        error (Exception): The exception that was raised.
    """

    if isinstance(error, (commands.CommandNotFound, commands.BadArgument, commands.CheckFailure, commands.BadUnionArgument, commands.BotMissingPermissions, commands.TooManyArguments)):
        return
    else:
        try:
            error_type = type(error)
            error_trace = error.__traceback__
            error_list = traceback.format_exception(error_type, error, error_trace)
            error_text = "".join(error_list)

            await ctx.send(f"```\n{error_text}\n```".replace(config.token, "[R E D A C T E D"))
        finally:
            raise error

@bot.event
async def on_guild_join(guild):
    """When the bot joins a server send a webhook with detailed information as well as print out some basic information."""

    embed = discord.Embed(
        title = "Joined a server!",
        timestamp = datetime.datetime.utcnow(),
        color = 0x77DD77
    )
    embed.add_field(name = "Server Name", value = guild.name)
    embed.add_field(name = "Server Members", value = len(guild.members) - 1)
    embed.add_field(name = "Server ID", value = guild.id)
    embed.add_field(name = "Server Owner ID", value = guild.owner.id)
    embed.set_footer(text = f"I am now in {len(bot.guilds)} servers", icon_url = guild.icon_url)
    owner = bot.get_user(guild.owner_id)
    if owner:
        embed.add_field(name = "Server Owner", value = f"{owner}")
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(config.webhook, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Joined a server")
    print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}[JOINED-SERVER]{Fore.WHITE} Joined {Fore.YELLOW}{guild.name}{Fore.WHITE} with {Fore.YELLOW}{len(guild.members) - 1}{Fore.WHITE} members.")

@bot.event
async def on_guild_remove(guild):
    """When the bot leaves a server send a webhook with detailed information as well as print out some basic information."""

    embed = discord.Embed(
        title = "Left a server!",
        timestamp = datetime.datetime.utcnow(),
        color = 0xFF6961
    )
    embed.add_field(name = "Server Name", value = guild.name)
    embed.add_field(name = "Server Members", value = len(guild.members))
    embed.add_field(name = "Server ID", value = guild.id)
    embed.add_field(name = "Server Owner ID", value = guild.owner_id)
    embed.set_footer(text = f"I am now in {len(bot.guilds)} servers", icon_url = guild.icon_url)
    owner = bot.get_user(guild.owner_id)
    if owner:
        embed.add_field(name = "Server Owner", value = f"{owner}")
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(config.webhook, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Left a server")
    print(f"{Style.BRIGHT}{Fore.LIGHTRED_EX}[LEFT-SERVER]{Fore.WHITE} Left {Fore.YELLOW}{guild.name}{Fore.WHITE} with {Fore.YELLOW}{len(guild.members)}{Fore.WHITE} members.")

@bot.event
async def on_shard_ready(shard_id):
    """When a shard starts print out that the shard has started.

    Args:
        shard_id (int): The ID of the shard that has started. (Starts from 0).
    """

    print(f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[SHARD-STARTED]{Fore.WHITE} Shard {Fore.YELLOW}{shard_id}{Fore.WHITE} has started!")

@bot.event
async def on_shard_connect(shard_id):
    """When a shard connects log that it has connected.

    Args:
        shard_id (int): The ID of the shard that has connected. (Starts from 0).
    """

    embed = discord.Embed(
        color = 0x43B581
    )
    embed.set_author(name = f"Shard #{shard_id} has connected!", icon_url = "https://cdn.discordapp.com/emojis/736694890536370317.png?v=1")
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(config.shard_webhook, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Shard Connected")
    print(f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[SHARD-CONNECTED]{Fore.WHITE} Shard {Fore.YELLOW}{shard_id}{Fore.WHITE} has connected!")

@bot.event
async def on_shard_disconnect(shard_id):
    """When a shard disconnects log that it has disconnected.

    Args:
        shard_id (int): The ID of the shard that has disconnected. (Starts from 0).
    """

    embed = discord.Embed(
        color = 0xF04747
    )
    embed.set_author(name = f"Shard #{shard_id} has disconnected!", icon_url = "https://cdn.discordapp.com/emojis/736694890007625750.png?v=1")
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(config.shard_webhook, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Shard Disconnected")
    print(f"{Style.BRIGHT}{Fore.RED}[SHARD-DISCONNECTED]{Fore.WHITE} Shard {Fore.YELLOW}{shard_id}{Fore.WHITE} has disconnected!")

@bot.event
async def on_shard_resume(shard_id):
    """When a shard resumes log that it has resumed.

    Args:
        shard_id (int): The ID of the shard that has resumed. (Starts from 0).
    """

    embed = discord.Embed(
        color = 0x43B581
    )
    embed.set_author(name = f"Shard #{shard_id} has resumed!", icon_url = "https://cdn.discordapp.com/emojis/736694890536370317.png?v=1")
    async with aiohttp.ClientSession() as session:
        webhook = discord.Webhook.from_url(config.shard_webhook, adapter = discord.AsyncWebhookAdapter(session))
        await webhook.send(embed = embed, username = "Shard Resumed")
    print(f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[SHARD-RESUMED]{Fore.WHITE} Shard {Fore.YELLOW}{shard_id}{Fore.WHITE} has resumed!")

@bot.event
async def on_ready():
    """When the bot fully starts print out that the bot has started and set the status."""
    
    print(f"{Style.BRIGHT}{Fore.LIGHTBLUE_EX}[BOT-STARTED]{Fore.WHITE} I'm currently in {len(bot.guilds)} servers with {len(bot.users)} users!")
    while True:
        await bot.change_presence(status = discord.Status.online, activity = discord.Game(f"with {config.prefix}help | {len(bot.users)} Users"))
        await sleep(1800)

# Start the bot.
bot.run(config.token)