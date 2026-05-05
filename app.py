import streamlit as st
import pandas as pd

# Configuración de página para que se vea bien en celulares
st.set_page_config(page_title="Calculadora Inteligente", layout="centered")

# Estilo personalizado para mejorar la visualización móvil
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 1. CARGA DE DATOS (Tu lista de 500 marcas)
@st.cache_data
def cargar_datos():
    try:
        # Probamos leer con coma y si falla, con punto y coma (común en Excel español)
        try:
            df = pd.read_csv('marcas.csv', sep=',')
            if len(df.columns) < 2: raise Exception()
        except:
            df = pd.read_csv('marcas.csv', sep=';')
        
        # Limpiamos espacios en blanco en los nombres de las columnas
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        # Lista de respaldo en caso de que el archivo no cargue
        return pd.DataFrame({'Marca': ['Toyota', 'Nissan'], 'Origen': ['Japonés', 'Japonés']})

df_marcas = cargar_datos()

st.title("🚗 Evaluador Automático")
st.write("Selecciona la marca y los datos del vehículo.")

# --- INTERFAZ DE USUARIO ---
# Buscador de Marca con autocompletado
lista_marcas = sorted(df_marcas['Marca'].unique().tolist())
marca_seleccionada = st.selectbox("Busca o selecciona la Marca", [""] + lista_marcas)

# Lógica de Autocompletado de Origen
origen_detectado = ""
if marca_seleccionada != "":
    # Buscamos el origen en el DataFrame
    origen_detectado = df_marcas[df_marcas['Marca'] == marca_seleccionada]['Origen'].values[0]
    st.success(f"Origen detectado: **{origen_detectado}**")
else:
    # Si no hay marca seleccionada, permite elegir manualmente
    origen_detectado = st.selectbox("O selecciona Origen manualmente", ["Americano", "Chino/Indio", "Coreano", "Europeo", "Japonés", "Otro"])

# Entrada de Año de fabricación
anio = st.number_input("Año de fabricación", min_value=2000, max_value=2026, value=2025)

# --- LÓGICA DE REGLAS DE NEGOCIO ---
if st.button("Generar Estrategia"):
    recomendacion = ""
    
    # Regla 3: Si el año es 2026 (Máxima prioridad)
    if anio == 2026:
        recomendacion = "Ofrece 3 cuotas GRATIS (ver T&C)"
    
    # Regla 2: Si es Chino/Indio o Europeo y menor a 2026
    elif origen_detectado in ["Chino/Indio", "Europeo"] and anio < 2026:
        recomendacion = "Ofrece 3 cuotas GRATIS (ver T&C)"
    
    # Regla 1: Cualquier otro origen menor a 2026
    else:
        recomendacion = "Ofrece 2 cuotas GRATIS (ver T&C)"
    
    # Visualización del resultado
    st.divider()
    st.subheader("Resultado de la Estrategia:")
    st.info(f"**{recomendacion}**")
    st.markdown("**Adicional:** Hasta 20% de descuento")
    st.warning("⚠️ Nota: El descuento afecta tu comisión")
