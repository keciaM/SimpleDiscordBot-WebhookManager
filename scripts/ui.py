import discord
from discord.ext import commands


class PresistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        super().__init__(command_prefix=commands.when_mentioned_or('.'), intents=intents)
    async def setup_hook(self) -> None:
        self.add_view(TicketSetup())

class TicketSetup(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Title", style=discord.ButtonStyle.primary, emoji="🎉", custom_id='1')
    async def title_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("test", ephemeral=True)

    @discord.ui.button(label="Description", style=discord.ButtonStyle.primary, emoji="📄", custom_id='2')
    async def description_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("test", ephemeral=True)

    @discord.ui.button(label="Color", style=discord.ButtonStyle.primary, emoji="🎨", custom_id='3')
    async def color_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("test", ephemeral=True)

    @discord.ui.button(label="Server Avatar", style=discord.ButtonStyle.primary, emoji="📷", custom_id='4')
    async def avatar_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("test", ephemeral=True)
    
    @discord.ui.button(label="Set!", style=discord.ButtonStyle.primary, emoji="💥", custom_id='5')
    async def set_button_callback(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("test", ephemeral=True)
