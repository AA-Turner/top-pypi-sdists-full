"""MIME lookups.

Nothing MIME-related is authored or derived here; the reference tables come
from abstract_essentials via ``.module_imports``.

* ``MIME_TYPES``  - extension categories ({category: {".ext": mime}}); an extension
  is listed under every category it belongs to.
* ``MIME_NAMES``  - whole-basename matches (LICENSE, config.json, tokenizer.model ...).
* ``MIME_META``   - matching rules plus the suffixes/dirs a scanner should skip.
* ``MEDIA_TYPES`` - category -> set of extensions (abstract_essentials').
"""
from .module_imports import (
    make_list,
    get_keys,
    make_key_map,
    MEDIA_TYPES,
    MIME_META,
    MIME_NAMES,
    MIME_REFERENCE,
    MIME_TYPES,
    load_mime_reference,
    mime_for_name,
)
