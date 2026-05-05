import streamlit as st
import pandas as pd

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
    origen_detectado = st.selectbox("O selecciona Origen manualmente", ["Americano", "Chino/Indio", "Coreano", "Europeo", "Japonés", "Otro"])

# Entrada de Año
anio = st.number_input("Año de fabricación", min_value=2000, max_value=2026, value=2025)

# 4. LÓGICA DE NEGOCIO
if st.button("Generar Estrategia"):
    resultado = ""
    
    # REGLA 3: Año 2026 (Prioridad máxima)
    if anio == 2026:
        resultado = "Ofrece 3 cuotas GRATIS (ver T&C)"
    
    # REGLA 2: ChinoIndio o Europeo menor a 2026
    elif str(origen_detectado).strip() in ["Chino/Indio", "Europeo"] and anio < 2026:
        resultado = "Ofrece 3 cuotas GRATIS (ver T&C)"
    
    # REGLA 1: Otros orígenes menores a 2026
    else:
        resultado = "Ofrece 2 cuotas GRATIS (ver T&C)"
    
    # Mostrar el resultado final
    st.divider()
    st.subheader("Estrategia Recomendada:")
    st.info(f"**{resultado}**")
    st.markdown("🎯 **Bono adicional:** Hasta 20% de descuento.")
    st.warning("⚠️ Nota: El descuento afecta la comisión del asesor.")
