import re
import sys


def read_lines():
    lines = []

    while True:
        try:
            lines.append(input())
        except EOFError:
            break

    return tuple(lines)


def report_error(message):
    print(message, file=sys.stderr)
    exit(1)


def get_test_tube_count(lines):
    if not len(lines) >= 1:
        report_error('試験管の数が見つかりません。')

    if not re.fullmatch(r'\d+', lines[0]):
        report_error('試験管の数は数値で記述してください。')

    test_tube_count = int(lines[0])

    if not (1 <= test_tube_count <= 64):
        report_error('試験管の数は1〜64にしてください。')

    return test_tube_count


def get_test_tube_sizes(lines, test_tube_count):
    if not len(lines) >= 1 + test_tube_count:
        report_error('試験管のサイズが見つかりません。')

    test_tube_sizes = []

    for i in range(test_tube_count):
        line = lines[1 + i]

        if not re.fullmatch(r'\d+', line):
            report_error(f'{i + 1}番目の試験管のサイズが不正です。試験管のサイズは数値で記述してください。')

        test_tube_size = int(line)

        if not (1 <= test_tube_size <= 32):
            report_error(f'{i + 1}番目の試験管のサイズが不正です。試験管のサイズは1〜64にしてください。')

        test_tube_sizes.append(test_tube_size)

    return tuple(test_tube_sizes)


def get_initial_test_tubes(lines, test_tube_count):
    if not len(lines) >= 1 + test_tube_count + test_tube_count:
        report_error('試験管の初期状態が見つかりません。')

    test_tubes = []

    for i in range(test_tube_count):
        line = lines[1 + test_tube_count + i]

        if not re.fullmatch(r'(|[a-f\d]{2}( [a-f\d]{2})*)', line):
            report_error(f'{i + 1}番目の試験管の初期状態が不正です。試験管の初期状態は空白区切りの16進数（a〜fは小文字）で記述してください。')

        test_tubes.append(tuple(map(lambda s: int(s, 16), line.split())))

    return tuple(test_tubes)


def get_answer_test_tubes(lines, test_tube_count):
    if not len(lines) >= 1 + test_tube_count + test_tube_count + test_tube_count:
        report_error('試験管の解答の状態が見つかりません。')

    test_tubes = []

    for i in range(test_tube_count):
        line = lines[1 + test_tube_count + test_tube_count + i]

        if not re.fullmatch(r'(|[a-f\d]{2}( [a-f\d]{2})*)', line):
            report_error(f'{i + 1}番目の試験管の解答の状態が不正です。試験管の解答の状態は空白区切りの16進数（a〜fは小文字）で記述してください。')

        test_tubes.append(tuple(map(lambda s: int(s, 16), line.split())))

    return tuple(test_tubes)


lines = read_lines()

test_tube_count = get_test_tube_count(lines)
test_tube_sizes = get_test_tube_sizes(lines, test_tube_count)
initial_test_tubes = get_initial_test_tubes(lines, test_tube_count)
answer_test_tubes = get_answer_test_tubes(lines, test_tube_count)

print(test_tube_sizes)
print(initial_test_tubes)
print(answer_test_tubes)
