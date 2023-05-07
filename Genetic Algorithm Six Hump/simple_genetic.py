# Author Riyad Khan
# ECE 457A Assignment 6 Question 3

# Import from random library to generate random points
from random import randint, random, sample
from tabnanny import check

# for mathematical operations like cos
import math

# import a custom class for 2D points
import TD_Point as TDP
import numpy as np

# Library for plotting the points
import matplotlib.pyplot as plt


class SGA:
    def __init__(
        self,
        bounds,
        num_bits: int,
        pop_size: int,
        gen_num: int,
        mut_rate: float,
        cross_over_rate: float,
    ):
        # population of solutions
        self.soln_pop = []
        # size of the population
        self.pop_size = pop_size
        # number of generations to run the algorithm for
        self.gen_num = gen_num
        # mutation rate
        self.mut_rate = mut_rate
        # bounds that the solution coordinates must fall within
        self.bounds = bounds
        # number of bits used to represent a solution chromosome
        self.num_bits = num_bits
        # fitness scores for each individual in the population
        self.fitness = []
        # cross over rate typically in range (0.6, 0.9)
        self.cross_over_rate = cross_over_rate
        # best fitness tracker
        self.best_fitness_tracker = []
        # average fitness tracker
        self.average_fitness_tracker = []
        # simple counter for debugging
        self.gen_counter = 0

        # initial solution

    def six_hump(self, x: float, y: float) -> float:
        return (
            (4 - 2.1 * x * x + (pow(x, 4) / 3)) * pow(x, 2)
            + x * y
            + (-4 + 4 * y * y) * y * y
        )

    def gen_pop(self):
        """
        Generate the first population
        """
        # Generate a random population of pop_size solutions with num_bits bits
        self.soln_pop = np.random.choice([0, 1], size=(self.pop_size, self.num_bits))

    def gen_pop_fitness(self):
        # determines all fitness values for the entire population
        self.fitness = [
            self.fitness_function(self.convert_bin_to_phenotype(soln, 0.001))
            for soln in self.soln_pop
        ]

    def gen_pop_phenotype(self):
        # generate an entire population of phenotypes
        phenotype = [
            self.convert_bin_to_phenotype(soln, 0.001) for soln in self.soln_pop
        ]

        return phenotype

    #
    def fitness_function(self, sol: TDP) -> float:
        """
        Takes a phenotype solution consisting of a 2D x, y point
        and evaluates its fitness
        We want to minimize the function hence the lower a solution's
        value is the higher its fitness.
        We will use a normalization of z values assuming rang 5, -5
        Also use negative sign to ensure negative values have a higher fitness than positive ones
        """
        # if the solution is outside of allowable range then o fitness
        if (
            sol.x > self.bounds[0]
            or sol.x < self.bounds[1]
            or sol.y > self.bounds[0]
            or sol.y < self.bounds[1]
        ):
            return -9999
        else:
            camel_result = self.six_hump(sol.x, sol.y)
            return -1 * camel_result + 5 / (5 + 5)

    def convert_bin_to_phenotype(self, chromosome, precision) -> TDP:
        """
        Converts a chromosome to its phenotype, that is converts a binary representation to its
        x, y point form representation
        """
        #  the first num_bits/2 bits is the x value
        # the next num_bits/2 bits is the y value
        x_bits = chromosome[0 : int(self.num_bits / 2)]
        y_bits = chromosome[int(self.num_bits / 2) : int(self.num_bits)]

        # now convert from binary to decimal rank in scaling
        x_rank = 0
        for bit_index in range(len(x_bits)):
            x_rank = x_rank + (x_bits[bit_index]) * pow(2, bit_index)

        y_rank = 0
        for bit_index in range(len(y_bits)):
            y_rank = y_rank + (y_bits[bit_index]) * pow(2, bit_index)

        # now convert scaled ranking back into the actual decimal float values
        x_float = (x_rank - 1) * precision + self.bounds[1]
        y_float = (y_rank - 1) * precision + self.bounds[1]

        # prepare point for shipment

        phenotype = TDP.TD_Point(x_float, y_float)

        # print("X bits", x_bits)
        # print("y bits", y_bits)
        # print("X float", x_float)
        # print("y float", y_float)

        return phenotype

    # Parent selection, parents fight it out in the cell games for the right to reproduce

    # select k members at random and then select the best of these
    def tournament_of_power(self, k):
        # parent selection via tournament selection

        # random initial choice
        champion = randint(0, self.pop_size - 1)

        # print("Campion", champion)

        challengers = sample([i for i in range(1, self.pop_size - 1)], k)

        for index in challengers:
            # print("Challengers: ", challengers)
            # for index in randint(0, self.pop_size, k-1):
            # tournament time now fight
            # are you better?
            # print("Index", index)
            # print("Fitness list", self.fitness)
            # print("Fitness list index value", self.fitness[index])
            # print("Fit Lenght", len(self.fitness))
            # print("Campion", self.fitness[champion])
            if self.fitness[index] > self.fitness[champion]:
                champion = index

        return self.soln_pop[champion]

    def crossover(self, parent_1, parent_2, n_points):
        # first copy children from parents
        child_1, child_2 = parent_1, parent_2
        # check random probability of crossover
        if random() < self.cross_over_rate:
            # choose random point on parent
            # -2 since otherswise we would be out of bounds or not cutting anything
            c_point = randint(1, len(parent_1) - 2)
            # smexy time
            # print("Parent 1:", parent_1)
            # print("Parent 2:", parent_2)
            # print("c_point:", c_point)
            # print("P1 half:", parent_1[0: c_point])
            # print("P2 half", parent_2[c_point: self.num_bits])
            child_1 = np.hstack(
                (parent_1[0:c_point], parent_2[c_point : self.num_bits])
            )
            # = parent_1[0: c_point] + parent_2[c_point: self.num_bits]
            child_2 = np.hstack(
                (parent_2[0:c_point], parent_1[c_point : self.num_bits])
            )
            # child_2 = parent_2[0: c_point] + parent_1[c_point: self.num_bits]

        return [child_1, child_2]

    def mutation(self, soln):
        for gene in range(len(soln)):
            # random decide on mutating the gene
            if random() < self.mut_rate:
                # mutate i.e toggle bit
                soln[gene] = 1 - soln[gene]

    def new_gen(self):
        """
        Create the next generation for the pupolation
        """
        children = []

        # run the tournament
        # let the cell games begin

        # assuming we pick around 4 for the torunament
        parent_pool = [self.tournament_of_power(4) for index in range(self.pop_size)]

        # print("Parent Pool", parent_pool)
        # print("Parent Pool 0", parent_pool[0])

        for p_index in range(0, self.pop_size - 1, 2):
            # print("Index; ", p_index)
            parent_1, parent_2 = parent_pool[p_index], parent_pool[p_index + 1]

            # now mate and mutate
            for child in self.crossover(parent_1, parent_2, 1):
                # mutate
                self.mutation(child)
                # add child to generation_list
                children.append(child)

        # update our population pool
        self.soln_pop = children
        return

    def get_avg_fitness(self) -> float:
        total_fitness = 0
        # summ all fitness values and
        # find average
        for index in self.fitness:
            total_fitness = total_fitness + index

        return total_fitness / self.pop_size

    def get_best_fitness(self):
        best_fitness = -9999
        # comb through our pop and find the one with the
        # best fitness value
        for index in range(len(self.soln_pop)):
            # check and update fitness
            if self.fitness[index] > best_fitness:
                best_fitness = self.fitness[index]

        return best_fitness

    def get_best_fitness_index(self):
        best_fitness = -9999
        best_index = 0
        # comb through our pop and find the one with the
        # best fitness value
        # print("Fit", self.fitness)
        for index in range(len(self.soln_pop)):
            # check and update fitness
            if self.fitness[index] > best_fitness:
                best_fitness = self.fitness[index]
                best_index = index

        return best_index

    def plot_fitness_values(self):
        generations_data = [i for i in range(1, self.gen_num + 1)]

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
        plt.ylabel("Fitness")
        plt.title("Average fitness value of solutions over the generations")
        plt.show()

        best_data = plt.scatter(
            generations_data,
            self.best_fitness_tracker,
            edgecolors="r",
            label="raw_data",
        )
        # axes.set_aspect(1)
        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        plt.title("Best fitness value of solutions over the generations")
        plt.show()

    def genetic_algo(self):
        # generate the initial population:
        self.gen_pop()

        # keep going until we complete our generations
        while self.gen_counter < self.gen_num:
            # cal fitness of entire population
            self.gen_pop_fitness()
            self.best_fitness_tracker.append(self.get_best_fitness())
            self.average_fitness_tracker.append(self.get_avg_fitness())

            # generate new population
            self.new_gen()
            #  update our fitness values
            self.gen_pop_fitness()
            # update counter
            self.gen_counter = self.gen_counter + 1
            self.SGA_logger()

        # best_index = self.get_best_fitness_index()
        # print("Best Index", best_index)

        # print graphs
        self.plot_fitness_values()
        # log for debugging
        self.SGA_logger()
        best_index = self.get_best_fitness_index()
        # print("Fitness", self.fitness)
        best_phenos = self.convert_bin_to_phenotype(self.soln_pop[best_index], 0.001)
        print("Best x, y", best_phenos.x, best_phenos.y)
        print("Best Z", self.six_hump(best_phenos.x, best_phenos.y))

    def testing(self):
        # print("TESTING")

        self.gen_pop()
        self.SGA_logger()

        # self.convert_bin_to_phenotype([1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1], 0.001)
        # print(len(self.soln_pop))
        # print("One row size", len(self.soln_pop[0]))
        # print("Checking one soln size")
        # print(self.soln_pop[0][0])
        # print(self.six_hump(-0.089840, 0.712659))
        # print(self.six_hump(0,0))
        # print(self.six_hump(0.089840,  -0.712659))
        # test_point = TDP.TD_Point(0.089840,  -0.712659)
        # test_point_1 = TDP.TD_Point(5,  5)
        # test_point_2 = TDP.TD_Point(-5,  -5)
        # print(self.fitness_function(test_point))
        # print(self.fitness_function(test_point_1))
        # print(self.fitness_function(test_point_2))

    def SGA_logger(self):
        # print("TODO")

        print("Poplation", self.soln_pop)
        print("Curent Gen:", self.gen_counter)
        print("Fitness", self.fitness)

        print("Best Fitness", self.best_fitness_tracker)
        print("Avg Fitness", self.average_fitness_tracker)
        print("Final Best Fitness", self.best_fitness_tracker[-1])

        # print("Current sol:", self.curr_sol  )
        # print("Tabu List:", self.tabu_list )
        # print("Cost:", self.cost )
        # print("Iterations:", self.iterations )
        # print("Best so far:", self.best_so_far)
        # print("Best solution seen:", self.best_soln_seen)
