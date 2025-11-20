import pygame
import sys
from neondash_personnage import personnage
from neondash_cube import Cube
from neondash_spike import Spike

WIDTH, HEIGHT = 800, 400
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# États du jeu
MENU = 'menu'
GAME = 'game'
SETTINGS = 'settings'
QUIT = 'quit'

def draw_text(surface, text, size, x, y, color=WHITE, return_rect=False):
    font = pygame.font.SysFont('Arial', size, bold=True)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)
    if return_rect:
        return text_rect
    return None

def menu_screen(window):
    selected = 0
    options = ['Jouer', 'Paramètres', 'Quitter']
    clock = pygame.time.Clock()
    option_rects = [None] * len(options)
    while True:
        window.fill(BLACK)
        draw_text(window, 'NEONDASH', 60, WIDTH//2, 80, CYAN)
        for i, option in enumerate(options):
            color = MAGENTA if i == selected else WHITE
            rect = draw_text(window, option, 40, WIDTH//2, 180 + i*60, color, return_rect=True)
            option_rects[i] = rect
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected == 0:
                        return GAME
                    elif selected == 1:
                        return SETTINGS
                    elif selected == 2:
                        return QUIT
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                for i, rect in enumerate(option_rects):
                    if rect and rect.collidepoint(mx, my):
                        if i == 0:
                            return GAME
                        elif i == 1:
                            return SETTINGS
                        elif i == 2:
                            return QUIT
        clock.tick(FPS)

def settings_screen(window):
    clock = pygame.time.Clock()
    while True:
        window.fill(BLACK)
        draw_text(window, 'Paramètres', 50, WIDTH//2, 100, CYAN)
        draw_text(window, 'Appuie sur Echap pour revenir', 30, WIDTH//2, 300, WHITE)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return MENU
        clock.tick(FPS)

import random
def game_screen(window):
    clock = pygame.time.Clock()
    running = True
    player = personnage(100, HEIGHT//2, size=50, color=(0, 200, 255), screen_height=HEIGHT)
    cubes = []
    spikes = []
    obstacle_timer = 0
    obstacle_interval = 1500  # ms
    last_time = pygame.time.get_ticks()

    while running:
        dt = clock.tick(FPS) / 1000.0
        window.fill((30, 30, 40))

        now = pygame.time.get_ticks()
        if now - obstacle_timer > obstacle_interval:
            if random.choice([True, False]):
                cubes.append(Cube(WIDTH, HEIGHT-80, size=40, color=(255,255,0), speed=6))
            else:
                spikes.append(Spike(WIDTH, HEIGHT-60, width=30, height=40, color=(255,0,0), speed=6))
            obstacle_timer = now

        for cube in cubes:
            cube.update()
        for spike in spikes:
            spike.update()
        cubes = [c for c in cubes if c.rect.right > 0]
        spikes = [s for s in spikes if s.rect.right > 0]

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move_up()
        elif keys[pygame.K_DOWN]:
            player.move_down()
        else:
            player.stop()
        player.update(dt)

        player.draw(window)
        for cube in cubes:
            cube.draw(window)
        for spike in spikes:
            spike.draw(window)

        draw_text(window, 'Echap pour menu', 24, WIDTH//2, 30, CYAN)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        # Collision (simple)
        for cube in cubes:
            if player.rect.colliderect(cube.rect):
                running = False
        for spike in spikes:
            if player.rect.colliderect(spike.rect):
                running = False
    return MENU

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('NeonDash')
    state = MENU
    while True:
        if state == MENU:
            state = menu_screen(window)
        elif state == SETTINGS:
            state = settings_screen(window)
        elif state == GAME:
            state = game_screen(window)
        elif state == QUIT:
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    main()

