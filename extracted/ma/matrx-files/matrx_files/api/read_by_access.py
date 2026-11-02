"""The marker a matrx-files route carries when its read is DECIDED BY ACCESS.

``Depends(file_read_decided_by_access)`` on a GET route says: this handler authorizes the named
file by ``FileService.read_record(file_id, user_id=…)`` (``files.has_access_for`` as the
person), so the host's organization admission must not refuse it for a missing — or foreign —
organization. The standalone service composes these declarations from its route table
(``matrx_files/standalone/admission.py``) and hands them to ``AuthMiddleware`` as
``authenticated_resource_routes``.

It is a pure MARKER and enforces nothing: matrx-connect's ``authenticated_resource_bootstrap``
would also demand ``is_authenticated``, which is False on the file-session cookie lane every
``<img>``/``<video>`` byte GET rides — using it here would 401 every private media render.
Identity is still required by each route's own ``user_id_dep``.
"""

from __future__ import annotations


async def file_read_decided_by_access() -> None:
    """Marker only — see the module docstring."""
    return None
