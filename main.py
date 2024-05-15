import asyncio
from dotenv import load_dotenv
import json
import os

import discord


load_dotenv()

data = {
  'prefix': '^',
  'verify_channel': 1168539275298619513,
  'verify_role': 1240386768541454436,
  'verify_password': 'hshhome',
}

def save_data():
  with open('data.json', 'w') as f:
    json.dump(data, f)

try:
  with open('data.json') as f:
    data.update(**json.load(f))
except FileNotFoundError:
  save_data()

async def adminhelp_command(message: discord.Message, args: str):
  await message.channel.send(f'Admin commands: `{", ".join(admin_commands)}`')

async def prefix_command(message: discord.Message, args: str):
  if len(args) == 1:
    data['prefix'] = args
    save_data()
    await message.channel.send(f'Command prefix changed to `{args}`')
  else:
    await message.channel.send(f'Command prefix: `{data["prefix"]}`')

async def verifychannel_command(message: discord.Message, args: str):
  if args.isnumeric() and len(args) >= 16:
    data['verify_channel'] = args
    save_data()
    await message.channel.send(f'Verify channel ID changed to `{args}`')
  elif args == '':
    await message.channel.send(f'Verify channel ID: `{data["verify_channel"]}`')
  else:
    await message.channel.send('Invalid channel ID')

async def verifyrole_command(message: discord.Message, args: str):
  if args.isnumeric() and len(args) >= 16:
    data['verify_role'] = args
    save_data()
    await message.channel.send(f'Verify role ID changed to `{args}`')
  elif args == '':
    await message.channel.send(f'Verify role ID: `{data["verify_role"]}`')
  else:
    await message.channel.send('Invalid role ID')

async def verifypassword_command(message: discord.Message, args: str):
  password = args.replace(' ', '').lower()
  if len(password) >= 6:
    data['verify_password'] = password
    save_data()
    await message.channel.send(f'Verify password changed to `{password}`')
  elif args == '':
    await message.channel.send(f'Verify password: `{data["verify_password"]}`')
  else:
    await message.channel.send('Password must be at least 6 characters long (spaces not included)')

admin_commands = {
  'adminhelp': adminhelp_command,
  'prefix': prefix_command,
  'verifyrole': verifyrole_command,
  'verifychannel': verifychannel_command,
  'verifypassword': verifypassword_command,
}

async def help_command(message: discord.Message, args: str):
  await message.channel.send(f'Commands: `{", ".join(commands)}`')

commands = {
  'help': help_command,
}

class Bot(discord.Client):
  def __init__(self, intents):
    super().__init__(intents=intents)

  async def on_message(self, message: discord.Message):
    if message.channel.id == data['verify_channel']:
      password = message.content.replace(' ', '').lower()
      if password == data['verify_password']:
        await message.author.add_roles(message.guild.get_role(data['verify_role']))
      await message.delete()
    else:
      pre_post = message.content.split(data['prefix'], 1)
      if len(pre_post) == 2 and pre_post[0] == '':
        cmd_args = pre_post[1].split(None, 1)
        if message.author.guild_permissions.administrator and cmd_args[0] in admin_commands:
          admin_commands[cmd_args[0]](message, (cmd_args[1:] or [''])[0])
        elif cmd_args[0] in commands:
          commands[cmd_args[0]](message, (cmd_args[1:] or [''])[0])

bot = Bot(discord.Intents.all())
bot.run(os.getenv('token'))