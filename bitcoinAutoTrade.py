import time
import selectCocde
import pandas as pd
import pyupbit
import datetime

access = "KgllxJAgoxZKIDneomxhxim0sCOrnbI5l5xAEx1e"          # 본인 값으로 변경
secret = "C7ej5kSoYrxyE75BAFB7ai64F3PqIFR2vinzy7B7"          # 본인 값으로 변경

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b["currency"] == ticker:
            if b["balance"] is not None:
                return float(b["balance"])
            else:
                return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("AutoTrade Start")

def get_list():
    return  pd.read_csv("./today_list.csv")



# 자동매매 시작
while True:
    try:
        for k in range(0,5):
            pd_list = get_list()
            coinCodeK = pd_list.iloc[k][1]
            #print(coinCodeK)
            coinCode = pd_list.iloc[k][1].replace("KRW-","")
            now = datetime.datetime.now()
            start_time = get_start_time(coinCodeK)
            end_time = start_time + datetime.timedelta(days=1)

            if now.replace(hour=9, minute=0, second=0, microsecond=0) <= now <= now.replace(hour=9, minute=10, second=0, microsecond=0):
                time.sleep(600)
                selectCocde.selectCode()
                print("Select code pass")
            elif start_time < now < end_time - datetime.timedelta(seconds=60):
                target_price = get_target_price(coinCodeK, 0.4)

                current_price = get_current_price(coinCodeK)
                if target_price < current_price:
                    krw = get_balance("KRW")
                    if krw > 5000 and get_balance(coinCode) < 0.00001 :
                        upbit.buy_market_order(coinCodeK, 500000)

            else:
                btc = get_balance(coinCode)
                if btc > 0.00008:
                    upbit.sell_market_order(coinCodeK, btc)

            btc = get_balance(coinCode)
            print(coinCodeK ,": ", now, ", target : ", target_price,  " ,price : ", get_current_price(coinCodeK),", my balance : ", btc)
            time.sleep(2)

    except Exception as e:
        print(e)
        time.sleep(2)
