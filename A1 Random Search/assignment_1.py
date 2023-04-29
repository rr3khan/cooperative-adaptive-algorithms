# Author Riyad Khan
# ECE 457A Assignment 1 Question 3

import mazeRunner


def main():
    maze = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    ]

    # This is a 2D list in Python. Note that the first row in the 2D list is the y = 0 row (i.e. bottom-most row in the maze figure). '1' indicates that the node is blocked, '0' indicates that it is free.

    # Given Data from the question
    # Special tile coordinates (x,y) each costing 30 points

    special_tiles = [
        [2, 12],
        [2, 13],
        [2, 14],
        [2, 15],
        [2, 16],
        [3, 16],
        [4, 16],
        [5, 16],
        [6, 16],
        [7, 16],
        [8, 16],
        [9, 16],
        [9, 17],
        [10, 17],
        [11, 17],
        [12, 17],
        [13, 17],
        [14, 17],
        [15, 17],
        [16, 17],
        [17, 17],
        [18, 17],
        [19, 17],
        [20, 17],
        [21, 17],
        [22, 17],
        [23, 17],
        [23, 18],
    ]

    # Set the value of the special tiles to a specific value for the special cost tiles
    for coordinate in special_tiles:
        maze[coordinate[1]][coordinate[0]] = mazeRunner.cell.SPECIAL

    a1S_start = [2, 11]

    a1E1_exit = [23, 19]

    a1E2_exit = [2, 21]

    move_limits = (pow(10, 3), pow(10, 4), pow(10, 5), pow(10, 6))

    user_Input = int(
        input(
            "What experiment do you want to run? please enter a number between 1 and 4 \n"
        )
    )

    match user_Input:
        case 1:
            # experiment 1 1 K moves
            randMaze1 = mazeRunner.mazeRunner(
                a1S_start, (a1E1_exit, a1E2_exit), move_limits[0], maze, special_tiles
            )
            randMaze1.randSearch()
        case 2:
            # experiment 2 10 K moves
            randMaze2 = mazeRunner.mazeRunner(
                a1S_start, (a1E1_exit, a1E2_exit), move_limits[1], maze, special_tiles
            )
            randMaze2.randSearch()
        case 3:
            # experiment 3 100 K moves
            randMaze3 = mazeRunner.mazeRunner(
                a1S_start, (a1E1_exit, a1E2_exit), move_limits[2], maze, special_tiles
            )
            randMaze3.randSearch()
        case 4:
            # experiment 4 1000 K moves
            randMaze4 = mazeRunner.mazeRunner(
                a1S_start, (a1E1_exit, a1E2_exit), move_limits[3], maze, special_tiles
            )
            randMaze4.randSearch()
        case _:
            print("Please enter an interger from 1 to 4 inclusive")

if __name__ == "__main__":
    main()