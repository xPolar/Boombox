# Packages.
## Packages that have to be installed through the package manager.
import discord
from colorama import Fore, Style
from discord.ext import commands as discord_commands
from twitchio.ext import commands as commands
## Packages on this machine.
import config

class Twitch(discord_commands.Cog):
    def __init__(self, bot):
        self.discord_bot = bot
        self.initial_channels = []
        for document in config.sync_cluster.connected.documents.find({}):
            for name in document["twitch"]:
                if name not in self.initial_channels:
                    self.initial_channels.append(name)

        self.bot = commands.Bot(
            irc_token = "oauth:3njhsgosehwfzhvd9lr65zn1ke758c",
            client_id = "",
            nick = "polar_dev",
            prefix = "!",
            initial_channels = self.initial_channels
        )
        self.task = self.discord_bot.loop.create_task(self.bot.start())
    
    def cog_unload(self):
        self.task.cancel()

    @discord_commands.Cog.listener()
    async def on_message(self, message):
        if len(message.embeds) != 0 and message.author.id in config.supported_bots:
            if message.author.id in [234395307759108106, 368424172730187786, 287378523843198976] and message.embeds[0].description != discord.Embed.Empty and message.embeds[0].title == "Now playing" and message.author.voice: # Groovy 1-3
                document = await config.cluster.connected.documents.find_one({"channel": message.author.voice.channel.id, "bot": message.author.id})
                if document:
                    song_name = message.embeds[0].description.split("]")[0][1:]
                    for name in document["twitch"]:
                        channel = self.bot.get_channel(name)
                        if not channel:
                            await self.bot.join_channels([name])
                            channel = self.bot.get_channel(name)
                        await channel.send(f"Now playing: {song_name}")
                        print(f"{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}[NOW-PLAYING] {Fore.YELLOW}{song_name} {Fore.WHITE} in {Fore.YELLOW}{message.author.voice.channel.name} {Fore.WHITE}using {Fore.YELLOW}{message.author.name}{Fore.WHITE} -> {Fore.YELLOW}{name}{Fore.WHITE}!{Style.RESET_ALL}")
            elif message.author.id in [235088799074484224, 252128902418268161, 814675737331105832, 814675803065155585, 814675864859836417, 826622077615341569] and message.embeds[0].description != discord.Embed.Empty and message.embeds[0].title == "Now Playing 🎵" and message.author.voice: # Rythm 1-5 & Rythm-Chan
                document = await config.cluster.connected.documents.find_one({"channel": message.author.voice.channel.id, "bot": message.author.id})
                if document:
                    song_name = message.embeds[0].description.split("]")[0][1:]
                    for name in document["twitch"]:
                        channel = self.bot.get_channel(name)
                        if not channel:
                            await self.bot.join_channels([name])
                            chanenl = self.bot.get_channel(name)
                        await channel.send(f"Now playing: {song_name}")
                        print(f"{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}[NOW-PLAYING] {Fore.YELLOW}{song_name} {Fore.WHITE} in {Fore.YELLOW}{message.author.voice.channel.name} {Fore.WHITE}using {Fore.YELLOW}{message.author.name}{Fore.WHITE} -> {Fore.YELLOW}{name}{Fore.WHITE}!{Style.RESET_ALL}")
            elif message.author.id in [547905866255433758] and message.embeds[0].description != discord.Embed.Empty and message.embeds[0].title == "Now playing" and message.author.voice: # Hydra
                document = await config.cluster.connected.documents.find_one({"channel": message.author.voice.channel.id, "bot": message.author.id})
                if document:
                    song_name = message.embeds[0].description.split("]")[0][1:]
                    for name in document["twitch"]:
                        channel = self.bot.get_channel(name)
                        if not channel:
                            await self.bot.join_channels([name])
                            channel = self.bot.get_channel(name)
                        await channel.send(f"Now playing: {discord.utils.remove_markdown(song_name)}")
                        print(f"{Style.BRIGHT}{Fore.LIGHTMAGENTA_EX}[NOW-PLAYING] {Fore.YELLOW}{song_name} {Fore.WHITE} in {Fore.YELLOW}{message.author.voice.channel.name} {Fore.WHITE}using {Fore.YELLOW}{message.author.name}{Fore.WHITE} -> {Fore.YELLOW}{name}{Fore.WHITE}!{Style.RESET_ALL}")

def setup(discord_bot):
    discord_bot.add_cog(Twitch(discord_bot))