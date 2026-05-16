import tkinter as tk
from tkinter import messagebox
import numpy as np
from simulation import Simulation


class Interface_Billard:
    def __init__(self):
        self.L = 600
        self.H = 300
        self.r = 10
        self.i = 0

        self.p_i = np.array([(self.L - self.r*2)/4, self.H/2], dtype=float)
        
        self.fenetre = tk.Tk()
        self.fenetre.title("Partie de billard")

        self.table_billard = tk.Canvas(self.fenetre, bg="green", height=self.H, width=self.L)
        self.table_billard.grid(row=0, column=0)
        self.bande = self.table_billard.create_rectangle(self.r, self.r, self.L - self.r, self.H - self.r, outline="black", width=1)
        self.balle = self.table_billard.create_oval(self.p_i[0] - self.r, self.p_i[1] - self.r, self.p_i[0] + self.r, self.p_i[1] + self.r, fill="white")

        tk.Label(self.fenetre, text="Vitesse initiale de la balle:").grid(row=1, column=0)
        self.v_i = tk.Entry(self.fenetre)
        self.v_i.grid(row=2, column=0)

        tk.Label(self.fenetre, text="Angle du tir:").grid(row=3, column=0)
        self.angle = tk.Entry(self.fenetre)
        self.angle.grid(row=4, column=0)

        tk.Label(self.fenetre, text="Coefficient de friction:").grid(row=5, column=0)
        self.coefficient_friction = tk.Entry(self.fenetre)
        self.coefficient_friction.grid(row=6, column=0)

        tk.Button(self.fenetre, text="Lancer", command=self.lancer).grid(row=7, column=0)
        tk.Button(self.fenetre, text="Position finale", command=self.afficher_position_finale).grid(row=2, column=1)
        
        tk.Button(self.fenetre, text="Reculer d'un pas", command=self.pas_precedent).grid(row=4, column=1)
        tk.Button(self.fenetre, text="Avancer d'un pas", command=self.pas_suivant).grid(row=3, column=1)
        tk.Button(self.fenetre, text="Réinitialiser", command=self.reset).grid(row=5, column=1)
        
        self.simulation = None



    def creer_etat_initial(self):
        try:
            vitesse_initiale = float(self.v_i.get())
            angle = -1 *float(self.angle.get())

        except:
            return None

        if vitesse_initiale == 0:
            return [self.p_i[0], self.p_i[1], 0.0, 0.0]
        
        return [self.p_i[0], self.p_i[1], vitesse_initiale * np.cos(np.radians(angle)), vitesse_initiale * np.sin(np.radians(angle))]
    
    def lancer(self):
        etat_initial = self.creer_etat_initial()
        if etat_initial is None:
            return
        
        try:
            coefficient_friction = float(self.coefficient_friction.get())

            if coefficient_friction > 1 or coefficient_friction < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Erreur",
                "Le coefficient de friction doit être un nombre entre 0 et 1."
            )
            return

        self.simulation = Simulation(
                self.fenetre,
                self.table_billard,
                self.H,
                self.L,
                self.balle,
                self.r,
                etat_initial,
                coefficient_friction
            )
        
        self.p_i = self.simulation.avancer_balle()

    def afficher_position_finale(self):
        etat_initial = self.creer_etat_initial()
        if etat_initial is None:
            return
        
        try:
            coefficient_friction = float(self.coefficient_friction.get())

            if coefficient_friction > 1 or coefficient_friction < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Erreur",
                "Le coefficient de friction doit être un nombre entre 0 et 1."
            )
            return
        
        self.simulation = Simulation(
                self.fenetre,
                self.table_billard,
                self.H,
                self.L,
                self.balle,
                self.r,
                etat_initial,
                coefficient_friction
            )
        
        self.p_i = self.simulation.afficher_position_finale()


    def pas_suivant(self):
        if self.simulation is None:
            return
        if self.i >= len(self.simulation.trajectoire) - 1:
            return

        x0, y0 = self.simulation.trajectoire[self.i][:2]
        self.i += 1
        x1, y1 = self.simulation.trajectoire[self.i][:2]

        dx = x1 - x0
        dy = y1 - y0

        self.table_billard.move(self.balle, dx, dy)


    def pas_precedent(self):
        if self.simulation is None:
            return
        if self.i <= 0:
            return

        x0, y0 = self.simulation.trajectoire[self.i][:2]
        self.i -= 1
        x1, y1 = self.simulation.trajectoire[self.i][:2]

        dx = x1 - x0
        dy = y1 - y0

        self.table_billard.move(self.balle, dx, dy)


    def reset(self):
        if self.simulation is None:
            return

        x, y = self.simulation.trajectoire[0][:2]

        self.table_billard.coords(                  # on additionne et on soustrait le rayon aux coordonnées, car .coords() demande les 4 points de l'objet à déplacer 
            self.balle,                             # par exemple, « x - self.r » est le point gauche, « y - self.r » est le point en haut, « x + self.r » est le point à droite et « y + self.r » est le point en bas
            x - self.r, y - self.r,
            x + self.r, y + self.r
        )

        
       






    def run(self):
        self.fenetre.mainloop()

if __name__ == '__main__':
    app = Interface_Billard()
    app.run()

