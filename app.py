import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from dotenv import load_dotenv
load_dotenv()
    
import os
from supabase import create_client

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

class App(tk.Tk):
    COLOR_GRAY = "#C3C3C3"
    COLOR_THEME = "#598FDB"   # lightblue

    def __init__(self):
        super().__init__()
        self.geometry("800x600")
        self.title("TKD Database Management")
        self.create_widgets()

    def create_widgets(self):
        # Frame para las opciones (izquierda)
        options_frame = tk.Frame(master=self, bg=self.COLOR_GRAY)   # lightblue
        options_frame.pack(side=tk.LEFT, fill="y")
        options_frame.pack_propagate(False)
        options_frame.configure(width=200)

        # Frame para el contenido dinámico (derecha)
        self.content_frame = tk.Frame(master=self, padx=10, pady=10)
        self.content_frame.pack(side=tk.LEFT, fill="both", expand=True)

        # Creamos los botones del menu de opciones
        self.btn_welcome = tk.Label(options_frame, text="Bienvenida", bg=self.COLOR_GRAY, pady=10, padx=10)
        self.btn_welcome.pack(fill="x")
        self.btn_welcome.bind("<Button-1>", lambda e:self.show_frame(self.btn_welcome, 1))

        self.btn_inventory = tk.Label(options_frame, text="Inventario", bg=self.COLOR_GRAY, pady=10, padx=10)
        self.btn_inventory.pack(fill="x")
        self.btn_inventory.bind("<Button-1>", lambda e:self.show_frame(self.btn_inventory, 2))

        self.btn_students = tk.Label(options_frame, text="Alumnos", bg=self.COLOR_GRAY, pady=10, padx=10)
        self.btn_students.pack(fill="x")
        self.btn_students.bind("<Button-1>", lambda e:self.show_frame(self.btn_students, 3))

        # Iniciamos con el frame de bienvenida
        self.show_frame(self.btn_welcome, 1)

    def deselect_options_btns(self):
        # Restablecer todos los botones(labels) a su color original
        self.btn_welcome.configure(bg=self.COLOR_GRAY)
        self.btn_inventory.configure(bg=self.COLOR_GRAY)
        self.btn_students.configure(bg=self.COLOR_GRAY)

    def show_frame(self, option, frame_number):
        # Deseleccionar todos los labels (volviendo a su color original)
        self.deselect_options_btns()

        # Seleccionar el label actual
        option.configure(bg=self.COLOR_THEME)

        # Cambiar el contenido en el Frame de la derecha
        self.clear_content_frame()

        match(frame_number):
            case 1:
                self.show_welcome_frame()
            case 2:
                self.show_inventory_frame()
            case 3:
                self.show_students_frame()
            case _:
                print("No se encontro el frame especificado.")


    def clear_content_frame(self):
        # Eliminar todos los widgets en el Frame de contenido
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_welcome_frame(self):
        label = ttk.Label(self.content_frame, text="Bienvenido!")
        label.pack()

    def show_inventory_frame(self):
        for i in range(6):
            self.content_frame.columnconfigure(i, weight=1)

        label_product = ttk.Label(self.content_frame, text="Producto:")
        label_product.grid(row=0, column=0, sticky="e", padx=5, pady=10)

        self.textbox = ttk.Entry(self.content_frame)
        self.textbox.grid(row=0, column=1, columnspan=3, sticky="nesw", padx=5, pady=10)

        btn_search = ttk.Button(self.content_frame, text="Buscar")
        btn_search.grid(row=0, column=4, sticky="nesw", padx=5, pady=10)

        btn_clean = ttk.Button(self.content_frame, text="Limpiar")
        btn_clean.grid(row=0, column=5, sticky="nesw", padx=5, pady=10)

        btn_edit = ttk.Button(self.content_frame, text="Modificar")
        btn_edit.grid(row=1, column=0, columnspan=4, sticky="nesw", padx=5, pady=10)

        btn_delete = ttk.Button(self.content_frame, text="Eliminar")
        btn_delete.grid(row=1, column=4, columnspan=3, sticky="nesw", padx=5, pady=10)
        
        self.table_inventory = ttk.Treeview(self.content_frame, height=10, columns=("col1", "col2", "col3", "col4", "col5"))
        self.table_inventory.grid(row=2, column=0, columnspan=6, sticky="nesw")
        # Definir los encabezados de las columnas
        self.table_inventory.heading("#0", text="ID", anchor="w")  # Columna de árbol
        self.table_inventory.heading("col1", text="Descripcion", anchor="w")
        self.table_inventory.heading("col2", text="Talla", anchor="w")
        self.table_inventory.heading("col3", text="Marca", anchor="w")
        self.table_inventory.heading("col4", text="Precio u.", anchor="w")
        self.table_inventory.heading("col5", text="Stock", anchor="w")

        # Definir el ancho de las columnas
        self.table_inventory.column("#0", width=50)  # Columna de árbol
        self.table_inventory.column("col1", width=150)
        self.table_inventory.column("col2", width=50)
        self.table_inventory.column("col3", width=100)
        self.table_inventory.column("col4", width=80)
        self.table_inventory.column("col5", width=50)

        response = supabase.table("product").select("*").execute()
        print(response)




    def show_students_frame(self):
        label = ttk.Label(self.content_frame, text="Este es el frame de los alumnos")
        label.pack()

if __name__ == "__main__":
    app = App()
    app.mainloop()