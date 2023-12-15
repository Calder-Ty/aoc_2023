import itertools
import math
import pathlib
import typing

import utils

DATA_DIR = utils.get_data_dir(__file__)
EXPAND_FACTOR = 10


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


def do_challenge(data: typing.List[str]) -> int:
    # First expand the universe
    ncols = len(data[0])
    nrows = len(data)
    expanded_cols = [1] * ncols
    expanded_rows = [1] * nrows
    for y, row in enumerate(data):
        for x, symbol in enumerate(row):
            if symbol == '#':
                expanded_cols[x] = 0
                expanded_rows[y] = 0

    # First expand the rows:
    for i, row in reversed(list(enumerate(expanded_rows))):
        if row == 0:
            continue
        print(f"Inserting into row {i}")
        data.insert(i, "."*ncols)

    for i, col in reversed(list(enumerate(expanded_cols))):
        if col == 0:
            continue
        print(f"Inserting into col {i}")
        for y, row in enumerate(data):
            data[y] = f"{row[:i]}.{row[i:]}"

    # Then calc distance of each galaxy
    galaxys = []
    for y, row in enumerate(data):
        for x, symbol in enumerate(row):
            if symbol == "#":
                galaxys.append((x, y))

    distances = []
    for a, b in itertools.combinations(galaxys, r=2):
        distances.append(manhattan_distance(a, b))

    return sum(distances)


def manhattan_distance(a: typing.Tuple[int, int], b: typing.Tuple[int, int]):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def do_challenge2(data: typing.List[str]) -> int:
    EXPAND_FACTOR = 1_000_000
    ncols = len(data[0])
    nrows = len(data)
    expanded_cols = [1] * ncols
    expanded_rows = [1] * nrows
    galaxys = []
    for y, row in enumerate(data):
        for x, symbol in enumerate(row):
            if symbol == '#':
                expanded_cols[x] = 0
                expanded_rows[y] = 0
                galaxys.append((x, y))

    distances = []
    for a, b in itertools.combinations(galaxys, r=2):
        # Compute the additional Rows and Cols for expansion
        xmin, xmax = min(a[0], b[0]), max(a[0], b[0])
        ymin, ymax = min(a[1], b[1]), max(a[1], b[1])
        n_cols = sum(expanded_cols[xmin:xmax])
        n_rows = sum(expanded_rows[ymin:ymax])
        distance = manhattan_distance(a, b)
        distances.append(distance + ((n_rows*EXPAND_FACTOR - n_rows) + (n_cols*EXPAND_FACTOR - n_cols)))

    return sum(distances)


if __name__ == "__main__":
    main()
