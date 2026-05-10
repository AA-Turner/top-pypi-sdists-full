"""Local GGUF model provider via llama-cpp-python."""

from __future__ import annotations

import contextlib
import gc
import logging
import os
import platform
import sys
from collections.abc import Iterator

from ..config import LocalModel, SageConfig
from .base import Message, ModelInfo, ProviderBase

_logger = logging.getLogger(__name__)


@contextlib.contextmanager
def _suppress_native_stderr():
    """File-descriptor-level stderr capture while loading llama_cpp.

    The llama-cpp-python C library writes errors (Metal shader compilation
    failures, model-load failures, partial-init __del__ AttributeError) to
    file descriptor 2 directly — Python-level `sys.stderr = io.StringIO()`
    has no effect. We dup2 fd 2 to an OS pipe for the duration of the load,
    then restore. The pipe's read end is yielded so callers can pull the
    captured text on failure (they'll typically log it at debug level
    rather than print it; sage falls back gracefully when llama_cpp dies).
    """
    sys.stderr.flush()
    pipe_r, pipe_w = os.pipe()
    saved_fd = os.dup(2)
    os.dup2(pipe_w, 2)
    os.close(pipe_w)

    captured: list[bytes] = []

    class _Reader:
        def read_text(self) -> str:
            # Drain the pipe (non-blocking) and decode.
            os.set_blocking(pipe_r, False)
            while True:
                try:
                    chunk = os.read(pipe_r, 65536)
                except BlockingIOError:
                    break
                if not chunk:
                    break
                captured.append(chunk)
            return b"".join(captured).decode("utf-8", errors="replace")

    reader = _Reader()
    try:
        yield reader
    finally:
        # Restore fd 2 first so subsequent normal output works.
        os.dup2(saved_fd, 2)
        os.close(saved_fd)
        # Drain anything still in flight.
        try:
            reader.read_text()
        except Exception:
            pass
        try:
            os.close(pipe_r)
        except Exception:
            pass

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

    def _maybe_speculative_kwargs(self) -> dict:
        """Return kwargs for speculative decoding when configured.

        Wave 3: small draft model proposes tokens, target model verifies.
        Lazy import keeps the speculative module optional.
        """
        try:
            from sage.core.speculative import speculative_kwargs
            return speculative_kwargs(self._config)
        except Exception:
            return {}

    def _try_load_prefix_cache(self, model_name: str, system_prompt: str) -> bool:
        """Hydrate the loaded model's KV state from disk for a known prefix.

        Wave 5: prefix cache. Returns True if a cache hit was loaded.
        Uses Llama.load_state() when available; silently skips otherwise.
        """
        if self._model is None or not system_prompt:
            return False
        try:
            from sage.core.prefix_cache import PrefixCache, PrefixCacheKey, prefix_id_for
        except Exception:
            return False
        pid = prefix_id_for(system_prompt, model_name)
        cache = PrefixCache()
        path = cache.get(PrefixCacheKey(model=f"llama_cpp:{model_name}", prefix_id=pid))
        if path is None:
            return False
        try:
            data = path.read_bytes()
            self._model.load_state(data)  # type: ignore[union-attr]
            return True
        except Exception:
            return False

    def _save_prefix_cache(self, model_name: str, system_prompt: str) -> None:
        """Persist the loaded model's current KV state for the given prefix."""
        if self._model is None or not system_prompt:
            return
        try:
            from sage.core.prefix_cache import PrefixCache, PrefixCacheKey, prefix_id_for
        except Exception:
            return
        try:
            data = self._model.save_state()  # type: ignore[union-attr]
        except Exception:
            return
        if isinstance(data, (bytes, bytearray)):
            payload = bytes(data)
        else:
            return
        pid = prefix_id_for(system_prompt, model_name)
        PrefixCache().put(PrefixCacheKey(model=f"llama_cpp:{model_name}", prefix_id=pid), payload)

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
        # Wave 3: speculative decoding (no-op when not configured)
        kwargs.update(self._maybe_speculative_kwargs())

        # Wrap Llama() in fd-level stderr capture so the C library's noisy
        # output (Metal shader compile errors, partial-init __del__ traces)
        # doesn't pollute the user's terminal when sage is going to fall
        # back to Ollama anyway. On success the buffer is empty / boring;
        # on failure we log it at debug level for diagnostics.
        load_error_msg: str | None = None
        captured_text = ""
        with _suppress_native_stderr() as captured:
            try:
                self._model = Llama(**kwargs)
                self._loaded_name = model_name
            except BaseException as exc:
                # Capture the message NOW. We don't keep a reference to
                # `exc` itself: its `__traceback__` would hold the local
                # frame which holds the partially-initialized Llama object,
                # which would survive GC until the calling code's exception
                # cleanup runs — at which point fd 2 is restored and the
                # broken `__del__` AttributeError leaks to the terminal.
                load_error_msg = f"{type(exc).__name__}: {exc}"
                exc.__traceback__ = None
                del exc
            # Force any partial Llama / LlamaModel object to GC NOW, while
            # stderr is still suppressed. Their broken __del__ writes go
            # into the captured buffer instead of leaking to the terminal.
            gc.collect()
            captured_text = captured.read_text()

        if load_error_msg is not None:
            if captured_text:
                _logger.debug(
                    "llama_cpp native stderr during failed load (%d chars):\n%s",
                    len(captured_text), captured_text[:2000],
                )
            _logger.debug("llama_cpp load_error: %s", load_error_msg)
            # Plain raise (no `from`) — `from exc` would keep `exc` alive,
            # and `exc` may hold transitive references to a partial Llama
            # object that hasn't finished GC. sage's fallback chain in
            # main.py catches RuntimeError and routes to Ollama / cloud.
            raise RuntimeError(
                f"llama_cpp could not load '{model_name}'. SAGE will fall "
                "back to Ollama or a cloud model. For diagnostics: "
                "`sage --log-level debug run` or `sage fix-llama-cpp`."
            )

    def _to_chat_messages(self, messages: list[Message]) -> list[dict]:
        return [{"role": m.role, "content": m.content} for m in messages]

    def _maybe_grammar(self, enable: bool):
        """Return a LlamaGrammar instance when enable=True, else None.

        Wave 2: GBNF-constrained output for the FILE/READ/RUN/SEARCH protocol.
        Loaded lazily so the import-time cost is only paid when we use it.
        """
        if not enable:
            return None
        try:
            from sage.core.grammar import load_grammar
            return load_grammar()
        except Exception:
            return None

    def generate(
        self,
        messages: list[Message],
        model: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        enable_grammar: bool = False,
    ) -> str:
        name = model or self._first_model()
        self._ensure_loaded(name)
        kwargs: dict = {
            "messages": self._to_chat_messages(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
            "repeat_penalty": 1.1,
            "top_p": 0.9,
            "stream": False,
        }
        gram = self._maybe_grammar(enable_grammar)
        if gram is not None:
            kwargs["grammar"] = gram
        result = self._model.create_chat_completion(**kwargs)  # type: ignore[union-attr]
        return result["choices"][0]["message"]["content"]

    def stream(
        self,
        messages: list[Message],
        model: str = "",
        temperature: float = 0.7,
        max_tokens: int = 2048,
        enable_grammar: bool = False,
    ) -> Iterator[str]:
        name = model or self._first_model()
        self._ensure_loaded(name)
        kwargs: dict = {
            "messages": self._to_chat_messages(messages),
            "temperature": temperature,
            "max_tokens": max_tokens,
            "repeat_penalty": 1.1,
            "top_p": 0.9,
            "stream": True,
        }
        gram = self._maybe_grammar(enable_grammar)
        if gram is not None:
            kwargs["grammar"] = gram
        chunks = self._model.create_chat_completion(**kwargs)  # type: ignore[union-attr]
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
