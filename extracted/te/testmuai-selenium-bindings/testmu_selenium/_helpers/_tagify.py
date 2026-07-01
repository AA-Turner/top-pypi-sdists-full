"""Mobile tagify JS script — tags DOM nodes for vision/OCR queries.

Vendored stub. The actual mobile tagify script is loaded at runtime when available
and pushed into ``utils.constants.MOBILE_TAGIFY_SCRIPT`` via ``set_mobile_tagify_script``.

Strategy:
- Best-effort import from ``utils.constants`` when running inside the host runtime.
- Fallback to ``None`` when running standalone bindings (HyperExecute / CI).
  The Heal methods guard mobile-tagify branches with ``if self.mobile_tagify:``
  which is falsy for both ``None`` and empty string. ``None`` is the correct sentinel.

TODO: If a future phase needs richer tagging in standalone mode, vendor the JS body here
(or load it from a sibling .js resource via ``importlib.resources``).
"""
from __future__ import annotations

try:
    # Try to load from the host runtime when available.
    from utils.constants import get_mobile_tagify_script  # type: ignore  # host-runtime module; absent in standalone mode

    MOBILE_TAGIFY_SCRIPT = get_mobile_tagify_script() or None
except Exception:
    # Standalone fallback — None is the sentinel for "no mobile tagify".
    # Heal methods guard with ``if self.mobile_tagify:``; None is falsy.
    MOBILE_TAGIFY_SCRIPT = None

__all__ = ["MOBILE_TAGIFY_SCRIPT"]
