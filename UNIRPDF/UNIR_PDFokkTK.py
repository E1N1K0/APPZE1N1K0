#Unir Pdf:

#Si no esta instalado, en terminal escribe: pip install PyPDF4

#Primero instalar librerias! 

#importar módulos para interfaz gráfica:
import tkinter as tk
from tkinter import filedialog

#Importar modulo para trabajar con PDF:
from PyPDF4 import PdfFileMerger

#crear instancia de PdfFileMerge
unir = PdfFileMerger()
#Crear lista vacía para los PDF:
pdfs_a_unir = []

#función para que el usuario seleccione archivos PDF y se agreguen a la lista.
def seleccionar_archivos():
    global pdfs_a_unir
    filenames = filedialog.askopenfilenames(
        title="Selecciona PDFs (usa CTRL)",
        filetypes=(("Archivos PDF", "*.pdf"), )
    )
    
    pdfs_a_unir.extend(filenames)
    label["text"] = "Archivos seleccionados: "+str(len(pdfs_a_unir))

#funcion que itera, une al pdf anterior.
def unir_pdfs():
    global pdfs_a_unir, unir
    
    for pdf in pdfs_a_unir:
        unir.append(pdf)
  
#write escribe el pdf unido:  
    unir.write("pdf_unido.pdf")
    label["text"] += "\n¡PDFs unidos!"

#ENTORNO TKINTER: 
ventana = tk.Tk()
#Tamaño ventana:
ventana.geometry("300x200")

#Titulo entorno:
ventana.title("Unir PDFs")

#Boton para agregar pdf:
button1 = tk.Button(ventana, text="Selecciona PDFs", command=seleccionar_archivos)
button1.pack()

#Boton para unir pdf:
button2 = tk.Button(ventana, text="Unir PDFs", command=unir_pdfs)
button2.pack()
  
label = tk.Label(ventana, text="")
label.pack()
  
ventana.mainloop()
