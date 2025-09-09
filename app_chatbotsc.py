import streamlit as st
import os
from azure.storage.blob import BlobServiceClient
import time  # Usado para la simulación
import openai  # Importar la librería de OpenAI

# --- Configuración de Streamlit y del Chatbot ---
st.set_page_config(page_title="Mi Chatbot de Documentos", page_icon="🤖")
st.title("🤖 Chatbot de Documentos")
st.write("¡Hola! Soy un chatbot entrenado con tus documentos. Hazme una pregunta.")

# --- Configuración de Variables de Entorno y Conexión a Azure y OpenAI ---

# En Streamlit Cloud, las variables de entorno se configuran como 'secrets'.
try:
    connection_string = st.secrets["AZURE_STORAGE_CONNECTION_STRING"]
    container_name = st.secrets["AZURE_CONTAINER_NAME"]
    openai_api_key = st.secrets["OPENAI_API_KEY"]

    # Conectar al servicio de Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Configurar API de OpenAI
    openai.api_key = openai_api_key

except KeyError as e:
    st.error(f"Error: La variable de entorno '{e.args[0]}' no está configurada. Por favor, revisa tus 'secrets' en Streamlit Cloud.")
    st.stop()
except Exception as e:
    st.error(f"Error al conectar con un servicio: {e}")
    st.stop()

# --- Lógica del Chatbot (Conexión a OpenAI) ---
def get_chatbot_response(prompt, messages):
    response = openai.ChatCompletion(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente amigable y útil."},
            *messages
        ]
    )
    return response.choices[0].message.content

# --- Historial de Chat y UI de Streamlit ---
if "messages" not in st.session_state:
    # Inicializa el historial con un mensaje del asistente
    st.session_state.messages = [{"role": "assistant", "content": "¡Hola! ¿Cómo puedo ayudarte con tus documentos?"}]

# Mostrar mensajes previos
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Manejar la entrada del usuario
if prompt := st.chat_input("¿Qué deseas saber sobre los documentos?"):
    # Agregar el mensaje del usuario al historial
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Obtener respuesta del chatbot
    with st.chat_message("assistant"):
        with st.spinner("Procesando tu solicitud..."):
            try:
                response = get_chatbot_response(prompt, st.session_state.messages)
                st.markdown(response)
                # Agregar la respuesta del asistente al historial
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Ocurrió un error al obtener la respuesta: {e}")
