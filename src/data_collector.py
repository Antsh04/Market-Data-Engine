import aiohttp as ah
import json as js
import asyncio as aio
import time


async def fetch_data(session,symbol, interval, limit):
    url1 = "https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        async with session.get(url1, params=params) as response:

            if response.status == 200:
                data = await response.json()
                normalized_data=[]

                for row in data:
                    record={
                            "symbol":symbol,
                            "open_time": int(row[0]/1000),
                            "open": float(row[1]),
                            "high": float(row[2]),
                            "low": float(row[3]),
                            "close": float(row[4]),
                            "volume": float(row[5]),
                    }
                    normalized_data.append(record)
                return normalized_data

            else:
                print(f"Error for {symbol}")
                return None


    except ah.ContentTypeError:
        print(f"EClient Error for {symbol}")
        return None
    except Exception as e:
            print(e)


async def save_data(files):
    with open("data.jsonl" ,"w", newline="",) as f:

        for row in files:
            f.write(js.dumps(row)+"\n")



async def main():
    start_time=time.time()




    async with ah.ClientSession() as session:
        results = await aio.gather(
            fetch_data(session,"BTCUSDT", "1m", 10),
            fetch_data(session,"ETHUSDT", "1m", 10),
            fetch_data(session,"BNBUSDT", "1m", 10),
            fetch_data(session, "SOLUSDT", "1m", 10),
            fetch_data(session, "ADAUSDT", "1m", 10),
            fetch_data(session, "wrong", "1m", 10)
        )


        data_to_save=[item for sublist in results if sublist is not None for item in sublist]

        await save_data(data_to_save)

    end_time=time.time()
    print(f"Process completed in : {end_time-start_time:.5f} seconds")

if __name__ == "__main__":
    aio.run(main())