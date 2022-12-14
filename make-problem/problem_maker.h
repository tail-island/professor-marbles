#pragma once

#include <algorithm>
#include <cstdint>
#include <random>
#include <ranges>
#include <tuple>

#include "game.h"
#include "solver.h"

namespace problem_maker {

constexpr auto min_size = 10;
constexpr auto max_size = 20;

constexpr auto min_tube_size = 1;
constexpr auto max_tube_size = 32;

constexpr auto min_marble_id = 0;
constexpr auto max_marble_id = 64;

template <typename RNG>
inline auto make_game(RNG &rng) noexcept {
  const auto size = std::uniform_int_distribution(min_size, max_size)(rng);

  const auto tube_sizes = [&] {
    auto result = std::vector<int>{};

    std::ranges::copy(std::views::iota(0, size) | std::views::transform([&](const auto &_) {
                        return std::uniform_int_distribution{min_tube_size, max_tube_size}(rng);
                      }),
                      std::back_inserter(result));

    return result;
  }();

  const auto tubes = [&] {
    auto result = std::vector<std::vector<std::uint8_t>>{};

    std::ranges::copy(tube_sizes | std::views::transform([&](const auto &tube_size) {
                        auto result = std::vector<std::uint8_t>{};

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

inline auto random_problem(unsigned int seed) noexcept {
  auto rng = std::default_random_engine(seed);

  return make_game(rng);
}

inline auto make_problem(unsigned int seed) noexcept {
  const auto game = random_problem(seed);
  const auto state = solve(game);

  return std::make_tuple(game.tube_sizes(), game.initial_state().tubes, state.tubes);
}

} // namespace problem_maker
