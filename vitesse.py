import numpy as np


class Vitesse:
    def __init__(self, vitesse_initiale, angle):
        self.vitesse_initiale = vitesse_initiale
        self.angle = angle

    def calculer_vitesse_x(self):
        return self.vitesse_initiale * np.cos(np.radians(self.angle))

    def calculer_vitesse_y(self):
        return self.vitesse_initiale * np.sin(np.radians(self.angle))
    
    def position_finale(self):
        x = self.calculer_vitesse_x()
        y = self.calculer_vitesse_y()
        x_f = x - 0.5 * x
        y_f = y - 0.5 * y
        for i in np.linspace(0, x_f, num=10):
            #aller en i pour x
            #ajouter à une liste avec liste.append
            #si il touche coordonnée du coté, inverser x
            pass
        for j in np.linspace(0, y_f, num=10):
            #aller en j pour y
            #ajouter à une liste avec liste.append
            #si il touche coordonnée du plafond, inverser y
            pass
    
    def voir_vitesse(self):
        # parcourir les listes de positions et les afficher
        # avant / après

        return (x_f, y_f)


#vitesse = a
#angle = b 
#u = [[vitesse * np.cos(np.radians(angle))], [vitesse * np.sin(np.radians(angle))]]
#v_x = np.array([1, 0])
#v_y = np.array([0, 1])