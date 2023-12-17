import pathlib
import typing
import dataclasses

import utils

DATA_DIR = utils.get_data_dir(__file__)

RED = "red"
GREEN = "green"
BLUE = "blue"

CONSTRAINTS = {
    RED: 12,
    GREEN: 13,
    BLUE: 14,
}


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


Round_T = typing.TypeVar("Round")


@dataclasses.dataclass
class Round:
    red: int = 0
    green: int = 0
    blue: int = 0

    @staticmethod
    def from_string(input_str) -> Round_T:
        assert input_str.count(",") <= 2, f"Malformed Input String: {input_str}"
        color_draws = input_str.split(",")
        in_dict = {}
        for draw in color_draws:
            count, color = draw.strip().split(' ')
            in_dict[color] = int(count)
        return Round(**in_dict)


GameRecord_T = typing.TypeVar("GameRecord")


@dataclasses.dataclass
class GameRecord:
    id_: int
    rounds: typing.List[Round]

    @staticmethod
    def from_string(input_str: str) -> GameRecord_T:
        assert input_str.count(":") == 1, f"Malformed Input: {input_str}"
        game_id, rounds = input_str.split(":", 1)
        id_ = int(game_id.replace("Game ", "").strip())
        rounds = [Round.from_string(r) for r in rounds.split(";")]
        return GameRecord(id_=id_, rounds=rounds)

    def is_possible(self, constraint: dict):
        for round in self.rounds:
            for color, limit in constraint.items():
                if getattr(round, color) > limit:
                    return False
        return True

    def fewest_needed(self, ) -> Round:
        data = {
            RED: 0,
            BLUE: 0,
            GREEN: 0,
        }
        for round in self.rounds:
            for color in data.keys():
                if (val := getattr(round, color)) > data.get(color):
                    data[color] = val
        return Round(**data)

    def power(self):
        min_set = self.fewest_needed()
        return min_set.blue * min_set.red * min_set.green


def do_challenge(data: typing.List[str]):
    games = GameRecord.from_string(rec) for rec in data]
    valid_games = filter(lambda g: g.is_possible(CONSTRAINTS), games)
    return sum((v.id_ for v in valid_games))


def do_challenge2(data: typing.List[str]):
    games = [GameRecord.from_string(rec) for rec in data]
    powers = map(lambda g: g.power(), games)
    return sum(powers)


if __name__ == "__main__":
    main()
