import streamlit as st
from groq import Groq
import json
import os

# 🔑 TU API KEY (pon la tuya real)
client = Groq(api_key="gsk_TU_API_KEY")

# 📂 Archivo de memoria
ARCHIVO_MEMORIA = "memoria.json"

# 🧠 Cargar memoria
if os.path.exists(ARCHIVO_MEMORIA):
    with open(ARCHIVO_MEMORIA, "r", encoding="utf-8") as f:
        historial = json.load(f)
else:
    historial = [
        {
            "role": "system",
            "content": "Eres Cortana, un asistente moderno, amigable y claro. Responde SIEMPRE usando 1 o 2 emojis apropiados 😊✨ sin exagerar."
        }
    ]

# Guardar en sesión
if "historial" not in st.session_state:
    st.session_state.historial = historial

# 🎨 Interfaz
st.set_page_config(page_title="Cortana IA", page_icon="🤖")
st.title("🤖 Cortana IA")

# Mostrar historial
for msg in st.session_state.historial:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").write(msg["content"])

# Entrada
mensaje = st.chat_input("Escribe algo...")

if mensaje:
    # Guardar mensaje usuario
    st.session_state.historial.append({"role": "user", "content": mensaje})

    try:
        respuesta = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.historial
        )

        texto = respuesta.choices[0].message.content

        # Guardar respuesta
        st.session_state.historial.append({"role": "assistant", "content": texto})

    except Exception as e:
        texto = "ERROR: " + str(e)

    # Guardar en archivo
    with open(ARCHIVO_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(st.session_state.historial, f, indent=4, ensure_ascii=False)

    # Mostrar respuesta
    st.chat_message("assistant").write(texto)
