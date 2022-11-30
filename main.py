from prettytable import PrettyTable
from Investor import Investor
from urllib.request import urlopen
import json
import statistics


def parse_json() -> dict:
    """
    haald data via de url en stopt deze in een dict.

    :return coins_data: een dict met coin als key en waarde als value.
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
    # coins: list met alle coins.

    for coin in coins:
        url = f"https://api.basecampcrypto.nl/v1/coin/{coin}/history?key=gxV34Ebr5s6ul15q"
        # url: de url van de server met de data.
        url = urlopen(url).read()

        data = json.loads(url)

        history_data = []
        # history_data: list met de waarde die de coin toen was.
        for history in data['history']:
            history_data.append(float(history['value']))

        coins_data.update({coin: history_data})

    return coins_data


def calc_days(coin_data: list, func: callable) -> int:
    """
    berkent het aantal dagen waarin de waarde hoger/lager is dan de dag ervoor.

    :param coin_data: list met data van de coins

    :return days: het aantal dagen dat hoger/lager zijn
    """
    days = 0
    previous_value = 0

    for price in coin_data:
        if func(price, previous_value):
            days += 1

        previous_value = price

    return days


def calc_ldays(coin_data: list, func: callable) -> int:
    """
    berkent de streak waarin het aantal dagen waarin de
    waarde hoger/lager is dan de dag ervoor.

    :param coin_data: list met data van de coins

    :return max(lst_days): de hoogste value uit de list is de hoogste streak
    """
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
    """
    maakt een table met pretty tables met de berekeningen die je maakt.

    :param coin_data: dict met data van de coins
    """
    table = PrettyTable()

    table.field_names = ['₿', 'AVG', 'MIN', 'MAX', 'SD', 'Q1',
                         ' Q2', 'Q3', 'RNG', 'IQR', 'UPS', 'DOWNS', 'LUP', 'LDWN']

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


def main():
    """
    De main menu hier kan je een keuze maken voor welke data je wil zien.
    Voor de table met de waarde van de coins druk je op T.
    Voor de uitslag van de investeres druk op I
    Voor de grafiek van de waarde van de coins druk op G.
    Om het spel te spelen type Play.
    Als je klaar bent kan je met programma stoppen met quit(Q).
    """

    print("[T] Table with statistics")
    print("[I] Outcome for the 6 investers")
    print("[G] The Graph")
    print("[play] To play The game")
    print("[Q] Quit program")

    coins_data = parse_json()

    # Test dingen :)
    start_money = 1_000_000

    Alice = Investor(money=start_money, coin_data=coins_data['ALB'])
    Alice.invest(Investor.buy_at_rate, Investor.sell_at_rate, buy_rate=1500, sell_rate=1600)
    print(Alice.money)

    Bob = Investor(money=start_money, coin_data=coins_data['BHA'])
    Bob.invest(Investor.buy_at_rate, Investor.sell_at_rate, buy_rate=1000, sell_rate=1100)
    print(Bob.money)

    run = True

    while run is True:
        choice = input("choose:\n")

        if choice in ("t", "T"):
            draw_table(coins_data)
            break
        if choice in ("i", "I"):
            pass
        if choice in ("g", "G"):
            pass
        if choice in ("play", "Play"):
            pass
        if choice in ("q", "Q"):
            run = False


if __name__ == "__main__":
    main()
