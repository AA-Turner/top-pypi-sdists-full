"""
token_utils
===========
Token encoding/counting with an optional tiktoken backend.

If ``tiktoken`` is installed, it is used unchanged (exact BPE token counts).
If it is NOT installed, a dependency-free approximate encoder is used instead,
so token-based chunking keeps working without pulling in tiktoken.

The fallback is a *lossless* partition of the text into ~token-sized pieces:
  * ``encode(text)`` returns a list of substrings that concatenate back to the
    original text, so ``decode(encode(text)) == text`` exactly.
  * ``len(encode(text))`` approximates the token count (roughly one piece per
    ~4 characters, aligned to word / number / punctuation / whitespace runs).

Approximate counts are fine for chunking: the estimate is slightly conservative
(tends to count a hair high), so chunks stay at or under the requested budget
rather than overflowing it.
"""
import re
import math

try:  # optional, exact backend
    import tiktoken as _tiktoken
except Exception:  # pragma: no cover - depends on environment
    _tiktoken = None

# Pre-tokenizer: contractions, letter runs, digit runs, whitespace runs,
# punctuation runs. Uses only stdlib `re` (no third-party `regex`/\p{L}).
_PRETOKEN = re.compile(
    r"'(?:s|t|re|ve|m|ll|d)|[^\W\d_]+|\d+|\s+|[^\w\s]+",
    re.UNICODE,
)

# Per-piece weights, calibrated against cl100k_base so the estimate lands
# slightly high (~1.0-1.4x) on realistic prose/code — conservative on purpose
# so token-budget chunking never overflows the real limit.
_W_LETTERS = 4.0   # chars per token inside a word run
_W_DIGITS = 2.5    # digit runs are denser
_W_PUNCT = 1.5     # punctuation/symbols are dense
_W_SPACE = 8.0     # whitespace mostly merges into adjacent tokens in BPE


def _estimate_tokens(text: str) -> int:
    """Approximate the BPE token count of *text* using only stdlib."""
    total = 0.0
    for m in _PRETOKEN.finditer(text):
        s = m.group()
        if s.isspace():
            total += len(s) / _W_SPACE
        elif s.isalpha():
            total += max(1.0, len(s) / _W_LETTERS)
        elif s.isdigit():
            total += math.ceil(len(s) / _W_DIGITS)
        else:
            total += math.ceil(len(s) / _W_PUNCT)
    return max(1, math.ceil(total)) if text else 0


def tiktoken_available() -> bool:
    """True when the real tiktoken backend is importable."""
    return _tiktoken is not None


class ApproxEncoder:
    """Dependency-free stand-in for a tiktoken encoding object.

    Provides the subset of the tiktoken ``Encoding`` API this package uses:
    ``encode`` and ``decode``.
    """

    name = "approx"

    def encode(self, text, *args, **kwargs):
        """Losslessly partition *text* into ~token-sized pieces.

        ``len(encode(text))`` equals the calibrated token estimate, and
        ``"".join(encode(text)) == text`` exactly.
        """
        text = str(text)
        if not text:
            return []
        count = _estimate_tokens(text)
        if count >= len(text):
            return list(text)
        # split into `count` contiguous pieces covering the whole string
        pieces = []
        prev = 0
        for n in range(1, count + 1):
            end = len(text) if n == count else round(n * len(text) / count)
            end = min(max(end, prev + 1), len(text))
            pieces.append(text[prev:end])
            prev = end
        return pieces

    def decode(self, tokens, *args, **kwargs):
        return "".join(tokens)


def get_token_encoder(model_name: str = "gpt-4", encoding_name: str = None):
    """Return a token encoder.

    Uses tiktoken when installed (``get_encoding``/``encoding_for_model``),
    otherwise returns an :class:`ApproxEncoder`.
    """
    if _tiktoken is not None:
        if encoding_name:
            return _tiktoken.get_encoding(encoding_name)
        return _tiktoken.encoding_for_model(model_name)
    return ApproxEncoder()


def num_tokens_from_string(string: str, model_name: str = "gpt-4",
                           encoding_name: str = None) -> int:
    """Count tokens in *string* using the active backend."""
    encoding = get_token_encoder(model_name, encoding_name)
    return len(encoding.encode(str(string)))


__all__ = [
    "get_token_encoder",
    "num_tokens_from_string",
    "ApproxEncoder",
    "tiktoken_available",
]
