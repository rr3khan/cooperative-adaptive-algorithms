# Author Riyad Khan
# ECE 457A Assignment 7 Question 3

# Import from random library to generate random points
from random import randint, random, sample
from tabnanny import check

import pandas as pd

# for mathematical operations like cos
import math

# import a custom class for 2D points
import TD_Point as TDP
import numpy as np

# Library for plotting the points
import matplotlib.pyplot as plt
from math import sqrt, pow


class ACO:
    def __init__(
        self,
        num_ants: int,
        num_iterations: int,
        alpha: float,
        beta: float,
        evap_rate: float,
        pher_const_q: int,
        city_data,
    ):
        # parameters
        # num ants
        self.num_ants = num_ants
        # alpha importance of pheromone
        self.alpha = alpha
        # importance of heuristic/distance costs
        self.beta = beta
        # rate of evaporation of the pheromone
        self.evap_rate = evap_rate
        # Initial pheromone constant deposit q
        self.pq = pher_const_q
        # stopping criteria
        self.num_iterations = num_iterations
        # current iteration
        self.cur_iteration = 0
        # city data for travelling salesman problem
        #  adj matrix contaianing distances between cities
        self.city_data = city_data
        # pheromone matrix
        self.pheromone_matrix = []
        # best fitness tracker
        self.best_fitness_tracker = []
        # average fitness tracker
        self.average_fitness_tracker = []

        # online delayed appraoch
        # delta pherij = Q/L^k

        # ant tabu list

        # max num iterations
        # initial pheromone
        # pheromone devay parameter

        # components
        # transistion rule

        # pheromone evap rule
        # phher update rule
        # prob heuristic
        # quality of soln
        #  mem or list consraints
        #  termination criteria

        # initial solution

    def initialize_pheromone_matrix(self):
        self.pheromone_matrix = [
            [self.pq for city_1 in range(len(self.city_data))]
            for city_2 in range(len(self.city_data))
        ]
        return

    def update_pheromones(self, pop_ants):
        for column in range(len(self.pheromone_matrix)):
            for row in range(len(self.pheromone_matrix[0])):
                # evaporate some of the pheromone
                self.pheromone_matrix[column][row] *= self.evap_rate
                for worker_ant in pop_ants:
                    # add the pheromone contributions by the path the ants travelled
                    self.pheromone_matrix[column][row] += worker_ant.del_pheromone[
                        column
                    ][row]

    def plot_fitness_values(self):
        generations_data = [i for i in range(1, self.num_iterations + 1)]

        # figure, axes = plt.subplots()
        # best_data = plt.scatter(generations_data, self.best_fitness_tracker, edgecolors='b', label="raw_data")
        avg_data = plt.scatter(
            generations_data,
            self.average_fitness_tracker,
            edgecolors="r",
            label="raw_data",
        )
        # axes.set_aspect(1)
        plt.xlabel("Generations")
        plt.ylabel("Fitness (Length of Path Travelled)")
        plt.title("Average fitness value of Ant Paths over the generations")
        plt.show()

        best_data = plt.scatter(
            generations_data,
            self.best_fitness_tracker,
            edgecolors="r",
            label="raw_data",
        )
        # axes.set_aspect(1)
        plt.xlabel("Generations")
        plt.ylabel("Fitness (Length of Path Travelled)")
        plt.title("Best fitness value of Ant fitness over the generations")
        plt.show()

    def aco_algo(self):
        # first step initialize the pheromone matrix
        self.initialize_pheromone_matrix()

        best_fitness = float("inf")
        best_path = []
        while self.cur_iteration < self.num_iterations:
            # initialize sum of fitnesses for a generation
            fitness_sum = 0
            # assemble the ant army
            pop_ants = [Ant_worker(self) for ant in range(self.num_ants)]
            for worker_ant in pop_ants:
                for city in range(len(self.city_data) - 1):
                    worker_ant.pick_next_node()
                # add cost from final city to first city to the
                # ant fitness
                worker_ant.fitness += self.city_data[worker_ant.cur_node][
                    worker_ant.start_node
                ]
                # update best seen so far
                if worker_ant.fitness < best_fitness:
                    best_fitness = worker_ant.fitness
                    best_path = [] + worker_ant.ant_tabu_list

                # sum up all fitnesses
                fitness_sum += worker_ant.fitness
                # ant updates its pheromones to be desposited
                worker_ant.update_del_pheromone()
            # at end of iteration all ants update the global environment pheromones
            self.update_pheromones(pop_ants)
            # update iteration count
            # update best fitness tracker
            self.best_fitness_tracker.append(best_fitness)
            # update average fitness
            self.average_fitness_tracker.append(fitness_sum / self.num_ants)
            self.cur_iteration += 1
            print("Current Iteration", self.cur_iteration)

        self.plot_fitness_values()
        print("Best fitness", best_fitness)
        print("Best Path", best_path)
        # self.testing()

        return

    def testing(self):
        print("TESTING")
        # self.ACO_logger()
        # print("Pher matrix size:", len(self.pheromone_matrix) )
        # print("Pher matrix size:", len(self.pheromone_matrix[1]) )
        # test_map = City_Map()

    def ACO_logger(self):
        # print("TODO")

        print("Num ants", self.num_ants)
        print("Best fitness over generations", self.best_fitness_tracker)
        print("Average fitness over generations", self.average_fitness_tracker)
        # print("Pheromone Matrix:", self.pheromone_matrix)
        # print("Fitness", self.fitness)

        # print("Best Fitness", self.best_fitness_tracker)
        # print("Avg Fitness", self.average_fitness_tracker)
        # print("Final Best Fitness", self.best_fitness_tracker[-1])

        # print("Current sol:", self.curr_sol  )
        # print("Tabu List:", self.tabu_list )
        # print("Cost:", self.cost )
        # print("Iterations:", self.iterations )
        # print("Best so far:", self.best_so_far)
        # print("Best solution seen:", self.best_soln_seen)


# helper class to act as each individual ant
class Ant_worker:
    def __init__(self, ant_colony: ACO, start_node=0):
        self.colony = ant_colony
        # start node that is first city
        self.start_node = start_node
        # total distance travelled by ant in path of cities
        self.fitness = 0.0
        # list of cities travelled by the any
        self.ant_tabu_list = [start_node]
        # change in pheromone to add to update equation
        self.del_pheromone = []
        # first starting city
        self.start_node = start_node
        # current node the ant is at
        self.cur_node = start_node

    def pick_next_node(self):
        # function to calculate the probabilities for selecting another node/city to visit
        #
        sum_pher_div_dist = 0
        for city_next in range(len(self.colony.city_data)):
            if city_next != self.cur_node and city_next not in self.ant_tabu_list:
                # print("Phermatrix", self.colony.city_data)
                sum_pher_div_dist += pow(
                    self.colony.pheromone_matrix[self.cur_node][city_next],
                    self.colony.alpha,
                ) / (
                    pow(
                        self.colony.city_data[self.cur_node][city_next],
                        self.colony.beta,
                    )
                )

        # initialize matrix of probabilitites
        city_prob = [0 for city in range(len(self.colony.city_data))]

        for city in range(len(city_prob)):
            if city != self.cur_node and city not in self.ant_tabu_list:
                city_prob[city] = (
                    pow(
                        self.colony.pheromone_matrix[self.cur_node][city],
                        self.colony.alpha,
                    )
                    / (
                        pow(
                            self.colony.city_data[self.cur_node][city], self.colony.beta
                        )
                    )
                ) / sum_pher_div_dist

        next_city = -9999
        # select a city from the probability list
        # generate a random number between 0 and 1
        # continuously generate random numbers until we pick a city
        while next_city == -9999:
            randNum = random()
            # ()/10
            for prob_index in range(len(city_prob)):
                if randNum < city_prob[prob_index] and prob_index != self.cur_node:
                    next_city = prob_index
                    break

        # finish selecting now update the self variables
        self.ant_tabu_list.append(next_city)
        self.fitness += self.colony.city_data[self.cur_node][next_city]
        self.cur_node = next_city

    # update the pheromone values
    def update_del_pheromone(self):
        # reset pheromone delta values
        self.del_pheromone = [
            [0 for city_1 in range(len(self.colony.city_data))]
            for city_2 in range(len(self.colony.city_data))
        ]
        # iterate through the tabu list/visited cities and calculate the
        # delta pheromone value for that city pair link
        for visited in range(1, len(self.ant_tabu_list)):
            city_prev = self.ant_tabu_list[visited - 1]  # previous city
            city_next = self.ant_tabu_list[visited]  # next city

            # online delayed pheromone update formula delta Tij = Q/Lk
            self.del_pheromone[city_prev][city_next] = self.colony.pq / self.fitness


# test_map = City_Map(54)
# print(test_map.city_map_logger())


# given an x,y coordinate of two cities calculate the euclidean distances
# between the two cities
def calc_eucl_dist(x1_cord: int, y1_coord: int, x2_cord: int, y2_coord: int):
    distance = sqrt(pow((x2_cord - x1_cord), 2) + (pow(y2_coord - y1_coord, 2)))

    return distance


# print(calc_eucl_dist(1150, 1760, 630, 1160))
