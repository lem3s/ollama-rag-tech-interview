import argparse
from utils import get_embedding_function
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

PROMPT_TEMPLATE = """
Considerando que você é um chatbot de Q&A com foco em RH responda em português 
brasileiro a questão que lhe é fornecida com base somente no seguinte contexto:

{context}

---

Responda a seguinte questão com base no contexto acima: {question}.

Se a questão não está relacionada as informações de RH fornecidas você deve responder
que não há informações suficientes para responder a questão. Responda em português brasileiro.
"""

class Retriever:
    def __init__(self, chroma_path: str, ollama_model: str):
        self.chroma_path = chroma_path
        self.ollama_model = ollama_model

    def get_user_query(self) -> str:
        parser = argparse.ArgumentParser()
        parser.add_argument("query_text", type=str, help="The query text.")
        args = parser.parse_args()

        return args.query_text

    def query_rag(self, query: str) -> str:
        embedding_function = get_embedding_function(self.ollama_model)
        vector_store = Chroma(
            persist_directory=self.chroma_path,
            embedding_function=embedding_function
        )

        search_results = vector_store.similarity_search(query, k=3)

        context_text = "\n\n---\n\n".join([doc.page_content for doc in search_results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query)

        model = OllamaLLM(model=self.ollama_model)
        response_text = model.invoke(prompt)

        sources = [doc.metadata.get("id", None) for doc in search_results]
        formatted_response = f"Response: {response_text}\nSources: {sources}"
        print(formatted_response)
        return response_text
