from config import longueur_terrain

def position_but_adverse(joueur, joueurs_dom):
    if joueur in joueurs_dom :
        return 0,15
    else :
        return 30,15


def position_gardien_adverse(joueur, joueurs_dom, joueurs_ext):
    adversaires = joueurs_ext if joueur in joueurs_dom else joueurs_dom
    for j in adversaires:
        if j.poste == "gardien":
            return j.position
    return (longueur_terrain // 2, 15)  # centre du terrain par défaut
