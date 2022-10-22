import csv
from datetime import datetime
import random
import time

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


# TODO: https://de.wikipedia.org/wiki/Poker
class Poker:

    #   13 * 4 = 52
    #   highest card in a color ist ass
    def __init__(self, symbol_count: int = 13, color_count: int = 4):
        self.symbol_count = symbol_count
        self.color_count = color_count
        self.deck = []
        self.hand = []

    def new_deck(self):
        self.deck = [i for i in range(self.color_count * self.symbol_count)]
        return self.deck

    #  pick_hand has made problems, because the function random.intrand() was used instead of random.randrange(),
    #  which differ in the range of values, when the same values are given
    def pick_hand(self, _deck: list = None, amount: int = 5, sort: bool = True):
        if _deck is None:
            _deck = self.deck
        if len(_deck) < amount:
            raise Exception("amount cannot be greater than the deck size(" + str(len(_deck)) + ")")
        for i in range(amount):
            index = random.randrange(0, len(_deck) - i, 1)
            _deck[-(i + 1)], _deck[index] = _deck[index], _deck[-(i + 1)]
            self.hand = _deck[-amount:]
            if sort:
                self.hand.sort()
        return self.deck

    def __str__(self):
        return "class:Poker"

    # check-functions

    # TODO: highest card (not really ^^)
    def is_high_card(self):
        return True

    # TODO: one pair
    def is_one_pair(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand
        temp = [0] * 13
        for h in _hand:
            temp[h % self.symbol_count] += 1
        return 4 == len([t for t in temp if t != 0])

    # TODO: two pair
    def is_two_pair(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand
        temp = [0] * 13
        for h in _hand:
            temp[h % self.symbol_count] += 1
        temp = [t for t in temp if t != 0]
        if len(temp) != 3:
            return False
        return 2 == sum(t == 2 for t in temp)

    # TODO: three of a kind
    def is_three_of_a_kind(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand
            # loop rounds -2, because checking 2 cards are never going to be four_of_a_kind.
            for i in range(len(_hand) - 2):
                # checking if one card is the same as other cards and
                # if there are 3 same cards (2 True values in list) it will return True
                if 2 == sum([_hand[i] % self.symbol_count == _hand[j] % self.symbol_count
                             for j in range(i + 1, len(_hand))]):
                    return True
            return False

    # TODO: straight
    def is_straight(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand
        _hand = sorted(h % self.symbol_count for h in _hand)
        ass_amount = sum(h == self.symbol_count - 1 for h in _hand)
        if 1 < ass_amount:
            return False
        if ass_amount == 1:
            if all(_hand[i] == i for i in range(0, len(_hand) - 1)):
                return True
        return all(_hand[i] + 1 == _hand[i + 1] for i in range(len(_hand) - 1))

    # TODO: flush
    def is_flush(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand
        return all(int(_h / self.symbol_count) == int(_hand[0] / self.symbol_count) for _h in _hand)

    # TODO: full house
    # TODO: only works for hand size of 5
    def is_full_house(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand
        temp = [0] * 13
        for h in _hand:
            temp[h % self.symbol_count] += 1
        temp = [t for t in temp if t != 0]
        if len(temp) != 2:
            return False
        return any(temp[i] == 2 and temp[(i + 1) % len(temp)] == 3 for i in range(len(temp)))

    # TODO: four of a kind
    def is_four_of_a_kind(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand
        # loop rounds -3, because checking 3 cards are never going to be four_of_a_kind.
        for i in range(len(_hand) - 3):
            # checking if one card is the same as other cards and
            # if there are 4 same cards (3 True values in list) it will return True
            if 3 == sum([_hand[i] % self.symbol_count == _hand[j] % self.symbol_count
                         for j in range(i + 1, len(_hand))]):
                return True
        return False

    # TODO: straight flush
    # TODO: doesn't work for 7 cards, as long as all cards aren'T directly in a row and in one color
    def is_straight_flush(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand
        # check if all cards are from the same color
        if not all(int(_h / self.symbol_count) == int(_hand[0] / self.symbol_count) for _h in _hand):
            return False
        # check if there are multiple ass
        ass_amount = sum(h % self.symbol_count == self.symbol_count - 1 for h in _hand)
        if 1 < ass_amount:
            return False
        if ass_amount == 1:
            if all(_hand[i] % self.symbol_count == i for i in range(0, len(_hand) - 1)):
                return True
        # check if all cards are directly in a row
        return all(_hand[i] % self.symbol_count + 1 == _hand[i + 1] % self.symbol_count for i in range(len(_hand) - 1))

    # TODO: royal flush
    # TODO: doesn't work for 7 cards, as long as all cards aren'T directly in a row, in one color
    #       and the highest card is ass
    def is_royal_flush(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand
        # check if all cards are from the same color
        if not all(int(_h / self.symbol_count) == int(_hand[0] / self.symbol_count) for _h in _hand):
            return False
        # check if the highest card is an ass
        if _hand[-1] % self.symbol_count is not self.symbol_count - 1:
            return False
        # check if all cards are directly in a row
        return all(_hand[i] % self.symbol_count + 1 == _hand[i + 1] % self.symbol_count for i in range(len(_hand) - 1))


def check_basics():
    p = Poker(symbol_count=13, color_count=4)
    p.new_deck()
    print(p.deck)
    p.pick_hand()
    print(p.deck)
    print(p.is_royal_flush())


def check_is_royal_flush():
    p = Poker()
    p.new_deck()
    counter = []
    _time = time.time()
    for i in range(10000000):
        p.pick_hand()
        counter.append(p.is_royal_flush())
    _time = time.time() - _time
    print("time:" + str(_time))
    print("len:" + str(len(counter)))
    print("sum:" + str(sum(counter)))
    average = sum(counter) / (len(counter))
    print("avg:" + f"{average * 100:.6f}" + "%")


def check(rounds: int = 10000000, hand_size: int = 5, symbol_size: int = 13, color_size: int = 4):
    print("Poker simulation")
    p = Poker(symbol_count=symbol_size, color_count=color_size)
    p.new_deck()
    stat = csv_stat_format
    _time = time.time()
    for i in range(rounds):
        p.pick_hand(amount=hand_size)
        if p.is_royal_flush():
            stat['royal_flush'] += 1
            # print('royal flush')
            continue
        if p.is_straight_flush():
            stat['straight_flush'] += 1
            # print('straight flush')
            continue
        if p.is_four_of_a_kind():
            stat['four_of_a_kind'] += 1
            # print('four_of_a_kind')
            continue
        if p.is_full_house():
            stat['full_house'] += 1
            # print('full house')
            continue
        if p.is_flush():
            stat['flush'] += 1
            # print('flush')
            continue
        if p.is_straight():
            stat['straight'] += 1
            # print('straight')
            continue
        if p.is_three_of_a_kind():
            stat['three_of_a_kind'] += 1
            # print('three of a kind')
            continue
        if p.is_two_pair():
            stat['two_pair'] += 1
            continue
        if p.is_one_pair():
            stat['one_pair'] += 1
            continue
        if p.is_high_card():
            stat['high_card'] += 1
            continue
    _time = time.time() - _time
    stat['procedure_time'] = _time
    stat['rounds'] = rounds
    print("rounds:\t" + str(rounds) + "\ttimes")
    print("time:\t" + str(_time) + "\tseconds")
    print(stat)
    for i in range(3, len(stat.keys())):
        keys = [key for key in stat.keys()]
        print(str(keys[i]) + ":\t" + f"{(stat[keys[i]] / rounds * 100):.6f}%")
    save_stats(stat)


def save_stats(stat: dict):
    content = {}
    with open("stats.csv") as csv_f:
        reader = csv.reader(csv_f, delimiter=';')
        for line in reader:
            content[line[0]] = line[1:]
    print(content)
    with open("stats.csv", 'w', newline='') as csv_f:
        writer = csv.writer(csv_f, delimiter=";")
        last_id = -1
        for c_key in content:
            writer.writerow([c_key] + content[c_key])
            if c_key != 'id':
                last_id = int(c_key)
        new_stat = [stat[s] for s in stat]
        new_stat[0] = last_id + 1
        print(new_stat)
        writer.writerow(new_stat)


if __name__ == '__main__':
    print("Main")
    check()
    print("end")
