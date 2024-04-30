import copy
import random

import numpy as np
from .permutation_table import perms_all, viable_moves


class RubiksCube:
    def __init__(self, scramble=""):
        self.cube = {
            'F': np.array([[1 for _ in range(3)] for _ in range(3)]),
            'B': np.array([[2 for _ in range(3)] for _ in range(3)]),
            'U': np.array([[3 for _ in range(3)] for _ in range(3)]),
            'D': np.array([[4 for _ in range(3)] for _ in range(3)]),
            'L': np.array([[5 for _ in range(3)] for _ in range(3)]),
            'R': np.array([[6 for _ in range(3)] for _ in range(3)])
        }
        self.adjacencies_2 = {
            'U': {'edges': [('F', (2, 1), (0, 1)), ('R', (1, 2), (0, 1)), ('B', (0, 1), (0, 1)), ('L', (1, 0), (0, 1))],
                  'corners': [('F', 'R', (2, 2), (0, 2), (0, 0)), ('R', 'B', (0, 2), (0, 2), (0, 0)),
                              ('B', 'L', (0, 0), (0, 2), (0, 0)), ('L', 'F', (2, 0), (0, 2), (0, 0))]},
            'D': {'edges': [('F', (0, 1), (2, 1)), ('R', (1, 2), (2, 1)), ('B', (2, 1), (2, 1)), ('L', (1, 0), (2, 1))],
                  'corners': [('F', 'R', (0, 2), (2, 2), (2, 0)), ('R', 'B', (2, 2), (2, 2), (2, 0)),
                              ('B', 'L', (2, 0), (2, 2), (2, 0)), ('L', 'F', (0, 0), (2, 2), (2, 0))]},
            'R': {'edges': [('F', (1, 0), (1, 2)), ('U', (0, 2), (1, 2)), ('B', (1, 2), (1, 0)), ('D', (2, 1), (1, 2))],
                  'corners': [('F', 'U', (0, 0), (0, 2), (2, 2)), ('U', 'B', (0, 2), (0, 2), (0, 0)),
                              ('B', 'D', (2, 2), (2, 0), (2, 2)), ('D', 'F', (2, 0), (0, 2), (2, 2))]},
            'L': {'edges': [('F', (1, 2), (1, 0)), ('U', (0, 1), (1, 0)), ('B', (1, 0), (1, 2)), ('D', (2, 1), (1, 0))],
                  'corners': [('F', 'U', (0, 2), (0, 0), (2, 0)), ('U', 'B', (0, 0), (0, 0), (0, 2)),
                              ('B', 'D', (2, 0), (2, 2), (2, 0)), ('D', 'F', (2, 2), (0, 2), (2, 0))]},
            'F': {'edges': [('U', (0, 1), (2, 1)), ('R', (1, 2), (1, 0)), ('D', (2, 1), (0, 1)), ('L', (1, 0), (1, 2))],
                  'corners': [('U', 'R', (0, 2), (2, 2), (0, 0)), ('R', 'D', (2, 2), (2, 0), (0, 2)),
                              ('D', 'L', (2, 0), (0, 0), (2, 2)), ('L', 'U', (0, 0), (0, 2), (2, 0))]},
            'B': {'edges': [('U', (0, 1), (0, 1)), ('R', (1, 0), (1, 2)), ('D', (2, 1), (2, 1)), ('L', (1, 2), (1, 0))],
                  'corners': [('U', 'R', (0, 0), (0, 2), (0, 2)), ('R', 'D', (2, 0), (2, 2), (2, 2)),
                              ('D', 'L', (2, 2), (2, 0), (2, 0)), ('L', 'U', (0, 2), (0, 0), (2, 0))]}
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

    def copy(self):
        new_cube = RubiksCube(self.scramble)
        new_cube.cube = copy.deepcopy(self.cube)
        new_cube.move_history = copy.deepcopy(self.move_history)
        return new_cube
    def update(self, other):
        self.scramble = other.scramble
        self.cube = copy.deepcopy(other.cube)
        self.move_history = copy.deepcopy(other.move_history)

    def rotate_face(self, face):
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
            # Temporarily store the edges
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
            # Temporarily store the edges
            temp_front = np.copy(self.cube['F'][2, :])
            temp_left = np.copy(self.cube['L'][2, :])
            temp_back = np.copy(self.cube['B'][2, :])
            temp_right = np.copy(self.cube['R'][2, :])

            # Rotate the edges
            self.cube['B'][2, :] = temp_right
            self.cube['R'][2, :] = temp_front
            self.cube['F'][2, :] = temp_left
            self.cube['L'][2, :] = temp_back
        elif face == "D'":
            self.cube["D"] = np.rot90(self.cube["D"])
            # Temporarily store the edges
            temp_front = np.copy(self.cube['F'][2, :])
            temp_left = np.copy(self.cube['L'][2, :])
            temp_back = np.copy(self.cube['B'][2, :])
            temp_right = np.copy(self.cube['R'][2, :])

            # Rotate the edges
            self.cube['B'][2, :] = temp_left
            self.cube['R'][2, :] = temp_back
            self.cube['F'][2, :] = temp_right
            self.cube['L'][2, :] = temp_front
        elif face == "D2":
            self.cube["D"] = np.rot90(self.cube["D"], k=2)
            # Temporarily store the edges
            temp_front = np.copy(self.cube['F'][2, :])
            temp_left = np.copy(self.cube['L'][2, :])
            temp_back = np.copy(self.cube['B'][2, :])
            temp_right = np.copy(self.cube['R'][2, :])

            # Rotate the edges
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
            # self.display()
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
            # self.display()
        elif face == "x'":
            # self.display()
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
            # self.display()
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
            # Temporarily store the edges
            temp_top = np.copy(self.cube['U'])
            temp_bottom = np.copy(self.cube['D'])
            temp_left = np.copy(self.cube['L'])
            temp_right = np.copy(self.cube['R'])

            self.cube['U'] = np.rot90(temp_bottom, k=2)
            self.cube['D'] = np.rot90(temp_top, k=2)
            self.cube['L'] = np.rot90(temp_right, k=2)
            self.cube['R'] = np.rot90(temp_left, k=2)

    def make_alg(self, alg_name, alg="", move_count=1):
        permutation = {k: v for (k, v) in enumerate(perms_all)}
        if alg != "":
            moves = alg.split(" ")
            for i in range(len(moves)):
                self.rotate_face(moves[i])
                self.move_history.append(moves[i])
            return
        if alg_name == "Aa":
            alg_str = "x z' R2 U2 R' D' R U2 R' D R' z x'"
            moves = alg_str.split(" ")
            for i in range(len(moves)):
                self.rotate_face(moves[i])
            self.move_history.append(alg_name)
        if alg_name == "random_algs":
            for j in range(int(move_count)):
                random_key = random.choice(list(permutation.keys()))
                random_value = permutation[random_key]
                moves = random_value.split(" ")
                for i in range(len(moves)):
                    self.rotate_face(moves[i])
                # print(str(random_key))
                # print(f"randomkey {random_key}")

                self.move_history.append(str(random_key))
        if alg_name == "random_moves":
            for j in range(int(move_count)):
                random_move = random.choice(list(viable_moves))
                self.rotate_face(random_move)
                self.move_history.append(random_move)
        if alg_name == "random_scramble":
            scramble = "B' D2 L' F' B2 U2 D  F2 R' U' D2 L2 F L2 B F2 R D L D' F2 L2 B' L' R'"
            moves = scramble.split(" ")
            for i in range(len(moves)):
                self.rotate_face(moves[i])
                self.move_history.append(moves[i])
        if alg_name == "scramble":
            moves = self.scramble.split(" ")
            print(moves)
            for i in range(len(moves)):
                self.rotate_face(moves[i])

    def get_score_2(self):
        score = 0
        for face in self.cube:
            center = self.cube[face][1, 1]
            for row in self.cube[face]:
                for cell in row:
                    if cell != center:
                        score += 1
        return score

    def get_score(self):
        score = 0
        for face in self.cube:
            center = self.cube[face][1, 1]
            for row in self.cube[face]:
                for cell in row:
                    if cell != center:
                        score += 1
            adjacent = self.adjacencies[face]
            adjacent_edges = adjacent["edges"]
            adjacent_corners = adjacent["corners"]
            for adjacent_face, edge_coords_1, edge_coords_2 in adjacent_edges:
                if (self.cube[face][edge_coords_1[0]][edge_coords_1[1]] != center or
                        self.cube[adjacent_face][edge_coords_2[0]][edge_coords_2[1]] != self.cube[adjacent_face][1][1]):
                    score += 1
            for adjacent_face_1, adjacent_face_2, edge_coords_1, edge_coords_2, edge_coords_3 in adjacent_corners:
                if (self.cube[face][edge_coords_1[0]][edge_coords_1[1]] != center or
                        self.cube[adjacent_face_1][edge_coords_2[0]][edge_coords_2[1]] !=
                        self.cube[adjacent_face_1][1][1] or
                        self.cube[adjacent_face_2][edge_coords_3[0]][edge_coords_3[1]] !=
                        self.cube[adjacent_face_2][1][1]):
                    score += 1
        return score

    def display(self):
        blank_face = np.full((3, 3), ' ')
        upper = np.hstack((blank_face, self.cube['U'], blank_face, blank_face))
        middle = np.hstack((self.cube['L'], self.cube['F'], self.cube['R'], self.cube['B']))
        lower = np.hstack((blank_face, self.cube['D'], blank_face, blank_face))

        cross = np.vstack((upper, middle, lower))

        for row in cross:
            print(' '.join(str(cell) for cell in row))
        print()
