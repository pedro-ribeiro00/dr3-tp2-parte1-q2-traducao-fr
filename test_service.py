from unittest.mock import Mock, patch
import torch
from service import Translator


def test_all_input_tokens_are_processed_in_batched_tensors():
    tokenizer = Mock()
    tokenizer.encode.return_value = list(range(700))
    tokenizer.eos_token_id = 2
    tokenizer.prepare_for_model.side_effect = lambda ids, **kw: {"input_ids": torch.tensor(ids), "attention_mask": torch.ones(len(ids), dtype=torch.long)}
    tokenizer.decode.return_value = "translated block"
    model = Mock()
    model.config.max_position_embeddings = 512
    model.generate.return_value = torch.tensor([[0, 2]])
    with patch("service.AutoTokenizer.from_pretrained", return_value=tokenizer), patch("service.AutoModelForSeq2SeqLM.from_pretrained", return_value=model):
        translator = Translator("model-test")
        assert translator.translate("long input") == "translated block translated block translated block"
    calls = model.generate.call_args_list
    assert len(calls) == 3
    assert [c.kwargs["input_ids"].shape for c in calls] == [(1,320),(1,320),(1,60)]
    recovered = torch.cat([c.kwargs["input_ids"][0] for c in calls]).tolist()
    assert recovered == list(range(700))
