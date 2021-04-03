# Packages.
## Packages that have to be installed through the package manager.
from discord import Embed
from discord.ext import commands
## Packages on this machine.
from config import maincolor

class Miscellaneous(commands.Cog):

    def __init__(self, bot : commands.AutoShardedBot) -> None:
        self.bot = bot
    
    @commands.command(aliases = ["latency"])
    async def ping(self, ctx : commands.Context) -> None:
        """Get the bot's gateway latency.

        Args:
            ctx (commands.Context): Discord's context object.
        """

        embed = Embed(
            title = "🏓 Pong!",
            description = f"Gateway latency is {int(round(self.bot.latency * 1000, 2))}ms.",
            color = maincolor
        )
        await ctx.send(embed = embed)
    
def setup(bot):
    bot.add_cog(Miscellaneous(bot))