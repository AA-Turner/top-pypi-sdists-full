"""The words matrx-ai itself puts in front of a model, by key — host-supplied, with standalone defaults.

Standalone defaults; on the AI Matrx platform the host supplies these from System Context items.
The defaults live in ``platform_texts.json`` (package data, read through ``importlib.resources``) and are
the bare-install fallback, never the platform's source. The host installs ONE resolver with
``matrx_ai.configure(platform_texts=...)``: ``Callable[[str], str | None]`` (synchronous; return ``None``
for a key it has no usable text for, and the default is used). Named ``{slots}`` are filled in one pass,
so a filled value is never re-scanned and other braces are left alone.
"""

from __future__ import annotations

import json
import re
from collections.abc import Callable
from functools import cache
from importlib import resources

PlatformTextResolver = Callable[[str], "str | None"]

_resolver: PlatformTextResolver | None = None
_SLOT = re.compile(r"\{([a-z_]+)\}")


def configure_platform_texts(resolver: PlatformTextResolver | None) -> None:
    """Install (or, with ``None``, remove) the host's platform-text resolver."""
    global _resolver
    _resolver = resolver


@cache
def default_platform_texts() -> dict[str, str]:
    """The standalone defaults, keyed (the ``_about`` note excluded)."""
    raw = resources.files("matrx_ai.config").joinpath("platform_texts.json").read_text(encoding="utf-8")
    return {k: v for k, v in json.loads(raw).items() if not k.startswith("_")}


def platform_text(key: str, **fill: str) -> str:
    """The text for ``key``: the host's when it supplies usable text, else the packaged default."""
    defaults = default_platform_texts()
    if key not in defaults:
        raise KeyError(f"unknown platform text {key!r}")
    text = _resolver(key) if _resolver is not None else None
    if not isinstance(text, str) or not text.strip():
        text = defaults[key]
    return _SLOT.sub(lambda m: fill.get(m.group(1), m.group(0)), text) if fill else text
