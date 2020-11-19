__arglist__ = {'等級': 'rank', '金幣': 'coins'}

def __invoke__(arg):
	import math
	Numberofcoinneeded = int(arg['coins'])
	Rank = int(arg['rank'])
	if not 1 <= Rank <= 20:
		print('輸入錯誤：等級必須為1~20!')
		return
	Coinslevel = [320, 432, 544, 640, 736, 832, 925, 1024, 1120, 1312, 1408, 1504, 1594, 1687, 1775, 1866, 1951, 2044, 2133, 2222]
	coins = int(Coinslevel[Rank-1])
	for i in range(10):
		level = math.ceil(math.ceil(Numberofcoinneeded/coins)*40/(i+1))
		if level <= 56:
			n = 0
			while n==0:
				if level%8 == 0:
					level = level/8*5
					n = 1
				elif level%4 == 0:
					level = round(level/8+0.01)*5-2
					n = 1
				elif (level-1)%4 == 0:
					level = round(level/8+0.01)*5-1
					n = 1
				elif (level-2)%8 == 0:
					level = round(level/8)*5+2
					n = 1
				else:
					level += 1
		elif level > 56 :
			level -= 56
			k = 0
			while k == 0:
				if level%8 == 0:
					level = level/4+35
					k = 1
				elif (level-2)%8 == 0:
					level = (level-2)/4+36
					k = 1
				else:
					level += 1
		print("你必須到達", level,"層",(i+1),"次")
		if level <= 10:
			break
