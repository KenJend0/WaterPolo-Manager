import config
from modules.placement.position_utils import placer_entre
import random as r

def defense(joueur, joueurs_dom, joueurs_ext, marquages: dict):
    """
    Calcule la position défensive du joueur en fonction de l'adversaire à marquer.
    - `marquages` est un dictionnaire {defenseur: attaquant} partagé entre appels.
    - Retourne une position (x, y) vers laquelle aller.
    """
    equipe = joueurs_dom if joueur in joueurs_dom else joueurs_ext
    adversaires = joueurs_ext if joueur in joueurs_dom else joueurs_dom

    but = (
        config.longueur_terrain, config.largeur_terrain / 2
    ) if joueur in joueurs_dom else (
        0, config.largeur_terrain / 2
    )

    # Cas spécifique : défenseur pointe marque le pointe
    if joueur.poste == "défenseur pointe":
        for adv in adversaires:
            if adv.poste == "pointe":
                marquages[joueur] = adv
                return placer_entre(adv.position, but, 0.90)

    # Autres défenseurs : trouver un adversaire disponible
    adversaires_disponibles = [
        j for j in adversaires
        if j.poste not in {"gardien", "pointe"} and j not in marquages.values()
    ]

    if adversaires_disponibles:
        adversaire = min(adversaires_disponibles, key=lambda j: joueur.distance_au_joueur(j))
        marquages[joueur] = adversaire
        return placer_entre(adversaire.position, but, 0.85)

    # Si déjà assigné auparavant
    if joueur in marquages:
        return placer_entre(marquages[joueur].position, but, 0.85)

    return (0, 0)  # Aucune action possible

def se_demarquer(deplacement: float):
    """
    Génère une position de démarquage aléatoire influencée par la capacité de déplacement.
    """
    facteur = 1 + (deplacement / 100)
    ciblex = facteur * r.uniform(1, 2)
    cibley = facteur * r.uniform(1, 2)
    return ciblex, cibley