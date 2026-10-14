import streamlit as st
from dotenv import load_dotenv
from agentes.agente_1 import AgenteUno
from agentes.agente_2 import AgenteDos

# Carga la API key desde el archivo .env
load_dotenv()

st.set_page_config(page_title="Sistema Multi-Agente", layout="wide")
st.title("Interfaz Multi-Agente Interconectada")

# Instancia individual de cada agente
agente_1 = AgenteUno()
agente_2 = AgenteDos()

# Columnas en la GUI para separar los agentes
col1, col2 = st.columns(2)

with col1:
    st.header("Agente 1")
    entrada_agente_1 = st.text_area("Entrada inicial:", "Escribe aquí la consulta inicial...")
    
    if st.button("Ejecutar Agente 1"):
        with st.spinner("Procesando Agente 1..."):
            salida_1 = agente_1.responder(entrada_agente_1)
            st.session_state['salida_agente_1'] = salida_1
            st.success("Respuesta Agente 1:")
            st.write(salida_1)

with col2:
    st.header("Agente 2")
    if 'salida_agente_1' in st.session_state:
        st.info("Recibida salida previa del Agente 1.")
        
        if st.button("Enviar al Agente 2"):
            with st.spinner("Procesando Agente 2..."):
                salida_2 = agente_2.responder(st.session_state['salida_agente_1'])
                st.success("Respuesta Agente 2:")
                st.write(salida_2)
    else:
        st.caption("Ejecuta primero el Agente 1 para conectar la respuesta.")