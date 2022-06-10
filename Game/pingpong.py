import pygame

pygame.init()
screen_width=800
screen_height=480
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

def Game2():
    score = 0
    large_font = pygame.font.Font('MaruBuri-Regular.ttf', 72)
    small_font = pygame.font.Font('MaruBuri-Regular.ttf', 36)
    game_over = False

    bar_width, bar_height = screen_width / 32., screen_height / 6.
    bar_dist_from_edge = screen_width / 64.
    circle_diameter = screen_height / 16.
    circle_radius = circle_diameter / 2.
    bar_1_start_x = bar_dist_from_edge
    bar_start_y = (screen_height - bar_height) / 2.
    bar_max_y = screen_height - bar_height - bar_dist_from_edge
    circle_start_x, circle_start_y = (screen_width - circle_diameter), (screen_width - circle_diameter) / 2.

    screen = pygame.display.set_mode((int(screen_width), int(screen_height)), 0, 32)

    back = pygame.Surface((int(screen_width), int(screen_height)))
    background = back.convert()
    background.fill((0, 0, 0))
    bar = pygame.Surface((int(bar_width), int(bar_height)))
    bar1 = bar.convert()
    bar1.fill((255, 255, 255))
    circle_surface = pygame.Surface((int(circle_diameter), int(circle_diameter)))
    pygame.draw.circle(circle_surface, (255, 255, 255), (int(circle_radius), int(circle_radius)), int(circle_radius))
    circle = circle_surface.convert()
    circle.set_colorkey((0, 0, 0))
    bar1_x = bar_1_start_x
    bar1_y = bar_start_y
    circle_x, circle_y = circle_start_x, circle_start_y
    bar1_move= 0
    speed_x, speed_y, speed_bar = -screen_width / 1.28, screen_height / 1.92, screen_height * 1.2

    clock = pygame.time.Clock()

    while True:
        event = pygame.event.poll()
        if event.type == pygame.QUIT: 
            pygame.quit()
            break
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            pos = pygame.mouse.get_pos()
            if (0, 0) <= pos <= (400, 240):
                bar1_move = -ai_speed
            elif (400, 0) <= pos <= (800, 240):
                bar1_move = ai_speed
        elif event.type == pygame.MOUSEBUTTONUP:
                bar1_move = 0.

        screen.blit(background, (0, 0))
        screen.blit(bar1, (bar1_x, bar1_y))
        screen.blit(circle, (circle_x, circle_y))
    
        bar1_y += bar1_move

        time_passed = clock.tick(60)
        time_sec = time_passed / 1000.0

        circle_x += speed_x * time_sec
        circle_y += speed_y * time_sec
        ai_speed = speed_bar * time_sec

        if bar1_y >= bar_max_y:
            bar1_y = bar_max_y
        elif bar1_y <= bar_dist_from_edge:
            bar1_y = bar_dist_from_edge

        if circle_x < bar_dist_from_edge + bar_width:
            if circle_y >= bar1_y - circle_radius and circle_y <= bar1_y + bar_height + circle_radius:
                circle_x = bar_dist_from_edge + bar_width
                speed_x = -speed_x
                score += 1
        if circle_x < -circle_radius:
            game_over = True
            speed_x= 0
            speed_y= 0
            circle_x, circle_y = circle_start_x, circle_start_y
            bar1_y, bar_2_y = bar_start_y, bar_start_y
            bar1_y, bar_2_y = bar_start_y, bar_start_y
        elif circle_x > screen_width - circle_diameter:
            speed_x = -speed_x
        if circle_y <= bar_dist_from_edge:
            speed_y = -speed_y
            circle_y = bar_dist_from_edge
        elif circle_y >= screen_height - circle_diameter - circle_radius:
            speed_y = -speed_y
            circle_y = screen_height - circle_diameter - circle_radius
        
        score_image = small_font.render('점수 {}'.format(score), True, WHITE)
        screen.blit(score_image, (650, 10))        
        
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
                        Game2()
                        pygame.display.update()
        pygame.display.update()

def play_pingpong():
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("호두파이 핑퐁 게임")
    game2script = pygame.image.load('images/bugpongImages/game2script.png')
    GameStart = pygame.image.load('images/bugpongImages/start.png')
    GameStartRect = GameStart.get_rect()
    GameStartRect.center = (650, 50)
    
    while True:
        screen.blit(game2script, (0, 0))
        screen.blit(GameStart, GameStartRect)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                if GameStartRect.collidepoint((mousex, mousey)):
                    Game2()
        pygame.display.update() 

# play_pingpong()
