#!/usr/bin/env python3

"""Kesk (V1.0) is a simple keyboard-only drawing software made with pygame"""

import pygame
from config import *
pygame.init()

class Kesk:
    """The application's class."""

    def __init__(self,
                 fg_color=DEFAULT_FG_COLOR,
                 bg_color=DEFAULT_BG_COLOR,
                 width=DEFAULT_SKETCH_WIDTH,
                 height=DEFAULT_SKETCH_HEIGHT):
        """Init Kesk."""
        self.fg_color = fg_color
        self.bg_color = bg_color
        self.sketch = Sketch((width, height), self.bg_color)
        self.scale = 4
        self.screen = pygame.display.set_mode((0, 0), pygame.VIDEORESIZE)
        pygame.display.set_caption("Kesk")
        self.cursor = int(self.sketch.size[0]/2), int(self.sketch.size[1]/2)
        self.historic_backward = []
        self.historic_forward = []

    def do_actions(self, keys):
        """Do the actions related to the keys (k)"""
        def k(code):
            """Say if the key corresponding to the code have been pressed"""
            if type(ACTION_KEYS[code]) is list:
                for _k in ACTION_KEYS[code]:
                    if keys[_k]: return True
                return False
            else: return keys[ACTION_KEYS[code]]

        repeat = ACTION_REPETITIONS if k("repeat") else 1
        for _ in range(repeat):

            # move the cursor
            if k("cursor_left_up"):
                self.cursor = move(self.cursor, (-1, -1))
            if k("cursor_up"):
                self.cursor = move(self.cursor, ( 0, -1))
            if k("cursor_right_up"):
                self.cursor = move(self.cursor, (+1, -1))
            if k("cursor_left"):
                self.cursor = move(self.cursor, (-1,  0))
            if k("cursor_right"):
                self.cursor = move(self.cursor, (+1,  0))
            if k("cursor_left_down"):
                self.cursor = move(self.cursor, (-1, +1))
            if k("cursor_down"):
                self.cursor = move(self.cursor, ( 0, +1))
            if k("cursor_right_down"):
                self.cursor = move(self.cursor, (+1, +1))
            # constrain the cursor
            self.cursor = constrain(self.cursor,self.sketch.size)

            # move the image in the window
            if k("view_up"):
                self.sketch.pos = move(self.sketch.pos, (0, -1))
            if k("view_left"):
                self.sketch.pos = move(self.sketch.pos, (-1, 0))
            if k("view_down"):
                self.sketch.pos = move(self.sketch.pos, (0, +1))
            if k("view_right"):
                self.sketch.pos = move(self.sketch.pos, (+1, 0))

            # Zoom the image
            if k("zoom_out"):
                if self.scale > 1: self.scale -= 1
            if k("zoom_in"):
                self.scale += 1

            # change value of selected pixel
            if k("draw"):
                self.set_at_cursor(self.fg_color)
            if k("erase"):
                self.set_at_cursor(self.bg_color)

        # Unrepeatables actions
        if k("undo"): # Undo
            if len(self.historic_backward) > 0:
                self.historic_forward.append(self.sketch.copy())
                self.sketch = self.historic_backward[-1]
                del self.historic_backward[-1]
        if k("redo"): # Redo
            if len(self.historic_forward) > 0:
                self.historic_backward.append(self.sketch.copy())
                self.sketch = self.historic_forward[-1]
                del self.historic_forward[-1]
        if k("reset"): # reset
            self.update_historic()
            self.sketch = Sketch(self.sketch.size, self.bg_color)
        if k("save"): # save
            pygame.image.save(self.get_surface(), 'sketch.png')
        if k("quit"):
            self.quit = True

    def set_at_cursor(self, color):
        if self.sketch.get_at(self.cursor) != color:
            self.update_historic()
            self.sketch.set_at(self.cursor, color)

    def get_surface(self, cursor=False, scale=1):
        """Return the surface of the sketch."""
        surface = pygame.Surface(self.sketch.size)

        # draw the surface
        surface.blit(self.sketch, (0, 0))
        if cursor :
            surface.set_at(self.cursor, CURSOR_COLOR)

        # scale the surface
        size = (surface.get_width() * scale,
                surface.get_height() * scale)
        surface = pygame.transform.scale(surface, size)
        return surface

    def update_historic(self):
        """add the current sketch state to the historic"""
        self.historic_backward.append(self.sketch.copy())
        self.historic_forward = []
        if len(self.historic_backward) > HISTORIC_MAX_LEN:
            del self.historic_backward[0]

    def main_loop(self):
        """The app main loop"""

        cursor_blink = CURSOR_BLINK_FRAMES

        self.update_historic()
        clock = pygame.time.Clock()
        self.quit = False
        while not self.quit:
            # events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # quit the program
                    self.quit = True
                if event.type == pygame.VIDEORESIZE:
                    # resize the window
                    window_size = (event.w, event.h)
                    self.screen = pygame.display.set_mode(
                        window_size,
                        pygame.RESIZABLE
                    )
                if event.type == pygame.KEYDOWN:
                    # Do actions
                    self.do_actions(pygame.key.get_pressed())

            # display
            self.screen.fill(WIN_COLOR)
            surface = self.get_surface(cursor=cursor_blink>0, scale=self.scale)
            self.screen.blit(surface, self.sketch.pos)

            # blink
            cursor_blink -= 1
            if cursor_blink < -CURSOR_BLINK_FRAMES:
                cursor_blink = CURSOR_BLINK_FRAMES

            pygame.display.update()
            clock.tick(60)


class Sketch(pygame.Surface):
    """A drawing"""

    def width():
        doc = "The width property."
        def fget(self): return self.size[0]
        def fset(self, value): self.size = value, self.size[1]
        return locals()
    width = property(**width())

    def height():
        doc = "The height property."
        def fget(self): return self.size[1]
        def fset(self, value): self.size = self.size[0], value
        return locals()
    height = property(**height())

    def __init__(self, size, bg_color):
        super().__init__(size)
        self.size = size
        self.pos = (0, 0)
        self.fill(bg_color)

    def copy(self):
        """Return a copy of the sketch"""
        new_sketch = super(Sketch, self).copy()
        new_sketch.size = self.size
        new_sketch.pos = self.pos
        return new_sketch


def move(pos, mov):
    """Change a position (pos) by a movement (mov). Both must be (x,y) tuples"""
    return (pos[0]+mov[0], pos[1]+mov[1])

def constrain(pos, size):
    """constrain a position (pos) in the area defined by size"""
    x, y = pos
    w, h = size
    if x >= w: x = w-1
    if y >= h: y = h-1
    if x < 0: x = 0
    if y < 0: y = 0
    return x, y


if __name__ == "__main__": Kesk().main_loop()
