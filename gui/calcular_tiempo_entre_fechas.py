import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Función para calcular la diferencia entre fechas
def calcular_diferencia():
    try:
        fecha1 = datetime.strptime(entry_fecha1.get(), '%Y-%m-%d')
        fecha2 = datetime.strptime(entry_fecha2.get(), '%Y-%m-%d')
        
        # Asegurar que la primera fecha sea menor o igual a la segunda
        if fecha1 > fecha2:
            fecha1, fecha2 = fecha2, fecha1

        # Calcular la diferencia
        diferencia = relativedelta(fecha2, fecha1)
        
        # Mostrar el resultado
        resultado = f"Diferencia: {diferencia.years} años, {diferencia.months} meses, y {diferencia.days} días."
        label_resultado.config(text=resultado)
    except ValueError:
        messagebox.showerror("Error", "Formato de fecha incorrecto. Usa el formato YYYY-MM-DD.")

# Configuración de la ventana principal
root = tk.Tk()
root.title("Calculadora de Diferencia de Fechas")

# Crear los widgets
label_instruccion = tk.Label(root, text="Ingresa las fechas en el formato YYYY-MM-DD:")
label_fecha1 = tk.Label(root, text="Fecha 1:")
entry_fecha1 = tk.Entry(root)
label_fecha2 = tk.Label(root, text="Fecha 2:")
entry_fecha2 = tk.Entry(root)
btn_calcular = tk.Button(root, text="Calcular Diferencia", command=calcular_diferencia)
label_resultado = tk.Label(root, text="")

# Colocar los widgets en la ventana
label_instruccion.grid(row=0, column=0, columnspan=2, pady=5)
label_fecha1.grid(row=1, column=0, pady=5)
entry_fecha1.grid(row=1, column=1, pady=5)
label_fecha2.grid(row=2, column=0, pady=5)
entry_fecha2.grid(row=2, column=1, pady=5)
btn_calcular.grid(row=3, column=0, columnspan=2, pady=5)
label_resultado.grid(row=4, column=0, columnspan=2, pady=5)

root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)
# Ejecutar el loop principal de la aplicación
root.mainloop()
