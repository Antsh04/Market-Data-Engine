import aiohttp as ah
import csv as cs
import asyncio as aio

async def fetch_data(session,symbol, interval, limit):
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    try:
        async with session.get("https://api.binance.com/api/v3/klines", params=params) as response:

            if response.status == 200:
                data = await response.json()
                return [row + [symbol] for row in data]
            else:
                return None
    except Exception as e:
            print(e)


async def save_data(files):
    with open("data.csv" ,"w", newline="",) as f:
        writer=cs.writer(f,)
        writer.writerow(["open_time", "open", "high", "low", "close", "volume", "close_time", "symbol"])


        for row in files:
            writer.writerow(row)



async def main():

    async with ah.ClientSession() as session:
        results = await aio.gather(
            fetch_data(session,"BTCUSDT", "1m", 1000),
            fetch_data(session,"ETHUSDT", "1m", 1000),
            fetch_data(session,"BNBUSDT", "1m", 1000)
        )



        data_to_save=[item for sublist in results if sublist is not None for item in sublist]

        await save_data(data_to_save)


if __name__ == "__main__":
    aio.run(main())