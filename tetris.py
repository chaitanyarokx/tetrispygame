import pygame, random, sys, time
from pygame.locals import *


def terminate():  # Exit function
    pygame.quit()
    sys.exit(0)


tetpy = pygame
shapes = [[[2, 2], [2, 2]], [[2, 0], [2, 0], [2, 2]], [[0, 2], [0, 2], [2, 2]], [[2], [2], [2], [2]],
          [[0, 2, 2], [2, 2, 0]], [[2, 2, 0], [0, 2, 2]], [[2, 2, 2], [0, 2, 0]]]  # The shapes of the tetris blocks (7)
colours = [(0, 0, 0), (25, 25, 112), (255, 20, 147), (0, 150, 220), (0, 220, 150), (60, 200, 10), (180, 210, 5),
           (210, 180, 10), (100, 200, 170)]  # Colour for tetris blocks
tetpy.init()
tetpy.display.set_mode((320, 240))
screen_surface = tetpy.display.get_surface()
frame = [[1] + [0 for a in range(8)] + [1] for a in range(19)] + [
    [1 for a in range(10)]]  # Setup the 2d frame for blocks
s = 12  # side length of blocks
block = Rect((100, 0, s, s))  # renders the rectangle
rand = -1
change = 0
shape_chosen = []
location = [-9, 0]  # Location[0] stores the left and right location location[1] stores the direction north and south
time_loaction_increase = 0
block_speed_counter = 60
instant_down = 0
clear_row= []
back_ground = tetpy.image.load("trip.jpg")  # Load background image
game_over = tetpy.image.load("gameover.jpg")  # Loading background image
game_variable = -1
font_disp = tetpy.font.Font(tetpy.font.get_default_font(), 14)
score = 0
tetpy.mixer.music.load("trip.ogg")  # Loading music file
tetpy.mixer.music.play(-1)  # Looping music file
while 1:
    screen_surface.fill((0, 0, 0))
    score_disp = font_disp.render("Score " + str(score), 1, (255, 255, 255))  # Display the score on screen
    rect_get = score_disp.get_rect()
    rect_get.bottomright = (310, 230)  # Position where the score should be shown
    screen_surface.blit(back_ground, (0, 0))  # Background image renderer
    screen_surface.blit(score_disp, rect_get)
    if game_variable > - 1:
        rand = 10
        instant_down = 0
        if not time_loaction_increase % 5:
            game_variable -= 1
            time_loaction_increase = 1
        if game_variable == 0:  # Game over condition
            game_variable = 99
    if rand < -1:
        rand += 1  # Increments b till -1 so that it can chose next shape
    if rand == -1:
        rand = random.randint(0, 6)  # Choosing a random integer
        shape_chosen = shapes[rand]  # Choosing a random shape based on random integer
        location = [5 - len(shape_chosen) // 2, 0]  # Sets the starting coordinates
    if not time_loaction_increase % block_speed_counter or instant_down:  # Current shape loop
        operation = [shape_chosen[:], location[:]]  # Making the shape
        location[1] += 1
    next_shape_selector = 0
    c = 0
    for l in shape_chosen:
        r = 0
        for k in l:  # Direction of shape
            while c + location[0] < 1:  # Screen left boundary check
                location[0] += 1
            while c + location[0] > 8:  # Screen right boundary check
                location[0] -= 1
            if frame[r + location[1]][c + location[0]] and k:  # Screen lower boundary check
                if location[1] == 0:  # To check if blocks reached top of screen
                    game_variable = 10
                next_shape_selector = 1  # To get the next shape if current shape has reached top of blocks
            r += 1
        c += 1
    if next_shape_selector and not change:  # Loop to render the new shape
        shape_chosen, location = operation
        column_shape = 0
        for l in shape_chosen:
            row_shape = 0
            for k in l:
                if k:
                    frame[row_shape + location[1]][column_shape + location[0]] = rand + 2  # Inserting next shape
                row_shape += 1
            column_shape += 1
        rand = -20  # Reinitializing other values
        time_loaction_increase = 1  # all the values are set to a default parameter which is common to all new shapes
        next_shape_selector = 0
        instant_down = 0
        shape_chosen = []
    change = False
    for r in frame[:-1]:              # Loop to remove the completed line
        if not r.count(0):            # checks whether a line is complete or not
            wr = r                    # assigns it to a temp variable
            clear_row+= [[frame.index(wr), 200]]
            time.sleep(2)
            frame.remove(wr)           # removes the complete line
            frame = [[1] + [0 for x in range(8)] + [1]] + frame  # Inserting empty line in the frame
            if game_variable == -1:  # A line of 8 blocks complete
                score += 10  # Score increased
                block_speed_counter = max(8,block_speed_counter - 1)     #   increases the speed a bit when every line is cleared
    c = 0
    for l in frame:
        r = 0
        for k in l:
            try:
                if r >= location[0] and c >= location[1] and shape_chosen[r - location[0]][c - location[1]]:  # makes the shapes visible when it falls
                    k = rand + 2
            except:
                pass
            screen_surface.fill([x * 1 for x in colours[k]], block.move(r * s, c * s))  # Fills colour behind the grid
            r += 1
        c += 1

    if game_variable >= 0:
        screen_surface.blit(game_over, (0, 0))  # displays the gameover image at the end
        if game_variable == 99:
            tetpy.display.flip()
            time.sleep(4)
            print (
            "The game is over. Your score was : {0} and number of lines cleared were : {1}".format(score, score / 10))
            sys.exit()
    tetpy.display.flip()  # Display the game
    time_loaction_increase += 1
    for event in tetpy.event.get():  # Event loop

        if event.type == QUIT:  # To Exit from game
            terminate()

        if event.type == KEYDOWN:
            if event.key in (K_LEFT, K_a):  # When left key pressed
                operation = [shape_chosen[:], location[:]]
                location[0] -= 1
            if event.key in (K_RIGHT, K_d):  # When right key pressed
                operation = [shape_chosen[:], location[:]]
                location[0] += 1
            if event.key in (K_DOWN, K_s):  # When down key pressed
                operation = [shape_chosen[:], location[:]]
                location[1] += 1
                time_loaction_increase += 1
            if event.key in (K_UP, K_w) and shape_chosen:  # When up key pressed
                operation = [shape_chosen[:], location[:]]
                shape_chosen = [[shape_chosen[x][-y - 1] for x in range(len(shape_chosen))] for y in
                                range(len(shape_chosen[0]))]  # Changing the orientation of the shape
                change = 1
            if event.key == K_SPACE:
                instant_down = 1


