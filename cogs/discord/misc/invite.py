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
    async def invite(self, ctx : commands.Context) -> None:
        """Get the bot's invite link.

        Args:
            ctx (commands.Context): Discord's context object.
        """

        embed = Embed(
            title = "🔗 Bot Invite Link",
            url = "https://discord.com/api/oauth2/authorize?client_id=825880443273478164&permissions=8&redirect_uri=http%3A%2F%2F127.0.0.1%3A5000%2Flogin%2F&response_type=code&scope=bot%20identify%20connections",
            color = maincolor
        )
        await ctx.send(embed = embed)
    
def setup(bot):
    bot.add_cog(Miscellaneous(bot))