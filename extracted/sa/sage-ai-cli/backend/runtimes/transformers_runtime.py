import torch

from ..schemas import ChatMessage
from .base import RuntimeAdapter


class TransformersRuntime(RuntimeAdapter):
    def __init__(self) -> None:
        self.model = None
        self.tokenizer = None

    def load(self, model_path: str, threads: int | None = None) -> None:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer

        if threads:
            torch.set_num_threads(threads)
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_path,
            local_files_only=True,
            trust_remote_code=True,
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            local_files_only=True,
            trust_remote_code=True,
            device_map="auto",
        )
        self.model.eval()

    def _render_messages(self, messages: list[ChatMessage]) -> str:
        rendered = []
        for msg in messages:
            rendered.append(f"{msg.role}: {msg.content}")
        rendered.append("assistant:")
        return "\n".join(rendered)

    def chat(
        self,
        messages: list[ChatMessage],
        temperature: float,
        max_tokens: int,
    ) -> str:
        if self.model is None or self.tokenizer is None:
            raise RuntimeError("Model is not loaded")
        prompt = self._render_messages(messages)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_tokens,
                temperature=temperature,
                do_sample=temperature > 0,
                top_p=0.95,
                pad_token_id=self.tokenizer.eos_token_id,
            )
        completion = self.tokenizer.decode(
            output[0][inputs["input_ids"].shape[-1] :],
            skip_special_tokens=True,
        )
        return completion.strip()

    def stream_chat(
        self,
        messages: list[ChatMessage],
        temperature: float,
        max_tokens: int,
    ):
        text = self.chat(messages, temperature, max_tokens)
        if not text:
            return
        for token in text.split():
            yield token + " "
