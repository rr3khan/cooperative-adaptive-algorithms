# Author Riyad Khan
# ECE 457A Assignment 7 Question 3

import particle_swarm as PSO
import math
# from random import randint
import pandas as pd
from itertools import combinations, permutations
import TD_Point as TDP
import numpy as np

def master():

    # bounds for the particle swarm search space
    bounds = [5, -5]

    # Initiaize W, C
    # Needed for convergence
    # w < 1, c > 0
    # 2*w -c + 2 > 0

    # popular set of parameters promposed by clerc and kennedy 2003
    # w = 0.792, c1 = c2 = 1.4944

    pso_1 = PSO.PSO(10, 10, 1.4944, 1.4944, 0.792, 5, bounds)
    pso_1.pso_algo()

    pso_2 = PSO.PSO(50, 50, 1.4944, 1.4944, 0.792, 5, bounds)
    pso_2.pso_algo()

    pso_3 = PSO.PSO(50, 50, 1, 1.4944, 0.792, 5, bounds)
    pso_3.pso_algo()

    # test_particle = PSO.particle(pso_1)
    # test_particle.particle_log()
    # test_particle

if __name__ == "__main__":
    master()
