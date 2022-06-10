import random, pygame, sys
from typing import Sequence
from pygame.locals import *

FPS = 30 #초당 프레임, 프로그램의 일반속도
WINDOWWIDTH = 600 #윈도우의 너비(픽셀단위)
WINDOWHEIGHT = 480 #윈도우의 높이(픽셀단위)
REVEALSPEED = 5 #상자가 보였다가 가려지는 속도
BOXSIZE = 40 #상자의 너비와 높이(픽셀단위)
GAPSIZE = 10 # 상자 사이의 간격(픽셀단위)
BOARDWIDTH = 4 # 아이콘 가로줄 수
BOARDHEIGHT = 4 # 아이콘 세로줄 수
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number oqf boxes for pairs of matches.'
XMARGIN = int((WINDOWWIDTH -  (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
reset_img = pygame.image.load('images/pictureImages/reset.png').convert_alpha()
showAgain_img = pygame.image.load('images/pictureImages/showAgain.png').convert_alpha()
success_img = pygame.image.load('images/pictureImages/success.jpg')
success_img = pygame.transform.scale(success_img, (WINDOWWIDTH, WINDOWHEIGHT))
manual_img = pygame.image.load('images/pictureImages/manual.PNG')
manual_img = pygame.transform.scale(manual_img, (WINDOWWIDTH, WINDOWHEIGHT))

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
transparent = (0, 0, 0, 0)

BGCOLOR = BLACK
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
#assert 문은 asser 키워드, 표현식, 표현식이 false일 때 크러쉬 일으키면서 마지막 부분을 출력
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, "Board is too big for the number of shapes/colors defined."

class Button() :
    def __init__(self, x, y, image, scale) :
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False
    
    def draw(self) : #버튼과 텍스트 출력
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos) :
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        if pygame.mouse.get_pressed()[0] == 0 :
            self.clicked = False

        DISPLAYSURF.blit(self.image, (self.rect.x, self.rect.y))

        return action

def play_picture_game():
    global FPSCLOCK, DISPLAYSURF #전역변수 설정
    pygame.init()
    FPSCLOCK = pygame.time.Clock()

    reset_button = Button(10, 20, reset_img, 0.8)
    showAgain_button = Button(100, 20, showAgain_img, 0.8)

    mousex = 0 #마우스 이벤트 발생 시 x좌표
    mousey = 0 #마우스 이벤트 발생 시 y좌표
    pygame.display.set_caption('호두파이 그림 짝맞추기')

    mainBoard = getRandomizedBoard() #게임판의 상태를 나타내는 함수
    revealedBoxes = generateRevealedBoxesData(False) #false를 전달하면
    # false면 닫힌 상태 true면 상자가 열린 상태
    # 이 함수가 반환할 값은 2차원 리스트

    firstSelection = None #첫 번째 상자를 클릭했을 때 (x, y)를 저장
    #프로그램은 이 값을 보고 두 번째 아이콘을 찾는 클릭인지 아닌지 알아낸다

    DISPLAYSURF.fill(BGCOLOR)

    DISPLAYSURF.blit(manual_img, (0, 0))
    pygame.display.update()
    pygame.time.wait(5000)

    DISPLAYSURF.fill(BGCOLOR)

    #reset Button이 눌렸을때 다시 시작
    if reset_button.draw() == True:
        #게임판 재설정
        showAgain_button.draw()
        mainBoard = getRandomizedBoard()
        revealedBoxes = generateRevealedBoxesData(False)
        #잠시 동안 게임판의 박스 열어서 보여준다
        drawBoard(mainBoard, revealedBoxes)
        pygame.display.update()
        pygame.time.wait(1000)
        #게임 시작 에니메이션 보여주기
        startGameAnimation(mainBoard)
        firstSelection = None #firstSelection 변수 리셋
        #화면을 다시 그린 다음 시간 지연을 기다린다
        pygame.display.update()
        FPSCLOCK.tick(FPS)

    #showAgain Button이 눌렸을때 다시 보여주기
    if showAgain_button.draw() == True:
        startGameAnimation(mainBoard)

    startGameAnimation(mainBoard) #미리보여주기 함수

    while True: #게임 루프
        mouseClicked = False #아직 그림 클릭을 안했으니 false

        DISPLAYSURF.fill(BGCOLOR) #윈도우를 그린다
        drawBoard(mainBoard, revealedBoxes)

        for event in pygame.event.get(): #이벤트 처리 루프
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION: #마우스 움직이면 커서 위치 저장
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True #클릭했으니 true 저장

        boxx, boxy = getBoxAtPixel(mousex, mousey)

        #reset Button이 눌렸을때 다시 시작
        if reset_button.draw() == True:
            #게임판 재설정
            showAgain_button.draw()
            mainBoard = getRandomizedBoard()
            revealedBoxes = generateRevealedBoxesData(False)
            #잠시 동안 게임판의 박스 열어서 보여준다
            drawBoard(mainBoard, revealedBoxes)
            pygame.display.update()
            pygame.time.wait(1000)
            #게임 시작 에니메이션 보여주기
            startGameAnimation(mainBoard)
            firstSelection = None #firstSelection 변수 리셋
            #화면을 다시 그린 다음 시간 지연을 기다린다
            pygame.display.update()
            FPSCLOCK.tick(FPS)
        
        if showAgain_button.draw() == True:
            startGameAnimation(mainBoard)

        if boxx != None and boxy != None:
            #마우스가 현재 박스 위에 있다
            if not revealedBoxes[boxx][boxy]: #false라면 박스가 닫혀있다
                drawHighlightBox(boxx, boxy) #박스 테두리 그리기
            if not revealedBoxes[boxx][boxy] and mouseClicked: #박스를 클릭했을때
                revealBoxesAnimation(mainBoard, [(boxx, boxy)]) #박스가 열리는 애니메이션 실행
                revealedBoxes[boxx][boxy] = True #박스를 보이는 것으로 설정
                if firstSelection == None: #현재의 박스가 처음 클릭한 박스
                    firstSelection = (boxx, boxy)
                else: #현재의 박스가 두 번째 클릭한 박스라면
                    #두 아이콘이 서로 맞는 짝인지 검사한다
                    icon1shape, icon1color = getShapeAndColor(mainBoard, firstSelection[0], firstSelection[1])
                    icon2shape, icon2color = getShapeAndColor(mainBoard, boxx, boxy)
                    #getShapeAndClolr는 그 위치에 있는 아이콘의 색과 형태 알아낸다

                    if icon1shape != icon2shape or icon1color != icon2color:
                        #아이콘이 맞지 않다면 두 박스 모두 덮기
                        pygame.time.wait(1000) # 1초 기다리기
                        coverBoxesAnimation(mainBoard, [(firstSelection[0], firstSelection[1]), (boxx, boxy)])
                        revealedBoxes[firstSelection[0]][firstSelection[1]] = False #박스 닫기
                        revealedBoxes[boxx][boxy] = False
                    elif hasWon(revealedBoxes): #모든 박스가 열렸는지 확인
                        gameWonAnimation(mainBoard) #게임 끝난 애니메이션
                        # DISPLAYSURF.blit(success_img, (0, 0))
                        # pygame.display.update()
                        # FPSCLOCK.tick(FPS)

                        # #게임판 재설정
                        # mainBoard = getRandomizedBoard()
                        # revealedBoxes = generateRevealedBoxesData(False)

                        # #잠시 동안 게임판의 박스 열어서 보여준다
                        # drawBoard(mainBoard, revealedBoxes)
                        # pygame.display.update()
                        # pygame.time.wait(1000)

                        # #게임 시작 에니메이션 보여주기
                        # startGameAnimation(mainBoard)
                    firstSelection = None #firstSelection 변수 리셋

        #화면을 다시 그린 다음 시간 지연을 기다린다
        pygame.display.update()
        FPSCLOCK.tick(FPS)

#열린 박스에 대한 데이터 구조 만들기
def generateRevealedBoxesData(val): #구성 요소의 값을 val
    revealedBoxes = []
    for i in range(BOARDWIDTH):
        revealedBoxes.append([val] * BOARDHEIGHT) #불리언 값을 갖는 2차원 리스트
    return revealedBoxes #revealBoxes[x][y]가 된다

#모든 가능한 색에서 가능한 모양의 목록을 모두 얻어내기
def getRandomizedBoard():
    icons = []
    for color in ALLCOLORS:
        for shape in ALLSHAPES:
            icons.append( (shape, color) )

    random.shuffle(icons) #아이콘 리스트의 순서를 랜덤으로 한다
    numIconsUsed = int(BOARDWIDTH * BOARDHEIGHT / 2) # 얼마나 많은 아이콘이 필요한지 계산
    icons = icons[:numIconsUsed] * 2 #각각의 짝 만들기
    random.shuffle(icons)
    #아이콘이 2개씩 있어야 하므로 곱한 값을 2로 나눈 값을 numIconUsed에 저장
    #icons를 numIconUsed만큼 잘라내여 새로운 리스트를 * 2 해서 두개로 만든다
    #shuffle 사용해서 섞기

    #랜덤하게 아이콘이 놓여 있는 게임판의 데이터 구조를 만든다
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):  
            column.append(icons[0])
            del icons[0] #방금 추가한 아이콘을 지운다
        board.append(column)
    return board
    #icons list에 있는 값들을 column에 넣고 icons 지워가며 icons[0]에 새로운 값 넣기
    #길이가 짧아진다


def splitIntoGroupsOf(groupSize, theList):
    #리스트를 2차원 리스트로 만든다 
    #안쪽의 리스트는 최대로 groupsize개 만큼의 아이템이 있다
    result = []
    for i in range(0, len(theList), groupSize):
        result.append(theList[i:i + groupSize])
    return result


#게임판 좌표계를 픽셀 좌표계로 변환한다
#카드마다 좌표를 새로 줘서 더 좌표를 쉽게 찾는다
def leftTopCoordsOfBox(boxx, boxy):
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


#픽셀 좌표계에서 게임판 좌표계로 변환하기
def getBoxAtPixel(x, y):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


#그리기 함수에서는 대부분 박스의 중간위치와 1/4위치를 필요 하는 경우가 많아서 미리 정의 
def drawIcon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25) # syntactic sugar
    half =    int(BOXSIZE * 0.5)  # syntactic sugar

    left, top = leftTopCoordsOfBox(boxx, boxy) #보드의 좌표에서 픽셀 좌표 얻기
    #형태를 그린다
    if shape == DONUT:
        pygame.draw.circle(DISPLAYSURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAYSURF, BGCOLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAYSURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAYSURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAYSURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAYSURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAYSURF, color, (left, top + quarter, BOXSIZE, half))


def getShapeAndColor(board, boxx, boxy):
    #x, y 위치의 아이콘 형태의 값은 board[x][y][0]
    #x, y 위치의 아이콘 색의 값은 board[x][y][1]
    return board[boxx][boxy][0], board[boxx][boxy][1]


def drawBoxCovers(board, boxes, coverage):
    #닫히거나 열린 상태의 박스 그리기
    #박스는 아이템 2개짜리 리스트이며 박스의 x, y 위치를 갖는다
    for box in boxes:
        left, top = leftTopCoordsOfBox(box[0], box[1])
        pygame.draw.rect(DISPLAYSURF, BGCOLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = getShapeAndColor(board, box[0], box[1])
        drawIcon(shape, color, box[0], box[1])
        if coverage > 0: #닫힌 상태면 덮개만 그리기
            pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def revealBoxesAnimation(board, boxesToReveal):
    #박스가 열리는 애니메이션 수행
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        drawBoxCovers(board, boxesToReveal, coverage)


def coverBoxesAnimation(board, boxesToCover):
    #박스가 닫히는 애니메이션 수행
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        drawBoxCovers(board, boxesToCover, coverage)


def startRevealBoxesAnimation(board, boxesToReveal):
    #맨 처음에 박스가 열리는 애니메이션 수행
    for coverage in range(BOXSIZE, (-1) - 1, -1):
        drawBoxCovers(board, boxesToReveal, coverage)


def startCoverBoxesAnimation(board, boxesToCover):
    #맨 처음에 박스가 닫히는 애니메이션 수행
    for coverage in range(0, BOXSIZE + 1, 1):
        drawBoxCovers(board, boxesToCover, coverage)


def drawBoard(board, revealed):
    #모든 박스를 상태에 맞게 그리기
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if not revealed[boxx][boxy]:
                #닫힌 박스를 그린다
                pygame.draw.rect(DISPLAYSURF, BOXCOLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                #열린 박스, 즉 아이콘을 그린다
                shape, color = getShapeAndColor(board, boxx, boxy)
                drawIcon(shape, color, boxx, boxy)


def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 5, top - 5, BOXSIZE + 10, BOXSIZE + 10), 4)


def startGameAnimation(board):
    #박스 열어서 보여준다
    coveredBoxes = generateRevealedBoxesData(False)
    boxes = []
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            boxes.append( (x, y) )
    random.shuffle(boxes)
    boxGroups = splitIntoGroupsOf(16, boxes)

    drawBoard(board, coveredBoxes)
    for boxGroup in boxGroups:
        startRevealBoxesAnimation(board, boxGroup)
        startCoverBoxesAnimation(board, boxGroup)


def gameWonAnimation(board):
    #  플레이어가 승리하면 배경색 깜빡이기
    #  -> 이미지 넣는 것으로 변경 
    coveredBoxes = generateRevealedBoxesData(True)
    DISPLAYSURF.blit(success_img, (0, 0))
    # drawBoard(board, coveredBoxes)
    # pygame.time.wait(5000)
    pygame.display.update()
    pygame.time.wait(3000)
    pygame.display.update()

    
    # color1 = LIGHTBGCOLOR
    # color2 = BGCOLOR

    # for i in range(13):
    #      color1, color2 = color2, color1 #배경색을 변경한다
    #      DISPLAYSURF.fill(color1)
    #      drawBoard(board, coveredBoxes)
    #      pygame.display.update()
    #      pygame.time.wait(300)


def hasWon(revealedBoxes):
    #모든 박스를 열었으면 true, 아니면 false
    for i in revealedBoxes:
        if False in i:
            return False #닫힌 박스가 있으면 false
    return True


#def showAgainAnimation(board, revealedBoxes):
    #for i in revealedBoxes:
        #if False in i:  #닫힌 박스가 있으면 false
            #print(i)
    #revealBoxesAnimation(board, targetBoxes)
    #startGameAnimation(board)

#메인 함수 사용
# if __name__ == '__main__':
#     play_picture_game()