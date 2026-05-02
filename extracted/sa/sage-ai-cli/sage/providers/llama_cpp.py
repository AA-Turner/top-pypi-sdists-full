"""Local GGUF model provider via llama-cpp-python."""

from __future__ import annotations

import platform
from collections.abc import Iterator

from ..config import LocalModel, SageConfig
from .base import Message, ModelInfo, ProviderBase

_MODELS_DIR_DEFAULT = None  # resolved lazily

# Architectures known to work with the installed llama-cpp-python.
# When a GGUF file declares an unsupported architecture we skip it rather
# than registering it (which causes repeated "Failed to load model" errors).
_KNOWN_SUPPORTED_ARCHS = {
    "llama", "llama2", "mistral", "mixtral",
    "phi2", "phi", "starcoder", "refact",
    "bert", "nomic-bert", "bloom",
    "falcon", "mpt", "gptj", "gpt2", "gpt-j",
    "orion", "stablelm",
    "qwen2", "qwen2moe",
    "deepseek2",
    "gemma", "gemma2",          # gemma / gemma2 OK
    "command-r", "cohere",
    "dbrx", "jais",
    "internlm2",
    "exaone",
}


def _gguf_arch_supported(path) -> bool:
    """Read the GGUF file header and return True if the architecture is supported."""
    import struct
    try:
        with open(path, "rb") as f:
            magic = f.read(4)
            if magic != b"GGUF":
                return False
            version = struct.unpack("<I", f.read(4))[0]
            if version < 2:
                return True  # very old — attempt to load
            # Skip tensor_count + metadata_kv_count
            f.read(16)
            # Scan metadata for "general.architecture"
            kv_count = struct.unpack("<Q", f.read(8))[0]
            # We only care about the first few KV entries
            for _ in range(min(kv_count, 20)):
                # key: length (u64) + bytes
                klen = struct.unpack("<Q", f.read(8))[0]
                key = f.read(klen).decode("utf-8", errors="replace")
                # value type (u32)
                vtype = struct.unpack("<I", f.read(4))[0]
                if vtype == 8:  # STRING
                    slen = struct.unpack("<Q", f.read(8))[0]
                    val = f.read(slen).decode("utf-8", errors="replace")
                    if key == "general.architecture":
                        return val.lower() in _KNOWN_SUPPORTED_ARCHS
                elif vtype == 0:  f.read(1)       # UINT8
                elif vtype == 1:  f.read(1)        # INT8
                elif vtype == 2:  f.read(2)        # UINT16
                elif vtype == 3:  f.read(2)        # INT16
                elif vtype == 4:  f.read(4)        # UINT32
                elif vtype == 5:  f.read(4)        # INT32
                elif vtype == 6:  f.read(4)        # FLOAT32
                elif vtype == 7:  f.read(1)        # BOOL
                elif vtype == 9:  f.read(8)        # UINT64
                elif vtype == 10: f.read(8)        # INT64
                elif vtype == 11: f.read(8)        # FLOAT64
                elif vtype == 12:                  # ARRAY — skip
                    atype = struct.unpack("<I", f.read(4))[0]
                    alen  = struct.unpack("<Q", f.read(8))[0]
                    break  # can't easily skip arrays; stop scanning
                else:
                    break
    except Exception:
        pass
    return True  # unknown → attempt to load (fail-safe)


def _models_dir():
    from sage.config import SAGE_DIR
    d = SAGE_DIR / "models"
    d.mkdir(parents=True, exist_ok=True)
    return d


class LlamaCppProvider(ProviderBase):
    """Runs GGUF models locally through llama-cpp-python."""

    name = "llama_cpp"

    def __init__(self, config: SageConfig) -> None:
        self._config = config
        self._loaded_name: str | None = None
        self._model: object | None = None  # Llama instance (lazy import)

    def _all_local_models(self) -> list[tuple[str, "Path"]]:
        """Return (name, path) for every usable local GGUF model.

        Combines config-registered models with any .gguf files already
        present in ~/.sage/models/ — so models downloaded via `sage pull`
        are visible even before being explicitly registered.
        """
        from pathlib import Path

        seen: dict[str, Path] = {}

        # Config-registered models (highest priority)
        for name in self._config.local_model_names():
            entry = self._config.get_local_model(name)
            if entry:
                p = Path(entry.path)
                if p.is_file() and p.stat().st_size > 0:
                    seen[name] = p

        # Disk scan — picks up any .gguf files pulled via `sage pull`
        models_dir = _models_dir()
        for gguf in sorted(models_dir.glob("*.gguf")):
            if gguf.stat().st_size > 0 and gguf.stem not in seen:
                # Quick sanity-check: read the GGUF architecture field.
                # If the architecture is not supported by this llama.cpp build, skip it.
                if not _gguf_arch_supported(gguf):
                    continue
                seen[gguf.stem] = gguf
                # Auto-register so future commands don't need another scan
                try:
                    from sage.config import save_config
                    if gguf.stem not in self._config.models:
                        self._config.models[gguf.stem] = {"path": str(gguf)}
                        save_config(self._config)
                except Exception:
                    pass

        return list(seen.items())

    def is_available(self) -> bool:
        # Catch broad Exception (not just ImportError): a wheel whose
        # bundled libllama.so can't load (e.g. musl wheel on glibc) raises
        # RuntimeError on import, and we want to report unavailable rather
        # than crash the provider router.
        try:
            import llama_cpp as _  # noqa: F401
        except Exception:
            return False
        return len(self._all_local_models()) > 0

    def list_models(self) -> list[ModelInfo]:
        try:
            import llama_cpp as _  # noqa: F401
        except Exception:
            return []
        return [
            ModelInfo(id=name, provider="llama_cpp", name=name, local=True)
            for name, _ in self._all_local_models()
        ]

    def _ensure_loaded(self, model_name: str) -> None:
        """Load the model if not already loaded (or if a different model is requested)."""
        if self._loaded_name == model_name and self._model is not None:
            return

        # Try config first, then disk scan
        entry: LocalModel | None = self._config.get_local_model(model_name)
        model_path_str: str | None = entry.path if entry else None
        if model_path_str is None:
            for name, path in self._all_local_models():
                if name == model_name:
                    model_path_str = str(path)
                    break
        if model_path_str is None:
            raise RuntimeError(
                f"Model '{model_name}' not found. Run: sage pull {model_name}"
            )

        # Patch entry for the rest of this method
        class _Entry:
            path = model_path_str
            threads = entry.threads if entry else None

        entry = _Entry()  # type: ignore[assignment]

        try:
            from llama_cpp import Llama
        except ImportError as exc:
            raise RuntimeError(
                "llama-cpp-python is not installed. Run `sage` once to bootstrap it, "
                f"or `sage pull ollama:{model_name} && sage use ollama:{model_name}` "
                "to use Ollama instead."
            ) from exc
        except Exception as exc:
            raise RuntimeError(
                f"llama-cpp-python is installed but its native library failed to load: {exc}. "
                f"Try `sage` (auto-repairs) or fall back with "
                f"`sage pull ollama:{model_name} && sage use ollama:{model_name}`."
            ) from exc

        kwargs: dict = {
            "model_path": entry.path,
            "n_ctx": 16384,
            "n_batch": 1024,
            "verbose": False,
        }
        # Disable GPU on x86_64 macOS (Rosetta) — Metal requires arm64
        if platform.system() == "Darwin" and platform.machine() == "x86_64":
            kwargs["n_gpu_layers"] = 0
        if entry.threads:
            kwargs["n_threads"] = entry.threads

        self._model = Llama(**kwargs)
        self._loaded_name = model_name

    def _to_chat_messages(self, messages: list[Message]) -> list[dict]:
        return [{"role": m.role, "content": m.content} for m in messages]

    def generate(
        self,
        messages: list[Message],
        model: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> str:
        name = model or self._first_model()
        self._ensure_loaded(name)
        result = self._model.create_chat_completion(  # type: ignore[union-attr]
            messages=self._to_chat_messages(messages),
            temperature=temperature,
            max_tokens=max_tokens,
            repeat_penalty=1.1,
            top_p=0.9,
            stream=False,
        )
        return result["choices"][0]["message"]["content"]

    def stream(
        self,
        messages: list[Message],
        model: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048,
    ) -> Iterator[str]:
        name = model or self._first_model()
        self._ensure_loaded(name)
        chunks = self._model.create_chat_completion(  # type: ignore[union-attr]
            messages=self._to_chat_messages(messages),
            temperature=temperature,
            max_tokens=max_tokens,
            repeat_penalty=1.1,
            top_p=0.9,
            stream=True,
        )
        for chunk in chunks:
            delta = chunk["choices"][0].get("delta", {})
            text = delta.get("content")
            if text:
                yield text

    def _first_model(self) -> str:
        names = self._config.local_model_names()
        if not names:
            raise RuntimeError(
                "No local models registered. Run: sage config set models.<name>.path /path/to/model.gguf"
            )
        return names[0]
