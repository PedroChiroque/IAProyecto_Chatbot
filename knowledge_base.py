import os
from azure.storage.blob import BlobServiceClient
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

class AzureKnowledgeBase:
    """
    Clase para interactuar con los servicios de conocimiento de Azure.
    """
    def __init__(self):
        # Obtener credenciales de las variables de entorno para mayor seguridad.
        self.blob_connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.blob_container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        
        self.search_service_endpoint = os.getenv("AZURE_SEARCH_SERVICE_ENDPOINT")
        self.search_api_key = os.getenv("AZURE_SEARCH_API_KEY")
        self.search_index_name = os.getenv("AZURE_SEARCH_INDEX_NAME")
        
        # Validar que todas las variables de entorno están configuradas
        if not all([self.blob_connection_string, self.blob_container_name, 
                    self.search_service_endpoint, self.search_api_key, 
                    self.search_index_name]):
            raise ValueError("Las variables de entorno de Azure no están configuradas correctamente.")
            
        # Inicializar los clientes de Azure
        self.blob_service_client = BlobServiceClient.from_connection_string(self.blob_connection_string)
        self.search_client = SearchClient(
            endpoint=self.search_service_endpoint,
            index_name=self.search_index_name,
            credential=AzureKeyCredential(self.search_api_key)
        )
        
    def search_documents(self, query: str):
        """
        Busca documentos relevantes en el índice de Azure AI Search.
        Retorna los resultados de la búsqueda.
        """
        try:
            results = self.search_client.search(search_text=query)
            return [result for result in results]
        except Exception as e:
            print(f"Error al buscar en Azure AI Search: {e}")
            return []

    def get_document_content(self, document_id: str):
        """
        Descarga el contenido de un documento específico desde Azure Blob Storage.
        """
        try:
            container_client = self.blob_service_client.get_container_client(self.blob_container_name)
            blob_client = container_client.get_blob_client(document_id)
            blob_data = blob_client.download_blob().readall()
            return blob_data.decode("utf-8")
        except Exception as e:
            print(f"Error al descargar el documento del blob: {e}")
            return None
