import tkinter as tk
from tkinter import messagebox

# Paramètres de déplacement
STEP = 10  # pixels par mouvement
CANVAS_WIDTH = 400
CANVAS_HEIGHT = 200

def move_forward():
    """Déplace l'objet vers la droite."""
    x1, y1, x2, y2 = canvas.coords(obj)
    if x2 + STEP <= CANVAS_WIDTH:
        canvas.move(obj, STEP, 0)
    else:
        messagebox.showinfo("Info", "Limite droite atteinte.")

def move_backward():
    """Déplace l'objet vers la gauche."""
    x1, y1, x2, y2 = canvas.coords(obj)
    if x1 - STEP >= 0:
        canvas.move(obj, -STEP, 0)
    else:
        messagebox.showinfo("Info", "Limite gauche atteinte.")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Marche avant / arrière - Tkinter")

# Création du Canvas
canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
canvas.pack(pady=10)

# Création d'un objet (rectangle rouge)
obj = canvas.create_rectangle(50, 80, 100, 120, fill="red")

# Boutons de contrôle
frame_buttons = tk.Frame(root)
frame_buttons.pack()

btn_backward = tk.Button(frame_buttons, text="←", command=move_backward)
btn_backward.pack(side=tk.LEFT, padx=5)

btn_forward = tk.Button(frame_buttons, text="→", command=move_forward)
btn_forward.pack(side=tk.LEFT, padx=5)
root.mainloop()
