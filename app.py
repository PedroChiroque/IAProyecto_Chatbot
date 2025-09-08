import streamlit as st
import os
from azure.storage.blob import BlobServiceClient
import io
import time # Para simular una respuesta

# --- Configuración de Streamlit y del Chatbot ---
st.set_page_config(page_title="Mi Chatbot de Documentos", page_icon="🤖")

st.title("🤖 Chatbot de Documentos")
st.write("¡Hola! Soy un chatbot entrenado con tus documentos. Hazme una pregunta.")
# 

# --- Configuración de Variables de Entorno y Conexión a Azure ---
# En Streamlit Cloud, las variables de entorno se configuran como 'secrets'.
# Aquí accedemos a ellas a través de st.secrets.
# NO subas el archivo .env a GitHub.
try:
    connection_string = st.secrets["AZURE_STORAGE_CONNECTION_STRING"]
    container_name = st.secrets["AZURE_CONTAINER_NAME"]

    # Conectar al servicio de Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    
    # Aquí puedes listar los archivos si quieres
    blob_list = container_client.list_blobs()
    #st.sidebar.title("Documentos Cargados:")
    #for blob in blob_list:
    #    st.sidebar.text(blob.name)

except KeyError:
    st.error("Error: Las variables de entorno de Azure no están configuradas. Por favor, revisa tus 'secrets' en Streamlit Cloud.")
    st.stop()
except Exception as e:
    st.error(f"Error al conectar con Azure Blob Storage: {e}")
    st.stop()

# --- Lógica del Chatbot ---
def get_chatbot_response(prompt, documents):
    """
    Esta función simula la lógica de tu chatbot.
    Reemplaza esto con tu código real de chatbot.
    """
    # Aquí es donde iría tu lógica de conexión con los modelos de IA
    # y la búsqueda de conocimiento en los documentos.
    # Por ejemplo, con LangChain, OpenAI, etc.

    # Simulación de carga y procesamiento
    time.sleep(2) 

    # Simulación de respuesta
    response = f"Gracias por tu pregunta: **{prompt}**. Actualmente estoy procesando la información de tus documentos para darte una respuesta completa. ¡Vuelve pronto!"
    return response

# --- Historial de Chat y UI de Streamlit ---
if "messages" not in st.session_state:
    st.session_state.messages = []

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
            # Llama a tu función real aquí
            response = get_chatbot_response(prompt, None) 
            st.markdown(response)

    # Agregar la respuesta del asistente al historial
    st.session_state.messages.append({"role": "assistant", "content": response})
