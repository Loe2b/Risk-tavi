 #RiskTaVi

#Import libraries
import pygame

#Import autres fichiers
from Class import *

#Constantes
f_w, f_h = 1380, 800 #dimension fenetre

#Variables
Etat_jeu = True #true si le jeu continue, False sinon

def game_test():
    joueur1 = Joueur("orange", "joueur1","0")
    joueur2 = Joueur("rouge", "joueur2","0")
    joueur3 = Joueur("vert", "joueur3", "0")
    joueur4 = Joueur("jaune", "joueur4", "0")
    joueur5 = Joueur("violet", "joueur5", "0")
    return [joueur1, joueur2, joueur3, joueur4, joueur5]

if __name__ == '__main__':
    #Initialisation partie et fenetre
    Monde = Map("Terre")
    pygame.init()
    clock = pygame.time.Clock()
    fenetre = pygame.display.set_mode((f_w, f_h))
    fen = Fenetre(fenetre, Monde, clock, game_test())
    clock.tick(60)

    fen.afficher(Etat_jeu)