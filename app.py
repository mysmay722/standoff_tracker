import streamlit as st
import requests
import os
from config import MAPA_IMAGENES

st.set_page_config(layout="wide")
st.title("Galería de Mercado Standoff 2")

# Función para descargar el JSON online con caché temporal para optimizar rendimiento
@st.cache_data(ttl=30)  # Mantiene los datos en caché por 30 segundos antes de volver a consultar la URL
def obtener_precios_online():
    url = "https://standoff2markettracker.com/items.json"
    try:
        respuesta = requests.get(url)
        if respuesta.status_code == 200:
            return respuesta.json()
        else:
            st.error(f"Error de conexión con el servidor de precios (Código: {respuesta.status_code})")
            return {}
    except Exception as e:
        st.error(f"No se pudo conectar a la base de datos del mercado: {e}")
        return {}

# Descargamos el estado actual de los precios desde la URL
datos_mercado = obtener_precios_online()

# Estado de sesión para registrar la interacción del usuario
if 'skin_seleccionada' not in st.session_state:
    st.session_state.skin_seleccionada = None

# Construcción de la cuadrícula visualizada
num_columnas = 3
cols = st.columns(num_columnas)

# Despliegue de imágenes vinculadas al config.py
for i, (nombre_skin, ruta_img) in enumerate(MAPA_IMAGENES.items()):
    col_actual = cols[i % num_columnas]
    with col_actual:
        if os.path.exists(ruta_img):
            st.image(ruta_img, use_container_width=True)
            # Botón interactivo para asignar la skin seleccionada al estado de la aplicación
            if st.button(f"Ver precio de {nombre_skin}", key=nombre_skin):
                st.session_state.skin_seleccionada = nombre_skin
        else:
            st.error(f"Archivo de imagen faltante: {ruta_img}")

# --- Panel inferior de visualización de precios del JSON ---
if st.session_state.skin_seleccionada:
    st.divider()
    nombre = st.session_state.skin_seleccionada
    ruta_img = MAPA_IMAGENES[nombre]
    
    st.subheader(f"Precio en tiempo real: {nombre}")
    
    col_izq, col_der = st.columns(2)
    with col_izq:
        st.image(ruta_img, use_container_width=True)
        
    with col_der:
        precio_detectado = "No encontrado en el JSON"
        
        # Validación de formato de diccionario (Clave -> Valor)
        if isinstance(datos_mercado, dict):
            if nombre in datos_mercado:
                info_item = datos_mercado[nombre]
                if isinstance(info_item, dict):
                    precio_detectado = info_item.get("price") or info_item.get("precio") or "No definido"
                else:
                    precio_detectado = info_item
                    
        # Validación alternativa si el JSON remoto se procesa como una lista de objetos
        elif isinstance(datos_mercado, list):
            for elemento in datos_mercado:
                if elemento.get("name") == nombre or elemento.get("nombre") == nombre:
                    precio_detectado = elemento.get("price") or elemento.get("precio") or "No definido"
                    break
        
        # Muestra el indicador numérico extraído del sitio web externo
        st.metric(label="Valor del Mercado Actual", value=f"{precio_detectado}")
