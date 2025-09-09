import streamlit as st
import os
from azure.storage.blob import BlobServiceClient
import openai
from openai import RateLimitError, APIError, APIConnectionError

# --- Configuración de Streamlit ---
st.set_page_config(page_title="Mi Chatbot de Documentos", page_icon="🤖")
st.title("🤖 Chatbot de Documentos")
st.write("¡Hola! Soy un chatbot entrenado con tus documentos. Hazme una pregunta.")

# --- Configuración de Variables de Entorno y Conexión ---
try:
    connection_string = st.secrets["AZURE_STORAGE_CONNECTION_STRING"]
    container_name = st.secrets["AZURE_CONTAINER_NAME"]
    openai_api_key = st.secrets["OPENAI_API_KEY"]

    # Conectar al servicio de Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    # Inicializar cliente de OpenAI
    client = openai.OpenAI(api_key=openai_api_key)

except KeyError as e:
    st.error(f"❌ Error: La variable de entorno '{e.args[0]}' no está configurada. Revisa tus 'secrets' en Streamlit Cloud.")
    st.stop()
except Exception as e:
    st.error(f"❌ Error al conectar con un servicio: {e}")
    st.stop()

# --- Función para conectarse a OpenAI ---
def get_chatbot_response(prompt, messages):
    """
    Se conecta a la API de OpenAI para obtener respuesta.
    Envía solo los últimos mensajes para no gastar demasiados tokens.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-5-nano",  # Puedes cambiar a "gpt-4" si tienes acceso
            messages=[
                {"role": "system", "content": "Eres un asistente amigable y útil."},
                *messages[-5:]  # Solo últimos 5 mensajes
            ]
        )
        return response.choices[0].message.content

    except RateLimitError:
        return "⚠️ Has alcanzado el límite de uso de la API de OpenAI. Intenta más tarde o revisa tu plan."
    except APIConnectionError:
        return "⚠️ No se pudo conectar con los servidores de OpenAI. Verifica tu conexión a internet."
    except APIError as e:
        return f"⚠️ Error en la API de OpenAI: {str(e)}"
    except Exception as e:
        return f"⚠️ Ocurrió un error inesperado: {str(e)}"

# --- Historial de Chat ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "¡Hola! ¿Cómo puedo ayudarte con tus documentos?"}
    ]

# Mostrar historial de mensajes
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Manejar entrada del usuario
if prompt := st.chat_input("Escribe tu pregunta sobre los documentos..."):
    # Guardar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Obtener respuesta del chatbot
    with st.chat_message("assistant"):
        with st.spinner("Procesando tu solicitud..."):
            response = get_chatbot_response(prompt, st.session_state.messages)
            st.markdown(response)

    # Guardar respuesta del asistente
    st.session_state.messages.append({"role": "assistant", "content": response})
