import dataclasses
import collections
import pathlib
import typing

import utils

DATA_DIR = utils.get_data_dir(__file__)


def main():
    parser = utils.make_common_parser()
    args = parser.parse_args()
    data = read_data(DATA_DIR / args.input_file)

    res = do_challenge2(data)
    print(f"The value is: {res}")


def read_data(path: pathlib.Path) -> typing.List[str]:
    with path.open('r') as fi:
        res = fi.readlines()
    return res


Card_T = typing.TypeVar("Card")


@dataclasses.dataclass
class Card:
    id_: int
    winners: typing.Set[int]
    scratched: typing.List[int]

    @staticmethod
    def from_string(input_text: str) -> Card_T:
        assert input_text.count(':') == 1, f"Malformed Input, {input_text}"
        assert input_text.count('|') == 1, f"Malformed Input, {input_text}"
        id_str, game_data = input_text.split(":")
        winners_str, scratched_str = game_data.strip().split('|')
        id_ = int(id_str.replace("Card ", "").strip())
        winners = set(winners_str.strip().split())
        scratched = scratched_str.strip().split()

        return Card(id_, winners, scratched)

    def count_wins(self):
        return len(self.winners.intersection(self.scratched))

    def score(self):
        num_wins = self.count_wins()
        if num_wins:
            return 1 << (self.count_wins() - 1)
        else:
            return num_wins

    def collect_winnings(self, winnings_counter):
        num_copies = winnings_counter[self.id_]
        num_wins = self.count_wins()
        for i in range(self.id_ + 1, self.id_ + 1 + num_wins):
            winnings_counter[i] += num_copies


def do_challenge(data: typing.List[str]) -> int:
    games = [Card.from_string(line.strip()) for line in data]
    return sum([x.score() for x in games])


def do_challenge2(data: typing.List[str]) -> int:
    games = [Card.from_string(line.strip()) for line in data]
    winnings = collections.defaultdict(lambda: 1)
    for game in games:
        game.collect_winnings(winnings)
    return sum([v for v in winnings.values()])

if __name__ == "__main__":
    main()
