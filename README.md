# Parte 1 - Questão 2: inglês para francês

## Como executar

Use Python 3.11 ou 3.12. Dentro desta pasta, crie um ambiente e instale as dependências:

```bash
python -m venv .venv
```

Ative o ambiente:

```bash
# Linux ou macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\Activate.ps1
```

```bash
python -m pip install -r requirements.txt
uvicorn main:app --port 8000
```

Abra http://127.0.0.1:8000/docs, selecione POST /translate, clique em “Try it out” e envie:

```json
{"text": "The weather is beautiful today."}
```

Também é possível enviar pelo terminal (no Windows, use curl.exe):

```bash
curl -X POST http://127.0.0.1:8000/translate -H "Content-Type: application/json" -d '{"text":"The weather is beautiful today."}'
```

Execute uma aplicação por vez na porta 8000. Textos vazios são recusados com erro 422.

O primeiro início baixa o modelo do Hugging Face e precisa de internet. Depois, os pesos ficam no cache. A execução utiliza CPU.

Textos longos são traduzidos frase por frase. Frases maiores que 350 tokens são divididas em blocos. Isso evita ultrapassar o limite de entrada do modelo, mas pode perder contexto entre blocos.

A resposta tem o formato `{"translation": "texto traduzido"}`.
