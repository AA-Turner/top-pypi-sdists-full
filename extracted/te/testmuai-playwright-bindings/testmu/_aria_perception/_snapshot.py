"""The single home of Playwright's AI snapshot call.

Playwright >= 1.59 exposes it publicly as ``page.aria_snapshot(mode="ai")``;
1.57/1.58 only have the private ``snapshotForAI`` page-channel command. This
module is the only place the private call exists.
"""
from __future__ import annotations

import inspect


class PlaywrightInternalsError(RuntimeError):
    """The installed Playwright lacks a private call this package relies on."""


def internals_error(call: str, exc: BaseException) -> PlaywrightInternalsError | None:
    """The clear error for ``exc`` when it means the private ``call`` is
    missing or changed (not an ordinary page error); None otherwise."""
    if not (isinstance(exc, (AttributeError, TypeError)) or "Unknown scheme" in str(exc)):
        return None
    try:
        from importlib.metadata import version
        installed = version("playwright")
    except Exception:  # noqa: BLE001
        installed = "(unknown version)"
    return PlaywrightInternalsError(
        f"Firefox perception needs Playwright 1.57–1.58 internals; installed "
        f"Playwright {installed} does not provide {call}"
    )


async def snapshot_for_ai(page, *, timeout_ms: int = 10_000) -> str:
    """Full AI snapshot text (iframes inlined, refs [ref=eN]/[ref=fKeN]).
    >=1.59: page.aria_snapshot(mode="ai", timeout=...)  (detect via inspect.signature)
    else:   (await page._impl_obj._channel.send_return_as_dict("snapshotForAI", None, {"timeout": timeout_ms}))["full"]"""
    public = getattr(page, "aria_snapshot", None)
    if public is not None:
        try:
            has_mode = "mode" in inspect.signature(public).parameters
        except (TypeError, ValueError):
            has_mode = False
        if has_mode:
            return await public(mode="ai", timeout=timeout_ms)
    try:
        channel = page._impl_obj._channel
        result = await channel.send_return_as_dict(
            "snapshotForAI", None, {"timeout": timeout_ms},
        )
    except Exception as e:
        err = internals_error("snapshotForAI", e)
        if err is not None:
            raise err from e
        raise
    return (result or {}).get("full") or ""
