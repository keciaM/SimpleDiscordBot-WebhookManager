import discord
from discord.ext import commands, tasks

from random import choice
from asyncio import TimeoutError

from scripts.config import discord_bot_version
from scripts.constants import *
from scripts.utils import *
from scripts.modals import AutoRoleModal
from scripts.ui import TicketSetup, PresistentViewBot


class DiscordBot():
    def __init__(self):

        self.bot = PresistentViewBot()
        self.bot.remove_command("help")

        self.on_ready()
        self.add_tasks()
        self.add_events()
        self.add_commands()
        self.add_admin_commands()      
        self.dev_mode()
        self.add_games()
        self.add_context_menu()

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

        @self.bot.event
        async def on_raw_reaction_add(payload):
            message_id = payload.message_id
            emoji = payload.emoji.name

            autorole_content = get_autorole_content(db_servers_path, payload.guild_id, message_id)
            if autorole_content is not None:
                for content in autorole_content:
                    if content['emoji'] == emoji:
                        role_id = content['role_id']

                        guild = discord.utils.find(lambda g : g.id == payload.guild_id, self.bot.guilds)
                        role = discord.utils.get(guild.roles, id=role_id)
                        if role is not None:
                            member = guild.get_member(payload.user_id)

                            if member is not None:
                                await member.add_roles(role)
                                print(f"Added role {role.name} to {member.name}")
                            else:
                                print(f"Member with ID {payload.user_id} not found in guild.")
                        else:
                            print(f"Role with ID {role_id} not found in guild.")
                        

    def add_commands(self):
        @self.bot.tree.command(name='help', description='List of all available commands and how to use them, for a detailed description, see the docs')
        async def help(interaction: discord.Interaction):
            user = interaction.user
            timestamp = datetime.now().strftime("%m/%d/%Y - %H:%M:%S")
            image_url = getattr(user.avatar, 'url', default_discord_ico)
            help_embed = discord.Embed(
                title='**ks. abp. py. Tomasz Jagódka**',
                description=f'Obecna wersja: {discord_bot_version}',
                color=discord.Color.dark_blue()
            ).set_author(
                name="keciaM", url="https://www.youtube.com/@keciaam", icon_url="https://images2.imgbox.com/a8/65/cIgpMy3R_o.jpg"
            ).set_footer(
                text=f'{user} // {timestamp}', icon_url=image_url
            )
            sections = {
                "Moderation 👮‍♂️": [],
                "Developer 👨🏻‍💻": [
                    '*/dev_mode*', '[True/False]\nSets Developer Mode On/Off',
                    '*/set_welcome*', '{user} {server}\nSet welcome message',
                    '*/set_leave*', '{user} {server}\nSet leave message',
                    '*/set_on_join_roles*', 'Set automatically added roles when member joining the server'
                ],
                "Forms 📋": [],
                "Games 🎮": [],
                "Others 🚣🏿‍♂️": []
            }
            for section, content in sections.items():
                help_embed.add_field(name=f'{10*invisible_sign}**{section}**', value='', inline=False)
                for i in range(0, len(content), 2):
                    help_embed.add_field(name=content[i], value=content[i+1], inline=True)
            await interaction.response.send_message(embed=help_embed)

        @self.bot.tree.command(name='user_info', description='Some info about user you choose')
        async def help(interaction: discord.Interaction, member: discord.Member):
            await interaction.response.send_message(embed=create_user_info_embed(member)) 

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
        
        @self.bot.tree.command(name='set_autorole', description='Set autorole channel to message emoji <channel>')
        async def modal(interaction: discord.Interaction, channel: discord.abc.GuildChannel):
            if interaction.user.guild_permissions.administrator:
                modal = AutoRoleModal()
                await interaction.response.send_modal(modal)

                await modal.submit_event.wait()
                modal.submit_event.clear()
                await modal.send_embed(interaction, channel)
                await modal.send_response_message(interaction, channel.id)
            else:
                await interaction.response.send_message(f'{interaction.user.mention} You do not have sufficient permissions to use this command')

        @self.bot.tree.command(name='set_autorole_emoji', description="Set autorole to emoji reaction on message <message_id> (or the bot's last message if None).")
        async def modal(interaction: discord.Interaction, emoji: str, role: discord.Role, message_id: str = None):
            message_id = int(message_id) if message_id else None  # Konwertuj message_id na int, jeśli jest podany
            if interaction.user.guild_permissions.administrator:
                if message_id is None:
                    did_mess_exists, mess_channel = check_autorole_mess(db_servers_path, interaction.user.guild.id)
                    if did_mess_exists and mess_channel:
                        add_autorole_content(db_servers_path, interaction.user.guild.id, did_mess_exists, emoji, role.id, role.name)
                        try:
                            channel = self.bot.get_channel(mess_channel)
                            mess = await channel.fetch_message(did_mess_exists)
                            await mess.add_reaction(emoji)
                            await interaction.response.send_message(
                                f'{interaction.user.mention} The autorole has been successfully set up.',
                              ephemeral=True)
                        except Exception as e:
                            await interaction.response.send_message(f'Error: {e}', ephemeral=True)
                    else:
                        await interaction.response.send_message(
                            f'{interaction.user.mention} No autorole message has been added on this server. '
                            'Please either manually enter the message ID or create a message using the **/set_autorole command.**'
                        )
                else:
                    try:
                        user_channel = interaction.channel
                        message = await user_channel.fetch_message(message_id)
                    except Exception as e:
                        print(f'Error fetching message: {e}')
                        return 

                    add_autorole(db_servers_path, interaction.user.guild.id, message_id, user_channel.id)
                    add_autorole_content(db_servers_path, interaction.user.guild.id, message_id, emoji, role.id, role.name)
                    try:
                        await message.add_reaction(emoji)
                        await interaction.response.send_message(
                            f'{interaction.user.mention} The autorole has been successfully set up.'
                        )
                    except Exception as e:
                        print(f'Error adding reaction: {e}')
            else:
                await interaction.response.send_message(f'{interaction.user.mention} You do not have sufficient permissions to use this command')

        @self.bot.tree.command(name='set_ticket_system', description="Set up ticket system on your server.")
        async def set_ticket_system(interaction: discord.Interaction):
            await interaction.response.send_message(f'{interaction.user.mention} Setting up the ticket system:', view=TicketSetup())
    


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

    def add_context_menu(self):
        @self.bot.tree.context_menu(name='Message ID')
        async def message_id_context(interaction: discord.Interaction, message: discord.Message):
            await interaction.response.send_message(f'The ID of this message is **{message.id}**', ephemeral=True)

        @self.bot.tree.context_menu(name='User Info')
        async def user_info_context(interaction: discord.Interaction, member: discord.Member):
            await interaction.response.send_message(embed=create_user_info_embed(member), ephemeral=True)

    def run(self, token):
        self.bot.run(token)
