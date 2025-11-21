import pygame
import random
import math
from neondash_cube import Cube
from neondash_spike import Spike


class Decoration:
    def __init__(self, img, x, y, idx):
        self.img = img
        self.x = x
        self.y = y
        self.idx = idx

    def update(self, dt, speed):
        self.x -= speed * dt

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))


class BackgroundScroller:
    def __init__(self, path, width, height, speed):
        img = pygame.image.load(path).convert()
        self.img = pygame.transform.scale(img, (width, height))
        self.width = width
        self.height = height
        self.x = 0
        self.speed = speed
        # Tint effect state: start/current/target colors and timing
        # Start with a blue tint
        self.current_color = (0, 100, 255)
        self.start_color = self.current_color
        self.target_color = self.current_color
        self.tint_elapsed = 0.0
        self.tint_duration = random.uniform(6.0, 12.0)
        # Immediately pick a new random target so the effect starts animating
        self._pick_new_tint()

    def _pick_new_tint(self):
        # Choose a new random target color (allow full RGB range)
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.start_color = self.current_color
        self.target_color = (r, g, b)
        self.tint_elapsed = 0.0
        # Faster transitions than before (un peu plus rapide)
        self.tint_duration = random.uniform(2.0, 5.0)

    def update(self, dt):
        self.x -= self.speed * dt
        if self.x <= -self.width:
            self.x += self.width

        # Update tint interpolation
        self.tint_elapsed += dt
        if self.tint_elapsed >= self.tint_duration:
            # Finish transition and pick a new target
            self.current_color = self.target_color
            self._pick_new_tint()
        else:
            t = self.tint_elapsed / max(1e-6, self.tint_duration)
            # Linear interpolation per channel
            cr = int(self.start_color[0] + (self.target_color[0] - self.start_color[0]) * t)
            cg = int(self.start_color[1] + (self.target_color[1] - self.start_color[1]) * t)
            cb = int(self.start_color[2] + (self.target_color[2] - self.start_color[2]) * t)
            self.current_color = (cr, cg, cb)

    def draw(self, surface):
        # Apply tint to a copy of the background using multiplicative blend
        try:
            tinted = self.img.copy()
            tint_surf = pygame.Surface((self.width, self.height)).convert_alpha()
            tint_surf.fill((int(self.current_color[0]), int(self.current_color[1]), int(self.current_color[2]), 255))
            tinted.blit(tint_surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(tinted, (self.x, 0))
            surface.blit(tinted, (self.x + self.width, 0))
        except Exception:
            # Fallback to original if tinting fails for any reason
            surface.blit(self.img, (self.x, 0))
            surface.blit(self.img, (self.x + self.width, 0))


class GameMap:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

        self.background = BackgroundScroller('fond/base/fond.png', width, height, speed=100)

        # décorations informations: (path, weight, type)
        self.deco_infos = [
            ('fond/lanternes/lanterne1.png', 1, 'lanterne'),
            ('fond/lanternes/lanterne2.png', 1, 'lanterne'),
            ('fond/lanternes/lanterne3.png', 1, 'lanterne'),
            ('fond/brique/brique.png', 0.3, 'brique'),
            ('fond/chaines/chaine.png', 1, 'chaine'),
            ('fond/chaines/chaine1.png', 1, 'chaine'),
            ('fond/chaines/chaine2.png', 1, 'chaine'),
            ('fond/chaines/chaine3.png', 1, 'chaine'),
        ]

        # Charger et mettre à l'échelle les images
        self.deco_images = []
        for path, _, deco_type in self.deco_infos:
            img = pygame.image.load(path).convert_alpha()
            if deco_type == 'chaine':
                new_width = 40
                new_height = 800
            elif deco_type == 'lanterne':
                new_width = 80
                new_height = 800
            else:
                new_height = self.HEIGHT
                new_width = img.get_width()
            img = pygame.transform.scale(img, (int(new_width), int(new_height)))
            self.deco_images.append(img)

        self.decorations = []
        self.min_distance = 500
        self.deco_speed = 120
        self.max_deco_on_screen = 2

        # initial spawn
        last_deco_x = 0
        last_idx = None
        for _ in range(self.max_deco_on_screen):
            deco = self._spawn_deco(last_idx)
            if not self.decorations or deco[0] - last_deco_x > self.min_distance:
                self.decorations.append(Decoration(self.deco_images[deco[2]], deco[0], deco[1], deco[2]))
                last_deco_x = deco[0]
                last_idx = deco[2]

    def _spawn_deco(self, last_idx=None):
        idxs = list(range(len(self.deco_infos)))
        weights = [info[1] for info in self.deco_infos]
        if last_idx is not None and len(idxs) > 1:
            weights = [w if i != last_idx else 0 for i, w in enumerate(weights)]
        idx = random.choices(idxs, weights=weights)[0]
        img = self.deco_images[idx]
        deco_type = self.deco_infos[idx][2]
        if deco_type == 'chaine':
            y = 0
        else:
            y = random.randint(0, max(0, self.HEIGHT - img.get_height()))
        x = self.WIDTH + random.randint(0, 200)
        return (x, y, idx)

    def update(self, dt):
        self.background.update(dt)

        # update decorations
        for d in self.decorations:
            d.update(dt, self.deco_speed)

        # remove off-screen
        self.decorations = [d for d in self.decorations if d.x + d.img.get_width() > 0]

        # spawn new if needed
        if not self.decorations or (self.decorations and self.decorations[-1].x < self.WIDTH - self.min_distance):
            last_idx = self.decorations[-1].idx if self.decorations else None
            new = self._spawn_deco(last_idx)
            if not self.decorations or new[0] - self.decorations[-1].x > self.min_distance:
                self.decorations.append(Decoration(self.deco_images[new[2]], new[0], new[1], new[2]))

    def draw(self, surface):
        self.background.draw(surface)
        for d in self.decorations:
            d.draw(surface)
