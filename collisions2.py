import tkinter as tk
import random

# Paramètres de la fenêtre
WIDTH = 500
HEIGHT = 400
BALL_RADIUS = 20
REFRESH_DELAY = 10  # en ms

class Ball:
    def __init__(self, canvas, color):
        self.canvas = canvas
        # Position initiale aléatoire
        x = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
        y = random.randint(BALL_RADIUS, HEIGHT - BALL_RADIUS)
        self.id = canvas.create_oval(
            x - BALL_RADIUS, y - BALL_RADIUS,
            x + BALL_RADIUS, y + BALL_RADIUS,
            fill=color
        )
        # Vitesse initiale aléatoire
        self.vx = random.choice([-3, -2, 2, 3])
        self.vy = random.choice([-3, -2, 2, 3])

    def move(self):
        # Déplacer la balle
        self.canvas.move(self.id, self.vx, self.vy)
        x1, y1, x2, y2 = self.canvas.coords(self.id)

        # Rebond sur les bords horizontaux
        if x1 <= 0 or x2 >= WIDTH:
            self.vx = -self.vx
        # Rebond sur les bords verticaux
        if y1 <= 0 or y2 >= HEIGHT:
            self.vy = -self.vy
        # Rebond sur l'autre balle
        for other in balls:
            if other != self:
                ox1, oy1, ox2, oy2 = self.canvas.coords(other.id)
                if (x1 < ox2 and x2 > ox1 and y1 < oy2 and y2 > oy1):
                    self.vx = -self.vx
                    self.vy = -self.vy
                    other.vx = -other.vx
                    other.vy = -other.vy

def update():
    for ball in balls:
        ball.move()
    root.after(REFRESH_DELAY, update)

# Création de la fenêtre
root = tk.Tk()
root.title("Deux balles rebondissantes")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# Création de deux balles
balls = [
    Ball(canvas, "red"),
    Ball(canvas, "blue")
]

# Lancer l'animation
update()

root.mainloop()
