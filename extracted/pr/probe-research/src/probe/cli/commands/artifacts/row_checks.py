"""the usage checks of one artifact write: code kinds are stored (never referenced), the name it lands under, where --kind went."""

from __future__ import annotations
import os

import typer
from ....sdk.artifact.anchors import FILE_ANCHORS as _FILE_ANCHORS, Anchor
from ....sdk.artifact.kinds import (
    DEFAULT_ARTIFACT_KIND,
    ArtifactKind,
    normalize_artifact_kind)
from ....sdk.artifact.filetype import name_with_extension


#: Artifact kinds whose bytes Probe STORES rather than points at.
#:
#: A reference to code is the failure this whole surface exists to avoid. A
#: `file://` pointer resolves on one machine, for as long as that machine and
#: that checkout survive, and nothing downstream can tell a live pointer from a
#: dead one without going and looking -- which is exactly why git referencing
#: was retired from `capture_manifest`. Leaving the same hole open on the manual
#: door would just move it. Scripts are small and storing them is cheap.
#:
#: RUN-anchored by construction: `--kind` is a run-only flag (the project /
#: experiment / workspace upload contract rejects it), so a non-run artifact is
#: always the default kind (`other`) and never lands here.
#:
#: Read through the vocabulary (`normalize_artifact_kind`), never a list of
#: spellings: `--kind` is free text, so `code-snapshot`, ` Code `, `script`,
#: `test` and `code_bundle` must all land where the server will file them. A set
#: missing one of them is a rule with a typo-shaped hole: `--kind code-snapshot
#: --reference` would record exactly the pointer this exists to prevent.
CODE_KINDS = frozenset({ArtifactKind.CODE, ArtifactKind.CODE_SNAPSHOT, ArtifactKind.CODE_BYTES})


def _is_code_kind(kind: str | None) -> bool:
    """Is this the kind of artifact whose bytes Probe stores rather than points at?

    True when the server would FILE the word as code (``code``, ``code_snapshot``
    or ``code_bytes``): a listed kind in any case or separator, or a synonym of
    one (``script``, ``source``, ``test``, ``code_bundle``). Normalized exactly
    as the server normalizes it, so surrounding whitespace out of a manifest
    row cannot walk a code artifact past the rule.
    """
    return normalize_artifact_kind(kind)[0] in CODE_KINDS


def _say_where_the_kind_went(kind: str | None) -> None:
    """After an `artifact add` landed or queued: one stderr line when `--kind`
    was a word the vocabulary does not list. The server files it under a listed
    kind and keeps the word as the row's label, and the caller learns that here
    rather than from a listing that shows a different kind than they typed."""
    filed, label = normalize_artifact_kind(kind)
    if label is not None:
        typer.echo(f"kind: filed as {filed.value} (label: {label})", err=True)


def _reference_after_code_check(
    kind: str, *, reference: bool, path: str | None, allow_missing: bool
) -> bool:
    """The effective ``reference`` flag: never True for a code kind.

    Returns what ``reference`` should actually be, so a code artifact takes the
    upload path even when ``--reference`` was passed.

    REFUSES rather than quietly recording a pointer when the bytes cannot be
    read from here. Falling back to a reference would reintroduce the exact row
    this rule exists to prevent, and do it in the one case nobody is watching.
    """
    if not (reference and _is_code_kind(kind)):
        return reference
    if allow_missing or not path or not os.path.isfile(path):
        raise typer.BadParameter(
            f"--kind {kind} is stored, never referenced, so its bytes have to be "
            f"readable from this host — {path!r} is not. Point it at a readable "
            "file (and drop --allow-missing), or use a non-code --kind if a "
            "pointer is genuinely what you want."
        )
    return False


def _validate_artifact_row(
    anchor: Anchor,
    *,
    path: str | None,
    uri: str | None,
    name: str | None,
    reference: bool,
    hash_content: bool,
    allow_missing: bool,
    kind: str,
    step: int | None,
    span: str | None,
    # Only its truthiness is read, so the caller may hand over either spelling:
    # the CLI's raw `--meta k=v` list or a manifest row's already-parsed object.
    meta: dict | list | None,
) -> str:
    """The usage checks for ONE artifact write, and the name it lands under.

    Shared by the single-file `artifact add` and every `--from-manifest` row so
    the two cannot disagree about what is legal. That matters more than the
    duplication it saves: a manifest is the bulk path, so a rule enforced on the
    command line and not on a row would be discovered a hundred thousand rows
    later, server-side, with no operator watching.

    Raises :class:`typer.BadParameter`. On the command line that aborts, which is
    right for one file; the manifest catches it per row and keeps going.
    """
    resolved = name
    if resolved is None and path:
        resolved = os.path.basename(path)
    if resolved is None:
        raise typer.BadParameter("artifact needs --name (or a path to derive it from)")
    # `--name` REPLACES the basename, and agents pass an identity there, so the
    # extension arrives here already stripped. Put it back from the path the bytes
    # came from -- additive only, and applied at THIS door (not just the SDK's) so
    # the async branch journals the repaired name rather than the bare one.
    resolved = name_with_extension(resolved, path)
    if reference and uri is not None:
        raise typer.BadParameter(
            "--reference derives a file:// pointer from the path; pass --reference OR "
            "--uri, not both"
        )
    if reference and not path:
        raise typer.BadParameter("--reference needs a local file path")
    # The OTHER door to a machine-local code pointer. `--reference` derives a
    # file:// uri from a path; `--uri file://...` states one outright, and
    # closing only the first would leave the rule true in the help text and
    # false in the CLI. Bucket schemes (s3/r2/https) are untouched for every
    # kind -- those name durable storage, and there is no local file to upload
    # in their place. Checked here so the command line and every manifest row
    # get the same answer.
    if uri is not None and _is_code_kind(kind) and str(uri).strip().lower().startswith("file:"):
        raise typer.BadParameter(
            f"--kind {kind} is stored, never referenced, so it cannot be a "
            f"file:// pointer: {uri!r} names a path on one machine. Pass the "
            "local path to upload the bytes, or use a bucket uri (s3://, r2://) "
            "if they already live in durable storage."
        )
    if (hash_content or allow_missing) and not reference:
        raise typer.BadParameter("--hash and --allow-missing only apply to --reference")
    if anchor is not Anchor.RUN:
        # The default kind is "no kind": `other`, or `file` as it was spelled
        # before (still what an older manifest row may carry).
        chose_kind = normalize_artifact_kind(kind) != (DEFAULT_ARTIFACT_KIND, None)
        if step is not None or chose_kind or span is not None or meta:
            raise typer.BadParameter(
                f"--kind/--step/--span/--meta are run-only; "
                f"the {anchor.value} upload contract rejects them"
            )
        if (uri is not None or reference) and anchor in _FILE_ANCHORS:
            # Caught here rather than in the SDK so it reads as a usage error instead
            # of an unhandled ValueError traceback: a file IS its bytes, so there is
            # no reference-without-bytes form and the backend declares no such route.
            raise typer.BadParameter(
                f"a {anchor.value} file cannot be a reference (it IS its bytes). "
                "Pass a local path to upload the bytes instead."
            )
    return resolved
