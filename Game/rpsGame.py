import random
import pygame

class Button():
    def __init__(self, x, y, pos, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.pos = pos

    def clicked(self, pos):
        self.pos = pygame.mouse.get_pos()
        if self.pos[0] > self.x and self.pos[0] < self.x + self.width:
            if self.pos[1] > self.y and self.pos[1] < self.y + self.height:
                return True
        return False


class RpsGame():
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 480))
        pygame.display.set_caption("호두파이 가위바위보")

        self.bg = pygame.image.load("images/rpsImages/background.png")
        self.win = pygame.image.load("images/rpsImages/win.jpg")
        self.lose = pygame.image.load("images/rpsImages/lose.jpg")
        self.r_btn = pygame.image.load("images/rpsImages/r_button.png").convert_alpha()
        self.p_btn = pygame.image.load("images/rpsImages/p_button.png").convert_alpha()
        self.s_btn = pygame.image.load("images/rpsImages/s_button.png").convert_alpha()
        self.start_btn = pygame.image.load("images/rpsImages/start_btn.png").convert_alpha()
        self.start = pygame.image.load("images/rpsImages/start.png")
        self.main = pygame.image.load("images/rpsImages/main_button.png").convert_alpha()
        self.retry = pygame.image.load("images/rpsImages/retry_button.png").convert_alpha()

        self.choose_rock = pygame.image.load("images/rpsImages/rock.png").convert_alpha()
        self.choose_paper = pygame.image.load("images/rpsImages/paper.png").convert_alpha()
        self.choose_scissors = pygame.image.load("images/rpsImages/scissors.png").convert_alpha()

        self.screen.blit(self.start, (0, 0))
        self.screen.blit(self.start_btn, (150, 280))
        #self.screen.blit(self.bg, (0, 0))
        #self.screen.blit(self.r_btn, (330, 500))
        #self.screen.blit(self.p_btn, (640, 500))
        #self.screen.blit(self.s_btn, (20, 500))

        self.start_btn = Button(150, 280, (150, 280), 150, 60)
        self.rock_btn = Button(280, 380, (280, 380), 220, 88)
        self.paper_btn = Button(540, 380, (540, 380), 220, 88)
        self.scissors_btn = Button(30, 380, (30, 380), 220, 88)
        self.main_btn = Button(30, 0, (30, 0), 220, 88)
        self.retry_btn = Button(540, 0, (540, 0), 220, 88)

        self.font = pygame.font.Font(('Splatch.ttf'), 80)
        self.text = self.font.render(f" ", True, (0, 0, 0))

        self.pl_score = 0
        self.pc_score = 0

    def player(self):
        if self.rock_btn.clicked(280):
            self.p_option = "rock"
            self.screen.blit(self.choose_rock, (100, 140))
        elif self.paper_btn.clicked(540):
            self.p_option = "paper"
            self.screen.blit(self.choose_paper, (100, 140))
        else:
            self.scissors_btn.clicked(30)
            self.p_option = "scissors"
            self.screen.blit(self.choose_scissors, (100, 140))

        return self.p_option

    def computer(self):
        self.pc_random_choice = " "
        option = ["rock", "paper", "scissors"]
        pc_choice = random.choice(list(option))
        if pc_choice == "rock":
            self.pc_random_choice = "rock"
            self.screen.blit(self.choose_rock, (480, 140))
        elif pc_choice == "paper":
            self.pc_random_choice = "paper"
            self.screen.blit(self.choose_paper, (480, 140))
        else:
            self.pc_random_choice = "scissors"
            self.screen.blit(self.choose_scissors, (480, 140))
        return pc_choice

    def pl_score_cache(self):
        self.pl_score = 0
        self.pc_score = 0

        pl = self.p_option
        pc = self.pc_random_choice

        if pl == "rock" and pc == "paper" or pl == "paper" and pc == "scissors" or pl == "scissors" and pc == "rock":
            self.pc_score += 1
        elif pl == pc:
            pass
        else:
            self.pl_score += 1

        return self.pl_score

    def pc_score_cache(self):
        self.pl_score = 0
        self.pc_score = 0

        pl = self.p_option
        pc = self.pc_random_choice

        if pl == "rock" and pc == "paper" or pl == "paper" and pc == "scissors" or pl == "scissors" and pc == "rock":
            self.pc_score += 1
        elif pl == pc:
            pass
        else:
            self.pl_score += 1
        return self.pc_score

    def image_reset(self):
        self.screen.blit(self.text, (260, 0))
        self.text = self.font.render(" ", True, (0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        self.screen.blit(self.r_btn, (280, 380))
        self.screen.blit(self.p_btn, (540, 380))
        self.screen.blit(self.s_btn, (20, 380))

        pass

    def game_loop(self):
        run = True
        game_start = False
        #clock = pygame.time.Clock()
        rps_game = RpsGame()
        while run:
            pygame.display.update()
            self.screen.blit(self.text, (260, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_btn.clicked(150):
                        rps_game.image_reset()
                        rps_game.computer()

                    elif self.rock_btn.clicked(280) or self.paper_btn.clicked(540) or self.scissors_btn.clicked(30):
                        rps_game.image_reset()
                        rps_game.player()

                        self.pl_score += rps_game.pl_score_cache()
                        self.pc_score += rps_game.pc_score_cache()
                        self.text = self.font.render(f"{self.pl_score} : {self.pc_score}", True, (0, 0, 0))
                        rps_game.computer()


            if self.pl_score == 3:
                self.screen.blit(self.win, (0, 0))
                self.screen.blit(self.main, (30, 0))
                self.screen.blit(self.retry, (540, 0))

            if self.pc_score == 3:
                self.screen.blit(self.lose, (0, 0))
                self.screen.blit(self.main, (30, 0))
                self.screen.blit(self.retry, (540, 0))

            if self.pl_score or self.pc_score == 3:
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.main_btn.clicked(30):
                            run = False
                        if self.retry_btn.clicked(540):
                             play_rps_game()
            pygame.display.flip()
            #clock.tick(100)

        #pygame.quit()

def play_rps_game():
    game = RpsGame()
    game.game_loop()

# if __name__ == '__main__':
#     game = RpsGame()
#     game.game_loop()