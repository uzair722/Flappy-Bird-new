import random
import sys
import pygame
from pygame.locals import *

FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND ='gallery/sprites/background.png'
PIPE ='gallery/sprites/pipe.png'

def welcomeScreen():
    playerx = int(SCREENWIDTH/5)
    playerY = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH- GAME_SPRITES['message'].get_width())/2)
    messageY = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type==KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type== KEYDOWN and (event.key==K_SPACE or event.key == K_UP):
                return
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playerY))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messageY))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()
                FPSCLOCK.tick(FPS)

def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playerY = int(SCREENWIDTH/2)
    basex = 0

    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    upperPipes = [
        {'x': SCREENWIDTH+200,'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH + 200+(SCREENWIDTH/2), 'y': newPipe1[0]['y']},
    ]
    lowerPipes = [
        {'x': SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': SCREENWIDTH + 200 + (SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]


    pipeVelx = -4

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    playerFlapAccv = -8
    playerFlapped = False


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerY > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True


        crashTest = isCollide(playerx, playerY, upperPipes, lowerPipes)
        if crashTest:
            return

        playerMidPos = playerx + GAME_SPRITES['player'].get_height()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos +4:
                score +=1
                print(f"your score is {score}")

        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False
        playerHeight = GAME_SPRITES['player'].get_height()
        playerY = playerY +min(playerVelY, GROUNDY - playerY - playerHeight)

        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVelx
            lowerPipe['x'] += pipeVelx
        
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])


        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        SCREEN.blit(GAME_SPRITES['background'],(0, 0))
        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        SCREEN.blit(GAME_SPRITES['base'],(basex, GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx, playerY))
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
def isCollide(playerx, playerY, upperPipes, lowerPipes):
    if playerY > GROUNDY - 25 or  playerY<0:
        return True

    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playerY < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            return True
    for pipe in lowerPipes:
        if (playerY + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            return True



    return False     

def getRandomPipe():
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT - GAME_SPRITES['base'].get_height() -1.2 * offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe =  [
        {'x': pipeX, 'y': -y1},                                                                                                                                     
        {'x': pipeX, 'y': y2}
    ]
    return pipe




if __name__=="__main__":
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by UZAIRSHAIKH')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/0.png.png').convert_alpha(),
        pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/1.png.png').convert_alpha(),
        pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/2.png.png').convert_alpha(),
        pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/3.png.png').convert_alpha(),
        pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/4.png.png').convert_alpha(),
        pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/5.png.png').convert_alpha(),
        pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/6.png.png').convert_alpha(),
        pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/7.png.png').convert_alpha(),
        pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/8.png.png').convert_alpha(),
        pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/9.png.png').convert_alpha(),
    )

    GAME_SPRITES['message'] = pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/message.png.jfif').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/base.png.png').convert_alpha()
    GAME_SPRITES['pipe'] = (pygame.transform.rotate(pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/pipe.png.png').convert_alpha(), 180),
    pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/pipe.png.png').convert_alpha()
    )

    GAME_SPRITES['background'] = pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/background.png.png').convert_alpha()
    GAME_SPRITES['player'] = pygame.image.load('F:\code playground\Tuts\Flappy Bird\gallery\sprites/bird.png.png').convert_alpha()

    while True:
        welcomeScreen()
        mainGame()

