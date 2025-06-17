def update_chrono_attaque(chrono):

    if chrono > 0:
        chrono -= 1
    else:
        print("⏳ Temps d'attaque écoulé ! Changement de possession.")
        transferer_possession()

#il faudrait voir ou mettre cette fonction car elle depend de transferer_possession qui se trouve dans match.py
