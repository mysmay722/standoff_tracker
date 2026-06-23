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

# Filtro general de skin
df_skin = df[df["Skin"] == skin_seleccionada].copy()

# --- GRÁFICA PRINCIPAL ---
st.subheader(f"Tendencia: {skin_seleccionada}")
fig = px.line(df_skin, x='Fecha', y='Precio', markers=True)
fig.update_layout(xaxis_title="Fecha", yaxis_title="Oro", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

# --- SECCIÓN DE ESTADÍSTICAS (Métricas) ---
st.divider()
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
    
    # Cálculo de porcentaje: ((Final - Inicio) / Inicio) * 100
    variacion = ((precio_actual - precio_inicio) / precio_inicio) * 100
    
    return min_val, max_val, variacion

# Crear columnas para las 3 métricas
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
            st.info("Sin datos aún.")

if st.button("Recargar Página"):
    st.rerun()
