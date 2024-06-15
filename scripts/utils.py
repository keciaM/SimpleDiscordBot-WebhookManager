from discord import Embed, member
from datetime import datetime

from scripts.database import *
from scripts.constants import default_discord_ico


def check_if_server_exists_in_db(path, id, guild_name):
    data = load_data(path)
    new_server = check_server(data, id)
    if new_server:
        data = add_server(data, guild_name, id)
        save_data(path, data)

def make_discord_embed(title, desc, url):
    embed=Embed(title=title, description=desc, timestamp=datetime.now()).set_image(url=url)
    return embed

def format_message(message: str, member, guild):
    formatted_message = message.replace('{user}', member).replace('{server}', guild)
    return formatted_message