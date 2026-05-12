# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 01:11:11 2024

@author: Nicolas
"""

# Approximate color palette based on the provided image
colors = [
    '#DB805A', # Soft orange
    '#F2C643', # Yellow
    '#E6C37E', # Light beige-yellow
    '#6D8458', # Olive green
    '#B57C61', # Light dusty pink, 
    '#D49E8D', # Light brown-pink
    '#8A6A63', # Muted brown
    '#A1BD4D', # Light olive green
    '#C75856', # Muted red
    '#E5544D', # Bright red
    '#CBBBA0', # Beige-gray
    '#6DA2A5'  # Soft teal
]

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.backends.backend_svg as svg

# Cargar los datos desde el archivo Excel
data = pd.read_excel('HOJA_TABULADA03.xlsx', sheet_name='BBDD', header=0)

# El archivo tiene columnas adicionales con valores null, vamos a usar solo las primeras 5 columnas
print("Forma original del DataFrame:", data.shape)
print("Columnas originales:", data.columns.tolist())

# Tomar solo las primeras 5 columnas que contienen los datos que necesitamos
data = data.iloc[:, :5]

# Renombrar correctamente las columnas intercambiando TIPO_DESCRIPTOR y DESCRIPTOR
data.columns = ['PRODUCTO', 'NOMBRE', 'DESCRIPTOR', 'TIPO_DESCRIPTOR', 'INTENSIDAD']

print("Forma final del DataFrame:", data.shape)
print("Columnas finales:", data.columns.tolist())
print("Primeras filas:")
print(data.head())

# Remover filas vacías
data = data.dropna(subset=['PRODUCTO', 'DESCRIPTOR'])

# Agrupar datos por PRODUCTO, DESCRIPTOR y TIPO_DESCRIPTOR para promediar las intensidades de múltiples evaluadores
data = data.groupby(['PRODUCTO', 'DESCRIPTOR', 'TIPO_DESCRIPTOR'])['INTENSIDAD'].mean().reset_index()

# Filtrar por tipo de descriptor y productos únicos
productos = data['PRODUCTO'].unique()
tipos_descriptor = ['AROMA', 'SABOR']

print("Productos disponibles:", productos)
print("Tipos de descriptor:", tipos_descriptor)

# Crear directorio de salida para los gráficos
output_dir = "GRAFICA_CIRCULAR"
os.makedirs(output_dir, exist_ok=True)

# Encontrar la intensidad máxima global para normalizar todos los gráficos
max_intensidad_global = data['INTENSIDAD'].max()
print(f"Intensidad máxima global: {max_intensidad_global}")

# Configuración para establecer el punto de partida para intensidades menores
inicio_desde_porc_max = True  # Cambia a False si no deseas que inicie desde un % del valor máximo

# Variable de control para normalizar o no los gráficos
normalizar = False  # Cambia a False si no deseas normalizar las intensidades

# Configuración para limitar las longitudes de los pedazos de pastel
limitar_longitud_pastel = True  # Cambia a False si no deseas limitar la longitud del pastel

def crear_grafico_vectorial(df, producto, tipo_descriptor, max_intensidad_global, normalizar):
    """
    Create radar chart for hop sensory analysis
    """
    # Filtrar datos por producto y tipo_descriptor
    data_filtrada = df[(df['PRODUCTO'] == producto) & 
                       (df['TIPO_DESCRIPTOR'] == tipo_descriptor)]
    
    if data_filtrada.empty:
        print(f"No se encontraron datos para {producto} - {tipo_descriptor}")
        return
    
    # Obtener los descriptores y sus intensidades (ya están agrupados)
    descriptores = data_filtrada['DESCRIPTOR']
    intensidades = data_filtrada['INTENSIDAD']
    
    print(f"\nProcesando {producto} - {tipo_descriptor}:")
    for desc, intens in zip(descriptores, intensidades):
        print(f"  {desc}: {intens:.1f}")
    
    # Determinar la intensidad máxima de normalización para cada gráfico
    max_intensidad = max_intensidad_global if normalizar else intensidades.max()
    
    # Calcular la longitud inicial para intensidades mínimas distintas de cero
    intensidad_min = intensidades[intensidades > 0].min() if (intensidades > 0).any() else 0
    
    # Radio de la corona donde estarán las etiquetas de los descriptores
    corona_radio = max_intensidad * 1.1
    limite_radio = 0.9 * corona_radio
    
    # Escalar intensidades si se activa la configuración de límite de longitud
    if limitar_longitud_pastel and max_intensidad > limite_radio:
        escala = limite_radio / max_intensidad
        intensidades = intensidades * escala
        max_intensidad *= escala
    
    # Configuración para establecer la longitud de inicio de la intensidad mínima
    inicio_longitud = 0.7 * limite_radio if inicio_desde_porc_max else 0
    
    # Crear segmentos de ángulo iguales
    num_descriptores = len(descriptores)
    theta = np.linspace(0, 2 * np.pi, num_descriptores, endpoint=False)
    width = 2 * np.pi / num_descriptores
    
    # Crear figura con dimensiones fijas en pulgadas (aproximadamente 2000 píxeles de ancho)
    fig, ax = plt.subplots(figsize=(2000/300, 2000/300), subplot_kw=dict(polar=True))
    
    # Graficar cada segmento del gráfico principal
    for i, (desc, intensidad) in enumerate(zip(descriptores, intensidades)):
        altura_base = intensidad
        if intensidad > 0 and intensidad < max_intensidad and intensidad_min > 0:
            factor_escala = (limite_radio - inicio_longitud) / (max_intensidad - intensidad_min)
            altura_barra = inicio_longitud + (altura_base - intensidad_min) * factor_escala
        else:
            altura_barra = altura_base * (limite_radio / max_intensidad) if max_intensidad > 0 else 0
        
        # Usar color basado en el índice del descriptor
        color_idx = i % len(colors)
        ax.bar(theta[i], altura_barra, width=width, color=colors[color_idx], 
               edgecolor='black', linewidth=0.5)
    
    # Añadir la corona externa coloreada
    corona_ancho = max_intensidad * 0.3
    
    for i, desc in enumerate(descriptores):
        color_idx = i % len(colors)
        ax.bar(theta[i], corona_ancho, 
               bottom=corona_radio,  
               width=width, 
               color=colors[color_idx],
               edgecolor='black',
               alpha=1,
               linewidth=0.5)
    
    # Añadir líneas de cuadrícula radiales
    for angle in theta:
        desplazamiento = width / 2
        ax.plot([angle - desplazamiento, angle + desplazamiento], 
                [0, corona_radio], 
                color='gray', 
                linestyle='--', 
                linewidth=0.5, 
                alpha=0.2)
    
    # Configurar límites del gráfico
    ax.set_ylim(0, max_intensidad * 1.5)

    # Configuración para el texto de los descriptores
    altura_texto_descriptor = corona_radio + corona_ancho / 2
    
    for i, (label, intensidad) in enumerate(zip(descriptores, intensidades)):
        angle_rad = theta[i]
        
        # Ajustar la rotación del texto
        rotation = np.degrees(angle_rad) + 90
        if rotation > 90 and rotation <= 270:
            rotation = rotation - 180
            
        # Procesar el texto para agregar saltos de línea si contiene espacios
        words = label.split()
        lines = []
        words_per_line = 1  # Ajustar este número para controlar cuántas palabras por línea
        
        for j in range(0, len(words), words_per_line):
            line = ' '.join(words[j:j + words_per_line])
            lines.append(line)
        
        label_with_breaks = '\n'.join(lines)
        
        # Dibujar el texto del descriptor con la nueva altura y formato
        ax.text(angle_rad, altura_texto_descriptor, label_with_breaks,
                ha='center', va='center',
                rotation=rotation,
                fontsize=10,
                color='black',
                linespacing=1.2)
        
        # Dibujar el valor de intensidad
        ax.text(angle_rad, corona_radio + corona_ancho * 1.5, f'{intensidad:.1f}',
                ha='center', va='center',
                rotation=rotation,
                fontsize=11,
                fontweight='bold',
                color='black')

    # Configurar ejes
    ax.set_yticklabels([])
    ax.xaxis.set_visible(False)
    
    # Configurar cuadrícula
    ax.yaxis.set_major_locator(plt.LinearLocator(5))
    
    for line in ax.yaxis.get_gridlines():
        line.set_linestyle('--')
        line.set_linewidth(0.5)
        line.set_alpha(0.5)
        line.set_color('gray')
    
    # Guardar el gráfico
    # Limpiar el nombre del archivo removiendo caracteres especiales
    producto_clean = producto.replace('(', '').replace(')', '').replace(' ', '_')
    file_name = f"{output_dir}/{producto_clean}_{tipo_descriptor}.jpg"
    fig.savefig(file_name, format='jpg', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    
    print(f"Gráfico guardado: {file_name}")
    plt.close(fig)

# Generar gráficos vectoriales para cada combinación
print("Generando gráficos radar...")
for producto in productos:
    for tipo_descriptor in tipos_descriptor:
        crear_grafico_vectorial(data, producto, tipo_descriptor, max_intensidad_global, normalizar)

print(f"\nTodos los gráficos generados en el directorio: {output_dir}")
print("Combinaciones disponibles:")
for producto in productos:
    for tipo_descriptor in tipos_descriptor:
        print(f"  - {producto} ({tipo_descriptor})")