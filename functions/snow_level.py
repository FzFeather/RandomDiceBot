__arglist__ = {'等級': 'level'}

def __invoke__(arg):
	level = int(arg["level"])
	for i in range(2,5):
	 point = round((50-i*4)/(5+0.5*(level-7))+0.5)
	 point_1 = round((50-(i-1)*4)/(5+0.5*(level-7))+0.5)
	 if point != point_1 or i == 2:
	  print(i, "顆共", round((50-i*4)/(5+0.5*(level-7))+0.5), "點")
	 if i == 4:
	  print("pvp不建議4顆或以上,pve不建議5顆或以上")
