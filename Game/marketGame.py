import pygame
import random
from marketGameSettings import *
from marketGameSprites import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = pygame.image.load(BACKGROUND)
        pygame.display.set_caption("호두파이 장보기 게임")
        self.clock = pygame.time.Clock()
        self.myFont = pygame.font.Font("MaruBuri-Regular.ttf", 30)
        self.playing = True
        self.stage = OPENING
        self.money = 10000 + random.randrange(0, 11) * 1000
        self.sum = 0
        self.inventory = list()
        self.puppy = Puppy(0, 300)

    def show_opening(self):
        self.explain = pygame.image.load(EXPLAIN)
        self.screen.blit(self.explain, (10, 20))

        self.start_btn = Button(530, 340)
        self.start_btn.put_img(START_BTN)
        self.screen.blit(self.start_btn.img, self.start_btn.get_position())

    def show_explain(self):
        self.explain_title = self.myFont.render("EXPLAIN", True, GREEN)

        self.text_rect = self.explain_title.get_rect()
        self.text_rect.centerx = round(SCREEN_WIDTH / 2)
        self.text_rect.y = 50

        self.screen.blit(self.explain_title, self.text_rect)
        # 게임 시작 버튼을 오프닝 화면 게임 방법 버튼의 위치에 표시
        self.screen.blit(self.start_btn.img, self.explain_btn.get_position())

    def show_play(self):
        self.done_btn = Button(280, 15)
        self.done_btn.put_img(DONE_BTN)
        self.screen.blit(self.done_btn.img, self.done_btn.get_position())

        self.exit_btn = Button(430, 15)
        self.exit_btn.put_img(EXIT_BTN)
        self.screen.blit(self.exit_btn.img, self.exit_btn.get_position())

        # 제한 시간 표시
        self.time_text = Button(610, 15)
        self.time_text.put_img(TIME_TEXT)
        self.screen.blit(self.time_text.img, self.time_text.get_position())
        self.seconds = (pygame.time.get_ticks() - self.start_time) / 1000
        self.seconds_print = self.myFont.render(str(TOTAL_TIME - int(self.seconds)).rjust(3, ' '), True, GREEN)
        if TOTAL_TIME - self.seconds <= 0:
            self.stage = CALCULATE
        self.screen.blit(self.seconds_print, (700, 24))

        # 주어진 금액 표시
        self.money_text = Button(25, 15)
        self.money_text.put_img(MONEY_TEXT)
        self.screen.blit(self.money_text.img, self.money_text.get_position())
        self.money_print = self.myFont.render(str(self.money), True, GREEN)
        self.screen.blit(self.money_print, (135, 24))

        # 캐릭터 표시
        self.puppy.put_img(PUPPY)
        self.screen.blit(self.puppy.img, self.puppy.get_position())        

        # 상품 표시
        self.product_list = list()
        # product1 : 포카리스웨트 (800원)
        self.product_list.append(Product(50, 100, 800))
        # product2 : 신라면 봉지 (800원)
        self.product_list.append(Product(150, 100, 800))
        # product3 : 짜파게티 봉지 (900원)
        self.product_list.append(Product(250, 100, 900))
        # product4 : 새우깡 (1200원)
        self.product_list.append(Product(350, 100, 1200))
        # product5 : 꼬깔콘 (1200원)
        self.product_list.append(Product(450, 100, 1200))
        # product6 : 콘푸로스트 (3100원)
        self.product_list.append(Product(550, 100, 3100))
        # product7 : 코코볼 (2800원)
        self.product_list.append(Product(650, 100, 2800))
        # product8 : 게토레이 (1500원)
        self.product_list.append(Product(50, 200, 1500))
        # product9 : 신라면 컵 (1100원)
        self.product_list.append(Product(150, 200, 1100))
        # product10 : 짜파게티 컵 (1100원)
        self.product_list.append(Product(250, 200, 1100))
        # product11 : 초코칩쿠키 (1600원)
        self.product_list.append(Product(350, 200, 1600))
        # product12 : 초코파이 (2500원)
        self.product_list.append(Product(450, 200, 2500))
        # product13 : 마이구미 (500원)
        self.product_list.append(Product(550, 200, 500))
        # product14 : 후라보노 (400원)
        self.product_list.append(Product(650, 200, 400))
        
        i = 0
        for product in self.product_list:
            product.put_img(PRODUCT_IMG[i])
            product.put_in_img(PRODUCT_IN_IMG[i])
            self.screen.blit(product.img, product.get_position())
            i = i + 1

        # 인벤토리에 들어 있는 상품 표시
        i = 0
        for product_in in self.inventory:
            self.screen.blit(product_in.in_img, (30 * i, 440))
            i = i + 1

    def show_calculate(self):
        if self.inventory.__len__() > 0:
            self.calculate_text = Button(200, 420)
            self.calculate_text.put_img(CALCULATE_TEXT)
            self.screen.blit(self.calculate_text.img, self.calculate_text.get_position())
        else:
            self.check_btn = Button(320, 420)
            self.check_btn.put_img(CHECK_BTN)
            self.screen.blit(self.check_btn.img, self.check_btn.get_position())
        
        self.screen.blit(self.money_text.img, self.money_text.get_position())
        self.screen.blit(self.money_print, (135, 24))
        
        self.price_text = Button(510, 15)
        self.price_text.put_img(PRICE_TEXT)
        self.screen.blit(self.price_text.img, self.price_text.get_position())

        self.sum_print = self.myFont.render(str(self.sum).rjust(5, ' '), True, GREEN)
        self.screen.blit(self.sum_print, (670, 24))

        # 인벤토리에 들어 있는 상품 표시
        i = 0
        for product_in in self.inventory:
            self.screen.blit(product_in.img, (50 + 100 * (i % 7), 100 + 100 * int(i / 7)))
            i = i + 1
                
    def show_ending(self):
        # 성공 시 엔딩
        if self.money == self.sum:
            self.ending = pygame.image.load(WIN)
        # 실패 시 엔딩
        else:
            self.ending = pygame.image.load(LOSE)  
        self.screen.blit(self.ending, (200, 100))

        self.back_btn = Button(175, 350)
        self.back_btn.put_img(BACK_BTN)
        self.screen.blit(self.back_btn.img, self.back_btn.get_position())

        self.replay_btn = Button(425, 350)
        self.replay_btn.put_img(REPLAY_BTN)
        self.screen.blit(self.replay_btn.img, self.replay_btn.get_position())

    def draw(self):
        self.screen.blit(self.background, (0, 0))

    def opening_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # 오프닝에서 게임 시작 선택
                if self.stage == OPENING and pos[0] > self.start_btn.x and pos[1] > self.start_btn.y and pos[0] < self.start_btn.x + self.start_btn.sx and pos[1] < self.start_btn.y + self.start_btn.sy:
                    self.stage = PLAY
                    self.start_time = pygame.time.get_ticks()
    
    def play_event(self):    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # 상품 선택
                lastIndex = len(self.product_list) - 1
                if pos[0] > self.product_list[0].x and pos[1] > self.product_list[0].y and pos[0] < self.product_list[lastIndex].x + self.product_list[lastIndex].sx and pos[1] < self.product_list[lastIndex].y + self.product_list[lastIndex].sy:
                    index = int((pos[0] - 50) / 100) + int((pos[1] - 100) / 100) * 7
                    self.inventory.append(self.product_list[index])
                # 상품 선택 취소
                elif pos[1] > 440:
                    index = int(pos[0] / 30)
                    if index >= 0 and index < self.inventory.__len__():
                        del self.inventory[index]
                # 상품 선택 완료
                elif pos[0] > self.done_btn.x and pos[1] > self.done_btn.y and pos[0] < self.done_btn.x + self.done_btn.sx and pos[1] < self.done_btn.y + self.done_btn.sy:
                    self.stage = CALCULATE
                # 종료 버튼 선택
                elif pos[0] > self.exit_btn.x and pos[1] > self.exit_btn.y and pos[0] < self.exit_btn.x + self.exit_btn.sx and pos[1] < self.exit_btn.y + self.exit_btn.sy:
                    self.playing = False
                self.puppy.set_position(pos[0], self.puppy.y)

    def calculate_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                # 엔딩으로 이동
                if self.inventory.__len__() == 0 and pos[0] > self.check_btn.x and pos[1] > self.check_btn.y and pos[0] < self.check_btn.x + self.check_btn.sx and pos[1] < self.check_btn.y + self.check_btn.sy:
                    self.stage = ENDING
                # 화면을 터치하면 인벤토리 내의 상품이 하나씩 계산됨
                elif self.inventory.__len__() > 0:
                    self.sum = self.sum + self.inventory.pop().price

    def ending_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] > self.back_btn.x and pos[1] > self.back_btn.y and pos[0] < self.back_btn.x + self.back_btn.sx and pos[1] < self.back_btn.y + self.back_btn.sy:
                    self.playing = False
                elif pos[0] > self.replay_btn.x and pos[1] > self.replay_btn.y and pos[0] < self.replay_btn.x + self.replay_btn.sx and pos[1] < self.replay_btn.y + self.replay_btn.sy:
                    play_market_game()
    def update(self):
        pygame.display.flip()
        self.clock.tick(60)

def play_market_game():
    game = Game()
    while game.playing:
        game.draw()
        if game.stage == OPENING:
            game.show_opening()
        if game.stage == PLAY:
            game.show_play()
            game.play_event()
        if game.stage == CALCULATE:
            game.show_calculate()
            game.calculate_event()
        if game.stage == ENDING:
            game.show_ending()
            game.ending_event()
        game.opening_event()
        game.update()
    return
