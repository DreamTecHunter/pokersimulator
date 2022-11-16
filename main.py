import csv
import string
from datetime import datetime
import random
import time
from enum import Enum

csv_stat_format = {
    'id': -1,
    'datetime': str(datetime.now()),
    'rounds': 0,
    'procedure_time': 0,
    'high_card': 0,
    'one_pair': 0,
    'two_pair': 0,
    'three_of_a_kind': 0,
    'straight': 0,
    'flush': 0,
    'full_house': 0,
    'four_of_a_kind': 0,
    'straight_flush': 0,
    'royal_flush': 0
}

source_path = "stats.csv"
target_path = "stats.csv"
delimiter = ";"


class HandBiggerThanDeckException(Exception):
    def __init__(self, deck_size: int, hand_size, message: str = None):
        self.deck_size = deck_size
        self.hand_size = hand_size
        self.message = ("Hand-size cannot be greater then deck-size!\nhand-size: " + str(len(self.hand_size))
                        + "\tdeck-size" + str(len(self.deck_size)) if message is None else message)
        super().__init__(self.message)


class PokerStats:
    def __init__(self,
                 _source_path: str = None,
                 _target_path: str = None,
                 _csv_stat_format: dict = None,
                 _delimiter: str = None):
        self.stats = None
        self.source_path = source_path if _source_path is None else _source_path
        self.target_path = target_path if _target_path is None else _target_path
        if _csv_stat_format is None:
            self.reset_stats()
        else:
            self.stats = _csv_stat_format
        self.delimiter = delimiter if _delimiter is None else _delimiter

    def __str__(self):
        return "class:PokerStats" \
               "\n\tsource_path: " + self.source_path + \
               "\n\ttarget_path: " + self.target_path + \
               "\n\tdefault-csv_file_format: " + csv_stat_format + \
               "\n\tdelimiter: " + self.delimiter

    def reset_stats(self):
        self.stats = csv_stat_format

    def get_all_stats_from_csv(self):
        content = {}
        with open(self.source_path) as csv_file:
            reader = csv.reader(csv_file, delimiter=self.delimiter)
            for line in reader:
                content[line[0]] = line[1:]
        return content

    def add_new_stat_into_csv(self, _stat: dict):
        content = self.get_all_stats_from_csv()
        with open(self.target_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=self.delimiter)
            last_id = -1
            for c_key in content:
                writer.writerow([c_key] + content[c_key])
                if c_key != 'id':
                    last_id = int(c_key)
            new_stat = [_stat[s] for s in _stat]
            new_stat[0] = last_id + 1
            writer.writerow(new_stat)


class PokerColorEnum(Enum):
    SPADE = 0
    HEART = 1
    CLOVER = 2
    DIAMOND = 3


class PokerSymbolEnum(Enum):
    TWO = 0
    THREE = 1
    FOUR = 2
    FIVE = 3
    SIX = 4
    SEVEN = 5
    EIGHT = 6
    NINE = 7
    TEN = 8
    JACK = 9
    QUEEN = 10
    KING = 11
    ACE = 12


# TODO: https://de.wikipedia.org/wiki/Poker
class Poker:
    def __init__(self, symbol_count: int = 13, color_count: int = 4):
        self.symbol_count = symbol_count
        self.color_count = color_count
        self.deck = []
        self.hand = []

    def __str__(self):
        return "class: Poker\tsymbol_count: " + str(self.symbol_count) + "\tcolor_count: "
        + str(self.color_count) + "\n\tdeck: " + str(self.deck) + "\n\tpresent hand: " + str(self.hand)

    # preparation-methods

    def new_deck(self):
        self.deck = [i for i in range(self.color_count * self.symbol_count)]
        return self.deck

    def new_hand(self, _deck: list = None, hand_size: int = 5, sort: bool = True):
        # TODO:
        if _deck is None:
            _deck = self.deck
        if 5 != hand_size:
            raise Exception("Current methods in class:Poker only works with hand-size of 5")
        if len(_deck) < hand_size:
            raise HandBiggerThanDeckException()
        for i in range(hand_size):
            index = random.randrange(0, len(_deck) - i, 1)
            _deck[-(i + 1)], _deck[index] = _deck[index], _deck[-(i + 1)]
            self.hand = _deck[-hand_size:]
        return self.hand.sort() if sort else self.hand

    def get_name(self, card_value: int):
        return (list(PokerColorEnum)[int(card_value / self.symbol_count)].name +
                "-" +
                list(PokerSymbolEnum)[card_value % self.symbol_count].name)

    def get_deck(self, as_numbers: bool = True):
        return self.deck if as_numbers else [self.get_name(card) for card in self.deck]

    def get_hand(self, as_number: bool = True):
        return self.hand if as_number else [self.get_name(card) for card in self.hand]

    # support-methods

    def check_hand(self, _hand):
        return _hand if _hand is not None else self.hand

    def count_appearance(self, _hand, check_symbols: bool = True, clear: bool = False):
        temp = [0] * (self.symbol_count if check_symbols else self.color_count)
        for h in _hand:
            temp[h % self.symbol_count if check_symbols else int(h / self.symbol_count)] += 1
        return [t for t in temp if t != 0] if not clear else temp

    # check-hand-methods

    def is_high_card(self, _hand: list = None):
        return True

    def is_one_pair(self, _hand: list = None):
        _hand = self.check_hand(_hand)
        return 4 == len(self.count_appearance(_hand))

    def is_two_pair(self, _hand: list = None):
        _hand = self.check_hand(_hand)
        temp = self.count_appearance(_hand)
        if len(temp) != 3:
            return False
        return 2 == sum(t == 2 for t in temp)

    def is_three_of_a_kind(self, _hand: list = None):
        _hand = self.check_hand(_hand)
        temp = self.count_appearance(_hand)
        return 1 == sum(t == 3 for t in temp)

    def is_straight(self, _hand: list = None, with_ace_as_lowest: bool = True):
        _hand = self.check_hand(_hand)
        _hand = sorted(h % self.symbol_count for h in _hand)
        if with_ace_as_lowest:
            ace_amount = sum(h == self.symbol_count - 1 for h in _hand)
            if 1 < ace_amount:
                return False
            if ace_amount == 1:
                if all(_hand[i] == i for i in range(0, len(_hand) - 1)):
                    return True
        return all(_hand[i] + 1 == _hand[i + 1] for i in range(len(_hand) - 1))

    def is_flush(self, _hand: list = None):
        _hand = self.check_hand(_hand)
        return 1 == len(self.count_appearance(_hand, check_symbols=False))

    def full_house(self, _hand: list = None):
        _hand = self.check_hand(_hand)
        temp = self.count_appearance(_hand)
        return any(
            (temp[i] == 2 and temp[(i + 1) % len(temp)] == 3)
            or
            (temp[i] == 3 and temp[(i + 1) % len(temp)] == 2)
            for i in range(len(temp))
        )

    def is_four_of_a_kind(self, _hand: list = None):
        _hand = self.check_hand(_hand)
        temp = self.count_appearance(_hand)
        return 1 == sum(t == 4 for t in temp)

    def is_straight_flush(self, _hand: list = None):
        _hand = self.check_hand(_hand)
        return self.is_flush(_hand) and self.is_straight(_hand)

    def is_royal_flush(self, _hand: list = None):
        _hand = self.check_hand(_hand)
        if _hand[-1] % self.symbol_count != self.symbol_count - 1:
            return False
        return self.is_flush(_hand) and self.is_straight(_hand, with_ace_as_lowest=False)

    # in order of which the first eliminates the rest
    is_methods = [
        is_royal_flush,
        is_straight_flush,
        is_four_of_a_kind,
        full_house,
        is_flush,
        is_straight,
        is_three_of_a_kind,
        is_two_pair,
        is_one_pair,
        is_high_card
    ]

    def check_one_hand(self, _hand: list = None):
        for is_method in self.is_methods:
            if is_method(self, _hand=_hand):
                return is_method.__name__.replace("is_", "")

    def check_multiple_rounds(self, rounds: int = 10000000, message_on: bool = False):
        stat = {key: value for (key, value) in csv_stat_format.items()}
        self.new_deck()
        if message_on:
            print("new-deck:\t" + str(self.new_deck()))
            print("symbols:\t" + str(self.get_deck(as_numbers=False)))
        stat['datetime'] = str(datetime.now())
        if message_on:
            print("datetime:\t" + str(stat['datetime']))
            print("rounds:\t{:>10}".format(rounds))
        _time = time.time()
        temp_time = 0
        for i in range(rounds):
            if message_on and False:
                print("round:\t{:>10}".format(i), end='\r')
            self.new_hand()
            stat[self.check_one_hand()] += 1
        _time = time.time() - _time
        if message_on:
            print("procedure-time:\t" + str(_time))
        stat['procedure_time'] = _time
        stat['rounds'] = rounds
        print("\n")
        if message_on:
            for key in list(csv_stat_format.keys())[4:]:
                value = round(stat[key] / stat["rounds"] * 100 * 10 ** 7) / 10 ** 7
                print(str(key) + ":\t" + str(value) + "%")
        return stat


def pick_one_hand():
    p = Poker()
    p.new_deck()
    print(p.deck)
    print(p.get_deck())
    print(p.get_deck(as_numbers=False))
    p.new_hand()
    print(p.hand)
    print(p.get_hand())
    print(p.get_hand(as_number=False))


def poker_stats(rounds: int = 10000000, message_on: bool = False):
    p = Poker()
    ps = PokerStats()
    ps.add_new_stat_into_csv(_stat=p.check_multiple_rounds(rounds=rounds, message_on=message_on))


def poker_stats_from_ten_million_rounds(message_on: bool = False):
    poker_stats(message_on=message_on)


if __name__ == '__main__':
    print("poker-simulation")
    print("start")
    poker_stats(message_on=True)
    print("end")
