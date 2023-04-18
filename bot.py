import discord
import random
import pywhatkit
import os

from discord.ext import commands as cm
from discord.ext import tasks
from itertools import cycle

client = cm.Bot(command_prefix='.')
status = cycle(['VALORANT', 'SHIT', 'ON UR MOM', 'UR FEELINGS'])


@client.event
async def on_ready():
    # await client.change_presence(status=discord.Status.idle,activity=discord.Game('VALORANT'))
    change_status.start()
    print('Bot is ready !')


@client.event
async def on_member_join(member):
    print(f'{member} has joined the server !')


@client.event
async def on_member_remove(member):
    print(f'{member} has left the server !')


@client.event
async def on_command_error(ctx,error):
    if isinstance(error,cm.MissingRequiredArgument):
        await ctx.send('PLEASE PASS IN ALL REQUIRED ARGUMENTS !!!')

    if isinstance(error,cm.CommandNotFound):
        await ctx.send('INVALID COMMAND  !!!')


@tasks.loop(hours=1)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))


@client.command()
async def ping(ctx):
    await ctx.send(f'Pong, {round(client.latency * 1000)}ms !')


@client.command()
async def favsong(ctx):
    pywhatkit.playonyt('https://www.youtube.com/watch?v=KYis63WGGJo')
    await ctx.send('just dont cry ...')


@client.command()
async def youtube(ctx,*,song):
    pywhatkit.playonyt('song')
    await ctx.send(f'"{song}" is playing on youtube !')


@client.command(aliases=['8ball', 'guess'])
async def _8ball(ctx, *, question):
    responses = ['dont know',
                 'i think so',
                 'as you see ',
                 'yes',
                 'no',
                 'certain',
                 'could be ...'
                 ]
    await ctx.send(f'Your quistion :{question}\nMy answer: {random.choice(responses)}')


@client.command()
async def clear(ctx, amount:int):
    await ctx.channel.purge(limit=amount)


@clear.error
async def clear_error(ctx,error):
    if isinstance(error, cm.MissingRequiredArgument):
     await ctx.send('--clear command needs the amount--')


@client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f' {member.mention}  Kicked !')


@client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f' {member.mention}  Banned !')


@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    mem_name, mem_dis = member.split('#')
    for ban_mem in banned_users:
        user = ban_mem.user
        if (user.name, user.discriminator) == (mem_name, mem_dis):
            await ctx.guild.unban(user)
            await ctx.send(f' {user.mention} Unbanned !')
            return


@client.command()
@cm.has_permissions(manage_messages=True)
async def load(ctx, ext):
    client.load_extension(f'Cog.{ext}')
    await ctx.send(f'the file "{ext}" is loaded')


@client.command()
@cm.has_permissions(manage_messages=True)
async def unload(ctx, ext):
    client.unload_extension(f'Cog.{ext}')
    await ctx.send(f'the file "{ext}" is unloaded')


# auto load for 'py' files
for filename in os.listdir('./Cog'):
    if filename.endswith('.py'):
        client.load_extension(f'Cog.{filename[:-3]}')

client.run('ODY1MDc2NDc0NTM2OTE5MTAw.YO-vPw.yyjtSM6k0vGG-8yf4Ogd3aQW_mc')
