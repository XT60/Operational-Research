import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from src.RubiksCube import RubiksCube


last_mouse_pos = (0, 0)
scene_rotation = [0, 0]  # Rotation around X and Y axes
mouse_pressed = False  # Track whether the mouse button is pressed
cube = RubiksCube()
scene_scale = 1.0


def draw_cube_face(face, face_name):
    # Default positions, can be overridden as needed
    x, y, z = 0, 0, 0  # Initialize x, y, z to default values

    # Check the face and adjust positions
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

    # Apply rotation for U and D faces
    glPushMatrix()
    if face_name == 'D':
        glTranslatef(x, y, z)  # Move to the face center
        glRotatef(90, 1, 0, 0)  # Rotate around the X-axis
        glTranslatef(-x, -y, -z)  # Move back
    elif face_name == 'U':
        glTranslatef(x, y, z)  # Move to the face center
        glRotatef(-90, 1, 0, 0)  # Rotate around the X-axis
        glTranslatef(-x, -y, -z)
    elif face_name == 'R':
        glTranslatef(x, y, z)  # Move to the face center
        glRotatef(90, 0, 1, 0)  # Rotate around the X-axis
        glTranslatef(-x, -y, -z)  # Move back
    elif face_name == 'L':
        glTranslatef(x, y, z)  # Move to the face center
        glRotatef(-90, 0, 1, 0)  # Rotate around the X-axis
        glTranslatef(-x, -y, -z)
    elif face_name == 'B':
        glTranslatef(x, y, z)  # Move to the face center
        glRotatef(180, 0, 1, 0)  # Rotate around the X-axis
        glTranslatef(-x, -y, -z)

    glBegin(GL_QUADS)
    for i, row in enumerate(face):
        for j, color in enumerate(row):
            # Set color based on the color code
            if color == 1:
                glColor3f(0, 1, 0)  # Green
            elif color == 2:
                glColor3f(0, 0, 1)  # Blue
            elif color == 3:
                glColor3f(1, 1, 1)  # White
            elif color == 4:
                glColor3f(1, 1, 0)  # Yellow
            elif color == 5:
                glColor3f(1, 0.5, 0)  # Orange
            elif color == 6:
                glColor3f(1, 0, 0)  # Red

            # Define vertices for a square in the correct position
            vertices = [
                (x + j * 1 / 3, y - i * 1 / 3, z),
                (x + (j + 1) * 1 / 3, y - i * 1 / 3, z),
                (x + (j + 1) * 1 / 3, y - (i + 1) * 1 / 3, z),
                (x + j * 1 / 3, y - (i + 1) * 1 / 3, z),
            ]

            for vertex in vertices:
                glVertex3fv(vertex)
    glEnd()

    # Restore the original matrix for U and D faces after drawing

    glPopMatrix()


def mouse_button_callback(window, button, action, mods):
    global mouse_pressed
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            mouse_pressed = True
        elif action == glfw.RELEASE:
            mouse_pressed = False


def scroll_callback(window, xoffset, yoffset):
    global scene_scale
    # Adjust the scale factor based on scroll direction
    # Increase or decrease the scale factor to zoom in or out
    scene_scale += yoffset * 0.1
    scene_scale = max(0.1, scene_scale)


def mouse_callback(window, xpos, ypos):
    global last_mouse_pos, scene_rotation

    if not mouse_pressed:
        # Update the last_mouse_pos but do not rotate the scene
        last_mouse_pos = (xpos, ypos)
        return

    # Calculate mouse movement
    x_diff, y_diff = xpos - last_mouse_pos[0], ypos - last_mouse_pos[1]
    last_mouse_pos = (xpos, ypos)

    # Update scene rotation based on mouse movement
    sensitivity = 0.2
    scene_rotation[0] += y_diff * sensitivity
    scene_rotation[1] += x_diff * sensitivity


def key_callback(window, key, scancode, action, mods):
    if key == glfw.KEY_F and action == glfw.PRESS:
        if mods & glfw.MOD_SHIFT:
            cube.rotate_face("F'")
            print("Rotated face F'")
        elif mods & glfw.MOD_CONTROL:
            cube.rotate_face("F2")
            print("Rotated face F2")
        else:
            cube.rotate_face('F')
            print("Rotated face F")
    elif key == glfw.KEY_B and action == glfw.PRESS:
        if mods & glfw.MOD_SHIFT:
            cube.rotate_face("B'")
            print("Rotated face B'")
        elif mods & glfw.MOD_CONTROL:
            cube.rotate_face("B2")
            print("Rotated face B2")
        else:
            cube.rotate_face('B')
            print("Rotated face B")
    elif key == glfw.KEY_U and action == glfw.PRESS:
        if mods & glfw.MOD_SHIFT:
            cube.rotate_face("U'")
            print("Rotated face U'")
        elif mods & glfw.MOD_CONTROL:
            cube.rotate_face("U2")
            print("Rotated face U2")
        else:
            cube.rotate_face('U')
            print("Rotated face U")
    elif key == glfw.KEY_D and action == glfw.PRESS:
        if mods & glfw.MOD_SHIFT:
            cube.rotate_face("D'")
            print("Rotated face D'")
        elif mods & glfw.MOD_CONTROL:
            cube.rotate_face("D2")
            print("Rotated face D2")
        else:
            cube.rotate_face('D')
            print("Rotated face D")
    elif key == glfw.KEY_R and action == glfw.PRESS:
        if mods & glfw.MOD_SHIFT:
            cube.rotate_face("R'")
            print("Rotated face R'")
        elif mods & glfw.MOD_CONTROL:
            cube.rotate_face("R2")
            print("Rotated face R2")
        else:
            cube.rotate_face('R')
            print("Rotated face R")
    elif key == glfw.KEY_L and action == glfw.PRESS:
        if mods & glfw.MOD_SHIFT:
            cube.rotate_face("L'")
            print("Rotated face L'")
        elif mods & glfw.MOD_CONTROL:
            cube.rotate_face("L2")
            print("Rotated face L2")
        else:
            cube.rotate_face('L')
            print("Rotated face L")
    elif key == glfw.KEY_X and action == glfw.PRESS:
        if mods & glfw.MOD_SHIFT:
            cube.rotate_face("x'")
            print("Rotated face x'")
        elif mods & glfw.MOD_CONTROL:
            cube.rotate_face("x2")
            print("Rotated face x2")
        else:
            cube.rotate_face('x')
            print("Rotated face x")
    elif key == glfw.KEY_Y and action == glfw.PRESS:
        if mods & glfw.MOD_SHIFT:
            cube.rotate_face("y'")
            print("Rotated face y'")
        elif mods & glfw.MOD_CONTROL:
            cube.rotate_face("y2")
            print("Rotated face y2")
        else:
            cube.rotate_face('y')
            print("Rotated face y")
    elif key == glfw.KEY_Z and action == glfw.PRESS:
        if mods & glfw.MOD_SHIFT:
            cube.rotate_face("z'")
            print("Rotated face z'")
        elif mods & glfw.MOD_CONTROL:
            cube.rotate_face("z2")
            print("Rotated face z2")
        else:
            cube.rotate_face('z')
            print("Rotated face z")


def main():
    if not glfw.init():
        return

    window = glfw.create_window(640, 480, "Rubik's Cube", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, 640 / 480, 0.1, 50.0)

    # Set the mouse callbacks
    glfw.set_cursor_pos_callback(window, mouse_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_scroll_callback(window, scroll_callback)

    # Make sure you have your RubiksCube.py class defined
    i = 1
    current_move_index = 0
    temp_alg = "F L F U' R U F2 L2 U' L' B D' B' L2 U"
    temp_alg = "U' F2 R' L' U' B R2 D B U' R2 L B2 D' B2 U F2 B2 U' L2 B2 L2"
    moves = temp_alg.split(" ")
    # moves = []
    while not glfw.window_should_close(window):
        if i % 100 == 0 and current_move_index < len(moves):
            cube.rotate_face(moves[current_move_index])
            current_move_index += 1
        i += 1
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(2, 1, 3, 0, 0, 0, 0, 1, 0)

        # Apply scene rotation
        glRotatef(scene_rotation[0], 1, 0, 0)  # Rotation around X-axis
        glRotatef(scene_rotation[1], 0, 1, 0)  # Rotation around Y-axis
        glScalef(scene_scale, scene_scale, scene_scale)

        draw_cube_face(cube.cube['U'], 'U')
        draw_cube_face(cube.cube['L'], 'L')
        draw_cube_face(cube.cube['F'], 'F')
        draw_cube_face(cube.cube['R'], 'R')
        draw_cube_face(cube.cube['B'], 'B')
        draw_cube_face(cube.cube['D'], 'D')

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
