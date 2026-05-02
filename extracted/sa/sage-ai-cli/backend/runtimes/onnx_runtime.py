"""ONNX Runtime adapter for local inference.

Supports ONNX-format language models using onnxruntime or
onnxruntime-gpu. This is also the format used by ONNX Runtime Web
for in-browser inference via WebGPU/WebGL.
"""

import logging
from pathlib import Path

from ..schemas import ChatMessage
from .base import RuntimeAdapter

logger = logging.getLogger("ai-platform.runtime.onnx")


class OnnxRuntime(RuntimeAdapter):
    def __init__(self) -> None:
        self.session = None
        self.tokenizer = None

    def load(self, model_path: str, threads: int | None = None) -> None:
        import onnxruntime as ort

        path = Path(model_path)

        # Configure session options
        opts = ort.SessionOptions()
        if threads:
            opts.intra_op_num_threads = threads
            opts.inter_op_num_threads = threads
        opts.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL

        # Select execution providers
        providers = []
        available = ort.get_available_providers()
        if "CUDAExecutionProvider" in available:
            providers.append("CUDAExecutionProvider")
        if "CoreMLExecutionProvider" in available:
            providers.append("CoreMLExecutionProvider")
        providers.append("CPUExecutionProvider")

        # Locate the ONNX model file
        if path.is_dir():
            onnx_files = list(path.glob("*.onnx"))
            if not onnx_files:
                raise FileNotFoundError(f"No .onnx files found in {path}")
            model_file = str(onnx_files[0])
        else:
            model_file = str(path)

        self.session = ort.InferenceSession(model_file, opts, providers=providers)

        # Try to load a tokenizer from the same directory
        try:
            from transformers import AutoTokenizer

            tokenizer_dir = path if path.is_dir() else path.parent
            self.tokenizer = AutoTokenizer.from_pretrained(
                str(tokenizer_dir), local_files_only=True
            )
        except Exception:
            logger.warning(
                "No tokenizer found alongside ONNX model at %s. "
                "Chat will use a basic prompt format.",
                model_path,
            )
            self.tokenizer = None

        providers_list = self.session.get_providers() if self.session else []
        active_provider = providers_list[0] if providers_list else "unknown"
        logger.info("ONNX model loaded from %s (provider: %s)", model_file, active_provider)

    def _render_prompt(self, messages: list[ChatMessage]) -> str:
        if self.tokenizer and hasattr(self.tokenizer, "apply_chat_template"):
            dicts = [{"role": m.role, "content": m.content} for m in messages]
            return self.tokenizer.apply_chat_template(
                dicts, tokenize=False, add_generation_prompt=True
            )
        parts = []
        for m in messages:
            parts.append(f"{m.role}: {m.content}")
        parts.append("assistant:")
        return "\n".join(parts)

    def chat(
        self,
        messages: list[ChatMessage],
        temperature: float,
        max_tokens: int,
    ) -> str:
        if self.session is None:
            raise RuntimeError("ONNX model is not loaded")

        prompt = self._render_prompt(messages)

        if self.tokenizer:
            return self._generate_with_tokenizer(prompt, max_tokens, temperature)
        return self._generate_raw(prompt, max_tokens)

    def stream_chat(
        self,
        messages: list[ChatMessage],
        temperature: float,
        max_tokens: int,
    ):
        # ONNX Runtime doesn't natively stream — simulate with word-level chunks
        text = self.chat(messages, temperature, max_tokens)
        if not text:
            return
        for word in text.split():
            yield word + " "

    def _generate_with_tokenizer(
        self, prompt: str, max_tokens: int, temperature: float
    ) -> str:
        """Autoregressive generation with tokenizer + ONNX session."""
        import numpy as np

        input_ids = self.tokenizer.encode(prompt, return_tensors="np")
        generated = input_ids.copy()

        for _ in range(max_tokens):
            feeds = {"input_ids": generated}
            # Try to provide attention_mask if the model expects it
            input_names = [inp.name for inp in self.session.get_inputs()]
            if "attention_mask" in input_names:
                feeds["attention_mask"] = np.ones_like(generated)

            outputs = self.session.run(None, feeds)
            if not outputs:
                break
            logits = outputs[0]  # shape: (batch, seq_len, vocab_size)
            if logits is None or logits.size == 0:
                break
            next_logits = logits[0, -1, :]

            if temperature > 0:
                probs = _softmax(next_logits / temperature)
                next_token = np.random.choice(len(probs), p=probs)
            else:
                next_token = int(np.argmax(next_logits))

            if next_token == self.tokenizer.eos_token_id:
                break

            generated = np.concatenate(
                [generated, np.array([[next_token]])], axis=1
            )

        new_tokens = generated[0, input_ids.shape[1] :]
        return self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

    def _generate_raw(self, prompt: str, max_tokens: int) -> str:
        """Fallback: run a single forward pass and return raw output."""
        import numpy as np

        # Basic byte-level encoding as fallback
        input_array = np.array(
            [[ord(c) for c in prompt[:512]]], dtype=np.int64
        )
        input_names = [inp.name for inp in self.session.get_inputs()]
        if not input_names:
            return "[ONNX error: no input names found]"
        feeds = {input_names[0]: input_array}
        outputs = self.session.run(None, feeds)
        if not outputs:
            return "[ONNX error: no outputs]"
        return f"[ONNX raw output — shape {outputs[0].shape}]"


def _softmax(x):
    import numpy as np

    e = np.exp(x - np.max(x))
    return e / e.sum()
