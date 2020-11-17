from replit import db

db['組合傷害'] = {'funcname':'combo_damage', 'emoji':'💥',\
                 'description':'計算組合的單次傷害'}

db['農金幣'] = {'funcname':'achieve_coins_rank',\
               'emoji':'🤑',\
               'description':'算出需要到達多少層才能拿到金額'}


db['效率'] = {'funcname':'effectiveness_time_card',\
               'emoji':'<:398wave:692680055372906506>',\
               'description':'測農卡片的效率'}

db['組合等級'] = {'funcname':'combo_level', 'emoji':'🔢',\
                 'description':'計算組合的等級'}

db['暴風雪點數'] = {'funcname':'snow_level',\
               'emoji':'<:DiceBlizzard:692321221206867968>',\
               'description':'計算暴風雪滿緩速的點數(50%)[8秒]'}