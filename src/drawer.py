import random

import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

from .permutation_table import translate_moves, viable_moves
from .rubikscube import RubiksCube
from .solver import BeesAlgorithm
import threading


class Drawer:
    def __init__(self, cube=None):
        self.last_mouse_pos = (0, 0)
        self.scene_rotation = [0, 0]
        self.mouse_pressed = False
        if cube:
            self.cube = cube
        else:
            self.cube = RubiksCube()
        self.scene_scale = 1.0
        self.solution = []
        self.delay_solving = 500
        self.delay_between_moves = 10

    def set_delays(self, delay_solving, delay_between_moves):
        self.delay_solving = delay_solving
        self.delay_between_moves = delay_between_moves

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
        glEnable(GL_NORMALIZE)
        glEnable(GL_COLOR_MATERIAL)
        light_position = [1, 3, 3, 0]
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

    def update_cube(self, solution, new_cube):
        self.solution = solution
        self.cube.update(new_cube)

    def run(self, stop_event):
        """
        Drives the graphical representation of the Rubik's Cube solving process using OpenGL, rendering the cube's state continuously and applying moves sequentially.

        This method initializes a window using OpenGL and continually renders the Rubik's Cube's state until the window is closed or the solving process is complete. It displays the initial scramble and handles the application of each move in the solution sequence with a delay to visualize the solving process step by step.

        Args:
            stop_event (threading.Event): An event used to signal the termination of the thread running this method, ensuring proper shutdown and resource release.

        Workflow:
            1. Initialize the OpenGL window and print the scramble.
            2. Continuously render the cube's state in the window while it remains open.
            3. Sequentially apply moves from the solution list to the cube with a fixed delay between moves, allowing visualization of each step.
            4. If the cube is solved and the solution is non-empty, reset and re-scramble the cube after showing the full solution to restart the solving visualization.
            5. Terminate the OpenGL context and set the stop event upon closing the window to signal that the rendering thread has finished.

        This method effectively simulates a real-time solving environment for a Rubik's Cube, making it useful for demonstrations or interactive visualizations where users can watch the cube being solved in a controlled graphical setting.
        """
        window = self.init_gl()
        print(
            f"________________________________________________\nSolving a Rubik's Cube scrambled with"
            f" \n\n{self.cube.get_scramble()}\n\n________________________________________________\n\n\n")

        i = 0
        j = -self.delay_solving
        current_move_index = 0

        while not glfw.window_should_close(window):
            if self.cube.solved:
                if len(self.solution) > 0:
                    if j == 0:
                        self.cube.reset_state()
                        self.cube.make_alg("scramble")
                    if j > 500:
                        i += 1
                        if i % self.delay_between_moves == 0:
                            self.cube.rotate_face(self.solution[current_move_index])
                            current_move_index += 1
                        if current_move_index >= len(self.solution):
                            i = 0
                            j = -self.delay_solving
                            current_move_index = 0
                    j += 1
            self.draw_cube(self.cube)
            glfw.swap_buffers(window)
            glfw.poll_events()
        glfw.terminate()
        stop_event.set()
