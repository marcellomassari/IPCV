import pywavefront
from pyglet.gl import *
from pywavefront import visualization
import ctypes
import os

window = pyglet.window.Window(width=1280, height=720, resizable=True)

image = pyglet.resource.image("images/stanza_prova.jpeg")

root_path = os.path.dirname(__file__)
obj = pywavefront.Wavefront(os.path.join(root_path, 'models/cube_prova.obj'))

lightfv = ctypes.c_float * 4

@window.event
def on_resize(width, height):
    viewport_width, viewport_height = window.get_viewport_size()
    glViewport(0, 0, viewport_width, viewport_height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45., float(width)/height, 1., 100.)
    glMatrixMode(GL_MODELVIEW)
    return True

@window.event
def on_draw():

    # enable 3d
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)  # enable depth testing
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    draw_box(obj, 0.0, 0.0)

    #enable 2d
    glDisable(GL_DEPTH_TEST)
    # store the projection matrix to restore later
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    # load orthographic projection matrix
    glLoadIdentity()
    glOrtho(0, float(window.width),0, float(window.height), 0, 1)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    image.blit(0.0, 0.0, -1.0)

    # disable 2d
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()


def draw_box(box, x, y):
    glTranslated(x, y, -5.0)
    visualization.draw(box)

pyglet.app.run()

# comment