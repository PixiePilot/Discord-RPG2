import discord
from discord.ext import commands
import os
from discord.ext.commands import has_permissions, MissingPermissions
bot = commands.Bot(command_prefix="!")
#TOKEN = 'OTIxNDU5MjkwMjczODk4NTA3.YbzN1g.D4Gk6j-Mc2dDQELm6rGQeMebaNk'
with open("Token.txt") as read:
    TOKEN = (read.readline())
@bot.event
async def on_ready():
    print(f'Connection to discord : ok\non user: {bot.user}')

@commands.has_permissions(administrator=True)
@bot.command()
async def load(ctx, extension):
    print(f'{extension} has been loaded by {ctx.author}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loading {extension}!')
    pass

@commands.has_permissions(administrator=True)
@bot.command()
async def unload(ctx, extension):
    print(f'{extension} has been unloaded by {ctx.author}')
    bot.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloading {extension}!')
    pass

@commands.has_permissions(administrator=True)
@bot.command()
async def reload(ctx, extension):
    await ctx.send(f'Reloading {extension}')
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')
    await ctx.send('Reload complete!')
    pass

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
    pass

bot.run(TOKEN)




