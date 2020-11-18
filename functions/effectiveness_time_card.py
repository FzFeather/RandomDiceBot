__arglist__ = {'2選1:(關數請寫1,卡片數請寫2)': 'x', '其數量': 'card', '時間': 'time'}

def __invoke__(arg):
	Time = float(arg["time"])
	Card = int(arg["card"])
	Choice = int(arg["x"])
	if Choice==1 and Card>=36:
	  Card = (Card-35)*6+35
	Cardpertime = float(Card/Time)
	print("平均每分鐘獲得的卡片數量 : ", Cardpertime)
	if Cardpertime <= 4:
	  print("沒有效率!")
	elif Cardpertime >= 4 and Cardpertime <= 5:
	  print("還可以")
	else:
	  print("有效率!!!")
