"""Tokenizer loading helpers for River model aliases."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from huggingface_hub import hf_hub_download
from huggingface_hub.errors import StrictDataclassClassValidationError
from transformers import AutoTokenizer, PreTrainedTokenizerFast

# Canonical model roots. Any deployment name of the form "<root>-<suffix>"
# resolves to the root's tokenizer (see resolve_tokenizer_name), so a new
# canonical model whose own name extends an existing root with a hyphen
# (e.g. a hypothetical "<root>-Instruct" with a different tokenizer) MUST be
# added here as its own root — longest-root matching then keeps it distinct.
MODEL_TOKENIZER_ALIASES: dict[str, str] = {
    # The River serving alias uses FP8 weights but the published tokenizer is
    # attached to the underlying public Qwen checkpoint, not a separate FP8
    # Hugging Face repository.
    "Qwen/Qwen3.6-35B-A3B-FP8": "Qwen/Qwen3.6-35B-A3B",
    "Qwen/Qwen3.5-397B-A17B-FP8": "Qwen/Qwen3.5-397B-A17B-FP8",
    "nvidia/Kimi-K2.6-NVFP4": "nvidia/Kimi-K2.6-NVFP4",
    "nvidia/GLM-5.1-NVFP4": "nvidia/GLM-5.1-NVFP4",
    "nvidia/GLM-5.2-NVFP4": "nvidia/GLM-5.2-NVFP4",
}


def resolve_tokenizer_name(model_name: str) -> str:
    """Return the tokenizer for a canonical River model or one of its aliases.

    Deployment aliases must append a hyphen-delimited suffix to a canonical
    model name. Longest-root matching keeps the result deterministic if a
    future canonical model name extends another root.
    """
    matches = (
        (model_root, tokenizer_name)
        for model_root, tokenizer_name in MODEL_TOKENIZER_ALIASES.items()
        if model_name == model_root or model_name.startswith(f"{model_root}-")
    )
    match = max(matches, key=lambda candidate: len(candidate[0]), default=None)
    return model_name if match is None else match[1]


def _is_glm5_model(model_name: str) -> bool:
    lowered = model_name.lower()
    return "glm-5" in lowered or "glm5" in lowered


def _tokenizer_json_path(
    tokenizer_name: str,
    *,
    revision: str | None = None,
    local_files_only: bool = False,
) -> Path:
    tokenizer_path = Path(tokenizer_name)
    if tokenizer_path.exists():
        if revision is not None:
            raise ValueError("revision cannot be combined with a local tokenizer path")
        if tokenizer_path.is_file():
            return tokenizer_path
        return tokenizer_path / "tokenizer.json"
    kwargs: dict[str, Any] = {"revision": revision} if revision is not None else {}
    if local_files_only:
        kwargs["local_files_only"] = True
    return Path(hf_hub_download(tokenizer_name, "tokenizer.json", **kwargs))


def _load_glm5_tokenizer(
    tokenizer_name: str,
    *,
    revision: str | None = None,
    local_files_only: bool = False,
):
    tokenizer = PreTrainedTokenizerFast(
        tokenizer_file=str(
            _tokenizer_json_path(
                tokenizer_name,
                revision=revision,
                local_files_only=local_files_only,
            )
        ),
        eos_token="<|endoftext|>",
        pad_token="<|endoftext|>",
        # GLM-5.1 aliases in River are text-only. These special tokens mirror
        # the upstream tokenizer vocabulary; the fallback chat template below
        # intentionally assumes string message content.
        additional_special_tokens=[
            "[MASK]",
            "[gMASK]",
            "[sMASK]",
            "<sop>",
            "<eop>",
            "<|system|>",
            "<|user|>",
            "<|assistant|>",
            "<|observation|>",
            "<|begin_of_image|>",
            "<|end_of_image|>",
            "<|begin_of_video|>",
            "<|end_of_video|>",
            "<|begin_of_audio|>",
            "<|end_of_audio|>",
            "<|begin_of_transcription|>",
            "<|end_of_transcription|>",
        ],
    )
    tokenizer.chat_template = """[gMASK]<sop>
{%- for msg in messages %}
{%- if msg.role == 'system' %}
<|system|>
{{ msg.content }}
{%- elif msg.role == 'user' %}
<|user|>
{{ msg.content }}
{%- elif msg.role == 'assistant' %}
<|assistant|>
{{ msg.content }}
{%- endif %}
{%- endfor %}
{% if add_generation_prompt %}<|assistant|>
{% endif %}"""
    # ``PreTrainedTokenizerFast`` is initialized from a local tokenizer.json,
    # so retain the resolved Hugging Face source for callers that attest a
    # tokenizer object they already constructed.
    tokenizer.name_or_path = tokenizer_name
    return tokenizer


def _load_tokenizer_name(
    tokenizer_name: str,
    *,
    revision: str | None = None,
    local_files_only: bool = False,
):
    try:
        kwargs: dict[str, Any] = {"revision": revision} if revision is not None else {}
        if local_files_only:
            kwargs["local_files_only"] = True
        tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name,
            trust_remote_code=True,
            **kwargs,
        )
    except StrictDataclassClassValidationError:
        # Transformers validates newer GLM-5 model configurations before it
        # resolves the tokenizer implementation. River only needs the local
        # tokenizer.json for its text-only GLM-5 aliases.
        if not _is_glm5_model(tokenizer_name):
            raise
        return _load_glm5_tokenizer(
            tokenizer_name,
            revision=revision,
            local_files_only=local_files_only,
        )
    except ValueError as exc:
        # Observed with the locked transformers 4.57.1/5.6.0 paths when GLM-5
        # returns a TokenizersBackend object instead of a PreTrainedTokenizer.
        if not _is_glm5_model(tokenizer_name) or "TokenizersBackend" not in str(exc):
            raise
        return _load_glm5_tokenizer(
            tokenizer_name,
            revision=revision,
            local_files_only=local_files_only,
        )

    # The same locked transformers paths can also return TokenizersBackend
    # successfully, so normalize that case before River uses chat templating.
    if (
        _is_glm5_model(tokenizer_name)
        and type(tokenizer).__name__ == "TokenizersBackend"
    ):
        return _load_glm5_tokenizer(
            tokenizer_name,
            revision=revision,
            local_files_only=local_files_only,
        )
    return tokenizer


def load_tokenizer(
    tokenizer: str | Any | None = None,
    *,
    base_model: str | None = None,
    revision: str | None = None,
    local_files_only: bool = False,
    resolve_aliases: bool = True,
):
    """Load or return a tokenizer for River client result parsing.

    ``base_model`` remains the public River model name used for routing. When
    it is a hyphen-suffixed deployment alias of a known canonical model, this
    helper resolves it to the underlying Hugging Face tokenizer id before
    loading. ``local_files_only`` keeps sealed jobs from reaching Hugging Face
    after their tokenizer revision has been frozen. ``resolve_aliases=False``
    retains a deployment's own tokenizer source for unpinned compatibility
    paths.
    """
    if tokenizer is None:
        if base_model is None:
            raise ValueError("base_model is required when tokenizer is not provided")
        tokenizer_name = base_model
    elif isinstance(tokenizer, str):
        tokenizer_name = tokenizer
    else:
        if revision is not None:
            raise ValueError("revision cannot be combined with a pre-loaded tokenizer")
        return tokenizer

    if revision is not None and Path(tokenizer_name).exists():
        raise ValueError("revision cannot be combined with a local tokenizer path")
    if revision is not None and not resolve_aliases:
        resolved_name = resolve_tokenizer_name(tokenizer_name)
        if resolved_name != tokenizer_name:
            raise ValueError("immutable revisions require the resolved tokenizer alias")
    return _load_tokenizer_name(
        resolve_tokenizer_name(tokenizer_name) if resolve_aliases else tokenizer_name,
        revision=revision,
        local_files_only=local_files_only,
    )
