# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
import locale
import sys

DEFAULT_ENCODING = (
    locale.getencoding()
    if sys.version_info >= (3, 11)
    else locale.getpreferredencoding(do_setlocale=False)
)
