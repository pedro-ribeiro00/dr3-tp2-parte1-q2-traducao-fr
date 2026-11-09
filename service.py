from threading import Lock
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class Translator:
    def __init__(self, model_id: str):
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_id)
        self.model.eval()
        self.lock = Lock()
        # Reserva espaço para tokens especiais e para expansão da tradução.
        self.chunk_size = min(320, self.model.config.max_position_embeddings - 2)

    def translate(self, text: str) -> str:
        ids = self.tokenizer.encode(text, add_special_tokens=False)
        output = []
        # Evita truncamento silencioso: todos os tokens passam pelo modelo.
        # Cortes fixos podem separar frases e reduzir contexto entre blocos.
        with self.lock, torch.inference_mode():
            for start in range(0, len(ids), self.chunk_size):
                chunk = ids[start:start + self.chunk_size]
                inputs = self.tokenizer.prepare_for_model(chunk, return_tensors="pt")
                inputs = {name: value.unsqueeze(0) if value.ndim == 1 else value
                          for name, value in inputs.items()}
                result = self.model.generate(**inputs, max_new_tokens=500, num_beams=4)
                # Não devolver tradução incompleta caso a saída atinja o teto.
                if result[0, -1].item() != self.tokenizer.eos_token_id:
                    raise ValueError("A tradução excedeu o limite de saída; envie trechos menores.")
                output.append(self.tokenizer.decode(result[0], skip_special_tokens=True))
        return " ".join(output)
