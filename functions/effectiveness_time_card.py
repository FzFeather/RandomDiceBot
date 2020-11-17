__arglist__ = {'1, 關卡數 = ?, 時間': 'x', '\n2, 卡片數量': 'card', '時間': 'time'}

def __invoke__(arg):
	Time = float(arg["time"])
	Card = int(arg["card"])
	Choice = int(arg["x"])
	if Choice==1 and Card>=60:
	  Card = (Card-60)*3+60
	Cardpertime = float(Card/Time)
	print("平均每分鐘獲得的卡片數量 : ", Cardpertime)
	if Cardpertime <= 4:
	  print("沒有效率!")
	elif Cardpertime >= 4 and Cardpertime <= 5:
	  print("還可以")
	else:
	  print("有效率!!!")
