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
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. FUNCIÓN PARA CARGAR LOS DATOS
def cargar_datos():
    try:
        df = pd.read_csv('marcas.csv', sep=',', encoding='utf-8')
        df.columns = df.columns.str.strip()
        if len(df.columns) >= 2:
            df.columns = ['Marca', 'Origen'] + list(df.columns[2:])
        return df
    except Exception:
        return pd.DataFrame({'Marca': ['Toyota', 'Nissan'], 'Origen': ['Japonés', 'Japonés']})

df_marcas = cargar_datos()

# 3. INTERFAZ DE USUARIO
st.title("🚗 Evaluador Automático")
st.write("Complete los datos para calcular la estrategia.")

lista_marcas = sorted(df_marcas['Marca'].dropna().unique().tolist())
marca_seleccionada = st.selectbox("Busca o selecciona la Marca", [""] + lista_marcas)

origen_detectado = ""
if marca_seleccionada != "":
    origen_detectado = df_marcas[df_marcas['Marca'] == marca_seleccionada]['Origen'].values[0]
    st.success(f"Origen detectado: **{origen_detectado}**")
else:
    origen_detectado = st.selectbox("O selecciona Origen manualmente", ["Americano", "Chino / Indio", "Coreano", "Europeo", "Japonés", "Otro"])

anio = st.number_input("Año de fabricación", min_value=2000, max_value=2026, value=2025)

st.divider()
col1, col2 = st.columns(2)
with col1:
    prima_pacifico = st.number_input("Prima Anual Pacífico ($)", min_value=0.0, step=1.0, format="%.0f")
with col2:
    prima_competencia = st.number_input("Prima Anual Competencia ($)", min_value=0.0, step=1.0, format="%.0f")

# 4. LÓGICA DE NEGOCIO
if st.button("Generar Estrategia"):
    # Cálculos de diferencia y posible descuento
    diferencia_monto = prima_pacifico - prima_competencia
    
    if prima_pacifico > 0:
        porcentaje_calculado = (diferencia_monto / prima_pacifico) * 100
        pct_final = math.ceil(porcentaje_calculado)
    else:
        pct_final = 0

    # Topes de descuento adicional (0% a 20%)
    if pct_final > 20: pct_final = 20
    if pct_final < 0: pct_final = 0

    # Lógica de Cuotas Gratis
    num_cuotas = 0
    origen_clean = str(origen_detectado).strip()
    
    if anio == 2026:
        num_cuotas = 2
    elif origen_clean in ["Chino / Indio", "Europeo"] and anio < 2026:
        num_cuotas = 2
    else:
        num_cuotas = 1
    
    # Cálculo para el texto de la franja azul: ((Prima/12) * num_cuotas) / Prima Anual
    if prima_pacifico > 0:
        calculo_tyc = ((prima_pacifico / 12) * num_cuotas) / prima_pacifico * 100
    else:
        calculo_tyc = 0.0

    # MOSTRAR RESULTADOS
    st.divider()
    st.subheader("Estrategia Inicial:")
    
    # 1. Cuotas a ofrecer (Franja azul con el texto solicitado en una nueva línea)
    
    st.info(
        f"📅 **Ofrece {num_cuotas} cuota(s) GRATIS (ver T&C)**\n"
        f"Esto representa {calculo_tyc:.1f}% de la prima"
    )

    
    # 2. Diferencia detectada debajo de la franja azul
    st.metric(label="Diferencia detectada", value=f"${diferencia_monto:,.2f}")
    
    # 3. Recomendación final
    st.write("### Recomendación final:")
    st.write(f"**Posible descuento adicional: {pct_final}%**")
    
    st.warning("⚠️ Nota: El descuento afecta directamente la comisión del asesor.")
