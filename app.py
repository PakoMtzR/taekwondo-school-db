import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("300x400")
        self.title("TKD Database Management")
        self.create_widgets()

    def create_widgets(self):
        btn = ttk.Button(self, text="Hola")
        btn.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()