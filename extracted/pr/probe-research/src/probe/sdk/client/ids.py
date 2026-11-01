"""parse and normalize id references (uuid, `id:` refs, catalog refs) and drop absent query params."""

from __future__ import annotations
import re
import uuid
from typing import Any


def _is_uuid(value: object) -> bool:
    try:
        uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        return False
    return True


#: A bare ref read as an id (`_id_ref`): the 36-character form an id is printed
#: in. A 32-hex slug (an md5, say) stays a slug.
_BARE_ID = re.compile(r"[0-9a-fA-F]{8}-(?:[0-9a-fA-F]{4}-){3}[0-9a-fA-F]{12}")


def _id_ref(ref: str) -> bool:
    """A ref that names an id: ``id:<anything>``, or a bare `_BARE_ID`
    (`Client._project_by_id_ref`)."""
    return ref.startswith("id:") or bool(_BARE_ID.fullmatch(ref))


def catalog_path_ref(ref: str) -> str:
    """A catalog ref (`dataset:c4-clean@3`, `checkpoint:<run>@best`) as one path
    segment: `:` and `@` stay readable, anything else (a `/` in a source's
    canonical key) is percent-encoded."""
    from urllib.parse import quote

    return quote(str(ref), safe=":@")


def _present(params: dict[str, Any]) -> dict[str, Any] | None:
    """Query params minus the ones not given (None), booleans as `true`/`false`."""
    kept = {k: (str(v).lower() if isinstance(v, bool) else v) for k, v in params.items() if v is not None}
    return kept or None


def _norm_id(value: object) -> str:
    return str(value or "").strip().removeprefix("id:").lower()


def _same_id(got: object, want: str) -> bool:
    """Two refs to one row: an `id:` prefix and case do not count."""
    return bool(_norm_id(got)) and _norm_id(got) == _norm_id(want)
