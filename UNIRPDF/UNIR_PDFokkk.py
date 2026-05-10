"""
@author: E1n1k0programa@gmail.com

Si no esta instalado, escribe pip install PyPDF2, en el terminal y ejecútalo.
Coloca todos los archivos a unir en la misma carpeta que el script.
"""

from PyPDF2 import PdfMerger

# Crear el objeto mezclador
merger = PdfMerger()

# Lista de archivos a unir (escritos manualmente)
archivos = ["imagen1.pdf", "imagen2.pdf"]

# Recorrer la lista y agregar cada PDF
for pdf in archivos:
    merger.append(pdf)

# Guardar el resultado final
merger.write("PDF_Unido.pdf")
merger.close()

print("¡PDFs unidos exitosamente!")
