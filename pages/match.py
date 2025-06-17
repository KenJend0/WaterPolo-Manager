from joueur import Joueur
from ballon import Ballon
import random as r
import math
import config
import pygame
import copy
import time
from modules.moteur.actions import tir, passe, recup_ballon, resultat_tir
from modules.moteur.engagement import engagement
from modules.moteur.decision import choix_joueur

from modules.placement.formation import placement_initial, cible_attaque, reinitialiser_affectations
from modules.placement.position_utils import placer_entre, position_aleatoire

from modules.util.distance import distance_ballon
from modules.util.but import position_but_adverse, position_gardien_adverse
from modules.util.chrono import update_chrono_attaque


WHITE = (255, 255, 255)
BLUE = (0, 102, 204)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
SCREEN_WIDTH = 30 * config.longueur_terrain  # Largeur
SCREEN_HEIGHT = 30 * config.largeur_terrain  # Hauteur
# Facteur d'échelle pour transformer les mètres en pixels
SCALE_X = SCREEN_WIDTH / 30  # Terrain de 30m → largeur de la fenêtre
SCALE_Y = SCREEN_HEIGHT / 20  # Terrain de 20m → hauteur de la fenêtre


class Match :
    def __init__(self, equipe_A, equipe_B, JoueursA,JoueursB,):
        self.domicile = equipe_A
        self.exterieur = equipe_B
        self.joueurs_dom = JoueursA
        self.joueurs_ext = JoueursB
        self.chrono = 30*config.ticks
        self.ballon = Ballon((0,0))
        self.possesion = 0     # vaut 0 si personne, 1 si équie à dom, et -1 si équipe ext
        self.receveur = None
        self.emetteur = None
        self.passe_en_cours = False
        self.delai_passe = 0
        self.possession_precedente =0
        self.tir_en_cours = False
        self.score_dom = 0
        self.score_ext = 0

    def lancement_jeu(self) :
        self.placement_initial()
        self.lancement_balle()


        pygame.init()

        # Dimensions de la fenêtre (proportionnelles au terrain FINA 30m x 20m)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Simulation de Water-Polo")

        # Boucle de jeu
        running = True
        clock = pygame.time.Clock()
        self.afficher_terrain(self.screen)


        while running:
            # Gestion des événements (fermeture de la fenêtre)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for joueur in self.joueurs_dom :
                self.action(joueur, self.joueurs_dom)
            for joueur in self.joueurs_ext :
                self.action(joueur,self.joueurs_ext)
            self.update_chrono_attaque()
            self.afficher_terrain(self.screen)


            clock.tick(config.ticks*config.vitesse_du_jeu)

        pygame.quit()

    def afficher_terrain(self,screen):


        """Affiche le terrain, les lignes, les joueurs et le ballon"""
        screen.fill(BLUE)  # Fond bleu pour l'eau

        # Dessiner les cages
        cage_width = 2 * SCALE_X
        cage_height = config.taille_but * SCALE_Y
        pygame.draw.rect(screen, WHITE, (0, (SCREEN_HEIGHT - cage_height) // 2, cage_width, cage_height))
        pygame.draw.rect(screen, WHITE, (SCREEN_WIDTH - cage_width, (SCREEN_HEIGHT - cage_height) // 2, cage_width, cage_height))

        pygame.draw.line(screen, RED, (2 * SCALE_X, 0), (2 * SCALE_X, SCREEN_HEIGHT), 2)
        pygame.draw.line(screen, RED, ((config.longueur_terrain - 2) * SCALE_X, 0), ((config.longueur_terrain - 2) * SCALE_X, SCREEN_HEIGHT), 2)

        pygame.draw.line(screen, YELLOW, (5 * SCALE_X, 0), (5 * SCALE_X, SCREEN_HEIGHT), 2)
        pygame.draw.line(screen, YELLOW, ((config.longueur_terrain - 5) * SCALE_X, 0), ((config.longueur_terrain - 5) * SCALE_X, SCREEN_HEIGHT), 2)

        pygame.draw.line(screen, GREEN, (6 * SCALE_X, 0), (6 * SCALE_X, SCREEN_HEIGHT), 2)
        pygame.draw.line(screen, GREEN, ((config.longueur_terrain - 6) * SCALE_X, 0), ((config.longueur_terrain - 6) * SCALE_X, SCREEN_HEIGHT), 2)

        pygame.draw.line(screen, WHITE, (config.longueur_terrain/2 * SCALE_X, 0), (config.longueur_terrain/2 * SCALE_X, SCREEN_HEIGHT), 2)

        # Dessiner les joueurs
        for joueur in self.joueurs_dom:
            x, y = joueur.position
            pygame.draw.circle(screen, RED, (int(x * SCALE_X), int(y * SCALE_Y)), 7)  # Rouge = Équipe domicile

        for joueur in self.joueurs_ext:
            x, y = joueur.position
            pygame.draw.circle(screen, YELLOW, (int(x * SCALE_X), int(y * SCALE_Y)), 7)  # Jaune = Équipe extérieure

        # Dessiner le ballon
        bx, by = self.ballon.position
        pygame.draw.circle(screen, WHITE, (int(bx * SCALE_X), int(by * SCALE_Y)), 3)

        pygame.display.flip()


    def lancement_balle(self):
        self.ballon.position =  Match.position_aleatoire((config.longueur_terrain//2, 1),0.2)


    def action(self, joueur : Joueur, joueurs : list[Joueur]) :
        if self.possesion == 0 :
            self.recup_ballon(joueur)
            if self.passe_en_cours :
                self.passe_en_cours = self.passe(self.emetteur, self.receveur)
                if self.passe_en_cours == False :
                    self.receveur = None
                    self.emetteur = None

            if min([self.distance_ballon(j) for j in joueurs]) == self.distance_ballon(joueur) :
                joueur.mouvement_vers(self.ballon.position)
            else :
                joueur.mouvement_vers((self.ballon.position[0],joueur.position[1]))
        if self.possesion != self.possession_precedente and self.passe_en_cours == False:
            self.reinitialiser_affectations()
            self.possession_precedente = self.possesion
            self.chrono = 30*config.ticks
        if self.possesion == 1:
            if joueur in self.joueurs_dom :
                choix = self.choix_joueur(joueur)
                if choix == 2 :
                    chance = r.uniform(0, 1)
                    difficulte = self.tir(joueur)
                    if chance > 1 - difficulte:
                        self.tir_en_cours = True
                        while self.tir_en_cours :
                            self.deplacement_ballon(joueur,self.position_but_adverse(joueur))
                            self.afficher_terrain(self.screen)
                            #time.sleep(0.1)
                        self.score_dom+=1
                        print(f"But de {joueur.nom}. Score : {self.domicile} {self.score_dom} - {self.exterieur} {self.score_ext}")
                        joueur.a_le_ballon = False
                        self.tir_en_cours = False
                        self.engagement()
                        self.reinitialiser_affectations()
                        time.sleep(2)
                        for joueur in self.joueurs_ext :
                            if joueur.poste == "défenseur pointe" :
                                self.ballon.position = (joueur.position[0],joueur.position[1])
                                joueur.a_le_ballon = True
                        self.possesion = -1

                    else:
                        self.tir_en_cours = True
                        while self.tir_en_cours :
                            self.deplacement_ballon(joueur,self.position_gardien_adverse(joueur))
                            self.afficher_terrain(self.screen)
                        joueur.a_le_ballon = False
                        self.chrono =30*config.ticks
                        self.transferer_possession()
                if choix == 1 :
                    self.delai_passe = 30
                    self.emetteur = joueur
                    self.passe_en_cours = self.passe(self.emetteur,self.receveur)
                    self.possesion = 0
                else :
                    if joueur.poste != "gardien" :
                        cible = self.cible_attaque(joueur)
                        joueur.mouvement_vers(cible)
                        if joueur.a_le_ballon :
                            self.ballon.position = joueur.position
            else :
                if joueur.poste !="gardien":
                    cible = self.defense(joueur)
                    joueur.mouvement_vers(cible)
        elif self.possesion == -1 :
            if joueur in self.joueurs_ext :
                choix = self.choix_joueur(joueur)
                if choix == 2 :
                    chance = r.uniform(0, 1)
                    difficulte = self.tir(joueur)
                    if chance > difficulte:
                        self.tir_en_cours = True
                        while self.tir_en_cours :
                            self.deplacement_ballon(joueur,self.position_but_adverse(joueur))
                            self.afficher_terrain(self.screen)
                            #time.sleep(0.1)
                        self.score_ext+=1
                        print(f"But de {joueur.nom}. Score : {self.domicile} {self.score_dom} - {self.exterieur} {self.score_ext}")
                        joueur.a_le_ballon = False
                        self.engagement()
                        self.reinitialiser_affectations()
                        time.sleep(2)
                        for joueur in self.joueurs_dom :
                            if joueur.poste == "défenseur pointe" :
                                self.ballon.position = (joueur.position[0],joueur.position[1])
                                joueur.a_le_ballon = True
                        self.possesion = 1

                    else:
                        self.tir_en_cours = True
                        while self.tir_en_cours :
                            self.deplacement_ballon(joueur,self.position_gardien_adverse(joueur))
                            self.afficher_terrain(self.screen)
                        joueur.a_le_ballon = False
                        self.chrono =30*config.ticks
                        self.transferer_possession()


                if choix == 1 :
                    self.delai_passe = 30
                    self.emetteur = joueur
                    self.passe_en_cours = self.passe(self.emetteur,self.receveur)
                    self.possesion = 0
                else :
                    if joueur.poste != "gardien" :
                        cible = self.cible_attaque(joueur)
                        joueur.mouvement_vers(cible)
                        if joueur.a_le_ballon :
                            self.ballon.position = joueur.position
            else :
                if joueur.poste !="gardien":
                    cible = self.defense(joueur)
                    joueur.mouvement_vers(cible)


    def transferer_possession(self):
        joueur_actuel = next((j for j in self.joueurs_dom + self.joueurs_ext if j.a_le_ballon), None)
        if self.possesion == 1 :
            self.possesion = -1
        elif self.possesion == -1 :
            self.possesion = 1

        if joueur_actuel:
            joueur_actuel.a_le_ballon = False  # L'attaquant perd le ballon

            # Trouver le défenseur le plus proche
            if joueur_actuel in self.joueurs_dom:
                joueurs_defenseurs = self.joueurs_ext
            else:
                joueurs_defenseurs = self.joueurs_dom

            defenseur_proche = min(joueurs_defenseurs, key=lambda d: d.distance_au_joueur(joueur_actuel))

            # Nouveau porteur du ballon
            defenseur_proche.mouvement_vers(self.ballon.position)
            self.recup_ballon(defenseur_proche)
            self.ballon.position = defenseur_proche.position
            defenseur_proche.a_le_ballon = True
            self.chrono = 30*config.ticks  # Réinitialisation du chrono pour la nouvelle équipe
            print(f"🎯 {defenseur_proche.nom} récupère le ballon et la contre-attaque commence !")


    def deplacement_ballon(self,depart,arrivee):

        dx, dy =  (arrivee.position[0]-self.ballon.position[0]), (arrivee[1]-self.ballon.position[1])
        distance = (dx**2 + dy**2) ** 0.5

        if distance < 0.75 :
            self.ballon.position = arrivee
            self.tir_en_cours = False
            return False
        else :
            dx, dy = dx / distance, dy / distance  # Normalisation
            self.ballon.position = (self.ballon.position[0] + dx * 0.01, self.ballon.position[1] + dy * 0.01)  # Mise à jour de la position
            return True

