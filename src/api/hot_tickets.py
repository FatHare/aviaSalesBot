import requests
from datetime import datetime

from .exceptions import TicketCodeError

def get_russian_hot_ticket_offers(from_) -> list[dict]:
    hot_tickets = get_russian_hot_tickets(from_=from_)
    if not hot_tickets.get('offers'):
        return []

    name_city_by_code = get_name_city_by_code(hot_tickets['cities'])
    offers = formatting_offers(hot_tickets['offers'])
    for offer in offers:
        offer['destination_name'] = name_city_by_code.get(offer['destination'], {}).get('su')

    offers.sort(key=lambda dictionary: dictionary['value'])
        
    return offers


def get_russian_hot_tickets(from_) -> dict:

    headers = {
        'authority': 'ariadne.aviasales.ru',
        'accept': '*/*',
        'accept-language': 'en-RU,en;q=0.9,ru-RU;q=0.8,ru;q=0.7,en-GB;q=0.6,en-US;q=0.5',
        'content-type': 'application/json',
        'origin': 'https://www.aviasales.ru',
        'referer': 'https://www.aviasales.ru/',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
        'x-auid': 'CmofQ2RXYZsdsQAfCaFRAg==',
        'x-user-platform': 'web',
    }

    json_data = {
        'query': '\n  query MainContentQuery($brand: Brand!, $locales: [String!], $input: MainPageBlocksV1Input!) {\n    main_page_blocks_v1(input: $input, brand: $brand) {\n      blocks {\n        __typename\n\n        ... on ContentlessBlock {\n          type\n        }\n\n        ... on CityPOIsBlock {\n          city {\n            main_tag(filters: { locales: $locales })\n            entity {\n              iata\n            }\n          }\n          pois {\n            entity {\n              ark_id\n            }\n          }\n        }\n\n        ... on CityPOIBlock {\n          city {\n            main_tag(filters: { locales: $locales })\n            entity {\n              iata\n            }\n          }\n          poi {\n            entity {\n              ark_id\n            }\n          }\n        }\n\n        ... on POICompilationBlock {\n          ark_id\n        }\n\n        ... on CityPOICollectionBlock {\n          city {\n            entity {\n              iata\n            }\n          }\n          pois {\n            entity {\n              ark_id\n            }\n          }\n        }\n\n        ... on NationalParksCollectionBlock {\n          parks {\n            entity {\n              ark_id\n            }\n          }\n        }\n\n        ... on NationalParkPOIBlock {\n          park {\n            entity {\n              ark_id\n            }\n          }\n          poi {\n            entity {\n              ark_id\n            }\n          }\n        }\n\n        ... on LocationsCompilationBlock {\n          title\n          locations {\n            entity {\n              ark_id\n            }\n          }\n        }\n\n        ... on HotTicketsBlock {\n          offers {\n            price {\n              ...priceFields\n            }\n            old_price {\n              value\n            }\n          }\n          cities {\n            ...citiesFields\n          }\n          airlines {\n            ...airlinesFields\n          }\n          airports {\n            ...airportsFields\n          }\n        }\n      }\n    }\n  }\n\n  \nfragment priceFields on Price {\n  depart_date\n  return_date\n  value\n  cashback\n  found_at\n  signature\n  ticket_link\n  currency\n  convenient\n  provider\n  segments {\n    transfers {\n      duration_seconds\n      country_code\n      visa_required\n      night_transfer\n      at\n      to\n      tags\n    }\n    flight_legs {\n      origin\n      destination\n      local_depart_date\n      local_depart_time\n      local_arrival_date\n      local_arrival_time\n      flight_number\n      operating_carrier\n      aircraft_code\n      technical_stops\n      equipment_type\n      duration_seconds\n    }\n  }\n}\n\n  \nfragment airlinesFields on Airline {\n  iata\n  translations(filters: {locales: $locales})\n}\n  \nfragment citiesFields on CityInfo {\n  city{\n    iata\n    translations(filters: {locales: $locales})\n  }\n}\n  \nfragment airportsFields on Airport {\n  iata\n  translations(filters: {locales: $locales})\n  city {\n    iata\n    translations(filters: {locales: $locales})\n  }\n}\n',
        'variables': {
            'brand': 'AS',
            'locales': [
                'ru',
            ],
            'input': {
                'auid': 'CmofQ2RXYZsdsQAfCaFRAg==',
                'market': 'ru',
                'origin': from_,
                'currency': 'rub',
                'trip_class': 'Y',
                'passport_country': 'RU',
                'language': 'ru',
                'application': 'selene',
                'poi_compilation_limit': 10,
            },
        },
        'operation_name': 'main_page_blocks_v1',
    }

    response = requests.post('https://ariadne.aviasales.ru/api/gql', headers=headers, json=json_data)

    if response.status_code != 200:
        raise ConnectionError('Не удалось получить горячие билеты')
    
    response_json = response.json()
    if not response_json['data']:
        raise TicketCodeError('Не верный код города отправления.')
    
    return response_json['data']['main_page_blocks_v1']['blocks'][0]


def formatting_offers(data):

    offers = []
    for offer in data:
         flight_legs = offer['price']['segments'][0]['flight_legs']
         offers.append({
            'value': offer['price']['value'],
            'old_value': offer['old_price']['value'],
            'ticket_link': offer['price']['ticket_link'],
            'destination': flight_legs[-1]['destination'],
            'local_depart_date': datetime.strptime(
                f"""{flight_legs[0]['local_depart_date']} {flight_legs[0]['local_depart_time']}""",
                '%Y-%m-%d %H:%M'
            ),
            'local_arrival_date': datetime.strptime(
                f"""{flight_legs[-1]['local_arrival_date']} {flight_legs[-1]['local_arrival_time']}""",
                '%Y-%m-%d %H:%M'
            ),
        })

    return offers


def get_name_city_by_code(data_cities: list[dict]) -> dict:
    data = {'SVO': {'su': 'Москва'}}
    data.update({item['city']['iata']: item['city']['translations']['ru'] for item in data_cities})
    return data