from document_loader import DocumentLoader
from retrieval import Retriever

FILES_PATH = "data/files"
CHROMA_PATH = "data/vector_db"
OLLAMA_MODEL = "llama3:8b"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def main():
    documentLoader = DocumentLoader(FILES_PATH, CHROMA_PATH, OLLAMA_MODEL)
    docs = documentLoader.load_documents()
    chunks = documentLoader.chunk_documents(docs, CHUNK_SIZE, CHUNK_OVERLAP)
    documentLoader.add_new_chunks_to_vector_db(chunks)

    retriever = Retriever(CHROMA_PATH, OLLAMA_MODEL)
    retriever.query_rag(retriever.get_user_prompt())

if __name__ == "__main__":
    main()