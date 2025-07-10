from script.module import *

import script.scenetitle as scenetitle
import script.scenegame as scenegame

class Game():
    def __init__(self):
        self.key_mapping = {
            'f': GLFW_KEY_W, 'l': GLFW_KEY_A, 'b': GLFW_KEY_S, 'r': GLFW_KEY_D,
            'c_u': GLFW_KEY_UP, 'c_l': GLFW_KEY_LEFT, 'c_d': GLFW_KEY_D, 'c_r': GLFW_KEY_R
        }
        self.key_pressed = {
            'f': False, 'l': False, 'b': False, 'r': False,
            'c_u': False, 'c_l': False, 'c_d': False, 'c_r': False
        }

        self.scene = 'title'
        self.state = ''
        self.menu = False

        self.gl_init()
        pygame.init()
        self.load_font()
        
        self.surface_hud = pygame.surface.Surface((1280, 720), pygame.SRCALPHA)
        self.clock = pygame.time.Clock()
        self.fps = 60

    def gl_init(self):
        glfw.init()
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
        glfw.window_hint(GLFW_SCALE_TO_MONITOR, True)
        glfw.window_hint(GLFW_POSITION_X, 100)
        glfw.window_hint(GLFW_POSITION_Y, 100)
        self.window = glfwCreateWindow(1280, 720, 'OpenGL Adventure', None, None)
        self.monitor = glfwGetPrimaryMonitor()
        self.context = glfw.make_context_current(self.window)
        glfwSetKeyCallback(self.window, self.key_callback)
        glfwSetMouseButtonCallback(self.window, self.mouse_button_callback)
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
            print('v', glGetShaderInfoLog(self.v_shader))
        if not glGetShaderiv(self.f_shader, GL_COMPILE_STATUS):
            print('f', glGetShaderInfoLog(self.f_shader))

        self.location = {}
        self.location['u_mode_v'] = glGetUniformLocation(self.program, 'u_mode_v')
        self.location['u_mode_f'] = glGetUniformLocation(self.program, 'u_mode_f')
        self.location['u_color'] = glGetUniformLocation(self.program, 'u_color')
        self.location['u_model_pos'] = glGetUniformLocation(self.program, 'u_model_pos')
        self.location['u_model_scale'] = glGetUniformLocation(self.program, 'u_model_scale')
        self.location['u_cam_rot'] = glGetUniformLocation(self.program, 'u_cam_rot')
        self.location['u_cam_pos'] = glGetUniformLocation(self.program, 'u_cam_pos')
        self.location['a_position'] = glGetAttribLocation(self.program, 'a_position')
        self.location['a_position_hud'] = glGetAttribLocation(self.program, 'a_position_hud')
        self.location['a_texcoord'] = glGetAttribLocation(self.program, 'a_texcoord')
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
            -1.0, -1.0, 0.0, 1.0,
            -1.0, 1.0, 0.0, 0.0,
            1.0, 1.0, 1.0, 0.0,
            1.0, -1.0, 1.0, 1.0
        ], dtype = np.float32), GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.b_hud_index)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, np.array([
            1, 2, 0, 0, 2, 3
        ], dtype = np.int16), GL_STATIC_DRAW)
        glVertexAttribPointer(self.location['a_position_hud'], 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0 * 4))
        glEnableVertexAttribArray(self.location['a_position_hud'])
        glVertexAttribPointer(self.location['a_texcoord'], 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(2 * 4))
        glEnableVertexAttribArray(self.location['a_texcoord'])
        glBindBuffer(GL_ARRAY_BUFFER, self.b_cuboid)
        glBufferData(GL_ARRAY_BUFFER, np.array([
            -0.5, -0.5, -0.5,
            -0.5, 0.5, -0.5,
            0.5, 0.5, -0.5,
            0.5, -0.5, -0.5,
            -0.5, -0.5, 0.5,
            -0.5, 0.5, 0.5,
            0.5, 0.5, 0.5,
            0.5, -0.5, 0.5
        ], dtype = np.float32), GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.b_cuboid_index)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, np.array([
            0, 1, 4, 4, 1, 5,
            6, 2, 7, 7, 2, 3,
            5, 6, 4, 4, 6, 7,
            3, 2, 0, 0, 2, 1,
            1, 2, 5, 5, 2, 6,
            4, 7, 0, 0, 7, 3
        ], dtype = np.int16), GL_STATIC_DRAW)
        glVertexAttribPointer(self.location['a_position'], 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0 * 4))
        glEnableVertexAttribArray(self.location['a_position'])

        self.scale = glfwGetMonitorContentScale(self.monitor)
        if sys.platform == 'darwin':
            width = int(1280 * self.scale[0])
            height = int(720 * self.scale[1])
        else:
            width, height = 1280, 720
        glViewport(0, 0, width, height)

        self.cuboid1 = Cuboid3(0.2, 0.2, 1.5, 0.1, 0.1, 0.1)
        self.cuboid2 = Cuboid3(0.2, -0.2, 1.5, 0.1, 0.1, 0.1)
        self.cuboid3 = Cuboid3(-0.2, 0.2, 1.5, 0.1, 0.1, 0.1)
        self.cuboid4 = Cuboid3(-0.2, -0.2, 1.5, 0.1, 0.1, 0.1)
        self.camera = Camera()

    def load_font(self):
        pygame.font.init()
        Font.neodgm_32 = pygame.font.Font('font/neodgm.ttf', 32)
        Font.neodgm_16 = pygame.font.Font('font/neodgm.ttf', 16)

    def key_callback(self, window, key, scancode, action, mods):
        if action == GLFW_PRESS:
            for k in self.key_pressed:
                if key == self.key_mapping[k]:
                    self.key_pressed[k] = True
        if action == GLFW_RELEASE:
            for k in self.key_pressed:
                if key == self.key_mapping[k]:
                    self.key_pressed[k] = False

    def mouse_button_callback(self, window, button, action, mods):
        scale = glfwGetMonitorContentScale(self.monitor)
        pos_raw = glfwGetCursorPos(window)

        if sys.platform == 'darwin':
            pos = [pos_raw[0], pos_raw[1]]
        else:
            pos = [pos_raw[0] / scale[0], pos_raw[1] / scale[1]]
        
        if action == GLFW_RELEASE and button == GLFW_MOUSE_BUTTON_LEFT:
            if self.scene == 'title':
                scenetitle.mouse_up(self, pos)
            if self.scene == 'game':
                scenetitle.mouse_up(self, pos)

    def window_close_callback(self, window):
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    def run(self):
        while not glfwWindowShouldClose(self.window):
            self.clock.tick(self.fps)
            print(self.clock.get_fps())
            self.handle_scene()
            glfw.poll_events()

    def handle_scene(self):
        if self.scene == 'title':
            scenetitle.loop(self)
        elif self.scene == 'game':
            scenegame.loop(self)

if __name__ == '__main__':
    Game().run()
