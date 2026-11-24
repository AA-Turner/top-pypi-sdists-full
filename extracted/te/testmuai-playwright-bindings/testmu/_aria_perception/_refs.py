"""Portable element identity: Playwright aria refs <-> integer handles.

A handle is a synthetic integer carried in the existing
``backend_dom_node_id`` field, so every structure keyed by that field keeps
working unchanged. Encoding (stateless, reversible)::

    PORTABLE_TAG | (frame_seq << 32) | element_number
    "e17"   -> PORTABLE_TAG | (0 << 32) | 17
    "f3e17" -> PORTABLE_TAG | (3 << 32) | 17

CDP backend node ids never reach bit 48, so the two id spaces cannot collide.

Options of a native ``<select>`` have no aria ref of their own (they have no
box while the select is closed). Each gets an OPTION handle that names the
select's ref plus the option's position among the select's visible options
(the snapshot's order; hidden options are left out)::

    PORTABLE_TAG | OPTION_TAG | (frame_seq << 32) | (option_index << 20) | select_number
    option 2 of "f3e17" -> PORTABLE_TAG | OPTION_TAG | (3 << 32) | (2 << 20) | 17

``OPTION_TAG`` is bit 49 (bits 32-47 are the frame seq); the value stays
below 2**53, so it survives a JSON/JS number. Limits: select number < 2**20,
option index < 2**12 (larger ones keep the select's own handle). Every
non-option handle is encoded exactly as above. For an option handle,
``handle_to_aria_ref`` names the select (the ref'd anchor),
``ref_locator`` is the option element and ``anchor_locator`` the select.
"""
from __future__ import annotations

import re
from typing import Any

PORTABLE_TAG: int = 1 << 48

_REF_RE = re.compile(r"^(?:f(\d+))?e(\d+)$")
OPTION_TAG: int = 1 << 49

_ELEMENT_MASK = (1 << 32) - 1
_FRAME_MASK = (1 << 16) - 1
_OPTION_SELECT_BITS = 20
_OPTION_SELECT_MASK = (1 << _OPTION_SELECT_BITS) - 1
_OPTION_INDEX_MASK = (1 << 12) - 1


def aria_ref_to_handle(ref: str) -> int:
    m = _REF_RE.match(str(ref).strip())
    if not m:
        raise ValueError(f"not an aria ref: {ref!r}")
    seq = int(m.group(1) or 0)
    num = int(m.group(2))
    if seq > _FRAME_MASK or num > _ELEMENT_MASK:
        raise ValueError(f"aria ref out of range: {ref!r}")
    return PORTABLE_TAG | (seq << 32) | num


def is_portable_handle(handle: object) -> bool:
    return (
        isinstance(handle, int)
        and not isinstance(handle, bool)
        and handle >= 0
        and bool(handle & PORTABLE_TAG)
    )


def is_option_handle(handle: object) -> bool:
    """True for a native ``<select>`` option handle (see module doc)."""
    return is_portable_handle(handle) and bool(handle & OPTION_TAG)


def option_handle(select_handle_or_ref: int | str, index: int) -> int | None:
    """The handle of option ``index`` (its ``role=option`` position) of the
    select with this handle/ref; None when out of the encodable range."""
    select_handle = (
        aria_ref_to_handle(select_handle_or_ref)
        if isinstance(select_handle_or_ref, str) else select_handle_or_ref
    )
    if not is_portable_handle(select_handle) or is_option_handle(select_handle):
        raise ValueError(f"not a select handle: {select_handle_or_ref!r}")
    num = select_handle & _ELEMENT_MASK
    if num > _OPTION_SELECT_MASK or not 0 <= index <= _OPTION_INDEX_MASK:
        return None
    seq = (select_handle >> 32) & _FRAME_MASK
    return PORTABLE_TAG | OPTION_TAG | (seq << 32) | (index << _OPTION_SELECT_BITS) | num


def option_parts(handle: int) -> tuple[int, int]:
    """``(select_handle, option_index)`` of an option handle."""
    if not is_option_handle(handle):
        raise ValueError(f"not an option handle: {handle!r}")
    seq = (handle >> 32) & _FRAME_MASK
    num = handle & _OPTION_SELECT_MASK
    index = (handle >> _OPTION_SELECT_BITS) & _OPTION_INDEX_MASK
    return PORTABLE_TAG | (seq << 32) | num, index


def handle_to_aria_ref(handle: int) -> str:
    """The aria ref of the handle's element (of its select, for an option)."""
    if not is_portable_handle(handle):
        raise ValueError(f"not a portable handle: {handle!r}")
    if handle & OPTION_TAG:
        handle = option_parts(handle)[0]
    seq = (handle >> 32) & _FRAME_MASK
    num = handle & _ELEMENT_MASK
    return f"f{seq}e{num}" if seq else f"e{num}"


def frame_id_for_ref(ref: str) -> str:
    m = _REF_RE.match(str(ref).strip())
    if not m or not m.group(1):
        return ""
    return f"f{m.group(1)}"


def _as_ref(handle_or_ref: int | str) -> str:
    if isinstance(handle_or_ref, str):
        return handle_or_ref.strip()
    return handle_to_aria_ref(handle_or_ref)


def ref_locator(page, handle_or_ref: int | str):
    """``page.locator("aria-ref=<ref>")`` — resolves across iframes by itself
    (the ``f<seq>`` prefix routes to the frame). An option handle yields its
    ``<option>`` element (``role=option`` order, as in the snapshot)."""
    if is_option_handle(handle_or_ref):
        _, index = option_parts(handle_or_ref)
        return page.locator(
            f"aria-ref={handle_to_aria_ref(handle_or_ref)} >> internal:role=option >> nth={index}")
    return page.locator(f"aria-ref={_as_ref(handle_or_ref)}")


def anchor_locator(page, handle_or_ref: int | str):
    """The ref'd element carrying the handle's geometry: the element itself,
    or the ``<select>`` for an option handle (a closed select's options have
    no box)."""
    if is_option_handle(handle_or_ref):
        return page.locator(f"aria-ref={handle_to_aria_ref(handle_or_ref)}")
    return ref_locator(page, handle_or_ref)


async def call_on_ref(page, handle: int, fn_decl: str, arg: Any = None, *, timeout_ms: int = 1000):
    """Run a CDP-style `function(arg){ this... }` declaration against the element.
    Builds "(el, arg) => (" + fn_decl + ").call(el, arg)" in Python; returns the JSON value.

    Raises ``ValueError("node not found")`` at once when the ref resolves to
    nothing (a stale ref), instead of waiting out ``timeout_ms``."""
    locator = ref_locator(page, handle)
    if await locator.count() == 0:
        raise ValueError("node not found")
    expression = "(el, arg) => (" + fn_decl.strip() + ").call(el, arg)"
    return await locator.evaluate(expression, arg, timeout=timeout_ms)
