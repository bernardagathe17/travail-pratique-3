import tkinter as tk

def disable_button():
    # Disable the button
    my_button.config(state=tk.DISABLED)

def enable_button():
    # Enable the button
    my_button.config(state=tk.NORMAL)

# Create main window
root = tk.Tk()
root.title("Disable Button on Canvas Example")

# Create a Canvas
canvas = tk.Canvas(root, width=300, height=200, bg="lightgray")
canvas.pack(pady=20)

# Create a Button on the Canvas
my_button = tk.Button(canvas, text="Click Me", command=disable_button)
# Place the button at coordinates (100, 80) on the canvas
canvas.create_window(150, 80, window=my_button)

# Create an "Enable" button outside the canvas
enable_btn = tk.Button(root, text="Enable Button", command=enable_button)
enable_btn.pack(pady=10)

root.mainloop()
