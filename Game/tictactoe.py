import pygame
import sys
import time
from pygame.locals import *

mainmenu_background = pygame.image.load('images/tictactoeImages/explain.png')
mainmenu_start = pygame.image.load('images/tictactoeImages/start.png')

# Create the constants (go ahead and experiment with different values)
gridWIDTH = 3  # number of columns in the grid
gridHEIGHT = 3 # number of rows in the grid
TILESIZE = 101
WINDOWWIDTH = 800
WINDOWHEIGHT = 480
FPS = 30
BLANK = None
screen = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
clock = pygame.time.Clock()
go = False
#                 R    G    B
BLACK =         (  0,   0,   0)
WHITE =         (255, 255, 255)
LBLUE =         (153, 204, 255)
LPUR =          (204, 153, 255)
#배경색 밝기 조절할것
BGCOLOR = LBLUE
TILECOLOR = WHITE
TEXTCOLOR = BLACK
BORDERCOLOR = BLACK
BASICFONTSIZE = 30

BUTTONCOLOR = LPUR
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = BLACK

BLANK = 10
PLAYER_O = 11
PLAYER_X = 21

PLAYER_O_WIN = PLAYER_O * 3
PLAYER_X_WIN = PLAYER_X * 3

CONT_GAME         = 10
DRAW_GAME         = 20
QUIT_GAME         = 30

XMARGIN = int((WINDOWWIDTH - (TILESIZE * gridWIDTH + (gridWIDTH - 1))) / 2)
YMARGIN = int((WINDOWHEIGHT - (TILESIZE * gridHEIGHT + (gridHEIGHT - 1))) / 2)

choice = 0

def check_win_game(grid):
    def check_draw_game():
        return sum(grid)%10 == 9
    def check_horizontal(player):
        for i in [0, 3, 6]:
            if sum(grid[i:i+3]) == 3 * player:
                return player
    def check_vertical(player):
        for i in range(3):
            if sum(grid[i::3]) == 3 * player:
                return player
    def check_diagonals(player):
        if (sum(grid[0::4]) == 3 * player) or (sum(grid[2:7:2]) == 3 * player):
            return player
    for player in [PLAYER_X, PLAYER_O]:
        if any([check_horizontal(player), check_vertical(player), check_diagonals(player)]):
            return player
    return DRAW_GAME if check_draw_game() else CONT_GAME

def unit_score(winner, depth):
    if winner == DRAW_GAME:
        return 0
    else:
        return 10 - depth if winner == PLAYER_X else depth - 10

def get_available_step(grid):
    return [i for i in range(9) if grid[i] == BLANK]

def minmax(grid, depth):
    global choice
    result = check_win_game(grid)
    if result != CONT_GAME:
        return unit_score(result, depth)
    depth += 1
    scores = []
    steps = []
    for step in get_available_step(grid):
        score = minmax(update_state(grid, step, depth), depth)
        scores.append(score)
        steps.append(step)
    if depth % 2 == 1:
        max_value_index = scores.index(max(scores))
        choice = steps[max_value_index]
        return max(scores)
    else:
        min_value_index = scores.index(min(scores))
        choice = steps[min_value_index]
        return min(scores)

def update_state(grid, step, depth):
    grid = list(grid)
    grid[step] = PLAYER_X if depth % 2 else PLAYER_O
    return grid

def update_grid(grid, step, player):
    grid[step] = player

def change_to_player(player):
    if player == PLAYER_O:
        return 'O'
    elif player == PLAYER_X:
        return 'X'
    elif player == BLANK:
        return '-'

def drawgrid(grid, message):
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)
    for tilex in range(3):
        for tiley in range(3):
            if grid[tilex*3+tiley] != BLANK:
                drawTile(tilex, tiley, grid[tilex*3+tiley])
    left, top = getLeftTopOfTile(0, 0)
    width = gridWIDTH * TILESIZE
    height = gridHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5, top - 5, width + 11, height + 11), 4)
    for column_index in range(gridWIDTH):
                    for row_index in range(gridHEIGHT):
                        pygame.draw.rect(screen, BLACK, pygame.Rect(247 + column_index *TILESIZE, 87 + row_index *TILESIZE, TILESIZE, TILESIZE), 1)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(NEW_SURF2, NEW_RECT2)
    DISPLAYSURF.blit(NEW_SURF3, NEW_RECT3)

def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)

def makeText(text, color, bgcolor, top, left):
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)

def drawTile(tilex, tiley, symbol, adjx=0, adjy=0):
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(DISPLAYSURF, TILECOLOR, (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(symbol_to_str(symbol), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)

def symbol_to_str(symbol):
    if symbol == PLAYER_O:
        return 'O'
    elif symbol == PLAYER_X:
        return 'X'

def getSpotClicked(x, y):
    for tileX in range(3):
        for tileY in range(3):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return None

def grid_to_step(spotx, spoty):
    return spotx * 3 + spoty

def check_move_legal(coords, grid):
    step = grid_to_step(*coords)
    return grid[step] == BLANK

class Button:
    def __init__(self, img_in, x, y, action=None):
        mouse = pygame.mouse.get_pos()  #마우스 좌표
        click = pygame.mouse.get_pressed()  #클릭여부
        if mouse[0] > 600 and mouse[0] < 702 and mouse[1] > 150 and mouse[1] < 204 and click[0]:  # 마우스가 버튼안에서 클릭되었을 때
            time.sleep(0.2)
            action()
        else:
            screen.blit(img_in, (x, y))

def play_tictactoe():
    menu = True
    while menu:
        global go
        screen.blit(mainmenu_background, (0, 0))
        Button(mainmenu_start, 600, 150, game)   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()   
        if go == True:
            go = False
            break
        pygame.display.update()
        clock.tick(15)

def game():
    global go, FPSCLOCK, DISPLAYSURF, BASICFONT, NEW_SURF, NEW_RECT, NEW_SURF2, NEW_RECT2, NEW_SURF3, NEW_RECT3
    two_player = False #by default false
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('호두파이 틱택토')
    BASICFONT = pygame.font.Font('MaruBuri-Regular.ttf', BASICFONTSIZE)
    NEW_SURF, NEW_RECT = makeText('1인용 다시하기', BLACK, WHITE, WINDOWWIDTH - 210, WINDOWHEIGHT - 60)
    NEW_SURF2, NEW_RECT2 = makeText('2인용 다시하기', BLACK, WHITE, WINDOWWIDTH - 210, WINDOWHEIGHT - 120)
    NEW_SURF3, NEW_RECT3 = makeText('돌아가기', TEXTCOLOR, TILECOLOR, WINDOWWIDTH - 210, WINDOWHEIGHT - 180)
    image = pygame.image.load('images/tictactoeImages/win.jpg')
    imagee = pygame.image.load('images/tictactoeImages/lose.jpg')
    grid = [BLANK] * 9
    game_over = False
    x_turn = True
    msg = "친구와, 또는 컴퓨터와 즐기는 틱택토"
    drawgrid(grid, msg)
    pygame.display.update()
    while True:
        coords = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONUP:
                coords = getSpotClicked(event.pos[0], event.pos[1])
                if not coords and NEW_RECT.collidepoint(event.pos):
                    grid = [BLANK] * 9
                    game_over = False
                    msg = "컴퓨터와 즐기는 틱택토"
                    drawgrid(grid, msg)
                    pygame.display.update()
                    two_player = False
                if not coords and NEW_RECT2.collidepoint(event.pos):
                    grid = [BLANK] * 9
                    game_over = False
                    msg = "친구와 즐기는 틱택토"
                    drawgrid(grid, msg)
                    pygame.display.update()
                    two_player = True
                if not coords and NEW_RECT3.collidepoint(event.pos):
                    go = True
        if go == True:
            break
        if coords and check_move_legal(coords, grid) and not game_over:
            if two_player:
                next_step = grid_to_step(*coords)
                if x_turn:
                    update_grid(grid, next_step, PLAYER_X)
                    x_turn = False
                else:
                    update_grid(grid, next_step, PLAYER_O)
                    x_turn = True
                drawgrid(grid, msg)
                pygame.display.update()
                result = check_win_game(grid)
                game_over = (result != CONT_GAME)
                drawgrid(grid, msg)
                if result == PLAYER_X:
                    pygame.time.delay(2000)
                    msg = "X가 이겼어요!"
                    drawgrid(grid, msg)
                    DISPLAYSURF.blit(image,(248,88))
                elif result == PLAYER_O:
                    pygame.time.delay(2000)
                    msg = "O이 이겼어요!"
                    drawgrid(grid, msg)
                    DISPLAYSURF.blit(image,(248,88))
                elif result == DRAW_GAME:
                    pygame.time.delay(2000)
                    msg = "무승부에요"
                    drawgrid(grid, msg)
                pygame.display.update()
            if not two_player:
                next_step = grid_to_step(*coords)
                update_grid(grid, next_step, PLAYER_X)
                drawgrid(grid, msg)
                pygame.display.update()
                minmax(grid, 0)
                update_grid(grid, choice, PLAYER_O)
                result = check_win_game(grid)
                game_over = (result != CONT_GAME)
                drawgrid(grid, msg)
                if result == PLAYER_X:
                    pygame.time.delay(2000)
                    msg = "X가 이겼어요!"
                    drawgrid(grid, msg)
                    DISPLAYSURF.blit(image,(248,88))
                elif result == PLAYER_O:
                    pygame.time.delay(2000)
                    msg = "졌습니다ㅜㅜ"
                    drawgrid(grid, msg)
                    DISPLAYSURF.blit(imagee,(248,88))
                elif result == DRAW_GAME:
                    pygame.time.delay(2000)
                    msg = "무승부에요"
                    drawgrid(grid, msg)
                pygame.display.update()

if __name__ == '__main__':
    play_tictactoe()
