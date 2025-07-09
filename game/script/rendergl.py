from script.module import *

class RenderGL():
    @staticmethod
    def render_cuboid(game, cuboid, cam, color):
        glUniform3f(game.location['u_color'], color[0], color[1], color[2])
        glUniform3f(game.location['u_model_pos'], cuboid.pos.x, cuboid.pos.y, cuboid.pos.z)
        glUniform3f(game.location['u_model_scale'], cuboid.size.x, cuboid.size.y, cuboid.size.z)
        glBindBuffer(GL_ARRAY_BUFFER, game.b_cuboid)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, game.b_cuboid_index)
        glDrawElements(GL_TRIANGLES, 36, GL_UNSIGNED_SHORT, ctypes.c_void_p(0))