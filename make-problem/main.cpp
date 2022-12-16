#include <iomanip>
#include <iostream>
#include <random>

#include "problem_maker.h"

int main(int argc, char **argv) {
  const auto [tube_sizes, goal_tubes, initial_tubes] = problem_maker::make_problem(std::random_device{}());

  std::cout << std::size(tube_sizes) << std::endl;

  for (const auto &tube_size : tube_sizes) {
    std::cout << tube_size << std::endl;
  }

  for (const auto &tube : initial_tubes) {
    for (const auto &marble : tube) {
        std::cout << std::setw(2) << std::setfill('0') << std::hex << static_cast<int>(marble) << " ";
    }

    std::cout << std::endl;
  }

  for (const auto &tube : goal_tubes) {
    for (const auto &marble : tube) {
        std::cout << std::setw(2) << std::setfill('0') << std::hex << static_cast<int>(marble) << " ";
    }

    std::cout << std::endl;
  }

  return 0;
}
