import dataclasses
import math
import pathlib
import typing
import io

import utils

DATA_DIR = utils.get_data_dir(__file__)

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
    for row in reversed(expanded_rows):
        data.insert(row, "."*ncols)



    # Then calc distance of each galaxy


def do_challenge2(data: typing.List[str]) -> int:
    pass


if __name__ == "__main__":
    main()
