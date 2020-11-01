import curses
from time import sleep
from random import randint
from copy import deepcopy
from typing import List

# Credit: Implemented as per this guide: https://robertheaton.com/2018/07/20/project-2-game-of-life/index.html


def random_state(width: int, height: int) -> List[List[int]]:
    """ Generate a random board state.

    A state is 2D array with values that are either 0 (dead) or 1 (alive).
    Arguments:
    width -- width of board in integer
    height -- height of board in integer

    Returns:
        2D random array containing 0 or 1s.
    """
    return [[randint(0, 1) for _ in range(width)] for _ in range(height)]


def render(state: List[List[int]], scr, alive_char: str = "#") -> None:
    """ Pretty-print the board state in curses screen.
    Arguments:
        state: 2D array containing 0 or 1s.
        scr: ncurses screen
        alive_char: character to represent alive cell.
    """
    state_string = "-" * (len(state[0]) + 2) + "\n"
    for row in state:
        state_string += "|"
        state_string += "".join(map(lambda x: alive_char if x == 1 else " ", row))
        state_string += "|\n"
    state_string += "-" * (len(state[0]) + 2)
    scr.addstr(0, 0, state_string)
    scr.refresh()


def get_neighbours(state: List[List[int]]) -> List[List[int]]:
    """ Calculate and return neighbours of each cell in 2D array.

    Note: Ends wrap. E.g. [0,0] will have [-1,-1] as neighbour.

    Arguments:
        state: n*m array containing 0 or 1s.
    Returns:
        state: n*m array containing sum of 8 neighbours in corresponding position in state.
    """
    neighbours = deepcopy(state)

    for i in range(len(state)):
        top = i - 1
        bottom = (i + 1) % len(state)
        for j in range(len(state[i])):
            left = j - 1
            right = (j + 1) % len(state[i])

            neighbours[i][j] = (
                  state[top][left]
                + state[top][j]
                + state[top][right]
                + state[i][left]
                + state[i][right]
                + state[bottom][left]
                + state[bottom][j]
                + state[bottom][right]
            )

    return neighbours


def next_board_state(state: List[List[int]]) -> List[List[int]]:
    """ Calculate next state based on rules of game of life.

    1. Underpopulation. Any cell with <2 live neighbours dies.
    2. Overpopulation. Any cell with >3 live neighbours dies.
    3. Balanced. Any cell with 2 or 3 live neighbours lives.
    4. Reproduction. Dead cell with exactly 3 live neighbours becomes alive.

    Arguments:
        state: 2D array containing 0 or 1s.
    Returns:
        state: 2D array containing 0 or 1s representing next stage
               according to game of life rules
    """
    neighbours = get_neighbours(state)

    for i in range(len(state)):
        for j in range(len(state[i])):
            n = neighbours[i][j]
            # Over or underpopulated
            if n > 3 or n < 2:
                state[i][j] = 0
            # Reproduction. Rule 3 is handled automatically.
            elif n == 3:
                state[i][j] = 1
            else:
                continue
    return state


if __name__ == "__main__":
    state = random_state(80, 40)
    stdscr = curses.initscr()
    while True:
        render(state, stdscr)
        state = next_board_state(state)
        sleep(0.5)
