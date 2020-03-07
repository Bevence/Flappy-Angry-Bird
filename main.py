import random
import sys
import pygame
from pygame.locals import *

# variables for the game

FPS = 32
SCREENWIDTH = 1000
SCREENHEIGTH = 500
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGTH))
GROUND_Y = SCREENHEIGTH * 0.8
GAME_IMAGES = {}
GAME_SOUNDS = {}
PLAYER = 'media/img/player1.png'
BACKGROUND = 'media/img/background.jpg'
PIPES = 'media/img/pipe.png'


def welcomeScreen():
    player_x = int(SCREENWIDTH/5)
    player_y = int((SCREENHEIGTH - GAME_IMAGES['player'].get_height())/2)
    # message_x = int((SCREENWIDTH - GAME_IMAGES['screen'].get_width())/2)
    # message_y = int(SCREENHEIGTH * 0.1)
    base_x = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return

            else:
                SCREEN.blit(GAME_IMAGES['background'], (0, 0))
                SCREEN.blit(GAME_IMAGES['base'], (base_x, GROUND_Y))
                #SCREEN.blit(GAME_IMAGES['player'], (player_x, player_y))
                SCREEN.blit(GAME_IMAGES['screen'], (0, 0))
                pygame.display.update()
                FPSCLOCK.tick(FPS)


def mainGame():
    score = 0
    player_x = int(SCREENWIDTH/5)
    player_y = int(SCREENHEIGTH/2)
    base_x = 0

    # creates 2 pipes
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    newPipe3 = getRandomPipe()
    newPipe4 = getRandomPipe()
    newPipe5 = getRandomPipe()
    # newPipe6 = getRandomPipe()

    # list of upper pipe
    upper_pipes = [
        {'x': SCREENWIDTH, 'y': newPipe1[0]['y']},
        {'x': SCREENWIDTH + (SCREENWIDTH/5), 'y': newPipe2[0]['y']},
        {'x': SCREENWIDTH + 2*(SCREENWIDTH/5), 'y': newPipe3[0]['y']},
        {'x': SCREENWIDTH + 3*(SCREENWIDTH/5), 'y': newPipe4[0]['y']},
        {'x': SCREENWIDTH + 4*(SCREENWIDTH/5), 'y': newPipe5[0]['y']},
        # {'x': SCREENWIDTH + 5*(SCREENWIDTH/5), 'y': newPipe6[0]['y']}
    ]
    # print(upper_pipes)

    # list of lower pipe
    lower_pipes = [
        {'x': SCREENWIDTH, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + (SCREENWIDTH/5), 'y': newPipe2[1]['y']},
        {'x': SCREENWIDTH + 2*(SCREENWIDTH/5), 'y': newPipe3[1]['y']},
        {'x': SCREENWIDTH + 3*(SCREENWIDTH/5), 'y': newPipe4[1]['y']},
        {'x': SCREENWIDTH + 4*(SCREENWIDTH/5), 'y': newPipe5[1]['y']},
        # {'x': SCREENWIDTH + 5*(SCREENWIDTH/5), 'y': newPipe6[1]['y']}
    ]
    # print(lower_pipes)
    pipe_vel_x = -4

    player_vel_y = -9
    player_max_vel_y = 10
    player_min_vel_y = -8
    player_acc_y = 1

    player_flap_accv = -8
    player_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_vel_y = player_flap_accv
                    player_flapped = True
                    GAME_SOUNDS['wing'].play()

        crash_test = isCollide(player_x, player_y, upper_pipes, lower_pipes)
        if crash_test:
            return

        # score check
        player_mid_position = player_x + GAME_IMAGES['player'].get_width()/2
        for pipe in upper_pipes:
            pipe_mid_position = pipe['x'] + \
                GAME_IMAGES['pipe'][0].get_width()/2
            if pipe_mid_position < player_mid_position < pipe_mid_position + (-pipe_vel_x):
                score = score + 1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()
                if 10 < score < 20:  # increase the speed of the pipevelocity
                    pipe_vel_x -= 1
                if score == 20:  # increase the speed of the pipevelocity
                    pipe_vel_x -= 1

        if player_vel_y < player_max_vel_y and not player_flapped:
            player_vel_y += player_acc_y

        if player_flapped:
            player_flapped = False

        player_height = GAME_IMAGES['player'].get_height()
        player_y = player_y + \
            min(player_vel_y, GROUND_Y - player_y - player_height)

        # moves pipes to the left
        for upperpipe, lowerpipe in zip(upper_pipes, lower_pipes):
            upperpipe['x'] += pipe_vel_x
            lowerpipe['x'] += pipe_vel_x

        # add the new pipe
        if 0 < upper_pipes[0]['x'] < 7:
            new_pipe = getRandomPipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])

        # remove the pipe out of the screen
        if upper_pipes[0]['x'] < -GAME_IMAGES['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        # blit the screen
        SCREEN.blit(GAME_IMAGES['background'], (0, 0))
        for upperpipe, lowerpipe in zip(upper_pipes, lower_pipes):
            SCREEN.blit(GAME_IMAGES['pipe'][0],
                        (upperpipe['x'], upperpipe['y']))
            SCREEN.blit(GAME_IMAGES['pipe'][1],
                        (lowerpipe['x'], lowerpipe['y']))

        SCREEN.blit(GAME_IMAGES['base'], (base_x, GROUND_Y))
        SCREEN.blit(GAME_IMAGES['player'], (player_x, player_y))
        my_digits = [int(x) for x in list(str(score))]
        width = 0
        for digit in my_digits:
            width += GAME_IMAGES['numbers'][digit].get_width()
        x_offset = (SCREENWIDTH - width)/2

        for digit in my_digits:
            SCREEN.blit(GAME_IMAGES['numbers'][digit],
                        (x_offset, SCREENHEIGTH*0.12))
            x_offset += GAME_IMAGES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(player_x, player_y, upper_pipes, lower_pipes):
    if player_y > GROUND_Y - 50 or player_y < 0:
        GAME_SOUNDS['hit'].play()
        return True

    for pipe in upper_pipes:
        pipe_height = GAME_IMAGES['pipe'][0].get_height()
        if (player_y < pipe_height + pipe['y'] and abs(player_x - pipe['x']) < GAME_IMAGES['pipe'][0].get_width()/2):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lower_pipes:
        if (player_y + GAME_IMAGES['player'].get_height() > pipe['y'] and abs(player_x - pipe['x']) < GAME_IMAGES['pipe'][0].get_width()/2):
            GAME_SOUNDS['hit'].play()
            return True

    return False


def getRandomPipe():
    # generate position of pipes

    pipeHeight = GAME_IMAGES['pipe'][1].get_height()
    offset = SCREENHEIGTH/4
    y2 = offset + random.randrange(0, int(SCREENHEIGTH -
                                          GAME_IMAGES['base'].get_height() - 1.2 * offset))
    pipe_x = SCREENWIDTH
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipe_x, 'y': -y1},  # upper pipe
        {'x': pipe_x, 'y': y2}  # lower pipe
    ]
    return pipe


if __name__ == "__main__":
    # main function of the game
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Angry Bird')
    # images for game
    GAME_IMAGES['numbers'] = (
        pygame.image.load('media/img/0.png').convert_alpha(),
        pygame.image.load('media/img/1.png').convert_alpha(),
        pygame.image.load('media/img/2.png').convert_alpha(),
        pygame.image.load('media/img/3.png').convert_alpha(),
        pygame.image.load('media/img/4.png').convert_alpha(),
        pygame.image.load('media/img/5.png').convert_alpha(),
        pygame.image.load('media/img/6.png').convert_alpha(),
        pygame.image.load('media/img/7.png').convert_alpha(),
        pygame.image.load('media/img/8.png').convert_alpha(),
        pygame.image.load('media/img/9.png').convert_alpha(),
    )

    GAME_IMAGES['screen'] = pygame.image.load(
        'media/img/message.png').convert_alpha()
    GAME_IMAGES['base'] = pygame.image.load(
        'media/img/base.png').convert_alpha()
    GAME_IMAGES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPES).convert_alpha(), 180),
        pygame.image.load(PIPES).convert_alpha()
    )

    GAME_IMAGES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_IMAGES['player'] = pygame.image.load(PLAYER).convert_alpha()

    # audio effects for game
    GAME_SOUNDS['die'] = pygame.mixer.Sound('media/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('media/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('media/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('media/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('media/audio/wing.wav')

    while True:
        welcomeScreen()
        mainGame()
