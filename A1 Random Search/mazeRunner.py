# Author Riyad Khan
# ECE 457A Assignment 1 Question 3

# Import from random library to generate the moves for random search
from random import randint

# Import matplotlib to help with visualization
# from matplotlib import plt

class mazeRunner:
    def __init__(
        self,
        start_state: list[int, int],
        goal_state: tuple[int, int],
        moves_limit: int,
        map,
        special_tiles,
    ):
        self.cost_count = 0
        self.start_state = start_state
        self.goal_state = goal_state
        self.current_position = [start_state[0], start_state[1]]
        self.next_move = [0, 0]
        self.prev_position = [0, 0]
        self.moves_limit = moves_limit
        self.current_move_count = 0
        self.map = map
        self.special_tiles = special_tiles
        self.path = [start_state]

    # To move to the right increment x coordinate only

    def cal_right(self) -> list:
        return [self.current_position[0] + 1, self.current_position[1]]

    # To move to the left decrement x coordinate only

    def cal_left(self) -> list:
        return [self.current_position[0] - 1, self.current_position[1]]

    # To move up increment y coordinate only

    def cal_up(self) -> list:
        return [self.current_position[0], self.current_position[1] + 1]

    # To move down decrement y coordinate only

    def cal_down(self) -> list:
        return [self.current_position[0], self.current_position[1] - 1]

    # actually perform the move keeping track of costs and previous positions

    def update_position(self, next_move) -> None:
        self.prev_position = self.current_position
        self.current_position = next_move

        # If we land on a star tile increment by 30 else by 1
        if next_move in self.special_tiles:
            self.cost_count += 30
        else:
            self.cost_count += 1

        self.current_move_count += 1

    def check_blocked(self, potential_next_move) -> bool:
        if self.map[potential_next_move[1]][potential_next_move[0]] == 1:
            # code map is flipped i.e in terms of y then x ccordinates
            # print("Coordinate readings", potential_next_move[0], potential_next_move[1]  )
            # print("Map reading: ", self.map[potential_next_move[0]][potential_next_move[1]] )
            print(potential_next_move, " is blocked!")
            return True
        else:
            return False

    def debug_check_blocked(self, coordinate) -> bool:
        try:
            if self.map[coordinate[1]][coordinate[0]] == 1:
                # code map is flipped i.e in terms of y then x ccordinates
                # print("Coordinate readings", coordinate[0], coordinate[1]  )
                # print("Map reading: ", self.map[coordinate[0]][coordinate[1]])
                print(coordinate, " is blocked!")
                return True
            else:
                return False
        except:
            return False

    # check to make sure we do not go out of bounds of map
    # out of bounds would be if either x or y coordinate of next move
    # is negative or > 24
    def check_backrooms(self, potential_next_move) -> bool:
        ## try will only catch > 24 and not negative numbers
        try:
            self.map[potential_next_move[1]][potential_next_move[0]]
        except:
            print("Out of Bounds!")
            return True

        if (
            potential_next_move[0] < 0
            or potential_next_move[1] < 0
            or potential_next_move[0] > 24
            or potential_next_move[1] > 24
        ):
            print("Out of Bounds!")
            return True
        else:
            return False

    # check to ensure that we are not immediately returning to previous position
    def check_reversal(self, potential_next_move) -> bool:
        if potential_next_move == self.prev_position:
            return True
        else:
            return False

    # check trapped
    def check_trapped(self) -> bool:
        ## There are 2 known trapping coordinates (5, 22) and (6, 24) terminate if we get stuck here
        # To check if trapped check if all directions besides where you came from are blocked
        if self.current_position == [5, 22] or self.current_position == [6, 24]:
            print("Trapped in a corner")
            return True

        trapped = False
        for direction in [
            self.cal_right(),
            self.cal_down(),
            self.cal_left(),
            self.cal_up(),
        ]:
            print("Direction: ", direction)
            if direction == self.prev_position:
                print("Obstruction, recalculating move")
                # Do nothing we came from here so obviously it is not blocked
            # If any direction besides the previous position are not blocked then
            # return false we are not trapped
            elif self.debug_check_blocked(direction) == False:
                return False
            else:
                trapped = True

        print("UWU Onii Chan Help I'm Stuck")
        return trapped

    # used for debugging
    def log(self) -> None:
        print("Action cost count:", self.cost_count)
        print("Start: ", self.start_state)
        print("Goals: ", self.goal_state)
        print("Current Position: ", self.current_position)
        print("Next move: ", self.next_move)
        print("Previous move: ", self.prev_position)
        print("Moves limit: ", self.moves_limit)
        print("Move count: ", self.current_move_count)
        print("Path: ", self.path)

    def debugMap(self) -> None:
        print(self.map)
        # print ("Coordinates", self.map[tuple[0]][tuple[1]])

    def debug_next_move(self, next_move) -> None:
        self.next_move = next_move

    def debug_current_position(self, current_position) -> None:
        self.current_position = current_position
        print("Current test position is: ", current_position)

    # implementing the random search, use the randint function from the random module
    # decide on a random direction to move in by randomly generating an int between
    # 1 and 4 inclusive

    def randMove(self) -> list:
        randNum = randint(1, 4)
        print(randNum)

        # Move in a clockwise direction from 1 -> 4

        match randNum:
            case 1:
                print("Move Right")
                return self.cal_right()
            case 2:
                print("Move Down")
                return self.cal_down()
            case 3:
                print("Move Left")
                return self.cal_left()
            case 4:
                print("Move Up")
                return self.cal_up()
            case _:
                print(
                    "We should never reach here, bad luck no clip into the backrooms for you!"
                )
                return [-1, -1]

    def randSearch(self) -> None:
        # stop searching if either we use up all of our moves or reach to one of the goals

        while self.current_move_count < self.moves_limit:
            # Check if we are at the goal
            if (
                self.current_position == self.goal_state[1]
                or self.current_position == self.goal_state[0]
            ):
                self.log()
                print("Goal reached: ", self.current_position)
                break

            # Check if we are trapped
            if self.current_position == [5, 22] or self.current_position == [6, 25]:
                self.log()
                print("Got stuck terminating ", self.current_position)
                break

            # Not yet at goal, then continue moving
            potential_next_move = self.randMove()

            if (
                self.check_reversal(potential_next_move)
                or self.check_backrooms(potential_next_move)
                or self.check_blocked(potential_next_move)
            ):
                self.log()
                ## if we are blocked returning to previous position or going out of bounds do nothing and recalculate another move instead
            elif self.check_trapped():
                # If we are trapped terminate the search
                break
            else:
                self.next_move = potential_next_move
                self.update_position(self.next_move)
                self.path.append(self.next_move)
                self.log()

        if self.current_move_count == self.moves_limit:
            print("No goal found too bad, out of moves!")
