# Packages.
## Packages that have to be installed through the package manager.
from discord import Embed, utils
from colorama import Fore, Style
from discord.ext import commands as discord_commands
from twitchio.ext import commands as commands
## Packages on this machine.
from config import twitch_client_id, cluster, irc_token, twitch_prefix, nick, supported_bots, sync_cluster

class Twitch(discord_commands.Cog):

    def __init__(self, bot):
        self.discord_bot = bot
        self.initial_channels = []
        for document in sync_cluster.connected.documents.find({}):
            for name in document["twitch"]:
                if name not in self.initial_channels:
                    self.initial_channels.append(name)

        self.bot = commands.Bot(
            irc_token = irc_token,
            client_id = twitch_client_id,
            nick = nick,
            prefix = twitch_prefix,
            initial_channels = self.initial_channels
        )
        self.task = self.discord_bot.loop.create_task(self.bot.start())
    
    def cog_unload(self):
        self.task.cancel()

    @discord_commands.Cog.listener()
    async def on_message(self, message):
        if len(message.embeds) != 0 and message.author.id in supported_bots:
            if document := await cluster.connected.documents.find_one({"channel": message.author.voice.channel.id, "bot": message.author.id}):
                if message.author.id in [234395307759108106, 368424172730187786, 287378523843198976] and message.embeds[0].description != Embed.Empty and message.embeds[0].title == "Now playing" and message.author.voice:  # Groovy 1-3
                    song_name = message.embeds[0].description.split("]")[0][1:]
                    for name in document["twitch"]:
                        channel = self.bot.get_channel(name)
                        if not channel:
                            await self.bot.join_channels([name])
                            channel = self.bot.get_channel(name)
                        await channel.send(f"Now playing: {song_name}")
                        print(f"{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}[NOW-PLAYING] {Fore.YELLOW}{song_name} {Fore.WHITE} in {Fore.YELLOW}{message.author.voice.channel.name} {Fore.WHITE}using {Fore.YELLOW}{message.author.name}{Fore.WHITE} -> {Fore.YELLOW}{name}{Fore.WHITE}!{Style.RESET_ALL}")
                elif message.author.id in [235088799074484224, 252128902418268161, 814675737331105832, 814675803065155585, 814675864859836417, 826622077615341569] and message.embeds[0].description != Embed.Empty and message.embeds[0].title == "Now Playing 🎵" and message.author.voice:  # Rythm 1-5 & Rythm-Chan
                    song_name = message.embeds[0].description.split("]")[0][1:]
                    for name in document["twitch"]:
                        channel = self.bot.get_channel(name)
                        if not channel:
                            await self.bot.join_channels([name])
                            channel = self.bot.get_channel(name)
                        await channel.send(f"Now playing: {song_name}")
                        print(f"{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}[NOW-PLAYING] {Fore.YELLOW}{song_name} {Fore.WHITE} in {Fore.YELLOW}{message.author.voice.channel.name} {Fore.WHITE}using {Fore.YELLOW}{message.author.name}{Fore.WHITE} -> {Fore.YELLOW}{name}{Fore.WHITE}!{Style.RESET_ALL}")
                elif message.author.id in [547905866255433758] and message.embeds[0].description != Embed.Empty and message.embeds[0].title == "Now playing" and message.author.voice:  # Hydra
                    song_name = message.embeds[0].description.split("]")[0][1:]
                    for name in document["twitch"]:
                        channel = self.bot.get_channel(name)
                        if not channel:
                            await self.bot.join_channels([name])
                            channel = self.bot.get_channel(name)
                        await channel.send(f"Now playing: {utils.remove_markdown(song_name)}")
                        print(f"{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}[NOW-PLAYING] {Fore.YELLOW}{song_name} {Fore.WHITE} in {Fore.YELLOW}{message.author.voice.channel.name} {Fore.WHITE}using {Fore.YELLOW}{message.author.name}{Fore.WHITE} -> {Fore.YELLOW}{name}{Fore.WHITE}!{Style.RESET_ALL}")

def setup(discord_bot):
    discord_bot.add_cog(Twitch(discord_bot))
