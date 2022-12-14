#include <iomanip>
#include <iostream>
#include <random>

#include "problem_maker.h"

int main(int argc, char **argv) {
  const auto [tube_sizes, goal_tubes, initial_tubes] = problem_maker::make_problem(std::random_device{}());

  for (const auto &tube_size : tube_sizes) {
    std::cout << tube_size << std::endl;
  }

  for (const auto &i : std::views::iota(0, static_cast<int>(std::size(tube_sizes)))) {
    for (const auto &j : std::views::iota(0, tube_sizes[i])) {
      if (j < std::size(goal_tubes[i])) {
        std::cout << std::setw(2) << std::setfill('0') << std::hex << static_cast<int>(goal_tubes[i][j]);
      } else {
        std::cout << "--";
      }

      std::cout << " ";
    }

    std::cout << std::endl;
  }

  for (const auto &i : std::views::iota(0, static_cast<int>(std::size(tube_sizes)))) {
    for (const auto &j : std::views::iota(0, tube_sizes[i])) {
      if (j < std::size(initial_tubes[i])) {
        std::cout << std::setw(2) << std::setfill('0') << std::hex << static_cast<int>(initial_tubes[i][j]);
      } else {
        std::cout << "--";
      }

      std::cout << " ";
    }

    std::cout << std::endl;
  }

  // for (const auto &a : game.actions(goal_tubes)) {
  //   std::cout << a.from << ", " << a.to << ", " << a.size << std::endl;
  // }

  return 0;
}
