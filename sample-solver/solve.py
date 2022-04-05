from collections import deque
from itertools import product


# 保守性を上げるために、ゲームのルールを抽出しておきます。
class Game:
    def __init__(self, question):
        self.test_tube_sizes, self.initial_marbles_collection, self.goal_marbles_collection = question

    def get_initial_state(self):
        return self.initial_marbles_collection

    def is_goal(self, marbles_collection):
        return marbles_collection == self.goal_marbles_collection

    def get_legal_actions(self, marbles_collection):
        return filter(lambda action: action[0] != action[1],
                      product(filter(lambda i: len(marbles_collection[i]) > 0, range(len(marbles_collection))),
                              filter(lambda i: len(marbles_collection[i]) < self.test_tube_sizes[i], range(len(marbles_collection)))))

    def get_next_state(self, marbles_collection, action):
        # タプルは変更できないのでリストに変換して、リストはハッシュ化できないのでタプルに変換しています。。。

        from_index, to_index = action

        marbles_collection = list(marbles_collection)

        from_marbles = list(marbles_collection[from_index])
        to_marbles = list(marbles_collection[to_index])

        while len(from_marbles) > 0 and len(to_marbles) < self.test_tube_sizes[to_index]:
            to_marbles.append(from_marbles.pop())

        marbles_collection[to_index] = tuple(to_marbles)
        marbles_collection[from_index] = tuple(from_marbles)

        return tuple(marbles_collection)


# 問題を読み込みます。
def read_question():
    def read_test_tube_sizes(test_tube_count):
        for _ in range(test_tube_count):
            yield int(input())

    def read_marbles_collection(test_tube_count):
        for _ in range(test_tube_count):
            yield tuple(map(lambda marble: int(marble, 16), input().split()))

    test_tube_count = int(input())

    return (tuple(read_test_tube_sizes(test_tube_count)),
            tuple(read_marbles_collection(test_tube_count)),
            tuple(read_marbles_collection(test_tube_count)))


# 幅優先探索で問題をときます。
def solve(question):
    game = Game(question)

    queue = deque((((), game.get_initial_state()),))
    visited_states = set((game.get_initial_state(),))

    while queue:
        actions, state = queue.popleft()

        if game.is_goal(state):
            return actions

        for action in game.get_legal_actions(state):
            next_state = game.get_next_state(state, action)

            if next_state in visited_states:
                continue

            visited_states.add(next_state)
            queue.append((actions + (action,), next_state))

    return ()  # 手本の状態にできない問題の場合の考慮をしていないので、何もしない解答を作成します。


# 解答を出力します。
def write_answer(actions):
    for from_index, to_index in actions:
        print(f'{from_index} {to_index}')


write_answer(solve(read_question()))
