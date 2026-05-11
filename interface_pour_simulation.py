import tkinter as tk
import numpy as np
import json
from simulation import Simulation

with open('donnees.json', 'r', encoding='utf-8') as fichier:
    donnees = json.load(fichier)

class Interface_Billard:
    def __init__(self):
        self.L = donnees["largeur"]
        self.H = donnees["hauteur"]
        self.r = donnees["Rayon des balles"]
        self.p_i = np.array([(self.L - self.r*2)/4, self.H/2], dtype=float)
        self.simulation = None

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

        self.bouton_lancer = tk.Button(self.fenetre, text="Lancer", command=self.lancer)
        self.bouton_lancer.grid(row=5, column=0)

        self.bouton_arreter = tk.Button(self.fenetre, text="Arrêter", state='disabled', command=self.arreter)
        self.bouton_arreter.grid(row=5, column=1)

        self.bouton_reculer = tk.Button(self.fenetre, text="Reculer", state='disabled', command=self.reculer)
        self.bouton_reculer.grid(row=6, column=1)

        self.bouton_position_finale = tk.Button(self.fenetre, text="Position finale", state='disabled', command=self.afficher_position_finale)
        self.bouton_position_finale.grid(row=6, column=0)

    def lancer(self):
        try:
            vitesse = float(self.v_i.get())
            angle = float(self.angle.get())
        except ValueError:
            return

        vecteur_vitesse = np.array([
            float(vitesse * np.cos(np.radians(angle))),
            float(vitesse * np.sin(np.radians(angle)))
        ], dtype=float)

        if self.simulation is None:
            self.simulation = Simulation(
                vecteur_vitesse,
                self.p_i.copy(),
                angle,
                self.r,
                self.L,
                self.H,
                self.table_billard,
                self.balle,
                self.fenetre,
            )
            self.simulation.set_stop_button(self.bouton_arreter)
            self.bouton_reculer.config(state='normal')
            self.bouton_position_finale.config(state='normal')
        else:
            self.simulation.mise_a_jour_variables(vecteur_vitesse, angle)

        self.bouton_arreter.config(state='normal')
        self.simulation.bouger_balle()

    def arreter(self):
        if self.simulation is not None:
            self.simulation.arreter_balle()

    def reculer(self):
        if self.simulation is not None:
            self.simulation.reculer_position()

    def afficher_position_finale(self):
        if self.simulation is not None:
            self.simulation.afficher_position_finale()

    def run(self):
        self.fenetre.mainloop()

if __name__ == '__main__':
    app = Interface_Billard()
    app.run()

