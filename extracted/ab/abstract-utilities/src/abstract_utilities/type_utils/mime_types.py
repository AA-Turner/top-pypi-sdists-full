"""MIME lookups — they live in abstract_essentials.mime_utils; get_mime_type keeps
abstract_utilities' octet-stream fallback."""
from .imports import (
    get_media_map,
    get_media_exts,
    confirm_type,
    is_media_type,
    get_all_file_types,
    derive_media_type,
    Path,
    os,
    make_list,
    MIME_TYPES,
    MIME_NAMES,
    MIME_META,
    MEDIA_TYPES,
    MIME_REFERENCE,
    load_mime_reference,
    mime_for_name,
    essentials_get_mime_type,
)


def get_mime_type(path_or_ext):
    """
    Look up the MIME type for a path or extension; fall back to octet-stream.

    abstract_essentials.get_mime_type does the lookup (whole-basename entries
    win, then the longest matching suffix across the categories); this wrapper
    keeps the historical octet-stream fallback instead of None.
    """
    return essentials_get_mime_type(path_or_ext) or 'application/octet-stream'
