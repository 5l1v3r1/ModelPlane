#version 330 core

layout (location = 0) in vec3 a_position;
layout (location = 1) in vec3 a_color;

out vec3 color;

uniform mat4 u_modelview;
uniform mat4 u_projection;

void main() {
    gl_Position = u_projection * u_modelview * vec4(a_position, 1.0f);
    color = a_color;
}