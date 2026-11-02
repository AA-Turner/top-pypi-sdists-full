from ...imports import (
    make_list,
)

# The MIME reference and key helpers live in the stdlib-only core
# (abstract_essentials) — the suite-wide single source of record for file
# classification.
from abstract_essentials import (
    get_keys,
    make_key_map,
)
from abstract_essentials.mime_utils import (
    MEDIA_TYPES,
    MIME_META,
    MIME_NAMES,
    MIME_REFERENCE,
    MIME_TYPES,
    load_mime_reference,
    mime_for_name,
    get_mime_type as essentials_get_mime_type,
)

# type_utils proper lives in the core as well; the modules here re-export it.
from abstract_essentials.type_utils import *
from abstract_essentials.mime_utils import (
    get_media_map,
    get_media_exts,
    confirm_type,
    is_media_type,
    get_all_file_types,
    derive_media_type,
)
