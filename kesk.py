"""Kesk is a simple keyboard only drawing software"""
import pygame
pygame.init()

def main ():

    # size of the image
    size = width, height = 50,50
    # scale of the image in the window
    scale = 10
    # size of the window
    window_size = window_width, window_height = width*scale, height*scale
    # position of the image in the window
    img_pos = (0, 0)
    # colors
    fg_color = 0, 0, 0
    bg_color = 255, 255, 255

    # create window and clock
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
    pygame.display.set_caption("Kesk")
    clock = pygame.time.Clock()

    # 2D list for pixels values
    grid = [[bg_color for x in range(width)] for y in range(height)]

    # cursor position
    pos = (int(width/2), int(height/2))

    # historic for undo/redo
    historic_backward = []
    historic_forward = []

    # ticker for count frame when a key is pressed
    move_ticker = 0

    # Main loop
    quit = False
    while not quit:
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # quit the program
                quit = True
            if event.type == pygame.VIDEORESIZE:
                # resize the window
                window_size = (event.w, event.h)
                screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)
            if event.type == pygame.KEYDOWN:
                # keys
                if event.key == pygame.K_MINUS:
                    # zoom out
                    if scale > 1:
                        scale -= 1
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    # zoom in
                    scale += 1
                elif event.key == pygame.K_u:
                    # undo
                    if len(historic_backward) > 1:
                        historic_forward.append(historic_backward[-1])
                        del historic_backward[-1]
                        grid = historic_backward[-1][0]
                        pos = historic_backward[-1][1]
                elif event.key == pygame.K_y:
                    # redo
                    if len(historic_forward) > 1:
                        historic_backward.append(historic_forward[-1])
                        del historic_forward[-1]
                        grid = historic_backward[-1][0]
                        pos = historic_backward[-1][1]
                elif event.key == pygame.K_r:
                    # reset
                    grid = [[bg_color for x in range(width)] \
                           for y in range(height)]
                elif event.key == pygame.K_s:
                    # save
                    pass # NOT YET IMPLEMENTED !

        # get pressed keys
        keys = pygame.key.get_pressed()

        # if shift, do the move 5 times
        repeat = 1
        if keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT]:
            repeat = 5

        # do actions if no actions has been done since 10 frames
        if move_ticker <= 0:
            for i in range(repeat):
                move_ticker = 10

                # move the cursor
                if keys[pygame.K_a]:
                    pos = move(pos, (-1, -1))  # UP LEFT
                elif keys[pygame.K_z]:
                    pos = move(pos, ( 0, -1))  # UP
                elif keys[pygame.K_e]:
                    pos = move(pos, (+1, -1))  # UP RIGHT
                elif keys[pygame.K_q]:
                    pos = move(pos, (-1,  0))  # LEFT
                elif keys[pygame.K_d]:
                    pos = move(pos, (+1,  0))  # RIGHT
                elif keys[pygame.K_w]:
                    pos = move(pos, (-1, +1))  # DOWN LEFT
                elif keys[pygame.K_x]:
                    pos = move(pos, ( 0, +1))  # DOWN
                elif keys[pygame.K_c]:
                    pos = move(pos, (+1, +1))  # DOWN RIGHT
                # move the image in the window
                elif keys[pygame.K_UP]:
                    img_pos = move(img_pos, (0, -scale))
                elif keys[pygame.K_LEFT]:
                    img_pos = move(img_pos, (-scale, 0))
                elif keys[pygame.K_DOWN]:
                    img_pos = move(img_pos, (0, +scale))
                elif keys[pygame.K_RIGHT]:
                    img_pos = move(img_pos, (+scale, 0))
                # reset move_ticker if no actions
                else: move_ticker = 0

                pos = constrain(pos,size)

                # change value of selected pixel
                if keys[pygame.K_RETURN]:
                    grid[pos[0]][pos[1]] = fg_color
                elif keys[pygame.K_BACKSPACE]:
                    grid[pos[0]][pos[1]] = bg_color
        else:
            move_ticker -= 1

        # update historic
        if len(historic_backward) > 0:
            if not (grid == historic_backward[-1][0] and
                    pos == historic_backward[-1][1]):
                historic_backward.append(([list(x) for x in grid], pos))
                historic_forward = []
                if len(historic_backward) > 20:
                    historic_backward = historic_backward[1:]
        else:
            historic_backward.append((grid, pos))

        # draw
        screen.fill((255, 0, 0))
        for x, row in enumerate(grid):
            for y, value in enumerate(row):
                rect = (x*scale+img_pos[0], y*scale+img_pos[1], scale, scale)
                pygame.draw.rect(screen, value, rect)

        rect = (pos[0]*scale+img_pos[0], pos[1]*scale+img_pos[1], scale, scale)
        pygame.draw.rect(screen, (255, 0, 0), rect, 2)

        pygame.display.update()
        clock.tick(60)

def constrain(pos, size):
    """constrain a position (pos) in the area defined by size"""
    x, y = pos
    w, h = size
    if x >= w: x = x%w
    if y >= h: y = y%h
    while x < 0: x = w+x
    while y < 0: y = h+y
    return (x, y)

def move(pos, mov):
    """Change a position (pos) by a movement (mov). Both must be (x,y) tuples"""
    return (pos[0]+mov[0], pos[1]+mov[1])

main()
