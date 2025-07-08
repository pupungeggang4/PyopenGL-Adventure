import sys, pygame, glfw, numpy as np
from glfw.GLFW import *
from OpenGL.GL import *

import script.scenetitle as scenetitle
import script.scenegame as scenegame

class Game():
    def __init__(self):
        self.scene = 'title'
        self.state = ''
        self.menu = False

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
        glfwSetWindowCloseCallback(self.window, self.window_close_callback)

        f = open('shader/vertex.glsl')
        self.v_shader_source = f.read()
        f.close()
        f = open('shader/fragment.glsl')
        self.f_shader_source = f.read()
        f.close()
        self.v_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(self.v_shader, self.v_shader_source)
        glCompileShader(self.v_shader)
        self.f_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(self.f_shader, self.f_shader_source)
        glCompileShader(self.f_shader)
        self.program = glCreateProgram()
        glAttachShader(self.program, self.v_shader)
        glAttachShader(self.program, self.f_shader)
        glLinkProgram(self.program)

        if not glGetShaderiv(self.v_shader, GL_COMPILE_STATUS):
            print(glGetShaderInfoLog(self.v_shader))
        if not glGetShaderiv(self.f_shader, GL_COMPILE_STATUS):
            print(glGetShaderInfoLog(self.f_shader))

        self.location = {}
        self.location['a_position'] = glGetAttribLocation(self.program, 'a_position')
        self.location['a_texcoord'] = glGetAttribLocation(self.program, 'a_texcoord')
        self.location['u_mode_v'] = glGetUniformLocation(self.program, 'u_mode_v')
        self.location['u_mode_f'] = glGetUniformLocation(self.program, 'u_mode_f')
        self.location['u_color'] = glGetUniformLocation(self.program, 'u_color')
        self.texture = 1

        glGenTextures(1, self.texture)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)

        self.vao = 1; glGenVertexArrays(1, self.vao)
        self.b_hud = 1; glGenBuffers(1, self.b_hud)
        self.b_hud_index = 2; glGenBuffers(1, self.b_hud_index)
        self.b_cuboid = 3; glGenBuffers(1, self.b_cuboid)
        self.b_cuboid_index = 4; glGenBuffers(1, self.b_cuboid_index)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.b_hud)
        glBufferData(GL_ARRAY_BUFFER, np.array([
            -1.0, -1.0, 0.0, 0.0,
            -1.0, 1.0, 0.0, 1.0,
            1.0, 1.0, 1.0, 1.0,
            1.0, -1.0, 1.0, 0.0
        ], dtype = np.float32), GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.b_hud_index)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, np.array([
            1, 2, 0, 0, 2, 3
        ], dtype = np.int16), GL_STATIC_DRAW)

        glViewport(0, 0, 1280, 720)

    def key_callback(self, window, key, scancode, action, mods):
        pass

    def window_close_callback(self, window):
        glfwSetWindowShouldClose(self.window, GLFW_TRUE)

    def run(self):
        while not glfwWindowShouldClose(self.window):
            self.clock.tick(self.fps)
            self.handle_scene()
            glfw.poll_events()

    def handle_scene(self):
        if self.scene == 'title':
            scenetitle.loop(self)

if __name__ == '__main__':
    Game().run()
