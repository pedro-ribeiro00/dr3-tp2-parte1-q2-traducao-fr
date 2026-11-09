# Tradução inglês-francês

DR3 - TP2. Python 3.11 ou 3.12. Execute os comandos dentro desta pasta.

## Instalação

```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Execução

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

Abra http://127.0.0.1:8000/docs para testar pelo Swagger. Pare uma aplicação antes de iniciar outra na mesma porta. O endpoint `/health` confirma que o startup terminou.

```bash
curl -X POST http://127.0.0.1:8000/translate -H "Content-Type: application/json" -d '{"text":"The weather is beautiful today."}'
```

No PowerShell, use o Swagger ou `curl.exe`. Entrada inválida retorna 422. Falhas de serviço são documentadas no código. Não há autenticação pública: executar como protótipo local.

## Testes

```bash
python -m pytest -q
```

Os testes de contrato substituem a inferência para validar HTTP sem download nem cobrança. Eles não medem qualidade do modelo. Consulte `VALIDACAO.md` na raiz da entrega para as verificações realmente executadas.

## Modelos locais

O primeiro startup baixa os pesos do Hugging Face e exige internet e espaço em disco. Os próximos usam o cache local. A inferência usa CPU; cada worker duplica a memória do modelo. Comece com um worker. Transformers fica na série 4.x por compatibilidade. Sem chave OpenAI.

Para repetir as versões diretas usadas na validação, instale `requirements-testadas.txt` no lugar de `requirements.txt`. Os pacotes transitivos ainda são resolvidos pelo pip.

## Formato de saída

Exemplo ilustrativo; gerações reais podem variar.

```json
{
  "translation": "Le temps est beau aujourd’hui.",
  "source_language": "en",
  "target_language": "fr"
}
```
