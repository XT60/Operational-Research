import random

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

from .permutation_table import translate_moves, viable_moves
from .rubikscube import RubiksCube
from .solver import BeesAlgorithm
import threading


class Drawer:
    def __init__(self):
        self.last_mouse_pos = (0, 0)
        self.scene_rotation = [0, 0]
        self.mouse_pressed = False
        self.cube = RubiksCube()
        self.scene_scale = 1.0
        self.solution = []

    def draw_cube_face(self, face, face_name):
        x, y, z = 0, 0, 0
        if face_name == 'F':
            z = 0.5
        elif face_name == 'B':
            x, z = 1, -0.5
        elif face_name == 'L':
            x, z = 0, -0.5
        elif face_name == 'R':
            x, z = 1, 0.5
        elif face_name == 'U':
            y, z = 0, -0.5
        elif face_name == 'D':
            y, z = -1, 0.5
        x -= 0.5
        y += 0.5

        glPushMatrix()
        if face_name == 'D':
            glTranslatef(x, y, z)
            glRotatef(90, 1, 0, 0)
            glTranslatef(-x, -y, -z)
        elif face_name == 'U':
            glTranslatef(x, y, z)
            glRotatef(-90, 1, 0, 0)
            glTranslatef(-x, -y, -z)
        elif face_name == 'R':
            glTranslatef(x, y, z)
            glRotatef(90, 0, 1, 0)
            glTranslatef(-x, -y, -z)
        elif face_name == 'L':
            glTranslatef(x, y, z)
            glRotatef(-90, 0, 1, 0)
            glTranslatef(-x, -y, -z)
        elif face_name == 'B':
            glTranslatef(x, y, z)
            glRotatef(180, 0, 1, 0)
            glTranslatef(-x, -y, -z)

        glBegin(GL_QUADS)
        specular = [1.0, 1.0, 1.0, 1.0]
        shininess = [50.0]
        glMaterialfv(GL_FRONT, GL_SPECULAR, specular)
        glMaterialfv(GL_FRONT, GL_SHININESS, shininess)
        for i, row in enumerate(face):
            for j, color in enumerate(row):

                if color == 1:
                    glColor3f(0, 1, 0)
                elif color == 2:
                    glColor3f(0, 0, 1)
                elif color == 3:
                    glColor3f(1, 1, 1)
                elif color == 4:
                    glColor3f(1, 1, 0)
                elif color == 5:
                    glColor3f(1, 0.5, 0)
                elif color == 6:
                    glColor3f(1, 0, 0)
                glNormal3f(0, 0, 1)
                vertices = [
                    (x + j * 1 / 3, y - i * 1 / 3, z),
                    (x + (j + 1) * 1 / 3, y - i * 1 / 3, z),
                    (x + (j + 1) * 1 / 3, y - (i + 1) * 1 / 3, z),
                    (x + j * 1 / 3, y - (i + 1) * 1 / 3, z),
                ]

                for vertex in vertices:
                    glVertex3fv(vertex)
        glEnd()

        glPopMatrix()

    def mouse_button_callback(self, window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT:
            if action == glfw.PRESS:
                self.mouse_pressed = True
            elif action == glfw.RELEASE:
                self.mouse_pressed = False

    def scroll_callback(self, window, xoffset, yoffset):
        self.scene_scale += yoffset * 0.1
        self.scene_scale = max(0.1, self.scene_scale)

    def mouse_callback(self, window, xpos, ypos):
        if not self.mouse_pressed:
            self.last_mouse_pos = (xpos, ypos)
            return

        x_diff, y_diff = xpos - self.last_mouse_pos[0], ypos - self.last_mouse_pos[1]
        self.last_mouse_pos = (xpos, ypos)

        sensitivity = 0.2
        self.scene_rotation[0] += y_diff * sensitivity
        self.scene_rotation[1] += x_diff * sensitivity

    def key_callback(self, window, key, scancode, action, mods):
        if key == glfw.KEY_F and action == glfw.PRESS:
            if mods & glfw.MOD_SHIFT:
                self.cube.rotate_face("F'")
            elif mods & glfw.MOD_CONTROL:
                self.cube.rotate_face("F2")
            else:
                self.cube.rotate_face('F')
        elif key == glfw.KEY_B and action == glfw.PRESS:
            if mods & glfw.MOD_SHIFT:
                self.cube.rotate_face("B'")
            elif mods & glfw.MOD_CONTROL:
                self.cube.rotate_face("B2")
            else:
                self.cube.rotate_face('B')
        elif key == glfw.KEY_U and action == glfw.PRESS:
            if mods & glfw.MOD_SHIFT:
                self.cube.rotate_face("U'")
            elif mods & glfw.MOD_CONTROL:
                self.cube.rotate_face("U2")
            else:
                self.cube.rotate_face('U')
        elif key == glfw.KEY_D and action == glfw.PRESS:
            if mods & glfw.MOD_SHIFT:
                self.cube.rotate_face("D'")
            elif mods & glfw.MOD_CONTROL:
                self.cube.rotate_face("D2")
            else:
                self.cube.rotate_face('D')
        elif key == glfw.KEY_R and action == glfw.PRESS:
            if mods & glfw.MOD_SHIFT:
                self.cube.rotate_face("R'")
            elif mods & glfw.MOD_CONTROL:
                self.cube.rotate_face("R2")
            else:
                self.cube.rotate_face('R')
        elif key == glfw.KEY_L and action == glfw.PRESS:
            if mods & glfw.MOD_SHIFT:
                self.cube.rotate_face("L'")
            elif mods & glfw.MOD_CONTROL:
                self.cube.rotate_face("L2")
            else:
                self.cube.rotate_face('L')
        elif key == glfw.KEY_X and action == glfw.PRESS:
            if mods & glfw.MOD_SHIFT:
                self.cube.rotate_face("x'")
            elif mods & glfw.MOD_CONTROL:
                self.cube.rotate_face("x2")
            else:
                self.cube.rotate_face('x')
        elif key == glfw.KEY_Y and action == glfw.PRESS:
            if mods & glfw.MOD_SHIFT:
                self.cube.rotate_face("y'")
            elif mods & glfw.MOD_CONTROL:
                self.cube.rotate_face("y2")
            else:
                self.cube.rotate_face('y')
        elif key == glfw.KEY_Z and action == glfw.PRESS:
            if mods & glfw.MOD_SHIFT:
                self.cube.rotate_face("z'")
            elif mods & glfw.MOD_CONTROL:
                self.cube.rotate_face("z2")
            else:
                self.cube.rotate_face('z')
        elif key == glfw.KEY_M and action == glfw.PRESS:
            if mods & glfw.MOD_SHIFT:
                self.cube.rotate_face("M'")
            elif mods & glfw.MOD_CONTROL:
                self.cube.rotate_face("M2")
            else:
                self.cube.rotate_face('M')
        elif key == glfw.KEY_E and action == glfw.PRESS:
            if mods & glfw.MOD_SHIFT:
                self.cube.rotate_face("E'")
            elif mods & glfw.MOD_CONTROL:
                self.cube.rotate_face("E2")
            else:
                self.cube.rotate_face('E')
        elif key == glfw.KEY_S and action == glfw.PRESS:
            if mods & glfw.MOD_SHIFT:
                self.cube.rotate_face("S'")
            elif mods & glfw.MOD_CONTROL:
                self.cube.rotate_face("S2")
            else:
                self.cube.rotate_face('S')

    def draw_cube(self, cube):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(2, 1, 3, 0, 0, 0, 0, 1, 0)
        glPushMatrix()
        glRotatef(self.scene_rotation[0], 1, 0, 0)
        glRotatef(self.scene_rotation[1], 0, 1, 0)
        glScalef(self.scene_scale, self.scene_scale, self.scene_scale)
        for face_name, face in cube.cube.items():
            self.draw_cube_face(face, face_name)
        glPopMatrix()

    def window_resize_callback(self, window, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect_ratio = width / float(height) if height else 1.0
        gluPerspective(45, aspect_ratio, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def run_solver(self, solver, i, solved_cube, lock, stop_event, solution):
        print(f"________________________\nIteration: {0}")
        print(
            f"\nScore: {solved_cube.get_score()[0]}\nScore_corners: {solved_cube.get_score()[2]}\nScore_edges: {solved_cube.get_score()[1]}\n________________________\n\n")
        is_solved = False
        while not stop_event.is_set() and not is_solved:
            if i != 0:
                print(f"________________________\nIteration: {i}")
            is_solved, new_cube, solution = solver.solve(i)
            new_cube = new_cube.copy()
            with lock:
                self.solution = solution
                solved_cube.update(new_cube)
            print(
                f"\nScore: {solved_cube.get_score()[0]}\nScore_corners: {solved_cube.get_score()[2]}\nScore_edges: {solved_cube.get_score()[1]}\n________________________\n\n")
            if len(solution) == 1 and solution[0] == "Above Limit":
                break
            i += 1
        a = " ".join(translate_moves(self.cube.move_history))
        if is_solved:
            print(
                f"\n\n\n________________________________________________\n\nSolved the Rubik's Cube!\n\nFound Solution:\n\n{a}\n\n________________________________________________\n\n")
        else:
            self.solution = []
            print("Above Limit, Aborting")

    def init_gl(self):
        if not glfw.init():
            return
        glfw.window_hint(glfw.SAMPLES, 4)

        window = glfw.create_window(640, 480, "Rubik's Cube", None, None)
        if not window:
            glfw.terminate()
            return

        glfw.make_context_current(window)
        glfw.set_window_size_callback(window, self.window_resize_callback)

        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        glEnable(GL_COLOR_MATERIAL)
        light_position = [0, 1, 2, 0]
        glLightfv(GL_LIGHT0, GL_POSITION, light_position)

        ambient_light = [0.2, 0.2, 0.2, 1.0]
        diffuse_light = [0.7, 0.7, 0.7, 1.0]
        specular_light = [0.9, 0.9, 0.9, 1.0]
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)

        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        glDepthFunc(GL_LESS)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, 640 / 480, 0.1, 50.0)

        glfw.set_cursor_pos_callback(window, self.mouse_callback)
        glfw.set_mouse_button_callback(window, self.mouse_button_callback)
        glfw.set_key_callback(window, self.key_callback)
        glfw.set_scroll_callback(window, self.scroll_callback)
        return window

    def run(self):
        window = self.init_gl()

        # self.cube = RubiksCube("B' D2 L' F' B2 U2 D F2 R' U' D2 L2 F L2 B F2 R D L D' F2 L2 B' L' R'")
        self.cube = RubiksCube(" ".join(random.choices(viable_moves, k=50)))

        print(
            f"________________________________________________\nSolving a Rubik's Cube scrambled with \n\n{self.cube.get_scramble()}\n\n________________________________________________\n\n\n")

        solver = BeesAlgorithm(self.cube, 50, 50, 50, 50)

        lock = threading.Lock()
        stop_event = threading.Event()
        solver_thread = threading.Thread(target=self.run_solver,
                                         args=(solver, 1, self.cube, lock, stop_event, self.solution))
        solver_thread.start()

        i = 0
        j = -500
        current_move_index = 0
        delay_solving = 10
        while not glfw.window_should_close(window):
            if len(self.solution) > 0:
                if j == 0:
                    self.cube.reset_state()
                    self.cube.make_alg("scramble")
                if j > 500:
                    i += 1
                    if i % delay_solving == 0:
                        self.cube.rotate_face(self.solution[current_move_index])
                        current_move_index += 1
                    if current_move_index >= len(self.solution):
                        i = 0
                        j = -500
                        current_move_index = 0
                j += 1
            with lock:
                current_cube = self.cube.copy()
            self.draw_cube(current_cube)
            glfw.swap_buffers(window)
            glfw.poll_events()
        glfw.terminate()
        stop_event.set()
