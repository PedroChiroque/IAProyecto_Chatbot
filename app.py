import streamlit as st
import os
from azure.storage.blob import BlobServiceClient
import time # Usado para la simulación
import openai # Importar la librería de OpenAI

# --- Configuración de Streamlit y del Chatbot ---
st.set_page_config(page_title="Mi Chatbot de Documentos", page_icon="🤖")

st.title("🤖 Chatbot de Documentos")
st.write("¡Hola! Soy un chatbot entrenado con tus documentos. Hazme una pregunta.")
# 

# --- Configuración de Variables de Entorno y Conexión a Azure y OpenAI ---
# En Streamlit Cloud, las variables de entorno se configuran como 'secrets'.
# Accedemos a ellas a través de st.secrets.
try:
    connection_string = st.secrets["AZURE_STORAGE_CONNECTION_STRING"]
    container_name = st.secrets["AZURE_CONTAINER_NAME"]
    openai_api_key = st.secrets["OPENAI_API_KEY"]
    
    # Conectar al servicio de Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    
    # Inicializar el cliente de OpenAI
    client = openai.OpenAI(api_key=openai_api_key)

except KeyError as e:
    st.error(f"Error: La variable de entorno '{e.args[0]}' no está configurada. Por favor, revisa tus 'secrets' en Streamlit Cloud.")
    st.stop()
except Exception as e:
    st.error(f"Error al conectar con un servicio: {e}")
    st.stop()

# --- Lógica del Chatbot (Conexión a OpenAI) ---
def get_chatbot_response(prompt, messages):
    """
    Esta función se conecta a la API de OpenAI para obtener una respuesta.
    El historial de mensajes se envía para mantener el contexto de la conversación.
    """
    
    # NOTA: Para usar el conocimiento de tus PDFs, necesitarías una
    # arquitectura de "Retrieval-Augmented Generation" (RAG). Esto
    # implica buscar la información relevante en tus documentos ANTES
    # de llamar a la API de OpenAI y luego incluir esa información en el prompt.
    # Esto requiere librerías como LangChain o LlamaIndex.
    # Este código es solo un ejemplo de conexión directa con la API.
    
    response = client.chat.completions.create(
        model="gpt-5 mini", # Puedes usar otros modelos, como "gpt-4" gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "Eres un asistente amigable y útil."},
            *messages # El asterisco expande el historial de mensajes
        ]
    )
    
    # Extraer la respuesta del asistente
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
            # Llama a la función de respuesta con el historial completo
            response = get_chatbot_response(prompt, st.session_state.messages)
            st.markdown(response)

    # Agregar la respuesta del asistente al historial
    st.session_state.messages.append({"role": "assistant", "content": response})
