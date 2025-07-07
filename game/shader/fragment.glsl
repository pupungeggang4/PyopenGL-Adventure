#version 410 core

precision highp float;
uniform sampler2D t_sampler;
uniform int u_mode_f;
uniform vec3 u_color;
in vec2 p_texcoord;
out vec3 o_color;

void main() {
    if (u_mode_f == 0) {
        o_color = texture(t_sampler, p_texcoord);
    } else {
        o_color = vec4(u_color, 1.0);
    }
}