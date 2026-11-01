"""The file-type half of an artifact's identity: keeping the extension on its name.

Dependency-free like ``hashing``: client, run and the CLI all need it.

An artifact's ``name`` IS its relative posix path on the server: the dashboard
splits it on ``/`` for its folder tree, and preview picks text/raster/binary from
its extension. ``--name`` REPLACES the basename and agents pass an identity there
(``--name atomworks-study-README``), so the extension went with it and the file
arrived unpreviewable (no writer sets ``content_type``).

So the extension is put back here, from the source path. Only ADDITIVE: a name
that already has an extension (``report.txt``) is returned untouched.
"""

from __future__ import annotations

import re

from .kinds import DEFAULT_ARTIFACT_KIND, ArtifactKind, normalize_artifact_kind

#: An extension: alphanumeric, at most 12 chars (``dockerignore`` is the longest),
#: with a LETTER, so ``atomworks-study-v0.3`` is not read as extension ``3``.
_EXTENSION = re.compile(r"^[A-Za-z0-9]{1,12}$")


def file_extension(name: str) -> str:
    """The extension of ``name``'s leaf, without the dot, or ``''`` if it has none."""
    leaf = name.rsplit("/", 1)[-1]
    stem, dot, extension = leaf.rpartition(".")
    # A dotfile's (`.gitignore`) "extension" is its whole name: not one.
    if not dot or not stem:
        return ""
    if not _EXTENSION.match(extension) or not any(c.isalpha() for c in extension):
        return ""
    return extension


def name_with_extension(name: str, path: str | None) -> str:
    """``name`` carrying the local file's extension, unless it already has one.

    Idempotent: applied at both the CLI and SDK doors (the CLI async branch reaches
    only the first, an in-process script only the second) without double-appending.
    """
    if not path or file_extension(name):
        return name
    extension = file_extension(path.replace("\\", "/"))
    if not extension:
        return name
    # A name that already ends in '.' would otherwise become `foo..md`.
    separator = "" if name.endswith(".") else "."
    return f"{name}{separator}{extension}"


#: Saved model/training state, filed as ``checkpoint`` when no kind is given (the
#: failed-run alert and disk finding look for it). ``bin`` (any binary), ``gguf``
#: and ``onnx`` (exported models) are absent.
CHECKPOINT_EXTENSIONS = frozenset({"ckpt", "safetensors", "pt", "pth"})


def artifact_kind_for(name: str, path: str | None = None, *, checkpoints: bool = True) -> str:
    """The artifact kind a file's extension implies: ``checkpoint`` or ``other``.

    Only when the caller passed no kind; an explicit kind wins. Reads the name
    first (see ``name_with_extension``), then the path. An image is ``other``:
    a figure is not a kind; what it shows belongs in its notes.

    ``checkpoints=False`` is output capture's: a saved checkpoint folder holds
    ``scheduler.pt``, ``rng_state.pth`` etc., and each filed as ``checkpoint``
    would become "the last checkpoint" the alert and disk finding use.
    """
    extension = (file_extension(name) or (file_extension(path.replace("\\", "/")) if path else "")).lower()
    if checkpoints and extension in CHECKPOINT_EXTENSIONS:
        return ArtifactKind.CHECKPOINT.value
    return DEFAULT_ARTIFACT_KIND.value


def kind_to_send(kind: str | None) -> str | None:
    """``kind`` as an upload's presign carries it: NO kind for the default one.

    A presign without a kind means "default on a fresh row, keep what a restage
    holds", so re-uploading never clobbers an earlier kind. The default is
    ``other`` (formerly ``file``, still passed by the checkpoint and Harbor
    writers): both travel as None; any other word travels as itself.
    """
    if kind is None or normalize_artifact_kind(kind) == (DEFAULT_ARTIFACT_KIND, None):
        return None
    return kind
