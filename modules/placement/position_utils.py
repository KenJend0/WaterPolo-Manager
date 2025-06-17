from typing import Tuple
import random as r
from config import fact_alea_pos

def placer_entre(adversaire_pos, but_pos, facteur):

    x = but_pos[0] + facteur * (adversaire_pos[0] - but_pos[0])
    y = but_pos[1] + facteur * (adversaire_pos[1] - but_pos[1])
    return x, y


def position_aleatoire(position: Tuple[float, float], facteur = fact_alea_pos) -> Tuple[float, float]:
    dx,dy = r.uniform(-1,1),+ r.uniform(-1,1)
    distance = (dx**2 + dy**2)**0.5 / facteur
    dx,dy = dx / distance, dy/distance
    return position[0] + dx, position[1]+dy
