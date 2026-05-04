import numpy as np


class Vitesse:
    def __init__(self, vitesse_initiale, angle):
        self.vitesse_initiale = vitesse_initiale
        self.angle = angle
        self.frottement = 0.5 * 2.156
        self.liste = []
        self.vitesse_initiale = np.array([self.calculer_vitesse_x(), self.calculer_vitesse_y()])
        self.vitesse_finale = []

#    def calculer_vitesse_x(self):


#    def calculer_vitesse_y(self):

    
#    def position_finale(self):


