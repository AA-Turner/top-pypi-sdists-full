# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2026 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
import functools
import json
import re
from typing import Any, Optional

from .base64_helper import decode_base64
from .comet_api_key import parse_api_key

HIDDEN = "<HIDDEN>"

# The minimum own-key length matched anywhere, so a blank or toy key can't blank out unrelated text.
_MIN_OWN_KEY_LENGTH = 8

# 25 alphanumerics with an optional "sa-" prefix (service accounts), or the deprecated 64-alphanumeric form.
_KEY_SHAPE = re.compile(
    r"(?<![A-Za-z0-9])((?:sa-)?[A-Za-z0-9]{25}|[A-Za-z0-9]{64})(?![A-Za-z0-9])"
)

# A smart-key "*<base64>" suffix right after a key; it counts only if it decodes to the smart-key payload.
_SMART_KEY_SUFFIX = re.compile(r"\*([A-Za-z0-9+/]+=*)")


def mask_text(text: str, api_key: Optional[str]) -> str:
    """Masks the experiment's own key and self-identifying keys ("sa-" and smart keys).

    Other key-shaped tokens are left alone: without the key store, they can't be told apart from asset ids.
    """
    own_key = _raw_key(api_key)
    parts = []
    copied_up_to = 0
    for match in _KEY_SHAPE.finditer(text):
        # A token inside a smart-key suffix that was already masked belongs to that key.
        if match.start() < copied_up_to:
            continue
        key = match.group(1)
        suffix_end = _smart_key_suffix_end(text, match.end())
        if key == own_key or key.startswith("sa-") or suffix_end >= 0:
            parts.append(text[copied_up_to : match.start()])
            parts.append(HIDDEN)
            # A non-smart "*suffix" is not part of the key ("<key>*scale"), so it stays and is scanned like any text.
            copied_up_to = suffix_end if suffix_end >= 0 else match.end()
    parts.append(text[copied_up_to:])
    masked = "".join(parts)

    if own_key is not None and len(own_key) >= _MIN_OWN_KEY_LENGTH:
        masked = masked.replace(own_key, HIDDEN)
    return masked


def mask_value(value: Any, api_key: Optional[str]) -> Any:
    """Masks strings in a value, recursing into lists, tuples and dict values."""
    if isinstance(value, str):
        return mask_text(value, api_key)
    # Rebuilt as plain list/tuple: subclasses such as namedtuples can't be built from an iterable.
    if isinstance(value, list):
        return [mask_value(item, api_key) for item in value]
    if isinstance(value, tuple):
        return tuple(mask_value(item, api_key) for item in value)
    if isinstance(value, dict):
        return {key: mask_value(item, api_key) for key, item in value.items()}
    return value


@functools.lru_cache(maxsize=8)
def _raw_key(api_key: Optional[str]) -> Optional[str]:
    if not isinstance(api_key, str) or not api_key:
        return None
    try:
        parsed = parse_api_key(api_key)
    except Exception:
        return api_key
    return parsed.short_api_key if parsed is not None else None


def _smart_key_suffix_end(text: str, key_end: int) -> int:
    """End of a smart-key suffix starting at key_end, or -1 when there is none."""
    suffix = _SMART_KEY_SUFFIX.match(text, key_end)
    return (
        suffix.end()
        if suffix is not None and _is_smart_key_payload(suffix.group(1))
        else -1
    )


def _is_smart_key_payload(base64_data: str) -> bool:
    try:
        attributes = json.loads(decode_base64(base64_data))
    except Exception:
        return False
    return isinstance(attributes, dict) and "baseUrl" in attributes
