import position_utils
import config

def placement_initial(joueurs_dom,joueurs_ext) :

    for joueur in joueurs_dom :
        joueur.position = position_utils.position_aleatoire(config.positions_dom[joueur.poste])
    for joueur in joueurs_ext :
        joueur.position = position_utils.position_aleatoire(config.positions_ext[joueur.poste])

def reinitialiser_affectations():
    position_disponible = {poste: pos for poste, pos in config.formations.items() if poste != "pointe"}
    affectations = {}
    return position_disponible,affectations


def cible_attaque(joueur,joueurs_dom,joueurs_ext, ballon,possession,affectations,position_disponible):
    position_arrondie = (round(joueur.position[0]), round(joueur.position[1]))
    equipe = joueurs_dom if joueur in joueurs_dom else joueurs_ext
    equipe_sans_gardien = [j for j in equipe if j.poste != "gardien"]

    if not affectations:
        position_disponible, affectations = reinitialiser_affectations()


    for player in equipe_sans_gardien:
        if player.poste == "pointe":
            affectations[player] = (
                config.formations["pointe"][0] * -possession + 15,
                config.formations["pointe"][1]
            )


    # Affecter les autres postes
    for poste, position in position_disponible.items():
        position = (position[0] * -possession + 15, position[1])
        joueurs_non_places = [j for j in equipe_sans_gardien if j not in affectations]
        if not joueurs_non_places:
            break
        joueur_proche = min(joueurs_non_places, key=lambda j: j.distance_au_point(*position))
        affectations[joueur_proche] = position

    # Retourner la cible pour ce joueur
    if joueur in affectations:
        cible = affectations[joueur]
        if position_arrondie != cible:
            return cible
        elif joueur.poste != "pointe" and joueur.distance_au_point(ballon.position[0], ballon.position[1]) < 10:
            return position_utils.position_aleatoire(cible, 2)


    return joueur.position  # Si aucune position trouvée, le joueur reste en place

