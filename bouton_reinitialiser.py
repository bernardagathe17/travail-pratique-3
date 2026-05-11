import tkinter as tk
from tkinter import messagebox

def reset_canvas():
    """Efface tout le contenu du canvas et réinitialise les données."""
    if messagebox.askyesno("Confirmation", "Voulez-vous vraiment réinitialiser ?"):
        canvas.delete("all")  # Supprime tous les éléments du canvas
        user_data.clear()     # Vide la liste des données
        print("Canvas réinitialisé.")

def add_circle(event):
    """Ajoute un cercle à l'endroit cliqué par l'utilisateur."""
    x, y = event.x, event.y
    r = 20
    canvas.create_oval(x-r, y-r, x+r, y+r, fill="blue")
    user_data.append((x, y))  # Sauvegarde la position
    print(f"Cercle ajouté à ({x}, {y})")

# Création de la fenêtre principale
root = tk.Tk()
root.title("Exemple Canvas avec bouton Reset")
root.geometry("500x400")

# Liste pour stocker les données utilisateur
user_data = []

# Création du Canvas
canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack(pady=10)

# Lier un clic gauche pour ajouter un cercle
canvas.bind("<Button-1>", add_circle)

# Bouton pour réinitialiser
reset_button = tk.Button(root, text="Réinitialiser", command=reset_canvas, bg="red", fg="white")
reset_button.pack(pady=5)

root.mainloop()
