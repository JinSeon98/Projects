import pygame 
import random
import time
import math

pygame.init() 
screen_width = 800
screen_height = 480
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

def Game1():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("호두파이 벌레 잡기")
    background_image = pygame.image.load('images/bugpongImages/background.png')

    large_font = pygame.font.Font('MaruBuri-Regular.ttf', 72)
    small_font = pygame.font.Font('MaruBuri-Regular.ttf', 36)
    score = 0
    start_time = int(time.time())
    game_over = False
    clock = pygame.time.Clock()
    
    bug_image = pygame.image.load('images/bugpongImages/bug.png')
    bugs = []
    for i in range(3):
        bug = bug_image.get_rect(left=random.randint(0, screen_width) - bug_image.get_width(), top=random.randint(0, screen_height) - bug_image.get_height())
        degree = random.randint(0, 360)
        bugs.append((bug, degree))
    
    
    while True:
        screen.blit(background_image, (0, 0))

        event = pygame.event.poll() 
        if event.type == pygame.QUIT:
            break
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            for bug, degree in bugs:
                if bug.collidepoint(event.pos):
                    bugs.remove((bug, degree))
                    bug = bug_image.get_rect(left=random.randint(0, screen_width) - bug_image.get_width(), top=random.randint(0, screen_height) - bug_image.get_height())
                    degree = random.randint(0, 360)
                    bugs.append((bug, degree))
                    score += 1
        if not game_over:
            current_time = int(time.time())
            remain_second = 30 - (current_time - start_time)    

            if remain_second <= 0:
                game_over = True
        
            for bug, degree in bugs:
                radian = degree * (math.pi / 180)
                dx = 6 * math.cos(radian)
                dy =  - 6 * math.sin(radian)
                bug.left += dx
                bug.top += dy
            for bug, degree in bugs:
                if not bug.colliderect(screen.get_rect()):
                    bugs.remove((bug, degree))
                    bug = bug_image.get_rect(left=random.randint(0, screen_width) - bug_image.get_width(), top=random.randint(0, screen_height) - bug_image.get_height())
                    degree = random.randint(0, 360)
                    bugs.append((bug, degree))   
        
        for bug, degree in bugs:
            rotated_bug_image = pygame.transform.rotate(bug_image, degree)
            screen.blit(rotated_bug_image, (bug.left, bug.top)) 
                
        score_image = small_font.render('점수 {}'.format(score), True, YELLOW)
        screen.blit(score_image, (10, 10))
        remain_second_image = small_font.render('남은 시간 {}'.format(remain_second), True, YELLOW)
        screen.blit(remain_second_image, remain_second_image.get_rect(right=screen_width - 10, top=10))

        if game_over:
            game_over_image1 = large_font.render('게임 종료', True, RED)
            game_over_image2 = pygame.image.load('images/bugpongImages/restart.png')
            game_over_image2_rect = game_over_image2.get_rect()
            game_over_image2_rect.center = (400, 400)
            screen.blit(game_over_image1, game_over_image1.get_rect(centerx=screen_width // 2, centery=screen_height // 2))    
            screen.blit(game_over_image2, game_over_image2_rect)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mousex, mousey = event.pos
                    if game_over_image2_rect.collidepoint((mousex, mousey)):
                        Game1()
                        pygame.display.update()
        pygame.display.update() 
        clock.tick(60) 

def play_bug_game():
    screen = pygame.display.set_mode((screen_width, screen_height))
    game1script = pygame.image.load('images/bugpongImages/game1script.png')
    GameStart = pygame.image.load('images/bugpongImages/start.png')
    GameStartRect = GameStart.get_rect()
    GameStartRect.center = (650, 50)
    
    while True:
        screen.blit(game1script, (0, 0))
        screen.blit(GameStart, GameStartRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if GameStartRect.collidepoint((mousex, mousey)):
                    Game1()
        pygame.display.update() 

# play_bug_game()
