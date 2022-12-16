#pragma once

#include <cstdint>
#include <ranges>
#include <vector>

#include <boost/functional/hash/hash.hpp>

namespace problem_maker {

struct Action {
  int from;
  int to;
  int size;
};

using Tube = std::vector<std::uint8_t>;

inline auto operator==(const Tube &tube_1, const Tube &tube_2) noexcept {
  if (std::size(tube_1) != std::size(tube_2)) {
    return false;
  }

  for (const auto &i : std::views::iota(0, static_cast<int>(std::size(tube_1)))) {
    if (tube_1[i] != tube_2[i]) {
      return false;
    }
  }

  return true;
}

struct State {
  std::vector<Tube> tubes;
};

inline auto operator==(const State &state_1, const State &state_2) noexcept {
  if (std::size(state_1.tubes) != std::size(state_2.tubes)) {
    return false;
  }

  for (const auto &i : std::views::iota(0, static_cast<int>(std::size(state_1.tubes)))) {
    if (state_1.tubes[i] != state_2.tubes[i]) {
      return false;
    }
  }

  return true;
}

} // namespace problem_maker

namespace std {

template <>
struct hash<problem_maker::Tube> {
  auto operator()(const problem_maker::Tube &tube) const noexcept {
    auto result = static_cast<std::size_t>(0);

    for (const auto &marble : tube) {
      boost::hash_combine(result, marble);
    }

    return result;
  }
};

template <>
struct hash<problem_maker::State> {
  auto operator()(const problem_maker::State &state) const noexcept {
    auto result = static_cast<std::size_t>(0);

    for (const auto &tube : state.tubes) {
      boost::hash_combine(result, hash<problem_maker::Tube>{}(tube));
    }

    return result;
  }
};

} // namespace std

namespace problem_maker {

class Game {
  std::vector<int> _tube_sizes;
  State _initial_state;

public:
  Game(const std::vector<int> &tube_sizes, const std::vector<Tube> &tubes) noexcept : _tube_sizes{tube_sizes}, _initial_state{tubes} {
    ;
  }

  const auto &tube_sizes() const noexcept {
    return _tube_sizes;
  }

  const auto &initial_state() const noexcept {
    return _initial_state;
  }

  auto actions(const State &state) const noexcept {
    auto result = std::vector<Action>{};

    const auto size = static_cast<int>(std::size(_tube_sizes));

    for (const auto &i : std::views::iota(0, size) | std::views::filter([&](const auto &i) { return static_cast<int>(std::size(state.tubes[i])) > 0; })) {
      for (const auto &j : std::views::iota(0, size) | std::views::filter([&](const auto &j) { return static_cast<int>(std::size(state.tubes[j])) < _tube_sizes[j] && j != i; })) {
        if (static_cast<int>(std::size(state.tubes[j])) == 0) {
          for (const auto &k : std::views::iota(1, std::min(static_cast<int>(std::size(state.tubes[i])), _tube_sizes[j]) + 1)) {
            result.emplace_back(i, j, k);
          }

          continue;
        }

        if (static_cast<int>(std::size(state.tubes[i])) == _tube_sizes[i]) {
          for (const auto &k : std::views::iota(1, std::min(_tube_sizes[i], _tube_sizes[j] - static_cast<int>(std::size(state.tubes[j]))) + 1)) {
            result.emplace_back(i, j, k);
          }

          continue;
        }
      }
    }

    return result;
  }

  auto next_state(const State &state, const Action &action) const noexcept {
    auto next_state = state;

    for (const auto &_ : std::views::iota(0, action.size)) {
      next_state.tubes[action.to].emplace_back(next_state.tubes[action.from].back());
      next_state.tubes[action.from].pop_back();
    }

    next_state.tubes[action.to].shrink_to_fit();
    next_state.tubes[action.from].shrink_to_fit();

    return next_state;
  }
};

} // namespace problem_maker
