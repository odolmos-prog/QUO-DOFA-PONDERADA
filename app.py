import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import io
from PIL import Image

# Configuración de página
st.set_page_config(page_title="QUO DOFA PONDERADA", layout="wide")

# --- CABECERA ---
try:
    image = Image.open('logo_quo.png')
    st.image(image, width=250)
except:
    st.info("Logo QUO")

st.title("QUO DOFA PONDERADA")
st.caption("Contacto: omarolmos@grupoquo.net")

# --- FUNCION DE CARGA PERSONALIZADA ---
def cargar_factores(titulo, clave):
    st.subheader(f"Carga de {titulo}")
    n = st.number_input(f"¿Cuántos factores de {titulo}?", 0, 25, 0, key=f"n_{clave}")
    datos = []
    for i in range(n):
        col_txt, col_val = st.columns([3, 1])
        texto = col_txt.text_input(f"Descripción (máx 80 car.)", 
                                   max_chars=80, 
                                   placeholder=f"Ej: {titulo} específica...",
                                   key=f"txt_{clave}_{i}")
        val = col_val.selectbox("Impacto", range(1, 11), index=4, key=f"val_{clave}_{i}")
        if texto:
            datos.append({"Descripción": texto, "Impacto": val})
    return datos

# --- INTERFAZ ---
col1, col2 = st.columns(2)
with col1:
    amenazas = cargar_factores("AMENAZAS", "am")
    oportunidades = cargar_factores("OPORTUNIDADES", "op")
with col2:
    debilidades = cargar_factores("DEBILIDADES", "de")
    fortalezas = cargar_factores("FORTALEZAS", "fo")

# --- CÁLCULOS Y GRÁFICO ---
if st.button("🚀 CONSTRUIR MAPA ESTRATÉGICO"):
    if not (amenazas or oportunidades or debilidades or fortalezas):
        st.error("Por favor, ingresa datos para generar el análisis.")
    else:
        # Lógica de cálculo
        sum_x = sum([o['Impacto'] for o in oportunidades]) - sum([a['Impacto'] for a in amenazas])
        total_x = len(oportunidades) + len(amenazas)
        sum_y = sum([f['Impacto'] for f in fortalezas]) - sum([d['Impacto'] for d in debilidades])
        total_y = len(fortalezas) + len(debilidades)
        
        coord_x = round(sum_x / total_x, 2) if total_x > 0 else 0
        coord_y = round(sum_y / total_y, 2) if total_y > 0 else 0

        # Crear Gráfico
        fig, ax = plt.subplots(figsize=(10, 10))
        
        # Fondos y Etiquetas de Cuadrantes (Marcas de agua)
        # Verde: Crecimiento
        ax.fill_between([0, 10], 0, 10, color='#d4edda', alpha=0.5)
        ax.text(5, 5, "CRECER, ATACAR", fontsize=15, color='green', alpha=0.3, ha='center', va='center', fontweight='bold')
        
        # Amarillo (Debajo de verde): Adaptación
        ax.fill_between([0, 10], -10, 0, color='#fff3cd', alpha=0.5)
        ax.text(5, -5, "ADAPTARSE, AJUSTARSE", fontsize=15, color='#856404', alpha=0.3, ha='center', va='center', fontweight='bold')
        
        # Amarillo (Sobre rojo): Defensa
        ax.fill_between([-10, 0], 0, 10, color='#fff3cd', alpha=0.5)
        ax.text(-5, 5, "DEFENDERSE, AUTOPRESERVARSE", fontsize=12, color='#856404', alpha=0.3, ha='center', va='center', fontweight='bold')
        
        # Rojo: Supervivencia
        ax.fill_between([-10, 0], -10, 0, color='#f8d7da', alpha=0.5)
        ax.text(-5, -5, "SOBREVIVIR, PENSÁRSELO MEJOR", fontsize=12, color='red', alpha=0.3, ha='center', va='center', fontweight='bold')

        # Ejes y Nombres solicitados
        ax.set_xlim(-10, 10); ax.set_ylim(-10, 10)
        ax.axhline(0, color='black', linewidth=1.5)
        ax.axvline(0, color='black', linewidth=1.5)
        ax.set_xlabel("EJE EXTERNO A (-)   O (+)", fontsize=12, fontweight='bold')
        ax.set_ylabel("EJE INTERNO D (-)   F (+)", fontsize=12, fontweight='bold')

        # Punto de la entidad y Vector
        ax.scatter(coord_x, coord_y, s=300, color='#004a99', edgecolors='white', zorder=5)
        ax.text(coord_x + 0.3, coord_y + 0.3, f"({coord_x}, {coord_y})", fontsize=12, fontweight='bold', color='#004a99')
        ax.arrow(coord_x, coord_y, (10 - coord_x), (10 - coord_y), color='black', linestyle=':', alpha=0.4, head_width=0.3)

        st.pyplot(fig)

        # --- GENERACIÓN DE EXCEL ---
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            # Pestaña MATRIZ
            df_final = pd.concat([
                pd.DataFrame(amenazas).assign(Tipo='AMENAZA'),
                pd.DataFrame(oportunidades).assign(Tipo='OPORTUNIDAD'),
                pd.DataFrame(debilidades).assign(Tipo='DEBILIDAD'),
                pd.DataFrame(fortalezas).assign(Tipo='FORTALEZA')
            ])
            df_final.to_excel(writer, sheet_name='MATRIZ', index=False)
            
            # Pestaña MAPA (Datos de coordenadas)
            df_mapa = pd.DataFrame({'Eje': ['Externo (X)', 'Interno (Y)'], 'Valor': [coord_x, coord_y]})
            df_mapa.to_excel(writer, sheet_name='MAPA', index=False)
            
        st.download_button(
            label="📥 Descargar Reporte Excel",
            data=output.getvalue(),
            file_name="Reporte_QUO_DOFA.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )