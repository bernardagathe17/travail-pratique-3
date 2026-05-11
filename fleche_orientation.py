import tkinter as tk
import math

# Paramètres de la flèche
LENGTH = 100  # longueur de la flèche en pixels
CENTER_X = 200
CENTER_Y = 200

def update_arrow():
    """Met à jour la position de la flèche selon l'angle entré."""
    try:
        angle_deg = float(angle_entry.get())  # lecture de l'angle
    except ValueError:
        status_label.config(text="⚠ Veuillez entrer un nombre valide.")
        return

    # Conversion en radians
    angle_rad = math.radians(angle_deg)

    # Calcul des coordonnées de la pointe
    end_x = CENTER_X + LENGTH * math.cos(angle_rad)
    end_y = CENTER_Y - LENGTH * math.sin(angle_rad)  # Y inversé dans Tkinter

    # Effacer l'ancienne flèche
    canvas.delete("arrow")

    # Dessiner la nouvelle flèche
    canvas.create_line(
        CENTER_X, CENTER_Y, end_x, end_y,
        arrow=tk.LAST, width=3, fill="blue", tags="arrow"
    )

    status_label.config(text=f"Flèche orientée à {angle_deg:.1f}°")

# Fenêtre principale
root = tk.Tk()
root.title("Flèche orientable avec Tkinter")

# Canvas
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack(pady=10)

# Point central (optionnel : repère visuel)
canvas.create_oval(CENTER_X-3, CENTER_Y-3, CENTER_X+3, CENTER_Y+3, fill="red")

# Zone de saisie
frame = tk.Frame(root)
frame.pack()

tk.Label(frame, text="Angle (°) :").pack(side=tk.LEFT, padx=5)
angle_entry = tk.Entry(frame, width=10)
angle_entry.pack(side=tk.LEFT)
angle_entry.insert(0, "0")  # valeur par défaut

tk.Button(frame, text="Mettre à jour", command=update_arrow).pack(side=tk.LEFT, padx=5)

# Label de statut
status_label = tk.Label(root, text="Entrez un angle et cliquez sur 'Mettre à jour'")
status_label.pack(pady=5)

# Dessin initial
update_arrow()

root.mainloop()
