import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Dashboard Pro", layout="wide")

st.title("📊 Análisis de Mercado Standoff 2")
st.write(f"📅 **Fecha de hoy:** {datetime.now().strftime('%A, %d de %B de %Y')}")

if not pd.io.common.file_exists("historial_precios.csv"):
    st.warning("El bot aún no ha guardado datos. Espera unos minutos.")
    st.stop()

# Cargar y preparar datos
df = pd.read_csv("historial_precios.csv", names=["Fecha", "Skin", "Precio"])
df["Fecha"] = pd.to_datetime(df["Fecha"])

# Selectores
col1, col2 = st.columns(2)
with col1:
    skin_seleccionada = st.selectbox("Selecciona skin:", df["Skin"].unique())
with col2:
    rango = st.radio("Rango de tiempo:", ["1 Semana", "1 Mes", "3 Meses"], horizontal=True)

# Filtros
df_skin = df[df["Skin"] == skin_seleccionada].copy()
if rango == "1 Semana":
    fecha_limite = datetime.now() - pd.Timedelta(days=7)
elif rango == "1 Mes":
    fecha_limite = datetime.now() - pd.Timedelta(days=30)
else:
    fecha_limite = datetime.now() - pd.Timedelta(days=90)

df_filtrado = df_skin[df_skin["Fecha"] >= fecha_limite]

st.subheader(f"Tendencia: {skin_seleccionada}")

if not df_filtrado.empty:
    # Lógica de auto-escalado para evitar gráficas "infinitas" o planas
    min_precio = df_filtrado['Precio'].min()
    max_precio = df_filtrado['Precio'].max()
    margen = (max_precio - min_precio) * 0.1 if (max_precio - min_precio) > 0 else max_precio * 0.1
    y_min = max(0, min_precio - margen)
    y_max = max_precio + margen

    # Gráfica
    fig = px.line(df_filtrado, x='Fecha', y='Precio', markers=True)
    fig.update_layout(
        xaxis_title="Fecha",
        yaxis_title="Oro",
        hovermode="x unified",
        yaxis=dict(range=[y_min, y_max])
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Métrica de precio actual
    st.metric(label="Precio Actual", value=f"{df_filtrado.iloc[-1]['Precio']} Oro")
else:
    st.info("No hay datos suficientes para este periodo.")

if st.button("Recargar Página"):
    st.rerun()
