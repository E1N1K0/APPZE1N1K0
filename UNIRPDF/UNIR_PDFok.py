#Unir Pdf:

#Primero instalar librerias!
import PyPDF2

#Definir funcion:
def unir_pdf(archivos, nombre_salida):

#Define lista de archivos pdf a unir:
    archivos = ["imagen1.pdf",
                "imagen2.pdf"]

#Nombre del pdf final unido:
    nombre_salida = "pdf_unido.pdf"

    pdf_final = PyPDF2.PdfMerger()

#Itera a todos los archivos de la lista:
    for nombre_archivo in archivos:
        pdf_final.append(nombre_archivo)

#Genera pdf:
    pdf_final.write(nombre_salida)
    pdf_final.close()

#Ejecucion:
archivos = ["imagen1.pdf",
            "imagen2.pdf"]

nombre_salida = "pdf_unido.pdf"

unir_pdf(archivos, nombre_salida)
