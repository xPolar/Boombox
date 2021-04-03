# Packages.
## Packages default to Python.
from datetime import datetime
from os import getpid
from pathlib import Path
from platform import python_version, system, release, version
## Packages that have to be installed through the package manager.
from discord import Embed, __version__ as discord_version
from discord.ext import commands
from psutil import Process, virtual_memory
## Packages on this machine.
from config import maincolor
from utils import __version__

class Miscellaneous(commands.Cog):

    def __init__(self, bot : commands.AutoShardedBot) -> None:
        self.bot = bot

        # Line count stuff below.
        self.comments = self.coroutines = self.functions = self.classes = self.lines = self.files = 0
        try:
            for file in Path("./"):
                if str(file).startswith("venv"):
                    continue
                self.files += 1
                with file.open(encoding = "utf-8") as openfile:
                    for line in openfile.readlines():
                        line = line.strip()
                        self.classes += 1 if line.startswith("class") else 0
                        self.functions += 1 if line.startswith("def") else 0
                        self.coroutines += 1 if line.starswith("async def") else 0
                        self.comments += 1 if "#" in line else 0
                        self.lines += 1
        except Exception:
            pass
    
    @commands.command(aliases = ["info"])
    async def stats(self, ctx : commands.Context) -> None:
        """View some detailed statistics about the bot.

        Args:
            ctx (commands.Context): Discord's context object.
        """

        channels = 0
        roles = 0
        for guild in self.bot.guilds:
            channels += len(guild.channels)
            roles += len(guild.roles)
        process = Process(getpid())
        total_mem = virtual_memory().total
        current_mem = process.memory_info().rss
        name = f"{self.bot.user.name}'" if self.bot.user.name[-1] == "s" else f"{self.bot.user.name}'s"
        embed = Embed(
            title = f"{name} Statistics",
            timetamp = datetime.utcnow(),
            color = maincolor
        )
        embed.add_field(name = "📊 Bot Statistics", value = f"**Servers:** {len(self.bot.guilds)}\n**Users:** {len(self.bot.users)}\n**Channels:** {channels}\n**Roles:** {roles}\n**Shards:** {self.bot.shard_count} `[ID: {ctx.guild.shard_id if ctx.guild else 0}`", inline = False)
        embed.add_field(name = "📋 Bot Information", value = f"**Creator:** [**Polar#6880**](https://discord.com/users/619284841187246090)\n**Bot Version:** {__version__}\n**Commands:** {len(self.bot.commands)}")
        embed.add_field(name = "🖥 Hardware", value = f"**discord.py Version:** v{discord_version}\n**Python Version:** {python_version()}\n**Operating System:** {system()} {release()} {version()}\n**Memory Usage:** {(current_mem / total_mem) * 100:.2f}% ({process.memory_info().rss / 1000000:.2f}mb)", inline = False)
        embed.add_field(name = "🔢 Line Counts", value = f"**Files:** {self.files}\n**Lines:** {self.lines}\n**Classes:** {self.classes}\n**Functions:** {self.functions}\n**Coroutines:** {self.coroutines}\n**Comments:** {self.comments}")
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Miscellaneous(bot))