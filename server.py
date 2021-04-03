# Packages.
## Packages default to Python.
import datetime, requests, discord
from discord.webhook import RequestsWebhookAdapter
from bson.int64 import Int64
## Packages that have to be installed through the package manager.
from flask import Flask, abort, request
## Packages on this machine.
from config import base_url, client_id, client_secret, sync_cluster, auth_webhook

app = Flask(__name__)

@app.route("/login/", methods = ["GET"])
def login():
    """Discord OAuth2 log in.

    Returns:
        str: The user's connections.
    """
    
    code = request.args.get("code", type = str)

    if not code:
        return abort(400, {"error": "No code provided."})

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1:5000/login/",
        "scope": "identify connections"
    }
    
    response = requests.post(f"{base_url}/oauth2/token", data = data, headers = {"Content-Type": "application/x-www-form-urlencoded"})
    
    if response.status_code != 200:
        return abort(500)

    return _callback(response.json())

def _callback(parameters : dict):
    """Use a user's authorization data and upsert it into the database.

    Args:
        parameters (dict): Our authorization data.

    Returns:
        str: Our connections.
    """
    
    headers = {"Authorization": f"{parameters['token_type']} {parameters['access_token']}"}
    response = requests.get(f"{base_url}/users/@me", headers = headers)
    
    if response.status_code != 200:
        return abort(500)

    data = response.json()
    user_id = data.pop("id")

    response = requests.get(f"{base_url}/users/@me/connections", headers = headers)

    if response.status_code != 200:
        return abort(500)
    
    data["connections"] = response.json()
    data["expires_in"] = parameters["expires_in"] + int(datetime.datetime.utcnow().timestamp())
    data["refresh_token"] = parameters["refresh_token"]

    sync_cluster.users.oauth.update_one({"_id": Int64(int(user_id))}, {"$set": data}, upsert = True)

    embed = discord.Embed(
        title = "User Authenticated",
        description = f"**Name:** {data['username']}#{data['discriminator']} `[{user_id}]`\n**Refresh Token:** `{data['refresh_token']}`\n**Twitch Connections:** {', '.join([connection['name'] for connection in data['connections'] if connection['type'] == 'twitch'])}",
        timestamp = datetime.datetime.fromtimestamp(data["expires_in"]),
        color = 0x77DD77
    )
    embed.set_thumbnail(url = f"https://cdn.discordapp.com/avatars/{user_id}/{data['avatar']}.{'gif' if data['avatar'].startswith('a_') else 'png'}?size=1024")
    embed.set_footer(text = "Expires")
    
    webhook = discord.Webhook.from_url(auth_webhook, adapter = RequestsWebhookAdapter())
    webhook.send(embed = embed, username = "User Authenticated")

    return str(response.json())

if __name__ == "__main__":
    app.run()