__arglist__ = {'等級':'level',\
               'Lv':'in_game_level',\
               'Combo':'combo'}

def __invoke__(arg):
	# 組合傷害計算器(alpha)
	# level 骰子等級（遊戲外）
	# in_game_level 遊戲內等級
	# combo = 組合數
  level = int(arg['level'])
  in_game_level = int(arg['in_game_level'])
  combo = int(arg['combo'])
  damage = combo*(combo-1)/2*(8+(level-7)*2+(in_game_level-1)*1)+(level-6+in_game_level-1)*10
  print('組合傷害為'+str(damage))
