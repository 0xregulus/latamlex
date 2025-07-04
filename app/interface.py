import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import streamlit as st
from app.qa_chain import ask_question
import time

st.set_page_config(page_title="LatamLex - Asistente Regulatorio Fintech & Cripto en LATAM", layout="wide")

st.title("📄 LatamLex - Asistente Regulatorio Fintech & Cripto en LATAM")
st.markdown("Haz una pregunta sobre regulación financiera en Argentina, Brasil, México o Chile.")

# Inputs
query = st.text_input("🔎 Tu pregunta:", placeholder="¿Qué dice el BCRA sobre las stablecoins?")
country = st.selectbox("🌎 País", ["argentina", "brasil", "mexico", "chile"])

if st.button("Preguntar") and query:
    with st.spinner("Buscando en la normativa..."):
        start = time.time()
        answer = ask_question(query, country)
        duration = time.time() - start
    st.markdown("### 🧠 Respuesta")
    st.markdown(answer)
    st.markdown(f"⏱️ Tiempo de respuesta: {duration:.2f} segundos")