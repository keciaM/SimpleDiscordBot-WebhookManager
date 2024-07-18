from discord import Embed, Member, Colour, Color
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

def create_user_info_embed(user: Member):
    avatar_url = user.avatar.url if user.avatar else default_discord_ico

    embed = Embed(title=f'User Info - {user.name}', color=Color.blue())
    embed.set_image(url=avatar_url)
    
    embed.add_field(name='User ID', value=user.id, inline=False)
    embed.add_field(name='Username', value=user.name, inline=False)
    embed.add_field(name='Joined Server', value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name='Account Created', value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)

    return embed

def format_message(message: str, member, guild):
    formatted_message = message.replace('{user}', member).replace('{server}', guild)
    return formatted_message