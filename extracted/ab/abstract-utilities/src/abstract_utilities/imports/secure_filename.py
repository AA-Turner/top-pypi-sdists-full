"""werkzeug.utils.secure_filename, without werkzeug. Stdlib only.

Vendored verbatim (constants included) so filename sanitisation works with no
third-party dependency. Behaviour matches werkzeug's implementation.
"""
from __future__ import annotations

import os
import re
import unicodedata

__all__ = ["secure_filename"]

_filename_ascii_strip_re = re.compile(r"[^A-Za-z0-9_.-]")
_windows_device_files = frozenset({
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "COM¹", "COM²", "COM³",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
    "LPT¹", "LPT²", "LPT³",
    "CONIN$", "CONOUT$",
})


def secure_filename(filename: str) -> str:
    r"""Return a secure version of *filename*, safe to store on disk.

    >>> secure_filename("My cool movie.mov")
    'My_cool_movie.mov'
    >>> secure_filename("../../../etc/passwd")
    'etc_passwd'
    >>> secure_filename('i contain cool \xfcml\xe4uts.txt')
    'i_contain_cool_umlauts.txt'

    May return an empty string; the caller is responsible for handling that.
    """
    filename = unicodedata.normalize("NFKD", filename)
    filename = filename.encode("ascii", "ignore").decode("ascii")

    for sep in os.sep, os.path.altsep:
        if sep:
            filename = filename.replace(sep, " ")
    filename = str(_filename_ascii_strip_re.sub("", "_".join(filename.split()))).strip(
        "._"
    )

    # On NT, a couple of special device files are present in every folder;
    # ensure the target isn't named after one by prepending an underscore.
    if (
        os.name == "nt"
        and filename
        and filename.split(".")[0].upper() in _windows_device_files
    ):
        filename = f"_{filename}"

    return filename
