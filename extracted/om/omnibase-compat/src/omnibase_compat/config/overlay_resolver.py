# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

# COMPAT_MIGRATION_TARGET: omnibase_core.runtime.config (ModelRuntimeConfig / runtime/overlay)
# COMPAT_REMOVAL_DATE: 2026-09-01

"""Contract/overlay config resolver for ``omnibase_compat`` (OMN-13564).

This is the zero-upstream-dep stand-in for the canonical overlay system
(``ModelRuntimeConfig`` + ``runtime/overlay/`` in ``omnibase_core``). compat
must depend on **pydantic + typing-extensions only**, so this resolver:

- parses the overlay document with the **standard library** ``json`` module
  (no ``pyyaml`` runtime dependency — it is dev-only here),
- validates it into frozen pydantic models,
- supports ``${env.VAR}`` interpolation so the declared value is the authority
  and an environment variable may override it at resolution time, and
- fails **closed**: a missing/unparseable overlay or a missing required field
  raises rather than silently substituting a default.

The endpoint URL and the autowire strict-mode flag that previously lived as a
hardcoded Python literal (``_LINEAR_API_URL``) and a bare ``os.environ`` read
(``AUTOWIRE_STRICT``) now resolve through this surface. The overlay document
(``overlays/compat_runtime_overlay.json``) is the contract surface; the URL and
the flag never reappear as Python literals or raw env reads.
"""

from __future__ import annotations

import json
import os
import re
from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

_OVERLAY_FILENAME: str = "compat_runtime_overlay.json"
_OVERLAY_PATH: Path = Path(__file__).parent / "overlays" / _OVERLAY_FILENAME

# ``${env.VAR}`` interpolation token. The whole value must be a single token —
# partial / mixed-literal interpolation is intentionally unsupported so a value
# is either a literal authority or fully env-sourced, never a silent splice.
_ENV_TOKEN: re.Pattern[str] = re.compile(r"^\$\{env\.([A-Z0-9_]+)\}$")


class ModelEndpointOverlay(BaseModel):
    """A single declared service endpoint resolved from the overlay."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    url: str = Field(..., description="Service endpoint URL (contract-declared authority).")


class ModelAutowireOverlay(BaseModel):
    """Autowire layer tunables resolved from the overlay.

    ``strict_mode_raw`` carries the post-interpolation raw string for the
    ``AUTOWIRE_STRICT`` flag. The literal-``"1"``-only semantic lives at the
    call site (:func:`omnibase_compat.env.is_strict_mode`), not here.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    strict_mode_raw: str | None = Field(
        default=None,
        description=(
            "Post-interpolation raw value of the autowire strict-mode flag. "
            "``None`` when the source env var is unset; otherwise the exact "
            "string the operator supplied."
        ),
    )


class ModelCompatRuntimeOverlay(BaseModel):
    """Top-level overlay document for ``omnibase_compat``.

    Frozen + ``extra='forbid'`` so an unknown overlay key fails loudly at parse
    time instead of being silently ignored.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    schema_version: str = Field(..., description="Overlay schema version.")
    endpoints: dict[str, ModelEndpointOverlay] = Field(
        ...,
        description="Declared service endpoints keyed by logical name.",
    )
    autowire: ModelAutowireOverlay = Field(
        ...,
        description="Autowire layer tunables.",
    )


class OverlayResolutionError(RuntimeError):
    """Raised when the overlay cannot be located, parsed, or required-resolved."""


def _interpolate(value: object) -> object:
    """Resolve a single ``${env.VAR}`` token against the process environment.

    A bare ``${env.VAR}`` value resolves to ``os.environ.get("VAR")`` — i.e.
    ``None`` when the variable is unset (fail-open is intentional only for
    *optional* tunables; required fields fail closed at the model layer). Any
    other value is returned unchanged. Non-string values pass through.
    """
    if not isinstance(value, str):
        return value
    match = _ENV_TOKEN.match(value)
    if match is None:
        return value
    return os.environ.get(match.group(1))


def _interpolate_tree(node: object) -> object:
    """Recursively interpolate ``${env.VAR}`` tokens through a parsed JSON tree."""
    if isinstance(node, dict):
        return {key: _interpolate_tree(val) for key, val in node.items()}
    if isinstance(node, list):
        return [_interpolate_tree(item) for item in node]
    return _interpolate(node)


def _load_raw_overlay(overlay_path: Path) -> dict[str, object]:
    """Read + JSON-parse the overlay document. Fails closed on any problem."""
    try:
        text = overlay_path.read_text(encoding="utf-8")
    except OSError as exc:
        raise OverlayResolutionError(
            f"compat overlay not readable at {overlay_path}: {exc}"
        ) from exc
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError as exc:
        raise OverlayResolutionError(
            f"compat overlay at {overlay_path} is not valid JSON: {exc}"
        ) from exc
    if not isinstance(parsed, dict):
        raise OverlayResolutionError(
            f"compat overlay at {overlay_path} must be a JSON object, got {type(parsed).__name__}"
        )
    # The ``_comment`` documentation key is not part of the typed model.
    parsed.pop("_comment", None)
    return parsed


def load_overlay(overlay_path: Path | None = None) -> ModelCompatRuntimeOverlay:
    """Load, interpolate, and validate the compat runtime overlay.

    Args:
        overlay_path: Override the default packaged overlay location (tests).

    Returns:
        The validated, env-interpolated overlay document.

    Raises:
        OverlayResolutionError: overlay missing/unreadable/invalid JSON.
        pydantic.ValidationError: overlay shape does not match the model.
    """
    path = overlay_path or _OVERLAY_PATH
    raw = _load_raw_overlay(path)
    interpolated = _interpolate_tree(raw)
    return ModelCompatRuntimeOverlay.model_validate(interpolated)


@lru_cache(maxsize=1)
def _cached_endpoint_url(name: str) -> str:
    """Cached endpoint resolution for the packaged overlay (stable per process).

    Only the packaged-default path is cached. The autowire flag is read on
    every call (see :func:`resolve_autowire_strict_raw`) so tests and operators
    can toggle it without a process restart; an endpoint URL has no such
    requirement and benefits from a single parse.
    """
    overlay = load_overlay()
    endpoint = overlay.endpoints.get(name)
    if endpoint is None:
        raise OverlayResolutionError(
            f"compat overlay declares no endpoint named {name!r}; "
            f"known endpoints: {sorted(overlay.endpoints)}"
        )
    return endpoint.url


def resolve_endpoint_url(name: str, *, overlay_path: Path | None = None) -> str:
    """Resolve a declared endpoint URL from the overlay (fail-closed).

    Args:
        name: Logical endpoint key (e.g. ``"project_tracker_linear"``).
        overlay_path: Override the packaged overlay (tests); bypasses the cache.

    Returns:
        The resolved endpoint URL.

    Raises:
        OverlayResolutionError: no endpoint with that name is declared.
    """
    if overlay_path is not None:
        overlay = load_overlay(overlay_path)
        endpoint = overlay.endpoints.get(name)
        if endpoint is None:
            raise OverlayResolutionError(
                f"compat overlay declares no endpoint named {name!r}; "
                f"known endpoints: {sorted(overlay.endpoints)}"
            )
        return endpoint.url
    return _cached_endpoint_url(name)


def resolve_autowire_strict_raw(*, overlay_path: Path | None = None) -> str | None:
    """Resolve the post-interpolation raw value of the autowire strict flag.

    Read on every call (no caching) so the underlying env var can be toggled
    at runtime. Returns ``None`` when the source env var is unset.

    Args:
        overlay_path: Override the packaged overlay (tests).

    Returns:
        The raw flag string, or ``None`` when unset.
    """
    overlay = load_overlay(overlay_path)
    return overlay.autowire.strict_mode_raw


__all__: list[str] = [
    "ModelAutowireOverlay",
    "ModelCompatRuntimeOverlay",
    "ModelEndpointOverlay",
    "OverlayResolutionError",
    "load_overlay",
    "resolve_autowire_strict_raw",
    "resolve_endpoint_url",
]
