from discord import Embed, member, Colour
from datetime import datetime

from scripts.database import *
from scripts.constants import default_discord_ico


def check_if_server_exists_in_db(path, id, guild_name):
    data = load_data(path)
    new_server = check_server(data, id)
    if new_server:
        data = add_server(data, guild_name, id)
        save_data(path, data)

def make_discord_embed(title: str, desc: str, url: str, date: bool = True, embed_color: Colour = Colour.brand_red()):
    if date:
        time = datetime.now()
    else:
        time = None
    embed=Embed(title=title, description=desc, timestamp=time, color=embed_color).set_image(url=url)
    return embed

def format_message(message: str, member, guild):
    formatted_message = message.replace('{user}', member).replace('{server}', guild)
    return formatted_message