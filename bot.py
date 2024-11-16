#Todos os tokens foram retirados por questão de privacidade
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import sqlite3
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Carrega o token do bot a partir do arquivo .env
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

# Configura os intents para permitir que o bot veja membros
intents = discord.Intents.default()
intents.members = True

# Cria uma instância do bot com um prefixo de comando '!'
bot = commands.Bot(command_prefix='!', intents=intents)

# Conecta ao banco de dados SQLite (ou cria se não existir)
conn = sqlite3.connect('discord_bot_logs.db')
c = conn.cursor()

# Cria a tabela de logs se não existir
c.execute('''
          CREATE TABLE IF NOT EXISTS logs (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              user_id INTEGER,
              user_name TEXT,
              role_name TEXT,
              action TEXT,
              timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
          )
          ''')
conn.commit()

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    
    # Obtém o servidor (guild) pelo nome - substitua pelo nome do seu servidor
    guild = discord.utils.get(bot.guilds, name='Nome do Seu Servidor')
    
    # Nomes dos cargos a serem criados
    role_names = ['Acesso Básico', 'Acesso Avançado', 'Modo ADM']

    # Cria os cargos se ainda não existirem
    for role_name in role_names:
        existing_role = discord.utils.get(guild.roles, name=role_name)
        if not existing_role:
            await guild.create_role(name=role_name)
            print(f'Cargo {role_name} criado')

# Função para registrar logs no banco de dados
def log_role_change(user_id, user_name, role_name, action):
    c.execute('''
              INSERT INTO logs (user_id, user_name, role_name, action)
              VALUES (?, ?, ?, ?)
              ''', (user_id, user_name, role_name, action))
    conn.commit()

# Comando para escolher um cargo
@bot.command()
async def escolher(ctx, cargo: str):
    # Obtém o cargo pelo nome
    role = discord.utils.get(ctx.guild.roles, name=cargo)
    
    if role is None:
        await ctx.send(f'O cargo {cargo} não existe.')
        return

    # Adiciona ou remove o cargo do usuário conforme necessário
    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
        await ctx.send(f'O cargo {cargo} foi removido de você.')
        log_role_change(ctx.author.id, str(ctx.author), role.name, 'removed')
    else:
        await ctx.author.add_roles(role)
        await ctx.send(f'O cargo {cargo} foi atribuído a você.')
        log_role_change(ctx.author.id, str(ctx.author), role.name, 'added')

# Executa o bot
bot.run(TOKEN)


