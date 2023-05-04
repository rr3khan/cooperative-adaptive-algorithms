# Author Riyad Khan
# ECE 457A Assignment 5 Question 2

# Import from random library to generate random points
from random import randint, random, sample
from tabnanny import check

# for mathematical operations like cos
import math


# Define the tabu search class here:
# each potential solution is stored in a list where the index is the location and the value is the department
class TS:
    def __init__(
        self,
        initial_soln,
        tabu_tenure: int,
        tabu_list,
        distances,
        flows,
        stopping_criteria,
        aspiration: bool,
        tabu_freq: bool,
        half_hood: bool,
    ):
        # initial solution
        self.curr_sol = initial_soln
        # tabu tenure
        self.tabu_tenure = tabu_tenure
        # tabu list
        self.tabu_list = tabu_list
        # cost of the current solution
        self.cost = 0
        self.dist = distances
        self.flow = flows
        # stopping criteria
        self.stopping_criteria = stopping_criteria
        # Bool to indicate if we are using the aspiration list
        self.aspiration = aspiration
        # Bool to indicate if we are penalizing by frequency
        self.tabu_freq = tabu_freq
        # number of iterations the search has gone through
        self.iterations = 0
        self.best_so_far = 10000
        self.best_soln_seen = []
        self.half_hood = half_hood

    # define tabu tenure as sqaure root of neighbourhood size
    def update_tabu_List(self, action, tabu_tenure):
        # if an action has a tabu tenure decrement it
        for department in range(20):
            # department + 1 since you cannot swap a department with itself, diagonal should always be 0
            for location in range(department + 1, 20):
                if self.tabu_list[department][location] > 0:
                    self.tabu_list[department][location] = (
                        self.tabu_list[department][location] - 1
                    )

        # if its a new action add it to the list
        self.tabu_list[action[0] - 1][action[1] - 1] = tabu_tenure

    # Calculates the cost for a solution
    def cal_cost(self, soln, action):
        cost = 0
        ## assuming the distances given in the excel sheet is the rectilinear disances
        for index_1 in range(20):
            # department + 1 since you cannot swap a department with itself, diagonal should always be 0
            for index_2 in range(index_1, 20):
                dist = self.dist.values[index_1][index_2]
                # get the flow values from the csv file
                flow = self.flow.values[soln[index_1] - 1][soln[index_2] - 1]
                cost = cost + (dist * flow)

        if self.tabu_freq:
            # penalize cost based on frequency
            cost = cost + self.tabu_list[action[1] - 1][action[0] - 1]

        return cost

    def swap_action(self, soln, index_1, index_2):
        """Produces a new solution
        by swapping two indexes
        """
        soln_2 = soln.copy()
        index = soln.index(index_1)
        index2 = soln.index(index_2)

        soln_2[index], soln_2[index2] = soln_2[index2], soln_2[index]

        return soln_2

    def gen_neighborhood(self, soln):
        """Generates the neighbourhood of potential next solutions"""

        # Dictionary to hold the neighbourhood
        neighbourhood_dict = {}
        for index_1 in range(20):
            for index_2 in range(index_1 + 1, 20):
                temp_soln = self.swap_action(soln, soln[index_1], soln[index_2])
                neighbourhood_dict[(index_1 + 1, index_2 + 1)] = self.cal_cost(
                    temp_soln, [[index_1 + 1], [index_2 + 1]]
                )

        return neighbourhood_dict

    def gen_ran_half_neigh(self, soln):
        """Generates half the neighbourhood of potential next solutions randomly"""
        # Dictionary to hold the neighbourhood
        neighbourhood_dict = {}

        # hard code half the neighbourhood as size 95

        while len(neighbourhood_dict) < 95:
            # randonmly add moves to it
            rand_index, rand_index2 = sample(range(1, 20), 2)
            temp_soln = self.swap_action(
                soln, soln[rand_index - 1], soln[rand_index2 - 1]
            )
            neighbourhood_dict[(rand_index, rand_index2)] = self.cal_cost(
                temp_soln, [rand_index, rand_index2]
            )

        return neighbourhood_dict

    def get_next_soln(self, soln):
        """Selects a solution from the neighbourhood of potential next solutions
        updates the tabu list with the selected moved
        """

        # generate the neighbourhood of solutions
        if self.half_hood:
            n_dict = self.gen_ran_half_neigh(soln)
        else:
            n_dict = self.gen_neighborhood(soln)

        best_soln = min(n_dict, key=n_dict.get)

        # if our current soln is better than the best seen so far update it

        skip = False

        if n_dict[best_soln] < self.best_so_far and self.aspiration:
            # print("B so far", self.best_so_far)
            # print("Best now",  n_dict[best_soln])
            self.best_so_far = n_dict[best_soln]
            self.best_soln_seen = soln
            skip = True

        # print(n_dict)
        # print("best soln" , best_soln)
        # print("best soln 1" , best_soln[0])

        # soln_index_1 = best_soln[0]
        # soln_index_2 = best_soln[1]
        # print("Type: ", type(soln_index_1))

        # get best soln and check if its in tabu_list

        aspiration = False

        # check aspiration here
        # print("N dict before pop: ", n_dict)
        if not skip:
            while (
                self.tabu_list[best_soln[0] - 1][best_soln[1] - 1] > 0
                and not aspiration
            ):
                # in tabu list
                # check aspiration condition or skip

                #  delete the previous best and get the next best
                n_dict.pop((best_soln[0], best_soln[1]))
                # print("N dict after pop: ", n_dict)
                best_soln = min(n_dict, key=n_dict.get)

        # skip = False

        # if skip:
        #     #  delete the previous best and get the next best
        #     n_dict.pop((best_soln[0], best_soln[1]))
        #     # del n_dict[best_soln[0], best_soln[1]]

        # select the solution
        # update tabu list
        self.update_tabu_List(best_soln, self.tabu_tenure)

        # update frequency tabu list
        self.tabu_list[best_soln[1] - 1][best_soln[0] - 1] = (
            self.tabu_list[best_soln[1] - 1][best_soln[0] - 1] + 1
        )

        # update solution
        self.curr_sol = self.swap_action(self.curr_sol, best_soln[0], best_soln[1])

        # update actions count
        self.iterations = self.iterations + 1

        # update cost of current soln
        self.cost = self.cal_cost(self.curr_sol, [best_soln[0] - 1, best_soln[1] - 1])

    def tabu_search(self):
        while self.stopping_criteria > 0:
            self.get_next_soln(self.curr_sol)
            # self.TS_logger()
            self.stopping_criteria = self.stopping_criteria - 1

    def testing(self):
        # self.get_next_soln(self.curr_sol)
        # print("cost: ", self.cal_cost(self.curr_sol))
        self.tabu_search()
        # self.get_next_soln(self.curr_sol)
        # self.TS_logger()

    def TS_logger(self):
        print("Current sol:", self.curr_sol)
        print("Tabu List:", self.tabu_list)
        print("Cost:", self.cost)
        print("Iterations:", self.iterations)
        print("Best so far:", self.best_so_far)
        print("Best solution seen:", self.best_soln_seen)
