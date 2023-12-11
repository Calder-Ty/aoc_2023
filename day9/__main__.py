import itertools
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
        res = (_.strip() for _ in fi.readlines())
    return res


def parse_data(data: typing.List[str]) -> typing.List[typing.List[int]]:
    outlines = []
    for line in data:
        outlines.append([int(v) for v in line.strip().split()])
    return outlines


def predict(records: typing.List[int]):
    deltas = []  # List of List of differences
    deltas.append(differences(records))
    while not all([_ == 0 for _ in deltas[-1]]):
        deltas.append(differences(deltas[-1]))

    total = 0
    for d in deltas:
        total += d[-1]
    total += records[-1]
    return total


def differences(record: typing.List[int]) -> typing.List[int]:
    # Calculate the differences using a window
    result = []
    for (x, y) in sliding_window(record, 2):
        result.append(y - x)
    assert len(record) - len(result) == 1, "Uh OH, should have lost one value"
    return result


# Yoinked from itertools cookbook
def sliding_window(iterable, n):
    # sliding_window('ABCDEFG', 4) --> ABCD BCDE CDEF DEFG
    it = iter(iterable)
    window = collections.deque(itertools.islice(it, n-1), maxlen=n)
    for x in it:
        window.append(x)
        yield tuple(window)


def do_challenge(data: typing.List[str]) -> int:
    records = parse_data(data)
    predictions = []
    for record in records:
        predictions.append(predict(record))

    return sum(predictions)


def do_challenge2(data: typing.List[str]) -> int:
    records = parse_data(data)
    predictions = []
    for record in records:
        # breakpoint()
        predictions.append(invent(record))

    print(predictions)

    return sum(predictions)


def invent(records: typing.List[int]):
    deltas = []  # List of List of differences
    deltas.append(differences(records))
    while not all([_ == 0 for _ in deltas[-1]]):
        deltas.append(differences(deltas[-1]))

    diff = 0
    for d in reversed(deltas[:-1]):
        diff = d[0] - diff
    res = records[0] - diff
    return res


if __name__ == "__main__":
    main()
