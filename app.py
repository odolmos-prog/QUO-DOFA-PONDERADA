import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

# Configuración de página
st.set_page_config(page_title="QUO DOFA PONDERADA by Grupo QUO", layout="centered")

# --- CABECERA ARMONIOSA ---
# Cargamos y centramos el logo
try:
    image = Image.open('LOGO.png')
    st.image(image, width=300)
except:
    st.warning("Asegúrate de que 'LOGO.png' esté en el repositorio.")

st.title("QUO DOFA PONDERADA by Grupo QUO")
st.markdown("---")

# --- FUNCIONES DE RECOLECCIÓN ---
def entrada_datos(titulo):
    st.subheader(f"Carga de {titulo}")
    n_factores = st.number_input(f"¿Cuántos factores de {titulo} (máx 25)?", 0, 25, 0, key=titulo)
    puntos = []
    for i in range(n_factores):
        p = st.select_slider(f"{titulo} #{i+1}", options=range(1, 11), value=5, key=f"val_{titulo}_{i}")
        puntos.append(p)
    return puntos

# --- INTERFAZ ---
col1, col2 = st.columns(2)
with col1:
    pts_amenazas = entrada_datos("AMENAZAS")
    pts_oportunidades = entrada_datos("OPORTUNIDADES")
with col2:
    pts_debilidades = entrada_datos("DEBILIDADES")
    pts_fortalezas = entrada_datos("FORTALEZAS")

# --- CÁLCULOS Y GRÁFICO ---
if st.button("🚀 CONSTRUIR MAPA ESTRATÉGICO"):
    if not (pts_amenazas or pts_oportunidades or pts_debilidades or pts_fortalezas):
        st.error("Por favor, ingresa al menos un factor.")
    else:
        # Lógica de cambio de signo interna
        sum_x = sum(pts_oportunidades) - sum(pts_amenazas)
        total_x = len(pts_oportunidades) + len(pts_amenazas)
        sum_y = sum(pts_fortalezas) - sum(pts_debilidades)
        total_y = len(pts_fortalezas) + len(pts_debilidades)
        
        coord_x = sum_x / total_x if total_x > 0 else 0
        coord_y = sum_y / total_y if total_y > 0 else 0

        # Gráfico
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.fill_between([0, 10], 0, 10, color='#d4edda', alpha=0.6, label="Crecimiento")
        ax.fill_between([-10, 0], 0, 10, color='#fff3cd', alpha=0.6, label="Defensa")
        ax.fill_between([0, 10], -10, 0, color='#fff3cd', alpha=0.6, label="Adaptación")
        ax.fill_between([-10, 0], -10, 0, color='#f8d7da', alpha=0.6, label="Supervivencia")

        ax.scatter(coord_x, coord_y, s=300, color='#004a99', edgecolors='white', zorder=5)
        ax.arrow(coord_x, coord_y, (10 - coord_x), (10 - coord_y), 
                 color='black', linestyle=':', head_width=0.4, alpha=0.5)

        ax.set_xlim(-10, 10); ax.set_ylim(-10, 10)
        ax.axhline(0, color='black', linewidth=1); ax.axvline(0, color='black', linewidth=1)
        st.pyplot(fig)

# --- PIE DE PÁGINA ---
st.markdown("---")
st.caption("Contacto: omarolmos@grupoquo.net")