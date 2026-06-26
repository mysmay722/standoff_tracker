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
       # --- CREACIÓN DE LA GRÁFICA OPTIMIZADA ---
# 1. Extraemos los límites reales de tu información
fecha_min = df_skin["Fecha"].min()
fecha_max = df_skin["Fecha"].max() 

fig = px.line(
    df_skin, 
    x="Fecha", 
    y="Precio",
    markers=True
)

fig.update_traces(
    line=dict(color="#FF4B4B", width=3),
    marker=dict(size=6, color="#1f77b4"),
    hovertemplate="<b>📅 Fecha:</b> %{x|%d %b, %H:%M}<br><b>💰 Precio:</b> %{y} G<extra></extra>"
)

fig.update_layout(
    hovermode="x unified",
    showlegend=False,
    margin=dict(l=10, r=10, t=40, b=10),
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    xaxis_title="",
    yaxis_title="",
)

# 🔒 RESTRICCIÓN ESTRICTA DE EJES
fig.update_xaxes(
    showgrid=True,
    gridcolor="rgba(128, 128, 128, 0.2)",
    range=[fecha_min, fecha_max],  # Fuerza a la gráfica a abarcar SOLO donde hay datos
    minallowed=fecha_min,          # Pared invisible: Impide que se genere espacio hacia el pasado
    maxallowed=fecha_max,          # Pared invisible: Impide que aparezcan fechas del futuro
    rangeselector=dict(
        font=dict(size=12),
        buttons=list([
            dict(count=7, label="1S", step="day", stepmode="backward"),
            dict(count=1, label="1M", step="month", stepmode="backward"),
            dict(count=3, label="3M", step="month", stepmode="backward"),
            dict(count=6, label="6M", step="month", stepmode="backward"),
            dict(step="all", label="Todo")
        ]),
        bgcolor="rgba(255, 75, 75, 0.1)",
        activecolor="#FF4B4B",
    )
)

fig.update_yaxes(
    showgrid=True,
    gridcolor="rgba(128, 128, 128, 0.2)",
    # Se elimina fixedrange=True para que el eje Y se ajuste automáticamente si el usuario hace clic en los botones de tiempo
)

st.plotly_chart(
    fig, 
    use_container_width=True, 
    config={
        'displayModeBar': False, 
        'scrollZoom': False
    }
)

# --- SECCIÓN DE MÉTRICAS ---
st.subheader("📈 Estadísticas Históricas")

def calcular_estadisticas(df_data, dias):
    fecha_limite = datetime.now() - pd.Timedelta(days=dias)
    df_periodo = df_data[df_data["Fecha"] >= fecha_limite]
    
    if df_periodo.empty:
        return None
    
    min_val = df_periodo['Precio'].min()
    max_val = df_periodo['Precio'].max()
    precio_inicio = df_periodo.iloc[0]['Precio']
    precio_actual = df_periodo.iloc[-1]['Precio']
    
    # Evitar división por cero por seguridad
    if precio_inicio == 0:
        return min_val, max_val, 0.0
        
    variacion = ((precio_actual - precio_inicio) / precio_inicio) * 100
    return min_val, max_val, variacion

c1, c2, c3 = st.columns(3)
periodos = [("1 Semana", 7, c1), ("3 Meses", 90, c2), ("6 Meses", 180, c3)]

for nombre, dias, columna in periodos:
    res = calcular_estadisticas(df_skin, dias)
    with columna:
        st.write(f"**{nombre}**")
        if res:
            mn, mx, var = res
            st.metric("Mínimo", f"{mn} G")
            st.metric("Máximo", f"{mx} G")
            st.metric("Variación", f"{var:.2f}%", delta=f"{var:.2f}%")
        else:
            st.info("Sin datos suficientes en este rango.")

st.divider()
if st.button("Recargar Dashboard"):
    st.rerun()
