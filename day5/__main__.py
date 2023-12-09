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
        res = fi.readlines()
    return res


@dataclasses.dataclass
class MapLine:

    dest_start: int
    src_min: int
    src_max: int
    count: int

    @staticmethod
    def from_string(in_str):
        dest_start, src_min, count = [int(_) for _ in in_str.strip().split()]
        # Oh Map Line is Inclusive I forgot I Did that
        return MapLine(dest_start, src_min, src_min + count - 1, count)

    def to_dest(self, value):
        return self.dest_start + (value - self.src_min)

    def to_dest_range(self, value):
        """Gives range for values, from value to end of the range of mapped values"""
        return (self.dest_start + (value - self.src_min) , self.dest_start + self.count - 1)


BinaryNode_T = typing.TypeVar("BinaryNode")


@dataclasses.dataclass
class BinaryNode:
    key: MapLine
    parent: typing.Optional[BinaryNode_T]
    left: typing.Optional[BinaryNode_T] = None
    right: typing.Optional[BinaryNode_T] = None

    def search(self, value: int):
        """searches for a value by key src"""
        node = self
        while node is not None:
            if value >= node.key.src_min and value <= node.key.src_max:
                value = node.key.to_dest(value)
                break
            elif value < node.key.src_min:
                node = node.left
            else:
                node = node.right
        return value

    def search_range(self, value: int):
        """searches for a value and returns the range associated with that value"""
        node = self
        while node is not None:
            parent = node
            if value >= node.key.src_min and value <= node.key.src_max:
                # This range is inclusive
                value = node.key.to_dest_range(value)
                break
            elif value < node.key.src_min:
                node = node.left
                if node is None:
                    # This Value is Inclusive
                    value = (value, parent.key.src_min - 1)
            else:
                node = node.right
                if node is None:
                    n = parent.successor()
                    # This value is inclusive
                    value = (value, n.key.src_min - 1 if n else sys.maxsize)
        return value

    def successor(self) -> typing.Optional[BinaryNode_T]:
        node = self
        if node.right is not None:
            return node.right.minimum()
        parent = node.parent
        while parent is not None and node == parent.right:
            node = parent
            parent = node.parent
        return parent

    def minimum(self) -> BinaryNode_T:
        x = self
        while x.left is not None:
            x = x.left
        return x

    def maximum(self) -> BinaryNode_T:
        x = self
        while x.right is not None:
            x = x.right
        return x


def insert_range(tree: BinaryNode, key: MapLine):
    node = tree
    while node is not None:
        parent = node
        if key.src_min < node.key.src_min:
            node = node.left
        else:
            node = node.right
    new = BinaryNode(key=key, parent=parent)
    if key.src_min < parent.key.src_min:
        parent.left = new
    else:
        parent.right = new


def make_map_tree(map_lines: typing.List[MapLine]) -> BinaryNode:
    tree = BinaryNode(key=map_lines[0], parent=None)
    for line in map_lines[1:]:
        insert_range(tree, line)
    return tree


def do_challenge(data: typing.List[str]) -> int:
    gen = (line.strip() for line in data)

    map_trees = []
    seeds = []
    for line in gen:
        match line.split(':'):
            case["seeds", values]:
                seeds = values.strip().split()

            case[label, _]:
                # We are going to loop over the lines until we
                map_lines = []
                while map_line := next(gen):
                    map_lines.append(MapLine.from_string(map_line))
                map_trees.append(make_map_tree(map_lines))

            case[""]:
                continue

            case _:
                assert False, "Unreachable"

    min_location = None

    for seed in seeds:
        dest = int(seed)
        print(f"seed {seed}")
        for tree in map_trees:
            dest = tree.search(dest)

        loc = dest
        if min_location is None or int(loc) < min_location:
            min_location = int(loc)
    return min_location


def do_challenge2(data: typing.List[str]) -> int:
    gen = (line.strip() for line in data)

    map_trees = []
    seeds = []
    for line in gen:
        match line.split(':'):
            case["seeds", values]:
                seeds = values.strip().split()

            case[label, _]:
                # We are going to loop over the lines until we
                map_lines = []
                while map_line := next(gen):
                    map_lines.append(MapLine.from_string(map_line))
                map_trees.append(make_map_tree(map_lines))

            case[""]:
                continue

            case _:
                assert False, "Unreachable"

    min_location = None

    seeds = zip(*[iter(seeds)]*2)
    # This fancy zip trick will group every two numbers
    dest_ranges = []
    splits = {(int(low), int(low)+int(count)-1) for (low, count) in seeds}
    # print(f"Seeds: {splits}")
    for tree in map_trees:
        new = []
        for s in splits:
            new.extend(split_ranges(tree,s))
        splits = set(new)
        # print(splits)

    min_location = min(set(splits), key= lambda x: x[0])

    return min_location[0]




def split_ranges(tree: BinaryNode, in_range: typing.Tuple[int, int]):
    """Takes a range and uses the map func to split the range into a destination range"""
    splits = []
    rng = in_range
    min_v = in_range[0]
    max_v = in_range[1]
    span = (max_v - min_v)
    while span > 0:
        # print(f"Searching span: {rng}")
        rng = tree.search_range(min_v)
        if span > rng[1]-rng[0]:
            splits.append(rng)
        else:
            splits.append((rng[0], rng[0] + span))
        # Ranges from search are inclusively matched?
        min_v += (rng[1] - rng[0]) + 1
        span -= (rng[1] - rng[0]) + 1
    return splits


if __name__ == "__main__":
    main()
