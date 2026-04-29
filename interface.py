import tkinter as tk

fenetre = tk.Tk()

fenetre.title("Partie de billard")


fond = tk.Canvas(fenetre, bg="green",height=284, width=568)


fond.pack()
fenetre.mainloop()