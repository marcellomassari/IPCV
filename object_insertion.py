import pywavefront
from pyglet.gl import *
from pywavefront import visualization
import ctypes
import os
import cv2
import numpy as np

window = pyglet.window.Window(width=1280, height=720, resizable=True)

image = pyglet.resource.image("images/stanza_prova.jpeg")

root_path = os.path.dirname(__file__)
obj = pywavefront.Wavefront(os.path.join(root_path, 'models/cube_prova.obj'))

lightfv = ctypes.c_float * 4
rotation = 0.0

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
    window.clear()

    width, height = image.width, image.height
    image.anchor_x = width / 2
    image.anchor_y = height / 2

    image.blit(image.anchor_x, image.anchor_y)

    glLoadIdentity()

    #glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-1.0, 1.0, 1.0, 0.0))

    draw_box(obj, 0.0, 0.0)


def draw_box(box, x, y):
    glLoadIdentity()
    glTranslated(x, y, -10.0)

    visualization.draw(box)

def update(dt):
    global rotation
    rotation += 90.0 * dt

    if rotation > 720.0:
        rotation = 0.0

pyglet.clock.schedule(update)
pyglet.app.run()