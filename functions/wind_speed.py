__arglist__ = {'風等級':'wind_level',\
               '強風等級':'mwind_level'}

def __invoke__(arg):
  wind_level = int(arg["wind_level"])
  mwind_level = int(arg["mwind_level"])

  wind_acc = 10 + (wind_level - 1) * 2 + 10 * 4
  wind_period = 0.45*(1 - wind_acc/100)
  wind_speed = 1/wind_period

  mwind_bufftime = 3 + (mwind_level-5) * 0.3 + 4 * 0.3
  mwind_speed = (mwind_bufftime/0.1+7/0.6)/(mwind_bufftime + 7)

  typhoon_speed = (6/0.6 + 5/0.1)/11

  print('風平均速度為: {0:.2f}下/秒, 強風平均速度為: {1:.2f}下/秒, 颱風平均速度為: {2:.2f}下/秒'.format(wind_speed, mwind_speed, typhoon_speed))

