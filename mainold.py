import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from discord.utils import get
import datetime
from time import sleep as s
import random
import requests as r
from spotipy import SpotifyClientCredentials
import spotipy
from config import *
# from scripts.database import *
from scripts.meme import *
from scripts.mod import *
from scripts.valorantAPI import *
from scripts.youtubeAPI import *
from scripts.elevenlabsAPI import *
from scripts.ruletka import *
from scripts.constants import *
from scripts.utils import *

# Inicjowanie bota
intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members=True

bot = commands.Bot(command_prefix='/', intents=intents)
bot.remove_command("help")

# Database
# conn = DataBase('statystyki')
# conn.setup_connection()

# Lista statusów
status_list = [
    'Ctrl+C, Ctrl+V, Ctrl+Z ',
    'Stack Overflow',
    'Discord',
    'Reddit',
    'Amerykańska Ruletka',
    'Counter Strike 2',
    'VALORANT',
    "You want to play? Let's play",
    'Grand Theft Auto V',
    'Minecraft',
    'keciaM',
    'Jebać rudych',
    'Visual Studio Code',
    'ja też potrzebuję przerwy D:',
    'Phasmophobia',
    'YouTube.com'
]

# Logowanie oraz lista serwerów
@bot.event
async def on_ready():
    print('Logged on as', bot.user)
    await bot.tree.sync()
    change_status.start()
    checkforvideos.start()
    for guild in bot.guilds:
        print(f'-> {guild.name}')

#Pętle
@tasks.loop(seconds=30)
async def checkforvideos():
    try:
        chan, link = check_video()
        if chan and link is not None:
            vid_chan = bot.get_channel(int(chan))
            await vid_chan.send(link)
        else:
            print('Żaden debil nie wrzucił nic nowego ziomek')
    except TypeError as e:
        print(e)
# Zmiana statusu
@tasks.loop(seconds=120)
async def change_status():
    new_status = random.choice(list(status_list))
    await bot.change_presence(activity=discord.Game(name=new_status))

# Odpowiadacz
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f'{message.author} - {message.content}')
    message.content = message.content.lower()

    if message.content == 'ping':
        await message.channel.send('pong')
    if 'siema' in message.content:
        await message.channel.send(f'{message.author.mention} spierdalaj :>')
    if message.content == 'aha':
        await message.channel.send('aha')
        s(1)
        await message.channel.send('okej')

    if 'python' in message.content:
        await message.channel.send('koham')
        s(0.5)
        await message.channel.send('pajtona')
        s(0.5)
        await message.channel.send('kurwa')

    elif message.content in [':>', ':D', ':)']:
        hehe_dir = '\\data\\hehe.jpg'
        await message.channel.send('no hejka seksiaku :DD')
        await message.channel.send(file=discord.File(hehe_dir))

    if '<@775375717591416842>' in message.content or '<@851497297312743475>' in message.content:
        gif_url = 'https://media1.tenor.com/m/JGhQ_mPnjZwAAAAC/kowalski-matke.gif'
        await message.channel.send(f'{message.author.mention} co mnie oznaczasz')
        s(0.5)
        await message.channel.send(f'{gif_url}')

    if message.content.startswith('py.'):
        await bot.process_commands(message)

    if (message.content.lower() == "spierdalaj tomuś" or
            message.content.lower() == "spierdalaj tomek"):
        await message.channel.send('aha :<, no to spierdalam')
        print('Bot zostanie wyłączony na 5 minut...')
        await bot.close()

# Powitanie
@bot.event
async def on_member_join(member: discord.Member):
    if member.guild.id == kosciol_server_id:
        channel = bot.get_channel(welcome_channel_id)
        try:
            embed=discord.Embed(title=f"Siema {member.name}", 
                                description=f"Polecam ci kurwa wypierdalać 🙂!",
                                timestamp=datetime.now()).set_image(url=member.avatar.url)
        except Exception as e: 
            print(e)
            embed=discord.Embed(title=f"Siema {member.name}", 
                                description=f"Polecam ci kurwa wypierdalać 🙂!",
                                timestamp=datetime.now()).set_image(url=default_discord_img_url)
        await member.send(format_welcome_message(member))
        await channel.send(embed=embed)

# Pożegnanie
@bot.event
async def on_member_remove(member):
   if member.guild.id == kosciol_server_id:
    channel = bot.get_channel(992472331198939258)
    await channel.send(f"Ten debil, {member.name} nas opuścił, a to chujek z niego")

# Role na reakcje
@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    if message_id == sexrole_mess_id:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == '👍':
            role  = discord.utils.get(guild.roles, name='-PySiu-')
            print('-PySiu-')
        elif payload.emoji.name  == '👎':
            role  = discord.utils.get(guild.roles, name='-PySia-')
            print('-PySia-')
        
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
            else:
                print('a chuj ci na pizde')
    if message_id == py_role_mess_id:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == 'python':
            role  = discord.utils.get(guild.roles, name='Python')
            print('python')
        elif payload.emoji.name  == 'java':
            role  = discord.utils.get(guild.roles, name='Java')
            print('java')
        elif payload.emoji.name  == 'js':
            role  = discord.utils.get(guild.roles, name='JavaScript')
            print('js')
        elif payload.emoji.name  == 'cpp':
            role  = discord.utils.get(guild.roles, name='C++')
            print('c++')
        
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.add_roles(role)
            else:
                print('a chuj ci na pizde')
@bot.event
async def on_raw_reaction_remove(payload):
    message_id = payload.message_id
    if message_id == sexrole_mess_id:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == '👍':
            role  = discord.utils.get(guild.roles, name='-PySiu-')
            print('-PySiu-')
        elif payload.emoji.name  == '👎':
            role  = discord.utils.get(guild.roles, name='-PySia-')
            print('-PySia-')
        
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
            else:
                print('a chuj ci na pizde')
    if message_id == py_role_mess_id:
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, bot.guilds)

        if payload.emoji.name == 'python':
            role  = discord.utils.get(guild.roles, name='Python')
            print('python')
        elif payload.emoji.name  == 'java':
            role  = discord.utils.get(guild.roles, name='Java')
            print('java')
        elif payload.emoji.name  == 'js':
            role  = discord.utils.get(guild.roles, name='JavaScript')
            print('js')
        elif payload.emoji.name  == 'cpp':
            role  = discord.utils.get(guild.roles, name='C++')
            print('c++')
        
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            if member is not None:
                await member.remove_roles(role)
            else:
                print('a chuj ci na pizde')

#====================  
#       KOMENDY
#====================  

@bot.tree.command(name='help', description='O HUI TU CHODZI????')
async def help(interaction: discord.Interaction):
    user = interaction.user
    now = datetime.now()
    timestamp = now.strftime("%m/%d/%Y - %H:%M:%S")

    help_embed = discord.Embed(title='**ks. abp. py. Tomasz Jagódka**', description=f'Obecna wersja: {discord_bot_version}', color= discord.Color.dark_blue())
    help_embed.set_author(name="keciaM", url="https://www.youtube.com/@keciaam", icon_url="https://images2.imgbox.com/a8/65/cIgpMy3R_o.jpg") 
    # Moderacja
    help_embed.add_field(name=f'{30*invisible_sign}**Kącik Moderacji 👮‍♂️**', value='' , inline=False) 
    help_embed.add_field(name='*/ban*', value='Banujesz użytkownika na serwerze', inline=True)
    help_embed.add_field(name='*/unban*', value='Odbanowujesz użytkownika na serwerze (chwilowo nie działa)', inline=True) 
    help_embed.add_field(name='*/kick*', value='Wyrzucasz użytkownika z serwera', inline=True) 
    help_embed.add_field(name='*/warn*', value='Dajesz ostrzeżenie uźytkownikowi', inline=True)
    help_embed.add_field(name='*/gotohell*', value='Wyciszasz użytkownika (dostępne tylko na kościele)', inline=True)

    # Wazne
    help_embed.add_field(name='', value='' , inline=False)
    help_embed.add_field(name=f'{34*invisible_sign}**Ankiety 📋**', value='' , inline=False)
    help_embed.add_field(name='*/pythanin*', value='Dostań dodatkowe przywileje i zostań gigachadem', inline=True)
    help_embed.add_field(name='*/report*', value='Zgłaszasz użytkownika do moderacji', inline=True)

    #   Gry
    help_embed.add_field(name='', value='' , inline=False)
    help_embed.add_field(name=f'{35*invisible_sign}**Gry 🎮**', value='' , inline=False)
    help_embed.add_field(name='*/ruletka*', value='Zagraj w rosyjską ruletke', inline=True)
    help_embed.add_field(name='*/count*', value='Kto szybciej policzy? (1 - Łatwy, 2 - Nomralny, 3 - Trudny)', inline=True)

    # Pozostałe
    help_embed.add_field(name='', value='' , inline=False)
    help_embed.add_field(name=f'{35*invisible_sign}**Inne 🚣🏿‍♂️**', value='' , inline=False)
    help_embed.add_field(name='*/author*', value='O autorze tego bota i podziękowania', inline=True)
    help_embed.add_field(name='*/eleven*', value='Generuje głos AI z tekstu', inline=True)
    help_embed.add_field(name='*/help*', value='Wyświetla tą komendę', inline=True)
    help_embed.add_field(name='*/memeit*', value='Generuje obrazek z wybranym tekstem', inline=True)
    help_embed.add_field(name='*/valorank*', value='Generuje obrazek z rangą z gry VALORANT', inline=True)
    help_embed.add_field(name='*/serverstats*', value='Wyświetla statystyki serwera', inline=True)
    help_embed.add_field(name='*/userinfo*', value='Wyświetla profil użytkownika (możesz też użyć context menu)', inline=True)
    try:
        help_embed.set_footer(text=f'{user} // {timestamp}', icon_url = user.avatar)
    except Exception as e:
        print(e)
        help_embed.set_footer(text=f'{user} // {timestamp}', icon_url = default_discord_img_url)

    await interaction.response.send_message(embed=help_embed)  

@bot.tree.command(name='userinfo', description="chcesz dowiedziec sie cos o sobie? Oznacz użytkownika jeśli chcesz dowiedzieć się coś o kimś ")
async def userinfo(interaction: discord.Interaction, member: discord.Member = None):

    if member is None:
        user = interaction.user
    else:
        user = member
    
    try:
        embed = discord.Embed(title=f'User Info - {user.name}', color=discord.Color.blue()).set_image(url=user.avatar.url)
    except Exception as e:
        print(e)
        embed = discord.Embed(title=f'User Info - {user.name}', color=discord.Color.blue()).set_image(url=default_discord_img_url)
    embed.add_field(name='User ID', value=user.id, inline=False)
    embed.add_field(name='Username', value=user.name, inline=False)
    embed.add_field(name='Joined Server', value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name='Account Created', value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.context_menu(name='User Info')
async def userinfo_context(interaction: discord.Interaction, member: discord.Member):
    user = member
    try:
        embed = discord.Embed(title=f'User Info - {user.name}', color=discord.Color.blue()).set_image(url=user.avatar.url)
    except Exception as e:
        print(e)
        embed = discord.Embed(title=f'User Info - {user.name}', color=discord.Color.blue()).set_image(url=default_discord_img_url)
    embed.add_field(name='User ID', value=user.id, inline=False)
    embed.add_field(name='Username', value=user.name, inline=False)
    embed.add_field(name='Joined Server', value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name='Account Created', value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)

    await interaction.response.send_message(embed=embed, ephemeral=True)

@bot.tree.command(name='serverstats', description="chcesz dowiedziec sie cos o serwerze?")
async def serverstats(interaction: discord.Interaction):
    user = interaction.user
    server = user.guild
    # server.members
    # server.owner.name
    # server.owner.id 

    embed=discord.Embed(title=f"{server.name}")
    embed.set_author(name=server.owner.name, icon_url=server.owner.avatar.url)
    embed.add_field(name="Użytkownicy:", value=server.member_count, inline=False)
    embed.add_field(name="Kanały:", value=len(server.channels), inline=False)

    await interaction.response.send_message(embed=embed)

@bot.tree.command(name='eleven', description="Głos AI na twoje żądanie")
async def eleven(interaction: discord.Interaction, text: str):
    await interaction.response.send_message('Okej')
    try:
        output_filename = elevenlabs(text=text)
        with open(output_filename, 'rb') as file:
            
            await interaction.channel.send(file=discord.File(file, filename=output_filename))
    except FileNotFoundError:
            await interaction.response.send_message("Coś sie zjebało")   
    delete_temp_eleven()

@bot.tree.command(name='memeit', description="Generuje obrazek spadre z wybranym tekstem")
async def memeit(interaction: discord.Interaction, text: str):
    await interaction.response.send_message(file=discord.File(spadre(text)))

@bot.tree.command(name='author', description="Autorzy tego gówna")
async def author(interaction: discord.Interaction):
    embed=discord.Embed(title="Autor", url="https://www.youtube.com/@keciaam", description="Giga gówno zaprogramowane w pejncie\n Jeśli masz jakieś pomysły albo błedy wyślij mi je na discordzie:\n **[super.keciam](https://discordapp.com/users/775375717591416842)**", color=discord.Color.blue())
    embed.set_author(name="keciaM", url="https://www.youtube.com/@keciaam", icon_url="https://images2.imgbox.com/a8/65/cIgpMy3R_o.jpg")
    embed.add_field(name="**Podziękowania**", value="dla mojego przyjaciela (dsc: **parkurek**), za pomoc przy ogarnięciu kodu", inline=True)
    embed.set_image(url="https://images2.imgbox.com/01/8c/YykU4rrf_o.png")
    await interaction.response.send_message(embed=embed)

#VALORANT API
@bot.tree.command(name='valorank', description="Twoja obecna ranga w VALORANT")
async def valorank(interaction: discord.Interaction, nick: str, tag: str, region: str = 'eu'):
    valoapirankurl = f'https://api.henrikdev.xyz/valorant/v1/mmr/{region}/{nick}/{tag}'
    print(valoapirankurl)
    response = r.get(valoapirankurl)
    try:
        if response.status_code == 200:
            data = response.json()

            current_tier_patched = data['data']['currenttierpatched']
            ranking_in_tier = data['data']['ranking_in_tier']
            mmr_change_to_last_game = data['data']['mmr_change_to_last_game']
            name = data['data']['name']
            tag = data['data']['tag']
            rank_img = data['data']['images']['large']
            file = makevalorankcard(current_tier_patched, str(ranking_in_tier), name=name,  tag=tag, rank_img=rank_img, rr_last_game=mmr_change_to_last_game)
            await interaction.response.send_message(file=file)
        else:
            print("Nie udało się pobrać danych. Status kodu: ", response.status_code)
    except Exception as e:
        print(e)

@bot.tree.command(name='valorank_v2', description="Twoja obecna ranga w VALORANT // v2")
async def valorank_v2(interaction: discord.Interaction, nick: str, tag: str, region: str = 'eu'):
    await interaction.response.send_message('sie robi szefunciu')
    card_img, rank_img, account_level, rank, rr, rr_last_game, valo_name, valo_tag, puuid = get_valorant_acc_stats(region=region, nick=nick, tag=tag)
    print(f" URL karty gracza: {card_img}\n URL ikony gracza: {rank_img}\n Poziom konta: {account_level}\n Ranga: {rank}\n RR: {rr}\n RR w ostatniej grze: {rr_last_game}\n Nick: {valo_name}\n Tag: {valo_tag}\n Puuid: {puuid}")
    try:
        card_file = make_valorank_card_v2(valo_name, valo_tag, rank_img, str(account_level), card_img)
    except Exception as e:
        print(e)
    await interaction.channel.send(file=card_file)

#========================
#   Kącik moderacji
#========================

@bot.tree.command(name='ban', description="banuje skurwiela")
@has_permissions(administrator=True)
async def ban(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    user = interaction.user
    if  user.guild_permissions.administrator:
        if reason is None:
            reason = ('nic :>')
        message_ok = f"Dostałeś bana w **{user.guild.name}** za **'{reason}'**, weź się ogarnij"
        await member.send(message_ok)
        if member.guild.id == kosciol_server_id:
            target_channel = bot.get_channel(bans_channel_id)
            await target_channel.send(f'Ten debil, **{member.name}**\n właśnie dostał bana za **{reason}**. Dobrze mu tak')
            addban(jsondb, member, member.id, reason=reason, autor=user) 
        await member.ban(reason=reason)
        await interaction.response.send_message('Sie robi szefunciu', ephemeral=True)
    else:
        await interaction.response.send_message(f"Kutasie {user.mention}, nie masz uprawnień")

#DO NAPRAWY
@bot.tree.command(name='unban', description="analogicznie, odbanowuje go // NIE DZIAŁA, DO POPRAWY W KOLEJNYM UPDATE")
@has_permissions(administrator=True)
async def unban(interaction: discord.Interaction, member: str):
    user = interaction.user
    if  user.guild_permissions.administrator:
        await user.guild.unban(member)
        message_ok = f"Dostałeś unbana w **{interaction.guild.name}**, nie pozdrawiam"
        await member.send(message_ok)
        await interaction.response.send_message('Nie pojebało cie?', ephemeral=True)
    else:
        await interaction.response.send_message(f"Kutasie {user.mention}, nie masz uprawnień")

#DO NAPRAWY
@bot.tree.command(name='warn', description="daje ostrzeżenie skurwielowi")
@has_permissions(administrator=True)
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    user = interaction.user
    if  user.guild_permissions.administrator:
        if reason is None:
            reason = ('egzystencję :>')
        addwarn(member.id)
        x = checkwarns(member.id)
        print(x)
        message_ok = f"Dostałeś ostrzeżenie w **{interaction.guild.name}** za **'{reason}'**, weź nie wkurwiaj ludzi\n Liczba twoich warnów: **{x}**"
        await member.send(message_ok)
        await interaction.response.send_message('UwU', ephemeral=True)
    else:
        await interaction.response.send_message(f"Kutasie {user.mention}, nie masz uprawnień")

#DO NAPRAWY!!!
# @bot.command(help='| sprawdza ile warnów ma użytkownik')
# async def checkwarns(ctx, member: discord.Member):
#     warns_num = checkwarns(member.id)
#     await ctx.send(f"Użytkownik: **{member}**, ma {warns_num} ostrzeżeń")

# @bot.command(help='| resetuje warny użytkownika')
# async def removewarns(ctx, member: discord.Member):
#     if  ctx.author.guild_permissions.administrator: 
#         removewarn(member.id)
#         await ctx.send(f'Użytkonik **{member}**, nie ma już ostrzeżeń, farciarz...')      
#     else:
#         await ctx.send(f"Kutasie {ctx.author.mention}, nie masz uprawnień")

@bot.tree.command(name='kick', description="wywalasz niegrzecznego chujka")
@has_permissions(administrator=True)
async def kick(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    user = interaction.user
    if  user.guild_permissions.administrator:
        if reason is None:
            reason = ('nic :>')
        message_ok = f"Zostałeś wyrzucony z **{interaction.guild.name}** za **'{reason}'**, weź ładnie przeproś"
        await member.send(message_ok)
        if interaction.guild.id == kosciol_server_id:
            target_channel = bot.get_channel(bans_channel_id)
            await target_channel.send(f'Ten debil, **{member.name}**\n właśnie został wyrzucony za **{reason}**.')
        await member.kick(reason=reason)
        await interaction.response.send_message('No i zajebiście', ephemeral=True)
    else:
        await interaction.response.send_message(f"Kutasie {user.mention}, nie masz uprawnień")

#DO NAPRAWY
@bot.tree.command(name='gotohell', description="kolega zostaje czasowo wyciszony za bycie jebanym kutasiarzem", guild=bot.get_guild(kosciol_server_id))
@has_permissions(administrator=True)
async def gotohell(interaction: discord.Interaction, member: discord.Member, reason: str = None):
    user = interaction.user
    if reason is None:
        reason = ('nic :>')
    if  user.guild_permissions.administrator and interaction.guild_id == kosciol_server_id:
        message_ok = f"Zostałeś tymczasowo wyciszony z **{interaction.guild.name}** za **'{reason}'**, kogo tym razem wkurwiłeś?"
        await member.send(message_ok)
        role = discord.utils.get(interaction.guild.roles, name=desired_role_name)
        try:
            await member.edit(roles=[])
            await member.add_roles(role)
        except Exception as e:
            print(e)
        target_channel = bot.get_channel(bans_channel_id)
        await target_channel.send(f'Pajton piekielny właśnie pochłonoł tego debila, **{member.name}**\n za **{reason}**.')
        await interaction.response.send_message(f"C++ go skusił :(")
    else:
        await interaction.response.send_message(f"Kutasie {user.mention}, nie masz uprawnień")

#=====================================  
#           Modale kurwiu        
#=====================================   
    
class ReportModal(discord.ui.Modal, title='Zgłoszenie/Zażalenie do administracji'):
    username = discord.ui.TextInput(label='Użytkownik',placeholder='Kogo chcesz zgłosić? (opcjonalnie)', required=False, max_length=30, style=discord.TextStyle.short)
    description = discord.ui.TextInput(label='Co chcesz?', placeholder='np. Ten jebany w dupe chuj dał mi chujowy nick', required=True, max_length=2000, style = discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        now = datetime.now()
        timestamp = now.strftime("%m/%d/%Y - %H:%M:%S")
        await interaction.response.send_message(f'{interaction.user.mention}, twoje zgłoszenie zostało przekazane do administracji (może)', ephemeral=True)

        channel = discord.utils.get(interaction.guild.channels, name = 'moderacja-czy-cos')    

        await channel.send(f'***Zgłoszenie użytkownika {interaction.user.mention}***\n**Podejrzany**: {self.username}\n**Opis sytuacji**: {self.description}\n**Data zgłoszenia**: {timestamp}')

@bot.tree.command(name='report', description="Zgłoś użytkownika/ Złóż zażalenie")
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(ReportModal())

class PythaninModal(discord.ui.Modal, title='ZOSTAŃ GIGACHADEM JUŻ DZIŚ!'):
    username = discord.ui.TextInput(label='Podaj swój nick',placeholder='np. super.keciam', required=True, max_length=40, style= discord.TextStyle.short)
    language = discord.ui.TextInput(label='Jakiego języka programowania używasz?',placeholder='np. Python', required=True, max_length=40, style= discord.TextStyle.short)
    tutorial = discord.ui.TextInput(label='Czy chcesz poszerzać swoją wiedzę?',placeholder='Tak/Nie', required=True, max_length=40, style= discord.TextStyle.short)
    level = discord.ui.TextInput(label='Jak bardzo zaawansowany jesteś?',placeholder='np. No napisałem z rudym chujem prosty kod, jestem w chuj zaawansowany i doświadczony', required=True, max_length=500, style= discord.TextStyle.paragraph)
    about = discord.ui.TextInput(label='Dodaj coś od siebie / Uwagi (opcjonalnie)', placeholder='np. yyyyy jestem rudy i ne lubie Pythona', required=False, max_length=500, style= discord.TextStyle.paragraph)


    async def on_submit(self, interaction: discord.Interaction):
        now = datetime.now()
        timestamp = now.strftime("%m/%d/%Y - %H:%M:%S")
        await interaction.response.send_message(f'{interaction.user.mention}, twoje podanie o zostanie Pythaninem zostanie niedługo rozpatrzone', ephemeral=True)

        channel = discord.utils.get(interaction.guild.channels, name = 'moderacja-czy-cos')

        await channel.send(f"***Podanie użytkownika {interaction.user.mention}***"
                   f"\n========================================="
                   f"\n**Jakiego języka programowania używasz?**: *{self.language}*"
                   f"\n**Czy chcesz poszerzać swoją wiedzę?**: *{self.tutorial}*"
                   f"\n**Jak bardzo zaawansowany jesteś?**: *{self.level}*"
                   f"\n**Dodaj coś od siebie / Uwagi**: *{self.about}*"
                   f"\n========================================="
                   f"\n*{self.username} - {timestamp}*")

@bot.tree.command(name='pythanin', description="Zostań gigachadem")
async def modal(interaction: discord.Interaction):
    await interaction.response.send_modal(PythaninModal())

#========================
#   GRY
#========================

@bot.tree.command(name='ruletka', description="Rosyjska ruletka skurwielu!")
async def ruletka(interaction: discord.Interaction, enemy: discord.Member):    
    autor = interaction.user
    
    def bullet_check(message):
            return message.author == current_player and message.content.isdigit() and 1 <= int(message.content) <= 6

    def check_last_bullet(kill_bullet, available_bullets):
        return len(available_bullets) == 1 and kill_bullet in available_bullets

    if enemy == autor:
        await interaction.response.send_message("Nie możesz wybrać samego siebie jako przeciwnika jebany idioto!")
        return
    if enemy.bot:
        await interaction.response.send_message("No chyba cie coś boli")
        return
    await interaction.response.send_message(f"{enemy.mention}, *{autor.mention}* chce zagrać w rosyjską ruletkę! Czy przyjmujesz wyzwanie? (tak/nie)")
    def check(message):
        return message.author == enemy and message.content.lower() in ['tak', 'nie']
    try:
        response = await bot.wait_for('message', check=check, timeout=60)
    except TimeoutError:
        await interaction.channel.send(f"Czas na akceptację minął, {enemy.mention} obszczał zbroję. Gra anulowana.")
        return
    if response.content.lower() == 'nie':
        await interaction.channel.send(f"{enemy.mention} odmówił, pewnie ma pełne gacie. Gra anulowana.")
        return

    conn = DataBase('statystyki')
    author_id = autor.id
    przeciwnik_id = enemy.id

    players = [autor, enemy]
    print('Gracze: ',players)

    print('ID Autora: ', author_id)
    print('ID Przeciwnika: ', przeciwnik_id)
    if conn.get_player(author_id) is None:
        conn.add_player(author_id, 0, 0, 0)
    
    if conn.get_player(przeciwnik_id) is None:
        conn.add_player(przeciwnik_id, 0, 0, 0)
        
    await interaction.channel.send("Zaczynamy grę w rosyjską ruletkę ruletkę!")

    s(1)
    await interaction.channel.send("==================================")
    await interaction.channel.send(f"{autor.mention} vs {enemy.mention}")
    await interaction.channel.send("==================================")
    s(1)
    author_data = conn.get_player(autor.id)
    przeciwnik_data = conn.get_player(enemy.id)

    author_wins = author_data["wins"] if author_data else 0
    author_losses = author_data["losses"] if author_data else 0
    przeciwnik_wins = przeciwnik_data["wins"] if przeciwnik_data else 0
    przeciwnik_losses = przeciwnik_data["losses"] if przeciwnik_data else 0

    try:
        author_ico = autor.avatar.url
        print(author_ico)
        author_ico = download_user_ico(author_ico)
        print(author_ico)
        print('Załadowano ikonę autora')
    except Exception as e:
        print(e)
        author_ico = 'data/discorduser.jpeg'
        print('ERROR - Coś się zjebało z ikoną autora')
    try:
        przeciwnik_ico = enemy.avatar.url
        print(przeciwnik_ico)
        przeciwnik_ico = download_user_ico(przeciwnik_ico)
        print(przeciwnik_ico)
        print('Załadowano ikonę przeciwnika')
    except Exception as e:
        print(e)
        przeciwnik_ico = 'data/discorduser.jpeg'
        print('ERROR - Coś się zjebało z ikoną przeciwnika')
    print(author_ico, przeciwnik_ico)
    try:
        file = make_roulette_card(author_ico, przeciwnik_ico, autor.name, enemy.name, str(author_wins), str(author_losses), str(przeciwnik_wins), str(przeciwnik_losses))
        await interaction.channel.send(file=file)
    except Exception as e:
        await interaction.channel.send("coś się zjebało w związku z tworzeniem karty ruletki")
        print(e)
        

    available_bullets = [1, 2, 3, 4, 5, 6]
    kill_bullet = random.choice(available_bullets)
    player_one, player_two = random.sample(players, 2)
    current_player = player_one
    print('Obecny gracz: ',current_player)
    print(f'Gracz pierwszy: {player_one}\nKredyty: {conn.get_player(player_one.id)["credits"]}')
    print(f'Gracz drugi: {player_two}\nKredyty: {conn.get_player(player_two.id)["credits"]}')
    print('Pocisk który zabija: ',kill_bullet)

    while True:
        if check_last_bullet(kill_bullet, available_bullets):
            if player_one == current_player:
                print('aha gówno dwa')
                loser = player_one.id
                losername = player_one
                winner = player_two.id
                winnername = player_two
            else:
                print('ten pierwszy przegrał')
                loser = player_two.id
                losername = player_two
                winner = player_one.id
                winnername = player_one

            gif3_url = 'https://media1.tenor.com/m/RYQJ37l40NsAAAAd/ooof.gif'
            await interaction.channel.send(f"{losername.mention}, {winnername.mention} zabija cię ostatnim pociskiem bo sosiesz chuja")
            s(1)
            await interaction.channel.send(f"PRZEGRAŁEŚ! {losername.mention} , get better")
            await interaction.channel.send(f'{gif3_url}')
            await interaction.channel.send("Koniec gry")

            player_data_loser = conn.get_player(loser)
            if player_data_loser is None:
                conn.add_player(loser, 0, 0, 0)
                player_data_loser = conn.get_player(loser)

            player_data_winner = conn.get_player(winner)
            if player_data_winner is None:
                conn.add_player(winner, 0, 0, 0)
                player_data_winner = conn.get_player(winner)

            conn.update_player_lose(loser)
            conn.update_player_credits(loser, -1)
            
            conn.update_player_win(winner)
            conn.update_player_credits(winner, 1)
            break

        await interaction.channel.send(f"{current_player.mention}, wybierz numer pocisku [1-6]:")

        try:
            response = await bot.wait_for('message', check=bullet_check, timeout=60)
        except TimeoutError:
            await interaction.channel.send(f"Czas na wybór pocisku minął, {current_player.mention} może spróbuj zagrać w amerykańską ruletkę? Gra została poddana przez {current_player.mention}.")
            loser = current_player.id
            player_data_loser = conn.get_player(loser)
            if player_data_loser is None:
                conn.add_player(loser, 0, 0, 0)
                player_data_loser = conn.get_player(loser)
            conn.update_player_lose(loser)
            conn.update_player_credits(loser, -1)
            return

        chosen_bullet = int(response.content)

        if chosen_bullet == kill_bullet:
            gif2_url = 'https://media.tenor.com/BxFxrSLDKCAAAAAi/gif.gif'
            await interaction.channel.send(f"PRZEGRAŁEŚ! {current_player.mention} , get better")
            await interaction.channel.send(f'{gif2_url}')
            await interaction.channel.send("Koniec gry")
            if player_one == current_player:
                print('aha gówno')
                loser = player_one.id
                winner = player_two.id
            else:
                print('ten drugi przegrał')
                loser = player_two.id
                winner = player_one.id

            player_data_loser = conn.get_player(loser)
            if player_data_loser is None:
                conn.add_player(loser, 0, 0, 0)
                player_data_loser = conn.get_player(loser)

            player_data_winner = conn.get_player(winner)
            if player_data_winner is None:
                conn.add_player(winner, 0, 0, 0)
                player_data_winner = conn.get_player(winner)

            conn.update_player_lose(loser)
            conn.update_player_credits(loser, -1)
            
            conn.update_player_win(winner)
            conn.update_player_credits(winner, 1)

            break
        else:
            if chosen_bullet in available_bullets:
                available_bullets.remove(chosen_bullet)
                await interaction.channel.send(f"{current_player.mention} wybrał pocisk {chosen_bullet} i niestety przeżył. Dostępne pociski: {available_bullets}")
            else:
                await interaction.channel.send(f"{current_player.mention}, ten pocisk został już kurwa wybrany idioto jebany. Spróbuj ponownie.")
                continue
        
        current_player = player_two if current_player == player_one else player_one

@bot.tree.command(name='count', description="Kto szybciej policzy? (1 - Łatwy, 2 - Nomralny, 3 - Trudny)")
async def count(interaction: discord.Interaction, difficulty:  int = 2):
    operations = ['+', '-', '*', '/']
    operation = []
    numbers = []
    if difficulty == 0:
        number = random.randint(3, 3)
        zakresa, zakresb = 1, 10
        operations = ['+', '-']
    elif difficulty == 1:
        number = random.randint(3, 4)
        zakresa, zakresb = 1, 20
    elif difficulty == 2:
        number = random.randint(3, 5)
        zakresa, zakresb = 1, 50
    elif difficulty == 3:
        number = random.randint(3, 6)
        zakresa, zakresb = 1, 100
    else:
        interaction.response.send_message('Niepoprawny poziom trudności debilu') 

    for num in range(1, number):
        numbers.append(num)

    for index, integer in enumerate(numbers):
        if index != len(numbers) - 1:
            integer = randint(zakresa, zakresb)
            operation.append(str(integer))
            operation.append(random.choice(operations))
            print(integer)
        else:
            integer = randint(zakresa, zakresb)
            print(integer)
            operation.append(str(integer))

    print(operation)
    math = ''.join(operation)
    result = eval(math)
    if isinstance(result, float):
        result = round(result, 2)
    else:
        pass
    print("Działanie matematyczne:", math)
    print("Wynik:", result)

    await interaction.response.send_message(f'Policzcie to debile: {math}')

    def check(message):
        return message.content.lower()
    try:
        timeout = 120
        while True:
            response = await bot.wait_for('message', check=check, timeout=timeout)
            if str(result) in response.content:
                await interaction.channel.send(f'Gratulacje! {response.author.mention}, umiesz w matematyke!')
                break
            else:
                await interaction.channel.send(f'{response.author.mention} Kurwa debilu, ale weź może najpierw policz poprawnie')
                timeout = 60
    except TimeoutError:
        await interaction.channel.send(f"Te debile nie umieją w matematyka")

bot.run(TOKEN)



