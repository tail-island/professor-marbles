from collections import deque
from itertools import product


# 保守性を上げるために、ゲームのルールを抽出しておきます。
class Game:
    def __init__(self, question):
        self.test_tube_sizes, self.initial_test_tubes, self.answer_test_tubes = question

    def get_initial_state(self):
        return self.initial_test_tubes

    def has_finished(self, test_tubes):
        return test_tubes == self.answer_test_tubes

    def get_legal_actions(self, test_tubes):
        return filter(lambda action: action[0] != action[1],
                      product(filter(lambda i: len(test_tubes[i]) > 0, range(len(test_tubes))),
                              filter(lambda i: len(test_tubes[i]) < self.test_tube_sizes[i], range(len(test_tubes)))))

    def get_next_state(self, test_tubes, action):
        # タプルは変更できないのでリストに変換して、リストはハッシュ化できないのでタプルに変換しています。。。

        from_index, to_index = action

        test_tubes = list(test_tubes)

        from_test_tube = list(test_tubes[from_index])
        to_test_tube = list(test_tubes[to_index])

        while len(from_test_tube) > 0 and len(to_test_tube) < self.test_tube_sizes[to_index]:
            to_test_tube.append(from_test_tube.pop())

        test_tubes[to_index] = tuple(to_test_tube)
        test_tubes[from_index] = tuple(from_test_tube)

        return tuple(test_tubes)


# 問題を読み込みます。
def read_question():
    def read_test_tube_sizes(test_tube_count):
        for _ in range(test_tube_count):
            yield int(input())

    def read_test_tubes(test_tube_count):
        for _ in range(test_tube_count):
            yield tuple(map(lambda marble: int(marble, 16), input().split()))

    test_tube_count = int(input())

    return (tuple(read_test_tube_sizes(test_tube_count)),
            tuple(read_test_tubes(test_tube_count)),
            tuple(read_test_tubes(test_tube_count)))


# 幅優先探索で問題をときます。
def solve(question):
    game = Game(question)

    queue = deque((((), game.get_initial_state()),))
    visited_states = set((game.get_initial_state(),))

    while queue:
        actions, state = queue.popleft()

        if game.has_finished(state):
            return actions

        for action in game.get_legal_actions(state):
            next_state = game.get_next_state(state, action)

            if next_state in visited_states:
                continue

            visited_states.add(next_state)
            queue.append((actions + (action,), next_state))

    return ()  # 手本の状態にできない問題の場合の考慮をしていないので、何もしないことにします。


# 解答を出力します。
def write_answer(actions):
    for from_index, to_index in actions:
        print(f'{from_index} {to_index}')


write_answer(solve(read_question()))
