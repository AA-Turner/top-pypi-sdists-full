"""The file-type half of an artifact's identity: keeping the extension on its name.

Its own dependency-free module for the same reason as ``hashing``: ``sdk/client.py``,
``sdk/run.py`` and the CLI all need it and cannot import each other.

An artifact's ``name`` IS its relative posix path on the server
(``app/artifacts/schemas.py``): the dashboard builds its folder tree by splitting it
on ``/``, and the preview route decides text-vs-raster-vs-binary from its extension.
``--name`` REPLACES the file's basename, though, and agents pass an IDENTITY there --
the reuse check is keyed on the name, so ``--name atomworks-study-README`` is the
documented habit. The extension went with it, no writer sets ``content_type``, and the
file arrived intact and unpreviewable.

So the extension is put back HERE, at the door, from the path the bytes came from.
Only ever ADDITIVE: a name that already carries an extension is returned untouched, so
a caller who deliberately named an upload ``report.txt`` keeps it.
"""

from __future__ import annotations

import re

#: What counts as an extension on a leaf name: alphanumeric, at most 12 characters
#: (``safetensors`` is 11, ``dockerignore`` 12 -- the longest that occur), and it
#: must contain a LETTER. That last rule is what keeps ``atomworks-study-v0.3`` from
#: reading as extension ``3``, which would leave it unrepaired -- and that is exactly
#: the family of name this module exists for.
_EXTENSION = re.compile(r"^[A-Za-z0-9]{1,12}$")


def file_extension(name: str) -> str:
    """The extension of ``name``'s leaf, without the dot, or ``''`` if it has none."""
    leaf = name.rsplit("/", 1)[-1]
    stem, dot, extension = leaf.rpartition(".")
    # No dot at all, or a leading-dot dotfile (`.gitignore`), whose "extension" is its
    # whole name -- calling that an extension would refuse to repair `.gitignore` -> md.
    if not dot or not stem:
        return ""
    if not _EXTENSION.match(extension) or not any(c.isalpha() for c in extension):
        return ""
    return extension


def name_with_extension(name: str, path: str | None) -> str:
    """``name`` carrying the local file's extension, unless it already has one.

    Idempotent, so applying it at both the CLI door and the SDK door (the CLI's async
    branch reaches only the first, an in-process script only the second) cannot
    double-append.
    """
    if not path or file_extension(name):
        return name
    extension = file_extension(path.replace("\\", "/"))
    if not extension:
        return name
    # A name that already ends in '.' would otherwise become `foo..md`.
    separator = "" if name.endswith(".") else "."
    return f"{name}{separator}{extension}"


#: Extensions whose file is a picture of a result, so the SDK and `probe
#: artifact add` file it as a ``plot`` when the caller names no kind. Lower-case,
#: without the dot. PDF is deliberately absent: a paper or a report is a PDF far
#: more often than a figure is, and calling it a plot would mislabel them all.
PLOT_EXTENSIONS = frozenset({"png", "jpg", "jpeg", "svg", "gif", "webp"})


def artifact_kind_for(name: str, path: str | None = None) -> str:
    """The artifact kind a file's extension implies: ``plot`` or ``file``.

    Only for a caller that passed no kind; an explicit kind always wins. The
    name is read first (it carries the path's extension by the time the SDK
    asks, see ``name_with_extension``), then the path.
    """
    extension = file_extension(name) or (file_extension(path.replace("\\", "/")) if path else "")
    return "plot" if extension.lower() in PLOT_EXTENSIONS else "file"
