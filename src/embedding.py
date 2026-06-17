"""
Este modulo contiene la clase 'Embedder', la cual se encargará de la creación 
de los vectores de embedding a partir de un modelo pre-entrenado. Luego, 
devuelve los vectores de embedding
"""


from langchain_chroma import Chroma
from langchain_core import Document
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class Embedder(object):
    
    def __init__(self, model_name: str, database_path: str, chunk_size: int = 500, chunk_overlap: int = 100):
        
        assert model_name is not None, "Model name cannot be None"
        assert database_path is not None, "Database path cannot be None"

        try:
            __loaded_model = HuggingFaceEmbeddings(model_name = model_name)
        except Exception as e:
            print(f"Error loading model: {e}")
            raise e
        
        self.model = __loaded_model
        self.database_path = database_path
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size = chunk_size, chunk_overlap = chunk_overlap)
        self.vector_store = None


    def read_pdf_documents(self, documents_path: str) -> list[Document]:
        assert documents_path is not None, "Documents path cannot be None"

        loader = PyPDFDirectoryLoader(documents_path)    
        documents = loader.load()

        return self.__create_chunks(documents)


    def __create_chunks(self, documents: list[Document]) -> list[Document]:
        return self.text_splitter.split_documents(documents)
    

    def embed_and_store(self, chunks: list[Document]):
        assert chunks is not None, "Chunks cannot be None"

        if self.vector_store is None:
            self.vector_store = Chroma.from_documents(documents = chunks, embedding = self.model, persist_directory = self.database_path)
        
        self.vector_store.add_documents(documents = chunks)