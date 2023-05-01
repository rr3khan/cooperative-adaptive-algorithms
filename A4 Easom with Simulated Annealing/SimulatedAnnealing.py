# Author Riyad Khan
# ECE 457A Assignment 4 Question 3

# Import from random library to generate random points
from random import randint, random
from tabnanny import check

# for mathematical operations like cos
import math

# for our 2D coordinates x1 and x2
import TD_Coord


# Define the simulated annealing class here:
class SA:
    def __init__(
        self,
        sol0: TD_Coord,
        sol0_val,
        next_sol: TD_Coord,
        next_sol_val,
        t0: int,
        trf_alpha,
        iters_per_t,
        schedule,
    ):
        # initial solution location
        self.sol0 = sol0
        # initial solution value
        self.sol0_val = sol0_val
        # Potential next solution location
        self.next_sol = next_sol
        # Potential next solution value
        self.next_sol_val = next_sol_val
        # delta c the change in cost
        self.delta_c = 1000
        # initial temperature
        self.t0 = t0
        # alpha to determine how fast we decrease temperature
        self.trf_alpha = trf_alpha
        # probability of accepting the new solution
        # boolean determined by our acceptance function
        self.accept = False
        # number of iterations to check per temperature
        self.iters_per_t = iters_per_t
        # annealing schedule, either linear or geometric
        self.schedule = schedule
        # number of points checked
        self.num_pt_checked = 0
        # number of solutions accepted
        self.num_selected = 0

    # calculate distance to goal basically
    # calculate the distance between two points on a straight line
    # find distance from current solution to the point pi, pi

    def dist_goal(self, point: TD_Coord):
        return math.sqrt(pow(point.x1 - math.pi, 2) + pow(point.x2 - math.pi, 2))

    # calculate the cost difference between two solutions
    def cal_deltac(self) -> None:
        cost1 = self.dist_goal(self.sol0)
        cost2 = self.dist_goal(self.next_sol)
        # cost1 = 1 - abs(self.sol0_val)
        # cost2 = 1 - abs(self.next_sol_val)

        # print("Here delta_c:", self.delta_c)

        self.delta_c = cost2 - cost1

    # randomly calculates the next possible solution
    # using the neighbourhood of [-100, 100]
    # def cal_next(self) -> None:

    # self.next_sol.set_x1(randint(-100, 100))
    # self.next_sol.set_x2(randint(-100, 100))

    #     self.next_sol_val = easom_fn(self.next_sol.x1, self.next_sol.x2)

    # function to decide if we are keeping the new
    # solution or not

    def acceptance_fn(self):
        if self.delta_c <= 0:
            self.accept = True
        else:
            # calculate probability of acceptance
            prop = math.exp(-self.delta_c / self.t0)
            # generate a random point to determine
            # if we are selecting the worst solution
            randpt = random()
            # print("Random point:", randpt)
            if randpt < prop:
                self.accept = True
                # print("Accepted worst")
            else:
                self.accept = False

    def sa_algo(self):
        # Stopping condition t < 1
        while self.t0 > 1:
            # Repeat for each temperature iteration
            for iter in range(self.iters_per_t):
                # calculate change in cost of solutions
                self.cal_deltac()

                # check acceptance function
                self.acceptance_fn()

                # Update current solution
                if self.accept:
                    self.sol0.set_x1(self.next_sol.x1)
                    self.sol0.set_x2(self.next_sol.x2)
                    # self.sol0 = self.next_sol
                    self.sol0_val = easom_fn(self.sol0.x1, self.sol0.x2)
                    self.num_selected += 1

                self.num_pt_checked += 1

                # Generate another solution
                # self.cal_next()
                self.next_sol.set_x1(randint(-100, 100))
                self.next_sol.set_x2(randint(-100, 100))
                # self.next_sol.x2 = randint(-10, 10)
                self.next_sol_val = easom_fn(self.next_sol.x1, self.next_sol.x2)

                # compare solutions if they are the same point generate a new one
                # if self.sol0 == self.next_sol:
                #     self.next_sol = TD_Coord(randint(-10, 10), randint(-10, 10))
                #     # .x1 = randint(-10, 100)
                #     # self.next_sol.x2 = randint(-10, 100)
                #     self.next_sol_val = easom_fn(self.next_sol.x1, self.next_sol.x2)

                # self.sa_logger()

            # Decrease temperature based on annealing schedule
            if self.schedule == "linear":
                self.t0 = self.t0 - self.trf_alpha

            if self.schedule == "geometric":
                self.t0 = self.t0 * self.trf_alpha

        # self.sa_logger()
        print(
            "The annealing schedule of ",
            self.schedule,
            " found a solution at: ",
            self.sol0.x1,
            ",",
            self.sol0.x2,
            "with value: ",
            self.sol0_val,
        )

    def sa_logger(self):
        print("Current sol x1:", self.sol0.x1)
        print("Current sol x2:", self.sol0.x2)
        print("Current sol f:", self.sol0_val)
        # Potential next solution
        print("Next solution x1: ", self.next_sol.x1)
        print("Next solution x2: ", self.next_sol.x2)
        print("Next sol f:", self.next_sol_val)
        print("Delta C: ", self.delta_c)
        print("Iters per temp: ", self.iters_per_t)
        # initial temperature
        print("Current temperature: ", self.t0)
        # alpha to determine how fast we decrease temperature
        print("Current alpha: ", self.trf_alpha)
        # bound for the neighbourhood in our case [-100, 100]
        print("Accept next:", self.accept)
        print("Points checked:", self.num_pt_checked)
        print("Points accepted:", self.num_selected)
        print("Points rejected: ", self.num_pt_checked - self.num_selected)
        print("\n")


# define our Easom function here
def easom_fn(x1: int, x2: int):
    return (
        -math.cos(x1)
        * math.cos(x2)
        * math.exp(-pow((x1 - math.pi), 2) - pow((x2 - math.pi), 2))
    )


def debug_dist_goal(x1, x2):
    return math.sqrt(pow(x1 - math.pi, 2) + pow(x2 - math.pi, 2))
