
#Import des librairies
import pygame
import os
from PIL import Image
import random

#Constantes
code_couleur = {"bleu" : (57, 171, 217), "orange" :(235, 140, 10), "rouge" : (222, 28, 28), "vert" : (60, 200, 53), "jaune" : (229, 226, 34), "violet" : (203, 28, 190), "rose" : (232, 90, 204)}
#Code une fois le pays selectionner
code_selectionner = {"bleu" : (35, 135, 126), "orange" : (194, 119, 16), "rouge" : (149, 32, 23), "vert" : (43, 127, 20), "jaune" : (175, 173, 44), "violet" : (116, 25, 109), "rose": (185, 101, 169)}

#Definition des classes

class Continent:
	def __init__(self, L_pays, bonus_troupes, nom, Map):
		self.nom = nom
		self.pays = []
		self.bonus_troupes = bonus_troupes
		self.nb_pays = None

		#Creation des pays
		for p_nom in L_pays:
			P = Pays(p_nom, nom)
			self.pays.append(P)
			Map.pays.append(P)
		self.nb_pays = len(L_pays)

	def posseder(self):
		"""Verifie quel joueur possede le continent"""
		J = self.pays[0].joueur
		for pays in self.pays:
			if not pays.joueur == J:
				return False
		J.continents.append(self)


class Pays:
	def __init__(self, nom, continent):
		self.nom = nom
		self.continent = continent
		self.joueur = None
		self.troupes = 1
		self.voisins = []
		self.image = None
		self.couleur = None
		self.position = None

	def init_voisin(self, monde):
		"""Converti les indices des voisins en objet"""
		indice = self.voisins.copy()
		self.voisins = []
		for i in indice:
			#print(i)
			self.voisins.append(monde.pays[i-1])


class Joueur:
	def __init__(self, couleur, pseudo, ip):
		self.couleur = couleur
		self.pseudo = pseudo
		self.nbr_troupes = None
		self.pays = []
		self.ip = ip
		self.vivant = True
		self.continents = []

class Carte:
	def __init__(self, nom, bonus, troupe, pays):
		"""Bonus : si la carte contient les 3 troupes"""
		self.nom = nom
		self.bonus = bonus
		self.troupe = troupe
		self.pays = pays


class Map:
	def __init__(self, nom):
		self.nom = nom
		self.continents = []
		self.pays = []
		self.path = ""
		self.color_pays = {} #dictionnaire str(code couleur) : pays
		self.image = None

		#Donnees si la map choisi est la Terre
		if nom == 'Terre':
			self.path = "Img_Terre"

			self.continents.append(Continent(['Congo','Affrique de l\'Est','Egypte','Madagascar','Afrique du Nord','Afrique du Sud']
											,3,'Afrique', self))
			self.continents.append(Continent(['Alaska','Alberta','Amerique Centrale','Etats de l\'Est','Groenland','Territoires du Nord-Ouest','Ontario','Quebec','Etats de l\'Ouest']
											,5,'Amerique du Nord', self))
			self.continents.append(Continent(['Venezuela','Bresil','Perou','Argentine']
											,2,'Amerique du Sud', self))
			self.continents.append(Continent(['Afghanistan','Chine','Inde','Tchita','Japon','Kamchatka','Moyen-Orient','Mongolie','Siam','Siberie','Oural','Yakoutie']
											,7,'Asie', self))
			self.continents.append(Continent(['Grande-Bretagne','Islande','Europe du Nord','Scandinavie','Europe du Sud','Ukraine','Europe Occidentale']
											,5,'Europe', self))
			self.continents.append(Continent(['Australie Orientale','Indonésie','Nouvelle-Guinée','Australie Occidentale']
											,2,'Oceanie', self))

			#Initialise les voisins de chaque pays
			self.continents[0].pays[0].voisins=[2,5,6]
			self.continents[0].pays[1].voisins=[1,3,4,5,6,26]
			self.continents[0].pays[2].voisins=[2,5,36,26]
			self.continents[0].pays[3].voisins=[2,6]
			self.continents[0].pays[4].voisins=[1,2,3,17,36,38]
			self.continents[0].pays[5].voisins=[1,2,4]
			self.continents[1].pays[0].voisins=[8,12,25]
			self.continents[1].pays[1].voisins=[7,12,13,15]
			self.continents[1].pays[2].voisins=[15,10,19]#Am centrale
			self.continents[1].pays[3].voisins=[9,15,13,14]#10
			self.continents[1].pays[4].voisins=[12,13,14,33]
			self.continents[1].pays[5].voisins=[7,8,13,11]
			self.continents[1].pays[6].voisins=[8,15,10,14,11,12]
			self.continents[1].pays[7].voisins=[10,13,11]
			self.continents[1].pays[8].voisins=[9,10,8,13]
			self.continents[2].pays[0].voisins=[17,18]
			self.continents[2].pays[1].voisins=[16,18,19,5]
			self.continents[2].pays[2].voisins=[16,17,19]
			self.continents[2].pays[3].voisins=[18,17,9]#Argentine
			self.continents[3].pays[0].voisins=[21,22,26,30,37]#20
			self.continents[3].pays[1].voisins=[20,22,28,27,29,30]
			self.continents[3].pays[2].voisins=[20,21,26,28]
			self.continents[3].pays[3].voisins=[29,27,25,31]
			self.continents[3].pays[4].voisins=[27,25]
			self.continents[3].pays[5].voisins=[31,23,27,24,7]
			self.continents[3].pays[6].voisins=[20,22,37,2,3]
			self.continents[3].pays[7].voisins=[24,21,29,25,23]
			self.continents[3].pays[8].voisins=[21,22,40]
			self.continents[3].pays[9].voisins=[30,21,23,31,27]
			self.continents[3].pays[10].voisins=[20,21,29,37]#30
			self.continents[3].pays[11].voisins=[29,23,25]
			self.continents[4].pays[0].voisins=[33,35,34,38]
			self.continents[4].pays[1].voisins=[32,35,11]
			self.continents[4].pays[2].voisins=[32,35,37,36,38]
			self.continents[4].pays[3].voisins=[37,32,33,34]
			self.continents[4].pays[4].voisins=[38,34,37,3,26,5]
			self.continents[4].pays[5].voisins=[35,34,36,20,26,30]
			self.continents[4].pays[6].voisins=[32,34,36,5]
			self.continents[5].pays[0].voisins=[42,41]
			self.continents[5].pays[1].voisins=[42,41,28]#40
			self.continents[5].pays[2].voisins=[42,40,39]
			self.continents[5].pays[3].voisins=[39,41,40]

			#Initialise toutes les couleurs de pays
			self.continents[0].pays[0].couleur=(153,0,0)
			self.continents[0].pays[1].couleur=(153,76,0)
			self.continents[0].pays[2].couleur=(153,153,0)
			self.continents[0].pays[3].couleur=(76,153,0)
			self.continents[0].pays[4].couleur=(0,153,0)
			self.continents[0].pays[5].couleur=(0,153,76)
			self.continents[1].pays[0].couleur=(0,153,153)
			self.continents[1].pays[1].couleur=(0,76,153)
			self.continents[1].pays[2].couleur=(0,0,153)
			self.continents[1].pays[3].couleur=(76,0,153)
			self.continents[1].pays[4].couleur=(153,0,153)
			self.continents[1].pays[5].couleur=(153,0,76)
			self.continents[1].pays[6].couleur=(64,64,64)
			self.continents[1].pays[7].couleur=(204,0,0)
			self.continents[1].pays[8].couleur=(204,102,0)
			self.continents[2].pays[0].couleur=(204,204,0)
			self.continents[2].pays[1].couleur=(102,204,0)
			self.continents[2].pays[2].couleur=(0,204,0)
			self.continents[2].pays[3].couleur=(0, 204, 102)
			self.continents[3].pays[0].couleur=(0,204,204)
			self.continents[3].pays[1].couleur=(0,102,204)
			self.continents[3].pays[2].couleur=(0,0,204)
			self.continents[3].pays[3].couleur=(102,0,204)
			self.continents[3].pays[4].couleur=(204,0,204)
			self.continents[3].pays[5].couleur=(204,0,102)
			self.continents[3].pays[6].couleur=(96,96,96)
			self.continents[3].pays[7].couleur=(255,0,0)
			self.continents[3].pays[8].couleur=(255,128,0)
			self.continents[3].pays[9].couleur=(255,255,0)
			self.continents[3].pays[10].couleur=(128,255,0)
			self.continents[3].pays[11].couleur=(0,255,0)
			self.continents[4].pays[0].couleur=(0,255,128)
			self.continents[4].pays[1].couleur=(0,255,255)
			self.continents[4].pays[2].couleur=(0,128,255)
			self.continents[4].pays[3].couleur=(0,0,255)
			self.continents[4].pays[4].couleur=(127,0,255)
			self.continents[4].pays[5].couleur=(255,0,255)
			self.continents[4].pays[6].couleur=(255,0,127)
			self.continents[5].pays[0].couleur=(128,128,128)
			self.continents[5].pays[1].couleur=(255,51,51)
			self.continents[5].pays[2].couleur=(255,153,51)
			self.continents[5].pays[3].couleur=(255,255,51)

			#Initialise la position des texte du nombre de troupe
			self.continents[0].pays[0].position=(652, 361)
			self.continents[0].pays[1].position=(707, 317)
			self.continents[0].pays[2].position=(646, 244)
			self.continents[0].pays[3].position=(746, 448)
			self.continents[0].pays[4].position=(559, 272)
			self.continents[0].pays[5].position=(657, 459)
			self.continents[1].pays[0].position=(85, 72)
			self.continents[1].pays[1].position=(149, 114)
			self.continents[1].pays[2].position=(136, 254)
			self.continents[1].pays[3].position=(213, 196)
			self.continents[1].pays[4].position=(448, 38)
			self.continents[1].pays[5].position=(188, 71)
			self.continents[1].pays[6].position=(234, 117)
			self.continents[1].pays[7].position=(313, 112)
			self.continents[1].pays[8].position=(134, 177)
			self.continents[2].pays[0].position=(296, 510)
			self.continents[2].pays[1].position=(348, 413)
			self.continents[2].pays[2].position=(284, 431)
			self.continents[2].pays[3].position=(249, 335)
			self.continents[3].pays[0].position=(804, 157)
			self.continents[3].pays[1].position=(913, 196)
			self.continents[3].pays[2].position=(874, 251)
			self.continents[3].pays[3].position=(944, 112)
			self.continents[3].pays[4].position=(1096, 198)
			self.continents[3].pays[5].position=(1068, 69)
			self.continents[3].pays[6].position=(725, 219)
			self.continents[3].pays[7].position=(965, 156)
			self.continents[3].pays[8].position=(969, 279)
			self.continents[3].pays[9].position=(862, 64)
			self.continents[3].pays[10].position=(801, 89)
			self.continents[3].pays[11].position=(978, 69)
			self.continents[4].pays[0].position=(553, 120)
			self.continents[4].pays[1].position=(506, 73)
			self.continents[4].pays[2].position=(600, 128)
			self.continents[4].pays[3].position=(605, 86)
			self.continents[4].pays[4].position=(643, 161)
			self.continents[4].pays[5].position=(701, 109)
			self.continents[4].pays[6].position=(567, 147)
			self.continents[5].pays[0].position=(1139, 475)
			self.continents[5].pays[1].position=(1028, 358)
			self.continents[5].pays[2].position=(1139, 383)
			self.continents[5].pays[3].position=(1048, 480)

			for P in self.pays:
				P.init_voisin(self)
				#Atribution des couleurs pour reperage sur la carte
				self.color_pays[str(P.couleur)] = P




class Fenetre:
	def __init__(self, fenetre, monde, clock, joueurs):
		self.fenetre = fenetre
		self.monde = monde
		self.clock = clock
		self.color_map = None
		self.tour = None
		self.joueurs = joueurs
		self.select = None                  #Dernier pays selectionner
		self.precedent = None               #Pays selectionnee precedemment
		self.units = 1                      #Troupes choisis pour agir
		self.Next = pygame.Rect(850, 630, 100, 70)  #Rectangle du bouton Next

		#Ajout background
		self.background = pygame.image.load(self.monde.path + "/background.jpg").convert()
		self.fenetre.blit(self.background, (0,0))

		#Initialise l'image avec les couleurs de pays pour position de la souris
		self.jonction = pygame.image.load(self.monde.path + "/Risk_game_map_fixed_greylevel.png").convert_alpha()
		#self.color_map.set_colorkey((0,0,0)) #Rend le noir de l'image transparent
		self.fenetre.blit(self.jonction, (0,0))
		
		#Attribution des troupes et pays
		self.distribution_debut()

		path = self.monde.path + "/Maps/"
		for i, file in enumerate(os.listdir(path)):
			pays = pygame.image.load(path + file).convert_alpha()
			pays.set_colorkey((255,255,255))
			self.monde.pays[i].image = pays

		#Ajout de tous pays
		for P in self.monde.pays:
			self.colorisation_pays(P, code_couleur[P.joueur.couleur])
			self.affiche_troupes(P)

		self.bouton_next_init()

		#Initialise le premier tour
		self.tour = Tour(self, joueurs, monde)
		self.informations()

		#Mise à jour de l'affichage
		pygame.display.flip()

	def afficher(self, Etat_jeu):
		"""On rentre dans l'affichage evolutif du jeu"""
		while Etat_jeu:
			for event in pygame.event.get():    #Attente des événements
				if event.type == pygame.QUIT:
					pygame.quit()
				if event.type == pygame.MOUSEBUTTONDOWN:
					if event.button == 1:   #Si clic gauche
						pos = pygame.mouse.get_pos()
						print(pos)

						#Fonction si le bouton next est appuye
						if pygame.Rect.collidepoint(self.Next, pos):
							self.bouton_next()

						#obtient la couleur du pays sous la souris
						PIL_color_map = Image.open(self.monde.path + "/color_map.png")
						try:
							color_pixel = str(PIL_color_map.getpixel(pos))
						except:
							continue

						#Fonctionne si un pays a ete selectionner
						try : 
							pays_clique = self.monde.color_pays[color_pixel]

							if self.tour.phase == 0:
								self.click_phase_placement(pays_clique)

							elif self.tour.phase == 1:
								self.click_phase_attaque(pays_clique)

							elif self.tour.phase == 2:
								self.click_phase_renforcement(pays_clique)

						except :
							continue

					if event.button == 3:  #Annule la selection si clic droit
						if self.select:
							self.deselectionne_pays()

					try:
						if event.button==4:#scroll wheel up
							if self.units < self.choix_nombre():
								print("test")
								self.units+=1

						elif event.button==5:#scroll wheel down
							if self.units>1:
								self.units-=1
					except:
						continue

			self.informations()

			#Mise à jour de l'affichage
			pygame.display.flip()


	def informations(self):
		"""Affiche les information de la partie"""
		position = (40, 590, 250, 150)
		fond = (226, 208, 125)
		contour = (189, 174, 107)
		titre = "INFORMATIONS :"
		if self.units > self.tour.j_actuel.nbr_troupes:
			self.units = self.tour.j_actuel.nbr_troupes
		text1 = "Troupes à déployer : %i"%(self.tour.j_actuel.nbr_troupes)
		text2 = "Troupes selectionner : %i"%(self.units)
		text3 = "Pays possédés : %i"%(len(self.tour.j_actuel.pays))
		text4 = "Continents possédés : %i"%(len(self.tour.j_actuel.continents))
		T = [text1, text2, text3, text4]

		pygame.draw.rect(self.fenetre, fond, position)
		pygame.draw.rect(self.fenetre, contour, position, width = 3)

		#Titre
		Police = pygame.font.Font('freesansbold.ttf', 20)
		pygame.font.Font.set_underline(Police, True)
		text = Police.render(titre, True , (0,0,0))
		self.fenetre.blit(text, (80, 600))

		for i, text in enumerate(T):
			Police = pygame.font.Font('freesansbold.ttf', 18)
			text = Police.render(text, True , (0,0,0))

			_, _, motx, moty = pygame.Surface.get_bounding_rect(text)
			x = (250//2) - (motx//2) + 40

			self.fenetre.blit(text, (x, 630 + i*25))


	def choix_nombre(self):
		"""Retourne le maximum de troupes possible suivant la phase"""
		if self.precedent:
			self.tour.j_actuel.nbr_troupes = self.precedent.nbr_troupes
		elif self.tour.phase != 0:
			self.tour.j_actuel.nbr_troupes = 0
		return self.tour.j_actuel.nbr_troupes


	def click_phase_placement(self, pays_clique):
		"""Action apres le click si on est dans la pahse de placement""" 
		if pays_clique.joueur == self.tour.j_actuel:
			#Si rien n'est selectionner, ajoute juste un pays
			if not self.select:
				self.select = pays_clique
				self.couleur_pays_selectionner()

			#Si le meme pays etait selectionner, le valide (double click)
			elif self.select == pays_clique:
				self.tour.tour()

			#Si un autre pays etait deja selectionner
			else:
				self.precedent = self.select
				self.select = pays_clique
				self.couleur_pays_selectionner()


	def click_phase_attaque(self, pays_clique):
		"""Action apres le click si on est dans la phase d'attaque"""

		#Si le pays appartient au joueur
		if pays_clique.joueur == self.tour.j_actuel:
			#Si rien n'est selectionner, ajoute juste un pays
			if not self.select:
				self.select = pays_clique
				self.couleur_pays_selectionner()

			#Si un autre pays etait deja selectionner et qu'il appartenait au joueur
			#Changement d'attaquant
			else:
				self.deselectionne_pays()
				self.select = pays_clique
				self.couleur_pays_selectionner()

		else:
			#Selection de la cible
			if self.select.joueur  == self.tour.j_actuel and pays_clique in self.select.voisins:
				self.precedent = self.select
				self.select = pays_clique
				self.couleur_pays_selectionner(zero = False)

			#Validation de la cible (double click)
			elif self.select == pays_clique:
				#Victoire
				if self.tour.tour():
					self.deselectionne_pays()
					self.select = pays_clique
					self.couleur_pays_selectionner()

			#Changement de cible
			elif pays_clique in self.precedent.voisins:
				self.deselectionne_pays(zero = False)
				self.select = pays_clique
				self.couleur_pays_selectionner(zero = False)


	def click_phase_renforcement(self, pays_clique):
		"""Action apres le click si on est dans la phase de renforcement"""

		#Si le pays appartient au joueur
		if pays_clique.joueur == self.tour.j_actuel:
			#Si rien n'est selectionner, ajoute juste un pays
			if not self.select:
				self.select = pays_clique
				self.couleur_pays_selectionner()

			#Si un autre pays etait deja selectionner et qu'il appartient au joueur
			elif self.select.joueur == self.tour.j_actuel:
				if not self.precedent:
					#Si aucune cible n'est selectionner, devient la cible
					if self.chemin_placement(pays_clique):
						self.precedent = self.select
						self.select = pays_clique
						self.couleur_pays_selectionner(zero = False)

					#Changement d'attaquant sans cible
					else:
						self.deselectionne_pays()
						self.select = pays_clique
						self.couleur_pays_selectionner()

				elif self.select == pays_clique:    #Double click
						self.tour.tour()

				#Changement de cible
				elif self.chemin_placement(pays_clique):
					self.deselectionne_pays(zero = False)
					self.select = pays_clique
					self.couleur_pays_selectionner(zero = False)

				#Changement d'attaquant si c'est trop loin apres selection de cible
				else:
					self.deselectionne_pays()
					self.select = pays_clique
					self.couleur_pays_selectionner()


	def chemin_placement(self, cible):
		"""Verifie si il y a un chemin entre les cibles, cherche toutes les destinations possible du pays de depart"""
		debut = self.select
		deja_fait = [debut]     #tous les pays
		for i in deja_fait:
			for pays in i.voisins:
				if pays.joueur == self.tour.j_actuel and pays not in deja_fait:
					deja_fait.append(pays)
		deja_fait.remove(debut)

		if cible in deja_fait:
			return True


	def bouton_next(self):
		"""Anime le bouton next et passe au tour suivant"""
		self.bouton_next_init(appuyer = True)
		pygame.display.flip()
		pygame.time.delay(150)
		self.bouton_next_init()
		if self.select:
			self.deselectionne_pays()

		self.tour.next()


	def bouton_next_init(self, appuyer = False):
		"""Affiche le bouton next"""
		position = self.Next
		couleur_classique = ((209, 67, 123), (176, 57, 104))
		couleur_appuyer = ((187, 31, 93), (147, 22, 72))

		couleur = couleur_classique

		if appuyer:
			couleur = couleur_appuyer

		self.joli_rectangle(position, couleur[0], couleur[1], "Next")


	def deselectionne_pays(self, zero = True):
		"""Deselectionne le dernier pays et le precedent si zero"""
		self.colorisation_pays(self.select, code_couleur[self.select.joueur.couleur])
		self.affiche_troupes(self.select)
		self.select = None
		if self.precedent and zero:
			self.colorisation_pays(self.precedent, code_couleur[self.precedent.joueur.couleur])
			self.affiche_troupes(self.precedent)
			self.precedent = None


	def couleur_pays_selectionner(self, zero = True):
		"""Change la couleur du pays selectionner. Remet le precedent dans sa couleur d'origine si zero = True"""
		if self.select.couleur != code_selectionner[self.select.joueur.couleur]:
			self.colorisation_pays(self.select, code_selectionner[self.select.joueur.couleur])
			self.affiche_troupes(self.select)
			if self.precedent and zero:
				self.colorisation_pays(self.precedent, code_couleur[self.precedent.joueur.couleur])
				self.affiche_troupes(self.precedent)


	def colorisation_pays(self, P, toCouleur):
		"""Colorie les pays en fonction du code couleur"""
		self.change_couleur(P, toCouleur)
		self.fenetre.blit(P.image, (0,0))
		P.couleur = toCouleur


	def change_couleur(self, P, toCouleur):
		"""Juste pour blit sinon il lock la surface dans la meme fonction"""
		var = pygame.PixelArray(P.image)
		# var.replace(([Colour you want to replace]), [Colour you want])
		var.replace((P.couleur), (toCouleur))


	def distribution_debut(self):
		"""Distribution des troupes et pays de depart, place aleatoirement les troupes sur les pays"""
		#Nombre de troupes par joueur
		nb_players = len(self.joueurs)

		if nb_players==3:
			nb_troupes=35
		elif nb_players==4:
			nb_troupes=30
		elif nb_players==5:
			nb_troupes=25
		elif nb_players==6:
			nb_troupes=20

		#Attribution des troupes
		for J in self.joueurs:
			J.nbr_troupes = nb_troupes

		#Attribution des pays aleatoirement
		Liste = self.monde.pays.copy()
		random.shuffle(Liste)
		nb_continents = len(self.monde.pays)
		n = nb_continents // nb_players
		for y,i in enumerate(range(0, len(Liste),n)):
			if y < nb_players :
				#Les joueurs recoivent n pays
				self.joueurs[y].pays = Liste[i:i+n]
			else:
				#Le reste est distribuer aléatoirement
				for pays_restant in Liste[i:i+n]:
					self.joueurs[random.randint(0,len(self.joueurs)-1)].pays.append(pays_restant)

		#Donne à chaque pays le joueur qui le possede
		for J in self.joueurs:
			for pays in J.pays:
				pays.joueur = J

			#Distribue les troupes par pays
			for i in range(J.nbr_troupes - len(J.pays)):
				P = random.choice(J.pays)
				P.troupes += 1

			J.nbr_troupes =0


	def affiche_troupes(self, pays):
		"""Affiche les troupes du pays"""
		Police = pygame.font.Font('freesansbold.ttf',16)
		text = Police.render(str(pays.troupes) , True , (0,0,0))
		x, y = pays.position
		_, _, motx, moty = pygame.Surface.get_bounding_rect(text)
		cooX = x - motx//2
		cooY = y - moty//2
		self.fenetre.blit(text, (cooX, cooY))


	def joli_rectangle(self, position, fond, contour, contenu, taille_texte = 24):
		"""Dessine un joli rectangle avec du texte dessus"""
		pygame.draw.rect(self.fenetre, fond, position)
		pygame.draw.rect(self.fenetre, contour, position, width = 3)

		Police = pygame.font.Font('freesansbold.ttf', taille_texte)
		text = Police.render(contenu, True , (0,0,0))
		_, _, motx, moty = pygame.Surface.get_bounding_rect(text)
		x1, y1, x2, y2 = position
		cooX = (x2//2) - (motx//2) + x1
		cooY = (y2//2) - (moty//2) + y1
		self.fenetre.blit(text, (cooX,cooY))


class Tour:
	def __init__(self, fenetre, joueurs, monde):
		self.numero_tour = 0
		self.fenetre = fenetre
		self.monde = monde
		self.ordre_joueurs = joueurs.copy()
		random.shuffle(self.ordre_joueurs)

		self.i_actuel = 0           #Indice du joueur actuel dans ordre_joueurs
		self.j_actuel = None
		self.Liste_phases = ["Placement", "Attaque", "Renforcement"]
		self.phase = None

		#Initialise le tour du premier joueur
		self.j_actuel = self.ordre_joueurs[0]
		self.phase = 0
		self.nouveau_tour()

	def next(self):
		"""Passe a la phase/joueur/tour suivant"""
		#Phase suivante
		if self.phase < 2:
			self.phase += 1
		else:
			#Joueur suivant
			self.phase = 0
			if self.i_actuel < len(self.ordre_joueurs)-1:
				self.i_actuel += 1
				self.j_actuel = self.ordre_joueurs[self.i_actuel]
			#Tour suivant
			else:
				self.numero_tour += 1
				self.i_actuel = 0
				self.j_actuel = self.ordre_joueurs[0]

				#Reinitialise les listes de continents
				for J in self.fenetre.joueurs:
					J.continents = []

				#Ajoute les continents aux joueurs
				for C in self.monde.continents:
					C.posseder()

		self.nouveau_tour()


	def nouveau_tour(self):
		"""Initialisation du tour a chaque nouveau tour"""
		if self.phase == 0:
			self.phase_placement()
		self.affiche_joueurs()
		self.affiche_phase()


	def tour(self):
		"""Determine l'action a faire apres qu'un pays soit selectionner"""
		if self.phase == 0:
			self.placement_joueur(self.fenetre.select)
		elif self.phase == 1:
			return self.attaque()
		elif self.phase == 2:
			self.renforcement()

	def affiche_joueurs(self):
		"""Affiche tous les joueurs"""
		taille_act = (170,60)
		taille = (120, 40)
		pos = 30

		self.fenetre.fenetre.blit(self.fenetre.background, (1180, 30), (1180, 30, 170, 270))

		for i, J in enumerate(self.ordre_joueurs):
			if J == self.j_actuel:
				position = (1180, pos, taille_act[0], taille_act[1])
				fond = code_couleur[J.couleur]
				contour = code_selectionner[J.couleur]
				contenu = J.pseudo
				taille_texte = 24
				pos += 70

			else:
				position = (1180 + 40, pos, taille[0], taille[1])
				fond = code_couleur[J.couleur]
				contour = code_selectionner[J.couleur]
				contenu = J.pseudo
				taille_texte = 18
				pos += 50

			self.fenetre.joli_rectangle(position, fond, contour, contenu, taille_texte = taille_texte)

	def affiche_phase(self):
		"""Affiche la phase actuelle"""
		position = (385, 620, 445, 95)
		fond = (191, 133, 121)
		contour = (175, 100, 85)
		contenu = self.Liste_phases[self.phase]

		self.fenetre.joli_rectangle(position, fond, contour, contenu)


	def phase_placement(self):
		"""Attribue des nouvelles troupes au joueur"""
		#Verifie les continents possede
		J = self.j_actuel
		J.nbr_troupes = 3
		for C in J.continents:
			J.nbr_troupes += C.bonus_troupes


	def placement_joueur(self, pays):
		"""ajoute le nombre de troupes choisi au pays"""
		if self.j_actuel.nbr_troupes > 0:
			pays.troupes += self.fenetre.units
			self.fenetre.colorisation_pays(pays, pays.couleur)
			self.fenetre.affiche_troupes(pays)
			self.j_actuel.nbr_troupes -= self.fenetre.units


	def attaque(self):
		"""A l'abordaaaaaage, return True si victoire"""
		attaquant = self.fenetre.precedent
		defense = self.fenetre.select
		nbr_a, nbr_d = self.resultat_attaque(attaquant.troupes, defense.troupes)

		#Victoire attaquant
		if nbr_d == 0:
			attaquant.troupes = 1
			defense.troupes = nbr_a - 1
			defense.joueur.pays.remove(defense)
			attaquant.joueur.pays.append(defense)
			defense.joueur = attaquant.joueur

		#Victoire defense
		else:
			attaquant.troupes = 1
			defense.troupes = nbr_d
		
		self.fenetre.colorisation_pays(attaquant, code_selectionner[attaquant.joueur.couleur])
		self.fenetre.affiche_troupes(attaquant)
		self.fenetre.colorisation_pays(defense, code_selectionner[defense.joueur.couleur])
		self.fenetre.affiche_troupes(defense)
		
		if nbr_d == 0:
			return True
		else:
			return False


	def resultat_attaque(self, unit_att , unit_def):
		"""Renvoit le nombre d'unité de chaque parti"""
		while (unit_att > 1) and (unit_def > 0) :
			if unit_att > 3 :
				nb_des_att=3 #combien de des a l attaquant
			des_att = self.des(unit_att)
			if unit_def <= 2:
				des_def = self.des(1) #combien de des a la defense
			else : des_def = self.des(2)
			for j in range(len(des_def)): #on compare les listes
				if des_att[j] > des_def[j] :
					unit_def-=1
				else :
					unit_att-=1
		return unit_att , unit_def


	def des(self, nb_lance):
		"""lance le nombre de dé en argument et ajoute dans une liste"""
		result=[]
		for i in range(nb_lance):
			result.append(random.randint(1,6))
		result.sort(reverse=True)
		return result


	def renforcement(self):
		attaquant = self.fenetre.precedent
		defense = self.fenetre.select
		defense.troupes += attaquant.troupes
		attaquant.troupes = 1

		self.fenetre.deselectionne_pays()
		self.next()