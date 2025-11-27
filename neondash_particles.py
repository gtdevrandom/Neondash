import pygame
import random
import os

PARTICULES_PATH = 'textures/fond/particules'
PARTICULES_FILES = [
    'particule1.png', 'particule2.png', 'particule3.png', 'particule4.png',
    'particule5.png', 'particule6.png', 'particule7.png', 'particule8.png'
]

class Particle:
    def __init__(self, images, width, height):
        self.img = random.choice(images).copy()
        self.img.set_alpha(80)  # Opacité plus faible 30%)
        self.x = random.uniform(0, width)
        self.y = random.uniform(0, height)
        self.speed = random.uniform(80, 200)
        self.size = random.uniform(10, 25)  # Taille plus petite
        self.img = pygame.transform.scale(self.img, (int(self.size), int(self.size)))

    def update(self, dt, width, height):
        self.x -= self.speed * dt
        if self.x < -self.size:
            self.x = width + random.uniform(0, 100)
            self.y = random.uniform(0, height)
            self.speed = random.uniform(80, 200)
            self.size = random.uniform(10, 25)  # Taille plus petite
            self.img = pygame.transform.scale(self.img, (int(self.size), int(self.size)))
            self.img.set_alpha(80)

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

class ParticleSystem:
    def __init__(self, width, height, count=6):
        self.images = []
        for fname in PARTICULES_FILES:
            path = os.path.join(PARTICULES_PATH, fname)
            try:
                img = pygame.image.load(path).convert_alpha()
                img.set_alpha(80)
                self.images.append(img)
            except Exception:
                pass
        self.particles = [Particle(self.images, width, height) for _ in range(count)]
        self.width = width
        self.height = height

    def update(self, dt):
        for p in self.particles:
            p.update(dt, self.width, self.height)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
