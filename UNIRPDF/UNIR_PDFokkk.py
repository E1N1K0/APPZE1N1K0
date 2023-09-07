#Unir Pdf:

#Primero instalar librerias! pip install PyPDF4
from PyPDF4 import PdfFileMerger

merger = PdfFileMerger()

#Agrega los pdf a unir:
merger.append('imagen1.pdf')
merger.append('imagen2.pdf')

#Genera archivo pf final:
merger.write('pdf_unido.pdf')
merger.close
