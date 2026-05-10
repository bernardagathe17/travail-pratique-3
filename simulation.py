import numpy as np

class Simulation:
    def __init__(self, vitesse_initiale, position, angle, r, L, H, table_billard, balle, fenetre):
        self.vitesse = np.array(vitesse_initiale, dtype=float)
        self.position = np.array(position, dtype=float)
        self.angle = angle
        self.r = r
        self.L = L
        self.H = H
        self.table_billard = table_billard
        self.balle = balle
        self.fenetre = fenetre
        self.etat = None
        self.bouton = None
        self.friction = 0.99
        self.epsilon = 0.1

    def calculer_trajectoire(self):
        dt = 1

        if self.position[0] <= 2 * self.r or self.position[0] >= self.L - 3 * self.r:
            self.vitesse[0] = -self.vitesse[0]
        if self.position[1] <= 2 * self.r or self.position[1] >= self.H - 2 * self.r:
            self.vitesse[1] = -self.vitesse[1]

        self.position += self.vitesse * dt
        self.vitesse *= self.friction
        if np.linalg.norm(self.vitesse) < self.epsilon:
            self.vitesse[:] = 0

    def deplacement(self):
        self.calculer_trajectoire()
        self.table_billard.coords(
            self.balle,
            self.position[0] - self.r,
            self.position[1] - self.r,
            self.position[0] + self.r,
            self.position[1] + self.r,
        )

        if np.linalg.norm(self.vitesse) > self.epsilon:
            self.etat = self.fenetre.after(100, self.deplacement)
        else:
            self.etat = None

    def bouger_balle(self):
        if self.etat is None:
            self.deplacement()

    def set_stop_button(self, button):
        self.bouton = button
        self.bouton.config(command=self.arreter_balle, state='normal')

    def mise_a_jour_variables(self, vitesse, angle):
        self.vitesse = vitesse
        self.angle = angle

    def arreter_balle(self):
        if self.etat is not None:
            self.fenetre.after_cancel(self.etat)
            self.etat = None
        if self.bouton:
            self.bouton.config(state='disabled')

    def reculer_position(self):
        if self.etat is not None:
            self.fenetre.after_cancel(self.etat)
            self.etat = None

        dt = 1

        if self.position[0] <= 2 * self.r or self.position[0] >= self.L - 3 * self.r:
            self.vitesse[0] = -self.vitesse[0]
        if self.position[1] <= 2 * self.r or self.position[1] >= self.H - 2 * self.r:
            self.vitesse[1] = -self.vitesse[1]

        self.position = [pos - vel * dt for pos, vel in zip(self.position, self.vitesse)]
        self.table_billard.coords(
            self.balle,
            self.position[0] - self.r,
            self.position[1] - self.r,
            self.position[0] + self.r,
            self.position[1] + self.r,
        )

    def afficher_position_finale(self):
        if self.etat is not None:
            self.fenetre.after_cancel(self.etat)
            self.etat = None

        position = self.position.copy()
        vitesse = self.vitesse.copy()

        while np.linalg.norm(vitesse) >= self.epsilon:
            if position[0] <= 2 * self.r or position[0] >= self.L - 3 * self.r:
                vitesse[0] = -vitesse[0]
            if position[1] <= 2 * self.r or position[1] >= self.H - 2 * self.r:
                vitesse[1] = -vitesse[1]
            position += vitesse
            vitesse *= self.friction

        self.position = position
        self.vitesse = vitesse
        self.table_billard.coords(
            self.balle,
            self.position[0] - self.r,
            self.position[1] - self.r,
            self.position[0] + self.r,
            self.position[1] + self.r,
        )
        