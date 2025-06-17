import config
from ballon import Ballon
import random as r

import math

class Joueur:
    def __init__(self, nom, equipe, poste, position, endurance, precision_tir, agressivite,puissance,arret):
        self.nom = nom
        self.equipe = equipe
        self.poste = poste  # "gardien", "pointe", "ailier gauche", "ailier droit", "demi gauche", "demi droit", "défenseur pointe"
        self.position = position  # (x, y) sur le terrain
        self.endurance = endurance
        self.precision = precision_tir
        self.agressivite = agressivite
        self.puissance = puissance
        self.arret = arret
        self.a_le_ballon = False
        self.exclu_pour = 0  # Durée de l’exclusion en ticks
        self.vitesse = 0,0              #vitesse du joueur en x et y
        self.energie = 100
        self.deplacement = r.randint(20,100)



        self.stat_vitesse = 100

    def se_deplacer_vers(self, cible_x, cible_y, vitesse):
        """Déplacement vers une position cible"""
        if self.position != (cible_x, cible_y):
            dx = cible_x - self.position[0]
            dy = cible_y - self.position[1]

            distance = (dx**2 + dy**2) ** 0.5
            if distance < 3 :
                new_x = cible_x
                new_y = cible_y
            elif distance > 0:
                dx = (dx / distance) * vitesse
                dy = (dy / distance) * vitesse

            new_x = self.position[0] + dx
            new_y = self.position[1] + dy


            if 0<new_x<30 and 0<new_y<20:
                self.position = (new_x, new_y)
                self.endurance -= 1


    """def passe(self, recepteur) :
        if self.a_le_ballon :
            self.a_le_balon = False


        dx, dy = -ballon.position[0] + recepteur.position[0], -ballon.position[1] + recepteur.position[1]
        distance = (dx**2 + dy**2) ** 0.5

        if distance < 4 :
            ballon.position = recepteur.position
            recepteur.a_le_ballon = True
            return False
        else :
            dx, dy = dx / distance, dy / distance  # Normalisation
            ballon.position = (ballon.position[0] + dx * 4, ballon.position[1] + dy * 4)  # Mise à jour de la position
            return True

    def tir(self,tireur: Joueur) : 
        dx, dy = self.ballon[0] - tireur.position[0], self.ballon[1] - tireur.position[1]
        distance = (dx**2 + dy**2) ** 0.5
        proba = tireur.precision_tir * (6/distance)
        if (r.randint(0,100) > proba *100)"""

    ################################################""

    def mieux_placé(self, joueur):
        tolerence = 5

        poids_x = 0.8  # Moins important
        distance_but_self = abs(self.position[0] - config.longueur_terrain)
        distance_but_joueur = abs(joueur.position[0] - config.longueur_terrain)

        poids_y = 1.2  # Plus important
        distance_centre_self = (1/abs(self.position[1] - config.largeur_terrain / 2))*100
        distance_centre_joueur = (1/abs(joueur.position[1] - config.largeur_terrain / 2))*100

        score_self = poids_x * distance_but_self + poids_y * distance_centre_self
        score_joueur = poids_x * distance_but_joueur + poids_y * distance_centre_joueur

        return score_self > score_joueur +tolerence

    def mouvement_vers(self, cible : tuple[float,float]) :

        if self.distance_au_point(cible[0],cible[1]) >0.1  and self.poste != 'gardien':
            vitesse_max_joueur = config.Vitesse_max * self.stat_vitesse / 100 * self.endurance/100
            vitesse_actuel = (self.vitesse[0]**2 + self.vitesse[1]**2)**0.5
            vitesse_max_cible = cible[0]-self.position[0], cible[1]-self.position[1]
            vitesse_cible_norm = (vitesse_max_cible[0]**2 + vitesse_max_cible[1]**2)**0.5
            vitesse_max_cible = vitesse_max_cible[0]/vitesse_cible_norm * vitesse_max_joueur, vitesse_max_cible[1]/vitesse_cible_norm * vitesse_max_joueur
            acceleration = vitesse_max_cible[0] - self.vitesse[0], vitesse_max_cible[1] - self.vitesse[1]
            acceleration_norm = (acceleration[0]**2 + acceleration[1]**2)**0.5
            if acceleration_norm ==0 :
                acceleration= (0,0)
            else : acceleration = acceleration[0]/acceleration_norm*config.acceleration, acceleration[1]/acceleration_norm*config.acceleration

            temps = 1/config.ticks
            self.position = self.position[0]+ self.vitesse[0]*temps + acceleration[0]/2*(temps**2), self.position[1]+ self.vitesse[1]*temps + acceleration[1]/2*(temps**2)
            self.vitesse = self.vitesse[0] + acceleration[0] *temps, self.vitesse[1] + acceleration[1] *temps

