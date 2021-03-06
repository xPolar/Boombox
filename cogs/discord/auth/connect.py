# Packages.
## Packages default to Python.
from bson.int64 import Int64
from typing import Union
## Packages that have to be installed through the package manager.
from discord import Embed, User, VoiceChannel
from discord.ext import commands
## Packages on this machine.
from config import cluster, errorcolor, maincolor, supported_bots 

class Authorization(commands.Cog):

    def __init__(self, bot : commands.AutoShardedBot) -> None:
        self.bot = bot

    @commands.command()
    async def connect(self, ctx : commands.Context, channel : Union[VoiceChannel, str] = None, bot : User = None, twitch : str = None) -> None:
        """Connect a Discord voice channel with a twitch chat.

        Args:
            ctx (commands.Context): Discord's context object.
            channel (Union[VoiceChannel, str]): The voice channel we want to connect.
            bot (User): The bot we want to connect with.
            twitch (str): The twitch user to connect to.
        """

        if not channel:
            embed = Embed(
                title = "Empty Argument",
                description = "Please provide a voice channel to connect to!",
                color = errorcolor
            )
        elif not bot:
            embed = Embed(
                title = "Empty Argument",
                description = "Please provide a bot to connect with!",
                color = errorcolor
            )
        elif not twitch:
            embed = Embed(
                title = "Empty Argument",
                description = "Please provide a twitch channel to connect to!",
                color = errorcolor
            )
        elif not bot.bot or bot.id not in supported_bots:
            embed = Embed(
                title = "Empty Argument",
                description = "Please provide a valid music bot that we support! Find a list of supported music bots [**here**](TODO gitbook to supported music bots).",
                color = errorcolor
            )
        else:
            document = await cluster.users.oauth.find_one({"_id": ctx.author.id})
            if not document:
                embed = Embed(
                    title = "Not Authorized",
                    description = "Please authorize with Boombox by clicking [**here**](https://discord.com/api/oauth2/authorize?client_id=825880443273478164&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Flogin%2F&response_type=code&scope=connections%20identify)",
                    color = errorcolor
                )
            else:
                twitch = twitch.split("/")[-1]
                if twitch not in [channel["name"] for channel in document["connections"] if channel["type"] == "twitch"] and twitch not in [channel["id"] for channel in document["connections"] if channel["type"] == "twitch"]:
                    embed = Embed(
                        title = "Not Connected",
                        description = f"If you are the owner of {twitch} please connect it to your Discord account! If you need help with this please feel free to join our [**support server**](https://discord.gg/DeDNDYhtwb)!",
                        color = errorcolor
                    )
                else:
                    embed = Embed(
                        title = "Bot Connected",
                        description = f"Whenever **{bot.mention}** plays a new song in **{channel}** I will now post a message into **{twitch}**!",
                        color = maincolor
                    )
                    await cluster.connected.documents.update_one({"channel": Int64(channel.id), "bot": Int64(bot.id)}, {"$addToSet": {"twitch": twitch}}, upsert = True)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Authorization(bot))
