import discord
import sqlite3
import re
from discord.ext import commands
from config import settings
from gamemode_parameters import laps_settings
import scoreboardshow
from Player import Player

conn = sqlite3.connect(r'data/SpinOsBD.db')
cur = conn.cursor()

bot = commands.Bot(command_prefix = settings['prefix'])

#ключевое
game_is_on = False
laps = 10
players = []

#----------register_channel------------------
@bot.command(pass_context=True)
async def register(ctx):

    if ctx.message.channel.id == settings['register_channel']:

        s = re.split(r' ', ctx.message.content) 
        
        if len(s) >= 2: #брехня, придумать чего получше
            name = s[1]
            id = ctx.message.author.id

            cur.execute(f"select Name from Players where id = {id}")
            search_result = cur.fetchall()

            if len(search_result) == 0: # если id не найдется в базе, то создать
                cur.execute(f"insert into Players values ({id},'{name}',0)")
                conn.commit()
                await ctx.send(f'Игрок {ctx.message.author.mention} зарегистрирован в системе под ником - {name}!')  
            else:
                await ctx.send(f'Вы уже зарегистрированы в системе!')
        else:
            await ctx.send(f'Ошибка ввода команды!')
    else:
        await ctx.send('Данная команда не разрешена в этом чате.')

#----------game_channel------------------
@bot.command(pass_context=True)
async def gm(ctx):
    if ctx.message.channel.id == settings['game_channel'] and not game_is_on:
        s = re.split(r' ', ctx.message.content)
        if len(s) == 2: #брехня, придумать чего получше
            laps = laps_settings[ s[1] ]
            embed = discord.Embed(title="Настройки игры:", color=0x808080)
            embed.add_field(name="Кол-во кругов", value=laps, inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'Ошибка ввода команды!')
    else:
        await ctx.send('Данная команда не разрешена в этом чате.')

@bot.command(pass_context=True)
async def join(ctx):
    if ctx.message.channel.id == settings['game_channel'] and not game_is_on:
        cur.execute(f"select Name from Players where id = {ctx.message.author.id}")
        name = cur.fetchall()
        already_added = False
        for x in players:
            if name[0][0] in x.name:
                already_added = True
        if name is not None and not already_added:
            players.append( Player( ctx.message.author.id, name[0][0], 0) )
            await ctx.send(f'{ctx.message.author.mention} присоединился к игре o/')
        elif name is not None and already_added:
            await ctx.send(f'{ctx.message.author.mention} уже в списке игроков!')
        else:
            await ctx.send(f'{ctx.message.author.mention} не зарегистрирован')

@bot.command(pass_context=True)
async def tb(ctx):
    if ctx.message.channel.id == settings['game_channel']:
        await ctx.send(f"```\n{scoreboardshow.scoreboardshow.show_in_game_table(players)}\n```")

@bot.command(pass_context=True)
async def start():
    if ctx.message.channel.id == settings['game_channel'] and not game_is_on:
        game_is_on = True
    elif ctx.message.channel.id == settings['game_channel'] and game_is_on:
        await ctx.send('Игра уже идет.')
    else:
        await ctx.send('Данная команда не разрешена в этом чате.')

@bot.command(pass_context=True)
async def nx():
    #123
    await ctx.send('')

#----------scoreboard_channel------------------
@bot.command(pass_context=True)
async def sc(ctx):
    if ctx.message.channel.id == settings['scoreboard_channel']:
        list = scoreboardshow.scoreboardshow.show(cur)
        await ctx.send(f"```\n{list}\n```")
    else:
        await ctx.send('Данная команда не разрешена в этом чате.')

#----------game_channel_not_botcomm------------------
async def check_lap():
    #123
    await ctx.send('')

bot.run(settings['token'])
