class Investor:

    def __init__(self, money=1_000_000, coin_data=[]):
        self.money: float = money
        self.coin_data: list = coin_data

        self.net_profit: float = 0

    def invest(self, buy_check: callable, sell_check: callable, buy_rate: float = 0, sell_rate: float = 0) -> float:
        """
        Investeer het start geld op basis van de strategieen die als argumenten
        meegegeven worden.

        :param self, huidige object
        :param buy_check: callable, functie om te checken of het gekocht kan worden
        :param sell_check: callable, functie die checkt of het verkocht kan worden
        :param buy_rate: float, op welke rate je het wilt kopen (optional)
        :param sell_rate: float, op welke rate je het wil verkopen (optional)

        :return self.money: float, nieuw aantal geld dat gemaakt is
        """
        current_amount = 0

        for day, value in enumerate(self.coin_data):
            day += 1
            if buy_check(self.coin_data, day, value, rate=buy_rate) and self.money > value:
                current_amount = round(self.money / value, 1)
                self.money = round(self.money - (current_amount * value), 2)
            elif sell_check(self.coin_data, day, value, rate=sell_rate) or day == 365:
                self.money = round(current_amount * value, 2)

        return self.money

    @staticmethod
    def buy_at_rate(coin_data: list, day: int, value: float, rate: float = 0) -> bool:
        """
        of je op basis van het huidige bedracht het wilt kopen.

        :param coin_data: list, data van de coin
        :param day: int, huidige dag
        :param value: float, huidige waarde van de coin
        :param rate: float, op welke rate je het moet kopen

        :return bool, of het gekocht kan worden
        """
        return value < rate

    @staticmethod
    def sell_at_rate(coin_data: list, day: int, value: float, rate: float = 0) -> bool:
        """
        of je op basis van het huidige bedracht het wilt verkopen.

        :param coin_data: list, data van de coin
        :param day: int, huidige dag
        :param value: float, huidige waarde van de coin
        :param rate: float, op welke rate je het moet kopen

        :return bool, of het verkocht kan worden
        """
        return value > rate

    @staticmethod
    def buy_at_valley(coin_data: list, day: int, value: float, rate: float = 0) -> bool:
        """
        of je op basis van de valley het wilt kopen het wilt kopen.

        :param coin_data: list, data van de coin
        :param day: int, huidige dag
        :param value: float, huidige waarde van de coin
        :param rate: float, op welke rate je het moet kopen

        :return bool, of het verkocht kan worden
        """

        previous_value = coin_data[day - 1]

        try:
            next_value = coin_data[day + 1]
        except IndexError:
            return True

        return value < previous_value and value < next_value

    @staticmethod
    def sell_at_peak(coin_data: list, day: int, value: float, rate: float = 0) -> bool:
        """
        of je op basis van de peak het wilt kopen het wilt verkopen.

        :param coin_data: list, data van de coin
        :param day: int, huidige dag
        :param value: float, huidige waarde van de coin
        :param rate: float, op welke rate je het moet kopen

        :return bool, of het verkocht kan worden
        """

        previous_value = coin_data[day - 1]

        try:
            next_value = coin_data[day + 1]
        except IndexError:
            return True

        return value > previous_value and value > next_value

    @staticmethod
    def buy_at_decrease(coin_data: list, day: int, value: float, rate: float = 0) -> bool:
        """
        of je op basis van de decrease het wilt kopen het wilt kopen.

        :param coin_data: list, data van de coin
        :param day: int, huidige dag
        :param value: float, huidige waarde van de coin
        :param rate: float, op welke rate je het moet kopen

        :return bool, of het verkocht kan worden
        """
        if day == 1:
            return True

        previous_value = coin_data[day - 1]
        percentage_change = 100 * (previous_value - value) / value

        return round(percentage_change) == -20

    @staticmethod
    def sell_at_increase(coin_data: list, day: int, value: float, rate: float = 0) -> bool:
        """
        of je op basis van de increase het wilt kopen het wilt verkopen.

        :param coin_data: list, data van de coin
        :param day: int, huidige dag
        :param value: float, huidige waarde van de coin
        :param rate: float, op welke rate je het moet kopen

        :return bool, of het verkocht kan worden
        """
        if day == 1:
            return False

        previous_value = coin_data[day - 1]
        percentage_change = 100 * (value - previous_value) / previous_value

        return round(percentage_change) == -20

    @staticmethod
    def buy_at_three_decrease(coin_data: list, day: int, value: float, rate: float = 0) -> bool:
        """
        of je op basis van het huidige bedracht het wilt kopen.

        :param coin_data: list, data van de coin
        :param day: int, huidige dag
        :param value: float, huidige waarde van de coin
        :param rate: float, op welke rate je het moet kopen

        :return bool, of het gekocht kan worden
        """
        previous_value = coin_data[day - 2]
        previous_previous_value = coin_data[day - 3]

        return previous_previous_value > previous_value > value

    @staticmethod
    def sell_at_three_increase(coin_data: list, day: int, value: float, rate: float = 0) -> bool:
        """
        of je op basis van het huidige bedracht het wilt verkopen.

        :param coin_data: list, data van de coin
        :param day: int, huidige dag
        :param value: float, huidige waarde van de coin
        :param rate: float, op welke rate je het moet kopen

        :return bool, of het verkocht kan worden
        """
        previous_value = coin_data[day - 2]
        previous_previous_value = coin_data[day - 3]

        return previous_previous_value < previous_value < value

    @staticmethod
    def buy_at_date(coin_data: list, day: int, value: float, rate: float = 0) -> bool:
        """
        of je op basis van het huidige bedracht het wilt kopen.

        :param coin_data: list, data van de coin
        :param day: int, huidige dag
        :param value: float, huidige waarde van de coin
        :param rate: float, op welke rate je het moet kopen

        :return bool, of het gekocht kan worden
        """
        day = str(day)
        last_number = day[-1:]
        return last_number == "1"

    @staticmethod
    def sell_at_date(coin_data: list, day: int, value: float, rate: float = 0) -> bool:
        """
        of je op basis van het huidige bedracht het wilt verkopen.

        :param coin_data: list, data van de coin
        :param day: int, huidige dag
        :param value: float, huidige waarde van de coin
        :param rate: float, op welke rate je het moet kopen

        :return bool, of het verkocht kan worden
        """
        day = str(day)
        last_number = day[-1:]
        return last_number == "5"
