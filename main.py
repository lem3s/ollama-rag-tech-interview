from document_loader import DocumentLoader
from retrieval import Retrieval

FILES_PATH = "data/files"
CHROMA_PATH = "data/vector_db"
OLLAMA_MODEL = "llama3:8b"

def main():
    documentLoader = DocumentLoader(FILES_PATH, CHROMA_PATH, OLLAMA_MODEL)
    docs = documentLoader.load_documents()
    chunks = documentLoader.split_documents(docs)
    documentLoader.add_new_chunks_to_chroma(chunks)

    retrieval_tool = Retrieval(CHROMA_PATH, OLLAMA_MODEL)
    retrieval_tool.query_rag(retrieval_tool.get_user_query())

if __name__ == "__main__":
    main()