import os

import requests

from ..schemas import ChatMessage
from .base import RuntimeAdapter


class VllmRuntime(RuntimeAdapter):
    def __init__(self) -> None:
        self.model_name = ""
        self.base_url = os.getenv(
            "AI_PLATFORM_VLLM_BASE_URL", "http://127.0.0.1:8001/v1"
        )

    def load(self, model_path: str, threads: int | None = None) -> None:
        _ = threads
        self.model_name = model_path

    def chat(
        self,
        messages: list[ChatMessage],
        temperature: float,
        max_tokens: int,
    ) -> str:
        payload = {
            "model": self.model_name,
            "messages": [m.model_dump() for m in messages],
            "temperature": temperature,
            "max_tokens": max_tokens,
            "stream": False,
        }
        response = requests.post(
            f"{self.base_url}/chat/completions", json=payload, timeout=120
        )
        response.raise_for_status()
        data = response.json()
        # Safe extraction with bounds checking
        choices = data.get("choices", [])
        if not choices:
            return ""
        first_choice = choices[0] if choices else {}
        message = first_choice.get("message", {})
        return message.get("content", "")

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
