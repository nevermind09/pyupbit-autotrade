import time
import pyupbit
import datetime
import pandas as pd

allcode = pyupbit.get_tickers(fiat="KRW")

todaylist =[]*len(allcode)

for c in allcode:
    i=0
    print(c)
    dfTemp = pyupbit.get_ohlcv(c, count=2)
    t0amount = dfTemp.iloc[0][4] * (dfTemp.iloc[0][1] + dfTemp.iloc[0][2]) / 2
    todaylist.append([c, t0amount])
    print(todaylist)
    print(dfTemp, "\n\n\n\n\n\n")

    time.sleep(0.3)
    i = i+1


col_name = ['code', 'am']
list_df = pd.DataFrame(todaylist, columns=col_name)
list_df=list_df.sort_values(by=['am'], ascending=False)
print(list_df.head(5))

list_df.to_csv("today_list.csv")

print(dfTemp)

print(dfTemp)