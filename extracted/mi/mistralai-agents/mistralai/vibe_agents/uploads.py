"""Files uploaded to a remote Session: their URIs, and the upload contract both sides share.

An upload URI names a file the control plane stores for a Session, for example
``upload://agent/0199c5e1-8a3b-7d42-9f20-3c5e7a2b1d84``. The authority is the namespace of
the resolver, not a tenant, and the path is the opaque upload id: nothing in the URI says
where the bytes are stored.

The control plane and its clients also share the size and name limits of one upload.
Clients infer declared media types with Python's ``mimetypes`` or supply one explicitly.
"""

from urllib.parse import urlsplit
from uuid import UUID

UPLOAD_URI_SCHEME = "upload"
UPLOAD_URI_NAMESPACE = "agent"

MAX_UPLOAD_BYTES = 100 * 1024 * 1024
"""The most bytes one upload may hold, 100 MiB."""
MAX_UPLOAD_NAME_LENGTH = 255
"""The longest file name, in characters, an upload may declare."""


def upload_uri(upload_id: UUID) -> str:
    return f"{UPLOAD_URI_SCHEME}://{UPLOAD_URI_NAMESPACE}/{upload_id}"


def is_upload_uri(uri: str) -> bool:
    return urlsplit(uri).scheme == UPLOAD_URI_SCHEME


def parse_upload_uri(uri: str) -> UUID | None:
    """Return the upload id, or ``None`` when ``uri`` is not an upload URI.

    Raises ``ValueError`` for a URI with the upload scheme that does not have the
    ``upload://agent/<uuid>`` shape.
    """

    parts = urlsplit(uri)
    if parts.scheme != UPLOAD_URI_SCHEME:
        return None
    if parts.netloc != UPLOAD_URI_NAMESPACE:
        raise ValueError(f"upload URIs must use the {UPLOAD_URI_NAMESPACE!r} namespace: {uri!r}")
    if parts.query or parts.fragment:
        raise ValueError(f"upload URIs cannot have a query or fragment: {uri!r}")
    upload_id = parts.path.removeprefix("/")
    if not upload_id or "/" in upload_id:
        raise ValueError(f"upload URIs must name exactly one upload id: {uri!r}")
    try:
        return UUID(upload_id)
    except ValueError as error:
        raise ValueError(f"upload URIs must name a UUID: {uri!r}") from error


__all__ = [
    "MAX_UPLOAD_BYTES",
    "MAX_UPLOAD_NAME_LENGTH",
    "UPLOAD_URI_NAMESPACE",
    "UPLOAD_URI_SCHEME",
    "is_upload_uri",
    "parse_upload_uri",
    "upload_uri",
]
