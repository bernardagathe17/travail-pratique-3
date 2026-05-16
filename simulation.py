import numpy as np

<<<<<<< HEAD
class Simulation:
    def __init__(self, fenetre, table_billard, hauteur, longueur, balle, rayon, etat_initial, coefficient_friction):
        self.fenetre = fenetre
        self.table_billard = table_billard
        self.hauteur = hauteur
        self.longueur = longueur
        self.balle = balle
        self.rayon = rayon
        
        self.dt = 0.1
        self.coefficient_friction = coefficient_friction
        self.epsilon = 0.01

        self.etat_initial = etat_initial         # dans etat, position_courante[0] = p_ix, position_courante[1] = p_iy, position_courante[2] = v_ix, position_courante[3] = v_y                              
                                          # etat est utilisé pour dire si la balle est en mouvement ou non, si etat = None, alors elle ne bouge pas
        self.trajectoire = self.calculer_trajectoire()

        self.i_avance = 0

=======

class Simulation():
    def __init__(self, vitesse_initiale, position, angle, r, L, H, table_billard, balle, fenetre, largeur_bande, config=None):
        self.vitesse = np.array(vitesse_initiale, dtype=float)
        self.position = np.array(position, dtype=float)
        self.angle = angle
        self.r = r
        self.L = L
        self.H = H
        self.largeur_bande = largeur_bande
        self.table_billard = table_billard
        self.balle = balle
        self.fenetre = fenetre
        self.etat = None
        self.bouton = None
        self.config = config or {}
        self.friction = self.config.get("coefficient de friction", 0.95)
        self.epsilon = self.config.get("epsilon", 0.1)
>>>>>>> origin/main

    def calculer_trajectoire(self):
        position_min = np.array([self.rayon, self.rayon])
        position_max = np.array([self.longueur - self.rayon, self.hauteur - self.rayon])

<<<<<<< HEAD
        position = np.array([self.etat_initial[0], self.etat_initial[1]])
        vitesse = np.array([self.etat_initial[2], self.etat_initial[3]])
        
        trajectoire = []     
        trajectoire.append([position[0], position[1], vitesse[0], vitesse[1]])                                                                   
        
        while np.linalg.norm(vitesse) > self.epsilon:                                                   
            vitesse = vitesse * (1 - self.coefficient_friction * self.dt)
            
            #bord gauche = px <= r          n = (1,0)
            #bord droit = px >= L-r         n = (-1,0)
            #bord supérieur = py <= r       n = (0,1)
            #bord inférieur = py>= H-r      n = (0,-1)
=======
        min_x = self.largeur_bande + self.r
        max_x = self.L - self.largeur_bande - self.r
        min_y = self.largeur_bande + self.r
        max_y = self.H - self.largeur_bande - self.r

        if self.position[0] <= min_x or self.position[0] >= max_x:
            self.vitesse[0] = -self.vitesse[0]
        if self.position[1] <= min_y or self.position[1] >= max_y:
            self.vitesse[1] = -self.vitesse[1]
>>>>>>> origin/main


            if position[0] <= position_min[0]:
                position[0] = self.rayon
                n = np.array([1, 0])
                vitesse = vitesse - 2* np.dot(vitesse, n) * n

<<<<<<< HEAD
            if position[0] >= position_max[0]:
                position[0] = self.longueur - self.rayon
                n = np.array([-1, 0])
                vitesse = vitesse - 2* np.dot(vitesse, n) * n
=======
        if np.linalg.norm(self.vitesse) > self.epsilon:
            self.etat = self.fenetre.after(20, self.deplacement)
        else:
            self.etat = None
>>>>>>> origin/main

            if position[1] <= position_min[1]:
                position[1] = self.rayon
                n = np.array([0, 1])
                vitesse = vitesse - 2* np.dot(vitesse, n) * n
            
            if position[1] >= position_max[1]:
                position[1] = self.hauteur - self.rayon
                n = np.array([0, -1])
                vitesse = vitesse - 2* np.dot(vitesse, n) * n
            

            position = position + vitesse * self.dt
            trajectoire.append([position[0], position[1], vitesse[0], vitesse[1]])
            #print(f"position courante = {self.position_courante}")
            position = np.array([trajectoire[-1][0], trajectoire[-1][1]])
            vitesse = np.array([trajectoire[-1][2], trajectoire[-1][3]])

        return trajectoire

    def deplacement_avant(self):
        if self.i_avance >= len(self.trajectoire) - 1:                  # i est l'incrément, mais il correspond principalement à l'état/ la position de l'état dans la liste
            return                                                      # par exemple, i = 0 signifira qu'on est a l'état initiale dans la liste
        
        position_x_initiale = self.trajectoire[self.i_avance][0]                   
        position_y_initiale = self.trajectoire[self.i_avance][1]
        position_x_finale = self.trajectoire[self.i_avance + 1][0]
        position_y_finale = self.trajectoire[self.i_avance + 1][1]

        self.table_billard.move(self.balle, position_x_finale - position_x_initiale, position_y_finale - position_y_initiale)
            
        self.i_avance += 1

        self.fenetre.after(10, self.deplacement_avant)
                
    def avancer_balle(self):
        self.i_avance = 0
        self.deplacement_avant()

<<<<<<< HEAD
        return self.trajectoire[-1][:2]
=======
        min_x = self.largeur_bande + self.r
        max_x = self.L - self.largeur_bande - self.r
        min_y = self.largeur_bande + self.r
        max_y = self.H - self.largeur_bande - self.r

        if self.position[0] <= min_x or self.position[0] >= max_x:
            self.vitesse[0] = -self.vitesse[0]
        if self.position[1] <= min_y or self.position[1] >= max_y:
            self.vitesse[1] = -self.vitesse[1]

        self.position = self.position - self.vitesse * dt
        self.table_billard.coords(
            self.balle,
            self.position[0] - self.r,
            self.position[1] - self.r,
            self.position[0] + self.r,
            self.position[1] + self.r,
        )
>>>>>>> origin/main

    def afficher_position_finale(self):
        self.trajectoire = self.calculer_trajectoire()
        position_x_initiale = self.trajectoire[0][0]
        position_y_initiale = self.trajectoire[0][1]
        position_x_finale = self.trajectoire[-1][0]
        position_y_finale = self.trajectoire[-1][1]

        self.table_billard.move(self.balle, position_x_finale - position_x_initiale, position_y_finale - position_y_initiale)

<<<<<<< HEAD
        return [position_x_finale, position_y_finale]
=======
        min_x = self.largeur_bande + self.r
        max_x = self.L - self.largeur_bande - self.r
        min_y = self.largeur_bande + self.r
        max_y = self.H - self.largeur_bande - self.r

        while np.linalg.norm(vitesse) >= self.epsilon:
            if position[0] <= min_x or position[0] >= max_x:
                vitesse[0] = -vitesse[0]
            if position[1] <= min_y or position[1] >= max_y:
                vitesse[1] = -vitesse[1]
            position += vitesse
            vitesse *= self.friction
>>>>>>> origin/main

