import collections
import pprint
import dataclasses
import pathlib
import typing

import utils

DATA_DIR = utils.get_data_dir(__file__)


FIVE_OF_A_KIND = 6
FOUR_OF_A_KIND = 5
FULL_HOUSE = 4
THREE_OF_A_KIND = 3
TWO_PAIR = 2
ONE_PAIR = 1
HIGH_CARD = 0


CARD_VALUES = {
    "A": 0,
    "K": -1,
    "Q": -2,
    "J": -3,
    "T": -4,
    "9": -5,
    "8": -6,
    "7": -7,
    "6": -8,
    "5": -9,
    "4": -11,
    "3": -12,
    "2": -13,
    "J": -14
}


def main():
    parser = utils.make_common_parser()
    args = parser.parse_args()
    data = read_data(DATA_DIR / args.input_file)

    res = do_challenge(data)
    print(f"The value is: {res}")


Hand_T = typing.TypeVar("Hand")


@dataclasses.dataclass
class Hand:
    cards: str
    bid: int

    @staticmethod
    def from_string(in_str: str) -> Hand_T:
        assert in_str.count(' ') == 1, "Malformed input"
        cards, sBid = in_str.split(" ")
        return Hand(cards, sBid)

    def __eq__(self, other: Hand_T) -> bool:
        return self.cards == other.cards

    def __lt__(self, other: Hand_T) -> bool:
        for (c, o) in zip(self.cards, other.cards):
            if CARD_VALUES[c] < CARD_VALUES[o]:
                return True
            elif CARD_VALUES[c] > CARD_VALUES[o]:
                return False
        # Cards are equal
        return False

    def __le__(self, other: Hand_T) -> bool:
        for (c, o) in zip(self.cards, other.cards):
            if CARD_VALUES[c] < CARD_VALUES[o]:
                return True
            elif CARD_VALUES[c] > CARD_VALUES[o]:
                return False
        # Cards are equal
        return True

    def __gt__(self, other: Hand_T) -> bool:
        for (c, o) in zip(self.cards, other.cards):
            if CARD_VALUES[c] > CARD_VALUES[o]:
                return True
            elif CARD_VALUES[c] < CARD_VALUES[o]:
                return False
        # Cards are equal
        return False

    def __ge__(self, other: Hand_T) -> bool:
        for (c, o) in zip(self.cards, other.cards):
            if CARD_VALUES[c] > CARD_VALUES[o]:
                return True
            elif CARD_VALUES[c] < CARD_VALUES[o]:
                return False
        # Cards are equal
        return True


def read_data(path: pathlib.Path) -> typing.List[str]:
    with path.open('r') as fi:
        res = (_.strip() for _ in fi.readlines())
    return res


def do_challenge(data: typing.List[str]) -> int:
    pp = pprint.PrettyPrinter(indent=2)
    hands = [Hand.from_string(_) for _ in data]
    hands = sort_hands(hands)
    pp.pprint(hands)
    total = 0
    for i, h in enumerate(hands):
        total += int(h.bid) * (i+1)
    return total


def sort_hands(hands: typing.List[Hand]) -> typing.List[Hand]:
    hands_by_type = [None] * 7  # There are 7 hand types
    for hand in hands:
        # First Determine Type of Hand.
        type_ = hand_type(hand)

        # Then Insert into place in the Tree
        if (tree := hands_by_type[type_]) is not None:
            tree.insert(hand)
        else:
            # First Hand in the tree
            tree = utils.BinaryNode(key=hand, parent=None)
            hands_by_type[type_] = tree

    sorted_hands = []
    for tree in hands_by_type:
        if tree is not None:
            sorted_hands.extend(tree.in_order_walk())
    return sorted_hands


def hand_type(hand: Hand) -> int:
    counter = collections.Counter(hand.cards)
    # Resolve the Joker
    if n_jokers := counter.pop("J", None):
        try:
            label, _ = counter.most_common()[0]
        except IndexError:
            counter['J'] = n_jokers
        else:
            counter[label] += n_jokers
    match counter.most_common():
        case[(_, 5)]:
            print(f"{hand.cards} is a  Five of a kind")
            return FIVE_OF_A_KIND
        case[(_, 4), _]:
            print(f"{hand.cards} is a  Four of a kind")
            return FOUR_OF_A_KIND
        case[(_, 3), (_, 2)]:
            print(f"{hand.cards} is a  Full House")
            return FULL_HOUSE
        case[(_, 3), *rest]:
            print(f"{hand.cards} is a  Three of a Kind")
            return THREE_OF_A_KIND
        case[(_, 2), (_, 2), *rest]:
            print(f"{hand.cards} is a  Two pair")
            return TWO_PAIR
        case[(_, 2), *rest]:
            print(f"{hand.cards} is a  One Pair")
            return ONE_PAIR
        case _:
            print(f"{hand.cards} is a  HIGH_CARD")
            return HIGH_CARD


def do_challenge2(data: typing.List[str]) -> int:
    pass


if __name__ == "__main__":
    main()
