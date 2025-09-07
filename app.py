import gradio as gr
from azure.storage.blob import BlobServiceClient
import os

# Configura las variables de entorno para Azure
# Se recomienda usar secretos de Hugging Face
AZURE_STORAGE_CONNECTION_STRING = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
CONTAINER_NAME = os.environ["CONTAINER_NAME"]

# Conexión a Azure Blob Storage
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(CONTAINER_NAME)

# Lógica del chatbot
def chatbot_response(user_input):
    # Aquí iría tu lógica para procesar el input del usuario
    # y buscar la respuesta en los documentos del blob.
    # Por ejemplo, puedes descargar el archivo, procesarlo con un modelo, etc.

    # Ejemplo de cómo obtener un blob y leer su contenido
    blob_client = container_client.get_blob_client("knowledge_base.txt")
    blob_data = blob_client.download_blob().readall()
    knowledge_base = blob_data.decode("utf-8")

    # Lógica de búsqueda de respuesta (RAG, etc.)
    response = f"Respuesta basada en la base de conocimiento: {knowledge_base[:100]}..." # Ejemplo
    return response

# Interfaz de Gradio
iface = gr.Interface(
    fn=chatbot_response,
    inputs="text",
    outputs="text",
    title="Mi Chatbot de Azure",
    description="Pregúntame cualquier cosa sobre mis documentos de conocimiento."
)

iface.launch()
