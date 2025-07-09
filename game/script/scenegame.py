from script.module import *

def loop(game):
    render(game)

def render(game):
    game.surface_hud.fill(Color.transparent)
    surf_texture = pygame.image.tobytes(game.surface_hud, 'RGBA')

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_BLEND)
    glDisable(GL_DEPTH_TEST)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(game.program)
   
    glBindVertexArray(game.vao)

    glDisableVertexAttribArray(game.location['a_position_hud'])
    glDisableVertexAttribArray(game.location['a_texcoord'])
    glEnableVertexAttribArray(game.location['a_position'])

    glUniform1i(game.location['u_mode_v'], 1)
    glUniform1i(game.location['u_mode_f'], 1)
    glUniform3f(game.location['u_color'], 0.0, 1.0, 0.0)
    glBindBuffer(GL_ARRAY_BUFFER, game.b_cuboid)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, game.b_cuboid_index)
    glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_SHORT, ctypes.c_void_p(0))

    glEnable(GL_DEPTH_TEST)
    glEnableVertexAttribArray(game.location['a_position_hud'])
    glEnableVertexAttribArray(game.location['a_texcoord'])
    glDisableVertexAttribArray(game.location['a_position'])
    
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1280, 720, 0, GL_RGBA, GL_UNSIGNED_BYTE, surf_texture)
    glUniform1i(game.location['u_mode_v'], 0)
    glUniform1i(game.location['u_mode_f'], 0)
    RenderGL.render_cuboid(game, game.cuboid, 0, [0.0, 1.0, 0.0])
    
    glfw.swap_buffers(game.window)

def mouse_up(game, pos):
    if point_inside_rect_ui(pos, UI.Title.button_start):
        game.scene = 'game'
        game.state = ''