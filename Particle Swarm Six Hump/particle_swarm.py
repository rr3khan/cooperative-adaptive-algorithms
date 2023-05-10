# Author Riyad Khan
# ECE 457A Assignment 8 Question 3

# Import from random library to generate random points
from random import randint, random, sample, uniform
from tabnanny import check

# import a custom class for 2D points
import TD_Point as TDP
import numpy as np

# Library for plotting the points
import matplotlib.pyplot as plt
from math import sqrt, pow


# Particle Swarm optimization class
class PSO:
    def __init__(
        self,
        num_particles: int,
        num_iterations: int,
        c1_p_coeff: float,
        c2_s_coeff: float,
        w_coeff: float,
        speed_limit: float,
        bounds: list,
    ):
        # parameters
        # number of particles
        self.num_particles = num_particles
        # empty particle swarm list
        self.swarm_pop = []
        # bounds of the particle swarm search space
        self.bounds = bounds
        # acceleration coefficient c1 for the cognitive component
        self.c1_p_coeff = c1_p_coeff
        # acceleration coefficient c2 for the social/swam component
        self.c2_s_coeff = c2_s_coeff
        # inertial weight coefficient of the particle
        self.w_coeff = w_coeff
        # speed limit
        self.speed_limit = speed_limit
        # stopping criteria
        self.num_iterations = num_iterations
        # current iteration
        self.cur_iteration = 0
        # random values for each dimension
        self.rx = random()
        self.ry = random()
        # best fitness tracker
        self.best_fitness_tracker = []
        # average fitness tracker
        self.average_fitness_tracker = []
        # best position seen in the neighbourhood
        self.nbest = TDP.TD_Point(-5, -5)

    def update_nbest(self):
        for particle in self.swarm_pop:
            if fitness_function(particle.pbest) < fitness_function(self.nbest):
                self.nbest = particle.pbest
        return

    def plot_fitness_values(self):
        iterations_data = [i for i in range(1, self.num_iterations + 1)]

        # figure, axes = plt.subplots()
        # best_data = plt.scatter(generations_data, self.best_fitness_tracker, edgecolors='b', label="raw_data")
        avg_data = plt.scatter(
            iterations_data,
            self.average_fitness_tracker,
            edgecolors="r",
            label="raw_data",
        )
        # axes.set_aspect(1)
        plt.xlabel("Iterations")
        plt.ylabel("Fitness")
        plt.title("Average fitness value of Particle over the iterations")
        plt.show()

        best_data = plt.scatter(
            iterations_data, self.best_fitness_tracker, edgecolors="r", label="raw_data"
        )
        # axes.set_aspect(1)
        plt.xlabel("Iterations")
        plt.ylabel("Fitness")
        plt.title("Best fitness value of Particle over the iterations")
        plt.show()

    def pso_algo(self):
        #  initialize swarm
        # for count in range(self.num_particles):
        #     self.swarm_pop.append(particle(self))
        self.swarm_pop = [Particle(self) for count in range(self.num_particles)]

        # while terminal conditions not met
        while self.cur_iteration < self.num_iterations:
            fitness_sum = 0
            # asynchronous update method
            for particle in self.swarm_pop:
                # update particle's velocity and position
                particle.update_particle_position()
                particle.update_personal_best()

                # update nbest assume global for now
                # update here for asynchronous update
                self.update_nbest()

                # update fitness sum
                # sum up all fitnesses
                fitness_sum += fitness_function(particle.curr_position)

            # update tracker
            self.best_fitness_tracker.append(fitness_function(self.nbest))

            #  update average tracker
            self.average_fitness_tracker.append(fitness_sum / self.num_particles)

            # increment iterations
            self.cur_iteration = self.cur_iteration + 1
            print("Current iteration:", self.cur_iteration)

        # make plots
        self.plot_fitness_values()

        print("Best fitness tracker", self.best_fitness_tracker)
        print("Average fitness tracker", self.average_fitness_tracker)
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


# helper class to act as each individual particle
class Particle:
    def __init__(self, swarm: PSO):
        # the swarm that the particle belongs to
        self.swarm = swarm
        # particle current position x, y
        # initiaize a random position in the bounds
        self.curr_position = TDP.TD_Point(
            uniform(self.swarm.bounds[0], self.swarm.bounds[1]),
            uniform(self.swarm.bounds[0], self.swarm.bounds[1]),
        )
        # current velocity of particle
        self.velocity = TDP.TD_Point(0, 0)
        # best position seen so far
        self.pbest = self.curr_position

    # update the particle velocity and position
    def update_particle_position(self):
        new_velocity_x = (
            self.swarm.w_coeff * self.velocity.x
            + self.swarm.c1_p_coeff
            * self.swarm.rx
            * (self.pbest.x - self.curr_position.x)
            + self.swarm.c2_s_coeff
            * self.swarm.rx
            * (self.swarm.nbest.x - self.curr_position.x)
        )
        new_velocity_y = (
            self.swarm.w_coeff * self.velocity.y
            + self.swarm.c1_p_coeff
            * self.swarm.ry
            * (self.pbest.y - self.curr_position.y)
            + self.swarm.c2_s_coeff
            * self.swarm.ry
            * (self.swarm.nbest.y - self.curr_position.y)
        )

        # enforce speed limit so that we do not speed off
        if abs(new_velocity_x) > self.swarm.speed_limit:
            new_velocity_x = self.swarm.speed_limit

        if abs(new_velocity_y) > self.swarm.speed_limit:
            new_velocity_y = self.swarm.speed_limit

        # update self velocity

        self.velocity.x = new_velocity_x
        self.velocity.y = new_velocity_y

        # update position

        self.curr_position.x = self.curr_position.x + self.velocity.x
        self.curr_position.y = self.curr_position.y + self.velocity.y

        return

    # update the personal best position for the particle
    def update_personal_best(self):
        if fitness_function(self.curr_position) <= fitness_function(self.pbest):
            self.pbest = self.curr_position
            # update personal best
        return

    def particle_log(self):
        # log the particle data
        # particle current position x, y
        # initiaize a random position in the bounds
        print("Current Position:", self.curr_position.x, self.curr_position.y)
        # current velocity of particle
        print("Current Velocity:", self.velocity.x, self.velocity.y)
        # best position seen so far
        print("Best Personal Position:", self.pbest.x, self.pbest.y)
        print("Best Neighbourhood Position:", self.nbest.x, self.nbest.y)


def six_hump(x: float, y: float) -> float:
    return (
        (4 - 2.1 * x * x + (pow(x, 4) / 3)) * pow(x, 2)
        + x * y
        + (-4 + 4 * y * y) * y * y
    )


def fitness_function(sol: TDP) -> float:
    """
    Takes a solution consisting of a 2D x, y point
    and evaluates its fitness
    We want to minimize the function hence the lower a solution's
    value is the higher its fitness.
    We will use a normalization of z values assuming rang 5, -5
    Also use negative sign to ensure negative values have a higher fitness than positive ones
    """
    return six_hump(sol.x, sol.y)
    # # if the solution is outside of allowable range then 0 fitness
    # if sol.x > self.bounds[0] or sol.x < self.bounds[1] or sol.y > self.bounds[0] or sol.y < self.bounds[1]:
    #     return -9999
    # else:
    #     camel_result = self.six_hump(sol.x, sol.y)
    #     return -1*camel_result+5/(5+5)
