import collections
import dataclasses
import pathlib
import typing
import math

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

class Edges(typing.NamedTuple):
    left: str
    right: str

def parse_data(data):
    instructions = data[0]
    nodes = {}
    for line in data[2:]:
        node, sEdges = line.split(' = ')
        left, right = sEdges.strip('()').split(', ')
        edges = Edges(left, right)
        nodes[node] = edges
    return instructions, nodes



def do_challenge(data: typing.List[str]) -> int:
    instructions, nodes = parse_data(list(data))
    node = "AAA"
    edges = nodes[node]
    count = 0
    print(instructions)
    dirs = iter_instructions(instructions)
    while True:
        dir = next(dirs)
        print(f"{node}: {edges}")
        print(dir)
        count += 1
        match dir:
            case "L":
                node = edges.left
                edges = nodes[node]
            case "R":
                node = edges.right
                edges = nodes[node]
        if node == "ZZZ":
            break
    return count


def iter_instructions(pattern: str):
    while pattern:
        for c in pattern:
            yield c


def do_challenge2(data: typing.List[str]) -> int:
    instructions, graph = parse_data(list(data))
    nodes = [k for k in graph.keys() if k[-1] == "A"]
    cycle_counts = [None] * len(nodes)
    count = 0
    print(instructions)
    dirs = iter_instructions(instructions)
    while any(nodes):
        dir = next(dirs)
        count += 1
        for i, node in enumerate(nodes):
            if node is None:
                continue
            match dir:
                case "L":
                    nodes[i] = graph[node].left
                case "R":
                    nodes[i] = graph[node].right

        for i, node in enumerate(nodes):
            if node is None:
                continue
            if node[-1] == 'Z':
                print(f"{i}: {count} / {len(instructions)} = {count/len(instructions)}")
                nodes[i] = None
                cycle_counts[i] = count

    return math.lcm(*cycle_counts)







if __name__ == "__main__":
    main()
