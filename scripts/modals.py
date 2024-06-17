import discord
from asyncio import Event

class AutoRoleModal(discord.ui.Modal, title='Set autorole to message emoji'):

    submit_event = Event()
    modal_title = discord.ui.TextInput(label='Title', placeholder='e.g. Choose your gender!', required=True, max_length=50, style=discord.TextStyle.short)
    description = discord.ui.TextInput(label='Description', placeholder='e.g.👱‍♂️ - Male (Use shift + enter to write on a new line)', required=True, max_length=2000, style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'{interaction.user.mention}, Okay, I have the title and description of your message,'
                                                 ' and I sent them to the desired channel. Your unique message id is **{}**.' 
                                                 ' To set the emojis and roles I should add, maybe use the **/set_autorole_emoji** command')
        self.submit_event.set()
        
    def get_values(self):
        return self.modal_title.value, self.description.value


        