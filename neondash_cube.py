import pygame, sys
from pygame.locals import *

#*************************************************
class Cube:
	def __init__(self, x, y, size=40, color=(255, 255, 0), speed=5):
		self.rect = pygame.Rect(x, y, size, size)
		self.color = color
		self.speed = speed
		try:
			self.skin = pygame.image.load('cubes/cubes.png').convert_alpha()
			self.skin = pygame.transform.scale(self.skin, (size, size))
		except Exception:
			self.skin = None

	def update(self):
		self.rect.x -= self.speed

	def draw(self, surface):
		if self.skin:
			surface.blit(self.skin, self.rect)
		else:
			pygame.draw.rect(surface, self.color, self.rect)
