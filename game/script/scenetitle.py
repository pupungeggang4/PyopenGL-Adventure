from script.module import *

def loop(game):
    render(game)

def render(game):
    game.surface_hud.fill(Color.white)
    game.surface_hud.blit(Font.neodgm_32.render('Adventure', False, Color.black), UI.Title.text_title)
    game.surface_hud.blit(Font.neodgm_32.render('Start Game', False, Color.black), UI.Title.text_start)
    game.surface_hud.blit(Font.neodgm_32.render('Erase Data', False, Color.black), UI.Title.text_erase)
    pygame.draw.rect(game.surface_hud, Color.black, UI.Title.button_start, 2)
    pygame.draw.rect(game.surface_hud, Color.black, UI.Title.button_erase, 2)
    surf_texture = pygame.image.tobytes(game.surface_hud, 'RGBA')

    glClearColor(0.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(game.program)

    glEnableVertexAttribArray(game.location['a_position_hud'])
    glEnableVertexAttribArray(game.location['a_texcoord'])
    glDisableVertexAttribArray(game.location['a_position'])
   
    glBindVertexArray(game.vao)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, 1280, 720, 0, GL_RGBA, GL_UNSIGNED_BYTE, surf_texture)
    glUniform1i(game.location['u_mode_v'], 0)
    glUniform1i(game.location['u_mode_f'], 0)
    glBindBuffer(GL_ARRAY_BUFFER, game.b_hud)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, game.b_hud_index)
    glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_SHORT, ctypes.c_void_p(0))
    
    glfw.swap_buffers(game.window)

def mouse_up(game, pos):
    if point_inside_rect_ui(pos, UI.Title.button_start):
        game.scene = 'game'
        game.state = ''