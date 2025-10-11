

import requests as re
import csv as cs

def fetch_dat(symbol , interval , limit):
    url = "https://api.binance.com/api/v3/klines"
    parameters = {"symbol": symbol, "interval": interval, "limit": limit}
    data= re.get(url, params=parameters, timeout=10)
    return data.json()

def save_data(files):
    with open("data.csv","w") as f:
        writer=cs.writer(f)
        writer.writerow(["open_time", "open", "high","low","close","volume","close_time"])
        for row in files:
            writer.writerow([row[0], row[1], row[2], row[3], row[4], row[5], row[6]])




if __name__ == "__main__":
    save_data(fetch_dat("BTCUSDT","1m",10))
    print("Done")










