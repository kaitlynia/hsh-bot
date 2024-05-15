import asyncio
from dotenv import load_dotenv
import json
import os

import discord


load_dotenv()

data = {
  'verify_channel': 1168539275298619513,
  'verify_password': 'hshhome',
  'verify_role': 1240386768541454436
}

try:
  with open('data.json') as f:
    data.update(**json.load(f))
except FileNotFoundError:
  with open('data.json', 'w') as f:
    json.dump(data, f)


class Bot(discord.Client):
  def __init__(self, intents):
    super().__init__(intents=intents)

  async def on_message(self, message: discord.Message):
    if message.channel.id == data['verify_channel']:
      password = message.content.replace(' ', '').lower()
      if password == data['verify_password']:
        await message.author.add_roles(message.guild.get_role(data['verify_role']))
      await message.delete()

bot = Bot(discord.Intents.all())
bot.run(os.getenv('token'))