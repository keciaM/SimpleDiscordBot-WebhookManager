import discord
from asyncio import Event

from scripts.utils import make_discord_embed
from scripts.constants import db_servers_path
from scripts.database import add_autorole

class AutoRoleModal(discord.ui.Modal, title='Set autorole to message emoji'):

    submit_event = Event()
    modal_title = discord.ui.TextInput(label='Title', placeholder='e.g. Choose your gender!', required=True, max_length=50, style=discord.TextStyle.short)
    description = discord.ui.TextInput(label='Description', placeholder='e.g.👱‍♂️ - Male (Use shift + enter to write on a new line)', required=True, max_length=2000, style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        self.submit_event.set()
        await interaction.response.send_message('Okay, your message has been sent successfully!')
    
    async def send_embed(self, interaction: discord.Interaction, channel):
            self.embed = make_discord_embed(self.modal_title.value, self.description.value, None, False)
            self.message = await channel.send(embed=self.embed)
            add_autorole(db_servers_path, interaction.user.guild.id, self.message.id, channel.id)
    
    async def send_response_message(self, interaction: discord.Interaction, user_channel: int):
        await interaction.channel.send(f'{interaction.user.mention}, Your message ID is **{self.message.id}** on **<#{user_channel}>**.\n' 
                                        'To set the emojis and roles, please use the **/set_autorole_emoji** command.')


        