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

def get_legal_actions(marbles_collection):
    for i in filter(lambda i: len(marbles_collection[i]) > 0, range(len(marbles_collection))):  # 移動先でループします。ビーダマが入っている試験管は、他の試験管からビーダマが移動してきた可能性があります。
        for j in filter(lambda j: len(marbles_collection[j]) < test_tube_sizes[j] and j != i, range(len(marbles_collection))):  # 移動元でループします。ビーダマが満タンではない試験管は、他の試験管にビーダマを移動させられた可能性があります。
            if len(marbles_collection[j]) == 0:  # 移動元の試験管が空になった場合
                for k in range(1, min(len(marbles_collection[i]), test_tube_sizes[j]) + 1):
                    yield j, i, k
            elif len(marbles_collection[i]) == test_tube_sizes[i]:  # 移動先が満タンになった場合
                for k in range(1, min(test_tube_sizes[i], test_tube_sizes[j] - len(marbles_collection[j])) + 1):
                    yield j, i, k


# 次（ゲームでは一つ前）の状態を作成します。

def get_next_state(marbles_collection, action):
    from_index, to_index, move_count = action

    marbles_collection = list(marbles_collection)

    from_marbles = list(marbles_collection[from_index])
    to_marbles = list(marbles_collection[to_index])

    for _ in range(move_count):
        from_marbles.append(to_marbles.pop())

    marbles_collection[to_index] = tuple(to_marbles)
    marbles_collection[from_index] = tuple(from_marbles)

    return tuple(marbles_collection)


# ランダムに試験管とゴールを作成します。

rng = Random()

marbles = list(range(256))
rng.shuffle(marbles)

test_tube_count = rng.randint(3, MAX_TEST_TUBE_COUNT)

test_tube_sizes = tuple(map(lambda _: rng.randint(1, MAX_TEST_TUBE_SIZE),
                            range(test_tube_count)))

goal_marbles_collection = tuple(map(lambda i: tuple(map(lambda _: marbles[rng.randrange(MAX_MARBLE)],
                                                        range(rng.randint(0, test_tube_sizes[i])))),
                                    range(test_tube_count)))

print(test_tube_sizes, file=sys.stderr)
print(goal_marbles_collection, file=sys.stderr)

# 深さ優先探索して、すべての盤面を作成します。

stack = deque((goal_marbles_collection,))

graph = nx.DiGraph()
graph.add_node(goal_marbles_collection)

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

initial_marbles_collection, path_length = max(nx.shortest_path_length(graph, source=goal_marbles_collection).items(), key=second)

print(initial_marbles_collection, file=sys.stderr)
print(path_length, file=sys.stderr)

# nx.nx_agraph.to_agraph(graph).draw('graph.pdf', prog='dot')

# 問題を出力します。

print(test_tube_count)

for test_tube_size in test_tube_sizes:
    print(test_tube_size)

for test_tube in initial_marbles_collection:
    print(' '.join(map(lambda marble: f'{marble:02x}', test_tube)))

for test_tube in goal_marbles_collection:
    print(' '.join(map(lambda marble: f'{marble:02x}', test_tube)))
