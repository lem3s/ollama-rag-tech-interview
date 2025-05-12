# ollama-rag-tech-interview

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

