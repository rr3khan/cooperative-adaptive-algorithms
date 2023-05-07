# Author Riyad Khan
# ECE 457A Assignment 7 Question 3

import ant_colony as ACO
import math

# from random import randint
import pandas as pd
from itertools import combinations, permutations
import TD_Point as TDP
import numpy as np


def master():
    # import data
    city_coordinates = pd.read_excel("Assignment7-city coordinates.xlsx").values
    # print(city_coordinates)
    num_cities = len(city_coordinates)

    # # construct the adjacency matrix of distance values between cities
    city_distances = []
    for city_1 in range(num_cities):
        #  initialize dist_row
        dist_row = []
        for city_2 in range(num_cities):
            dist_row.append(
                ACO.calc_eucl_dist(
                    city_coordinates[city_1][1],
                    city_coordinates[city_1][2],
                    city_coordinates[city_2][1],
                    city_coordinates[city_2][2],
                )
            )

        city_distances.append(dist_row)

    # aco_1 = ACO.ACO(10, 10, 0.7, 1, 0.5, 1, city_distances)
    # print()
    # aco_1.aco_algo()
    # aco_2 = ACO.ACO(50, 10, 0.7, 1, 0.5, 1, city_distances)
    # aco_2.aco_algo()

    # aco_3 = ACO.ACO(50, 50, 0.7, 1, 0.5, 1, city_distances)
    # aco_3.aco_algo()

    # aco_4 = ACO.ACO(50, 50, 1, 1, 0.5, 1, city_distances)
    # aco_4.aco_algo()

    # aco_5 = ACO.ACO(50, 50, 1, 0.7, 0.9, 1, city_distances)
    # aco_5.aco_algo()

    aco_6 = ACO.ACO(50, 50, 1, 0.7, 0.5, 50, city_distances)
    aco_6.aco_algo()
    # aco_1.ACO_logger()
    # # aco_1 = ACO.ACO(100, 50, 0.7, 1, 0.5, 100, city_distances)
    # print(aco_1.aco_algo())
    # aco_1.ACO_logger()

    # print(city_distances)
    # print(len(city_distances[1]))

    # print(city_coordinates.values[0][1])

    # print(len(city_coordinates))


if __name__ == "__main__":
    master()
