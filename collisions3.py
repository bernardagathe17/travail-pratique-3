import numpy as np
# ...existing code...

WIDTH = 400
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
        # champs pour séquence de vitesses (optionnel)
        self.vx_list = None
        self.vy_list = None
        self._vlist_index = 0

    def move(self):
        # Si une séquence de vitesses est attachée, l'utiliser pas à pas
        if self.vx_list is not None and self._vlist_index < len(self.vx_list):
            self.vx = self.vx_list[self._vlist_index]
            self.vy = self.vy_list[self._vlist_index]
            self._vlist_index += 1

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
# ...existing code...


class Vitesse:
    def __init__(self, vitesse_initiale, angle, steps=10, friction=1):
        """
        vitesse_initiale : magnitude initiale (px/frame)
        angle : en degrés (0 = vers la droite, 90 = vers le bas)
        steps : nombre d'étapes (ici 10)
        friction : quantité soustraite à la magnitude par étape (positif)
        """
        self.v0 = max(0.0, float(vitesse_initiale))
        self.angle = float(angle)
        self.steps = int(steps)
        self.friction = abs(float(friction))

    def _speed_at_step(self, i):
        # i = 0..steps-1
        s = self.v0 - i * self.friction
        return max(0.0, s)

    def generate_sequence(self):
        """Retourne liste de (vx, vy) de longueur self.steps.
           La magnitude décroît de self.friction par étape, dernière = 0 si atteint."""
        ang_rad = np.radians(self.angle)
        seq = []
        for i in range(self.steps):
            s = self._speed_at_step(i)
            vx = s * np.cos(ang_rad)
            vy = s * np.sin(ang_rad)
            seq.append((vx, vy))
        return seq

    def appliquer_sur_ball(self, ball):
        """Attache la séquence vx_list/vy_list à l'objet Ball."""
        seq = self.generate_sequence()
        ball.vx_list = [vx for vx, _ in seq]
        ball.vy_list = [vy for _, vy in seq]
        ball._vlist_index = 0

    def position_finale(self, start_coords):
        """
        (optionnel) Calcule les positions successives (x1,y1,x2,y2) en appliquant
        la séquence sur un rectangle initial start_coords = (x1,y1,x2,y2),
        sans gérer collisions entre balles (gère uniquement rebonds sur bords).
        """
        x1, y1, x2, y2 = start_coords
        w = x2 - x1
        h = y2 - y1
        positions = []
        for vx, vy in self.generate_sequence():
            nx1 = x1 + vx
            ny1 = y1 + vy
            nx2 = nx1 + w
            ny2 = ny1 + h

            # rebond horizontaux
            if nx1 <= 0:
                nx1 = 0
                nx2 = nx1 + w
            if nx2 >= WIDTH:
                nx2 = WIDTH
                nx1 = nx2 - w
            # rebond verticaux
            if ny1 <= 0:
                ny1 = 0
                ny2 = ny1 + h
            if ny2 >= HEIGHT:
                ny2 = HEIGHT
                ny1 = ny2 - h

            positions.append((nx1, ny1, nx2, ny2))
            x1, y1, x2, y2 = nx1, ny1, nx2, ny2

        return positions
# ...existing code...

# ...existing code...
if __name__ == "__main__":
    import tkinter as tk
    import random

    root = tk.Tk()
    root.title("Test Vitesse")

    canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
    canvas.pack()

    # Création de deux balles pour le test
    balls = [Ball(canvas, "red"), Ball(canvas, "blue")]

    # Appliquer une Vitesse de test (magn. 10 px/frame, angle 30°, friction 1, 10 étapes)
    v = Vitesse(10, 30, steps=10, friction=1)
    v.appliquer_sur_ball(balls[0])

    # Boucle d'animation locale (utilise REFRESH_DELAY)
    def update_frame():
        for ball in balls:
            ball.move()
        root.after(REFRESH_DELAY, update_frame)

    update_frame()
    root.mainloop()
# ...existing code...