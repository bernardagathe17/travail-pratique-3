import tkinter as tk
import numpy as np



x_vel = 5
y_vel = 5

def bouger_balle(x, y ,x_vel, y_vel):
    if x < 0:
        x_vel = 5
    if x > 560:
        x_vel = -5
    if y < 0:
        y_vel = 5
    if y > 260:
        y_vel = -5
    fond.move(balle, x_vel, y_vel)
    coordinates = fond.coords(balle)
    x = coordinates[0]
    y = coordinates[1]
    fenetre.after(100, bouger_balle, x, y ,x_vel, y_vel)



# .move() pour déplacer la balle





largeur = 600
hauteur = 300
rayon = 10
largeur_bande = 20
position_initiale_balle = np.array([(largeur - largeur_bande*2)/4, hauteur/2])
x,y = position_initiale_balle

fenetre = tk.Tk()
fenetre.title("Partie de billard")

fond = tk.Canvas(fenetre, bg="green",height=hauteur, width=largeur)
fond.grid(row=0, column=0)
bande = fond.create_rectangle(largeur_bande, largeur_bande, largeur - largeur_bande, hauteur - largeur_bande, outline="black", width=0.5)
balle = fond.create_oval(x - rayon, y - rayon, x + rayon, y + rayon, fill="white")

tk.Label(fenetre, text="Vitesse intiale de la balle:").pack()
vitesse_intitale = tk.Entry(fenetre)
vitesse_intitale.pack(side= tk.BOTTOM)
bouger_balle(x, y, x_vel, y_vel)


fond.pack()
fenetre.mainloop()

