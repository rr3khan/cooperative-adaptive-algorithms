# Author Riyad Khan
# ECE 457A Assignment 6 Question 3

import simple_genetic as SGA
import math

# from random import randint
import pandas as pd
from itertools import combinations, permutations
import TD_Point as TDP
import numpy as np


def master():
    bounds = [5, -5]

    num_bits = 28
    pop_size = 50
    gen_num = 10
    #  mutation rate is typically between 1/pop_size and 1/chromosome_length
    mut_rate = 1 / num_bits

    # crossover rate typically in range 0.6 to 0.9 hence choose around 0.75
    cross_over_rate = 0.75

    six_hump = SGA.SGA(bounds, num_bits, pop_size, gen_num, mut_rate, cross_over_rate)
    six_hump.genetic_algo()

    six_hump2 = SGA.SGA(bounds, num_bits, 50, 50, mut_rate, cross_over_rate)
    six_hump2.genetic_algo()

    six_hump3 = SGA.SGA(bounds, num_bits, 100, 100, mut_rate, cross_over_rate)
    six_hump3.genetic_algo()

    six_hump4 = SGA.SGA(bounds, num_bits, 500, 500, mut_rate, cross_over_rate)
    six_hump4.genetic_algo()


if __name__ == "__main__":
    master()
