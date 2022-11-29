from prettytable import PrettyTable
from urllib.request import urlopen
import json
import statistics


def parse_json() -> dict:
    """

    """
    coins_data = {}

    coins = [
        'ALB',
        'BHA',
        'CAS',
        'DUB',
        'ELG',
        'FAW'
    ]

    for coin in coins:
        url = f"https://api.basecampcrypto.nl/v1/coin/{coin}/history?key=gxV34Ebr5s6ul15q"
        url = urlopen(url).read()

        data = json.loads(url)

        history_data = []
        for history in data['history']:
            history_data.append(float(history['value']))

        coins_data.update({coin: history_data})

    return coins_data


def calc_days(coin_data: list, func: callable) -> int:

    days = 0
    previous_value = 0

    for price in coin_data:
        if func(price, previous_value):
            days += 1

        previous_value = price

    return days


def calc_ldays(coin_data: list, func: callable) -> int:

    days = 0
    lst_days = []
    previous_value = 0

    for price in coin_data:
        if func(price, previous_value):
            days += 1
        else:
            lst_days.append(days)
            days = 0
        previous_value = price

    return max(lst_days)


def draw_table(coins_data: dict) -> None:
    """"""
    table = PrettyTable()

    table.field_names = ['₿', 'AVG', 'MIN', 'MAX', 'SD', 'Q1', ' Q2', 'Q3', 'RNG', 'IQR', 'UPS', 'DOWNS', 'LUP', 'LDWN']

    for coin, history in coins_data.items():
        row_data = []
        row_data.append(coin)
        row_data.append(round(statistics.mean(history), 2))

        min_data = min(history)
        max_data = max(history)
        row_data.append(min_data)
        row_data.append(max_data)
        row_data.append(round(statistics.stdev(history), 2))

        coin_quantiles = statistics.quantiles(history, n=4)
        row_data.append(round(coin_quantiles[0], 2))
        row_data.append(coin_quantiles[1])
        row_data.append(coin_quantiles[2])

        row_data.append(round(max_data - min_data, 2))
        row_data.append(round(coin_quantiles[2] - coin_quantiles[1], 2))

        row_data.append(calc_days(history, lambda x, y: x > y))
        row_data.append(calc_days(history, lambda x, y: x < y))

        row_data.append(calc_ldays(history, lambda x, y: x > y))
        row_data.append(calc_ldays(history, lambda x, y: x < y))

        table.add_row(row_data)

    print(table)


if __name__ == "__main__":
    coins_data = parse_json()
    draw_table(coins_data)
