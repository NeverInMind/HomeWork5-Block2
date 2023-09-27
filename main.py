import platform
import sys
import aiohttp
import asyncio
import datetime
from pydash import py_


def work_with_data(result: dict):
    result_dict = {}
    date = result.get('date')
    result_dict[date] = {}
    data = result.get('exchangeRate')
    cur_arr = ['EUR', 'USD']
    for i in cur_arr:
        test = py_.find(data, lambda value: value['currency'] == i )
        result_dict[date][i] = {'purchaseRate': test['purchaseRate'], 'saleRate': test['saleRate']}
    return result_dict
    


async def main():
    if isinstance(sys.argv[1], int):
        return 'Argument is not integer'
    if int(sys.argv[1]) > 10:
        return 'Too many days picked'
    result_arr = []
    for i in range(0, int(sys.argv[1])):
        filter_date = (datetime.datetime.now() - datetime.timedelta(days=float(i))).strftime('%d.%m.%Y')
        async with aiohttp.ClientSession() as session:
            async with session.get(f'https://api.privatbank.ua/p24api/exchange_rates?date={filter_date}') as response:
                print("Status:", response.status)
                if response.status == 200:
                    print("Content-type:", response.headers['content-type'])
                    print('Cookies: ', response.cookies)
                    print(response.ok)
                    result = await response.json()
                    test = work_with_data(result)
                    result_arr.append(test)
                else:
                    print(f"Error status: {response.status} for current request")
    print(result_arr)

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main())
    print(r)