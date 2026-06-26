import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime
from config import MAPA_IMAGENES

st.set_page_config(page_title="Dashboard Pro", layout="wide")

st.title("📊 Análisis de Mercado Standoff 2")
st.write(f"📅 **Fecha de hoy:** {datetime.now().strftime('%A, %d de %B de %Y')}")

if not pd.io.common.file_exists("historial_precios.csv"):
    st.warning("El bot aún no ha guardado datos. Espera unos minutos.")
    st.stop()

# Cargar y preparar datos
df = pd.read_csv("historial_precios.csv", names=["Fecha", "Skin", "Precio"])
df["Fecha"] = pd.to_datetime(df["Fecha"])

# Inicializar estado para los botones de la galería
if 'skin_seleccionada' not in st.session_state:
    st.session_state.skin_seleccionada = None

st.subheader("Galería de Skins")

# --- CONSTRUCCIÓN DE LA CUADRÍCULA ---
num_columnas = 3
cols = st.columns(num_columnas)

for i, (nombre_skin, ruta_img) in enumerate(MAPA_IMAGENES.items()):
    col_actual = cols[i % num_columnas]
    with col_actual:
        if os.path.exists(ruta_img):
            st.image(ruta_img, use_container_width=True)
            # El botón activa el análisis de la skin
            if st.button(f"Ver Análisis de {nombre_skin}", key=f"btn_{nombre_skin}"):
                st.session_state.skin_seleccionada = nombre_skin
        else:
            st.error(f"Imagen faltante en la carpeta assets: {ruta_img}")

# --- SECCIÓN DE GRÁFICAS Y ESTADÍSTICAS ---
if st.session_state.skin_seleccionada:
    skin_actual = st.session_state.skin_seleccionada
    st.divider()
    
    # Mostrar título e imagen pequeña al lado de la gráfica
    col_img, col_tit = st.columns([1, 4])
    with col_img:
        if os.path.exists(MAPA_IMAGENES.get(skin_actual, "")):
            st.image(MAPA_IMAGENES[skin_actual], use_container_width=True)
    with col_tit:
        st.subheader(f"Tendencia Histórica: {skin_actual}")

    # Filtrar el DataFrame
    df_skin = df[df["Skin"] == skin_actual].copy()

    # Si no hay datos en el CSV para esa skin exacta
    if df_skin.empty:
        st.warning(f"No hay registros en el historial para: {skin_actual}. Verifica que el nombre coincida exactamente con el del CSV.")
    else:
       # --- CREACIÓN DE LA GRÁFICA OPTIMIZADA Y ESTÁTICA ---
        fig = px.line(
            df_skin, 
            x="Fecha", 
            y="Precio",
            markers=True,  # Añade puntos en cada registro para facilitar el clic/hover
        )

        # Personalización del diseño (Estilo limpio y profesional)
        fig.update_traces(
            line=dict(color="#FF4B4B", width=3),  # Línea un poco más gruesa y estilizada
            marker=dict(size=6, color="#1f77b4"),
            # Cambiamos el diseño del cuadro flotante al pasar el mouse (Tooltip)
            hovertemplate="<b>📅 Fecha:</b> %{x|%d %b, %H:%M}<br><b>💰 Precio:</b> %{y} G<extra></extra>"
        )

        fig.update_layout(
            hovermode="x unified",  # Traza una línea vertical guía al pasar el mouse
            showlegend=False,
            margin=dict(l=10, r=10, t=40, b=10),
            plot_bgcolor="rgba(0,0,0,0)",  # Fondo transparente para adaptarse al tema de Streamlit
            paper_bgcolor="rgba(0,0,0,0)",
            # Títulos de los ejes vacíos si quieres un diseño ultra limpio como la otra web
            xaxis_title="",
            yaxis_title="",
        )

        # 🔒 BLOQUEO DE EJES Y CONFIGURACIÓN DE BOTONES DE TIEMPO
        fig.update_xaxes(
            showgrid=True,
            gridcolor="rgba(128, 128, 128, 0.2)",  # Cuadrícula muy suave
            fixedrange=True,  # 🚫 EVITA QUE EL USUARIO ARRASTRE LA GRÁFICA AL INFINITO EN X
            rangeselector=dict(
                font=dict(size=12),
                buttons=list([
                    dict(count=7, label="1S", step="day", stepmode="backward"),
                    dict(count=1, label="1M", step="month", stepmode="backward"),
                    dict(count=3, label="3M", step="month", stepmode="backward"),
                    dict(count=6, label="6M", step="month", stepmode="backward"),
                    dict(step="all", label="Todo")
                ]),
                bgcolor="rgba(255, 75, 75, 0.1)",  # Color de fondo de los botones
                activecolor="#FF4B4B",              # Color del botón seleccionado
            )
        )

        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(128, 128, 128, 0.2)",
            fixedrange=True  # 🚫 EVITA QUE EL USUARIO ARRASTRE LA GRÁFICA AL INFINITO EN Y
        )

        # 🛠️ CONFIGURACIÓN DE STREAMLIT PARA OCULTAR LA BARRA FLOTANTE DE PLOTLY
        st.plotly_chart(
            fig, 
            use_container_width=True, 
            config={
                'displayModeBar': False,  # Oculta la barra superior con íconos de cámara, zoom, pan, etc.
                'scrollZoom': False       # Desactiva por completo el zoom con la rueda del mouse
            }
        )

st.divider()
if st.button("Recargar Dashboard"):
    st.rerun()
