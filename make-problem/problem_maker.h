#pragma once

#include <algorithm>
#include <random>
#include <ranges>
#include <tuple>

#include "game.h"
#include "solver.h"

namespace problem_maker {

constexpr auto min_marble_id = 0;
constexpr auto max_marble_id = 2;

template <typename RNG>
inline auto make_random_game(RNG &rng) noexcept {
  const auto tube_sizes = std::vector<int>{2, 3, 4, 5, 6, 7, 8};

  const auto tubes = [&] {
    auto result = std::vector<Tube>{};

    std::ranges::copy(tube_sizes | std::views::transform([&](const auto &tube_size) {
                        auto result = Tube{};

                        std::ranges::copy(std::views::iota(0, std::uniform_int_distribution{0, tube_size}(rng)) | std::views::transform([&](const auto &_) {
                                            return std::uniform_int_distribution{min_marble_id, max_marble_id}(rng);
                                          }),
                                          std::back_inserter(result));

                        return result;
                      }),
                      std::back_inserter(result));

    return result;
  }();

  return Game{tube_sizes, tubes};
}

inline auto make_problem(unsigned int seed) noexcept {
  auto rng = std::default_random_engine(seed);

  const auto game = make_random_game(rng);
  const auto goal_state = solve(game, rng);

  return std::make_tuple(game.tube_sizes(), game.initial_state().tubes, goal_state.tubes);
}

} // namespace problem_maker
