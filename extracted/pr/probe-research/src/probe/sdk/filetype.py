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

from .artifact_kinds import DEFAULT_ARTIFACT_KIND, ArtifactKind, normalize_artifact_kind

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


#: Extensions whose file is saved model or training state, filed as a
#: ``checkpoint`` when the caller names no kind -- the kind the failed-run alert
#: ("resume from") and the disk-space finding look for. ``bin``, ``gguf`` and
#: ``onnx`` are absent: ``bin`` is any binary, the other two are exported models.
CHECKPOINT_EXTENSIONS = frozenset({"ckpt", "safetensors", "pt", "pth"})


def artifact_kind_for(name: str, path: str | None = None, *, checkpoints: bool = True) -> str:
    """The artifact kind a file's extension implies: ``checkpoint`` or ``other``.

    Only for a caller that passed no kind; an explicit kind always wins. The
    name is read first (it carries the path's extension by the time the SDK
    asks, see ``name_with_extension``), then the path. An image is ``other``
    like any other file: a figure is not a kind (``artifact_kinds``), and what
    a picture shows belongs in its notes.

    ``checkpoints=False`` is output capture's: the files a run left in its folder
    include every file of a saved checkpoint folder (``scheduler.pt``,
    ``rng_state.pth``), and each of those filed as a ``checkpoint`` would become
    "the last checkpoint" the alert names and the disk finding sizes against.
    """
    extension = (file_extension(name) or (file_extension(path.replace("\\", "/")) if path else "")).lower()
    if checkpoints and extension in CHECKPOINT_EXTENSIONS:
        return ArtifactKind.CHECKPOINT.value
    return DEFAULT_ARTIFACT_KIND.value


def kind_to_send(kind: str | None) -> str | None:
    """``kind`` as an upload's presign carries it: NO kind for the default one.

    The server reads a presign without a kind as "the default on a fresh row,
    whatever the row already holds on a restage", so re-uploading a name without
    choosing a kind never clobbers the one an earlier write chose. The default
    is spelled ``other`` now and was ``file`` before (still what the checkpoint
    and Harbor writers pass), so both travel as None; any other word, a label
    included, travels as itself.
    """
    if kind is None or normalize_artifact_kind(kind) == (DEFAULT_ARTIFACT_KIND, None):
        return None
    return kind
