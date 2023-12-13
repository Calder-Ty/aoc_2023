import dataclasses
import math
import pathlib
import typing

import utils

DATA_DIR = utils.get_data_dir(__file__)

NORTH = "north"
SOUTH = "south"
EAST = "east"
WEST = "west"


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
    max_rows = len(data)
    max_cols = len(data[0])
    # First Build the map
    start = find_start(data)
    # Then Do A search from each direction till we find out what to do
    for dir in [start.north(), start.west(), start.south(), start.east()]:
        # Do validation
        current = dir
        path = {start}
        while current:
            if (
                    current.x >= max_cols
                    or current.x < 0
                    or current.y >= max_rows
                    or current.y < 0
            ):
                # Fallen off the map
                path = None
                break

            path.add(current)

            match data[current.y][current.x]:
                case '|':
                    # a vertical pipe connecting north and south.
                    next = {current.north(), current.south()}
                case '-':
                    # a horizontal pipe connecting east and west.
                    next = {current.west(), current.east()}
                case 'L':
                    # a 90-degree bend connecting north and east.
                    next = {current.north(), current.east()}
                case 'J':
                    # a 90-degree bend connecting north and west.
                    next = {current.north(), current.west()}
                case '7':
                    # a 90-degree bend connecting south and west.
                    next = {current.west(), current.south()}
                case 'F':
                    # a 90-degree bend connecting south and east.
                    next = {current.east(), current.south()}
                case '.':
                    # Reset
                    path = None
                    break
                case _:
                    assert False, "Unreachable"

            # We are only adding visited pipes and so the next pipe will always only have 1
            # Coord that isn't visited yet
            current = next.difference(path)
            if current:
                current = current.pop()

        if path:
            return math.ceil(len(path)/2)


Coord_T = typing.TypeVar("Coord")


class Coord(typing.NamedTuple):
    x: int
    y: int

    def heading(self, from_coord: Coord_T):
        """Give the direction traveled from a coord to the current"""
        match(from_coord.x - self.x, from_coord.y - self.y):
            case(1, 0):
                return EAST
            case(-1, 0):
                return WEST
            case(0, 1):
                return NORTH
            case(0, -1):
                return SOUTH
            case _:
                assert False, "Heading must be given to adjacent coords"

    def get_left(self, heading: str) -> Coord_T:
        match heading:
            case NORTH:
                self.west()
            case EAST:
                self.north()
            case SOUTH:
                self.east()
            case WEST:
                self.south()
            case _:
                raise ValueError(f"Invalid heading {heading}")

    def get_left(self, heading: str) -> Coord_T:
        match heading:
            case SOUTH:
                self.west()
            case WEST:
                self.north()
            case NORTH:
                self.east()
            case EAST:
                self.south()
            case _:
                raise ValueError(f"Invalid heading {heading}")

    def north(self) -> Coord_T:
        # 0, 0 is in the top left corner
        return Coord(self.x, self.y-1)

    def south(self) -> Coord_T:
        # 0, 0 is in the top left corner
        return Coord(self.x, self.y+1)

    def west(self) -> Coord_T:
        # 0, 0 is in the top left corner
        return Coord(self.x-1, self.y)

    def east(self) -> Coord_T:
        # 0, 0 is in the top left corner
        return Coord(self.x+1, self.y)


def find_start(data: typing.List[str]):
    for y, row in enumerate(data):
        for x, symbol in enumerate(row):
            if symbol == "S":
                return Coord(x, y)


def do_challenge2(data: typing.List[str]) -> int:
    pipe_map = build_pipe_map(data)
    lefts = []
    rights = []
    degree


class PipeWalker():

    def __init__(self, data: typing.List[str], pipe_map: typing.List[Coord]):
        self.data = data
        self.pipe_map = pipe_map
        self.last = None
        self.lefts = set()
        self.rights = set()
        self.degree = 0

    def walk(self):
        prev = pipe_map[0]
        for coord in pipe_map[1:]:
            # Get Admin Data
            heading = coord.heading(prev)
            symbol = coord_to_symbol(self.data, coord)
            self.check_left_right(heading)

            # Now, handle turning:
            match symbol:
                case '|':
                    # a vertical pipe connecting north and south.
                    pass
                case '-':
                    # a horizontal pipe connecting east and west.
                    pass
                case 'L':
                    # a 90-degree bend connecting north and east.
                    heading = NORTH if heading is WEST else EAST
                    if heading == NORTH:
                        self.degree -= 90
                    else:
                        self.degree += 90
                case 'J':
                    # a 90-degree bend connecting north and west.
                    heading = NORTH if heading is EAST else WEST
                    if heading == NORTH:
                        self.degree += 90
                    else:
                        self.degree -= 90
                case '7':
                    # a 90-degree bend connecting south and west.
                    heading = SOUTH if heading is EAST else WEST
                case 'F':
                    # a 90-degree bend connecting south and east.
                    heading = SOUTH if heading is WEST else EAST
                case _:
                    assert False, "Unreachable"

            self.check_left_right(heading)

    def check_left_right(self, heading: str):
        left = coord_to_symbol(self.data, coord.get_left(heading))
        right = coord_to_symbol(self.data, coord.get_right(heading))

        if left = ".":
            self.lefts.add(left)
        if right = ".":
            self.rights.add(right)


def coord_to_symbol(data: typing.List[str], coord: Coord):
    return data[coord.y][coord.x]


def build_pipe_map(data):
    """Builds out Map of pipes"""
    max_rows = len(data)
    max_cols = len(data[0])
    # First Build the map
    start = find_start(data)
    # Then Do A search from each direction till we find out what to do
    for dir in [start.north(), start.west(), start.south(), start.east()]:
        # Do validation
        path = find_pipe_path(dir)
        if path:
            break
    return path


def find_pipe_path(dir) -> typing.List[Coord]:
    current = dir
    path = [start]
    while current:
        if (
                current.x >= max_cols
                or current.x < 0
                or current.y >= max_rows
                or current.y < 0
        ):
            # Fallen off the map
            path = None
            break

        path.append(current)

        match data[current.y][current.x]:
            case '|':
                # a vertical pipe connecting north and south.
                next = {current.north(), current.south()}
            case '-':
                # a horizontal pipe connecting east and west.
                next = {current.west(), current.east()}
            case 'L':
                # a 90-degree bend connecting north and east.
                next = {current.north(), current.east()}
            case 'J':
                # a 90-degree bend connecting north and west.
                next = {current.north(), current.west()}
            case '7':
                # a 90-degree bend connecting south and west.
                next = {current.west(), current.south()}
            case 'F':
                # a 90-degree bend connecting south and east.
                next = {current.east(), current.south()}
            case '.':
                # Reset
                path = None
                break
            case _:
                assert False, "Unreachable"

        # We are only adding visited pipes and so the next pipe will always only have 1
        # Coord that isn't visited yet, until it gets to the start
        current = next.difference(set(path))
        if current:
            current = current.pop()
    return path


if __name__ == "__main__":
    main()
