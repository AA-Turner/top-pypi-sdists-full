"""Error types for the version-routed UDF path.

Three distinct failure modes, deliberately different classes so a notebook can
tell them apart:

  * :class:`UDFRegistrationError` — the UDF itself cannot be shipped to a
    version-mismatched engine (a live connection in a closure, a nested
    closure, a non-picklable capture). Raised at *registration* time, never at
    execution time.
  * :class:`UDFSidecarError` — the sidecar was reachable but failed to build
    the command (bad return type, source that will not ``exec``). Carries the
    sidecar's own traceback.
  * :class:`UDFUnsupportedError` — the operation is out of scope on a
    mismatched engine (the inline family: ``mapInPandas`` and friends).
"""

from __future__ import annotations

import textwrap
from typing import Any, Dict


class UDFRegistrationError(ValueError):
    """An un-shippable UDF, detected at registration time."""


class UDFSidecarError(RuntimeError):
    """The sidecar reported a failure while building the UDF command."""


class UDFUnsupportedError(NotImplementedError):
    """The requested operation is not supported on a version-mismatched engine."""


def format_sidecar_error(resp: Dict[str, Any]) -> UDFSidecarError:
    """Turn a sidecar error response into a readable local exception.

    The sidecar runs in a different interpreter, so its traceback is text, not
    a live frame chain. Indent it under an explicit header so it does not merge
    into the local traceback and confuse the reader.
    """
    error = resp.get("error") or "unknown sidecar failure"
    parts = [f"UDF sidecar failed to build this function: {error}"]
    remote_tb = resp.get("traceback")
    if remote_tb:
        parts.append("Sidecar traceback:")
        parts.append(textwrap.indent(str(remote_tb).rstrip("\n"), "    "))
    return UDFSidecarError("\n".join(parts))
