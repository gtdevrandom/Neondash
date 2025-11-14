import pygame, sys
import random
from pygame.locals import *

#*************************************************
# Classe pour gérer les arbres du décor
class arbre:
    
    # Liste des images d'arbres disponibles
    images_arbres = [
        'arbre/arbre1.png',
        'arbre/arbre2.png',
        'arbre/arbre3.png',
        'arbre/arbre4.png'
    ]
    
    def __init__(self, x):
        """Constructeur - crée un arbre à la position x
        Args:
            x: position horizontale initiale de l'arbre
        """
        # Choisir une image aléatoire parmi les arbres disponibles
        image_path = random.choice(self.images_arbres)
        try:
            self.image = pygame.image.load(image_path).convert_alpha()
        except:
            # Si l'image ne charge pas, utiliser l'image PNG par défaut
            self.image = pygame.image.load('arbre/arbre1.png').convert_alpha()
        
        self.x = x
        self.y = 60
        self.width = self.image.get_width()
        self.height = self.image.get_height()
    
    def affichage_arbre(self, fenetre):
        """Affiche l'arbre à l'écran
        Args:
            fenetre: surface pygame où afficher l'arbre
        """
        fenetre.blit(self.image, (self.x, self.y))
    
    def bouge_arbre(self, vitesse):
        """Déplace l'arbre vers la gauche (l'arbre se rapproche du personnage)
        Args:
            vitesse: vitesse de déplacement en pixels par frame
        """
        self.x -= vitesse
