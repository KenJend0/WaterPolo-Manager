import config

def engagement(joueurs_dom,joueurs_ext):
    for joueur in joueurs_dom :
        joueur.position = (config.positions_dom[joueur.poste][0]-13,config.positions_dom[joueur.poste][1])
    for joueur in joueurs_ext :
        joueur.position = (config.positions_ext[joueur.poste][0]+13,config.positions_dom[joueur.poste][1])
