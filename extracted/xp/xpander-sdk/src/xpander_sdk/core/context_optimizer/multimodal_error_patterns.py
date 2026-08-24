"""Provider-error classification for rejected multimodal input.

Sibling of ``error_patterns.py``. Used by the worker and the agent gateway to
degrade-retry once without attachments when the provider 400s on image/file
content ("Unknown model error" today). Patterns are deliberately tight and
must NOT overlap the context-overflow patterns - an overflow retry without
attachments would mask the real problem.
"""

import re

_MULTIMODAL_INPUT_PATTERNS = [
    re.compile(r"invalid_multimodal_input", re.IGNORECASE),
    re.compile(r"does not support image", re.IGNORECASE),
    re.compile(r"unsupported image", re.IGNORECASE),
    re.compile(r"image input is not supported", re.IGNORECASE),
    re.compile(r"image content is not supported", re.IGNORECASE),
    re.compile(r"messages with image content", re.IGNORECASE),
    re.compile(r"no endpoints found that support image input", re.IGNORECASE),
    re.compile(r"invalid base64", re.IGNORECASE),
    re.compile(r"could not process image", re.IGNORECASE),
    re.compile(r"unsupported media type", re.IGNORECASE),
    re.compile(r"invalid media type", re.IGNORECASE),
    re.compile(r"image exceeds \d+ *[mk]b", re.IGNORECASE),
    re.compile(r"unsupported (?:file|document) (?:type|format)", re.IGNORECASE),
    re.compile(r"file content is not supported", re.IGNORECASE),
    re.compile(r"document.{0,40}not supported", re.IGNORECASE),
    re.compile(r"vision is not (?:supported|enabled)", re.IGNORECASE),
    re.compile(
        r"model does not support (?:vision|multimodal|attachments|files)", re.IGNORECASE
    ),
    # Audio/video rejections read differently per provider, and a turn that carries
    # only an .mp3 would otherwise fail hard instead of degrading to its transcript.
    re.compile(
        r"audio (?:input )?is (?:currently )?(?:un|not )supported", re.IGNORECASE
    ),
    re.compile(r"does not support audio", re.IGNORECASE),
    re.compile(r"audio content is not supported", re.IGNORECASE),
    re.compile(r"unsupported audio (?:type|format)", re.IGNORECASE),
    re.compile(
        r"video (?:input )?is (?:currently )?(?:un|not )supported", re.IGNORECASE
    ),
    re.compile(r"does not support video", re.IGNORECASE),
    re.compile(r"unsupported video (?:type|format)", re.IGNORECASE),
    re.compile(r"invalid_?(?:audio|video)_?(?:input|format)", re.IGNORECASE),
]


def is_multimodal_input_error(exc: BaseException) -> bool:
    """Return True when *exc* looks like the provider rejected image/file input."""
    try:
        text = str(exc)
    except Exception:
        return False
    if not text:
        return False
    return any(pat.search(text) for pat in _MULTIMODAL_INPUT_PATTERNS)
