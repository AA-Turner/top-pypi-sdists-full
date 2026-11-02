"""The ONE place matrx-files learns which organization a request was admitted with.

Why this module exists (production outage, 2026-09-19, `common-docs/projects/
acquisition-frontier/own-files/VERIFICATION.md` §15/§16): every upload to
`files.matrxserver.com` returned ``400 matrx-files: this write carries no
organization`` even though the browser sent a correct ``X-Organization-Id`` and
``AuthMiddleware`` VERIFIED it against real membership. Nobody could attach a
source to any Masterwork.

The seam that broke:

* ``AuthMiddleware`` pins the verified organization onto the **matrx-connect**
  ``AppContext``.
* ``SyncEngine._carried_organization_id`` read it from the **matrx-utils**
  ambient context (``matrx_utils.ctx.get_active_organization_id``).
* Those two are joined only when a host calls ``matrx_utils.configure_context``.
  ``aidream`` does (``aidream/package_integration.py``). The matrx-files
  **standalone** app — the service the browser actually talks to — never did, so
  ``get_active_context()`` returned ``None``, ``get_active_organization_id()``
  returned ``None`` for every request, and the write funnel refused.

Before ``ce44577124`` (2026-09-17) that same blind read fell through to
a per-user saved-organization lookup, so the standalone service had been
silently filing every upload into an organization picked for the owner instead of the
tenant the person was working in. The refusal did not create the defect; it
made an already-wrong answer visible.

**The class, and the rule this module encodes:** the organization of a request is
resolved ONCE, at the API edge, from the admitted request itself — never
re-derived deep in a write path from an ambient seam or a metadata dict that
some other layer may or may not have filled. Every source below is a *reading of
the same admitted request*; none of them defaults, guesses, or falls back to an
organization picked for the owner.
"""

from __future__ import annotations

__all__ = [
    "admitted_organization_id",
    "context_seam_status",
]


def _from_matrx_utils_context() -> str | None:
    """The organization on the host-configured ambient context, if any.

    This is the seam ``aidream`` wires with ``configure_context(try_get_app_context)``.
    It is checked FIRST so a host that deliberately scopes a background task to
    one organization (``set_manual_context``) keeps winning.
    """
    try:
        from matrx_utils.ctx import get_active_organization_id
    except Exception:  # pragma: no cover - matrx_utils is a hard dependency
        return None
    try:
        carried = get_active_organization_id()
    except Exception:
        return None
    return str(carried) if carried else None


def _from_matrx_connect_context() -> str | None:
    """The organization the auth boundary ADMITTED for this request.

    ``AuthMiddleware._resolve_organization`` verifies ``X-Organization-Id`` (or
    the JWT's organization claim) against real membership and pins the result on
    the ``AppContext`` as ``organization_id`` with
    ``organization_admission="verified"``. A request that named an organization
    it could not be admitted to never reaches route code at all — the middleware
    answers it — so anything we read here is already verified.

    Reading it directly means matrx-files no longer depends on a host having
    joined the two context systems together.
    """
    try:
        from matrx_connect import get_app_context
    except Exception:
        return None
    try:
        ctx = get_app_context()
    except Exception:
        return None
    if ctx is None:
        return None
    admitted = getattr(ctx, "organization_id", None)
    return str(admitted) if admitted else None


def admitted_organization_id() -> str | None:
    """The one organization this request was admitted with, or ``None``.

    ``None`` means the request genuinely named no organization — NOT that a
    lookup failed and not "use an organization picked for the owner". Callers refuse on it.
    """
    return _from_matrx_utils_context() or _from_matrx_connect_context()


def context_seam_status() -> dict[str, bool]:
    """What organization seams this PROCESS can actually read — for boot guards.

    A host that wires neither seam cannot carry an organization into any write,
    and every org-scoped upload it serves will refuse at request time. A boot
    guard reads this and says so at startup instead of letting the first person
    to drag a file discover it.
    """
    matrx_utils_wired = False
    try:
        from matrx_utils import ctx as _ctx

        matrx_utils_wired = getattr(_ctx, "_context_getter", None) is not None
    except Exception:
        matrx_utils_wired = False

    matrx_connect_wired = False
    try:
        from matrx_connect import get_app_context  # noqa: F401

        matrx_connect_wired = True
    except Exception:
        matrx_connect_wired = False

    return {
        "matrx_utils_context": matrx_utils_wired,
        "matrx_connect_app_context": matrx_connect_wired,
    }
