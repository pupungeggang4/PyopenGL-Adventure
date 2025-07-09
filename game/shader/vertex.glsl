#version 410 core

uniform int u_mode_v;
in vec2 a_texcoord;
in vec4 a_position_hud;
in vec4 a_position;
uniform vec3 u_model_pos; 
uniform vec3 u_model_scale;
uniform vec3 u_cam_pos;
uniform vec3 u_cam_rot;
out vec2 p_texcoord;

void main() {
    if (u_mode_v == 0) {
        gl_Position = a_position_hud;
    } else {
        vec4 pos = a_position;
        mat4 m_model_pos = mat4(
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            u_model_pos.x, u_model_pos.y, u_model_pos.z, 1.0
        );
        mat4 m_model_scale = mat4(
            u_model_scale.x, 0.0, 0.0, 0.0,
            0.0, u_model_scale.y, 0.0, 0.0,
            0.0, 0.0, u_model_scale.z, 0.0,
            0.0, 0.0, 0.0, 1.0
        );
        pos = m_model_scale * pos;
        pos = m_model_pos * pos;
        gl_Position = pos;
    }
    p_texcoord = a_texcoord;
}