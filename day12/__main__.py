import collections
import itertools
import functools
import dataclasses
import pathlib
import typing

import utils

DATA_DIR = utils.get_data_dir(__file__)

UNFOLD_FACTOR = 1

WORKING = '.'
DAMAGED = '#'
UNKNOWN = '?'


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
    # We are going to do some Dynamic Programming to solve this.
    spring_rows = parse_data(data)
    counts = []
    for row in spring_rows:
        counts.append(row.n_ways_dyn())
    return sum(counts)


@functools.lru_cache(maxsize=None)
def calc_total_ways(sequence: str, array: typing.List[int]):
    """Recursively find the number of ways the sequence can be made with the array"""
    if sum(array) > (sequence.count(DAMAGED) + sequence.count(UNKNOWN)):
        # At this point we have failed, return 0
        return 0

    # Figure out how many ways we can legally put the first number of DAMAGED spring_rows
    n_damaged = array[0]
    if len(array) == 1:
        return len(list(get_valid_first_ends(sequence, n_damaged)))

    total = 0
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
            index = seq.find(DAMAGED) + n + 1

        if index == len(seq):
            window_size = n
        else:
            window_size = n + 1

        for i, s in enumerate(list(sliding_window(seq[:index], n=window_size))):
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
