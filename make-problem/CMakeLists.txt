cmake_minimum_required(VERSION 3.18)

project(make-problem LANGUAGES CXX)

find_package(Boost REQUIRED)

add_compile_options("$<$<CXX_COMPILER_ID:MSVC>:/utf-8>")

add_executable(${PROJECT_NAME}
    game.h
    main.cpp
    problem_maker.h
    solver.h
)

target_compile_features(${PROJECT_NAME} PRIVATE
    cxx_std_20
)

target_link_libraries(${PROJECT_NAME}
    Boost::headers
)
