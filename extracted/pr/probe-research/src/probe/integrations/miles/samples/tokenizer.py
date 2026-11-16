"""The run's tokenizer (`args.hf_checkpoint`) as a `Decode`, loaded once per process and only when a sample needs
decoded turns (no messages, not a Harbor trial: D4). No transformers, or a checkpoint that will not load: no decode."""

from __future__ import annotations

import logging
import threading
from typing import Any

from probe.sdk.run.samples.rollout import Decode, make_decode

logger = logging.getLogger(__name__)

_decodes: dict[str, Decode | None] = {}
_lock = threading.Lock()


def get_decode(checkpoint: str | None) -> Decode | None:
    """``checkpoint``'s tokenizer as a `Decode`; None when it cannot load (logged once per checkpoint)."""
    if not checkpoint:
        return None
    with _lock:
        if checkpoint not in _decodes:
            tokenizer = load_tokenizer(checkpoint)
            _decodes[checkpoint] = make_decode(tokenizer) if tokenizer is not None else None
        return _decodes[checkpoint]


def load_tokenizer(checkpoint: str) -> Any | None:
    try:
        from transformers import AutoTokenizer
    except ImportError:
        logger.info("Probe cannot rebuild Miles turns from tokens: transformers is not installed")
        return None
    try:
        return AutoTokenizer.from_pretrained(checkpoint, trust_remote_code=True)
    except Exception:  # noqa: BLE001 -- a broken checkpoint never fails the rollout
        logger.warning("Probe could not load the tokenizer at %s; samples keep no decoded turns", checkpoint,
                       exc_info=True)
        return None
