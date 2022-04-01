import networkx as nx
import sys

from collections import deque
from funcy import second
from random import Random


# ルール上は試験管の数の最大値は64、試験管のサイズの最大値は64、ビーダマの色は255ですけど、探索が終わらなそうなので制限してみました。

MAX_TEST_TUBE_COUNT = 4
MAX_TEST_TUBE_SIZE = 4
MAX_MARBLE = 4 - 1


# アクション（ゲームで移動先になる試験管のインデックス、ゲームで移動もとになる試験管のインデックス、移動するビーダマの数）の集合を取得します。

def get_legal_actions(test_tubes):
    for i in filter(lambda i: len(test_tubes[i]) > 0, range(len(test_tubes))):  # 移動先でループします。ビーダマが入っている試験管は、他の試験管からビーダマが移動してきた可能性があります。
        for j in filter(lambda j: len(test_tubes[j]) < test_tube_sizes[j] and j != i, range(len(test_tubes))):  # 移動元でループします。ビーダマが満タンではない試験管は、他の試験管にビーダマを移動させられた可能性があります。
            if len(test_tubes[j]) == 0:  # 移動元の試験管が空になった場合
                for k in range(1, min(len(test_tubes[i]), test_tube_sizes[j]) + 1):
                    yield j, i, k
            elif len(test_tubes[i]) == test_tube_sizes[i]:  # 移動先が満タンになった場合
                for k in range(1, min(test_tube_sizes[i], test_tube_sizes[j] - len(test_tubes[j])) + 1):
                    yield j, i, k


# 次（ゲームでは一つ前）の状態を作成します。

def get_next_state(test_tubes, action):
    from_index, to_index, move_count = action

    test_tubes = list(test_tubes)

    from_test_tube = list(test_tubes[from_index])
    to_test_tube = list(test_tubes[to_index])

    for _ in range(move_count):
        from_test_tube.append(to_test_tube.pop())

    test_tubes[to_index] = tuple(to_test_tube)
    test_tubes[from_index] = tuple(from_test_tube)

    return tuple(test_tubes)


# ランダムに試験管とゴールを作成します。

rng = Random()

marbles = list(range(256))
rng.shuffle(marbles)

test_tube_count = rng.randint(3, MAX_TEST_TUBE_COUNT)

test_tube_sizes = tuple(map(lambda _: rng.randint(1, MAX_TEST_TUBE_SIZE),
                            range(test_tube_count)))

answer_test_tubes = tuple(map(lambda i: tuple(map(lambda _: marbles[rng.randrange(MAX_MARBLE)],
                                                  range(rng.randint(0, test_tube_sizes[i])))),
                              range(test_tube_count)))

print(test_tube_sizes, file=sys.stderr)
print(answer_test_tubes, file=sys.stderr)

# 深さ優先探索して、すべての盤面を作成します。

stack = deque((answer_test_tubes,))

graph = nx.DiGraph()
graph.add_node(answer_test_tubes)

while stack:
    state = stack.pop()

    for action in get_legal_actions(state):
        next_state = get_next_state(state, action)

        if graph.has_node(next_state):
            graph.add_edge(state, next_state)
            continue

        graph.add_node(next_state)
        graph.add_edge(state, next_state)

        stack.append(next_state)

# ゴールから最も遠いノードを探します。

question_test_tubes, path_length = max(nx.shortest_path_length(graph, source=answer_test_tubes).items(), key=second)

print(question_test_tubes, file=sys.stderr)
print(path_length, file=sys.stderr)

# nx.nx_agraph.to_agraph(graph).draw('graph.pdf', prog='dot')

# 問題文を出力します。

print(test_tube_count)

for test_tube_size in test_tube_sizes:
    print(test_tube_size)

for test_tube in question_test_tubes:
    print(' '.join(map(lambda marble: f'{marble:02x}', test_tube)))

for test_tube in answer_test_tubes:
    print(' '.join(map(lambda marble: f'{marble:02x}', test_tube)))
