import streamlit as st
import os
# Importamos el diccionario desde tu archivo config.py
from config import MAPA_IMAGENES

st.title("Galería de Mercado Standoff 2")

# Selecciona una skin
# Usamos las llaves del diccionario para el menú desplegable
opciones = list(MAPA_IMAGENES.keys())
seleccion = st.selectbox("Selecciona una skin para ver su análisis detallado:", opciones)

# Obtenemos la ruta de la imagen
ruta_img = MAPA_IMAGENES[seleccion]

# Verificación de seguridad: ¿Existe la imagen antes de intentar cargarla?
if os.path.exists(ruta_img):
    st.image(ruta_img, use_container_width=True)
else:
    st.error(f"Error: No se pudo encontrar el archivo de imagen en: {ruta_img}")
    st.write("Asegúrate de que el nombre del archivo en la carpeta 'assets' coincida exactamente con lo escrito en config.py.")
