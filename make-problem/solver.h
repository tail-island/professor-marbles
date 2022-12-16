#pragma once

#include <random>
#include <ranges>

#include "game.h"

namespace problem_maker {

template <typename RNG>
inline auto solve(const Game &game, RNG &rng) noexcept {
  auto result = game.initial_state();

  for (const auto &_ : std::views::iota(0, 1'000'000)) {
    const auto &actions = game.actions(result);

    if (actions.empty()) {
      break;
    }

    result = game.next_state(result, actions[std::uniform_int_distribution(0, static_cast<int>(std::size(actions)) - 1)(rng)]);
  }

  return result;
}

// inline auto solve(const Game &game) noexcept {
//   auto result = game.initial_state();

//   auto queue = std::queue<State>{};
//   auto visited = std::unordered_set<State>{};

//   queue.emplace(game.initial_state());
//   visited.emplace(game.initial_state());

//   while (!std::empty(queue)) {
//     const auto &state = queue.front();

//     for (const auto &action : game.actions(state)) {
//       const auto &next_state = game.next_state(state, action);

//       if (!visited.emplace(next_state).second) {
//         continue;
//       }

//       queue.emplace(next_state);

//       result = next_state;
//     }

//     queue.pop();
//   }

//   return result;
// }

} // namespace problem_maker
