import pathlib
import typing
import io
import sys

sys.path.append('..')

# fmt: off
import utils
# fmt: on

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


class Map:

    def __init__(self, data: typing.List[str]):
        self.row_wise = data
        self.col_wise = transpose(data)

    def reflection_score(self):
        if i := find_reflection(self.row_wise):
            return (i) * 100
        else:
            return find_reflection(self.col_wise)

    def reflection_score_smuged(self):
        for y, row in enumerate(self.row_wise):
            old_row = row
            for x, symbol in enumerate(old_row):
                old_col = self.col_wise[x]
                self.col_wise[x] = old_col[:y] + clean_smduge(symbol) + old_col[y+1:]
                self.row_wise[y] = old_row[:x] + clean_smduge(symbol) + old_row[x+1:]

                if i := reflects_on_line(self.row_wise, y):
                    return (i) * 100
                elif i := reflects_on_line(self.col_wise, x):
                    return i
                else:
                    pass
                self.col_wise[x] = old_col
                self.row_wise[y] = old_row


def clean_smduge(symbol: str):
    match symbol:
        case '#':
            return '.'
        case '.':
            return '#'


def transpose(data: typing.List[str]) -> typing.List[str]:
    rows = [io.StringIO() for _ in range(len(data[0]))]
    for row in data:
        for i, c in enumerate(row):
            rows[i].write(c)
    for row in rows:
        row.seek(0)

    return [row.read() for row in rows]


def find_reflection(data: typing.List[str]) -> typing.Optional[int]:
    for i in range(1, len(data)):
        if i > len(data)//2:
            right = data[i:]
            left = data[i-len(right):i]
        else:
            left = data[:i]
            right = data[i:i+len(left)]
        if list(reversed(right)) == left:
            return i


def reflects_on_line(data: typing.List[str], linenum: int) -> typing.Optional[int]:
    for i in range(1, len(data)):
        if i > len(data)//2:
            right = data[i:]
            left = data[i-len(right):i]
        else:
            left = data[:i]
            right = data[i:i+len(left)]
        if linenum < i and i-len(right) > linenum:
            continue
        if linenum > i and i+len(right) - 1 < linenum:
            continue
        if list(reversed(right)) == left:
            return i


def do_challenge(data: typing.List[str]) -> int:
    rows = []
    maps = []
    for row in data:
        if row:
            rows.append(row)
        else:
            maps.append(Map(rows))
            rows = []

    print(len(maps))

    scores = []
    for m in maps:
        scores.append(m.reflection_score())
    print(scores)
    return sum(scores)


def do_challenge2(data: typing.List[str]) -> int:
    rows = []
    maps = []
    for row in data:
        if row:
            rows.append(row)
        else:
            maps.append(Map(rows))
            rows = []

    print(len(maps))

    scores = []
    for m in maps:
        scores.append(m.reflection_score_smuged())
    print(scores)
    return sum(scores)


if __name__ == "__main__":
    main()
