from script.module import *

def loop(game):
    render(game)

def render(game):
    glClearColor(0.0, 1.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glfw.swap_buffers(game.window)