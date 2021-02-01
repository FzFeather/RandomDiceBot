__arglist__ = {'暴擊傷害%':'crit_dmg', '骰子等級 Eg. C13;M9;T9':'dice_classes', '骰子星級/顆數 Eg. C7+M7+5T':'dice_setup'}

# Heading
## T/M/C/L/H/S 0 : Level of dice

# Content
## 0T : 0 * Time dice
## M0 : 0 Star Moon Dice
## Md0 : 0 Star Moon Dice (Disabled)
## C0 : 0 Star Critical 
## S0 : 0 Star Scope dice
########
# Not available
## L0 : 0 Star Light dice
## H : Hacked
## Sk : Skin
### P : Pantheon
### V : Club Violet
### D : Default

import re

class Buff:

  def __init__(self):
    self.self_speed_buff = 0
    self.opp_speed_buff = 0
    self.crit_buff = 0
    self.dmg_buff = 0
    self.extra_target_buff = 0
  def __add__(self, other):
    total_buff = Buff()
    total_buff.self_speed_buff = self.self_speed_buff+other.self_speed_buff
    total_buff.opp_speed_buff = self.opp_speed_buff + other.opp_speed_buff
    total_buff.crit_buff = self.crit_buff + other.crit_buff
    total_buff.dmg_buff = self.dmg_buff + other.dmg_buff
    total_buff.extra_target_buff = self.extra_target_buff + other.extra_target_buff
    return total_buff

  def buff_value(self):
    result = '己方速度加乘: ' + str(self.self_speed_buff) + '%\t'
    result += '對手速度加乘: ' + str(self.opp_speed_buff) + '%\t'
    result += '爆擊加乘: ' + str(self.crit_buff) + '%\t'
    result += '傷害加乘: ' + str(self.dmg_buff) + '%\t'
    result += '額外目標加乘: ' + str(self.extra_target_buff) + '%\t'
    return result
  
  def buff_multiple(self, crit_dmg):
    MAX_BUFF = 100-10/7
    if self.self_speed_buff > MAX_BUFF:
      self.self_speed_buff = MAX_BUFF
    if self.opp_speed_buff > MAX_BUFF:
      self.opp_speed_buff = MAX_BUFF
    if self.crit_buff > 100:
      self.crit_buff = 100
    speed_mult = 1/(1-self.self_speed_buff/100)*1/(1-self.opp_speed_buff/100)
    crit_rate = min((self.crit_buff+5)/100, 1)
    basic_crit_buff = 0.05 * crit_dmg/100 + 0.95
    crit_mult = (crit_rate * crit_dmg/100 + (1-crit_rate)) / basic_crit_buff
    dmg_mult = 1+self.dmg_buff/100
    extra_target_mult = 1 + self.extra_target_buff/100 * crit_dmg/100;
    result = '速度增益倍率: {0:.2f}\t'.format(speed_mult)
    result += '爆擊增益倍率: {0:.2f}\t'.format(crit_mult)
    result += '傷害增益倍率: {0:.2f}\n'.format(dmg_mult)
    result += '額外目標增益倍率: {0:.2f}\n'.format(extra_target_mult)
    result += '總增益倍率: {0:.2f}[非太陽]\t'.format(speed_mult * crit_mult * dmg_mult * extra_target_mult)
    annot = "(2王)" if self.extra_target_buff > 0 else ""
    result += ('{0:.2f}[太陽'+annot+']').format(speed_mult ** 2 * crit_mult * dmg_mult * (1+(extra_target_mult-1)*2))
    return result

def time_buff_fn(level):
  def time_buff():
    buff = Buff()
    buff.opp_speed_buff = 2 + 2 * 4 + 1 * (level-7)
    return buff
  return time_buff

def moon_buff_fn(level, enabled = True):
  def moon_buff(pips):
    buff = Buff()
    buff.self_speed_buff = (7 + 1 * (level-7)) * pips + 2 * 4
    if enabled:
      buff.self_speed_buff += 3
      buff.crit_buff = 5 * pips
      buff.dmg_buff = 10 * pips
    return buff
  return moon_buff

def crit_buff_fn(level):
  def crit_buff(pips):
    buff = Buff()
    buff.crit_buff = (8 + 0.2 * (level-3)) * pips + 1 * 4
    return buff
  return crit_buff

def scope_buff_fn(level):
  def scope_buff(pips):
    buff = Buff()
    buff.extra_target_buff = 9 + 3 * (level - 7) + 2 * pips;
    return buff;
  return scope_buff;

def __invoke__(arg):
  crit_dmg = int(arg['crit_dmg'])
  lvls = arg['dice_classes']
  content = arg['dice_setup']
  levels = {}
  for l in lvls.split(';'):
    dice, level = re.findall(r'(\w+?)(\d+)', l)[0]
    levels[dice] = int(level)

  buff_fn = {}
  if 'M' in levels:
    buff_fn['M'] = moon_buff_fn(levels['M'])
    buff_fn['Md'] = moon_buff_fn(levels['M'], False)
  if 'T' in levels:
    buff_fn['T'] = time_buff_fn(levels['T'])
  if 'C' in levels:
    buff_fn['C'] = crit_buff_fn(levels['C'])
  if 'S' in levels:
    buff_fn['S'] = scope_buff_fn(levels['S'])

  translation = {
    'C':'暴擊', 'T':'時間', 'M':'月亮', 'Md':'月亮(熄滅)', 'S':'狙擊鏡'
  }

  buffs = content.split('+')
  all_buffs = Buff()
  configs = []
  for b in buffs:
    if '0' <= b[0] <= '9':
      name = b[-1]
      value = int(b[:-1])
      if name == 'T':
        buff = buff_fn['T']()
        buff.opp_speed_buff *= value
      configs.append(str(value) + '顆' + translation[name])
    else:
      name = b[:-1]
      value = int(b[-1])
      buff = buff_fn[name](value)
      configs.append(str(value) + '星' + translation[name])
    all_buffs = all_buffs + buff
  
  prompt = '暴擊傷害:' + str(crit_dmg) + '%;\t'
  for d in levels.keys():
    prompt += translation[d] + ':' + str(levels[d]) + '級 '
  print(prompt)
  print('設置: ' + '+'.join(configs))
  print('（以下數字僅供參考）')
  print(all_buffs.buff_value())
  print(all_buffs.buff_multiple(crit_dmg))
