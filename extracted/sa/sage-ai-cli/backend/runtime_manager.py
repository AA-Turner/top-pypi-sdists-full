import threading


def _get_runtime_map():
    """Lazy-load runtime classes so optional deps (llama-cpp-python etc.)
    aren't required at import time — critical for Cloud Run where only
    the server extras are installed."""
    runtimes = {}
    try:
        from .runtimes.llama_cpp_runtime import LlamaCppRuntime
        runtimes["llama_cpp"] = LlamaCppRuntime
    except ImportError:
        pass
    try:
        from .runtimes.onnx_runtime import OnnxRuntime
        runtimes["onnx"] = OnnxRuntime
    except ImportError:
        pass
    try:
        from .runtimes.transformers_runtime import TransformersRuntime
        runtimes["transformers"] = TransformersRuntime
    except ImportError:
        pass
    try:
        from .runtimes.vllm_runtime import VllmRuntime
        runtimes["vllm"] = VllmRuntime
    except ImportError:
        pass
    try:
        from .runtimes.ollama_runtime import OllamaRuntime
        runtimes["ollama"] = OllamaRuntime
    except ImportError:
        pass
    try:
        from .runtimes.cloud_runtime import CloudRuntime
        runtimes["cloud"] = CloudRuntime
    except ImportError:
        pass
    return runtimes


class RuntimeManager:
    def __init__(self) -> None:
        self.runtime = None
        self.loaded_model_id: str | None = None
        self.loaded_runtime: str | None = None
        self._lock = threading.RLock()

    def load(
        self, runtime_name: str, model_id: str, model_path: str, threads: int | None
    ) -> None:
        with self._lock:
            cls = _get_runtime_map().get(runtime_name)
            if cls is None:
                raise ValueError(
                    f"Unsupported runtime: {runtime_name}. "
                    f"Available: {', '.join(_get_runtime_map())}"
                )

            # P1-11: Preserve current runtime if new load fails
            # Try to load new runtime BEFORE unloading current one
            new_runtime = cls()
            try:
                new_runtime.load(model_path, threads=threads)
            except Exception as e:
                # Close the failed new runtime
                closer = getattr(new_runtime, "close", None) or getattr(new_runtime, "unload", None)
                if callable(closer):
                    try:
                        closer()
                    except Exception:
                        pass
                # Re-raise with preserved current runtime
                raise RuntimeError(f"Failed to load {model_id}: {e}") from e

            # New runtime loaded successfully, now safe to unload old one
            self.unload()
            self.runtime = new_runtime
            self.loaded_model_id = model_id
            self.loaded_runtime = runtime_name

    def unload(self) -> None:
        with self._lock:
            runtime = self.runtime
            self.runtime = None
            self.loaded_model_id = None
            self.loaded_runtime = None
            if runtime is None:
                return
            closer = getattr(runtime, "close", None) or getattr(runtime, "unload", None)
            if callable(closer):
                closer()

    def ensure_loaded(self) -> None:
        with self._lock:
            if self.runtime is None:
                raise RuntimeError("No model loaded")
