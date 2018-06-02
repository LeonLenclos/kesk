import pygame as p

# The colors of the sketch
DEFAULT_FG_COLOR = 0, 0, 0
DEFAULT_BG_COLOR = 255, 255, 255

# The size of the sketch
DEFAULT_SKETCH_WIDTH = 50
DEFAULT_SKETCH_HEIGHT = 50

WIN_COLOR = 50, 50, 50
CURSOR_COLOR = 255, 0, 0
ACTION_REPETITIONS = 5
CURSOR_BLINK_FRAMES = 15
HISTORIC_MAX_LEN = 100

ACTION_KEYS = {
    "repeat" : [p.K_LSHIFT, p.K_RSHIFT],
    "cursor_up" : p.K_z,
    "cursor_right_up" : p.K_e,
    "cursor_right" : p.K_d,
    "cursor_right_down" : p.K_c,
    "cursor_down" : p.K_x,
    "cursor_left_down" : p.K_w,
    "cursor_left" : p.K_q,
    "cursor_left_up" : p.K_a,
    "view_up" : p.K_UP,
    "view_right" : p.K_RIGHT,
    "view_down" : p.K_DOWN,
    "view_left" : p.K_LEFT,
    "zoom_out" : p.K_MINUS,
    "zoom_in" : [p.K_PLUS, p.K_EQUALS],
    "draw" : p.K_RETURN,
    "erase" : p.K_BACKSPACE,
    "undo" : p.K_u,
    "redo" : p.K_y,
    "reset" : p.K_r,
    "save" : p.K_s,
    "quit" : p.K_ESCAPE
}
