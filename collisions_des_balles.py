import tkinter as tk
import random
import math

# Dimensions de la fenêtre
WIDTH = 500
HEIGHT = 400

# Paramètres des balles
BALL_RADIUS = 20
REFRESH_DELAY = 10  # ms

class Ball:
    def __init__(self, canvas, color):
        self.canvas = canvas

        # Position initiale aléatoire
        self.x = random.randint(BALL_RADIUS, WIDTH - BALL_RADIUS)
        self.y = random.randint(BALL_RADIUS, HEIGHT - BALL_RADIUS)

        # Création graphique
        self.id = canvas.create_oval(
            self.x - BALL_RADIUS,
            self.y - BALL_RADIUS,
            self.x + BALL_RADIUS,
            self.y + BALL_RADIUS,
            fill=color
        )

        # Vitesse aléatoire
        self.vx = random.choice([-3, -2, 2, 3])
        self.vy = random.choice([-3, -2, 2, 3])

    def move(self):
        # Mise à jour position
        self.x += self.vx
        self.y += self.vy

        # Rebond sur les murs
        if self.x - BALL_RADIUS <= 0 or self.x + BALL_RADIUS >= WIDTH:
            self.vx = -self.vx

        if self.y - BALL_RADIUS <= 0 or self.y + BALL_RADIUS >= HEIGHT:
            self.vy = -self.vy

        # Déplacement graphique
        self.canvas.coords(
            self.id,
            self.x - BALL_RADIUS,
            self.y - BALL_RADIUS, #redessine la balle à sa nouvelle position
            self.x + BALL_RADIUS,
            self.y + BALL_RADIUS
        )

def detect_collision(ball1, ball2):
    dx = ball1.x - ball2.x
    dy = ball1.y - ball2.y

    distance = math.sqrt(dx**2 + dy**2)

    # Collision si la distance entre centres
    # est inférieure au diamètre
    return distance <= 2 * BALL_RADIUS

def handle_collision(ball1, ball2):
    # Échange simple des vitesses
    ball1.vx, ball2.vx = ball2.vx, ball1.vx
    ball1.vy, ball2.vy = ball2.vy, ball1.vy

def update():
    # Déplacer les balles
    for ball in balls:
        ball.move()

    # Vérifier collision entre les deux balles
    if detect_collision(balls[0], balls[1]):
        handle_collision(balls[0], balls[1])

    root.after(REFRESH_DELAY, update)

# Fenêtre principale
root = tk.Tk()
root.title("Balles rebondissantes")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# Création des balles
balls = [
    Ball(canvas, "red"),
    Ball(canvas, "blue")
]

# Lancement animation
update()

root.mainloop()