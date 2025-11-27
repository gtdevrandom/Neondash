import pygame, sys
from pygame.locals import *

#*************************************************
class Cube:
	def __init__(self, x, y, size=40, color=(255, 255, 0), speed=200):
		self.rect = pygame.Rect(x, y, size, size)
		self.color = color
		self.speed = float(speed)  # pixels per second
		self.angle = 0  # angle de rotation en degrés
		try:
			self.skin = pygame.image.load('textures/cubes/cubes.png').convert_alpha()
			self.skin = pygame.transform.scale(self.skin, (size, size))
		except Exception:
			self.skin = None

	def update(self, dt):
		# move according to speed (pixels per second)
		self.rect.x -= int(self.speed * dt)

	def rotate(self, angle):
		self.angle = (self.angle + angle) % 360

	def draw(self, surface):
		if self.skin:
			rotated_skin = pygame.transform.rotate(self.skin, self.angle)
			rotated_rect = rotated_skin.get_rect(center=self.rect.center)
			surface.blit(rotated_skin, rotated_rect)
		else:
			# Pour le carré, on dessine aussi avec rotation
			s = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
			pygame.draw.rect(s, self.color, (0, 0, self.rect.width, self.rect.height))
			rotated_s = pygame.transform.rotate(s, self.angle)
			rotated_rect = rotated_s.get_rect(center=self.rect.center)
			surface.blit(rotated_s, rotated_rect)
