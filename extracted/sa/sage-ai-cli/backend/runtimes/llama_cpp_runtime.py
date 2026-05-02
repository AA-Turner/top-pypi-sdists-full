from ..schemas import ChatMessage
from .base import RuntimeAdapter


class LlamaCppRuntime(RuntimeAdapter):
    def __init__(self) -> None:
        self.model = None

    def load(self, model_path: str, threads: int | None = None) -> None:
        import platform
        try:
            from llama_cpp import Llama
        except ImportError as exc:
            raise RuntimeError(
                "llama-cpp-python is not installed in this environment."
            ) from exc
        except Exception as exc:
            # Wheel installed but bundled native library failed to load
            # (e.g. musl wheel on glibc, missing VC++ runtime on Windows).
            raise RuntimeError(
                f"llama-cpp-python native library failed to load: {exc}"
            ) from exc

        kwargs = {
            "model_path": model_path,
            "n_ctx": 4096,
            "n_batch": 512,
            "verbose": False,
        }
        # Disable GPU on x86_64 macOS (Rosetta) — Metal requires arm64
        if platform.system() == "Darwin" and platform.machine() == "x86_64":
            kwargs["n_gpu_layers"] = 0
        if threads:
            kwargs["n_threads"] = threads
        self.model = Llama(**kwargs)

    def chat(
        self,
        messages: list[ChatMessage],
        temperature: float,
        max_tokens: int,
    ) -> str:
        if self.model is None:
            raise RuntimeError("Model is not loaded")
        payload = [m.model_dump() for m in messages]
        result = self.model.create_chat_completion(
            messages=payload,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=False,
        )
        # Safe extraction with bounds checking
        choices = result.get("choices", [])
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
        if self.model is None:
            raise RuntimeError("Model is not loaded")
        payload = [m.model_dump() for m in messages]
        stream = self.model.create_chat_completion(
            messages=payload,
            temperature=temperature,
            max_tokens=max_tokens,
            stream=True,
        )
        for item in stream:
            # Safe extraction with bounds checking
            choices = item.get("choices", [])
            if not choices:
                continue
            first_choice = choices[0] if choices else {}
            delta = first_choice.get("delta", {})
            text = delta.get("content")
            if text:
                yield text
