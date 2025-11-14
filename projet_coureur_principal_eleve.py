import pygame, sys
from pygame.locals import *

from projet_coureur_personnage import *
from projet_coureur_arbre import *
from projet_coureur_maison import *

#*************************************************************
# Constantes
WIDTH = 800
HEIGHT = 300
VITESSE = 8  # Vitesse de déplacement du décor
CIEL = (135, 206, 235)  # Bleu ciel

#*************************************************************
# Fonction pour afficher la rue
def affichage_rue(fenetre):
    """Affiche la route grise
    Args:
        fenetre: surface pygame où afficher la route
    """
    pygame.draw.rect(fenetre, (192, 192, 192), (0, 200, WIDTH, HEIGHT//2), 0)

#*************************************************************
# Fonction pour gérer l'apparition infinie des arbres
def gerer_arbres(liste_arbres):
    """Gère l'apparition et la disparition des arbres pour créer un effet infini
    Args:
        liste_arbres: liste des arbres actifs
    """
    # Créer un nouvel arbre si le dernier est assez loin
    if len(liste_arbres) == 0 or liste_arbres[-1].x > 400:
        liste_arbres.append(arbre(WIDTH))
    
    # Afficher et déplacer les arbres
    for arbre_obj in liste_arbres[:]:
        arbre_obj.affichage_arbre(window)
        arbre_obj.bouge_arbre(VITESSE)
        
        # Supprimer les arbres qui ont quitté l'écran
        if arbre_obj.x + arbre_obj.width < 0:
            liste_arbres.remove(arbre_obj)

#*************************************************************
# Fonction pour gérer l'apparition infinie des maisons
def gerer_maisons(liste_maisons):
    """Gère l'apparition et la disparition des maisons pour créer un effet infini
    Args:
        liste_maisons: liste des maisons actives
    """
    # Créer une nouvelle maison si la dernière est assez loin
    if len(liste_maisons) == 0 or liste_maisons[-1].x > 450:
        liste_maisons.append(maison(WIDTH))
    
    # Afficher et déplacer les maisons
    for maison_obj in liste_maisons[:]:
        maison_obj.affichage_maison(window)
        maison_obj.bouge_maison(VITESSE)
        
        # Supprimer les maisons qui ont quitté l'écran
        if maison_obj.x + maison_obj.width < 0:
            liste_maisons.remove(maison_obj)

#*************************************************************
# Programme principal
pygame.init()

# Création de la fenêtre du jeu
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Balade en ville')

# Horloge pour contrôler la vitesse
clock = pygame.time.Clock()

# Création du personnage
sonic = personnage()

# Listes pour les éléments du décor
arbres = []
maisons = []

# Variables de contrôle
clock_speed = 60  # FPS (images par seconde)

#*************************************************************
# Boucle infinie du jeu
while True:
    # Remplir le fond avec le ciel
    window.fill(CIEL)
    
    # Afficher la rue (plan arrière)
    affichage_rue(window)
    
    # Afficher et gérer les maisons (plan intermédiaire)
    gerer_maisons(maisons)
    
    # Afficher et gérer les arbres (plan avant)
    gerer_arbres(arbres)
    
    # Afficher et animer le personnage (au premier plan, position fixe)
    sonic.bouge_personnage(window)
    
    # Gestion des événements (clavier et souris)
    for event in pygame.event.get():
        if event.type == QUIT:  # Croix rouge
            pygame.quit()
            sys.exit()
        
        # Détection des touches de clavier
        if event.type == KEYDOWN:
            # N'importe quelle touche démarre la course
            sonic.demarrer_course()
        
        if event.type == KEYUP:
            # Relâcher la touche arrête la course
            sonic.arreter_course()
    
    # Rafraîchissement de l'écran
    pygame.display.flip()
    
    # Contrôle de la vitesse d'affichage
    clock.tick(clock_speed)






