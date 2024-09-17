import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry

# Función que se ejecuta cuando se presiona el botón
def show_date():
    selected_date = date_entry.get()
    result_label.config(text=f"Fecha seleccionada: {selected_date}")

# Crear la ventana principal
root = tk.Tk()
root.title("Aplicación con DateEntry")
root.geometry("300x200")

# Crear un marco para organizar los widgets
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Etiqueta para el DateEntry
date_label = ttk.Label(frame, text="Selecciona una fecha:")
date_label.grid(row=0, column=0, padx=5, pady=5)

# Crear el DateEntry
date_entry = DateEntry(frame, width=12, background='darkblue', foreground='white', borderwidth=2)
date_entry.grid(row=0, column=1, padx=5, pady=5)

# Botón para mostrar la fecha seleccionada
show_button = ttk.Button(frame, text="Mostrar Fecha", command=show_date)
show_button.grid(row=1, column=0, columnspan=2, pady=10)

# Etiqueta para mostrar el resultado
result_label = ttk.Label(frame, text="")
result_label.grid(row=2, column=0, columnspan=2, pady=5)

# Ejecutar la aplicación
root.mainloop()
