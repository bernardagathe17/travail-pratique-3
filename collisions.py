import tkinter as tk

def check_collision():
    # Récupère les coordonnées (x1, y1, x2, y2) des deux objets
    x1, y1, x2, y2 = canvas.bbox(obj1)
    a1, b1, a2, b2 = canvas.bbox(obj2)

    # Test de chevauchement (collision)
    if (x1 < a2 and x2 > a1 and y1 < b2 and y2 > b1):
        canvas.itemconfig(obj1, fill="red")
        canvas.itemconfig(obj2, fill="red")
    else:
        canvas.itemconfig(obj1, fill="blue")
        canvas.itemconfig(obj2, fill="green")

    # Rappel toutes les 20 ms
    root.after(20, check_collision)

def move_obj2(event):
    """Déplace l'objet 2 avec les touches fléchées"""
    if event.keysym == "Up":
        canvas.move(obj2, 0, -5)
    elif event.keysym == "Down":
        canvas.move(obj2, 0, 5)
    elif event.keysym == "Left":
        canvas.move(obj2, -5, 0)
    elif event.keysym == "Right":
        canvas.move(obj2, 5, 0)

# Création de la fenêtre
root = tk.Tk()
root.title("Collision sur Canvas Tkinter")

canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

# Création de deux objets
obj1 = canvas.create_rectangle(5, 50, 100, 100, fill="blue")
obj2 = canvas.create_oval(200, 150, 250, 200, fill="green")

# Bind des touches fléchées
root.bind("<KeyPress>", move_obj2)

# Lancement de la détection
check_collision()

root.mainloop()
