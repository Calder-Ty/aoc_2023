import itertools
import functools
import dataclasses
import pathlib
import typing

import utils

DATA_DIR = utils.get_data_dir(__file__)

WORKING = '.'
DAMAGED = '#'
UNKOWN = '?'


def main():
    parser = utils.make_common_parser()
    args = parser.parse_args()
    data = read_data(DATA_DIR / args.input_file)

    res = do_challenge(list(data))
    print(f"The value is: {res}")


def read_data(path: pathlib.Path) -> typing.List[str]:
    with path.open('r') as fi:
        res = (_.strip() for _ in fi.readlines())
    return res


SpringRow_T = typing.TypeVar("SprintRow")


@dataclasses.dataclass
class SpringRow:
    springs: str
    fault_groups: typing.List[int]

    @staticmethod
    def from_string(input_str: str) -> SpringRow_T:
        springs, group_str = input_str.split(' ')
        groups = [int(x) for x in group_str.split(',')]
        return SpringRow(springs, groups)

    def n_valid_possibilities(self):
        """Calculates the Number of Valid possibilities"""
        count = 0
        for config in gen_spring_configs(self.springs, self.fault_groups):
            if valid_groups(config, self.fault_groups):
                count += 1
        return count


def valid_groups(S: str, A: typing.List[int]):
    groups = [[]]
    for symbol in S:
        if symbol == DAMAGED:
            groups[-1].append(symbol)
        else:
            if groups[-1]:
                groups.append([])
    if groups[-1] == []:
        group_lens = [len(x) for x in groups[:-1]]
    else:
        group_lens = [len(x) for x in groups]

    return group_lens == A


def gen_spring_configs(S: str, A: typing.List[int]):
    """Generates the possible strings"""
    unkowns = []
    for i, s in enumerate(S):
        if s == UNKOWN:
            unkowns.append(i)
    r = sum(A) - S.count(DAMAGED)
    for indexes in itertools.combinations(unkowns, r=r):
        s = S
        for i in indexes:
            if i == len(S) - 1:
                s = s[:i] + DAMAGED
            else:
                s = s[:i] + DAMAGED + S[i+1:]
        yield s


def parse_data(data: typing.List[str]):
    records = []
    for row in data:
        records.append(SpringRow.from_string(row))
    return records


def do_challenge(data: typing.List[str]) -> int:
    spring_rows = parse_data(data)
    counts = []
    for row in spring_rows:
        counts.append(row.n_valid_possibilities())

    print(counts)
    return sum(counts)


def do_challenge2(data: typing.List[str]) -> int:
    pass


if __name__ == "__main__":
    main()
