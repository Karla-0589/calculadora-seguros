import streamlit as st
import pandas as pd
import math

# 1. CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title="Calculadora Inteligente", layout="centered")

# Estilo para mejorar la apariencia en móviles
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #007bff;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIÓN PARA CARGAR LOS DATOS (Lectura de marcas.csv)
def cargar_datos():
    try:
        # Forzamos la lectura con punto y coma (;) detectado en tu archivo
        df = pd.read_csv('marcas.csv', sep=',')
        
        # Limpiamos espacios y estandarizamos nombres de columnas
        df.columns = df.columns.str.strip()
        
        # Si las columnas no se llaman exactamente Marca/Origen, las renombramos por posición
        if len(df.columns) >= 2:
            df.columns = ['Marca', 'Origen'] + list(df.columns[2:])
            
        return df
    except Exception as e:
        # Si falla, muestra el error en pantalla para diagnosticar
        st.error(f"Aviso técnico: No se pudo leer el archivo completo. Error: {e}")
        return pd.DataFrame({'Marca': ['Toyota', 'Nissan'], 'Origen': ['Japonés', 'Japonés']})

# Ejecutamos la carga
df_marcas = cargar_datos()

# 3. INTERFAZ DE USUARIO
st.title("🚗 Evaluador Automático")
st.write("Selecciona la marca para ver la estrategia comercial.")

# Buscador de Marcas
lista_marcas = sorted(df_marcas['Marca'].dropna().unique().tolist())
marca_seleccionada = st.selectbox("Busca o selecciona la Marca", [""] + lista_marcas)

# Autocompletado de Origen
origen_detectado = ""
if marca_seleccionada != "":
    # Extraemos el origen correspondiente
    origen_detectado = df_marcas[df_marcas['Marca'] == marca_seleccionada]['Origen'].values[0]
    st.success(f"Origen detectado: **{origen_detectado}**")
else:
    origen_detectado = st.selectbox("O selecciona Origen manualmente", ["Americano", "Chino / Indio", "Coreano", "Europeo", "Japonés", "Otro"])

# Entrada de Año
anio = st.number_input("Año de fabricación", min_value=2000, max_value=2026, value=2025)

# --- NUEVAS VARIABLES (MARCADAS EN VERDE) ---
st.divider()
col1, col2 = st.columns(2)
with col1:
    prima_competencia = st.number_input("Prima Anual Competencia ($)", min_value=0.0, step=1.0)
with col2:
    prima_pacifico = st.number_input("Prima Anual Pacífico ($)", min_value=0.0, step=1.0)

# 4. LÓGICA DE NEGOCIO Y REGLAS ADICIONALES
if st.button("Generar Estrategia"):
    # Cálculo de diferencia
    diferencia = prima_competencia - prima_pacifico
    
    # Cálculo de Descuento (Regla de la imagen: Diferencia - 3)
    # Redondeado hacia arriba (math.ceil)
    pct_descuento = math.ceil(diferencia - 3)
    
    # Aplicar Topes (Máximo 20% según tus notas anteriores)
    if pct_descuento > 20: pct_descuento = 20
    if pct_descuento < 0: pct_descuento = 0

    # Lógica de Cuotas (Reglas originales)
    resultado_cuotas = ""
    if anio == 2026:
        resultado_cuotas = "Ofrece 2 cuotas GRATIS (ver T&C)"
    elif str(origen_detectado).strip() in ["Chino / Indio", "Europeo"] and anio < 2026:
        resultado_cuotas = "Ofrece 2 cuotas GRATIS (ver T&C)"
    else:
        resultado_cuotas = "Ofrece 1 cuotas GRATIS (ver T&C)"
    
    # RESULTADOS FINALES
    st.divider()
    st.subheader("Estrategia Recomendada:")
    
    # Mostrar diferencia y descuento
    st.metric(label="Diferencia de Primas", value=f"${diferencia:,.2f}")
    
    st.info(f"**{resultado_cuotas}**")
    
    st.success(f"🎯 **Descuento sugerido: {pct_descuento}%**")
    
    st.warning("⚠️ Nota: El descuento afecta la comisión del asesor.")
