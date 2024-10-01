import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os
from dotenv import load_dotenv
from supabase import create_client
load_dotenv()
    
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
        """
        Muestra la interfaz para administrar los productos (CRUD)
        """
        for i in range(5):
            self.content_frame.columnconfigure(i, weight=1)

        # Creamos los labels
        for i, label in enumerate(["ID:", "Prodcuto:", "Marca:", "Talla:", "Precio Unitario:", "Stock"]):
            ttk.Label(self.content_frame, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)

        # Widgets para la entrada de datos
        self.entry_product_id = ttk.Entry(self.content_frame, state=tk.DISABLED)
        self.entry_product_id.grid(row=0, column=1, columnspan=2, sticky="nesw", padx=5, pady=5)

        self.entry_product_name = ttk.Entry(self.content_frame)
        self.entry_product_name.grid(row=1, column=1, columnspan=2, sticky="nesw", padx=5, pady=5)

        self.combobox_mark = ttk.Combobox(self.content_frame, state="readonly", values=["MOONDO", "KOS", "MOOTO", "DRAGONES ROJOS"])
        self.combobox_mark.grid(row=2, column=1, columnspan=2, sticky="nesw", padx=5, pady=5)
        
        size = [f"#{i}" for i in range(6)]
        size.extend(["#" + "X"*i + "S" for i in range(3,0,-1)])
        size.extend(["#S", "#M", "#L"])
        size.extend(["#" + "X"*i + "L" for i in range(1,4)])
        self.combobox_size = ttk.Combobox(self.content_frame, state="readonly", values=size)
        self.combobox_size.grid(row=3, column=1, columnspan=2, sticky="nesw", padx=5, pady=5)

        self.spinbox_price = ttk.Spinbox(self.content_frame, from_=0, to=2000)
        self.spinbox_price.grid(row=4, column=1, columnspan=2, sticky="nesw", padx=5, pady=5)

        self.spinbox_stock = ttk.Spinbox(self.content_frame, from_=0, to=50)
        self.spinbox_stock.grid(row=5, column=1, columnspan=2, sticky="nesw", padx=5, pady=5)
        
        # Botones de accion de CRUD
        self.btn_add_product = ttk.Button(self.content_frame, text="Agregar", command=self.add_product_to_inventory)
        self.btn_add_product.grid(row=0, column=3, sticky="nesw", padx=5, pady=5)

        self.btn_load_product_data = ttk.Button(self.content_frame, text="Cargar", command=self.load_product_data_into_form)
        self.btn_load_product_data.grid(row=1, column=3, sticky="nesw", padx=5, pady=5)

        self.btn_edit_product = ttk.Button(self.content_frame, text="Modificar", state=tk.DISABLED, command=self.edit_product)
        self.btn_edit_product.grid(row=2, column=3, sticky="nesw", padx=5, pady=5)

        self.btn_delete_product = ttk.Button(self.content_frame, text="Eliminar", command=self.delete_product_from_inventory)
        self.btn_delete_product.grid(row=3, column=3, sticky="nesw", padx=5, pady=5)

        btn_clean_product = ttk.Button(self.content_frame, text="Limpiar", command=self.clean_product_form)
        btn_clean_product.grid(row=4, column=3, sticky="nesw", padx=5, pady=5)

        # Tabla para visualizar el inventario
        self.table_inventory = ttk.Treeview(self.content_frame, columns=("descripcion", "marca", "talla", "precio", "stock"))
        # Definir los encabezados de las columnas
        self.table_inventory.heading("#0", text="ID")
        self.table_inventory.heading("descripcion", text="Descripcion")
        self.table_inventory.heading("marca", text="Marca")
        self.table_inventory.heading("talla", text="Talla")
        self.table_inventory.heading("precio", text="Precio Unitario")
        self.table_inventory.heading("stock", text="Stock")

        # Definir el ancho de las columnas
        self.table_inventory.column("#0", width=1)  # Columna de árbol
        self.table_inventory.column("descripcion", width=5)
        self.table_inventory.column("marca", width=1)
        self.table_inventory.column("talla", width=1)
        self.table_inventory.column("precio", width=1)
        self.table_inventory.column("stock", width=1)
        self.table_inventory.grid(row=6, column=0, columnspan=5, sticky="nesw", padx=5, pady=5)

        # Llenamos tabla con datos de los productos de supabase
        self.update_products_table()

    def show_students_frame(self):
        label = ttk.Label(self.content_frame, text="Este es el frame de los alumnos")
        label.pack()

    def clean_product_form(self):
        """
        Funcion para limpiar los campos del formulario de productos
        """
        # Limpiar los campos del formulario
        self.entry_product_id.configure(state=tk.NORMAL)
        self.entry_product_id.delete(0, tk.END)
        self.entry_product_id.configure(state=tk.DISABLED)
        self.entry_product_name.delete(0, tk.END)  # Borra el campo de texto
        self.combobox_size.set('')  # Restablece el combobox de talla
        self.combobox_mark.set('')  # Restablece el combobox de marca
        self.spinbox_price.delete(0, tk.END)  # Borra el valor del Spinbox de precio
        self.spinbox_stock.delete(0, tk.END)  # Borra el valor del Spinbox de stock

    def update_products_table(self):
        """
        Esta funcion limpia y llena la lista de productos de supabase
        """
        # Eliminar filas
        rows = self.table_inventory.get_children()
        for row in rows:
            self.table_inventory.delete(row)

        # Obtener datos de supabase y llenar tabla
        # Llenamos la tabla con datos de la DB
        response = supabase.table("producto").select("*").execute()
        for row in response.data:
            self.table_inventory.insert(
                "",
                tk.END,
                text=row["id_producto"],
                values=(row["descripcion"], row["marca"], row["talla"], row["precio_unitario"], row["stock"])
            )

    def validate_product_form(self):
        product = {
            "name": self.entry_product_name.get().upper(),
            "mark" : self.combobox_mark.get(),
            "size" : self.combobox_size.get(),
            "price" : self.spinbox_price.get(),
            "stock" : self.spinbox_stock.get(),
            "validate": False
        }

        # Validar que los campos no estén vacíos
        if not product["name"]:
            messagebox.showerror("Error", "El nombre del producto es obligatorio.")
            return product
        if not product["mark"]:
            messagebox.showerror("Error", "La marca es obligatoria.")
            return product
        if not product["size"]:
            messagebox.showerror("Error", "La talla es obligatoria.")
            return product

        # Validar que el precio sea un número positivo
        try:
            price_value = float(product["price"])
            if price_value <= 0:
                messagebox.showerror("Error", "El precio debe ser un valor positivo.")
                return product
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return product

        # Validar que el stock sea un número entero no negativo
        try:
            stock_value = int(product["stock"])
            if stock_value < 0:
                messagebox.showerror("Error", "El stock no puede ser negativo.")
                return product
        except ValueError:
            messagebox.showerror("Error", "El stock debe ser un número entero válido.")
            return product

        # Si todas las validaciones pasan
        product["validate"] = True
        return product

    def add_product_to_inventory(self):
        """
        Agrega un nuevo producto al inventario
        """
        product = self.validate_product_form()
        if product["validate"]:
            response = (
                supabase.table("producto")
                .insert({
                    "descripcion": product["name"],
                    "marca": product["mark"],
                    "talla": product["size"],
                    "precio_unitario": product["price"],
                    "stock": product["stock"]
                    })
                .execute()
            )

            # Rellenamos tabla con nuevos datos
            self.update_products_table()
            self.clean_product_form()

    def delete_product_from_inventory(self):
        """
        Funcion que elimina un producto de la tabla de inventario
        """
        # Verifica si existe un regristro seleccionado en la tabla
        row_selected = self.table_inventory.item(self.table_inventory.selection())
        if not row_selected["text"]:
            messagebox.showerror("Error","Seleccione un registro")
        else:
            product_id = row_selected["text"]
            product_name = row_selected["values"][0]

            if messagebox.askokcancel("Eliminar Registro", f"¿Estas segur@ de eliminar {product_name} de la BD?"):
                # Eliminamos el registro en la base de datos (supabase)
                response = supabase.table('producto').delete().eq('id_producto', product_id).execute()
                
                # Actualizamos la tabla
                self.update_products_table()

    def edit_product(self):
        self.btn_add_product.configure(state=tk.NORMAL)
        self.btn_load_product_data.configure(state=tk.NORMAL)
        self.btn_edit_product.configure(state=tk.DISABLED)
        self.btn_delete_product.configure(state=tk.NORMAL)
        
        product = self.validate_product_form()
        if product["validate"]:
            response = (
                supabase.table("producto")
                .update({
                    "descripcion": product["name"],
                    "marca": product["mark"],
                    "talla": product["size"],
                    "precio_unitario": product["price"],
                    "stock": product["stock"]
                    })
                .eq("id_producto", self.entry_product_id.get())
                .execute()
            )
            self.clean_product_form()
            self.update_products_table()

    def load_product_data_into_form(self):
        # Verifica si existe un regristro seleccionado en la tabla
        row_selected = self.table_inventory.item(self.table_inventory.selection())
        product_id = row_selected["text"]
        if not product_id:
            messagebox.showerror("Error","Seleccione un registro")
        else:
            # Deshabilitamos botones
            self.btn_add_product.configure(state=tk.DISABLED)
            self.btn_load_product_data.configure(state=tk.DISABLED)
            self.btn_edit_product.configure(state=tk.NORMAL)
            self.btn_delete_product.configure(state=tk.DISABLED)

            # Obtenemos valores del registro seleccionado
            product_name, mark, size, price, stock = row_selected["values"]
            # Cargamos datos en el formulario
            self.entry_product_id.configure(state=tk.NORMAL)
            self.entry_product_id.insert(0, product_id)
            self.entry_product_id.configure(state=tk.DISABLED)
            self.entry_product_name.insert(0, product_name)
            self.combobox_mark.set(mark)
            self.combobox_size.set(size)
            self.spinbox_price.set(price)
            self.spinbox_stock.set(stock)

        
if __name__ == "__main__":
    app = App()
    app.mainloop()