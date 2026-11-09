from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from schemas import TextRequest, TranslationResponse
from service import Translator


@asynccontextmanager
async def lifespan(app: FastAPI):
    translator = Translator("Helsinki-NLP/opus-mt-en-fr")
    app.state.translate = translator.translate
    yield

app = FastAPI(title="parte1_q2_traducao_fr", lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/translate", response_model=TranslationResponse)
def translate(data: TextRequest):
    try:
        result = app.state.translate(data.text)
        return {"translation": result, "target_language": "fr"}
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(503, "Falha de inferência local.") from exc
