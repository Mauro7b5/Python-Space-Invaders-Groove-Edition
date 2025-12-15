import pygame
import sys
import random
import time


pygame.init()
pygame.mixer.init()

from game import Game
import SoundEngine

OFFSET = 50
SCREEN_WIDTH = 850
SCREEN_HEIGHT = 700

bpm = 90
MUSICBEAT_MS = 60 / bpm

GREY = (29, 29, 27)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + (2 * OFFSET)))
pygame.display.set_caption("Space Invaders Groove Edition")
font = pygame.font.Font("Font/monogram.ttf", 40)

screen_center = screen.get_rect().center
title_image = pygame.image.load("Graphics/title.png")
subtitle_image = pygame.image.load("Graphics/subtitle.png")
title_image_rect = title_image.get_rect()
title_image_rect.center = (screen_center[0], int(screen_center[1] * 0.55))
subtitle_image_rect = subtitle_image.get_rect()
subtitle_image_rect.center = (screen_center[0], int(screen_center[1] * 0.7))
title_alien1_image = pygame.image.load("Graphics/alien_1.png")
title_alien2_image = pygame.image.load("Graphics/alien_2.png")
title_alien3_image = pygame.image.load("Graphics/alien_3.png")
title_mystery_image = pygame.image.load("Graphics/mystery.png")
title_spaceship_image = pygame.image.load("Graphics/spaceship.png")
title_alien1_rect = title_alien1_image.get_rect()
title_alien1_rect.center = (int(screen_center[0] * 0.8), int(screen_center[1] * 0.9))
title_alien2_rect = title_alien2_image.get_rect()
title_alien2_rect.center = (int(screen_center[0]), int(screen_center[1] * 0.9))
print(title_alien2_rect.center)
title_alien3_rect = title_alien3_image.get_rect()
title_alien3_rect.center = (int(screen_center[0] * 1.2), int(screen_center[1] * 0.9))
title_mystery_rect = title_mystery_image.get_rect()
title_mystery_rect.center = (int(screen_center[0] * 0.89), int(screen_center[1] * 0.42))
title_spaceship_rect = title_spaceship_image.get_rect()
title_spaceship_rect.center = (int(screen_center[0]), int(screen_center[1] * 1.5))


level_surface = font.render("DESTROY ALL ALIENS", False, WHITE)
game_over_surface = font.render("GAME OVER", False, WHITE)
win_surface = font.render("YOU WON", False, RED)
score_text_surface = font.render("SCORE", False, WHITE)
highscore_text_surface = font.render("HIGHSCORE", False, WHITE)
spacebar_reset_surface = font.render('PRESS "SPACEBAR" TO RESET', False, RED)
spacebar_start_surface = font.render('PRESS "SPACEBAR" TO START', False, RED)
spacebar_start_rect = spacebar_start_surface.get_rect()
spacebar_start_rect.center = (int(screen_center[0]), int(screen_center[1] * 1.7))
youlost_surface = font.render("YOU LOST", False, RED)
pause_surface = font.render('PRESS "P" TO RESUME', False, RED)
gameover_cycles = 0
game_pause = False


clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, 300)

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

beatnumber = 0
beat_time = time.time()
in_title_screen = True
SoundEngine.theme_in(2000)

while True:
    while in_title_screen:
        screen.fill(GREY)
        pygame.draw.rect(screen, WHITE, (10, 10, 880, 780), 2, 0, 60, 60, 60, 60)
        screen.blit(title_image, title_image_rect)
        screen.blit(subtitle_image, subtitle_image_rect)
        screen.blit(spacebar_start_surface, spacebar_start_rect)
        screen.blit(title_alien1_image, title_alien1_rect)
        screen.blit(title_alien2_image, title_alien2_rect)
        screen.blit(title_alien3_image, title_alien3_rect)
        screen.blit(title_mystery_image, title_mystery_rect)
        screen.blit(title_spaceship_image, title_spaceship_rect)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                SoundEngine.theme_out()
                in_title_screen = False
                game.reset()
        clock.tick(60)
        pass

    elapsed_time = time.time() - beat_time

    if elapsed_time >= MUSICBEAT_MS:
        beatnumber %= 4
        SoundEngine.playbeat(beatnumber + 1)
        beatnumber += 1
        beat_time = time.time()

    # main loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()

        if event.type == MYSTERYSHIP and game.run:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000, 8000))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and not game.run:
            game.reset()
            gameover_cycles = 0
        if keys[pygame.K_ESCAPE]:
            in_title_screen = True
            SoundEngine.theme_in(1200)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                game_pause = not game_pause

    while game_pause:
        clock.tick(60)
        screen.blit(pause_surface, (300, 30, 100, 100))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    game_pause = False
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # aggiorna elementi inchè run è true
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()

    # disegna sfondo e oggetti
    screen.fill(GREY)
    pygame.draw.rect(screen, WHITE, (10, 10, 880, 780), 2, 0, 60, 60, 60, 60)
    pygame.draw.line(screen, WHITE, (25, 730), (875, 730), 3)
    # block image transfer
    if game.run:
        screen.blit(level_surface, (570, 740, 50, 50))

    live_x = 50
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (live_x, 745))
        live_x += 50

    screen.blit(score_text_surface, (50, 15, 50, 50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font.render(formatted_score, False, WHITE)
    screen.blit(score_surface, (140, 15, 50, 50))
    screen.blit(highscore_text_surface, (620, 15, 50, 50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore_surface = font.render(formatted_highscore, False, WHITE)
    screen.blit(highscore_surface, (770, 15, 50, 50))

    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
        game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)

    if game.run:
        pygame.display.update()

    # freeze due secondi per gameover
    if not game.run and gameover_cycles == 0:
        gameover_cycles += 1
        if game.victory:
            screen.blit(game_over_surface, (670, 740, 50, 50))
            screen.blit(win_surface, (400, 640, 70, 60))
            time.sleep(0.5)
            SoundEngine.play_win()
        elif not game.victory:
            screen.blit(game_over_surface, (670, 740, 50, 50))
            screen.blit(youlost_surface, (390, 640, 70, 60))
            time.sleep(0.5)
            SoundEngine.play_loss()
        pygame.display.update()
        time.sleep(2)

    elif not game.run and gameover_cycles > 0:
        screen.blit(game_over_surface, (670, 740, 50, 50))
        screen.blit(spacebar_reset_surface, (265, 640, 70, 60))
        pygame.display.update()
        pass

    clock.tick(60)
