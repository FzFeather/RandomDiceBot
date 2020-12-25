__arglist__ = {'傷害':'damage',\
               'Lv':'in_game_level',\
               'Combo':'combo'}

def __invoke__(arg):
	# 組合等級計算器(alpha)
	# damage 傷害
	# in_game_level 遊戲內等級
	# combo = 組合數
  damage = int(arg['damage'])
  in_game_level = int(arg['in_game_level'])
  combo = int(arg['combo'])
  combo_power = combo*(combo+1)/2
  # Subtract the effect of in_game_level and base attack
  damage -= 10 + combo_power * 8 +(combo_power + 10) * (in_game_level-1)
  level = 7 + damage / (combo_power * 2 + 10)
  level_str = '{:.2f}'.format(level)
  if level_str[-3:] == '.00':
    level_str = level_str[:-3]
  if level < 7:
    print('組合等級為不合理數值['+level_str+']')
  else:
    print('組合等級為'+level_str)
