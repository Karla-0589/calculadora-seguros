import streamlit as st
import pandas as pd

# Configuración móvil
st.set_page_config(page_title="Calculadora Inteligente", layout="centered")

# 1. CARGA DE DATOS
@st.cache_data
def cargar_datos():
    try:
        # Probamos leer con coma, y si falla, con punto y coma
        try:
            df = pd.read_csv("marcas.csv", sep=",")
            if len(df.columns) < 2:
                raise Exception()
        except Exception:
            df = pd.read_csv("marcas.csv", sep=";")

        # Limpiamos espacios en blanco en los nombres de columnas
        df.columns = df.columns.str.strip()
        return df

    except Exception as e:
        return pd.DataFrame({
            "Marca": ["Error al leer archivo"],
            "Origen": ["Revisar formato"]
        })

df_marcas = cargar_datos()

st.title("🚗 Evaluador Automático")

# --- INTERFAZ ---
lista_marcas = df_marcas["Marca"].unique().tolist()
marca_seleccionada = st.selectbox(
    "Busca o selecciona la Marca",
    [""] + sorted(lista_marcas)
)

# Autocompletado de Origen
origen_detectado = ""
if marca_seleccionada != "":
    origen_detectado = df_marcas[
        df_marcas["Marca"] == marca_seleccionada
    ]["Origen"].values[0]
    st.success(f"Origen detectado: **{origen_detectado}**")
else:
    origen_detectado = st.selectbox(
        "O selecciona Origen manualmente",
        ["Americano", "Chino/Indio", "Coreano", "Europeo", "Japonés", "Otro"]
    )

anio = st.number_input(
    "Año de fabricación",
    min_value=2000,
    max_value=2026,
    value=2025
)

# --- LÓGICA DE REGLAS ---
if st.button("Generar Estrategia"):
    recomendacion = ""

    # Regla 3: Año 2026
    if anio == 2026:
        recomendacion = "Ofrece 3 cuotas GRATIS (ver T&C)"

    # Regla 2: Chinos/Indio o Europeo menor a 2026
    elif origen_detectado in ["Chino/Indio", "Europeo"] and anio < 2026:
        recomendacion = "Ofrece 3 cuotas GRATIS (ver T&C)"

    # Regla 1: El resto
    else:
        recomendacion = "Ofrece 2 cuotas GRATIS (ver T&C)"

    st.divider()
    st.subheader("Resultado:")
    st.info(recomendacion)
    st.warning("⚠️ Nota: El descuento afecta tu comisión (Hasta 20%)")
