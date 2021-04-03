# Packages.
## Packages default to Python.
import datetime, requests
from bson.int64 import Int64
## Packages that have to be installed through the package manager.
import requests_async as requests, discord, aiohttp
from colorama import Fore, Style
from discord.ext import commands, tasks
## Packages on this machine.
from config import cluster, client_id, client_secret, base_url, auth_webhook

class UpdateOauth(commands.Cog):

    def __init__(self, bot : commands.AutoShardedBot) -> None:
        """Whenever the cog is loaded do all of the following."""

        self.bot = bot
        self.update_oauth.start()
    
    def cog_unload(self):
        """Whenever the cog is unloaded do all of the following."""

        self.update_oauth.cancel()
    
    @tasks.loop(seconds = 30)
    async def update_oauth(self) -> None:
        """Update all users who are going to have their oauth invalidate within the next mintue."""

        async for document in cluster.users.oauth.aggregate([{"$match": {"expires_in": {"$lte": int(datetime.datetime.utcnow().timestamp()) + 60}}}]):

            data = {
                "client_id": client_id,
                "client_secret": client_secret,
                "grant_type": "refresh_token",
                "refresh_token": document["refresh_token"],
                "redirect_uri": "http://127.0.0.1:5000/callback/",
                "scope": "identify connections"
            }
            
            response = await requests.post(f"{base_url}/oauth2/token", data = data, headers = {"Content-Type": "application/x-www-form-urlencoded"})

            if response.status_code != 200:
                continue
            
            data = response.json()
            headers = {"Authorization": f"{data['token_type']} {data['access_token']}"}
            expires_in = data["expires_in"] + int(datetime.datetime.utcnow().timestamp())
            refresh_token = data["refresh_token"]
            
            response = await requests.get(f"{base_url}/users/@me", headers = headers)
            
            if response.status_code != 200:
                continue
            
            data = response.json()
            user_id = data.pop("id")

            response = await requests.get(f"{base_url}/users/@me/connections", headers = headers)
            
            if response.status_code != 200:
                continue
                
            data["connections"] = response.json()
            data["expires_in"] = expires_in
            data["refresh_token"] = refresh_token

            await cluster.users.oauth.update_one({"_id": Int64(int(user_id))}, {"$set": data})

            embed = discord.Embed(
                title = "User Reauthenticated",
                description = f"**Name:** {data['username']}#{data['discriminator']} `[{user_id}]`\n**Refresh Token:** `{data['refresh_token']}`\n**Twitch Connections:** {', '.join([connection['name'] for connection in data['connections'] if connection['type'] == 'twitch'])}",
                timestamp = datetime.datetime.fromtimestamp(data["expires_in"]),
                color = 0x77DD77
            )
            embed.set_thumbnail(url = f"https://cdn.discordapp.com/avatars/{user_id}/{data['avatar']}.{'gif' if data['avatar'].startswith('a_') else 'png'}?size=1024")
            embed.set_footer(text = "Expires")
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(auth_webhook, adapter = discord.AsyncWebhookAdapter(session))
                await webhook.send(embed = embed, username = "User Reauthenticated")

            print(f"{Style.BRIGHT}{Fore.GREEN}[OAUTH-UPDATED]{Fore.WHITE} OAuth updated for {Fore.YELLOW}{data['username']}#{data['discriminator']} ({user_id}){Fore.WHITE}!{Style.RESET_ALL}")

    @update_oauth.before_loop 
    async def waiter(self) -> None:
        """Wait until the bot is ready."""

        await self.bot.wait_until_ready() 
    
    @update_oauth.error
    async def update_oauth_error(self, error : Exception):
        """Whenever our update_oauth task has an error raise it.

        Args:
            error (Exception): The error that arose.

        Raises:
            error: The error that arose.
        """

        raise error

def setup(bot):
    bot.add_cog(UpdateOauth(bot))