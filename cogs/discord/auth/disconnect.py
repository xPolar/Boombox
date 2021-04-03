# Packages.
## Packages default to Python.
from bson.int64 import Int64
from typing import Union
## Packages that have to be installed through the package manager.
import discord
from discord.ext import commands
## Packages on this machine.
import config

class Authorization(commands.Cog):

    def __init__(self, bot : commands.AutoShardedBot) -> None:
        self.bot = bot

    @commands.command()
    async def disconnect(self, ctx : commands.Context, channel : Union[discord.VoiceChannel, str] = None, bot : discord.User = None, twitch : str = None) -> None:
        """Disconnect a Discord voice channel with a twitch chat.

        Args:
            ctx (commands.Context): Discord's context object.
            channel (Union[discord.VoiceChannel, str]): The voice channel we want to connect.
            bot (discord.User): The bot we want to connect with.
            twitch (str): The twitch user to connect to.
        """

        if not channel:
            embed = discord.Embed(
                title = "Empty Argument",
                description = "Please provide a voice channel to disconnect from!",
                color = config.errorcolor
            )
        elif not bot:
            embed = discord.Embed(
                title = "Empty Argument",
                description = "Please provide a bot to disconnect from!",
                color = config.errorcolor
            )
        elif not twitch:
            embed = discord.Embed(
                title = "Empty Argument",
                description = "Please provide a twitch channel to disconnect from!",
                color = config.errorcolor
            )
        else:
            if not bot.bot or bot.id not in config.supported_bots:
                embed = discord.Embed(
                    title = "Empty Argument",
                    description = "Please provide a valid music bot that we support! Find a list of supported music bots [**here**](TODO gitbook to supported music bots).",
                    color = config.errorcolor
                )
            else:
                document = await config.cluster.users.oauth.find_one({"_id": ctx.author.id})
                if not document:
                    embed = discord.Embed(
                        title = "Not Authorized",
                        description = "Please authorize with Boombox by clicking [**here**](TODO auth link)",
                        color = config.errorcolor
                    )
                else:
                    twitch = twitch.split("/")[-1]
                    if twitch not in [channel["name"] for channel in document["connections"] if channel["type"] == "twitch"] and twitch not in [channel["id"] for channel in document["connections"] if channel["type"] == "twitch"]:
                        embed = discord.Embed(
                            title = "Not Connected",
                            description = f"If you are the owner of {twitch} please connect it to your Discord account! If you need help with this please feel free to join our [**support server**](TODO Support server invite link)!",
                            color = config.errorcolor
                        )
                    else:
                        embed = discord.Embed(
                            title = "Bot Disconnected",
                            description = f"Whenever **{bot.mention}** plays a new song in **{channel}** I will no longer post a message into **{twitch}**!",
                            color = config.maincolor
                        )
                        await config.cluster.connected.documents.update_one({"channel": Int64(channel.id), "bot": Int64(bot.id)}, {"$pull": {"twitch": twitch}}, upsert = True)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Authorization(bot))