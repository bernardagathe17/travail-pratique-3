import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import json
from simulation import Simulation


class ConfigError(Exception):
    pass


class ConfigFileNotFoundError(ConfigError):
    pass


class ConfigParseError(ConfigError):
    pass


class MissingConfigFieldError(ConfigError):
    pass


class InvalidConfigValueError(ConfigError):
    pass


class Interface_Billard():
    def __init__(self):
        self.fichier = tk.filedialog.askopenfilename(title="Sélectionner un fichier de configuration", filetypes=[("JSON files", "*.json")])
        if not self.fichier:
            raise ConfigFileNotFoundError("Aucun fichier de configuration sélectionné.")

        self.config = self.load_config(self.fichier)
        self.L = self.config["largeur"]
        self.H = self.config["hauteur"]
        self.r = self.config["Rayon des balles"]
        self.largeur_bande = self.config["largeur_bande"]
        min_x = self.largeur_bande + self.r
        self.p_i = np.array([
            min_x + (self.L - 2 * min_x) / 4,
            self.H / 2,
        ], dtype=float)
        self.friction = self.config["coefficient de friction"]
        self.epsilon = self.config["epsilon"]

        self.simulation = None

        self.fenetre = tk.Tk()
        self.fenetre.title("Partie de billard")

        self.table_billard = tk.Canvas(self.fenetre, bg="green", height=self.H, width=self.L)
        self.table_billard.grid(row=0, column=0)
        self.bande = self.table_billard.create_rectangle(self.largeur_bande, self.largeur_bande, self.L - self.largeur_bande, self.H - self.largeur_bande, outline="black", width=1)
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

    def load_config(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as fichier:
                config = json.load(fichier)
        except FileNotFoundError as exc:
            raise ConfigFileNotFoundError(f"Fichier de configuration introuvable : {path}") from exc
        except json.JSONDecodeError as exc:
            raise ConfigParseError(f"Fichier JSON mal formé : {exc.msg} (ligne {exc.lineno}, colonne {exc.colno})") from exc

        self.validate_config(config)
        return config

    def validate_config(self, config):
        required_fields = [
            "largeur",
            "hauteur",
            "Rayon des balles",
            "largeur_bande",
            "coefficient de friction",
            "epsilon",
        ]
        for field in required_fields:
            if field not in config:
                raise MissingConfigFieldError(f"Champ manquant dans le fichier de configuration : {field}")

        largeur = config["largeur"]
        hauteur = config["hauteur"]
        rayon = config["Rayon des balles"]
        largeur_bande = config["largeur_bande"]
        friction = config["coefficient de friction"]
        epsilon = config["epsilon"]

        if not isinstance(largeur, (int, float)) or largeur <= 0:
            raise InvalidConfigValueError("'largeur' doit être un nombre strictement positif.")
        if not isinstance(hauteur, (int, float)) or hauteur <= 0:
            raise InvalidConfigValueError("'hauteur' doit être un nombre strictement positif.")
        if not isinstance(rayon, (int, float)) or rayon <= 0:
            raise InvalidConfigValueError("'Rayon des balles' doit être un nombre strictement positif.")
        if not isinstance(largeur_bande, (int, float)) or largeur_bande < 0:
            raise InvalidConfigValueError("'largeur_bande' doit être un nombre positif ou nul.")
        if largeur_bande * 2 >= min(largeur, hauteur):
            raise InvalidConfigValueError("'largeur_bande' est trop grande pour les dimensions de la table.")
        if largeur_bande + rayon >= largeur / 2:
            raise InvalidConfigValueError("'largeur_bande' et 'Rayon des balles' ne laissent pas assez de place horizontalement.")
        if largeur_bande + rayon >= hauteur / 2:
            raise InvalidConfigValueError("'largeur_bande' et 'Rayon des balles' ne laissent pas assez de place verticalement.")
        if not isinstance(friction, (int, float)) or not (0 <= friction <= 1):
            raise InvalidConfigValueError("'coefficient de friction' doit être un nombre entre 0 et 1.")
        if not isinstance(epsilon, (int, float)) or epsilon <= 0:
            raise InvalidConfigValueError("'epsilon' doit être un nombre strictement positif.")

    def lancer(self):
        #self.bande = self.table_billard.create_rectangle(self.r, self.r, self.L - self.r, self.H - self.r, outline="black", width=1)
        #self.balle = self.table_billard.create_oval(self.p_i[0] - self.r, self.p_i[1] - self.r, self.p_i[0] + self.r, self.p_i[1] + self.r, fill="white")
        from simulation import Simulation
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
                self.largeur_bande,
                self.config,
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
    try:
        app = Interface_Billard()
        app.run()
    except ConfigError as exc:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Erreur de configuration", str(exc))
        root.destroy()
        raise SystemExit(1)


