import pygame
import random
from marketGameSettings import *
from pictureGame import *
from marketGame import *
from tictactoe import *
from pingpong import *
from rpsGame import *
from bugGame import *

PINGPONG = 10
PICTURE_GAME = 20
RPS_GAME = 30
TICTACTOE = 40
MARKET_GAME = 50
BUG_GAME = 60

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("호두파이")
myFont = pygame.font.Font("MaruBuri-Regular.ttf", 40)

playing = True
game_choice = 0

while playing:
    screen.fill(WHITE)
    screen.blit(pygame.image.load("images/mainBackground.png"), (0, 0))

    screen.blit(pygame.image.load("images/pingBtn.png").convert_alpha(), (80, 160))
    screen.blit(pygame.image.load("images/pictureBtn.png").convert_alpha(), (360, 160))
    screen.blit(pygame.image.load("images/rpsBtn.png").convert_alpha(), (80, 260))
    screen.blit(pygame.image.load("images/tttBtn.png").convert_alpha(), (360, 260))
    screen.blit(pygame.image.load("images/marketBtn.png").convert_alpha(), (80, 360))
    screen.blit(pygame.image.load("images/bugBtn.png").convert_alpha(), (360, 360))
    screen.blit(pygame.image.load("images/randomBtn.png").convert_alpha(), (640, 160))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if pos[0] > 80 and pos[0] < 350 and pos[1] > 160 and pos[1] < 250:
                game_choice = PINGPONG
            elif pos[0] > 360 and pos[0] < 630 and pos[1] > 160 and pos[1] < 250:
                game_choice = PICTURE_GAME
            elif pos[0] > 80 and pos[0] < 350 and pos[1] > 260 and pos[1] < 350:
                game_choice = RPS_GAME
            elif pos[0] > 360 and pos[0] < 630 and pos[1] > 260 and pos[1] < 350:
                game_choice = TICTACTOE
            elif pos[0] > 80 and pos[0] < 350 and pos[1] > 360 and pos[1] < 450:
                game_choice = MARKET_GAME
            elif pos[0] > 360 and pos[0] < 630 and pos[1] > 360 and pos[1] < 450:
                game_choice = BUG_GAME
            elif pos[0] > 640 and pos[0] < 730 and pos[1] > 160 and pos[1] < 450:
                game_choice = random.randrange(1, 7) * 10

    if game_choice == PINGPONG:
        play_pingpong()
    elif game_choice == PICTURE_GAME:
        play_picture_game()
    elif game_choice == RPS_GAME:
        play_rps_game()
    elif game_choice == TICTACTOE:
        play_tictactoe()
    elif game_choice == MARKET_GAME:
        play_market_game()
    elif game_choice == BUG_GAME:
        play_bug_game()

    game_choice = 0

    pygame.display.update()
    clock.tick(30)

pygame.quit()