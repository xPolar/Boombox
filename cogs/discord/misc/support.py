# Packages.
## Packages that have to be installed through the package manager.
from discord import Embed
from discord.ext import commands
## Packages on this machine.
from config import maincolor

class Miscellaneous(commands.Cog):

    def __init__(self, bot : commands.AutoShardedBot) -> None:
        self.bot = bot
    
    @commands.command()
    async def support(self, ctx : commands.Context) -> None:
        """Get the bot's support server invite link.

        Args:
            ctx (commands.Context): Discord's context object.
        """

        embed = Embed(
            title = "🔗 Support Server Invite Link",
            url = "TODO support server invite",
            color = maincolor
        )
        await ctx.send(embed = embed)
    
def setup(bot):
    bot.add_cog(Miscellaneous(bot))