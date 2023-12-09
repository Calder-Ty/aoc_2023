import functools
import dataclasses
import collections
import pathlib
import sys
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


@dataclasses.dataclass
class GameRecords:
    times: typing.List[int]
    distances: typing.List[int]


def do_challenge(data: typing.List[str]) -> int:
    races = parse_data(data)
    ways_to_win = [0] * len(races.times)
    for i, (time, dist) in enumerate(zip(races.times, races.distances)):
        for t in range(time):
            speed = t  # millimeters per second
            remain = time - t
            if speed * remain > dist:
                ways_to_win[i] += 1
    print(ways_to_win)
    return functools.reduce(lambda x, y: x*y, ways_to_win)


def parse_data(data: typing.List[str]) -> GameRecords:
    for line in data:
        match line.split(':'):
            case["Time", times_str]:
                times = [int(_) for _ in times_str.strip().split()]
            case["Distance", dist_str]:
                dist = [int(_) for _ in dist_str.strip().split()]
            case _:
                raise ValueError(f"Malformated Input: {line}")
    return GameRecords(times, dist)


def travel_distance(charge_time, total_time):
    return total_time - charge_time * charge_time


def do_challenge2(data: typing.List[str]) -> int:
    races = parse_data2(data)
    ways_to_win = 0
    time = races.times
    dist = races.distances
    for t in range(time):
        speed = t  # millimeters per second
        remain = time - t
        if speed * remain > dist:
            ways_to_win += 1
    return ways_to_win


def parse_data2(data: typing.List[str]) -> GameRecords:
    for line in data:
        match line.split(':'):
            case["Time", times_str]:
                times = int(times_str.strip().replace(' ', ""))
            case["Distance", dist_str]:
                dist = int(dist_str.strip().replace(' ', ""))
            case _:
                raise ValueError(f"Malformated Input: {line}")
    return GameRecords(times, dist)


if __name__ == "__main__":
    main()
