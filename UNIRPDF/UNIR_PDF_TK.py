"""
@author: E1n1k0programa@gmail.com

Unir Pdf:

Si no esta instalado, escribe pip install PyPDF2, en el terminal y ejecútalo.
Coloca todos los archivos a unir en la misma carpeta que el script.
"""

import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger
import os

def agregar_archivos():
    """Abre un diálogo para seleccionar archivos PDF y los añade a la lista."""
    archivos_seleccionados = filedialog.askopenfilenames(
        title="Seleccionar archivos PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    
    for archivo in archivos_seleccionados:
        lista_archivos.insert(tk.END, archivo)

def limpiar_lista():
    """Elimina todos los archivos de la lista."""
    lista_archivos.delete(0, tk.END)

def unir_pdfs():
    """Realiza la unión de los PDFs listados."""
    rutas = lista_archivos.get(0, tk.END)
    
    if not rutas:
        messagebox.showwarning("Advertencia", "No has seleccionado ningún archivo para unir.")
        return

    # Nombre por defecto fijo a "unido.pdf"
    nombre_salida = "unido.pdf"

    # Abrir diálogo para elegir dónde guardar
    ruta_guardado = filedialog.asksaveasfilename(
        title="Guardar PDF unido como...",
        initialfile=nombre_salida,  # Predefine el nombre "unido" en el cuadro de diálogo
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")]
    )

    if not ruta_guardado:
        return  # El usuario canceló el guardado

    try:
        merger = PdfMerger()
        
        for pdf in rutas:
            merger.append(pdf)
        
        merger.write(ruta_guardado)
        merger.close()
        
        messagebox.showinfo("Éxito", f"¡PDFs unidos exitosamente!\nGuardado en:\n{ruta_guardado}")
        limpiar_lista()
        
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error al unir los archivos:\n{str(e)}")

# --- Configuración de la Interfaz Gráfica ---

root = tk.Tk()
root.title("Unir PDFs")
root.geometry("500x350")

# Lista para mostrar archivos
tk.Label(root, text="Archivos a unir (en orden):").pack(pady=(15, 0))
frame_lista = tk.Frame(root)
frame_lista.pack(pady=5, fill=tk.BOTH, expand=True, padx=10)

scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_archivos = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set)
lista_archivos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=lista_archivos.yview)

# Botones de acción
frame_botones = tk.Frame(root)
frame_botones.pack(pady=15)

btn_agregar = tk.Button(frame_botones, text="Agregar PDFs", command=agregar_archivos, bg="#DDDDDD")
btn_agregar.pack(side=tk.LEFT, padx=10)

btn_limpiar = tk.Button(frame_botones, text="Limpiar Lista", command=limpiar_lista, bg="#DDDDDD")
btn_limpiar.pack(side=tk.LEFT, padx=10)

btn_unir = tk.Button(frame_botones, text="UNIR PDFs", command=unir_pdfs, bg="#90EE90", font=("Arial", 10, "bold"))
btn_unir.pack(side=tk.LEFT, padx=10)

# Iniciar la aplicación
root.mainloop()
root.title("Unir PDFs")
root.geometry("500x400")

# Etiqueta y Campo para el nombre de salida
frame_nombre = tk.Frame(root)
frame_nombre.pack(pady=10)


# Lista para mostrar archivos
tk.Label(root, text="Archivos a unir (en orden):").pack(pady=(10, 0))
frame_lista = tk.Frame(root)
frame_lista.pack(pady=5, fill=tk.BOTH, expand=True, padx=10)


scrollbar = tk.Scrollbar(frame_lista)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

lista_archivos = tk.Listbox(frame_lista, yscrollcommand=scrollbar.set)
lista_archivos.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=lista_archivos.yview)

# Botones de acción
frame_botones = tk.Frame(root)
frame_botones.pack(pady=15)

btn_agregar = tk.Button(frame_botones, text="Agregar PDFs", command=agregar_archivos, bg="#DDDDDD")
btn_agregar.pack(side=tk.LEFT, padx=10)

btn_limpiar = tk.Button(frame_botones, text="Limpiar Lista", command=limpiar_lista, bg="#DDDDDD")
btn_limpiar.pack(side=tk.LEFT, padx=10)

btn_unir = tk.Button(frame_botones, text="UNIR PDFs", command=unir_pdfs, bg="#90EE90", font=("Arial", 10, "bold"))
btn_unir.pack(side=tk.LEFT, padx=10)

# Iniciar la aplicación
root.mainloop()
