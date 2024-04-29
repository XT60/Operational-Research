import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
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

    def window_resize_callback(self, window, width, height):
        # Update the viewport to match the new window dimensions
        glViewport(0, 0, width, height)
        # Update the projection matrix
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        # Adjust the perspective to maintain aspect ratio
        aspect_ratio = width / float(height) if height else 1.0
        gluPerspective(45, aspect_ratio, 0.1, 50.0)
        glMatrixMode(GL_MODELVIEW)

    def run_solver(self, solver, i, solved_cube, lock, stop_event):
        print(f"Score: {solved_cube.get_score()}")
        is_solved = False
        while not stop_event.is_set() and not is_solved:

            is_solved, new_cube = solver.solve(i)
            new_cube = new_cube.copy()
            with lock:
                solved_cube.update(new_cube)
            print(f"Score: {solved_cube.get_score()} {solved_cube.move_history}")

            i += 1
    def run(self):
        if not glfw.init():
            return

        window = glfw.create_window(640, 480, "Rubik's Cube", None, None)
        if not window:
            glfw.terminate()
            return

        glfw.make_context_current(window)
        glfw.set_window_size_callback(window, self.window_resize_callback)

        glEnable(GL_DEPTH_TEST)
        glMatrixMode(GL_PROJECTION)
        gluPerspective(45, 640 / 480, 0.1, 50.0)

        glfw.set_cursor_pos_callback(window, self.mouse_callback)
        glfw.set_mouse_button_callback(window, self.mouse_button_callback)
        glfw.set_key_callback(window, self.key_callback)
        glfw.set_scroll_callback(window, self.scroll_callback)

        i = 1
        current_move_index = 0
        temp_alg = "F L F U' R U F2 L2 U' L' B D' B' L2 U"
        temp_alg = "U' F2 R' L' U' B R2 D B U' R2 L B2 D' B2 U F2 B2 U' L2 B2 L2"
        moves = temp_alg.split(" ")
        moves = []
        solved_cube = RubiksCube("B' D2 L' F' B2 U2 D F2 R' U' D2 L2 F L2 B F2 R D L D' F2 L2 B' L' R'")
        # solved_cube.make_alg("scramble")
        lock = threading.Lock()
        stop_event = threading.Event()
        solver = BeesAlgorithm(solved_cube, 200, 200, 200, 200)
        solver_thread = threading.Thread(target=self.run_solver, args=(solver, 0, solved_cube, lock, stop_event))
        solver_thread.start()
        while not glfw.window_should_close(window):


            # if i % 100 == 0 and (current_move_index < len(moves) or 1):
            #     # self.cube.rotate_face(moves[current_move_index])
            #     # current_move_index += 1
            #     self.cube.make_alg("random_scramble")
            # if i % 10 == 0 and (current_move_index < len(moves) or 1):
            #     # self.cube.rotate_face(moves[current_move_index])
            #     # current_move_index += 1
            #     solved_cube = solver.solve(i//10).copy()
            #     print(solved_cube.get_score())
            # i += 1
            with lock:
                current_cube = solved_cube.copy()
            # self.cube.make_alg("Aa")

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glMatrixMode(GL_MODELVIEW)
            glLoadIdentity()
            gluLookAt(2, 1, 3, 0, 0, 0, 0, 1, 0)
            # print(self.cube.get_score())

            glRotatef(self.scene_rotation[0], 1, 0, 0)
            glRotatef(self.scene_rotation[1], 0, 1, 0)
            glScalef(self.scene_scale, self.scene_scale, self.scene_scale)

            self.draw_cube_face(current_cube.cube['U'], 'U')
            self.draw_cube_face(current_cube.cube['L'], 'L')
            self.draw_cube_face(current_cube.cube['F'], 'F')
            self.draw_cube_face(current_cube.cube['R'], 'R')
            self.draw_cube_face(current_cube.cube['B'], 'B')
            self.draw_cube_face(current_cube.cube['D'], 'D')

            glfw.swap_buffers(window)
            glfw.poll_events()

        glfw.terminate()
