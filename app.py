import streamlit as st
# Importamos el diccionario que creaste en config.py
from config import MAPA_IMAGENES

# Configuración de la página
st.set_page_config(page_title="Standoff Tracker", layout="wide")

st.title("🔫 Galería de Mercado Standoff 2")
st.write("Selecciona una skin para ver su análisis detallado:")

# Creamos una lista con los nombres de las armas disponibles en tu config
lista_armas = list(MAPA_IMAGENES.keys())

# Creamos un menú desplegable (Selectbox) para elegir el arma
arma_seleccionada = st.selectbox("Elige un arma:", lista_armas)

# Obtenemos la ruta de la imagen correspondiente al arma seleccionada
ruta_img = MAPA_IMAGENES.get(arma_seleccionada)

# --- AQUÍ ESTÁ EL "SEGURO" PARA EL ERROR ROJO ---
# Solo intentamos mostrar la imagen si la variable ruta_img tiene contenido
if ruta_img:
    st.image(ruta_img, use_container_width=True)
else:
    st.warning("La imagen para esta arma no está configurada correctamente.")

# Aquí puedes añadir más contenido debajo de la imagen cuando la tengas
st.write(f"Has seleccionado: {arma_seleccionada}")
