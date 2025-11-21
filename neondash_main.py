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
    title_img = pygame.image.load('title/title.png')
    title_rect = title_img.get_rect(center=(WIDTH//2, 60))
    while True:
        window.fill(BLACK)
        window.blit(title_img, title_rect)
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

    mouse_held = False
    while running:
        dt = clock.tick(FPS) / 1000.0
        window.fill((30, 30, 40))

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_held = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_held = False

        keys = pygame.key.get_pressed()
        jump_held = keys[pygame.K_UP] or keys[pygame.K_SPACE] or mouse_held or pygame.mouse.get_pressed()[0]
        if jump_held:
            player.jump()

        player.update(dt)
        player.draw(window)

        draw_text(window, 'Echap pour menu', 24, WIDTH//2, 30, CYAN)
        pygame.display.flip()
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

