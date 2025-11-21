import pygame, sys
from pygame.locals import *


#****************************************

class personnage:
    def __init__(self, x, y, size=50, color=(0, 128, 255), speed=200, screen_height=600):
        self.rect = pygame.Rect(int(x), int(y), int(size), int(size))
        self.color = color
        self.speed = float(speed)
        self.screen_height = int(screen_height)
        self.vel_y = 0.0
        self.gravity = 900  # pixels/sec^2
        self.jump_strength = -500  # vitesse de saut (négatif = vers le haut)
        # Chargement du skin
        try:
            self.skin = pygame.image.load('perso/personnage/personnage.png').convert_alpha()
            self.skin = pygame.transform.scale(self.skin, (size, size))
        except Exception:
            self.skin = None


    def jump(self):
        # Saut uniquement si au sol
        if self.rect.bottom >= self.screen_height:
            self.vel_y = self.jump_strength


    # move_down n'est plus utilisé, la gravité gère la descente


    def stop(self):
        pass  # Ne rien faire, la gravité s'applique toujours


    def set_velocity(self, vy):
        self.vel_y = float(vy)


    def update(self, dt):
        # Appliquer la gravité
        self.vel_y += self.gravity * dt
        dy = self.vel_y * float(dt)
        self.rect.y += int(dy)

        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = 0
        if self.rect.bottom >= self.screen_height:
            self.rect.bottom = self.screen_height
            self.vel_y = 0

    def draw(self, surface):
        if self.skin:
            surface.blit(self.skin, self.rect)
        else:
            pygame.draw.rect(surface, self.color, self.rect)













#     #consctructeur de la classe
#     def __init__(self):

#         perso = pygame.image.load('sonic_104_114.png').convert_alpha()
#         self.image=[]
#         for x in range(0,9*104, 104):
#             self.image.append(perso.subsurface(x,0,104,114))

#         self.index=0

# #fonction permettant d'affichr le personnage dans notre fenétre
#     def affichage_personnage(self,fenetre,index_image):
#         #blit permet d'afficher un elément à l'écran
#         fenetre.blit(self.image[index_image],(400,170))

# #fonction faisant bouger le perso
#     def bouge_personnage(self,fenetre):
#         self.index = self.index +1
#         if self.index == len(self.image):
#             self.index=0

#         self.affichage_personnage(fenetre,self.index)
