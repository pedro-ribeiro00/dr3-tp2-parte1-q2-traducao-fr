from pydantic import BaseModel, Field, field_validator

class TextRequest(BaseModel):
    text: str = Field(min_length=1, max_length=20000)

    @field_validator("text")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("O texto não pode estar em branco.")
        return value

class TranslationResponse(BaseModel):
    translation: str
    source_language: str = "en"
    target_language: str
