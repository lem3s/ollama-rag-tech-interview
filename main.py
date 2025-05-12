from document_loader import DocumentLoader
from retrieval import Retriever

FILES_PATH = "data/files"
CHROMA_PATH = "data/vector_db"
OLLAMA_MODEL = "llama3:8b"

def main():
    documentLoader = DocumentLoader(FILES_PATH, CHROMA_PATH, OLLAMA_MODEL)
    docs = documentLoader.load_documents()
    chunks = documentLoader.split_documents(docs)
    documentLoader.add_new_chunks_to_chroma(chunks)

    retriever = Retriever(CHROMA_PATH, OLLAMA_MODEL)
    retriever.query_rag(retriever.get_user_query())

if __name__ == "__main__":
    main()