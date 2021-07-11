import sys
import traceback
import discord 
import os
from dotenv import load_dotenv
from discord.ext import commands

bot = commands.Bot(command_prefix='!', case_insensitive=True, allowed_mentions=discord.AllowedMentions(roles=False, users=True, everyone=False))

#test commit


#stores which user corresponds with which channel
bot.channel_assignments = {}

#list of extensions to load
extensions = ('games',)

#load extensions
count = 0
for ext in extensions:
    bot.load_extension(f"{ext}")
    print(f'Loaded {ext}')
    count += 1


@bot.event
async def on_ready():
    await bot.wait_until_ready()
    print('--------------------------')
    print(f'Logged in as: {bot.user.name}')
    print(f'With ID: {bot.user.id}')
    print(f'Loaded {count} extensions')
    print('--------------------------')


@bot.command()
async def ping(ctx): 
    await ctx.send(f'Pong! {round(bot.latency*1000)}ms')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        #await ctx.send('Invalid command used.')
        return
    
    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(f'Command is missing required arguments. Correct usage: `{ctx.command} {ctx.command.signature}`')
    else:
        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)



load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN2")
bot.run(TOKEN)