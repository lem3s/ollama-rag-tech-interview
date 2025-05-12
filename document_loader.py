from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from utils import get_embedding_function

class DocumentLoader:
    def __init__(self, folder_path: str, chroma_path: str, ollama_model: str):
        self.folder_path = folder_path
        self.chroma_path = chroma_path
        self.ollama_model = ollama_model

    def load_documents(self) -> list[Document]:
        documents = []
        for filename in os.listdir(self.folder_path):
            if filename.endswith('.md') or filename.endswith('.txt'):
                file_path = os.path.join(self.folder_path, filename)
                document_loader = UnstructuredMarkdownLoader(file_path)
                documents.extend(document_loader.load())
        return documents
    
    def chunk_documents(self, documents: list[Document], chunk_size: int, chunk_overlap: int) -> list[Document]:
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap) 
        return text_splitter.split_documents(documents)

    def add_new_chunks_to_vector_db(self, chunks: list[Document]):
        vector_db = Chroma(
            persist_directory=self.chroma_path,
            embedding_function=get_embedding_function(self.ollama_model)
        )

        chunks = self.generate_chunks_ids(chunks)
        existing_items = vector_db.get(include=[])
        existing_ids : list[str] = existing_items["ids"]

        chunks_to_add : list[Document] = []
        for chunk in chunks:
            if chunk.metadata["id"] not in existing_ids:
                chunks_to_add.append(chunk)
        
        chunks_to_add_ids : list[str] = []
        for chunk in chunks_to_add:
            chunks_to_add_ids.append(chunk.metadata["id"])
        
        if len(chunks_to_add) > 0:
            vector_db.add_documents(chunks_to_add, ids=chunks_to_add_ids)

    
    def generate_chunks_ids(self, chunks: list[Document]) -> list[Document]:
        last_file : str = ""
        chunk_id : int = 0

        for chunk in chunks:
            if last_file != chunk.metadata["source"]:
                last_file = chunk.metadata["source"]
                chunk_id = 0

            chunk.metadata["id"] = f"{chunk.metadata["source"]}:{chunk_id}"
            chunk_id += 1

        return chunks