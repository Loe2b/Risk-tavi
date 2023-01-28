#Import libraries
import pygame
from tkinter import *
from tkinter import ttk

#Import autres fichiers
from Class import *

#Constantes
f_w, f_h = 1380, 800 #dimension fenetre

#Variables
Etat_jeu = True #true si le jeu continue, False sinon
couleurs = ["bleu", "orange", "rouge", "vert", "jaune", "violet"]

class Input:

	def __init__(self):
		self.root = Tk()
		self.root.title('Risk\'tavi')
		frm = ttk.Frame(self.root, padding=10)
		frm.grid()
		ttk.Label(frm, text="Nombre de joueur :").grid(column=0, row=0)

		self.current = StringVar(value=3)
		self.nbr_joueurs = int(self.current.get())
		s = ttk.Spinbox(frm, from_=3, to=6, textvariable=self.current, command=self.changed)
		s.grid(column=0, row=1)

		ttk.Button(frm, text="Quitter", command=self.root.destroy).grid(column=0, row=2, columnspan=2)
		ttk.Button(frm, text="Suivant", command=self.suivant).grid(column=1, row=2)
		self.root.mainloop()

	def changed(self):
		"""Permet de changer le nombre de joueur"""
		self.nbr_joueurs = int(self.current.get())


	def suivant(self):
		self.root.destroy()
		self.root = Tk()
		self.root.title('Risk\'tavi')
		self.frm = ttk.Frame(self.root, padding=10)
		frm = self.frm
		frm.grid()
		ttk.Label(frm, text="Choix du nom :").grid(column=0, row=0)

		self.zone_entree = []
		self.noms = []
		self.clr = couleurs[:self.nbr_joueurs]

		for i in range(self.nbr_joueurs): 
			entree = Entree_nom(self, frm, i)
			self.zone_entree.append(entree)
			option_menu = Option_menu(self, frm, i)
			self.noms.append("Joueur %i"%(i+1))

		self.alert = Label(self.frm, fg = 'white', text="Attention! La couleur random \na été selectionner plusieurs fois !")
		self.alert.grid(row=self.nbr_joueurs+2)

		ttk.Button(frm, text="Quitter", command=self.root.destroy).grid(column=0, row=self.nbr_joueurs+3, columnspan=2)
		ttk.Button(frm, text="Jouer !", command=self.jouer).grid(column=1, row=self.nbr_joueurs+3)
		self.root.mainloop()


	def jouer(self):
		#verifie que chaque couleur est differente et lance le jeu
		for c in couleurs:
			if self.clr.count(c) > 1:
				self.alert = ttk.Label(self.frm, text="Attention! La couleur %s \na été selectionner plusieurs fois !"%(c))
				self.alert.grid(row=self.nbr_joueurs+2)
				return False
		self.root.destroy()
		self.creer_jeu()


	def creer_jeu(self):
		"""Initialisation de la liste de joueur et de la fenetre de jeu"""
		joueurs = []
		for i in range(self.nbr_joueurs):
			self.zone_entree[i].get_nom()
			J = Joueur(self.clr[i], self.noms[i], "0")
			joueurs.append(J)

		#Initialisation partie et fenetre
		Monde = Map("Terre")
		pygame.init()
		clock = pygame.time.Clock()
		fenetre = pygame.display.set_mode((f_w, f_h))
		pygame.display.set_caption("Risk'tavi")
		fen = Fenetre(fenetre, Monde, clock, joueurs)
		clock.tick(60)

		fen.afficher(Etat_jeu)


class Entree_nom:
	def __init__(self, fenetre, frm, i):
		"""Classe qui permet de choisir les noms"""
		self.fen = fenetre
		self.i = i
		self.value = StringVar()
		self.value.set("Joueur %i"%(i+1))
		self.entree = Entry(frm, textvariable=self.value, width=30)
		self.entree.grid(column=0, row=i+1)

	def get_nom(self, *args):
		self.fen.noms[self.i] = self.value.get()

class Option_menu:
	def __init__(self, fenetre, frm, i):
		"""Classe qui permet de creer les Options menu, pour choisir les couleurs"""
		self.fen = fenetre
		self.i = i
		self.option_var = StringVar()
		self.option_menu = ttk.OptionMenu(frm, self.option_var, couleurs[i], *couleurs, command=self.get_color)
		self.option_menu.grid(column=1, row=i+1)

	def get_color(self, *args):
		self.fen.clr[self.i] = self.option_var.get()


if __name__ == '__main__':
	Fen = Input()