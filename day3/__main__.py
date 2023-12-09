import collections
import dataclasses
import enum
import itertools
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
        res = fi.readlines()
    return res


class States(enum.Enum):
    NotNumber = 1
    Number = 2


class SchemaIndex(typing.NamedTuple):
    x: int
    y: int


class PartNumberParser:
    """A State Machine for Parsing Part Numbers from the Schematic"""

    def __init__(self, schematic):
        self.schematic = schematic
        self.state = States.NotNumber
        self.start_index: typing.Optional[SchemaIndex] = None
        self.end_index: typing.Optional[SchemaIndex] = None

        self.part_numbers = []
        # Map Index of Gear to list of attatched numbers []
        self.gears = collections.defaultdict(list)

    def parse(self):
        print(f"({len(self.schematic[0])}, {len(self.schematic)})")
        for y, line in enumerate(self.schematic):
            for x, _ in enumerate(line):
                self.advance(SchemaIndex(x, y))

    def advance(self, index: SchemaIndex):
        """Entrypoint to the parse machine"""
        char = self.schematic[index.y][index.x]
        match(self.state):
            case States.NotNumber:
                if char.isdigit():
                    self.state = States.Number
                    self.start_index = index
                    self.end_index = index
            case States.Number:
                # Keep Counting
                if char.isdigit():
                    self.end_index = index

                    # At the end of a line we need to reset
                    if self.end_index.x == len(self.schematic[0]) - 1:
                        self.end_index = SchemaIndex(self.end_index.x + 1, self.end_index.y)
                        self.check_for_neighbors()
                        self.reset()
                # No More Numbers! Look for neighbor symbols
                else:
                    self.end_index = index
                    self.check_for_neighbors()
                    self.reset()

    def check_for_neighbors(self):
        num = self.schematic[self.start_index.y][self.start_index.x:self.end_index.x]
        neighbors = self.get_neighbor_indexes()
        added = False
        for index in neighbors:
            assert index.y < len(self.schematic), f"index y {index.y} is invalid"
            assert index.x < len(self.schematic[0]), f"index x {index.x} is invalid"
            char: str = self.schematic[index.y][index.x]

            if not char.isdigit() and not char == '.':
                # Has neighbor:
                assert all((x.isdigit for x in num)), f"Malformed number: {num} at index {index}"
                assert num != "", f"Error: empty number at index: {self.start_index}"
                # If we haven't noted this number yet, do so
                if not added:
                    added = True
                    self.part_numbers.append(int(num))

                # If Gear Note it down
                if char == "*":
                    self.gears[index].append(int(num))

    def get_neighbor_indexes(self):
        up = self.start_index.y - 1
        down = self.start_index.y + 1
        left = max(self.start_index.x - 1, 0)
        right = min(self.end_index.x + 1, len(self.schematic[0]))

        neighbors = []
        if up > 0:
            neighbors.extend((SchemaIndex(x, up) for x in range(left, right)))

        if down < len(self.schematic):
            neighbors.extend((SchemaIndex(x, down) for x in range(left, right)))

        if self.start_index.x - 1 > 0:
            neighbors.append(SchemaIndex(left, self.start_index.y))

        if self.end_index.x + 1 < len(self.schematic[0]):
            neighbors.append(SchemaIndex(right - 1, self.start_index.y))
        return neighbors

    def reset(self):
        self.state = States.NotNumber
        self.start_index = None
        self.end_index = None


def do_challenge(data: typing.List[str]) -> int:
    schematic = [line.strip() for line in data]
    parser = PartNumberParser(schematic)
    parser.parse()
    print(parser.part_numbers)
    return sum(parser.part_numbers)


def do_challenge2(data: typing.List[str]) -> int:
    schematic = [line.strip() for line in data]
    parser = PartNumberParser(schematic)
    parser.parse()
    print(parser.gears)
    count = 0
    for gear, nums in parser.gears.items():
        if len(nums) == 2:
            count += nums[0] * nums[1]
    return count


if __name__ == "__main__":
    main()
