"""One public-IP lookup per process, shared by every module that needs it.

ANA-18. Four modules carried a byte-identical copy of this lookup, and three of
them used ``timeout=120``::

    face_reg/face_recognition_client.py           _get_public_ip   timeout=120
    utils/business_metrics_manager_utils.py       _get_public_ip   timeout=120
    utils/incident_manager_utils.py               _get_public_ip   timeout=120  (dead code)
    usecases/license_plate_monitoring.py          _get_public_ip   timeout=2    (already fixed)

Every live copy is reached from a first-frame initialiser, none of them cached,
and each one is a blocking ``urlopen`` on the frame path -- so on a
network-restricted host a single frame could stall for minutes, once per copy,
and again on the next frame because nothing remembered the failure.

What the value is actually *for* is the narrow part. In every caller it feeds one
comparison -- "is the server we were handed this same host?" -- which selects
``http://localhost:{port}`` over ``http://{host}:{port}``, or picks a log label.
A wrong-but-cheap answer beats a correct one that costs the first frame two
minutes, so the failure path returns ``"localhost"`` and is cached exactly like a
success: a host that cannot reach v4.ident.me on frame 1 will not reach it on
frame 2, and retrying costs the full timeout every time.

This is a stdlib-only leaf on purpose. It follows the structure of
:mod:`.location_name_cache` -- extracted so six callers can share one
implementation without importing each other -- but deliberately does not live
*inside* it: that module's contract is that it "owns no I/O and no session", and
a ``urlopen`` here would break it. Nothing in ``utils/__init__.py`` imports the
caller modules, so this leaf adds no import cycle in either direction.
"""

from __future__ import annotations

import logging
import os
import threading
import urllib.request
from typing import List, Optional

__all__ = [
    "ENV_SKIP_PUBLIC_IP",
    "PUBLIC_IP_TIMEOUT_S",
    "reset_cache",
    "resolve_public_ip_once",
]

#: Total budget for the lookup. Was 120 s in three copies, which is not a
#: timeout so much as a promise never to answer: the request either completes in
#: well under a second or the host has no route to the internet.
PUBLIC_IP_TIMEOUT_S: float = 2.0

#: Set to 1/true/yes to skip the lookup entirely and assume ``"localhost"``.
#: For deployments that know they are air-gapped and do not want to spend even
#: :data:`PUBLIC_IP_TIMEOUT_S` finding out.
ENV_SKIP_PUBLIC_IP = "MATRICE_SKIP_PUBLIC_IP"

# One slot, module-scoped so every importer shares it. ``None`` means "not yet
# resolved"; any string -- including the "localhost" written on failure -- is
# final for the life of the process.
_cache: List[Optional[str]] = [None]
_lock = threading.Lock()

_module_logger = logging.getLogger(__name__)


def resolve_public_ip_once(logger: Optional[logging.Logger] = None) -> str:
    """This host's public IP, resolved at most once per process.

    Returns ``"localhost"`` when the lookup is disabled or fails. The lock is
    held across the request so N first-frame initialisers racing on startup make
    one lookup between them rather than N.
    """
    log = logger or _module_logger
    with _lock:
        if _cache[0] is not None:
            return _cache[0]
        if (os.environ.get(ENV_SKIP_PUBLIC_IP) or "").strip().lower() in {"1", "true", "yes"}:
            _cache[0] = "localhost"
            return _cache[0]
        try:
            public_ip = (
                # URL kept literal at the call site: a variable here defeats the static
                # scheme check (ruff S310) for no gain.
                urllib.request.urlopen("https://v4.ident.me", timeout=PUBLIC_IP_TIMEOUT_S)  # nosec B310  # nosemgrep: python.lang.security.audit.dynamic-urllib-use-detected.dynamic-urllib-use-detected
                .read()
                .decode("utf8")
                .strip()
            )
            _cache[0] = public_ip or "localhost"
        except Exception as e:
            log.warning(
                "Public IP lookup failed (%s); using 'localhost' for the rest of this "
                "process. Set %s=1 to skip the lookup entirely.",
                e,
                ENV_SKIP_PUBLIC_IP,
            )
            _cache[0] = "localhost"
        return _cache[0]


def reset_cache() -> None:
    """Forget the resolved value so the next call looks it up again.

    Test support. Production never calls this: the whole point of the module is
    that the answer is decided once, and re-deciding it re-introduces the
    per-frame stall this replaced.
    """
    with _lock:
        _cache[0] = None
