<h1 align="center">ollama-rag-tech-interview<h1>

## Como rodar?

- 1 - Tenha o modelo llama3:8b rodando na API local do ollama na porta 11434.
Portanto, execute:

```
ollama pull llama3:8b
```

```
ollama serve
```

- 2 - Navegue até a pasta to projeto e instale as dependências do Python

```
pip install -r requirements.txt
```

- 3 - Agora, basta executar o sistema com a query desejada via CLI:

```
python3 main.py user_prompt="Considerando que sou gestor qual será o meu PLR na Contoso?"
```

## Sobre o sistema

O sistema foi feito com base em duas partes principais:

- O processamento dos arquivos e inserção dos embedings no banco de dados vetorial
pela classe `DocumentLoader`

- A parte de retrieval e contexto do sistema RAG pela classe `Retrieval`

Como banco de dados vetorial utilizei o Chroma.

### DocumentLoader

Carrega os documentos no diretório `data/files`, gera os chunks desses arquivos,
gera os ids desses chunks e compara com os ids dos chunks que estão no banco de
dados vetorial para assim saber quais chunks precisam ser inseridos.

### Retrieval

Pega a query/prompt do usuário que foi passada via CLI e faz uma busca por similaridade
de vetores no banco de dados vetorial. Com base nisso busca os chunks do banco
com mais similaridade. Passa esses chunks como contexto, juntamente as instruções
e a pergunta para o LLM, nesse caso, um modelo do Ollama predefinido que retorna
uma resposta que é exibida ao usuário juntamente às fontes que foram passadas como
contexto.

## Próximos passos

Idealmente, a estrutura atual do RAG poderia ser evoluida para um contexto multi
agentes em que estes atores realizariam tarefas isoladas como: 

- ver se a pergunta é pertinente ao contexto do chatbot
- gerar queries/prompts auxiliares para o LLM com base na query do user
- validar a resposta do LLM com base nas fontes para evitar alucinações

Desde já agradeço 😃.