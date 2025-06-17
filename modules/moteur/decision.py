from joueur import Joueur
import config

def choix_joueur(joueurs_dom, joueurs_ext, joueur: Joueur, delai_passe: int, possession: int):
    """
    Détermine l'action du joueur en possession du ballon :
    - 1 = passe à un coéquipier
    - 0 = rien (par exemple continuer de nager)

    Retourne : (action: int, receveur: Joueur | None)
    """
    if not joueur.a_le_ballon:
        return 0, None

    # Déterminer équipe et adversaires
    equipe = joueurs_dom if joueur in joueurs_dom else joueurs_ext
    adversaires = joueurs_ext if joueur in joueurs_dom else joueurs_dom

    if delai_passe > 0:
        return 0, None

    receveurs_potentiels = []

    for coequipier in equipe:
        if coequipier is joueur or coequipier.a_le_ballon or coequipier.poste == "gardien":
            continue

        distance_coequipier = joueur.distance_au_joueur(coequipier)
        defenseur_plus_proche = min(adversaires, key=lambda d: d.distance_au_joueur(coequipier))
        distance_defenseur = defenseur_plus_proche.distance_au_joueur(coequipier)

        bien_place = coequipier.mieux_placé(joueur)
        plus_proche_du_but = abs(coequipier.position[0] - config.longueur_terrain) < abs(joueur.position[0] - config.longueur_terrain)

        # Conditions de passe
        if (distance_defenseur > 1 and bien_place) or (distance_defenseur > 3 and plus_proche_du_but):
            if coequipier.poste == "pointe":
                zone_pointe = (25 <= coequipier.position[0] <= 28) if possession == 1 else (2 <= coequipier.position[0] <= 5)
                if zone_pointe:
                    receveurs_potentiels.append((coequipier, distance_coequipier))
            else:
                receveurs_potentiels.append((coequipier, distance_coequipier))

    if receveurs_potentiels:
        receveurs_potentiels.sort(key=lambda x: x[1])
        receveur = receveurs_potentiels[0][0]
        print(f"{joueur.nom} passe à {receveur.nom} !")
        return 1, receveur

    return 0, None
