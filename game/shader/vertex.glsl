#version 410 core

uniform int u_mode_v;
in vec2 a_texcoord;
in vec4 a_position_hud;
in vec4 a_position;
uniform vec3 u_model_pos; 
uniform vec3 u_model_scale;
uniform vec3 u_cam_pos;
uniform vec3 u_cam_rot;
float fov = 1.1;
float asp = 16.0 / 9.0;
float near = 0.1;
float far = 10.0;
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
        mat4 m_cam_z_inv = mat4(
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, -1.0, 0.0,
            0.0, 0.0, 0.0, 1.0
        );
        mat4 m_cam_proj = mat4(
            1.0 / (asp * tan(fov / 2.0)), 0.0, 0.0, 0.0,
            0.0, 1.0 / tan(fov / 2.0), 0.0, 0.0,
            0.0, 0.0, -(far + near) / (far - near), -1.0,
            0.0, 0.0, -(2.0 * far * near) / (far - near), 0.0
        );
        mat4 m_cam_rot_x = mat4(
            1.0, 0.0, 0.0, 0.0,
            0.0, cos(u_cam_rot.x), sin(u_cam_rot.x), 0.0,
            0.0, -sin(u_cam_rot.x), cos(u_cam_rot.x), 0.0,
            0.0, 0.0, 0.0, 1.0
        );
        mat4 m_cam_rot_y = mat4(
            cos(u_cam_rot.y), 0.0, -sin(u_cam_rot.y), 0.0,
            0.0, 1.0, 0.0, 0.0,
            sin(u_cam_rot.y), 0.0, cos(u_cam_rot.y), 0.0,
            0.0, 0.0, 0.0, 1.0
        );
        mat4 m_cam_pos = mat4(
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            -u_cam_pos.x, -u_cam_pos.y, -u_cam_pos.z, 1.0
        );
        pos = m_model_scale * pos;
        pos = m_model_pos * pos;
        pos = m_cam_pos * pos;
        pos = m_cam_z_inv * pos;
        pos = m_cam_rot_x * pos;
        pos = m_cam_rot_y * pos;
        pos = m_cam_proj * pos;
        gl_Position = pos;
    }
    p_texcoord = a_texcoord;
}