import pandas as pd
import requests

def get_table_aviasales(from_, to_) -> pd.DataFrame:

    headers = {
        'authority': 'lyssa.aviasales.ru',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-RU,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'origin': 'https://www.aviasales.ru',
        'referer': 'https://www.aviasales.ru/',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    temp_url = 'https://lyssa.aviasales.ru/date_picker_prices?currency=rub&depart_months[]=2023-07-01&depart_months[]=2023-08-01&depart_months[]=2023-09-01&destination_iata={to_}&market=ru&one_way=true&origin_iata={from_}'

    response = requests.get(
        temp_url.format(from_=from_, to_=to_),
        headers=headers,
    )

    if response.status_code != 200:
        raise ConnectionError('Не удалось получить данные')
    
    return pd.DataFrame(data=response.json()["prices"])