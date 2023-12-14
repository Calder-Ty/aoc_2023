import dataclasses
import math
import pathlib
import typing
import io

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
        # Remember 0, 0 is TOP LEFT
        match(from_coord.x - self.x, from_coord.y - self.y):
            case(1, 0):
                return WEST
            case(-1, 0):
                return EAST
            case(0, 1):
                return NORTH
            case(0, -1):
                return SOUTH
            case _:
                assert False, "Heading must be given to adjacent coords"

    def get_left(self, heading: str) -> typing.Optional[Coord_T]:
        match heading:
            case "north":
                return self.west()
            case "east":
                return self.north()
            case "south":
                return self.east()
            case "west":
                return self.south()
            case _:
                raise ValueError(f"Invalid heading {heading}")

    def get_right(self, heading: str) -> typing.Optional[Coord_T]:
        match heading:
            case "south":
                return self.west()
            case "west":
                return self.north()
            case "north":
                return self.east()
            case "east":
                return self.south()
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

    def neighbors(self) -> typing.List[Coord_T]:
        return [self.north(), self.west(), self.south(), self.east()]


def find_start(data: typing.List[str]):
    for y, row in enumerate(data):
        for x, symbol in enumerate(row):
            if symbol == "S":
                return Coord(x, y)


def do_challenge2(data: typing.List[str]) -> int:
    pipe_map = build_pipe_map(data)
    walker = PipeWalker(data, pipe_map)
    walker.walk()
    if walker.degree == 360:
        # Counterclockwise
        inside = walker.lefts
    elif walker.degree == -360:
        # Clockwise
        inside = walker.rights
    else:
        assert False, "Mistake made calculating turns"

    # now that we have the adjacent tiles that are in, but are not touching the inside
    others = set()
    for coord in inside:
        to_check = {coord}
        while to_check:
            c = to_check.pop()
            contained_neighbors = set(c.neighbors()).difference(others, inside, set(pipe_map))
            # breakpoint()
            others = others | contained_neighbors
            to_check = to_check | (contained_neighbors)
    print(others)

    with (DATA_DIR/"output.txt").open('w') as fi:
        for y in range(len(data)):
            line = io.StringIO()
            for x in range(len(data[0])):
                coord = Coord(x, y)
                if coord in pipe_map:
                    line.write("█")
                elif coord in inside:
                    line.write("I")
                elif coord in others:
                    line.write("O")
                else:
                    line.write(" ")
            line.write('\n')
            line.seek(0)

            fi.write(line.read())



    return len(inside) + len(others)


class PipeWalker():

    def __init__(self, data: typing.List[str], pipe_map: typing.List[Coord]):
        self.data = data
        self.pipe_map = pipe_map
        self.last = None
        self.lefts = set()
        self.rights = set()
        self.degree = 0

    def walk(self):
        # The last coord in the previous coord in the loop
        prev = self.pipe_map[-1]
        for coord in self.pipe_map:
            # Get Admin Data
            heading = coord.heading(prev)
            symbol = coord_to_symbol(self.data, coord)
            if symbol == "S":
                # Replace the S with the approprate symbol
                match coord.heading(prev), self.pipe_map[1].heading(coord):
                    case("east", "east") | ("west", "west"):
                        symbol = '-'
                    case("north", "north") | ("south", "south"):
                        symbol = '|'
                    case("east", "north") | ("south", "west"):
                        symbol = 'J'
                    case("east", "south") | ("north", "west"):
                        symbol = '7'
                    case("west", "north") | ("south", "east"):
                        symbol = 'L'
                    case("west", "south") | ("north", "east"):
                        symbol = 'F'
                    case _:
                        ValueError("Unreachable")

            self.add_left(heading, coord)
            self.add_right(heading, coord)

            # Now, handle turning:
            match symbol:
                case '|':
                    # a vertical pipe connecting north and south.
                    pass
                case '-':
                    # a horizontal pipe connecting east and west.
                    pass
                case 'L':
                    # print(coord)
                    # a 90-degree bend connecting north and east.
                    heading = NORTH if heading is WEST else EAST
                    if heading == NORTH:
                        self.degree -= 90
                        # print(f"{symbol}: heading {heading}, turned RIGHT, degrees is {self.degree}")
                    else:
                        self.degree += 90
                        # print(f"{symbol}: heading {heading}, turned LEFT, degrees is {self.degree}")
                case 'J':
                    # a 90-degree bend connecting north and west.
                    # print(coord)
                    heading = NORTH if heading is EAST else WEST
                    if heading == NORTH:
                        self.degree += 90
                        # print(f"{symbol}: heading {heading}, turned LEFT, degrees is {self.degree}")
                    else:
                        self.degree -= 90
                        # print(f"{symbol}: heading {heading}, turned RIGHT, degrees is {self.degree}")
                case '7':
                    # a 90-degree bend connecting south and west.
                    # print(coord)
                    heading = SOUTH if heading is EAST else WEST
                    if heading == SOUTH:
                        self.degree -= 90
                        # print(f"{symbol}: heading {heading}, turned RIGHT, degrees is {self.degree}")
                    else:
                        self.degree += 90
                        # print(f"{symbol}: heading {heading}, turned LEFT, degrees is {self.degree}")
                case 'F':
                    # a 90-degree bend connecting south and east.
                    # print(coord)
                    heading = SOUTH if heading is WEST else EAST
                    if heading == SOUTH:
                        self.degree += 90
                        # print(f"{symbol}: heading {heading}, turned LEFT, degrees is {self.degree}")
                    else:
                        self.degree -= 90
                        # print(f"{symbol}: heading {heading}, turned RIGHT, degrees is {self.degree}")
                case _:
                    assert False, f"Unreachable, got symbol: {symbol}"
            self.add_left(heading, coord)
            self.add_right(heading, coord)
            prev = coord

    def add_left(self, heading: str, coord: Coord):
        if left := coord.get_left(heading):
            if left not in self.pipe_map:
                self.lefts.add(left)

    def add_right(self, heading: str, coord: Coord):
        if right := coord.get_right(heading):
            if right not in self.pipe_map:
                self.rights.add(right)


def coord_to_symbol(data: typing.List[str], coord: Coord):
    if coord.y >= 0 and coord.y < len(data) and coord.x >=0 and coord.x < len(data[0]):
        return data[coord.y][coord.x]


def build_pipe_map(data):
    """Builds out Map of pipes"""
    # First Build the map
    start = find_start(data)
    # Then Do A search from each direction till we find out what to do
    for (coord, dir) in [(start.north(), NORTH), (start.west(), WEST), (start.south(), SOUTH), (start.east(), EAST)]:
        # Do validation
        if coord is None:
            continue
        if (
            dir == NORTH and
            coord_to_symbol(data, coord) in ("L", "J", "-", ".")
        ) or (
            dir == SOUTH and
            coord_to_symbol(data, coord) in ("7", "F", "-", ".")
        ) or (
            dir == WEST and
            coord_to_symbol(data, coord) in ("7", "J", "|", ".")
        ) or (
            dir == EAST and
            coord_to_symbol(data, coord) in ("F", "L", "|", ".")
        ):
            # Invalid Symbol to move from start
            continue

        path = find_pipe_path(start, coord, data)
        if path:
            break
    return path


def find_pipe_path(start, dir, data) -> typing.List[Coord]:
    max_rows = len(data)
    max_cols = len(data[0])
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
