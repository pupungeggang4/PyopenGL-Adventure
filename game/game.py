import sys, numpy, pygame, glfw
from OpenGL.GL import *

class Game():
    def __init__(self):
        self.gl_init()
        pygame.init()
        self.surface_ui = pygame.surface.Surface((1280, 720), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.fps = 60

    def gl_init(self):
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        self.window = glfwCreateWindow(1280, 720, 'OpenGL Adventure', None, None)
        self.context = glfw.make_context_current(self.window)
        glfwSetKeyCallback(self.window, self.key_callback)

    def key_callback(self, window, key, scancode, action, mods):
        pass

    def run():
        while True:
            self.clock.tick(self.fps)

if __name__ == '__main__':
    Game().run()
