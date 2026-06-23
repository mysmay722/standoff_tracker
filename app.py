import streamlit as st
import os
from config import MAPA_IMAGENES

st.set_page_config(layout="wide") # Esto expande la app para que quepan más imágenes
st.title("Galería de Mercado Standoff 2")

# Definimos el número de columnas para la cuadrícula
num_columnas = 3
cols = st.columns(num_columnas)

# Iteramos sobre el diccionario de imágenes
for i, (nombre_skin, ruta_img) in enumerate(MAPA_IMAGENES.items()):
    # Usamos el operador módulo (%) para alternar entre columnas
    col_actual = cols[i % num_columnas]
    
    with col_actual:
        # Verificamos si la imagen existe antes de mostrarla
        if os.path.exists(ruta_img):
            st.image(ruta_img, caption=nombre_skin, use_container_width=True)
        else:
            st.error(f"Imagen no encontrada: {nombre_skin}")
            st.write(f"Ruta fallida: {ruta_img}")
