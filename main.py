import matplotlib.pyplot as plt
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


def investor_amounts(coins_data: dict) -> list:
    """
    Maak een list met al het geld dat verdient is door de
    investeerders

    :param coins_data: dict, data met de waardes van de coins

    :return investor_amounts: list, lijst met het aantal geld van de investeerders
    """
    investor_amounts = []

    start_money = 1_000_000

    Alice = Investor(money=start_money, coin_data=coins_data['ALB'])
    Alice.invest(Investor.buy_at_rate, Investor.sell_at_rate, buy_rate=1500, sell_rate=1600)
    investor_amounts.append(Alice.money)

    Bob = Investor(money=start_money, coin_data=coins_data['BHA'])
    Bob.invest(Investor.buy_at_rate, Investor.sell_at_rate, buy_rate=1000, sell_rate=1100)
    investor_amounts.append(Bob.money)

    Carol = Investor(money=start_money, coin_data=coins_data['CAS'])
    Carol.invest(Investor.buy_at_valley, Investor.sell_at_peak)
    investor_amounts.append(Carol.money)

    Dave = Investor(money=start_money, coin_data=coins_data['DUB'])
    Dave.invest(Investor.buy_at_three_decrease, Investor.sell_at_three_increase)
    investor_amounts.append(Dave.money)

    Eve = Investor(money=start_money, coin_data=coins_data['ELG'])
    Eve.invest(Investor.buy_at_date, Investor.sell_at_date)
    investor_amounts.append(Eve.money)

    Frank = Investor(money=start_money, coin_data=coins_data['FAW'])
    Frank.invest(Investor.buy_at_decrease, Investor.sell_at_increase)
    investor_amounts.append(Frank.money)

    return investor_amounts


def show_investor_bar_chart(coins_data: dict) -> None:
    """
    Toon een bar graph van het aantal verdiende geld van
    de investeerders

    :param coins_data: dict, data met de waardes van de coins
    """
    fig, ax = plt.subplots()

    investors = ['Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank']
    amounts = investor_amounts(coins_data)
    bar_labels = investors
    bar_colors = ['tab:red', 'tab:blue', 'tab:pink', 'tab:orange', 'tab:purple', 'tab:cyan']

    ax.bar(investors, amounts, label=bar_labels, color=bar_colors)

    ax.set_ylabel('Money')
    ax.set_title('How much the investors earned')
    ax.legend(title='Investors')

    plt.show()


def plot_coin(coin_name: str, coin_data: list) -> None:
    """
    Maak een simpele plot van een coin.

    :param coin_data: list, de waardes van een coin
    """
    fig, ax = plt.subplots(figsize=(len(coin_data) / 3, 5))

    x = range(len(coin_data))

    up_colour, down_colour = "green", "red"

    for x1, x2, d1, d2 in zip(x, x[1:], coin_data, coin_data[1:]):
        if d1 > d2:
            plt.plot([x1, x2], [d1, d2], down_colour)
        elif d1 < d2:
            plt.plot([x1, x2], [d1, d2], up_colour)

    ax.set(xlabel='Days', ylabel='Value', title=f'The value of {coin_name} over 365 days')

    plt.show()


def main():
    """
    De main menu hier kan je een keuze maken voor welke data je wil zien.
    Voor de table met de waarde van de coins druk je op T.
    Voor de uitslag van de investeres druk op I
    Voor de grafiek van de waarde van de coins druk op G.
    Om het spel te spelen type Play.
    Als je klaar bent kan je met programma stoppen met quit(Q).
    """
    coins_data = parse_json()

    print("[T] Table with statistics")
    print("[G] The Graphs")
    print("[P] To play The game")
    print("[Q] Quit program")

    run = True

    while run is True:
        choice = input("choose:\n")

        if choice in ("t", "T"):
            draw_table(coins_data)
        elif choice in ("g", "G"):
            print("What data do you want to see graphed?")
            print("[1] individual coins [2] histogram of coin [3] investors")
            choice = input("> ")

            if choice == "1":
                print("Choose a coin: ALB, BHA, CAS, DUB, ELG, FAW")
                coin_choice = input("> ").upper()

                if coin_choice in ['ALB', 'BHA', 'CAS', 'DUB', 'ELG', 'FAW']:
                    plot_coin(coin_choice, coins_data[coin_choice])
            elif choice == "2":
                print("Choose a coin: ALB, BHA, CAS, DUB, ELG, FAW")
                coin_choice = input("> ").upper()

                if coin_choice in ['ALB', 'BHA', 'CAS', 'DUB', 'ELG', 'FAW']:
                    fig, ax = plt.subplots()
                    plt.hist(coins_data[coin_choice])
                    ax.set(xlabel='Value', ylabel='Distribution', title=f'The value distribution of {coin_choice}')
                    plt.show()
            elif choice == "3":
                show_investor_bar_chart(coins_data)
            else:
                print("Not an option!")
        elif choice in ("play", "Play"):
            pass
        elif choice in ("q", "Q"):
            run = False


if __name__ == "__main__":
    main()
