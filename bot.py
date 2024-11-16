import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Certifique-se de que seu bot tem permissões para ver membros

bot = commands.Bot(command_prefix='!', intents=intents)

TOKEN = 'SEU_TOKEN_AQUI'  # Coloque o token do seu bot aqui

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def addrole(ctx, member: discord.Member, role: discord.Role):
    await member.add_roles(role)
    await ctx.send(f'O cargo {role.name} foi atribuído a {member.name}')

@bot.command()
@commands.has_permissions(manage_roles=True)
async def removerole(ctx, member: discord.Member, role: discord.Role):
    await member.remove_roles(role)
    await ctx.send(f'O cargo {role.name} foi removido de {member.name}')

bot.run(TOKEN)
