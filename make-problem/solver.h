#pragma once

#include <queue>
#include <unordered_set>

#include "game.h"

namespace problem_maker {

inline auto solve(const Game &game) noexcept {
  auto result = game.initial_state();

  auto queue = std::queue<State>{};
  auto visited = std::unordered_set<State>{};

  queue.emplace(game.initial_state());
  visited.emplace(game.initial_state());

  while (!std::empty(queue)) {
    const auto &state = queue.front();

    for (const auto &action : game.actions(state)) {
      const auto &next_state = game.next_state(state, action);

      if (!visited.emplace(next_state).second) {
        continue;
      }

      queue.emplace(next_state);

      result = next_state;
    }

    queue.pop();
  }

  return result;
}

} // namespace problem_maker
