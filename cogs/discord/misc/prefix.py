# Packages.
## Packages default to Python.
from bson.int64 import Int64
## Packages that have to be installed through the package manager.
from discord import Embed, Message
from discord.ext import commands
## Packages on this machine.
from config import cluster, maincolor, errorcolor
from utils import get_prefix

class Miscellaneous(commands.Cog):

    def __init__(self, bot : commands.AutoShardedBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message : Message) -> None:
        """Whenever a message is sent check if it's content equals the bot's mention, if so respond with the prefix.

        Args:
            message (discord.Message): The message that was sent.
        """

        if message.content.lower() in [f"<@!{self.bot.user.id}>", f"<@{self.bot.user.id}>"]:
            embed = Embed(
                title = f"👋 Hey there, my name is {self.bot.user.name} and my prefix here is **`{await get_prefix(message)}`**!",
                color = maincolor
            )
            await message.channel.send(embed = embed)

    @commands.command()
    async def prefix(self, ctx : commands.Context, new_prefix : str = None) -> None:
        """View or set the prefix for the bot.

        Args:
            ctx (commands.Context): Discord's context object.
            new_prefix (str): The prefix we want to set or `remove` to set the prefix.
        """

        if not new_prefix:
            embed = Embed(
                title = f"👋 Hey there, my name is {self.bot.user.name} and my prefix here is **`{await get_prefix(ctx.message)}`**!",
                color = maincolor
            )
        elif not ctx.author.guild_permissions.manage_guild:
            embed = Embed(
                title = "Missing Permissions",
                description = f"You require the **Manage Server** permission to change the prefix of this server!",
                color = errorcolor
            )
        else:
            if new_prefix.lower() == "remove":
                embed = Embed(
                    title = "Prefix Removed",
                    description = "I have removed the prefix for this server!",
                    color = maincolor
                )
                await cluster.servers.prefixes.delete_one({"_id": ctx.guild.id})
            else:
                embed = Embed(
                    title = "Prefix Set",
                    descritpion = f"I have set the prefix for this server to **`{new_prefix}`**!",
                    color = maincolor
                )
                await cluster.servers.prefixes.update_one({"_id": Int64(ctx.guild.id)}, {"$set": {"prefix": new_prefix}}, upsert = True)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))
