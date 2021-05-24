import requests
import json
import pandas as pd
import time
from bs4 import BeautifulSoup

def run_query(query):  # A simple function to use requests.post to make the API call.
    headers = {'X-API-KEY': 'BQYCJJ4NwnOPwVPLfvuoNiQyTzHjHFSi'}
    request = requests.post('https://graphql.bitquery.io/',
                            json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception('Query failed and return code is {}.      {}'.format(request.status_code,
                                                                             query))


# The GraphQL query

query = """
        {
        ethereum {
            dexTrades(options: {asc: ["date.date"]}, date: {since: "2021-05-01"}) {
            tradeAmount(in: USD)
            date {
                date
            }
            }
        }
        }
        """
def copy_create_arrray(data):
    global all_data
    temp = []
    temp.append(data)
    for dt in all_data:
        temp.append(dt)
    all_data=[]
    all_data=temp


def inner_extract(link,name):
    global all_data
    platfrom = ['Sushiswap','PancakeSwap (v2)','Uniswap (v2)']

    url = ('https://www.coingecko.com'+link+'#markets')

    soup1 = BeautifulSoup(requests.get(url).content)

    rows = soup1.find('table',{'data-target':'gecko-table.table'}).find_all('tr')

    for row in rows[3:]:
        td = row.find_all('td')
        temp = [str(i.text).replace('\n','') for i in td]
        if temp[1] in platfrom:
            data = []
            data.append(str(name).replace('\n',''))
            data.append(temp[1])
            data.append(str(td[2].find('a').text).replace('\n',''))
            data.append(temp[3])
            all_data.append(data)

def inner_extract_monitor(link,name):
    global all_data
    platfrom = ['Sushiswap','PancakeSwap (v2)','Uniswap (v2)']

    url = ('https://www.coingecko.com'+link+'#markets')

    soup1 = BeautifulSoup(requests.get(url).content)

    rows = soup1.find('table',{'data-target':'gecko-table.table'}).find_all('tr')

    for row in rows[3:]:
        td = row.find_all('td')
        temp = [str(i.text).replace('\n','') for i in td]
        if temp[1] in platfrom:
            data = []
            data.append(str(name).replace('\n',''))
            data.append(temp[1])
            data.append(str(td[2].find('a').text).replace('\n',''))
            data.append(temp[3])
            copy_create_arrray(data)


def monitor_():
    global all_coin
    soup = BeautifulSoup(requests.get('https://www.coingecko.com/en/coins/recently_added').content)

    coains = soup.find_all('a',{'class':'d-lg-none'})
    for coin in coains:
        if str(coin.text).replace('\n','').strip().lower() not in all_coin:
            all_coin.append(str(coin.text).replace('\n','').strip().lower())
            inner_extract_monitor(coin['href'],coin.text)


def monitor():
    global all_coin
    soup = BeautifulSoup(requests.get('https://www.coingecko.com/en/coins/recently_added').content)

    coains = soup.find_all('a',{'class':'d-lg-none'})
    for coin in coains:
        if str(coin.text).replace('\n','').strip().lower() not in all_coin:
            all_coin.append(str(coin.text).replace('\n','').strip().lower())
            inner_extract(coin['href'],coin.text)

if __name__ == '__main__':
    all_coin = []
    all_data = []
    column = ['Symbol','Market','Pair',"price"]
    platfrom = ['Sushiswap','PancakeSwap (v2)','Uniswap (v2)']

    monitor()
    df = pd.DataFrame(all_data)
    df.to_csv('All Data.csv')
    while True:
        monitor_()
        df = pd.DataFrame(all_data)
        df.to_csv('All Data.csv')
        time.sleep(60*5)



