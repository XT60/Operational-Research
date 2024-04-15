import numpy as np


class RubiksCube:
    def __init__(self):
        self.cube = {
            'F': np.array([[1 for _ in range(3)] for _ in range(3)]),
            'B': np.array([[2 for _ in range(3)] for _ in range(3)]),
            'U': np.array([[3 for _ in range(3)] for _ in range(3)]),
            'D': np.array([[4 for _ in range(3)] for _ in range(3)]),
            'L': np.array([[5 for _ in range(3)] for _ in range(3)]),
            'R': np.array([[6 for _ in range(3)] for _ in range(3)])
        }

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
            self.display()
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
            self.display()
        elif face == "x'":
            self.display()
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
            self.display()
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

    def get_score(self):
        score = 0
        for face in self.cube:
            center = self.cube[face][1, 1]
            for row in self.cube[face]:
                for cell in row:
                    if cell != center:
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
