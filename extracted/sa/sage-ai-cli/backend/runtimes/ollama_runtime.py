"""Ollama runtime — talks to local Ollama server via REST API."""

import json
import subprocess
import sys

import httpx

from ..schemas import ChatMessage
from .base import RuntimeAdapter


class OllamaRuntime(RuntimeAdapter):
    def __init__(self) -> None:
        import os
        self._base_url = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
        self._model_name: str | None = None

    def load(self, model_path: str, threads: int | None = None) -> None:
        """For Ollama, model_path is the model name (e.g. 'qwen3.5')."""
        self._model_name = model_path
        # Auto-pull if not available
        self._ensure_pulled(model_path)

    def _ensure_pulled(self, model: str) -> None:
        """P2-24: Ensure model is pulled with proper error handling."""
        # Check if model is already pulled
        try:
            with httpx.Client(timeout=5) as client:
                resp = client.get(f"{self._base_url}/api/tags")
                resp.raise_for_status()
                pulled = {m["name"].split(":")[0] for m in resp.json().get("models", [])}
                base = model.split(":")[0]
                if base in pulled or model in pulled:
                    return
        except httpx.ConnectError:
            raise RuntimeError(
                f"Cannot connect to Ollama at {self._base_url}. "
                "Is Ollama running? Start with: ollama serve"
            )
        except httpx.TimeoutException:
            print(f"  Warning: Ollama server check timed out", file=sys.stderr)
        except Exception as exc:
            print(f"  Warning: Could not check Ollama models: {exc}", file=sys.stderr)

        # Pull the model
        print(f"  Pulling {model} via Ollama...", file=sys.stderr)
        try:
            result = subprocess.run(
                ["ollama", "pull", model],
                check=False,
                timeout=600,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                stderr = result.stderr.strip() if result.stderr else "Unknown error"
                raise RuntimeError(f"Failed to pull Ollama model '{model}': {stderr}")
        except FileNotFoundError:
            raise RuntimeError(
                "Ollama is not installed. Install from https://ollama.com"
            )
        except subprocess.TimeoutExpired:
            raise RuntimeError(f"Ollama pull timed out after 10 minutes for '{model}'")

    def chat(
        self,
        messages: list[ChatMessage],
        temperature: float,
        max_tokens: int,
    ) -> str:
        if not self._model_name:
            raise RuntimeError("No Ollama model loaded")
        payload = {
            "model": self._model_name,
            "messages": [m.model_dump() for m in messages],
            "stream": False,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        with httpx.Client(timeout=120) as client:
            resp = client.post(f"{self._base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
            msg = data.get("message", {})
            content = msg.get("content", "")
            thinking = msg.get("thinking", "")
            # Some models (qwen3.5, deepseek-r1) put reasoning in 'thinking' field
            # Include thinking as collapsed section if content is empty
            if not content.strip() and thinking.strip():
                return thinking.strip()
            if thinking.strip() and content.strip():
                return f"<details><summary>Thinking...</summary>\n\n{thinking.strip()}\n\n</details>\n\n{content.strip()}"
            return content

    def stream_chat(
        self,
        messages: list[ChatMessage],
        temperature: float,
        max_tokens: int,
    ):
        if not self._model_name:
            raise RuntimeError("No Ollama model loaded")
        payload = {
            "model": self._model_name,
            "messages": [m.model_dump() for m in messages],
            "stream": True,
            "options": {"temperature": temperature, "num_predict": max_tokens},
        }
        thinking_buffer = []
        started_content = False
        with httpx.Client(timeout=120) as client:
            with client.stream("POST", f"{self._base_url}/api/chat", json=payload) as resp:
                resp.raise_for_status()
                for line in resp.iter_lines():
                    if not line:
                        continue
                    try:
                        chunk = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    msg = chunk.get("message", {})
                    content = msg.get("content", "")
                    thinking = msg.get("thinking", "")
                    # Handle thinking tokens
                    if thinking:
                        thinking_buffer.append(thinking)
                    if content:
                        # If we had thinking, flush it as a collapsed block first
                        if thinking_buffer and not started_content:
                            full_thinking = "".join(thinking_buffer)
                            yield f"<details><summary>Thinking...</summary>\n\n{full_thinking}\n\n</details>\n\n"
                            thinking_buffer.clear()
                        started_content = True
                        yield content
                    if chunk.get("done"):
                        # If only thinking and no content, yield the thinking
                        if thinking_buffer and not started_content:
                            full_thinking = "".join(thinking_buffer)
                            yield full_thinking
                        break
