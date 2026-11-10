"""parse and normalize id references (uuid, `id:` refs, catalog refs, the new-slug shape) and drop absent query params."""

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


#: A NEW project or experiment slug (D25): lowercase ASCII words joined by single '-', checked
#: by the server on every create (twin: app/shared/vocab/slugs.py). Existing slugs of any shape
#: keep resolving.
NEW_SLUG_PATTERN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
NEW_SLUG_MAX_LENGTH = 120


def is_new_slug(value: object) -> bool:
    """True when `value` may be created as a new project or experiment slug."""
    return isinstance(value, str) and len(value) <= NEW_SLUG_MAX_LENGTH and bool(NEW_SLUG_PATTERN.fullmatch(value))


def to_kebab_slug(text: str) -> str:
    """`text` spelled as a new slug ("Protein Folding" -> "protein-folding", "Café" -> "cafe"); ""
    when no ASCII letter or digit survives (twin: app/shared/vocab/slugs.py to_kebab_slug)."""
    import unicodedata

    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", folded.lower()).strip("-")[:NEW_SLUG_MAX_LENGTH].rstrip("-")


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
