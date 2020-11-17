import os

import discord
from discord.ext.commands import Bot
from interpreter import *
from keep_alive import keep_alive
import random

my_bot = Bot(command_prefix=('!', '?'))

__icon__ = '<:733931336175321119:766154394949255219>'

@my_bot.event
async def on_connect():
  game = discord.Game("!helper")
  await my_bot.change_presence(activity=game)

@my_bot.event
async def on_message(message):
  if has_input_buffer(message.author.id):
    try:
      write_buffer(message.author.id, message.content)
    except IOError:
      await message.channel.send('你對我做甚麼了😞，把你上一次成功時send的東西@一下Fz')

  if message.content.startswith('!'):
    await on_command(message)
  
  if message.content.startswith('?'):
    await on_query(message)

@my_bot.event
async def on_reaction_add(reaction, user):
  if user.id == 766159529788309524 or reaction.message.author.id != 766159529788309524:
    return
  print(str(reaction.emoji))
  if str(reaction.emoji) == '↩️':
    await call_helper(reaction.message.channel)
  else:
    await load_func_by_emoji(str(reaction.emoji), reaction.message.channel, user.id, my_bot)
  # await reaction.message.edit(content=str(reaction.emoji))

async def on_command(message):
  sender = message.channel
  cmd_type, content = extract_command(message.content)
  if cmd_type == '!run_python':
    if is_admin(message.author):
      content = content.strip('`')
      if content.startswith('python'):
        content = content[7:]
      await exec_code(content, message.author, sender)
  elif cmd_type == '!save_python':
    if is_admin(message.author):
      funcname, content = extract_command(content)
      res = save_codes(funcname, content)
      await message.channel.send("Success" if res else "Failure")
  elif cmd_type == '!calc':
    if is_admin(message.author):
      content = content.strip('`')
      if content.startswith('python'):
        content = content[7:]
      await calc_result(content, sender)
  elif cmd_type == '!check_role':
    print(is_admin(message.author))
  elif cmd_type == '!check_alive':
    await message.channel.send("I'm alive")
  elif cmd_type == '!show_func':
    await message.channel.send('\n'.join((pyfile for pyfile in os.listdir('functions') if pyfile.endswith('.py'))))
  elif cmd_type == '!print_func':
    if not content.endswith('.py'):
      content += '.py'
    try:
      code = '```python\n' 
      with open('functions/'+content) as f:
        for line in f.readlines()[3:]:
          code += line.lstrip('\t')
        code += '```'
        await message.channel.send(code)
    except:
      message.channel.send('No such function!')
  elif cmd_type == '!get_track':
    print(message)
    print(message.content)
  elif cmd_type == '!helper' or cmd_type == '!help#randomdice':
    await call_helper(sender)
  elif cmd_type == '!toss':
    choice = content.split(' ')
    result = choice[random.randint(0, len(choice)-1)]
    await message.channel.send(result+'！')
  elif cmd_type == '!test_selector':
    msg = await message.channel.send('目前為選項A')
    await msg.add_reaction('🅰️')
    await msg.add_reaction('🎴')

async def call_helper(sender):
  help_embed = discord.Embed(title = '歡迎召喚小mmm的小Rd '+__icon__, colour = 0x7ca84a)
  help_embed.add_field(name='技能', value=list_query())
  help_embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/766154394949255219.png?v=1')
  help_embed.set_footer(text = 'by @FzFeather#1154, @小mmm#2411')
  sended_msg = await sender.send('', embed = help_embed)
  for e in func_emojis():
    await sended_msg.add_reaction(e)

async def on_query(message):
  func, args = extract_command(message.content)
  func = func[1:]
  await load_func(func, args, message.channel)

def is_admin(member):
  if member.id == 689907863673372732:
    return True
  if hasattr(member, 'roles'):
    for r in member.roles:
      if r.id == 692194086068944926:
        return True
  return False

def extract_command(msg):
  spacing = msg.find(' ')
  nline = msg.find('\n')

  split_pos = -1
  if spacing != -1 and nline != -1:
    split_pos = min(spacing, nline)
  else:
    split_pos = max(spacing, nline)
  
  if split_pos != -1:
    return(msg[:split_pos], msg[split_pos+1:].lstrip(' \n'))
  else:
    return (msg, None)

keep_alive()
token = os.environ.get("BOT_TOKEN")
my_bot.run(token)
