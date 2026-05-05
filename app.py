import streamlit as st
import pandas as pd

# Configuración móvil
st.set_page_config(page_title="Calculadora Inteligente", layout="centered")

# 1. CARGA DE DATOS (Tu lista de 500 marcas)
@st.cache_data
def cargar_datos():
# Intenta leer el archivo CSV que subiste a GitHub
try:
df = pd.read_csv('marcas.csv')
return df
except:
# Si no encuentra el archivo, crea uno de ejemplo para que no falle
return pd.DataFrame({'Marca': ['Toyota', 'Nissan'], 'Origen': ['Japonés', 'Japonés']})

df_marcas = cargar_datos()

st.title("🚗 Evaluador Automático")

# --- INTERFAZ ---
# Buscador de Marca con autocompletado
lista_marcas = df_marcas['Marca'].unique().tolist()
marca_seleccionada = st.selectbox("Busca o selecciona la Marca", [""] + lista_marcas)

# Autocompletado de Origen
if marca_seleccionada:
# Busca el origen correspondiente en el CSV
origen_detectado = df_marcas[df_marcas['Marca'] == marca_seleccionada]['Origen'].values[0]
st.success(f"Origen detectado: **{origen_detectado}**")
else:
origen_detectado = st.selectbox("O selecciona Origen manualmente", ["Americano", "Chino/Indio", "Coreano", "Europeo", "Japonés", "Otro"])

# Entrada de Año
anio = st.number_input("Año de fabricación", min_value=2000, max_value=2026, value=2025)

# --- LÓGICA DE REGLAS (Igual a tu tabla) ---
if st.button("Generar Estrategia"):
recomendacion = ""

if anio == 2026:
recomendacion = "Ofrece 3 cuotas GRATIS (ver T&C)"
elif origen_detectado in ["Chino/Indio", "Europeo"] and anio < 2026:
recomendacion = "Ofrece 3 cuotas GRATIS (ver T&C)"
else:
recomendacion = "Ofrece 2 cuotas GRATIS (ver T&C)"

st.divider()
st.metric(label="Recomendación", value=recomendacion)
st.warning("Nota: El descuento afecta tu comisión (Hasta 20%)")
