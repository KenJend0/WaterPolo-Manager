import math
from joueur import Joueur

def distance_au_joueur(position, autre_joueur):
    """Calcule la distance entre ce joueur et un autre joueur."""
    x1, y1 = position
    x2, y2 = autre_joueur.position
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def distance_au_point(self, x, y):
    """Calcule la distance entre ce joueur et un point (x, y)."""
    x1, y1 = self.position
    return math.sqrt((x - x1) ** 2 + (y - y1) ** 2)

def distance_ballon(self, joueur : Joueur) -> float:

    distance = ((self.ballon.position[0] - joueur.position[0])**2 + (self.ballon.position[1] - joueur.position[1])**2)**0.5
    return distance
