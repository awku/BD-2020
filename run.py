import tkinter as tk
from aplikacja.gui import App
from aplikacja.database import DataBase

root = tk.Tk()
database = DataBase()
app = App(root, database)
root.mainloop()