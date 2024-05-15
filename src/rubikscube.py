import copy
import random

import numpy as np
from .permutation_table import viable_moves, edge_perms, corner_perms, reverse_moves


class RubiksCube:
    def __init__(self, scramble=""):
        """
        Initializes a new Rubik's Cube with a default configuration and allows for optional scrambling.

        Each face of the cube (Front, Back, Up, Down, Left, Right) is represented as a 3x3 matrix of integers, where
        each integer corresponds to a color:
        - 1: Front (F)
        - 2: Back (B)
        - 3: Up (U)
        - 4: Down (D)
        - 5: Left (L)
        - 6: Right (R)

        The cube's state is stored in a dictionary with keys as face identifiers and values as the 3x3 numpy arrays.

        Adjacency information is stored in another dictionary to manage the relationships between faces and their pieces.
        Used for calculating the score based on the number of scrambled pieces.

        Args:
            scramble (str): A string of moves to scramble the cube after initialization. Each character in the string
                            represents a specific move.

        Attributes:
            cube (dict): Dictionary containing the current state of each face of the cube, represented by 3x3 numpy arrays.
            adjacencies (dict): Contains the adjacency information for each face, detailing which rows or columns of one
                                face connect to another face during rotations.
            move_history (list): A list to keep track of each move applied to the cube.
            scramble (str): The initial set of moves applied to the cube upon creation.
            solved (bool): A flag to indicate whether the cube is in a solved state.

        This class also initializes the cube to a solved state unless a scramble sequence is provided, which will
        mix up the cube according to the sequence of moves defined.
        """
        self.cube = {
            'F': np.array([[1 for _ in range(3)] for _ in range(3)]),
            'B': np.array([[2 for _ in range(3)] for _ in range(3)]),
            'U': np.array([[3 for _ in range(3)] for _ in range(3)]),
            'D': np.array([[4 for _ in range(3)] for _ in range(3)]),
            'L': np.array([[5 for _ in range(3)] for _ in range(3)]),
            'R': np.array([[6 for _ in range(3)] for _ in range(3)])
        }
        self.adjacencies = {
            'U': {'edges': [('F', (2, 1), (0, 1)), ('R', (1, 2), (0, 1)), ('B', (0, 1), (0, 1)), ('L', (1, 0), (0, 1))],
                  'corners': [('F', 'R', (2, 2), (0, 2), (0, 0)), ('R', 'B', (0, 2), (0, 2), (0, 0)),
                              ('B', 'L', (0, 0), (0, 2), (0, 0)), ('L', 'F', (2, 0), (0, 2), (0, 0))]},
            'D': {'edges': [('F', (0, 1), (2, 1)), ('R', (1, 2), (2, 1)), ('B', (2, 1), (2, 1)), ('L', (1, 0), (2, 1))],
                  'corners': [('F', 'R', (0, 2), (2, 2), (2, 0)), ('R', 'B', (2, 2), (2, 2), (2, 0)),
                              ('B', 'L', (2, 0), (2, 2), (2, 0)), ('L', 'F', (0, 0), (2, 2), (2, 0))]},
            'R': {'edges': [('F', (1, 0), (1, 2)), ('B', (1, 2), (1, 0))],
                  'corners': []},
            'L': {'edges': [('F', (1, 2), (1, 0)), ('B', (1, 0), (1, 2))],
                  'corners': []},
            'F': {'edges': [],
                  'corners': []},
            'B': {'edges': [],
                  'corners': []}
        }
        self.move_history = []
        self.scramble = scramble
        self.solved = False

    def get_scramble(self):
        return self.scramble

    def reset_state(self):
        self.cube = {
            'F': np.array([[1 for _ in range(3)] for _ in range(3)]),
            'B': np.array([[2 for _ in range(3)] for _ in range(3)]),
            'U': np.array([[3 for _ in range(3)] for _ in range(3)]),
            'D': np.array([[4 for _ in range(3)] for _ in range(3)]),
            'L': np.array([[5 for _ in range(3)] for _ in range(3)]),
            'R': np.array([[6 for _ in range(3)] for _ in range(3)])
        }

    def copy(self):
        new_cube = RubiksCube(self.scramble)
        new_cube.cube = copy.deepcopy(self.cube)
        new_cube.move_history = copy.deepcopy(self.move_history)
        new_cube.solved = self.solved
        return new_cube

    def update(self, other):
        self.scramble = other.scramble
        self.cube = copy.deepcopy(other.cube)
        self.move_history = copy.deepcopy(other.move_history)
        self.solved = other.solved

    def rotate_face(self, face):
        """
               Rotates a specified face of the cube and updates adjacent edges accordingly.

               Args:
                   face (str): The face to rotate, followed by an optional direction (' or 2).
                               'F', 'B', 'U', 'D', 'L', 'R', 'M', 'E', 'S', 'x', 'y', 'z'.
               """

        if face == "F":
            self.cube["F"] = np.rot90(self.cube["F"], k=-1)
            temp_top = np.copy(self.cube['U'][2, :])
            temp_bottom = np.copy(self.cube['D'][0, :])
            temp_left = np.copy(self.cube['L'][:, 2])
            temp_right = np.copy(self.cube['R'][:, 0])

            self.cube['U'][2, :] = temp_left[::-1]
            self.cube['D'][0, :] = temp_right[::-1]
            self.cube['L'][:, 2] = temp_bottom
            self.cube['R'][:, 0] = temp_top
        elif face == "F'":
            self.cube["F"] = np.rot90(self.cube["F"])
            temp_top = np.copy(self.cube['U'][2, :])
            temp_bottom = np.copy(self.cube['D'][0, :])
            temp_left = np.copy(self.cube['L'][:, 2])
            temp_right = np.copy(self.cube['R'][:, 0])

            self.cube['U'][2, :] = temp_right
            self.cube['D'][0, :] = temp_left
            self.cube['L'][:, 2] = temp_top[::-1]
            self.cube['R'][:, 0] = temp_bottom[::-1]
        elif face == "F2":
            self.cube["F"] = np.rot90(self.cube["F"], k=2)
            temp_top = np.copy(self.cube['U'][2, :])
            temp_bottom = np.copy(self.cube['D'][0, :])
            temp_left = np.copy(self.cube['L'][:, 2])
            temp_right = np.copy(self.cube['R'][:, 0])

            self.cube['U'][2, :] = temp_bottom[::-1]
            self.cube['D'][0, :] = temp_top[::-1]
            self.cube['L'][:, 2] = temp_right[::-1]
            self.cube['R'][:, 0] = temp_left[::-1]

        elif face == "D":
            self.cube["D"] = np.rot90(self.cube["D"], k=-1)
            temp_front = np.copy(self.cube['F'][2, :])
            temp_left = np.copy(self.cube['L'][2, :])
            temp_back = np.copy(self.cube['B'][2, :])
            temp_right = np.copy(self.cube['R'][2, :])

            self.cube['B'][2, :] = temp_right
            self.cube['R'][2, :] = temp_front
            self.cube['F'][2, :] = temp_left
            self.cube['L'][2, :] = temp_back
        elif face == "D'":
            self.cube["D"] = np.rot90(self.cube["D"])
            temp_front = np.copy(self.cube['F'][2, :])
            temp_left = np.copy(self.cube['L'][2, :])
            temp_back = np.copy(self.cube['B'][2, :])
            temp_right = np.copy(self.cube['R'][2, :])

            self.cube['B'][2, :] = temp_left
            self.cube['R'][2, :] = temp_back
            self.cube['F'][2, :] = temp_right
            self.cube['L'][2, :] = temp_front
        elif face == "D2":
            self.cube["D"] = np.rot90(self.cube["D"], k=2)
            temp_front = np.copy(self.cube['F'][2, :])
            temp_left = np.copy(self.cube['L'][2, :])
            temp_back = np.copy(self.cube['B'][2, :])
            temp_right = np.copy(self.cube['R'][2, :])

            self.cube['B'][2, :] = temp_front
            self.cube['R'][2, :] = temp_left
            self.cube['F'][2, :] = temp_back
            self.cube['L'][2, :] = temp_right
        elif face == "R":
            self.cube["R"] = np.rot90(self.cube["R"], k=-1)
            temp_front = np.copy(self.cube['F'][:, 2])
            temp_up = np.copy(self.cube['U'][:, 2])
            temp_down = np.copy(self.cube['D'][:, 2])
            temp_back = np.copy(self.cube['B'][:, 0])

            self.cube['F'][:, 2] = temp_down
            self.cube['U'][:, 2] = temp_front
            self.cube['D'][:, 2] = temp_back[::-1]
            self.cube['B'][:, 0] = temp_up[::-1]
        elif face == "R'":
            self.cube["R"] = np.rot90(self.cube["R"])
            temp_front = np.copy(self.cube['F'][:, 2])
            temp_up = np.copy(self.cube['U'][:, 2])
            temp_down = np.copy(self.cube['D'][:, 2])
            temp_back = np.copy(self.cube['B'][:, 0])

            self.cube['F'][:, 2] = temp_up
            self.cube['U'][:, 2] = temp_back[::-1]
            self.cube['D'][:, 2] = temp_front
            self.cube['B'][:, 0] = temp_down[::-1]
        elif face == "R2":
            self.cube["R"] = np.rot90(self.cube["R"], k=2)
            temp_front = np.copy(self.cube['F'][:, 2])
            temp_up = np.copy(self.cube['U'][:, 2])
            temp_down = np.copy(self.cube['D'][:, 2])
            temp_back = np.copy(self.cube['B'][:, 0])

            self.cube['F'][:, 2] = temp_back[::-1]
            self.cube['U'][:, 2] = temp_down
            self.cube['D'][:, 2] = temp_up
            self.cube['B'][:, 0] = temp_front[::-1]
        elif face == "L":
            self.cube["L"] = np.rot90(self.cube["L"], k=-1)
            temp_front = np.copy(self.cube['F'][:, 0])
            temp_up = np.copy(self.cube['U'][:, 0])
            temp_down = np.copy(self.cube['D'][:, 0])
            temp_back = np.copy(self.cube['B'][:, 2])

            self.cube['F'][:, 0] = temp_up
            self.cube['U'][:, 0] = temp_back[::-1]
            self.cube['D'][:, 0] = temp_front
            self.cube['B'][:, 2] = temp_down[::-1]
        elif face == "L'":
            self.cube["L"] = np.rot90(self.cube["L"])
            temp_front = np.copy(self.cube['F'][:, 0])
            temp_up = np.copy(self.cube['U'][:, 0])
            temp_down = np.copy(self.cube['D'][:, 0])
            temp_back = np.copy(self.cube['B'][:, 2])

            self.cube['F'][:, 0] = temp_down
            self.cube['U'][:, 0] = temp_front
            self.cube['D'][:, 0] = temp_back[::-1]
            self.cube['B'][:, 2] = temp_up[::-1]
        elif face == "L2":
            self.cube["L"] = np.rot90(self.cube["L"], k=2)
            temp_front = np.copy(self.cube['F'][:, 0])
            temp_up = np.copy(self.cube['U'][:, 0])
            temp_down = np.copy(self.cube['D'][:, 0])
            temp_back = np.copy(self.cube['B'][:, 2])

            self.cube['F'][:, 0] = temp_back[::-1]
            self.cube['U'][:, 0] = temp_down
            self.cube['D'][:, 0] = temp_up
            self.cube['B'][:, 2] = temp_front[::-1]
        elif face == "B":
            self.cube["B"] = np.rot90(self.cube["B"], k=-1)
            temp_top = np.copy(self.cube['U'][0, :])
            temp_bottom = np.copy(self.cube['D'][2, :])
            temp_left = np.copy(self.cube['L'][:, 0])
            temp_right = np.copy(self.cube['R'][:, 2])

            self.cube['U'][0, :] = temp_right
            self.cube['D'][2, :] = temp_left
            self.cube['L'][:, 0] = temp_top[::-1]
            self.cube['R'][:, 2] = temp_bottom[::-1]
        elif face == "B'":
            self.cube["B"] = np.rot90(self.cube["B"])
            temp_top = np.copy(self.cube['U'][0, :])
            temp_bottom = np.copy(self.cube['D'][2, :])
            temp_left = np.copy(self.cube['L'][:, 0])
            temp_right = np.copy(self.cube['R'][:, 2])

            self.cube['U'][0, :] = temp_left[::-1]
            self.cube['D'][2, :] = temp_right[::-1]
            self.cube['L'][:, 0] = temp_bottom
            self.cube['R'][:, 2] = temp_top
        elif face == "B2":
            self.cube["B"] = np.rot90(self.cube["B"], k=2)
            temp_top = np.copy(self.cube['U'][0, :])
            temp_bottom = np.copy(self.cube['D'][2, :])
            temp_left = np.copy(self.cube['L'][:, 0])
            temp_right = np.copy(self.cube['R'][:, 2])

            self.cube['U'][0, :] = temp_bottom[::-1]
            self.cube['D'][2, :] = temp_top[::-1]
            self.cube['L'][:, 0] = temp_right[::-1]
            self.cube['R'][:, 2] = temp_left[::-1]
        elif face == "U":
            self.cube["U"] = np.rot90(self.cube["U"], k=-1)
            temp_front = np.copy(self.cube['F'][0, :])
            temp_left = np.copy(self.cube['L'][0, :])
            temp_back = np.copy(self.cube['B'][0, :])
            temp_right = np.copy(self.cube['R'][0, :])

            self.cube['F'][0, :] = temp_right
            self.cube['L'][0, :] = temp_front
            self.cube['B'][0, :] = temp_left
            self.cube['R'][0, :] = temp_back
        elif face == "U'":
            self.cube["U"] = np.rot90(self.cube["U"])
            temp_front = np.copy(self.cube['F'][0, :])
            temp_left = np.copy(self.cube['L'][0, :])
            temp_back = np.copy(self.cube['B'][0, :])
            temp_right = np.copy(self.cube['R'][0, :])

            self.cube['F'][0, :] = temp_left
            self.cube['L'][0, :] = temp_back
            self.cube['B'][0, :] = temp_right
            self.cube['R'][0, :] = temp_front
        elif face == "U2":
            self.cube["U"] = np.rot90(self.cube["U"], k=2)
            temp_front = np.copy(self.cube['F'][0, :])
            temp_left = np.copy(self.cube['L'][0, :])
            temp_back = np.copy(self.cube['B'][0, :])
            temp_right = np.copy(self.cube['R'][0, :])

            self.cube['F'][0, :] = temp_back
            self.cube['L'][0, :] = temp_right
            self.cube['B'][0, :] = temp_front
            self.cube['R'][0, :] = temp_left
        elif face == "x":
            self.cube["R"] = np.rot90(self.cube["R"], k=-1)
            self.cube["L"] = np.rot90(self.cube["L"])
            temp_front = np.copy(self.cube['F'])
            temp_up = np.copy(self.cube['U'])
            temp_down = np.copy(self.cube['D'])
            temp_back = np.copy(self.cube['B'])

            self.cube['F'] = temp_down
            self.cube['U'] = temp_front
            self.cube['D'] = np.rot90(temp_back, k=2)
            self.cube['B'] = np.rot90(temp_up, k=2)
        elif face == "x'":
            self.cube["R"] = np.rot90(self.cube["R"])
            self.cube["L"] = np.rot90(self.cube["L"], k=-1)
            temp_front = np.copy(self.cube['F'])
            temp_up = np.copy(self.cube['U'])
            temp_down = np.copy(self.cube['D'])
            temp_back = np.copy(self.cube['B'])

            self.cube['F'] = temp_up
            self.cube['U'] = np.rot90(temp_back, k=2)
            self.cube['D'] = temp_front
            self.cube['B'] = np.rot90(temp_down, k=2)
        elif face == "x2":
            self.cube["R"] = np.rot90(self.cube["R"], k=2)
            self.cube["L"] = np.rot90(self.cube["L"], k=2)
            temp_front = np.copy(self.cube['F'])
            temp_up = np.copy(self.cube['U'])
            temp_down = np.copy(self.cube['D'])
            temp_back = np.copy(self.cube['B'])

            self.cube['F'] = np.rot90(temp_back, k=2)
            self.cube['U'] = temp_down
            self.cube['D'] = temp_up
            self.cube['B'] = np.rot90(temp_front, k=2)
        elif face == "M":
            temp_front = np.copy(self.cube['F'])
            temp_up = np.copy(self.cube['U'])
            temp_down = np.copy(self.cube['D'])
            temp_back = np.copy(self.cube['B'])

            self.cube['F'][:, 1] = temp_up[:, 1]
            self.cube['U'][:, 1] = np.rot90(temp_back, k=2)[:, 1]
            self.cube['D'][:, 1] = temp_front[:, 1]
            self.cube['B'][:, 1] = np.rot90(temp_down, k=2)[:, 1]
        elif face == "M'":
            temp_front = np.copy(self.cube['F'])
            temp_up = np.copy(self.cube['U'])
            temp_down = np.copy(self.cube['D'])
            temp_back = np.copy(self.cube['B'])

            self.cube['F'][:, 1] = temp_down[:, 1]
            self.cube['U'][:, 1] = temp_front[:, 1]
            self.cube['D'][:, 1] = np.rot90(temp_back, k=2)[:, 1]
            self.cube['B'][:, 1] = np.rot90(temp_up, k=2)[:, 1]
        elif face == "M2":
            temp_front = np.copy(self.cube['F'])
            temp_up = np.copy(self.cube['U'])
            temp_down = np.copy(self.cube['D'])
            temp_back = np.copy(self.cube['B'])

            self.cube['F'][:, 1] = np.rot90(temp_back, k=2)[:, 1]
            self.cube['U'][:, 1] = temp_down[:, 1]
            self.cube['D'][:, 1] = temp_up[:, 1]
            self.cube['B'][:, 1] = np.rot90(temp_front, k=2)[:, 1]
        elif face == "y":
            self.cube["U"] = np.rot90(self.cube["U"], k=-1)
            self.cube["D"] = np.rot90(self.cube["D"])
            temp_front = np.copy(self.cube['F'])
            temp_left = np.copy(self.cube['L'])
            temp_back = np.copy(self.cube['B'])
            temp_right = np.copy(self.cube['R'])

            self.cube['F'] = temp_right
            self.cube['L'] = temp_front
            self.cube['B'] = temp_left
            self.cube['R'] = temp_back
        elif face == "y'":
            self.cube["U"] = np.rot90(self.cube["U"])
            self.cube["D"] = np.rot90(self.cube["D"], k=-1)
            temp_front = np.copy(self.cube['F'])
            temp_left = np.copy(self.cube['L'])
            temp_back = np.copy(self.cube['B'])
            temp_right = np.copy(self.cube['R'])

            self.cube['F'] = temp_left
            self.cube['L'] = temp_back
            self.cube['B'] = temp_right
            self.cube['R'] = temp_front
        elif face == "y2":
            self.cube["U"] = np.rot90(self.cube["U"], k=2)
            self.cube["D"] = np.rot90(self.cube["D"], k=2)
            temp_front = np.copy(self.cube['F'])
            temp_left = np.copy(self.cube['L'])
            temp_back = np.copy(self.cube['B'])
            temp_right = np.copy(self.cube['R'])

            self.cube['F'] = temp_back
            self.cube['L'] = temp_right
            self.cube['B'] = temp_front
            self.cube['R'] = temp_left
        elif face == "E":
            temp_front = np.copy(self.cube['F'])
            temp_left = np.copy(self.cube['L'])
            temp_back = np.copy(self.cube['B'])
            temp_right = np.copy(self.cube['R'])

            self.cube['F'][1, :] = temp_left[1, :]
            self.cube['L'][1, :] = temp_back[1, :]
            self.cube['B'][1, :] = temp_right[1, :]
            self.cube['R'][1, :] = temp_front[1, :]
        elif face == "E'":
            temp_front = np.copy(self.cube['F'])
            temp_left = np.copy(self.cube['L'])
            temp_back = np.copy(self.cube['B'])
            temp_right = np.copy(self.cube['R'])

            self.cube['F'][1, :] = temp_right[1, :]
            self.cube['L'][1, :] = temp_front[1, :]
            self.cube['B'][1, :] = temp_left[1, :]
            self.cube['R'][1, :] = temp_back[1, :]
        elif face == "E2":
            temp_front = np.copy(self.cube['F'])
            temp_left = np.copy(self.cube['L'])
            temp_back = np.copy(self.cube['B'])
            temp_right = np.copy(self.cube['R'])

            self.cube['F'][1, :] = temp_back[1, :]
            self.cube['L'][1, :] = temp_right[1, :]
            self.cube['B'][1, :] = temp_front[1, :]
            self.cube['R'][1, :] = temp_left[1, :]
        elif face == "z":
            self.cube["F"] = np.rot90(self.cube["F"], k=-1)
            self.cube["B"] = np.rot90(self.cube["B"])
            temp_top = np.copy(self.cube['U'])
            temp_bottom = np.copy(self.cube['D'])
            temp_left = np.copy(self.cube['L'])
            temp_right = np.copy(self.cube['R'])

            self.cube['U'] = np.rot90(temp_left, k=-1)
            self.cube['D'] = np.rot90(temp_right, k=-1)
            self.cube['L'] = np.rot90(temp_bottom, k=-1)
            self.cube['R'] = np.rot90(temp_top, k=-1)
        elif face == "z'":
            self.cube["F"] = np.rot90(self.cube["F"])
            self.cube["B"] = np.rot90(self.cube["B"], k=-1)
            temp_top = np.copy(self.cube['U'])
            temp_bottom = np.copy(self.cube['D'])
            temp_left = np.copy(self.cube['L'])
            temp_right = np.copy(self.cube['R'])

            self.cube['U'] = np.rot90(temp_right)
            self.cube['D'] = np.rot90(temp_left)
            self.cube['L'] = np.rot90(temp_top)
            self.cube['R'] = np.rot90(temp_bottom)
        elif face == "z2":
            self.cube["F"] = np.rot90(self.cube["F"], k=2)
            self.cube["B"] = np.rot90(self.cube["B"], k=2)
            temp_top = np.copy(self.cube['U'])
            temp_bottom = np.copy(self.cube['D'])
            temp_left = np.copy(self.cube['L'])
            temp_right = np.copy(self.cube['R'])

            self.cube['U'] = np.rot90(temp_bottom, k=2)
            self.cube['D'] = np.rot90(temp_top, k=2)
            self.cube['L'] = np.rot90(temp_right, k=2)
            self.cube['R'] = np.rot90(temp_left, k=2)
        elif face == "S":
            temp_top = np.copy(self.cube['U'])
            temp_bottom = np.copy(self.cube['D'])
            temp_left = np.copy(self.cube['L'])
            temp_right = np.copy(self.cube['R'])

            self.cube['U'][1, :] = np.rot90(temp_left, k=-1)[1, :]
            self.cube['D'][1, :] = np.rot90(temp_right, k=-1)[1, :]
            self.cube['L'][:, 1] = np.rot90(temp_bottom, k=-1)[:, 1]
            self.cube['R'][:, 1] = np.rot90(temp_top, k=-1)[:, 1]
        elif face == "S'":
            temp_top = np.copy(self.cube['U'])
            temp_bottom = np.copy(self.cube['D'])
            temp_left = np.copy(self.cube['L'])
            temp_right = np.copy(self.cube['R'])

            self.cube['U'][1, :] = np.rot90(temp_right)[1, :]
            self.cube['D'][1, :] = np.rot90(temp_left)[1, :]
            self.cube['L'][:, 1] = np.rot90(temp_top)[:, 1]
            self.cube['R'][:, 1] = np.rot90(temp_bottom)[:, 1]
        elif face == "S2":
            temp_top = np.copy(self.cube['U'])
            temp_bottom = np.copy(self.cube['D'])
            temp_left = np.copy(self.cube['L'])
            temp_right = np.copy(self.cube['R'])

            self.cube['U'][1, :] = np.rot90(temp_bottom, k=2)[1, :]
            self.cube['D'][1, :] = np.rot90(temp_top, k=2)[1, :]
            self.cube['L'][:, 1] = np.rot90(temp_right, k=2)[:, 1]
            self.cube['R'][:, 1] = np.rot90(temp_left, k=2)[:, 1]

    def make_alg(self, alg_name, move_count=1):
        """
        Applies a specific algorithm to the Rubik's Cube based on the provided algorithm name. The method supports
        multiple types of algorithm applications including random permutations of edges or corners, application of predefined
        moves, and even scrambling the cube based on a defined scramble sequence.

        Args:
            alg_name (str): The name of the algorithm to apply. It can be one of the following:
                            - "random_algs_edges": Applies a random algorithm from predefined edge permutations.
                            - "random_algs_corners": Applies a random algorithm from predefined corner permutations.
                            - "random_moves_algs_moves_prim_edges": Applies random moves, a predefined edge permutations, and then reverses the first moves.
                            - "random_moves_algs_moves_prim_corners": Applies random moves, a predefined corner permutations, and then reverses the first moves.
                            - "scramble": Applies a predefined scramble sequence.
            move_count (int): The number of times the algorithm is to be applied (default is 1).

        This method modifies the cube state directly by rotating faces as per the algorithms' definition and updates the
        move history to track changes.

        For "random_moves_algs_moves_prim_edges" and "random_moves_algs_moves_prim_corners", the method involves a
        three-step process:
        1. Applying a series of random moves.
        2. Applying a specific permutation from the predefined list.
        3. Reversing the initial random moves to bring the cube back to a potentially solvable state while embedding the permutation.

        For "scramble", it uses the scramble string split into moves and applies each move to the cube sequentially.

        The method leverages dictionaries of edge and corner permutations which map indices to specific move sequences
        ensuring varied and random application of these permutations based on random selections.
        """
        permutation_edges = {k: v for (k, v) in enumerate(edge_perms)}
        permutation_corners = {k: v for (k, v) in enumerate(corner_perms)}

        if alg_name == "random_algs_edges":
            for j in range(int(move_count)):
                random_key = random.choice(list(permutation_edges.keys()))
                random_value = permutation_edges[random_key]
                moves = random_value.split(" ")
                for i in range(len(moves)):
                    self.rotate_face(moves[i])

                self.move_history.append(str(random_key) + "_Edges")

        if alg_name == "random_algs_corners":
            for j in range(int(move_count)):
                random_key = random.choice(list(permutation_corners.keys()))
                random_value = permutation_corners[random_key]
                moves = random_value.split(" ")
                for i in range(len(moves)):
                    self.rotate_face(moves[i])

                self.move_history.append(str(random_key) + "_Corners")

        if alg_name == "random_moves_algs_moves_prim_edges":
            for j in range(int(move_count)):
                random_moves_str = " ".join([random.choice(list(viable_moves)) for _ in range(random.randint(0, 7))])
                random_moves = random_moves_str.split(" ")
                if random_moves[0] != "":
                    reverse_random_moves = (reverse_moves(random_moves_str)).split(" ")
                    for i in range(len(random_moves)):
                        self.rotate_face(random_moves[i])
                        self.move_history.append(random_moves[i])

                    random_key = random.choice(list(permutation_edges.keys()))
                    random_value = permutation_edges[random_key]
                    moves = random_value.split(" ")

                    for i in range(len(moves)):
                        self.rotate_face(moves[i])
                    self.move_history.append(str(random_key) + "_Edges")

                    for i in range(len(reverse_random_moves)):
                        self.rotate_face(reverse_random_moves[i])
                        self.move_history.append(reverse_random_moves[i])
                else:
                    random_key = random.choice(list(permutation_edges.keys()))
                    random_value = permutation_edges[random_key]
                    moves = random_value.split(" ")

                    for i in range(len(moves)):
                        self.rotate_face(moves[i])
                    self.move_history.append(str(random_key) + "_Edges")

        if alg_name == "random_moves_algs_moves_prim_corners":
            for j in range(int(move_count)):
                random_moves_str = " ".join([random.choice(list(viable_moves)) for _ in range(random.randint(0, 7))])
                random_moves = random_moves_str.split(" ")
                if random_moves[0] != "":
                    reverse_random_moves = (reverse_moves(random_moves_str)).split(" ")
                    for i in range(len(random_moves)):
                        self.rotate_face(random_moves[i])
                        self.move_history.append(random_moves[i])

                    random_key = random.choice(list(permutation_corners.keys()))
                    random_value = permutation_corners[random_key]
                    moves = random_value.split(" ")

                    for i in range(len(moves)):
                        self.rotate_face(moves[i])
                    self.move_history.append(str(random_key) + "_Corners")

                    for i in range(len(reverse_random_moves)):
                        self.rotate_face(reverse_random_moves[i])
                        self.move_history.append(reverse_random_moves[i])
                else:
                    random_key = random.choice(list(permutation_corners.keys()))
                    random_value = permutation_corners[random_key]
                    moves = random_value.split(" ")

                    for i in range(len(moves)):
                        self.rotate_face(moves[i])
                    self.move_history.append(str(random_key) + "_Corners")

        if alg_name == "scramble":
            moves = self.scramble.split(" ")
            for i in range(len(moves)):
                self.rotate_face(moves[i])

    def make_alg_from_moves(self, alg=""):
        if alg != "":
            moves = alg.split(" ")
            for i in range(len(moves)):
                self.rotate_face(moves[i])
                self.move_history.append(moves[i])
            return

    def get_score(self):
        """
        Calculates and returns a score based on the current state of the Rubik's Cube, assessing edge and corner alignment.

        This method iterates through each face of the cube, checking the alignment of each edge and corner with the center
        piece of each face. The scoring is based on the deviation from a solved state:
        - For each edge or corner that is not correctly aligned with the center pieces of its respective faces, the score increments.
        - Edge misalignments increment the edge score.
        - Corner misalignments increment the corner score.
        - The total score is the sum of all misalignments.

        The score serves as a heuristic for the cube's current state:
        - A total score of 0 indicates that the cube is solved.
        - Higher scores indicate more misalignments.

        Attributes are updated based on the score:
        - `solved` is set to True if the score is 0 (cube is solved), otherwise it is set to False.

        Returns:
            tuple: A tuple containing three integers:
                   1. Total score: The sum of edge and corner misalignments.
                   2. Edge score: The total number of edge misalignments.
                   3. Corner score: The total number of corner misalignments.
        """
        score = 0
        edge_score = 0
        corner_score = 0
        for face in self.cube:
            center = self.cube[face][1, 1]
            adjacent = self.adjacencies[face]
            adjacent_edges = adjacent["edges"]
            adjacent_corners = adjacent["corners"]
            for adjacent_face, edge_coords_1, edge_coords_2 in adjacent_edges:
                if (self.cube[face][edge_coords_1[0]][edge_coords_1[1]] != center or
                        self.cube[adjacent_face][edge_coords_2[0]][edge_coords_2[1]] != self.cube[adjacent_face][1][1]):
                    score += 1
                    edge_score += 1
            for adjacent_face_1, adjacent_face_2, edge_coords_1, edge_coords_2, edge_coords_3 in adjacent_corners:
                if (self.cube[face][edge_coords_1[0]][edge_coords_1[1]] != center or
                        self.cube[adjacent_face_1][edge_coords_2[0]][edge_coords_2[1]] !=
                        self.cube[adjacent_face_1][1][1] or
                        self.cube[adjacent_face_2][edge_coords_3[0]][edge_coords_3[1]] !=
                        self.cube[adjacent_face_2][1][1]):
                    score += 1
                    corner_score += 1
        if score == 0:
            self.solved = True
        else:
            self.solved = False
        return score, edge_score, corner_score

    def display(self):
        """
        Displays the current state of the Rubik's Cube in a 2D cross format.

        This method visualizes the cube by arranging the six faces (U, D, L, R, F, B) in a cross pattern, which
        facilitates a more intuitive view of the cube’s state on a 2D display. The layout is as follows:

            +---+---+---+
            |   | U |   |
            +---+---+---+
            | L | F | R | B |
            +---+---+---+
            |   | D |   |
            +---+---+---+

        The 'U' (Up), 'D' (Down), 'L' (Left), 'R' (Right), 'F' (Front), and 'B' (Back) faces are displayed using their
        respective identifiers, with blank spaces used for alignment.

        Each face is represented as a 3x3 grid, where each grid cell corresponds to a single sticker on the face.
        The grid cells are displayed with their current numeric identifiers, allowing for easy visualization of the
        cube's configuration. The method prints the cross directly to the standard output.

        Notes:
            - This method prints directly and does not return any values.
        """
        blank_face = np.full((3, 3), ' ')
        upper = np.hstack((blank_face, self.cube['U'], blank_face, blank_face))
        middle = np.hstack((self.cube['L'], self.cube['F'], self.cube['R'], self.cube['B']))
        lower = np.hstack((blank_face, self.cube['D'], blank_face, blank_face))

        cross = np.vstack((upper, middle, lower))

        for row in cross:
            print(' '.join(str(cell) for cell in row))
        print()
