# Author Riyad Khan
# ECE 457A Assignment 4 Question 3

import SimulatedAnnealing as SA
from random import randint

from TD_Coord import TD_Coord


def master():
    # sample the search space to figure out an initial temperature
    # take 10 samples
    # for sample in range(10):
    #         print("Sample random x1 and x2 coordinates: ", randint(-100, 100), randint(-100, 100) )
    # Points obtained from the above:  -20 16, 75 -79, -43 -3, 97 23, 98 -34, 33 13, 61 -17, 26 -65, 100 58, 63 -6

    # Calculate max delta c for the above

    # dist1 = SA.debug_dist_goal(100, 58)
    # dist2 = SA.debug_dist_goal(-20, 16)

    # delta_c = dist2 - dist1

    # print("Distances, dist1: ", dist1, "dist2: ", dist2, "change: ", delta_c)

    # From above the max delta C was found to be 84.84

    # print(SA.easom_fn(3, 3))

    # bounds = [-100, 100]

    # collect 10 random points and values

    print("10 random points for a linear schedule \n")

    for index in range(10):
        sol1 = TD_Coord(randint(-100, 100), randint(-100, 100))

        sol1_value = SA.easom_fn(sol1.x1, sol1.x2)

        next_sol = TD_Coord(randint(-100, 100), randint(-100, 100))

        next_sol_value = SA.easom_fn(next_sol.x1, next_sol.x2)

        print("Initial Sol 1:", sol1.x1, ",", sol1.x2, "value:", sol1_value)
        # print("Sol 2:", next_sol.x1, ",", next_sol.x2)

        # From calculations let t = 167
        t0 = 167

        alpha = 0.1

        sal1 = SA.SA(sol1, sol1_value, next_sol, next_sol_value, t0, alpha, 5, "linear")

        sal1.sa_algo()

        sal1.sa_logger()

    print("2 Points with higher temperatures 217 and 267 \n")

    for index in range(2):
        sol1 = TD_Coord(randint(-100, 100), randint(-100, 100))

        sol1_value = SA.easom_fn(sol1.x1, sol1.x2)

        next_sol = TD_Coord(randint(-100, 100), randint(-100, 100))

        next_sol_value = SA.easom_fn(next_sol.x1, next_sol.x2)

        print("Initial Sol 1:", sol1.x1, ",", sol1.x2, "value:", sol1_value)
        # print("Sol 2:", next_sol.x1, ",", next_sol.x2)

        # From calculations let t = 167
        t0 = 167 + 50 + 50 * (index)

        alpha = 0.1

        sal1 = SA.SA(sol1, sol1_value, next_sol, next_sol_value, t0, alpha, 5, "linear")

        sal1.sa_algo()

        sal1.sa_logger()

    print("2 Points with lower temperatures 117 and 67\n")

    for index in range(2):
        sol1 = TD_Coord(randint(-100, 100), randint(-100, 100))

        sol1_value = SA.easom_fn(sol1.x1, sol1.x2)

        next_sol = TD_Coord(randint(-100, 100), randint(-100, 100))

        next_sol_value = SA.easom_fn(next_sol.x1, next_sol.x2)

        print("Initial Sol 1:", sol1.x1, ",", sol1.x2, "value:", sol1_value)
        # print("Sol 2:", next_sol.x1, ",", next_sol.x2)

        # From calculations let t = 167
        t0 = 167 - 50 - 50 * (index)

        alpha = 0.1

        sal1 = SA.SA(sol1, sol1_value, next_sol, next_sol_value, t0, alpha, 5, "linear")

        sal1.sa_algo()

        sal1.sa_logger()

    print(
        "2 Geometric Annealing scheduling one with iter = 5 and another with iter = 50 \n"
    )

    sol1 = TD_Coord(randint(-100, 100), randint(-100, 100))

    sol1_value = SA.easom_fn(sol1.x1, sol1.x2)

    next_sol = TD_Coord(randint(-100, 100), randint(-100, 100))

    next_sol_value = SA.easom_fn(next_sol.x1, next_sol.x2)

    print("Initial Sol 1:", sol1.x1, ",", sol1.x2, "value:", sol1_value)
    # print("Sol 2:", next_sol.x1, ",", next_sol.x2)

    # From calculations let t = 167
    t0 = 167

    alpha = 0.1

    sal1 = SA.SA(sol1, sol1_value, next_sol, next_sol_value, t0, alpha, 5, "geometric")

    sal1.sa_algo()

    sal1.sa_logger()

    print("Geometric with iter = 50")

    sol1 = TD_Coord(randint(-100, 100), randint(-100, 100))

    sol1_value = SA.easom_fn(sol1.x1, sol1.x2)

    next_sol = TD_Coord(randint(-100, 100), randint(-100, 100))

    next_sol_value = SA.easom_fn(next_sol.x1, next_sol.x2)

    print("Initial Sol 1:", sol1.x1, ",", sol1.x2, "value:", sol1_value)
    # print("Sol 2:", next_sol.x1, ",", next_sol.x2)

    # From calculations let t = 167
    t0 = 167

    alpha = 0.1

    sal1 = SA.SA(sol1, sol1_value, next_sol, next_sol_value, t0, alpha, 50, "geometric")

    sal1.sa_algo()

    sal1.sa_logger()


if __name__ == "__main__":
    master()
