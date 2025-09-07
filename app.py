import os
from knowledge_base import AzureKnowledgeBase

# Cargar variables de entorno (para desarrollo local)
from dotenv import load_dotenv
load_dotenv()

# Inicializar la base de conocimiento de Azure
try:
    kb = AzureKnowledgeBase()
except ValueError as e:
    print(f"Error de configuración: {e}")
    exit()

def get_chatbot_response(user_input: str):
    """
    Función principal del chatbot para procesar una solicitud del usuario.
    """
    print(f"Procesando la pregunta: '{user_input}'")

    # Paso 1: Buscar documentos relevantes en Azure AI Search
    search_results = kb.search_documents(user_input)
    
    if not search_results:
        return "Lo siento, no pude encontrar información relevante para tu pregunta."

    # Usamos el primer resultado como ejemplo (puedes procesar varios)
    first_result = search_results[0]
    document_id = first_result.get('metadata_storage_name', '') # Asume que el ID está en este campo
    
    # Paso 2: Obtener el contenido del documento del Blob Storage
    document_content = kb.get_document_content(document_id)
    
    if not document_content:
        return "No pude recuperar el contenido del documento relevante."

    # Paso 3: Combinar el input del usuario y el contenido del documento
    # Esto es donde aplicarías tu lógica de modelo de lenguaje grande (LLM)
    # Ejemplo simple (puedes usar OpenAI, Llama, etc. aquí)
    print(f"Contenido relevante encontrado: {document_content[:200]}...")
    
    # Aquí iría la llamada a tu modelo de IA (ejemplo con un placeholder)
    final_response = (f"Basado en la información encontrada en tus documentos ('{document_content[:100]}...'), "
                      f"mi respuesta es: [Respuesta generada por el LLM].")
    
    return final_response

# Ejemplo de uso
if __name__ == "__main__":
    while True:
        user_question = input("Tú: ")
        if user_question.lower() in ["exit", "salir"]:
            break
        
        response = get_chatbot_response(user_question)
        print(f"Chatbot: {response}\n")
