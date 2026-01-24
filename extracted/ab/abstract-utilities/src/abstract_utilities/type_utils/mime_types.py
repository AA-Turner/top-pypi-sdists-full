from .imports import *
# A big, but by no means exhaustive, map of extensions to mime‐types by category:
def get_media_map(categories=None):
    """
    Return a sub‐dict of MEDIA_TYPES for the given categories.
    If categories is None or empty, return the whole MEDIA_TYPES.
    """
    if not categories:
        return MEDIA_TYPES
    cats = {str(c) for c in categories}
    return {c: MEDIA_TYPES[c] for c in cats if c in MEDIA_TYPES}


def get_media_exts(categories=None):
    """
    Return a flat, sorted list of all extensions for the given categories.
    """
    media_map = get_media_map(categories)
    return sorted({ext for exts in media_map.values() for ext in exts})


def confirm_type(path_or_ext, categories=None,**kwargs):
    """
    Given a file‐path or extension, return its media category (e.g. "image"), or None.
    """
    categories = categories or kwargs.get('media_types')
    ext = Path(path_or_ext).suffix.lower()
    media_map = get_media_map(categories)
    for category, exts in media_map.items():
        if ext in exts:
            return category
    return None


def is_media_type(path_or_ext, categories=None,**kwargs):
    """
    True if the given file‐path or extension belongs to one of the categories.
    """
    categories = categories or kwargs.get('media_types')
    return confirm_type(path_or_ext, categories) is not None


def get_mime_type(path_or_ext):
    """
    Look up the MIME type by extension in MIME_TYPES; fall back to octet‐stream.
    """
    ext = Path(path_or_ext).suffix.lower()
    for mapping in MIME_TYPES.values():
        if ext in mapping:
            return mapping[ext]
    return 'application/octet-stream'


def get_all_file_types(categories=None, directory=None,**kwargs):
    """
    Recursively glob for files under `directory` whose extension belongs to `categories`.
    Returns a list of full paths.
    """
    categories = categories or kwargs.get('media_types')
    base = Path(directory)
    if not base.is_dir():
        return []
    wanted = get_media_map(categories)
    return [
        str(p)
        for p in base.rglob('*')
        if p.is_file() and Path(p).suffix.lower() in {e for exts in wanted.values() for e in exts}
    ]
