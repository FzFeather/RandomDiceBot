import sys
import os
import contextlib
import traceback
import asyncio
import importlib
from replit import db
from io import StringIO
import math

buffered_users = {}
repeat_query = {}

@contextlib.contextmanager
def stdinIO(stdin=None):
    old_stdin, sys.stdin = sys.stdin, stdin
    yield stdin
    sys.stdin = old_stdin

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

async def exec_code(code, author, sender):

  r_exec, w_dc = os.pipe()
  exec_stdin = os.fdopen(r_exec, 'r')
  buffered_users[author.id] = os.fdopen(w_dc, 'w')

  with stdinIO(exec_stdin) as sin, stdoutIO() as sout:
    try:
      loop = asyncio.get_running_loop()
      await loop.run_in_executor(None, exec, code)
      # exec(code)
    except:
     await sender.send('Error:\n```\n'+trim_lines(traceback.format_exc(),(1,2))+'```')
    else:
      await sender.send('Output:\n```\n'+sout.getvalue()+'```')
  try:
    os.close(r_exec)
    os.close(w_dc)
  finally:
    buffered_users.pop(author.id, None)

def has_input_buffer(author_id):
  return (author_id in buffered_users.keys())

def write_buffer(author_id, msg):
  write_file = buffered_users[author_id]
  write_file.write(msg + '\n')
  write_file.flush()
    
def save_codes(name_def, codes):
  name, func_name = [s.strip(' ') for s in name_def.split('=')]
  db[name] = {'funcname':func_name, 'emoji':'', 'description':''}

  first_line = codes.find(']')
  func_arg = codes[1:first_line]
  arg_trans = {}
  for arg in func_arg.split(','):
    arg_pair = [a.strip(' ') for a in arg.split('=')]
    arg_trans[arg_pair[0]] = arg_pair[1]

  code_segment = codes[first_line+1:].strip(' `\n')
  if code_segment.startswith('python'):
    code_segment = code_segment[7:]
    
  filename = 'functions/' + func_name + '.py'
  try:
    with open(filename, 'w+') as f:
      f.write('__arglist__ = ' + str(arg_trans) +'\n\n')
      f.write('def __invoke__(arg):\n')
      for line in code_segment.split('\n'):
        f.write('\t' + line + '\n')
  except:
    success = False
  else:
    success = True
  return success

class InputException(Exception):
  pass

async def load_func(name, arg, sender):
  if name in db.keys():
    funcname = db[name]['funcname']
  else:
    return
  try:
    func = importlib.import_module('functions.'+funcname)
    func = importlib.reload(func)
    with stdoutIO() as s:
      try:
        func.__invoke__(arg_parser(arg, func.__arglist__))
      except (InputException, ValueError):
        error_msg = '輸入錯誤\n'
        error_msg += '格式：\n```?' + name + ' '
        error_msg += '=? '.join(func.__arglist__.keys())+'=?```'
        await sender.send(error_msg)
      except:
        await sender.send('Error:\n```\n'+trim_lines(traceback.format_exc(),(1,2))+'```')
      else:
        await sender.send('Output:\n```\n'+s.getvalue()+'```')
      
    
  except ImportError:
    await sender.send('程序不存在')

async def load_func_by_emoji(emoji, sender, questioner_id, bot):

  funcdetail = None
  for k in db.keys():
    if emoji == db[k]['emoji']:
      funcdetail = db[k]
      break
  if funcdetail == None:
    return
  funcname = funcdetail['funcname']
  try:
    func = importlib.import_module('functions.'+funcname)
    func = importlib.reload(func)
    arg = {}
    def check(m):
      return m.channel == sender and m.author.id == questioner_id
    names = func.__arglist__.keys()
    input_prompt = '> '+funcdetail['description'] + '\n'
    input_prompt += ', '.join([a+' = ?' for a in names])
    input_prompt += '   (請用逗號分隔)'
    await sender.send(input_prompt)
    msg = await bot.wait_for('message', check=check)
    content = msg.content.replace('，', ',').replace('﹐', ',')
    valid_char = '.1234567890+-*/ ()'
    for a in zip(names, content.split(',')):
      argvalue = a[1].strip(' ')
      for c in argvalue:
        if c not in valid_char:
          break
      else:
        try:
          argvalue = eval(argvalue, {'__buildins__':None})
        finally:
          pass
      arg[func.__arglist__[a[0]]] = argvalue
    
    err_msg = None
    with stdoutIO() as s:
      try:
        func.__invoke__(arg)
      except (InputException, ValueError, KeyError):
        error_msg = '輸入錯誤'
        reply = await sender.send(error_msg)
        err_msg = traceback.format_exc()
      except:
        reply = await sender.send('Error:\n```\n'+trim_lines(traceback.format_exc(),(1,2))+'```')
      else:
        reply = await sender.send('Output:\n```\n'+s.getvalue()+'```')
      finally:
        await reply.add_reaction(emoji)
        await reply.add_reaction('↩️')
    print(err_msg)

  except ImportError:
    await sender.send('程序不存在')

def arg_parser(arg_str, trans_dict):
  try:
    arg_str = '='.join([a.strip(' ') for a in arg_str.split('=')])
    arglist = arg_str.split(' ')
    args = {}
    for arg in arglist:
      arg_pair = [a.strip(' ') for a in arg.split('=')]
      args[trans_dict[arg_pair[0]]] = arg_pair[1]
  except:
    raise InputException
  return args


async def calc_result(code, sender):

  try:
    result = eval(code, {'math':math})
  except:
    await sender.send('Error:\n```\n'+trim_lines(traceback.format_exc(),(1,2))+'```')
  else:
    await sender.send('Output:\n```\n'+str(result)+'```')

def trim_lines(msg, index):
  lines = msg.split('\n')
  new_lines = ''
  for i in range(len(lines)):
    if not i in index:
      new_lines += lines[i] + '\n'
  return new_lines

def list_query():
  query_str = ''
  for k in db.keys():
    query_str += db[k]['emoji'] + ' - `?' + k + '` - ' + db[k]['description'] + '\n'
  return query_str

def func_emojis():
  return [db[k]['emoji'] for k in db.keys()]
