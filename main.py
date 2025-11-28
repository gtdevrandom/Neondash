import pygame
import sys
import os
from neondash_personnage import personnage
from neondash_map import GameMap
from neondash_particles import ParticleSystem

# --- Constantes globales ---
WIDTH, HEIGHT = 1600, 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
MENU = 'menu'
GAME = 'game'
SETTINGS = 'settings'
QUIT = 'quit'
DEATH = 'death'
VOLUME = 0.5

def draw_text(surface, text, size, x, y, color=WHITE, return_rect=False):
    font = pygame.font.SysFont('Arial', size, bold=True)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    bg_rect = text_rect.inflate(20, 10)
    pygame.draw.rect(surface, (20, 20, 30), bg_rect, border_radius=8)
    surface.blit(text_surface, text_rect)
    if return_rect:
        return bg_rect
    return None

# --- Classes d'écrans ---
class Screen:
    def __init__(self, window):
        self.window = window
    def run(self):
        raise NotImplementedError

class MenuScreen(Screen):
    def run(self):
        selected = 0
        options = ['Jouer', 'Paramètres', 'Quitter']
        clock = pygame.time.Clock()
        option_rects = [None] * len(options)
        title_img = pygame.image.load('textures/title/title.png')
        title_rect = title_img.get_rect(center=(WIDTH//2, 100))
        while True:
            self.window.fill((15, 10, 25))
            self.window.blit(title_img, title_rect)
            for i, option in enumerate(options):
                color = MAGENTA if i == selected else CYAN if i == 0 else WHITE
                rect = draw_text(self.window, option, 44, WIDTH//2, 300 + i*80, color, return_rect=True)
                pygame.draw.rect(self.window, color, rect, 3, border_radius=8)
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

class SettingsScreen(Screen):
    def run(self):
        global VOLUME
        clock = pygame.time.Clock()
        while True:
            self.window.fill((15, 10, 25))
            draw_text(self.window, 'Paramètres', 54, WIDTH//2, 120, CYAN)
            vol_percent = int(VOLUME * 100)
            draw_text(self.window, f'Volume musique : {vol_percent}%', 38, WIDTH//2, 220, WHITE)
            bar_x, bar_y, bar_w, bar_h = WIDTH//2 - 150, 260, 300, 18
            pygame.draw.rect(self.window, (40, 40, 60), (bar_x, bar_y, bar_w, bar_h), border_radius=8)
            pygame.draw.rect(self.window, CYAN, (bar_x, bar_y, int(bar_w * VOLUME), bar_h), border_radius=8)
            pygame.draw.rect(self.window, CYAN, (bar_x, bar_y, bar_w, bar_h), 2, border_radius=8)
            draw_text(self.window, '← → pour régler le volume', 24, WIDTH//2, 295, CYAN)
            draw_text(self.window, 'Appuie sur Echap pour revenir', 32, WIDTH//2, 350, WHITE)
            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return MENU
                    elif event.key == pygame.K_LEFT:
                        VOLUME = max(0.0, VOLUME - 0.05)
                        pygame.mixer.music.set_volume(VOLUME)
                    elif event.key == pygame.K_RIGHT:
                        VOLUME = min(1.0, VOLUME + 0.05)
                        pygame.mixer.music.set_volume(VOLUME)
            clock.tick(FPS)

class DeathScreen(Screen):
    def __init__(self, window, score=0):
        super().__init__(window)
        self.score = score

    def run(self):
        clock = pygame.time.Clock()
        selected = 0
        options = ['Rejouer', 'Menu principal', 'Quitter']
        while True:
            self.window.fill((30, 0, 40))
            draw_text(self.window, 'Vous êtes mort !', 70, WIDTH//2, 200, MAGENTA)
            draw_text(self.window, f'Score : {self.score}', 48, WIDTH//2, 270, CYAN)
            for i, option in enumerate(options):
                color = CYAN if i == selected else WHITE
                draw_text(self.window, option, 40, WIDTH//2, 350 + i*60, color)
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
                            return MENU
                        elif selected == 2:
                            return QUIT
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    for i in range(len(options)):
                        rect = pygame.Rect(WIDTH//2 - 150, 330 + i*60, 300, 50)
                        if rect.collidepoint(mx, my):
                            if i == 0:
                                return GAME
                            elif i == 1:
                                return MENU
                            elif i == 2:
                                return QUIT
            clock.tick(FPS)

def game_screen(window):
    global VOLUME
    clock = pygame.time.Clock()
    running = True
    player = personnage(100, HEIGHT//2, size=50, color=(0, 200, 255), screen_height=HEIGHT)
    game_map = GameMap(WIDTH, HEIGHT, map_file='maps/maps.json')
    particle_system = ParticleSystem(WIDTH, HEIGHT, count=12)
    mouse_held = False
    menu_btn_rect = pygame.Rect(20, 20, 180, 50)

    # Suppression des landing particles

    score = 0
    timer = 0.0

    # Lecture de la musique en boucle
    try:
        pygame.mixer.music.load('musique/m1.mp3')
        pygame.mixer.music.set_volume(VOLUME)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Erreur chargement musique : {e}")

    while running:
        dt = clock.tick(FPS) / 1000.0
        timer += dt
        if timer >= 1.0:
            score += 1
            timer -= 1.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return MENU
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mx, my = event.pos
                    if menu_btn_rect.collidepoint(mx, my):
                        pygame.mixer.music.stop()
                        return MENU
                    mouse_held = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_held = False

        keys = pygame.key.get_pressed()
        jump_held = keys[pygame.K_UP] or keys[pygame.K_SPACE] or mouse_held or pygame.mouse.get_pressed()[0]
        if jump_held:
            player.jump()

        game_map.update(dt)
        particle_system.update(dt)
        prev_bottom = player.rect.bottom
        player.update(dt)
        player.on_ground = False
        if player.rect.bottom >= HEIGHT:
            player.on_ground = True

        for c in game_map.cubes:
            if player.rect.colliderect(c.rect):
                if player.vel_y >= 0 and prev_bottom <= c.rect.top and player.rect.bottom >= c.rect.top:
                    player.rect.bottom = c.rect.top
                    player.vel_y = 0
                    player.on_ground = True
                else:
                    pygame.mixer.music.stop()
                    return ('death', score)

        for s in game_map.spikes:
            if player.rect.colliderect(s.rect):
                pygame.mixer.music.stop()
                return ('death', score)

        game_map.draw(window)
        particle_system.draw(window)
        player.draw(window)

        # Affichage du score en haut à droite
        draw_text(window, f"Score : {score}", 36, WIDTH - 120, 40, CYAN)

        pygame.draw.rect(window, (40, 40, 60), menu_btn_rect, border_radius=10)
        pygame.draw.rect(window, CYAN, menu_btn_rect, 3, border_radius=10)
        font = pygame.font.SysFont('Arial', 28, bold=True)
        txt = font.render('Retour menu', True, CYAN)
        txt_rect = txt.get_rect(center=menu_btn_rect.center)
        window.blit(txt, txt_rect)

        pygame.display.flip()
    pygame.mixer.music.stop()
    return MENU

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('NeonDash')
    state = MENU
    score = 0
    screen_map = {
        MENU: MenuScreen(window),
        SETTINGS: SettingsScreen(window)
    }
    while True:
        if state == GAME:
            result = game_screen(window)
            if isinstance(result, tuple) and result[0] == 'death':
                score = result[1]
                state = 'death'
            else:
                state = result
        elif state == 'death':
            death_screen = DeathScreen(window, score)
            state = death_screen.run()
        elif state in screen_map:
            state = screen_map[state].run()
        elif state == QUIT:
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    main()
