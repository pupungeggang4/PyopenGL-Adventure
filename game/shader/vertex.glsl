#version 410 core

uniform int u_mode_v;
in vec4 a_position;
in vec2 a_texcoord;
out vec2 p_texcoord;

void main() {
    if (u_mode_v == 0) {
        gl_Position = a_texcoord;
    } else {
        gl_Position = a_position;
    }
    p_texcoord = a_texcoord;
}