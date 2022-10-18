import random
import time


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

    # TODO: one pair
    def is_one_pair(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand
        for i in range(len(_hand)):
            # might have more pairs, but the condition-order should prevent miscalculations
            if 1 == sum([_hand[i] % self.symbol_count == _hand[j] for j in range(i + 1, len(_hand))]):
                return True
        return False

    # TODO: two pair
    def is_two_pair(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand

    # TODO: three of a kind
    def is_three_of_a_kind(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand

    # TODO: straight
    def is_straight(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand

    # TODO: flush
    def is_flush(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand

    # TODO: full house
    # TODO:
    def is_full_house(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand

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
    # TODO: ass is not included as lowes card
    def is_straight_flush(self, _hand: list = None):
        if _hand is None:
            _hand = self.hand
        # check if all cards are from the same color
        if not all(int(_h / self.symbol_count) == int(_hand[0] / self.symbol_count) for _h in _hand):
            return False

        # check if all cards are directly in a row
        if not all(_hand[i] % self.symbol_count + 1 == _hand[i + 1] % self.symbol_count for i in range(len(_hand) - 1)):
            return False
        return True

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
        if not all(_hand[i] % self.symbol_count + 1 == _hand[i + 1] % self.symbol_count for i in range(len(_hand) - 1)):
            return False
        return True


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


def check(rounds: int = 10000000, hand_size: int = 5, symbole_size: int = 13, color_size: int = 4):
    print("Poker simulation")
    p = Poker(symbol_count=symbole_size, color_count=color_size)
    p.new_deck()
    counter = {
        "four_of_a_kind": 0,
        "straight_flush": 0,
        "royal_flush": 0
    }
    _time = time.time()
    for i in range(rounds):
        p.pick_hand(amount=hand_size)
        if p.is_royal_flush():
            counter["royal_flush"] += 1
            # print("royal flush")
            continue
        if p.is_straight_flush():
            counter["straight_flush"] += 1
            # print("straight flush")
            continue
        if p.is_four_of_a_kind():
            counter["four_of_a_kind"] += 1
            # print("four_of_a_kind")
            continue
    _time = time.time() - _time
    print("rounds:\t" + str(rounds) + "\ttimes")
    print("time:\t" + str(_time) + "\tseconds")
    print(counter)
    for counter_key in counter:
        print(counter_key + ":\t" + f"{(counter[counter_key] / rounds * 100):.6f}%")
    _count = 0
    for counter_key in counter:
        _count += counter[counter_key] / rounds * 100
    print("sum:\t" + str(_count) + "%")


if __name__ == '__main__':
    print("Main")
    check()
    print("end")
