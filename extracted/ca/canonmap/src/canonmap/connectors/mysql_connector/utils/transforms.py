# src/canonmap/connectors/mysql_connector/utils/transforms.py

from __future__ import annotations

import re
from typing import Optional


def to_initialism(text: str | None) -> str | None:
    if not text:
        return None
    parts = re.findall(r"[A-Za-z]+", text)
    return "".join(p[0].upper() for p in parts) if parts else None


def to_phonetic(text: str | None) -> str | None:
    if not text:
        return None
    try:
        from metaphone import doublemetaphone
    except ImportError:
        raise RuntimeError("metaphone package not installed")
    p, s = doublemetaphone(text)
    return p or s or None


def to_soundex(text: str | None) -> str | None:
    if not text:
        return None
    try:
        import jellyfish
    except ImportError:
        raise RuntimeError("jellyfish package not installed for SOUNDEX")
    return jellyfish.soundex(text)


