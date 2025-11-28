import pygame, sys
from pygame.locals import *

class Spike:
	def __init__(self, x, y, width=30, height=40, color=(255, 0, 0), speed=200):
		self.rect = pygame.Rect(x, y, width, height)
		self.color = color
		self.speed = float(speed)  # pixels per second
		try:
			self.skin = pygame.image.load('textures/spike/grand_spike.png').convert_alpha()
			self.skin = pygame.transform.scale(self.skin, (width, height))
		except Exception:
			self.skin = None

	def update(self, dt):
		self.rect.x -= int(self.speed * dt)

	def draw(self, surface):
		if self.skin:
			surface.blit(self.skin, self.rect)
		else:
			# Triangle pour le spike
			points = [
				(self.rect.centerx, self.rect.top),
				(self.rect.left, self.rect.bottom),
				(self.rect.right, self.rect.bottom)
			]
			pygame.draw.polygon(surface, self.color, points)
