import argparse
import pathlib
import dataclasses
import typing

BinaryNode_T = typing.TypeVar("BinaryNode")
T = typing.TypeVar("T")

@dataclasses.dataclass
class BinaryNode(typing.Generic[T]):
    key: T
    parent: typing.Optional[BinaryNode_T]
    left: typing.Optional[BinaryNode_T] = None
    right: typing.Optional[BinaryNode_T] = None

    def search(self, value: int) -> typing.Optional[T]:
        """searches for a value by key src"""
        node = self
        ret = None
        while node is not None:
            if value == node.key:
                ret = node.key
                break
            elif value < node.key:
                node = node.left
            else:
                node = node.right
        return ret

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

    def insert(self, key: T):
        node = self
        while node is not None:
            parent = node
            if key< node.key:
                node = node.left
            else:
                node = node.right
        new = BinaryNode(key=key, parent=parent)
        if key< parent.key:
            parent.left = new
        else:
            parent.right = new

    def in_order_walk(self) -> typing.List[T]:
        node = self.minimum()
        keys = []
        while node is not None:
            keys.append(node.key)
            node = node.successor()
        return keys




def make_common_parser()-> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file", default="test.txt")
    return parser



def get_data_dir(filename) -> pathlib.Path:
    """Gets The Data Directory and returns it as a pathlib.Path

    This assumes a similar setup structure for the files like so

        ParentDir/
            |
            |- __main__.py
            |- other.py
            |- data/

    filename should be __file__, called from __main__.py
    """
    PARENT = pathlib.Path(filename).absolute().parent
    DATA_DIR = PARENT / "data"
    return DATA_DIR
