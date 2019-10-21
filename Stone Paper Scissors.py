import os
import pygame
from pygame.locals import *
from random import randint

WIDTH = 650
HEIGHT = 500

# COLORS
COLORS = {
    'BACKGROUND_COLOR': (255, 255, 0),
    'TEXT_COLOR': (0, 0, 0),
    'RED': (255, 0, 0),
    'YELLOW': (255, 255, 0),
    'BLUE': (0, 0, 200),
    'GREEN': (0, 255, 0),
    'BLACK': (0, 0, 0)
}


def getTextLength(text, size=30):
    font = pygame.font.SysFont("comicsansms", size)
    label = font.render(text, 1, (0, 0, 0))
    return label.get_rect()[2]


def displayText(text, pos, size=30, color=COLORS['TEXT_COLOR'], is_centered=False):
    """displays text on the screen

    Args:
        text (string): text to displat
        pos (tuple): pos of text to display
        size (int, optional): size of font. Defaults to 30.
        color (tuple, optional): color of font. Defaults to COLORS['TEXT_COLOR'].

    Returns:
        None
    """
    myFont = pygame.font.SysFont('Comic Sans MS', size)
    textsurface = myFont.render(text, False, color)

    x, y = pos

    if is_centered:
        x = (WIDTH-getTextLength(text, size))//2

    win.blit(textsurface, (x, y))


def welcomeScreen():
    """displays welcome screen on the screen
    """

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == KEYDOWN and event.key == K_RETURN:  # start game
                return
            else:
                win.fill(COLORS['BACKGROUND_COLOR'])
                displayText("Stone Paper Scissors",
                            (0, HEIGHT*0.4), 50, is_centered=True)
                pygame.display.update()


def getComputerTurn():
    x = randint(0, 2)
    return images[x]


def redrawGameWindow(player_turn, computer_turn, reset):

    win.fill(COLORS['BACKGROUND_COLOR'])
    displayText("STONE PAPER SCISSORS", (0, HEIGHT*0.01), 50, is_centered=True)

    displayText("SCORE : "+str(SCORES['computer']),
                (WIDTH*0.1, HEIGHT*0.2), color=COLORS['RED'])
    displayText("SCORE : "+str(SCORES['player']),
                (WIDTH*0.65, HEIGHT*0.2), color=COLORS['RED'])

    displayText("COMPUTER", (WIDTH*0.1, HEIGHT*0.85))
    displayText("PLAYER", (WIDTH*0.7, HEIGHT*0.85))

    displayText("Press 'R' to restart",
                (0, HEIGHT*0.92), 20, is_centered=True, color=COLORS['RED'])

    createPlayerButtons()

    if not reset:
        if player_turn != '' and computer_turn != '':
            win.blit(IMAGES[player_turn], (WIDTH*0.65, HEIGHT*0.33))
            win.blit(IMAGES[computer_turn], (WIDTH*0.1, HEIGHT*0.33))

            wins = getWinner(player_turn, computer_turn)
            if wins == None:
                wins = 'draw'
            displayText(wins.upper(), (0, HEIGHT*0.42),
                        is_centered=True, color=COLORS['BLUE'])
            if wins != 'draw':
                displayText("WINS", (0, HEIGHT*0.42+30),
                            is_centered=True, color=COLORS['BLUE'])

    pygame.display.update()


def createPlayerButtons():
    for x in range(0, 3):
        win.blit(pygame.transform.scale(
            IMAGES[images[x]], (player_size, player_size)), (PLAYER_BUTTONS[images[x]]['x'], PLAYER_BUTTONS[images[x]]['y']))


def getWinner(player_turn, computer_turn):
    if player_turn == 'rock':
        if computer_turn == 'rock':
            return None
        elif computer_turn == 'paper':
            return 'computer'
        elif computer_turn == 'scissors':
            return 'player'
    elif player_turn == 'paper':
        if computer_turn == 'rock':
            return 'player'
        elif computer_turn == 'paper':
            return None
        elif computer_turn == 'scissors':
            return 'computer'
    elif player_turn == 'scissors':
        if computer_turn == 'rock':
            return 'computer'
        elif computer_turn == 'paper':
            return 'player'
        elif computer_turn == 'scissors':
            return None


def mainGame():
    computer_turn = ''
    player_turn = ''
    reset = False

    while True:
        redrawGameWindow(player_turn, computer_turn, reset)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN and event.key == K_r:
                SCORES['computer'] = 0
                SCORES['player'] = 0
                reset = True
                # TODO: reset here

            if event.type == pygame.MOUSEBUTTONUP:
                mouseX = pygame.mouse.get_pos()[0]
                mouseY = pygame.mouse.get_pos()[1]
                for i in images:
                    playerX = PLAYER_BUTTONS[i]['x']
                    playerY = PLAYER_BUTTONS[i]['y']
                    if playerX < mouseX < playerX+player_size and playerY < mouseY < playerY+player_size:
                        reset = False
                        player_turn = i
                        computer_turn = getComputerTurn()
                        winner = getWinner(player_turn, computer_turn)
                        if winner != None:
                            SCORES[winner] += 1


if __name__ == "__main__":
    pygame.init()

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Stone Paper Scissors")

    DIR = os.path.dirname(__file__)

    X = 0
    PLAYER_BUTTONS = {}
    player_size = 70

    # loading images
    IMAGES = {
        'rock': pygame.image.load(DIR+"\\assets\\Rock.png").convert_alpha(),
        'paper': pygame.image.load(DIR+"\\assets\\Paper.png").convert_alpha(),
        'scissors': pygame.image.load(DIR+"\\assets\\Scissors.png").convert_alpha()
    }

    images = ['rock', 'paper', 'scissors']

    for i in images:
        PLAYER_BUTTONS[i] = {}
        PLAYER_BUTTONS[i]['x'] = WIDTH*0.59+X
        PLAYER_BUTTONS[i]['y'] = HEIGHT*0.67
        X += 75

    SCORES = {
        'computer': 0,
        'player': 0
    }
    while True:
        welcomeScreen()
        mainGame()
