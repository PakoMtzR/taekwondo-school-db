import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from dotenv import load_dotenv
load_dotenv()
    
import os
from supabase import create_client

# https://supabase.com/docs/reference/python/introduction

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
        """
        Funcion para construir los widgets de nuestra aplicacion
        """
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

        # Iniciamos la aplicacion con la ventana de bienvenida
        self.show_frame(self.btn_welcome, 1)

    def deselect_options_btns(self):
        """
        Restablece los botones del menu de opciones en su forma original
        """
        # Restablecer todos los botones(labels) a su color original
        self.btn_welcome.configure(bg=self.COLOR_GRAY)
        self.btn_inventory.configure(bg=self.COLOR_GRAY)
        self.btn_students.configure(bg=self.COLOR_GRAY)

    def show_frame(self, btn_option:tk.Label, frame_number:int):
        """
        Muestra en el frame de contenido la opcion del menu seleccionado
        """
        self.deselect_options_btns()                # Deseleccionar todos los labels (volviendo a su color original)
        btn_option.configure(bg=self.COLOR_THEME)   # Seleccionar el label actual
        self.clear_content_frame()                  # Cambiar el contenido en el Frame de la derecha

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
        """
        Elimina todos los widgets en el Frame de contenido
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_welcome_frame(self):
        label = ttk.Label(self.content_frame, text="Bienvenido!")
        label.pack()

    def show_inventory_frame(self):
        for i in range(6):
            self.content_frame.columnconfigure(i, weight=1)

        # Widgets para la busqueda de productos
        label_product = ttk.Label(self.content_frame, text="Producto:")
        label_product.grid(row=0, column=0, sticky="e", padx=5, pady=5)

        self.textbox = ttk.Entry(self.content_frame)
        self.textbox.grid(row=0, column=1, columnspan=3, sticky="nesw", padx=5, pady=5)

        btn_search = ttk.Button(self.content_frame, text="Buscar")
        btn_search.grid(row=0, column=4, sticky="nesw", padx=5, pady=5)

        btn_clean = ttk.Button(self.content_frame, text="Limpiar")
        btn_clean.grid(row=0, column=5, sticky="nesw", padx=5, pady=5)

        # Botones para CRUD -> Add/Edit/Delete
        btn_add_product = ttk.Button(self.content_frame, text="Agregar", command=self.open_product_window)
        btn_add_product.grid(row=1, column=0, columnspan=2, sticky="nesw", padx=5, pady=5)

        btn_edit_product = ttk.Button(self.content_frame, text="Modificar")
        btn_edit_product.grid(row=1, column=2, columnspan=2, sticky="nesw", padx=5, pady=5)

        btn_delete_product = ttk.Button(self.content_frame, text="Eliminar")
        btn_delete_product.grid(row=1, column=4, columnspan=2, sticky="nesw", padx=5, pady=5)
        
        # Tabla para visualizar el inventario
        self.table_inventory = ttk.Treeview(self.content_frame, columns=("descripcion", "talla", "marca", "precio", "stock"))
        # Definir los encabezados de las columnas
        self.table_inventory.heading("#0", text="ID")
        self.table_inventory.heading("descripcion", text="Descripcion")
        self.table_inventory.heading("talla", text="Talla")
        self.table_inventory.heading("marca", text="Marca")
        self.table_inventory.heading("precio", text="Precio Unitario")
        self.table_inventory.heading("stock", text="Stock")

        # Definir el ancho de las columnas
        self.table_inventory.column("#0", width=20)  # Columna de árbol
        self.table_inventory.column("descripcion", width=150)
        self.table_inventory.column("talla", width=20)
        self.table_inventory.column("marca", width=50)
        self.table_inventory.column("precio", width=50)
        self.table_inventory.column("stock", width=50)
        self.table_inventory.grid(row=2, column=0, columnspan=6, sticky="nesw")

        response = supabase.table("producto").select("*").execute()
        for row in response.data:
            self.table_inventory.insert(
                "",
                tk.END,
                text=row["id_producto"],
                values=(row["descripcion"], row["talla"], row["id_marca"], row["precio_unitario"], row["stock"])
            )

    def show_students_frame(self):
        label = ttk.Label(self.content_frame, text="Este es el frame de los alumnos")
        label.pack()

    def open_product_window(self):
        """
        Esta funcion abre una ventana emergente (formulario) para poder agregar o modificar un producto 
        """
        self.edit_window = tk.Toplevel()
        self.edit_window.title("Editar Registro")
        self.edit_window.geometry("360x200")
        self.edit_window.resizable(False, False)
        self.edit_window.columnconfigure(0, weight=0)
        self.edit_window.columnconfigure(1, weight=1)
        
        # Creamos los labels del formulario
        for i, label in enumerate(["Producto:", "Talla:", "Marca:", "Precio Unitario:", "Stock:"]):
            ttk.Label(self.edit_window, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
        
        self.entry_product_description = ttk.Entry(self.edit_window)
        self.entry_product_description.grid(row=0, column=1, sticky="nesw", padx=5, pady=5)
        self.entry_size = ttk.Entry(self.edit_window)
        self.entry_size.grid(row=1, column=1, sticky="nesw", padx=5, pady=5)
        self.entry_mark = ttk.Entry(self.edit_window)
        self.entry_mark.grid(row=2, column=1, sticky="nesw", padx=5, pady=5)
        self.entry_price = ttk.Spinbox(self.edit_window, from_=0)
        self.entry_price.grid(row=3, column=1, sticky="nesw", padx=5, pady=5)
        self.entry_stock = ttk.Spinbox(self.edit_window, from_=0)
        self.entry_stock.grid(row=4, column=1, sticky="nesw", padx=5, pady=5)

        ttk.Button(self.open_product_window, text="Aceptar").grid(row=5, column=0, columnspan=2, padx=10, pady=10)

if __name__ == "__main__":
    app = App()
    app.mainloop()