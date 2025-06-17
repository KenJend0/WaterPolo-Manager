import math
import config

def passe(emetteur, recepteur, ballon):
    """Fait avancer le ballon vers le receveur. Retourne True si la passe est encore en cours, False si terminée."""
    if emetteur.a_le_ballon:
        emetteur.a_le_ballon = False

    dx = recepteur.position[0] - ballon.position[0]
    dy = recepteur.position[1] - ballon.position[1]
    distance = (dx**2 + dy**2)**0.5

    if distance < 0.75:
        ballon.position = recepteur.position
        recepteur.a_le_ballon = True
        return False  # Passe terminée
    else:
        dx, dy = dx / distance, dy / distance  # Normalisation
        ballon.position = (
            ballon.position[0] + dx * 0.02,
            ballon.position[1] + dy * 0.02
        )
        return True  # Passe encore en cours



def calcul_difficulte_tir(joueur, gardien_adverse):
    but = (
        0 if joueur.equipe == "exterieur" else config.longueur_terrain,
        config.largeur_terrain / 2
    )

    distance = joueur.distance_au_point(*but)
    angle = abs(math.atan2(but[1] - joueur.position[1], but[0] - joueur.position[0]))

    max_distance = config.longueur_terrain
    max_angle = math.pi / 2

    facteur_puissance = max(0.5, 1 - joueur.puissance / 100)
    facteur_precision = max(0.5, 1 - joueur.precision / 100)
    impact_gardien = gardien_adverse.arret / 100

    difficulte_distance = (distance / max_distance) * facteur_puissance
    difficulte_angle = (1 - (angle / max_angle)) * facteur_precision

    difficulte = 0.4 * difficulte_distance + 0.3 * difficulte_angle + 0.3 * impact_gardien
    return max(0, min(1, difficulte))


def resultat_tir(joueur, gardien_adverse):
    difficulte = calcul_difficulte_tir(joueur, gardien_adverse)
    return difficulte <= 0.5

def recup_ballon(joueur, ballon, emetteur, joueurs_dom, joueurs_ext):
    """Attribue le ballon au joueur s'il est proche et pas l'émetteur. Met à jour la possession."""
    if (joueur.a_le_ballon or joueur.distance_au_point(*ballon.position) < 0.25) and joueur != emetteur:
        joueur.a_le_ballon = True
        ballon.position = joueur.position

        if joueur in joueurs_dom:
            return 1  # Possession équipe domicile
        else:
            return -1  # Possession équipe extérieure
    return 0  # Pas de changement
