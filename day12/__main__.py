import collections
import itertools
import functools
import dataclasses
import pathlib
import typing
import sys


sys.path.append('..')

import utils

DATA_DIR = utils.get_data_dir(__file__)
UNFOLD_FACTOR = 5

WORKING = '.'
DAMAGED = '#'
UNKNOWN = '?'

CORRECT = [4, 8, 16, 2, 10, 14, 1, 4, 6, 46, 1, 5, 2, 2, 25, 4, 13, 5, 4, 14, 13, 22, 20, 1, 4, 18, 5, 4, 1, 25, 13, 7, 1, 7, 11, 6, 4, 2, 2, 7, 2, 8, 12, 16, 10, 3, 4, 19, 1, 29, 10, 9, 15, 3, 2, 10, 4, 12, 27, 9, 5, 1, 3, 1, 2, 3, 2, 8, 1, 2, 2, 27, 4, 2, 7, 1, 4, 5, 3, 1, 11, 5, 6, 1, 14, 4, 7, 23, 5, 1, 70, 4, 2, 63, 11, 15, 16, 7, 6, 6, 2, 2, 52, 12, 6, 12, 1, 1, 8, 1, 7, 7, 2, 1, 6, 55, 5, 33, 8, 1, 6, 2, 90, 11, 5, 6, 16, 4, 4, 1, 6, 3, 6, 2, 1, 6, 1, 9, 3, 4, 9, 2, 2, 2, 3, 3, 7, 17, 1, 2, 1, 6, 2, 3, 4, 2, 3, 56, 8, 2, 126, 2, 1, 7, 26, 4, 5, 1, 4, 3, 4, 31, 4, 4, 2, 8, 10, 6, 6, 6, 6, 2, 2, 3, 29, 7, 3, 31, 9, 8, 2, 1, 12, 4, 2, 3, 7, 2, 2, 1, 2, 3, 1, 1, 17, 7, 2, 10, 1, 4, 6, 2, 3, 6, 61, 33, 1, 2, 6, 2, 4, 3, 23, 55, 45, 2, 15, 2, 12, 18, 2, 2, 6, 5, 6, 2, 3, 8, 63, 85, 3, 5, 35, 91, 6, 2, 5, 16, 4, 1, 2, 6, 5, 19, 4, 4, 8, 2, 2, 2, 5, 5, 20, 6, 2, 3, 4, 64, 12, 15, 5, 4, 21, 4, 1, 6, 1, 2, 11, 1, 1, 1, 1, 7, 2, 7, 15, 2, 34, 9, 8, 5, 1, 7, 15, 24, 2, 14, 3, 2, 4, 1, 3, 2, 9, 4, 1, 9, 16, 2, 9, 4, 3, 1, 4, 1, 1, 16, 3, 3, 7, 19, 9, 2, 16, 3, 29, 51, 1, 4, 20, 3, 6, 4, 75, 4, 4, 15, 35, 5, 27, 3, 8, 1, 9, 6, 1, 1, 6, 3, 2, 6, 2, 4, 3, 6, 3, 3, 2, 11, 3, 3, 1, 30, 1, 45, 2, 9, 19, 5, 9, 1, 6, 3, 6, 5, 2, 4, 20, 10, 16, 1, 1, 10, 1, 3, 17, 6, 5, 6, 4, 4, 15, 4, 6, 2, 1, 6, 8, 2, 10, 2, 22, 8, 6, 1, 4, 35, 13, 4, 1, 1, 3, 4, 4, 4, 8, 2, 6, 2, 11, 4, 5, 1, 2, 4, 1, 6, 4, 24, 20, 13, 4, 2, 12, 16, 5, 3, 4, 6, 15, 4, 7, 5, 8, 7, 4, 4, 4, 12, 2, 6, 5, 8, 9, 6, 1, 2, 21, 12, 6, 3, 24, 7, 2, 43, 1, 3, 13, 2, 6, 1, 12, 4, 2, 8, 4, 5, 2, 15, 28, 1, 2, 17, 3, 1, 6, 8, 1, 7, 6, 2, 1, 3, 2, 20,
           1, 24, 8, 8, 4, 2, 2, 1, 3, 18, 1, 10, 4, 2, 6, 2, 9, 35, 1, 1, 37, 11, 5, 9, 20, 6, 3, 2, 10, 3, 17, 8, 6, 1, 28, 2, 6, 31, 9, 2, 2, 7, 3, 5, 3, 16, 2, 1, 2, 13, 4, 1, 1, 10, 1, 2, 4, 47, 16, 1, 2, 2, 18, 12, 12, 6, 10, 8, 2, 18, 8, 3, 4, 1, 2, 10, 1, 2, 4, 6, 13, 3, 3, 2, 4, 1, 10, 12, 5, 2, 34, 2, 2, 1, 4, 6, 4, 9, 20, 1, 3, 4, 2, 2, 4, 1, 1, 10, 5, 3, 1, 4, 11, 1, 7, 16, 38, 10, 12, 3, 9, 1, 3, 1, 2, 6, 8, 3, 20, 5, 2, 2, 1, 1, 1, 4, 10, 3, 6, 2, 4, 4, 6, 4, 1, 40, 1, 13, 4, 1, 5, 91, 16, 11, 1, 1, 4, 1, 4, 1, 7, 4, 2, 8, 6, 9, 35, 1, 1, 2, 2, 24, 2, 6, 13, 14, 6, 4, 7, 7, 3, 2, 8, 6, 20, 2, 4, 2, 1, 17, 1, 1, 6, 4, 21, 2, 6, 6, 29, 4, 7, 3, 8, 7, 11, 1, 5, 5, 8, 3, 2, 6, 1, 1, 4, 3, 4, 2, 1, 25, 2, 6, 12, 3, 2, 3, 2, 4, 3, 1, 1, 4, 2, 2, 10, 2, 8, 5, 2, 10, 12, 1, 6, 2, 2, 8, 9, 1, 1, 2, 16, 7, 11, 22, 4, 6, 89, 5, 3, 3, 1, 3, 2, 12, 6, 12, 3, 2, 4, 1, 16, 15, 14, 4, 15, 14, 3, 1, 3, 7, 4, 46, 1, 10, 70, 3, 4, 1, 2, 2, 10, 4, 2, 2, 1, 6, 12, 2, 24, 3, 3, 3, 1, 2, 8, 2, 1, 4, 3, 3, 10, 10, 4, 1, 6, 2, 6, 10, 9, 7, 2, 4, 6, 6, 6, 2, 3, 2, 2, 22, 2, 8, 4, 7, 2, 15, 2, 6, 11, 7, 5, 12, 3, 3, 1, 3, 10, 4, 15, 2, 2, 6, 2, 18, 8, 2, 2, 17, 4, 2, 43, 3, 2, 9, 13, 2, 1, 1, 3, 7, 3, 9, 16, 2, 6, 12, 12, 1, 2, 5, 1, 3, 4, 6, 3, 1, 2, 3, 1, 7, 4, 1, 1, 5, 3, 3, 1, 10, 9, 1, 2, 4, 4, 3, 40, 2, 2, 32, 1, 3, 4, 10, 4, 3, 3, 2, 4, 8, 6, 3, 2, 1, 8, 6, 2, 2, 2, 2, 6, 6, 3, 2, 2, 3, 4, 10, 1, 6, 25, 4, 14, 34, 1, 9, 45, 1, 2, 16, 5, 4, 4, 2, 1, 2, 16, 12, 7, 14, 3, 2, 6, 16, 13, 3, 3, 3, 9, 20, 2, 4, 1, 2, 4, 1, 7, 1, 4, 4, 16, 1, 2, 2, 4, 4, 2, 3, 2, 3, 6, 4, 11, 3, 1, 1, 1, 1, 6, 31, 6, 4, 1, 56, 12, 1]


def main():
    parser = utils.make_common_parser()
    args = parser.parse_args()
    data = read_data(DATA_DIR / args.input_file)

    res = do_challenge2(list(data))
    print(f"The value is: {res}")


def read_data(path: pathlib.Path) -> typing.List[str]:
    with path.open('r') as fi:
        res = (_.strip() for _ in fi.readlines())
    return res


SpringRow_T = typing.TypeVar("SprintRow")


@dataclasses.dataclass
class SpringRow:
    springs: str
    fault_groups: typing.Tuple[int]

    @staticmethod
    def from_string(input_str: str) -> SpringRow_T:
        springs, group_str = input_str.split(' ')
        groups = [int(x) for x in group_str.split(',')]

        springs = "?".join([springs]*UNFOLD_FACTOR)
        groups = groups * UNFOLD_FACTOR
        return SpringRow(springs, tuple(groups))

    def n_valid_possibilities(self):
        """Calculates the Number of Valid possibilities"""
        count = 0
        for config in gen_spring_configs(self.springs, self.fault_groups):
            if valid_groups(config, self.fault_groups):
                count += 1
        return count

    def n_ways_dyn(self):
        """Calculates the Number of Valid Possibilities"""
        ways = calc_total_ways(self.springs, self.fault_groups)
        return ways


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
        if s == UNKNOWN:
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

    return sum(counts)


def do_challenge2(data: typing.List[str]) -> int:
    # spring_rows = parse_data(data)
    # counts_good = []
    # for row in spring_rows:
    # counts_good.append(row.n_valid_possibilities())
    # We are going to do some Dynamic Programming to solve this.
    spring_rows = parse_data(data)
    counts = []
    for row in spring_rows:
        counts.append(row.n_ways_dyn())

    # print([i for i, _ in enumerate(CORRECT) if CORRECT[i] != counts[i]])
    # print("")
    # print(counts_good)
    # print("")
    # print(counts)
    return sum(counts)


@functools.lru_cache(maxsize=None)
def calc_total_ways(sequence: str, array: typing.List[int]):
    """Recursively find the number of ways the sequence can be made with the array"""
    if sum(array) > (sequence.count(DAMAGED) + sequence.count(UNKNOWN)):
        # We have messed up, we have ran out of room for the damaged we need
        return 0
    if sum(array) < sequence.count(DAMAGED):
        # We have messd up, there are too many damaged left
        return 0

    # If we are at the last Item, we know that all the values of DAMAGED must be complete
    n_damaged = array[0]
    total = 0
    if len(array) == 1:
        for i in list(get_valid_first_ends(sequence, n_damaged)):
            if not sequence[i:].count(DAMAGED):
                total += 1
        return total

    # Figure out how many ways we can legally put the first number of DAMAGED spring_rows
    total = 0
    # print(list(get_valid_first_ends(sequence, n_damaged)))
    for split_point in get_valid_first_ends(sequence, n_damaged):
        total += calc_total_ways(sequence[split_point:], array[1:])
    return total


def get_valid_first_ends(seq: str, n: int):
    if len(seq) == n:
        if all([c in (UNKNOWN, DAMAGED) for c in seq]):
            yield len(seq)
    else:
        if (i := seq.find(DAMAGED)) == -1:
            index = len(seq)
        else:
            index = i + n

        if len(seq) <= index:
            seq += WORKING
        # [('?', '?'), ('?', '?'), ('?', '?'), ('?', '?'), ('?', '#'), ('#', '?')]
        for i, s in enumerate(list(sliding_window(seq[:index+1], n=n+1))):
            if all([_ in (UNKNOWN, DAMAGED) for _ in s[:-1]]) and s[-1] != DAMAGED:
                # Valid group
                yield i + n + 1


def sliding_window(iterable, n):
    """Yoinked from itertools cookbook"""
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n-1), maxlen=n)
    for x in it:
        window.append(x)
        yield tuple(window)


if __name__ == "__main__":
    main()
