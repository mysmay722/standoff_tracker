import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from config import MAPA_IMAGENES

st.set_page_config(page_title="Dashboard Pro", layout="wide")

# Inicializar el estado de la aplicación
if 'skin_seleccionada' not in st.session_state:
    st.session_state.skin_seleccionada = None

# Función para cargar datos
@st.cache_data
def cargar_datos():
    if not pd.io.common.file_exists("historial_precios.csv"):
        return None
    df = pd.read_csv("historial_precios.csv", names=["Fecha", "Skin", "Precio"])
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    return df

df = cargar_datos()

if df is None:
    st.warning("El bot aún no ha guardado datos. Espera unos minutos.")
    st.stop()

# --- LÓGICA DE NAVEGACIÓN ---
if st.session_state.skin_seleccionada is None:
    # PANTALLA DE GALERÍA
    st.title("🔫 Galería de Mercado Standoff 2")
    st.write("Selecciona una skin para ver su análisis detallado:")
    
    lista_skins = df["Skin"].unique()
    cols = st.columns(3)
    
    for i, skin in enumerate(lista_skins):
        col = cols[i % 3]
        with col:
            # Buscamos imagen en config.py, si no, una por defecto
            ruta_img = MAPA_IMAGENES.get(skin, "assets/default.png")
            st.image(ruta_img, use_container_width=True)
            if st.button(f"Ver {skin}", key=skin):
                st.session_state.skin_seleccionada = skin
                st.rerun()

else:
    # PANTALLA DE DETALLE (Gráfica + Estadísticas)
    skin = st.session_state.skin_seleccionada
    
    if st.button("⬅️ Volver a la galería"):
        st.session_state.skin_seleccionada = None
        st.rerun()

    st.title(f"📊 Análisis: {skin}")
    df_skin = df[df["Skin"] == skin].copy()

    # Gráfica
    fig = px.line(df_skin, x='Fecha', y='Precio', markers=True)
    fig.update_layout(xaxis_title="Fecha", yaxis_title="Oro", hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # Estadísticas
    st.subheader("📈 Estadísticas Históricas")
    
    def calcular_estadisticas(df_data, dias):
        fecha_limite = datetime.now() - pd.Timedelta(days=dias)
        df_periodo = df_data[df_data["Fecha"] >= fecha_limite]
        if df_periodo.empty: return None
        return df_periodo['Precio'].min(), df_periodo['Precio'].max(), ((df_periodo.iloc[-1]['Precio'] - df_periodo.iloc[0]['Precio']) / df_periodo.iloc[0]['Precio']) * 100

    c1, c2, c3 = st.columns(3)
    periodos = [("1 Semana", 7, c1), ("3 Meses", 90, c2), ("6 Meses", 180, c3)]

    for nombre, dias, col in periodos:
        res = calcular_estadisticas(df_skin, dias)
        with col:
            st.write(f"**{nombre}**")
            if res:
                mn, mx, var = res
                st.metric("Mínimo", f"{mn} G")
                st.metric("Máximo", f"{mx} G")
                st.metric("Variación", f"{var:.2f}%", delta=f"{var:.2f}%")
            else:
                st.info("Sin datos.")
