import pygame
import sys
from neondash_personnage import personnage
from neondash_cube import Cube
from neondash_spike import Spike

WIDTH, HEIGHT = 1600, 800
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

    # Chargement de l'image de fond
    fond_img = pygame.image.load('fond/base/fond.png').convert()
    fond_img = pygame.transform.scale(fond_img, (WIDTH, HEIGHT))
    fond_x = 0
    fond_speed = 100  # pixels par seconde (ajuster pour la vitesse de défilement)

    # Chargement des images décoratives
    deco_infos = [
        # (chemin, rareté, type)
        ('fond/lanternes/lanterne1.png', 1, 'lanterne'),
        ('fond/lanternes/lanterne2.png', 1, 'lanterne'),
        ('fond/lanternes/lanterne3.png', 1, 'lanterne'),
        ('fond/brique/brique.png', 0.3, 'brique'),  # rareté plus faible
        ('fond/chaines/chaine.png', 1, 'chaine'),
        ('fond/chaines/chaine1.png', 1, 'chaine'),
        ('fond/chaines/chaine2.png', 1, 'chaine'),
        ('fond/chaines/chaine3.png', 1, 'chaine'),
    ]
    deco_images = []
    for path, _, deco_type in deco_infos:
        img = pygame.image.load(path).convert_alpha()
        # Double la hauteur
        new_height = HEIGHT
        # Double la largeur pour lanternes et chaines
        if deco_type in ('lanterne', 'chaine'):
            new_width = img.get_width() * 2
        else:
            new_width = img.get_width()
        img = pygame.transform.scale(img, (new_width, new_height))
        deco_images.append(img)

    # Liste des décorations à afficher (x, y, idx_image)
    decorations = []
    min_distance = 400  # distance minimale entre deux décorations
    deco_speed = 120  # px/s
    max_deco_on_screen = 3

    def spawn_deco(last_idx=None):
        # Choix de l'image avec rareté, sans répéter la dernière
        idxs = list(range(len(deco_infos)))
        weights = [info[1] for info in deco_infos]
        if last_idx is not None and len(idxs) > 1:
            # Empêche de choisir la même image que la précédente
            weights = [w if i != last_idx else 0 for i, w in enumerate(weights)]
        idx = random.choices(idxs, weights=weights)[0]
        img = deco_images[idx]
        deco_type = deco_infos[idx][2]
        if deco_type == 'chaine':
            y = 0
        else:
            y = random.randint(0, HEIGHT - img.get_height())
        x = WIDTH + random.randint(0, 200)
        return (x, y, idx)

    # Initialisation de quelques décorations
    last_deco_x = 0
    last_idx = None
    for _ in range(max_deco_on_screen):
        deco = spawn_deco(last_idx)
        if not decorations or deco[0] - last_deco_x > min_distance:
            decorations.append(deco)
            last_deco_x = deco[0]
            last_idx = deco[2]

    mouse_held = False
    while running:
        dt = clock.tick(FPS) / 1000.0

        # Défilement du fond
        fond_x -= fond_speed * dt
        if fond_x <= -WIDTH:
            fond_x += WIDTH

        # Affichage du fond (2 images pour recoller à l'infini)
        window.blit(fond_img, (fond_x, 0))
        window.blit(fond_img, (fond_x + WIDTH, 0))

        # Défilement et affichage des décorations
        for i, (x, y, idx) in enumerate(decorations):
            decorations[i] = (x - deco_speed * dt, y, idx)
            window.blit(deco_images[idx], (x, y))

        # Suppression des décorations hors écran
        decorations = [d for d in decorations if d[0] + deco_images[d[2]].get_width() > 0]

        # Ajout de nouvelles décorations si besoin
        if not decorations or (decorations and decorations[-1][0] < WIDTH - min_distance):
            # Vérifie la distance minimale avec la dernière déco
            last_idx = decorations[-1][2] if decorations else None
            new_deco = spawn_deco(last_idx)
            if not decorations or new_deco[0] - decorations[-1][0] > min_distance:
                decorations.append(new_deco)

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


