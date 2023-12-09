"""Advent Of Code Day 1, 2023"""
import pathlib
import re
import typing

import utils

DATA_DIR = utils.get_data_dir(__file__)
TEXT_DIGITS = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

path = pathlib.Path("my/data/prod.txt")
# path = pathlib.Path("my/data/test.xt")


def main():
    parser = utils.make_common_parser()
    args = parser.parse_args()
    data = read_data(DATA_DIR / args.input_file)

    res = do_challenge(data)
    print(f"The value is: {res}")


def read_data(path: pathlib.Path) -> typing.List[str]:
    with path.open('r') as fi:
        res = fi.readlines()
    return res


def do_challenge(data: typing.List[str]):
    nums = [line_value(line) for line in data]
    print(nums)
    return sum(nums)


def line_value(line: str):
    first = None
    first_buff = ""
    last = None
    last_buff = ""
    for c in line:
        if c.isdigit():
            first = c
            break
        else:
            first_buff += c
            # Is the buffer a number?
            if val := has_text_number_from_front(first_buff):
                first = val
                break

    for c in reversed(line):
        if c.isdigit():
            last = c
            break
        else:
            last_buff = c + last_buff
            # Is the buffer a number?
            if val := has_text_number_from_back(last_buff):
                last = val
                break
    return int(str(first) + str(last))


def has_text_number_from_front(text: str) -> int:
    start = None
    val = 0
    for txt, v in TEXT_DIGITS.items():
        if res := re.search(txt, text):
            if start is None or res.start() < start:
                val = v
    return val


def has_text_number_from_back(text: str) -> int:
    end = 0
    val = 0
    for txt, v in TEXT_DIGITS.items():
        if res := re.search(txt, text):
            if res.end() > end:
                val = v
    return val


if __name__ == '__main__':
    main()
