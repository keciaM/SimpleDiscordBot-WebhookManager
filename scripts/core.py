import discord
from discord.ext import commands, tasks

from random import choice
from asyncio import TimeoutError

from scripts.config import discord_bot_version
from scripts.constants import *
from scripts.utils import *
from scripts.modals import AutoRoleModal

class DiscordBot():
    def __init__(self):

        self.intents = discord.Intents.default()
        self.intents.message_content = True
        self.intents.reactions = True
        self.intents.members = True

        self.bot = commands.Bot(command_prefix='/', intents=self.intents)
        self.bot.remove_command("help")

        self.on_ready()
        self.add_tasks()
        self.add_events()
        self.add_commands()
        self.add_admin_commands()      
        self.dev_mode()
        self.add_games()

    def on_ready(self):
        @self.bot.event
        async def on_ready():
            await self.bot.tree.sync() #Slash commands
            print(f'Logged on as {self.bot.user}') #Login in
            for guild in self.bot.guilds:
                print(f'-> {guild.name}')
                check_if_server_exists_in_db(db_servers_path, guild.id, guild.name)
                
            self.change_status.start()

    def add_tasks(self):
        @tasks.loop(seconds=120)
        async def change_status():
            new_status = choice(list(status_list))
            await self.bot.change_presence(activity=discord.Game(name=new_status)) 

        self.change_status = change_status

    def add_events(self):
        @self.bot.event
        async def on_guild_join(guild):
            embed=discord.Embed(title="**======== *Thanks For Adding Me!* ========**", 
                                description=f"Thanks for adding me to '{guild.name}'\n**Quick installation guide** \n"
                                "Use the /dev_mode command to start developer mode\n"
                                "Add welcome and farewell messages using /set_welcome and /set_leave\n"
                                "Try the /add_autorole command to give the community your unique roles\n",
                                color=0xd89522)
            check_if_server_exists_in_db(db_servers_path, guild.id, guild.name)
            await guild.text_channels[0].send(embed=embed)

        @self.bot.event
        async def on_member_join(member: discord.Member):
            data = load_data(db_servers_path)
            custom_mess_exist = check_custom_mess(data, member.guild.id , 'welcome')
            if custom_mess_exist:
                welcome_embed = get_welcome_message(db_servers_path, member.guild.id)
                channel = self.bot.get_channel(int(welcome_embed['channel_id']))
                try:
                    image_url = member.avatar.url
                except Exception as e:
                    print(e)
                    image_url = default_discord_ico
                
                title = format_message(welcome_embed['title'], member.name, member.guild.name)
                desc = format_message(welcome_embed['desc'], member.mention, member.guild.name)

                print(title, desc)

                embed = make_discord_embed(title, desc, image_url)

                await channel.send(embed=embed)

            roles = get_join_roles(db_servers_path, member.guild.id)
            
            for role in roles:
                try:
                    add_role = discord.utils.get(member.guild.roles, id=int(role))
                    await member.add_roles(add_role)
                except Exception as e:
                    print(e)
                    pass

        @self.bot.event
        async def on_member_remove(member: discord.Member): 
            data = load_data(db_servers_path)
            custom_mess_exist = check_custom_mess(data, member.guild.id , 'bye')
            if custom_mess_exist:
                bye_message = get_leave_message(db_servers_path, member.guild.id)
                channel = self.bot.get_channel(int(bye_message['channel_id']))
                await channel.send(format_message(bye_message['message'], member.name, member.guild.name))

    def add_commands(self):
        @self.bot.tree.command(name='help', description='List of all available commands and how to use them, for a detailed description, see the docs')
        async def help(interaction: discord.Interaction):
            user = interaction.user
            now = datetime.now()
            timestamp = now.strftime("%m/%d/%Y - %H:%M:%S")

            help_embed = discord.Embed(title='**ks. abp. py. Tomasz Jagódka**', description=f'Obecna wersja: {discord_bot_version}', color= discord.Color.dark_blue())
            help_embed.set_author(name="keciaM", url="https://www.youtube.com/@keciaam", icon_url="https://images2.imgbox.com/a8/65/cIgpMy3R_o.jpg") 
            # Moderacja
            help_embed.add_field(name=f'{10*invisible_sign}**Moderation 👮‍♂️**', value='' , inline=False) 
            
            # Developer
            help_embed.add_field(name=f'{10*invisible_sign}**Developer 👨🏻‍💻**', value='' , inline=False) 
            help_embed.add_field(name='*/dev_mode*', value='[True/False]\nSets Developer Mode On/Off', inline=True)
            help_embed.add_field(name='*/set_welcome*', value='{user} {server}\nSet welcome message', inline=True) 
            help_embed.add_field(name='*/set_leave*', value='{user} {server}\nSet leave message', inline=True) 
            help_embed.add_field(name='*/set_on_join_roles*', value='Set automatically added roles when member joining the server', inline=True) 

            # Wazne
            help_embed.add_field(name='', value='' , inline=False)
            help_embed.add_field(name=f'{10*invisible_sign}**Forms 📋**', value='' , inline=False)

            #   Gry
            help_embed.add_field(name='', value='' , inline=False)
            help_embed.add_field(name=f'{10*invisible_sign}**Games 🎮**', value='' , inline=False)

            # Pozostałe
            help_embed.add_field(name='', value='' , inline=False)
            help_embed.add_field(name=f'{10*invisible_sign}**Others 🚣🏿‍♂️**', value='' , inline=False)
            try:
                image_url = user.avatar.url
            except Exception as e:
                print(e)
                image_url = default_discord_ico

            help_embed.set_footer(text=f'{user} // {timestamp}', icon_url = image_url)

            await interaction.response.send_message(embed=help_embed)  

    def add_admin_commands(self):
        @self.bot.tree.command(name='set_welcome', description='Set welcome message <channel> <title> <description>')
        async def set_welcome(interaction: discord.Interaction, channel: discord.abc.GuildChannel, title: str, description: str):
            if  interaction.user.guild_permissions.administrator:
                data = load_data(db_servers_path)
                custom_mess = check_custom_mess(data, interaction.user.guild.id, 'welcome')
                if custom_mess:
                    await interaction.response.send_message(f'{interaction.user.mention} Welcome message on this server already is set.\n You still want to proceed? [yes/no]')
                    try:
                        response = await self.bot.wait_for("message", check=lambda m: m.author == interaction.user, timeout=30)
                        if response.content.lower() == "yes":
                            pass        
                        elif response.content.lower() == "no":
                            return
                    except TimeoutError:
                        await interaction.channel.send(f'{interaction.user.mention} You did not respond in time.')
                        return 
                add_welcome_message(db_servers_path, interaction.user.guild.id, channel.id, title, description)
                try:
                    await interaction.response.send_message(f'{interaction.user.mention} Your welcome message has been set successfully')
                except Exception as e:
                    print(f"Error: {e}")
                    await interaction.channel.send(f'{interaction.user.mention} Your welcome message has been set successfully')
                
            else:
                await interaction.response.send_message(f'{interaction.user.mention} You do not have sufficient permissions to use this command')

        @self.bot.tree.command(name='set_leave', description='Set leave message <channel> <message>')
        async def set_leave(interaction: discord.Interaction, channel: discord.abc.GuildChannel, message: str):
            if interaction.user.guild_permissions.administrator:
                data = load_data(db_servers_path)
                custom_mess = check_custom_mess(data, interaction.user.guild.id, 'bye')
                if custom_mess:
                    await interaction.response.send_message(f'{interaction.user.mention} Leave message on this server already is set.\n You still want to proceed? [yes/no]')
                    try:
                        response = await self.bot.wait_for("message", check=lambda m: m.author == interaction.user, timeout=30)
                        if response.content.lower() == "yes":
                            pass        
                        elif response.content.lower() == "no":
                            return
                    except TimeoutError:
                        await interaction.channel.send(f'{interaction.user.mention} You did not respond in time.')
                        return 
                add_leave_message(db_servers_path, interaction.user.guild.id, channel.id, message)
                try:
                    await interaction.response.send_message(f'{interaction.user.mention} Your leave message has been set successfully')
                except Exception as e:
                    print(f"Error: {e}")
                    await interaction.channel.send(f'{interaction.user.mention} Your leave message has been set successfully')               
            else:
                await interaction.response.send_message(f'{interaction.user.mention} You do not have sufficient permissions to use this command')

        @self.bot.tree.command(name='set_on_join_roles', description='Set automatically added roles when member joining the server <role>')
        async def set_on_join_roles(interaction: discord.Interaction, role: discord.Role):
            if interaction.user.guild_permissions.administrator:
                data = load_data(db_servers_path)
                print(role.id)
                add_role_on_join(db_servers_path, interaction.user.guild.id, role.id)
            else:
                await interaction.response.send_message(f'{interaction.user.mention} You do not have sufficient permissions to use this command')
        
        @self.bot.tree.command(name='set_autorole', description='Set autorole to message emoji <channel>')
        async def modal(interaction: discord.Interaction, channel: discord.abc.GuildChannel):
            if interaction.user.guild_permissions.administrator:
                modal = AutoRoleModal()
                await interaction.response.send_modal(modal)

                await modal.submit_event.wait()
                modal_title, modal_description = modal.get_values()

                embed = make_discord_embed(modal_title, modal_description, None, False)
                await channel.send(embed=embed)
            else:
                await interaction.response.send_message(f'{interaction.user.mention} You do not have sufficient permissions to use this command')

    def dev_mode(self):
        @self.bot.tree.command(name='dev_mode', description='Sets Developer Mode On/Off [True/False]')
        async def dev_mode(interaction: discord.Interaction, mode: str):
            if  interaction.user.guild_permissions.administrator:
                if mode.lower() in ['false', 'off']:
                    mode = False
                elif mode.lower() in ['true', 'on']:
                    mode = True
                else:
                    await interaction.response.send_message(f'Select the correct value', ephemeral=True)
                    return
                change_dev_mode(db_servers_path, int(interaction.user.guild.id), mode)
                await interaction.response.send_message(f'Your Developer Mode is now set to {mode}', ephemeral=True)
            else:
                await interaction.response.send_message(f'{interaction.user.mention} You do not have sufficient permissions to use this command')

    def add_games(self):
        pass

    def run(self, token):
        self.bot.run(token)
