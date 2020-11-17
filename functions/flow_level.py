__arglist__ = {'等級': 'level'}

def __invoke__(arg):
	level = int(arg["level"])
	for i in range(2,6):
	 point = round((40-i*2)/(2+0.3*(level-7))+0.5)
	 point_1 = round((40-(i-1)*2)/(2+0.3*(level-7))+0.5)
	 if point != point_1 or i == 2:
	  print(i, "顆共", point, "點")
	 if i == 5:
	  print("pve不建議5顆或以上")
