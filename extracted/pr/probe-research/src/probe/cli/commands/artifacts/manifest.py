"""probe artifact add --from-manifest: read JSONL rows, check and plan each one, enqueue them all."""

from __future__ import annotations
import json
import os
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ....sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer

from .... import errors
from ....sdk.artifact.anchors import FILE_ANCHORS as _FILE_ANCHORS, Anchor
from ....sdk import session_marker
from ....sdk.artifact.kinds import DEFAULT_ARTIFACT_KIND
from ....sdk.capture.code.sources.directory import DEFAULT_REFERENCE_OVER_BYTES as _SNAPSHOT_REFERENCE_OVER_BYTES


# -- bulk import (--from-manifest) ------------------------------------------
#
# WHY THIS EXISTS. One `probe artifact add` per file costs one Python process
# start, one network slug->id resolution, and -- when an agent is driving -- one
# model turn. At 200k files that is 20-45 CPU-hours before a single byte moves,
# and the resolution traffic is 200k requests for what is one answer. A manifest
# collapses all three: ONE process, ONE resolution per distinct anchor, N rows
# journalled to the outbox for the drainer to deliver.

#: Keys a manifest row may carry. Each is the flag of the same name on
#: `artifact add`, so a row and a command line mean exactly the same thing.
#:
#: An unrecognised key FAILS the row rather than being ignored. A manifest is
#: generated, not typed, so `"file"` where `"path"` was meant is the realistic
#: mistake -- and silently ignoring it enqueues nothing while reporting success,
#: which is the one outcome a bulk importer must never produce.
#:
#: `notes` is the one key that is read and dropped: files no longer carry notes,
#: and a manifest an older skill or importer wrote must still upload its files.
#: `_artifact_add_manifest` says so once.
_MANIFEST_KEYS = frozenset(
    {
        "path",
        "uri",
        "name",
        "notes",
        "kind",
        "step",
        "span",
        "content_type",
        "meta",
        "reference",
        "hash",
        "allow_missing",
        "run",
        "project",
        "experiment",
        "workspace",
        "shared",
    }
)

#: Above this size a manifest row is RECORDED rather than uploaded, unless the
#: row says otherwise. Same constant and same reasoning as the snapshot path: a
#: checkpoint or a dataset shard already sits on a shared volume, and copying
#: tens of GB per row to re-store what is already there is duplication, not
#: reproducibility.
_MANIFEST_REFERENCE_OVER_BYTES = _SNAPSHOT_REFERENCE_OVER_BYTES


def _manifest_field(row: dict, key: str, want: type | tuple[type, ...], label: str):
    """One row field, type-checked. A generated manifest gets types wrong (a
    stringified step, a list where a map belongs) and the error is far more
    useful here than as a 422 the drainer swallows hours later."""
    value = row.get(key)
    if value is None or isinstance(value, want):
        return value
    raise typer.BadParameter(f"{key!r} must be {label}, got {type(value).__name__}")


def _manifest_rows(path: str):
    """Yield ``(lineno, row, error)`` for every non-blank line of a JSONL file.

    Blank lines are skipped and not counted -- a trailing newline is not a row.
    """
    with open(path, encoding="utf-8") as handle:
        for lineno, raw in enumerate(handle, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                yield lineno, None, f"not JSON: {exc}"
                continue
            if not isinstance(row, dict):
                yield lineno, None, "each line must be a JSON object"
                continue
            yield lineno, row, None


def _plan_manifest_row(
    row: dict,
    *,
    default_anchor: tuple[Anchor, str | None] | None,
    reference_over: int,
    config: Any = None,
) -> dict:
    """Turn one row into the arguments :func:`_artifact_enqueue` takes.

    Deterministic and network-free, so the validation pass and the enqueue pass
    agree without carrying every parsed row in memory. Raises
    :class:`typer.BadParameter` for anything wrong with the row; the caller
    records that against the line number and moves to the next one.
    """
    unknown = sorted(set(row) - _MANIFEST_KEYS)
    if unknown:
        raise typer.BadParameter(
            f"unknown key(s): {', '.join(unknown)}. A row takes {', '.join(sorted(_MANIFEST_KEYS))}"
        )

    row_anchor = any(
        row.get(key) is not None for key in ("run", "project", "experiment", "workspace")
    ) or bool(row.get("shared"))
    if row_anchor:
        anchor, anchor_ref = _pick_anchor(
            run=_manifest_field(row, "run", str, "a string"),
            project=_manifest_field(row, "project", str, "a string"),
            experiment=_manifest_field(row, "experiment", str, "a string"),
            workspace=_manifest_field(row, "workspace", str, "a string"),
            shared=bool(row.get("shared")),
        )
    elif default_anchor is not None:
        anchor, anchor_ref = default_anchor
    else:
        raise typer.BadParameter(
            "needs an anchor: a run/project/experiment/workspace/shared key on the "
            "row, or --project/--experiment/--workspace/--shared on the command"
        )

    path = _manifest_field(row, "path", str, "a string")
    uri = _manifest_field(row, "uri", str, "a string")
    local = path if path else session_marker.probe_config().local_path_of(uri)
    if local:
        # A researcher's `.probe.config` excludes this row's file: refused like
        # any bad row (named by line), so nothing about it is recorded. One
        # checker (`config`) serves all the rows: rows in a folder share it.
        from probe.sdk.recording_rules import recording_rules as _exclusions

        verdict = config.check(local) if config is not None else _exclusions.excluded(local, hot=True)
        if verdict.excluded:
            raise typer.BadParameter(
                f"{session_marker.probe_config().shown(local)} is excluded by "
                f"{session_marker.verdict_source(verdict)}; Probe records nothing about it"
            )
    kind = _manifest_field(row, "kind", str, "a string") or DEFAULT_ARTIFACT_KIND.value
    step = _manifest_field(row, "step", int, "an integer")
    span = _manifest_field(row, "span", str, "a string")
    meta = _manifest_field(row, "meta", dict, "an object")
    # Through _manifest_field like every other key. `bool(row.get(k))` accepted
    # the string "false" as True -- a realistic generator error, since the prompt
    # shows the value as a bare `true|false` token -- and silently recorded a
    # file as a pointer whose bytes are never uploaded.
    reference = bool(_manifest_field(row, "reference", bool, "true or false"))
    hash_content = bool(_manifest_field(row, "hash", bool, "true or false"))
    allow_missing = bool(_manifest_field(row, "allow_missing", bool, "true or false"))
    # A RELATIVE path in a manifest row defaults to being the name, because it
    # IS the structure: `backfill.py` states the contract the dashboard depends
    # on -- "the name is the file's relative path and nothing else", and the
    # folder tree is built by splitting it on '/'. Defaulting to the basename
    # would flatten a whole import into one directory and collide every
    # `config.yaml` in it.
    #
    # An ABSOLUTE path falls back to the basename. It describes where a file
    # sits on the machine that wrote the manifest, which is not a name anyone
    # wants in a dashboard and leaks a local layout into shared data.
    default_name = path if (path and not os.path.isabs(path)) else None
    name = _validate_artifact_row(
        anchor,
        path=path,
        uri=uri,
        name=_manifest_field(row, "name", str, "a string") or default_name,
        reference=reference,
        hash_content=hash_content,
        allow_missing=allow_missing,
        kind=kind,
        step=step,
        span=span,
        meta=meta,
    )

    # A code row is stored, not pointed at, whatever "reference" said. Applied
    # here as well as on the command line because that is this function's whole
    # contract: a rule enforced on one and not the other is discovered a hundred
    # thousand rows later. No per-row print -- the summary reports modes.
    reference = _reference_after_code_check(
        kind, reference=reference, path=path, allow_missing=allow_missing
    )

    if reference:
        if not allow_missing and not os.path.exists(path):
            raise typer.BadParameter(
                f"cannot reference {path!r}: no such file. Set "
                '"allow_missing": true on the row to record it anyway '
                "(e.g. it lives on a mount this host does not see)"
            )
    elif uri is None:
        if not path:
            raise typer.BadParameter('needs "path" (or "reference", or "uri")')
        if not os.path.isfile(path):
            raise typer.BadParameter(f"{path} is not a regular file")
        # Big files are RECORDED, not copied -- see _MANIFEST_REFERENCE_OVER_BYTES.
        # Never for a workspace/Shared row: those anchors have no reference form
        # at all (a file IS its bytes), so promoting one would turn a legal row
        # into an illegal one behind the caller's back.
        #
        # Never for a CODE row either. Size is why a checkpoint is recorded
        # rather than copied; it is not a reason to point at code, and without
        # this a large code row demoted above would be promoted straight back
        # into the reference this rule exists to prevent.
        if (
            anchor not in _FILE_ANCHORS
            and not _is_code_kind(kind)
            and os.path.getsize(path) >= reference_over
        ):
            reference = True

    return {
        "anchor": anchor,
        "anchor_ref": anchor_ref,
        "name": name,
        "path": path,
        "uri": uri,
        "reference": reference,
        "hash_content": hash_content,
        "allow_missing": allow_missing,
        "kind": kind,
        "step": step,
        "span": span,
        "content_type": _manifest_field(row, "content_type", str, "a string"),
        "meta": meta,
    }


def _artifact_add_manifest(
    manifest: str,
    *,
    default_anchor: tuple[Anchor, str | None] | None,
    reference_over: int,
) -> None:
    """Enqueue every row of a JSONL manifest. See the block comment above.

    Two passes over the FILE, not over a list of parsed rows: validation must
    happen before any bytes are staged, and holding 200k parsed rows in memory to
    achieve that trades one resource problem for another. Re-parsing JSON is
    cheap next to the snapshot each row is about to cost. That is also why the
    manifest is a path and not stdin -- a stream cannot be read twice.
    """
    failures: dict[int, dict] = {}
    anchors: dict[tuple[Anchor, str], str | None | _AnchorFailure] = {}
    total = 0
    is_notes_dropped = False

    def fail(lineno: int, message: str) -> None:
        failures[lineno] = {"line": lineno, "error": message}

    # -- pass 1: parse, validate, resolve each distinct anchor exactly once ---
    from probe.sdk.recording_rules import recording_rules as _exclusions

    config = _exclusions.checker(hot=True)
    client: Client | None = None
    try:
        for lineno, row, error in _manifest_rows(manifest):
            total += 1
            if error is not None:
                fail(lineno, error)
                continue
            if row.get("notes") is not None and not is_notes_dropped:
                is_notes_dropped = True
                _warn_file_notes_ignored('"notes" in a manifest row')
            try:
                plan = _plan_manifest_row(
                    row, default_anchor=default_anchor, reference_over=reference_over, config=config
                )
            except ClickException as exc:
                fail(lineno, exc.format_message())
                continue
            except (OSError, ValueError) as exc:
                fail(lineno, str(exc))
                continue

            anchor, ref = plan["anchor"], plan["anchor_ref"]
            if anchor not in _SLUG_ANCHORS or not ref:
                continue
            key = (anchor, ref)
            if key not in anchors:
                if client is None:
                    client = _client()
                try:
                    anchors[key] = _anchor_id_for(client, anchor, ref)
                except Exception as exc:  # noqa: BLE001 -- recorded, not raised
                    anchors[key] = _AnchorFailure(str(exc))
            resolved = anchors[key]
            if isinstance(resolved, _AnchorFailure):
                fail(lineno, resolved.message)
    finally:
        if client is not None:
            client.close()

    # -- pass 2: journal the rows that survived -----------------------------
    enqueued = {"upload": 0, "reference": 0}
    if total > len(failures):
        with _async_client() as c:
            for lineno, row, error in _manifest_rows(manifest):
                if error is not None or lineno in failures:
                    continue
                # Guarded, exactly as pass 1 is. The file list is re-planned
                # here, and a shared research drive is LIVE -- a file deleted
                # between the two passes is the normal case, not a race. Letting
                # BadParameter escape aborted the command at exit 2, abandoning
                # every remaining row and never printing the summary.
                try:
                    plan = _plan_manifest_row(
                        row, default_anchor=default_anchor, reference_over=reference_over, config=config
                    )
                except (typer.BadParameter, OSError) as exc:
                    fail(lineno, str(exc))
                    continue
                anchor, ref = plan.pop("anchor"), plan.pop("anchor_ref")
                anchor_id = ref
                if anchor in _SLUG_ANCHORS and ref:
                    anchor_id = anchors[(anchor, ref)]
                name = plan.pop("name")
                try:
                    # in_parts=False: a bulk import's big rows stay its documented
                    # trade (a reference, or a row failure), never one staging each.
                    result = _artifact_enqueue(c, anchor, anchor_id, name, ping=False, in_parts=False, **plan)
                except ClickException as exc:
                    fail(lineno, exc.format_message())
                except (OSError, errors.RosError, ValueError) as exc:
                    fail(lineno, str(exc))
                else:
                    if result["mode"] not in enqueued:
                        # "refused"/"unstaged" are row FAILURES, not counters.
                        # _enqueue_upload swallows the OSError this `except` used
                        # to catch, so without this a full spool became a
                        # KeyError that aborted a 200k-row import with no summary.
                        fail(
                            lineno,
                            result.get("unstaged_reason")
                            or "could not be queued (the outbox is not writable)",
                        )
                    else:
                        enqueued[result["mode"]] += 1
        _kick_drainer()

    # Machine-readable and on stdout, because the caller is a script: counts,
    # then every row that did NOT land, with its line number and why. Only the
    # failures are enumerated -- a success list is one line per file, which at
    # manifest scale is a second copy of the manifest nobody asked for.
    _print_json(
        {
            "manifest": manifest,
            "rows": total,
            "enqueued": sum(enqueued.values()),
            "uploads": enqueued["upload"],
            "references": enqueued["reference"],
            "failed": len(failures),
            "anchors_resolved": len(anchors),
            "failures": [failures[line] for line in sorted(failures)],
        }
    )
    if failures:
        # Non-zero so an automated caller notices, AFTER the summary is printed:
        # the whole point is that the good rows landed and these ones did not.
        raise typer.Exit(1)
from probe.cli.commands.artifacts.anchors import _AnchorFailure, _SLUG_ANCHORS, _anchor_id_for, _pick_anchor  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.artifacts.enqueue import _artifact_enqueue  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.artifacts.row_checks import _is_code_kind, _reference_after_code_check, _validate_artifact_row  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.commands import ClickException  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.flag_values import _warn_file_notes_ignored  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _async_client, _client, _kick_drainer  # noqa: E402 -- pieces need each other; the front door loads this one first
