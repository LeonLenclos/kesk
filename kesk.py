#!/usr/bin/env python3

"""Kesk is a simple keyboard-only drawing software made with pygame"""

import pygame
pygame.init()

WIN_COLOR = 100, 100, 100
CURSOR_COLOR = 255, 50, 50
DEFAULT_FG_COLOR = 0, 0, 0
DEFAULT_BG_COLOR = 255, 255, 255

DEFAULT_SKETCH_WIDTH = 50
DEFAULT_SKETCH_HEIGHT = 50

SHIFT_REPETITIONS = 5
CURSOR_BLINK_FRAMES = 15

class Kesk:
    """The application's class."""

    def __init__(self):
        """Init Kesk."""

        # colors
        self.fg_color = DEFAULT_FG_COLOR
        self.bg_color = DEFAULT_BG_COLOR

        # display
        self.screen = pygame.display.set_mode((0, 0))
        pygame.display.set_caption("Kesk")
        self.size_max = self.screen.get_rect().size
        self.clock = pygame.time.Clock()

        # sketch
        sketch_size = DEFAULT_SKETCH_WIDTH, DEFAULT_SKETCH_HEIGHT
        self.sketch = Sketch(sketch_size, self.bg_color)
        self.scale = 1
        self.size = self.best_screen_size()

        # cursor is a x,y tuple
        self.cursor = int(self.sketch.size[0]/2), int(self.sketch.size[1]/2)

        # historic for undo/redo
        self.historic_backward = []
        self.historic_forward = []

    def do_actions(self, keys):
        """Do the actions related to the keys (k)
        Return True if some action have been done"""
        k = keys
        p = pygame

        # if shift, do the move SHIFT_REPETITIONS times
        repeat = 1
        if k[p.K_RSHIFT] or k[p.K_LSHIFT]:
            repeat = SHIFT_REPETITIONS

        # do actions if no actions has been done since 10 frames
        for i in range(repeat):

            # change value of selected pixel
            if k[p.K_RETURN]:
                self.sketch.set_at(self.cursor, self.fg_color)
            elif k[p.K_BACKSPACE]:
                self.sketch.set_at(self.cursor, self.bg_color)

            # move the cursor
            if k[p.K_a]:
                self.cursor = move(self.cursor, (-1, -1))  # UP LEFT
            elif k[p.K_z]:
                self.cursor = move(self.cursor, ( 0, -1))  # UP
            elif k[p.K_e]:
                self.cursor = move(self.cursor, (+1, -1))  # UP RIGHT
            elif k[p.K_q]:
                self.cursor = move(self.cursor, (-1,  0))  # LEFT
            elif k[p.K_d]:
                self.cursor = move(self.cursor, (+1,  0))  # RIGHT
            elif k[p.K_w]:
                self.cursor = move(self.cursor, (-1, +1))  # DOWN LEFT
            elif k[p.K_x]:
                self.cursor = move(self.cursor, ( 0, +1))  # DOWN
            elif k[p.K_c]:
                self.cursor = move(self.cursor, (+1, +1))  # DOWN RIGHT

            # move the image in the window
            elif k[p.K_UP]:
                self.sketch.pos = move(self.sketch.pos, (0, -1))
            elif k[p.K_LEFT]:
                self.sketch.pos = move(self.sketch.pos, (-1, 0))
            elif k[p.K_DOWN]:
                self.sketch.pos = move(self.sketch.pos, (0, +1))
            elif k[p.K_RIGHT]:
                self.sketch.pos = move(self.sketch.pos, (+1, 0))

            # Other actions
            elif k[p.K_MINUS]: # Zoom out
                if self.scale > 1: self.scale -= 1
            elif k[p.K_PLUS] or k[p.K_EQUALS]: # Zoom in
                self.scale += 1
            elif k[p.K_u]: # Undo
                if len(self.historic_backward) > 1:
                    self.historic_forward.append(self.historic_backward[-1])
                    del self.historic_backward[-1]
                    self.sketch = self.historic_backward[-1]
            elif k[p.K_y]: # Redo
                if len(self.historic_forward) > 1:
                    self.historic_backward.append(self.historic_forward[-1])
                    del self.historic_forward[-1]
                    self.sketch = self.historic_backward[-1]
            elif k[p.K_r]: # reset
                self.sketch = Sketch(self.sketch.size, self.bg_color)
                break
            elif k[p.K_s]: # save
                pass # TODO: Save as png or something
            else:
                return False

        return True


    def get_surface(self, cursor=True):

        surface = pygame.Surface(move(self.sketch.size, self.sketch.pos))

        # draw the surface
        surface.blit(self.sketch, self.sketch.pos)
        if cursor :
            cursor_pos = move(self.cursor, self.sketch.pos)
            surface.set_at(cursor_pos, CURSOR_COLOR)

        # scale the surface
        size = (surface.get_width() * self.scale,
                surface.get_height() * self.scale)
        surface = pygame.transform.scale(surface, size)

        return surface

    def main_loop(self):
        """The app main loop"""

        # ticker for count frame when a key is pressed
        keys_ticker = 0
        cursor_blink = CURSOR_BLINK_FRAMES

        quit = False
        while not quit:
            # events
            keys = None
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    # quit the program
                    quit = True

                if event.type == pygame.VIDEORESIZE:
                    # resize the window
                    window_size = (event.w, event.h)
                    self.screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

                if event.type == pygame.KEYDOWN:
                    pass

            # get pressed keys
            keys = pygame.key.get_pressed()

            # Do actions
            if keys_ticker <= 0:
                if keys:
                    if self.do_actions(keys):
                        keys_ticker = CURSOR_BLINK_FRAMES
            else : keys_ticker -= 1

            self.cursor = constrain(self.cursor,self.size)



            # TODO: historic
            # # update historic
            # grid = [list(x) for x in grid]
            # if len(historic_backward) > 0:
            #     print(historic_backward[-1] is grid)
            #     if grid != historic_backward[-1]:
            #
            #         historic_backward.append(grid)
            #         historic_forward = []
            #         if len(historic_backward) > 20:
            #             historic_backward = historic_backward[1:]
            # else:
            #     historic_backward.append(grid)
            #     print(0)


            # draw
            self.screen.fill(WIN_COLOR)
            self.screen.blit(self.get_surface(cursor_blink > 0), (0, 0))

            cursor_blink -= 1
            if cursor_blink < -CURSOR_BLINK_FRAMES:
                cursor_blink = CURSOR_BLINK_FRAMES

            pygame.display.update()
            self.clock.tick(60)


    def best_screen_size(self):
        """Set the window dimension and scale according to screen size.
        Return a w,h tuple"""
        height = self.size_max[1]
        width = self.sketch.width*self.size_max[1]/self.sketch.height
        if width > self.size_max[0]:
            height = self.sketch.height*self.size_max[0]/self.sketch.width
            width = self.size_max[0]

        self.scale = int(width/self.sketch.width)
        pygame.display.set_mode((int(width), int(height)))
        return width, height

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

def move(pos, mov):
    """Change a position (pos) by a movement (mov). Both must be (x,y) tuples"""
    return (pos[0]+mov[0], pos[1]+mov[1])

def constrain(pos, size):
    """constrain a position (pos) in the area defined by size"""
    x, y = pos
    w, h = size
    if x >= w: x = x % w
    if y >= h: y = y % h
    while x < 0: x = w + x
    while y < 0: y = h + y
    return x, y


if __name__ == "__main__":

    kesk = Kesk()
    kesk.main_loop()
