# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import io

from contrast.agent.assess.utils import is_tracked
from contrast.utils.decorators import fail_quietly
from contrast.utils.assess.duck_utils import safe_getattr, safe_iterator

from contrast.utils.safe_import import safe_import
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

SUPPORTED_TYPES = (
    str,
    bytes,
    bytearray,
)

DJANGO_PROMISE_TYPE = safe_import("django.utils.functional.Promise")


@fail_quietly("Failed check if obj is tracked", return_value=False)
def recursive_is_tracked(obj):  # pylint: disable=too-many-return-statements
    """
    This is a fairly hot code path in some applications; be mindful of performance
    """
    if obj is None:
        return False

    if isinstance(obj, SUPPORTED_TYPES):
        return is_tracked(obj)

    if isinstance(obj, dict):
        return any(
            recursive_is_tracked(key) or recursive_is_tracked(value)
            for key, value in obj.items()
        )
    if isinstance(obj, io.IOBase):
        return safe_getattr(obj, "cs__tracked", False) or safe_getattr(
            obj, "cs__source", False
        )
    # These are the only safe objects where we can guarantee that we won't
    # destructively modify the object such that the application may see
    # different results.
    if isinstance(obj, (list, tuple)):
        return any(recursive_is_tracked(item) for item in safe_iterator(obj))

    if DJANGO_PROMISE_TYPE and isinstance(obj, DJANGO_PROMISE_TYPE):
        return is_tracked(str(obj))

    return is_tracked(obj)
