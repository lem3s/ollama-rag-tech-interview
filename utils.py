from langchain_ollama import OllamaEmbeddings

def get_embedding_function(ollama_model: str):
    return OllamaEmbeddings(model=ollama_model)