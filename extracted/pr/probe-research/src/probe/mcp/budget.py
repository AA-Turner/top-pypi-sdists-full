"""Exact limits for the JSON text Probe emits, independent of MCP wire framing.

The reference encoding is frozen and packaged: using tiktoken.get_encoding would
download its vocabulary on an empty cache. Nothing here imports tiktoken or reads
the vocabulary until the first count. Initialize that count on an MCP worker,
not the event loop; ordinary CLI/SDK imports need no tokenizer work.
"""

from __future__ import annotations

import base64
import hashlib
import json
import math
import threading
from dataclasses import dataclass
from importlib import resources
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from tiktoken import Encoding

MIN_TOKENS = 512
DEFAULT_TOKENS = 2000
MAX_TOKENS = 8000
BYTES_PER_TOKEN = 8
TOKENIZER_NAME = "o200k_base"
TOKENIZER_VERSION = "0.13.0"
VOCABULARY_SHA256 = "446a9538cb6c348e3516120d7c08b09f57c36495e2acfffe59a5bf8b0cfb1a2d"
CONFIG_SHA256 = "006868169d3cc1be4af6655c6a3123805e54a9bfba07dc08ad3b6b180194f2ae"


class InvalidBudget(ValueError):
    """Unsupported requested limit; the message never echoes caller data."""


class SerializationError(ValueError):
    """The response is not supported, finite, Unicode JSON."""


class TokenizerUnavailable(RuntimeError):
    """Counting cannot proceed safely; callers must fail closed."""


def _validate_json(value: Any, active: set[int]) -> None:
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError
        return
    if not isinstance(value, (dict, list)) or id(value) in active:
        raise ValueError
    active.add(id(value))
    try:
        if isinstance(value, dict):
            for key, item in value.items():
                # json.dumps coerces integer keys, which can silently create
                # duplicate JSON names and corrupt a reconstructed record.
                if not isinstance(key, str):
                    raise ValueError
                _validate_json(item, active)
        else:
            for item in value:
                _validate_json(item, active)
    finally:
        active.remove(id(value))


def serialize(value: Any) -> str:
    """Canonical compact JSON, with no arbitrary-object stringification.

    Accept JSON scalars, lists and string-keyed dictionaries. Preserve Unicode,
    array order and meaningful nulls; sort object keys for continuation hashes.
    A caller with UUIDs/datetimes/models must explicitly normalize them first.
    """
    try:
        _validate_json(value, set())
        text = json.dumps(
            value, ensure_ascii=False, allow_nan=False, separators=(",", ":"), sort_keys=True
        )
        text.encode("utf-8")  # Reject lone surrogates rather than counting repaired text.
        return text
    except (TypeError, ValueError, RecursionError, OverflowError):
        raise SerializationError(
            "Response must contain finite JSON values and valid Unicode."
        ) from None


def _utf8(text: str) -> bytes:
    if not isinstance(text, str):
        raise SerializationError("Response text must be a Unicode string.")
    try:
        return text.encode("utf-8")
    except UnicodeError:
        raise SerializationError("Response text must contain valid Unicode.") from None


_encoding: Encoding | None = None
_encoding_lock = threading.Lock()


def _load_encoding() -> Encoding:
    # Parse package bytes directly: even tiktoken.load's local-file helper can
    # write to a user's cache. There is no cache directory or network fallback.
    import tiktoken

    assets = resources.files(__package__).joinpath("_tokenizer")
    config_bytes = assets.joinpath("o200k_base.json").read_bytes()
    if hashlib.sha256(config_bytes).hexdigest() != CONFIG_SHA256:
        raise ValueError("configuration checksum mismatch")
    config = json.loads(config_bytes)
    vocabulary = assets.joinpath("o200k_base.tiktoken").read_bytes()
    if hashlib.sha256(vocabulary).hexdigest() != VOCABULARY_SHA256:
        raise ValueError("vocabulary checksum mismatch")
    ranks = {}
    for line in vocabulary.splitlines():
        token, rank = line.split()
        ranks[base64.b64decode(token, validate=True)] = int(rank)
    return tiktoken.Encoding(
        name=config["name"],
        pat_str=config["pat_str"],
        special_tokens=config["special_tokens"],
        mergeable_ranks=ranks,
    )


def _get_encoding() -> Encoding:
    global _encoding
    if _encoding is None:
        # functools.cache alone can construct multiple copies on concurrent
        # first calls. The vocabulary/native tables belong once per process.
        with _encoding_lock:
            if _encoding is None:
                try:
                    _encoding = _load_encoding()
                except Exception:
                    raise TokenizerUnavailable(
                        "MCP tokenizer unavailable; verify packaged assets."
                    ) from None
    return _encoding


def count_tokens(text: str) -> int:
    """Count ordinary text with the frozen reference encoding, including specials."""
    _utf8(text)
    encoding = _get_encoding()
    try:
        return len(encoding.encode_ordinary(text))
    except Exception:
        raise TokenizerUnavailable("MCP tokenizer could not count response text.") from None


@dataclass(frozen=True)
class Budget:
    token_budget: int = DEFAULT_TOKENS

    def __post_init__(self) -> None:
        if type(self.token_budget) is not int or not MIN_TOKENS <= self.token_budget <= MAX_TOKENS:
            raise InvalidBudget(
                f"token_budget must be an integer from {MIN_TOKENS} through {MAX_TOKENS}."
            )

    @property
    def token_limit(self) -> int:
        return self.token_budget

    @property
    def byte_limit(self) -> int:
        return BYTES_PER_TOKEN * self.token_budget

    def fits_text(self, text: str) -> bool:
        """Check both exact limits; an over-byte result need not be tokenized."""
        return len(_utf8(text)) <= self.byte_limit and count_tokens(text) <= self.token_limit

    def fits(self, value: Any) -> bool:
        return self.fits_text(serialize(value))
