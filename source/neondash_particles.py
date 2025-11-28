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
        self.images = images
        self.width = width
        self.height = height
        self.reset()

    def reset(self):
        self.size = random.uniform(10, 25)
        self.speed = random.uniform(80, 200)
        self.x = random.uniform(0, self.width)
        self.y = random.uniform(0, self.height)
        self.img = pygame.transform.scale(random.choice(self.images).copy(), (int(self.size), int(self.size)))
        self.img.set_alpha(80)

    def update(self, dt):
        self.x -= self.speed * dt
        if self.x < -self.size:
            self.x = self.width + random.uniform(0, 100)
            self.reset()

    def draw(self, surface):
        surface.blit(self.img, (self.x, self.y))

class ParticleSystem:
    def __init__(self, width, height, count=6):
        self.images = [
            pygame.image.load(os.path.join(PARTICULES_PATH, fname)).convert_alpha()
            for fname in PARTICULES_FILES #nom des fichiers
            if os.path.exists(os.path.join(PARTICULES_PATH, fname))
        ]
        self.particles = [Particle(self.images, width, height) for _ in range(count)]
        self.width = width
        self.height = height


    def update(self, dt):
        for p in self.particles: #met a jour chaque particule
            p.update(dt) #dt est le delta time, le temps écoulé depuis la dernière mise à jour

    def draw(self, surface):
        for p in self.particles: #dessine chaque particule sur la surface
            p.draw(surface)
