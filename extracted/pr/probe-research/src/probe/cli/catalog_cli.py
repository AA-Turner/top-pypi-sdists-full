"""`probe source|dataset|checkpoint` and `probe provenance`: the data catalog
(plan data-catalog C5, C8, C11).

    probe source add https://huggingface.co/datasets/allenai/c4 --revision 1588ec4 --license ODC-BY
    probe dataset add data/c4-clean/ --name c4-clean --run dedup-v2 --source source:7f3c \\
        --note "dropped 1,204 seqs >90% identical to test"
    probe dataset add data/c4-clean/ --name c4-clean --from dataset:c4-raw@1 --step "dedup by hand"
    probe dataset list | show REF | use REF --run R --role train | download REF -o DIR
    probe checkpoint list --project odyssey-1b | use REF --run R
    probe provenance checkpoint:sft-7b@best --steps

Datasets, checkpoints and sources are the team's, not one project's. Reads
print a table (``--json`` for the server's answer); a refusal is an error line
and exit 1, like every other `probe` write.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Optional

import typer

from ..sdk import catalog, errors
from ..sdk.catalog_vocab import Direction, HashMode, Registered, Role, Stored

source_app = typer.Typer(
    no_args_is_help=True, help="external sources: Hub datasets, buckets, URLs, base models"
)
dataset_app = typer.Typer(no_args_is_help=True, help="the team's datasets and their versions")
checkpoint_app = typer.Typer(no_args_is_help=True, help="the checkpoints every run saved, team-wide")

#: Set in the Probe daemon's own `probe` calls (`daemon/tools.py`).
DAEMON_SESSION_ENV = "PROBE_DAEMON_SESSION"
#: `POST /v1/artifacts/download/batch` takes at most this many ids (F36).
DOWNLOAD_BATCH = 1000
#: Rows a list asks for per page (the server caps at 100).
PAGE = 100


def _main():
    """`probe.cli.main`, the module (the package re-exports its `main()`
    function under the same name)."""
    import importlib

    return importlib.import_module(f"{__package__}.main")


def _client():
    return _main()._client()


def _fail(message: str) -> None:
    typer.echo(f"error: {message}", err=True)
    raise typer.Exit(1)


def _print_json(obj: Any) -> None:
    _main()._print_json(obj)


def _label(value: Any) -> str:
    """A run, project or source as one word: its name, else slug, ref or id."""
    if isinstance(value, dict):
        for key in ("name", "label", "slug", "title", "ref", "canonical_key", "id"):
            if value.get(key):
                return str(value[key])
        return "-"
    return str(value) if value not in (None, "") else "-"


def _table(header: list[str], rows: list[list[str]]) -> None:
    widths = [len(h) for h in header]
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(widths[i], len(cell))
    for line in [header, *rows]:
        typer.echo("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(line)).rstrip())


def _count(value: Any) -> str:
    return f"{value:,}" if isinstance(value, int) and not isinstance(value, bool) else "-"


def _next(answer: dict) -> None:
    cursor = answer.get("next_cursor") if isinstance(answer, dict) else None
    if cursor:
        typer.echo(f"more: --cursor {cursor}", err=True)


def _refused(exc: catalog.CatalogRefused) -> None:
    _fail(str(exc))


# ---------------------------------------------------------------------------
# probe source
# ---------------------------------------------------------------------------


@source_app.command("add")
def source_add(
    uri: str = typer.Argument(..., help="where the data or model lives: a Hub URL, s3://, https://, git+https://"),
    revision: str = typer.Option(None, "--revision", help="commit sha, object version or snapshot date"),
    license_: str = typer.Option(None, "--license", help="e.g. ODC-BY, CC-BY-4.0"),
    title: str = typer.Option(None, "--title"),
    kind: str = typer.Option(None, "--kind", help="dataset, model or other (default: the server reads it from the uri)"),
    homepage: str = typer.Option(None, "--homepage"),
    citation: str = typer.Option(None, "--citation"),
    description: str = typer.Option(None, "--description"),
    as_json: bool = typer.Option(False, "--json", help="print the server's answer"),
) -> None:
    """Register an external source (or get the one already registered for the
    same uri and revision). A uri carrying a credential is refused."""
    try:
        body = catalog.source_body(
            uri, kind=kind, revision=revision, title=title, license=license_, homepage=homepage,
            citation=citation, description=description,
        )
    except catalog.CatalogRefused as exc:
        _refused(exc)
    with _client() as c:
        row = c.create_source(body) or {}
    if as_json:
        _print_json(row)
        return
    key = row.get("canonical_key") or uri
    rev = row.get("revision")
    typer.echo(f"{row.get('ref') or '-'}  {key}{'@' + rev if rev else ''}  ({'new' if row.get('created') else 'existing'})")


@source_app.command("list")
def source_list(
    query: str = typer.Option(None, "-q", "--query", help="text in the uri, key or title"),
    provider: str = typer.Option(None, "--provider", help="huggingface, s3, gcs, azure, http, git, ..."),
    kind: str = typer.Option(None, "--kind", help="dataset, model or other"),
    limit: int = typer.Option(PAGE, "--limit"),
    cursor: str = typer.Option(None, "--cursor"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    """The team's external sources, with how many runs and datasets use each."""
    with _client() as c:
        answer = c.list_sources(q=query, provider=provider, kind=kind, limit=limit, cursor=cursor) or {}
    if as_json:
        _print_json(answer)
        return
    rows = []
    for item in answer.get("items") or []:
        rev = item.get("revision")
        counts = item.get("counts") if isinstance(item.get("counts"), dict) else {}
        rows.append([
            str(item.get("ref") or "-"),
            f"{item.get('canonical_key') or item.get('uri') or '-'}{'@' + rev if rev else ''}",
            str(item.get("kind") or "-"),
            str(item.get("license") or "-"),
            f"{_count(counts.get('runs_using'))} runs",
            f"{_count(counts.get('datasets_derived'))} datasets",
        ])
    _table(["REF", "SOURCE", "KIND", "LICENSE", "USED BY", "DERIVED"], rows)
    _next(answer)


@source_app.command("show")
def source_show(ref: str = typer.Argument(..., help="source:<id> or source:<canonical key>[@<revision>]")) -> None:
    """One source and its use counts (JSON)."""
    with _client() as c:
        _print_json(c.get_source(ref))


# ---------------------------------------------------------------------------
# probe dataset
# ---------------------------------------------------------------------------


def _version_of(detail: dict, ref: str) -> dict:
    """The version ``ref`` names in a dataset detail (`@N`), else the latest."""
    versions = [v for v in detail.get("versions") or [] if isinstance(v, dict)]
    if not versions:
        return {}
    for v in versions:
        if v.get("ref") == ref:
            return v
    return max(versions, key=lambda v: v.get("n") or 0)


def _project_of(version: dict) -> str | None:
    """The project ref of a version's producer run, as `--project` takes it."""
    producer = version.get("producer") if isinstance(version.get("producer"), dict) else {}
    project = producer.get("project") or (producer.get("run") or {}).get("project") if producer else None
    if isinstance(project, dict):
        if project.get("slug"):
            return str(project["slug"])
        if project.get("id"):
            return f"id:{project['id']}"
        return None
    return str(project) if project else None


def _step_run(c: Any, from_ref: str, step: str | None, project: str | None):
    """`--from` without `--run` (R2, F22): the step is recorded as a finished
    run after the fact, filed under `--project`, else under the project of the
    `--from` version's producer run, else refused."""
    main = _main()
    if project is None:
        project = _project_of(_version_of(c.dataset(from_ref) or {}, from_ref))
        if project is None:
            _fail(
                f"--from {from_ref}: its producer run has no project to file this step under; "
                "name one with --project P"
            )
        typer.echo(f"recording the step under project {project} (where {from_ref} was made)", err=True)
    handle = c.run(
        project=main._project_slug(c, project),
        name=step or f"edit of {from_ref}",
        heartbeat=False,
        snapshot=False,
        capture_outputs=False,
        metadata={"recorded_after": True},
    )
    return handle


@dataset_app.command("add")
def dataset_add(
    path: str = typer.Argument(..., help="a local file or folder, or a remote uri (s3://, hf://, https://)"),
    name: str = typer.Option(..., "--name", help="the team dataset this becomes the next version of"),
    run: str = typer.Option(None, "--run", help="the run that produced it"),
    sources: list[str] = typer.Option(None, "--source", help="a source ref it came from (repeatable)"),
    note: str = typer.Option(None, "--note", help="what changed from the previous version, and why"),
    upload: bool = typer.Option(False, "--upload", help="store the bytes in Probe (hosted data)"),
    publish: bool = typer.Option(False, "--publish", help="needed from a read-restricted project"),
    from_ref: str = typer.Option(
        None, "--from", help="a dataset version this was made from by hand: records the step as a run"
    ),
    step: str = typer.Option(None, "--step", help="with --from: the step's name, e.g. 'dedup by hand'"),
    project: str = typer.Option(None, "--project", help="with --from: the project the step is filed under"),
    description: str = typer.Option(None, "--description", help="the dataset's description (first version)"),
    hash_mode: HashMode = typer.Option(
        HashMode.BUDGET, "--hash", help="budget: hash within the I/O budget (else fingerprint); full: every byte"
    ),
    preview: bool = typer.Option(True, "--preview/--no-preview", help="upload a 100-record sample of a reference"),
    as_json: bool = typer.Option(False, "--json", help="print the server's answer"),
) -> None:
    """Register a file, folder or remote uri as the next version of a team dataset.

    The bytes stay where they are unless --upload: a folder is identified by its
    manifest (every file's path, size and sha256), a remote uri by itself.
    --run names the run that produced it; --from records a step done by hand
    (or by an agent) as a finished run that read the --from version and made
    this one, filed under --project or the --from version's project."""
    if run and from_ref:
        _fail("--run and --from: pick one (--from records a new run for the step)")
    if (step or project) and not from_ref:
        _fail("--step and --project go with --from")
    if from_ref and catalog.is_moving_ref(from_ref):
        # The step is recorded after it happened, often by the agent: a moving
        # ref would pin whatever is newest now (D16).
        _fail(catalog.moving_ref_refusal(from_ref.strip()))
    try:
        catalog.check_name(name)
        prepared = catalog.prepare(path, hash_mode=hash_mode.value, upload=upload)
    except catalog.CatalogRefused as exc:
        _refused(exc)
    main = _main()
    with _client() as c:
        run_id = run_name = run_project = None
        step_handle = None
        if run:
            target = main._ref(c, "run", run)
            run_id = target.id
            row = target.row if isinstance(target.row, dict) else {}
            run_name = row.get("name") or row.get("slug") or run
            run_project = row.get("project_slug") or row.get("project_id")
        elif from_ref:
            step_handle = _step_run(c, from_ref, step, project)
            run_id, run_name = step_handle.id, step_handle.name
            run_project = project
        common = dict(
            note=note, sources=sources or (), publish=publish, description=description,
        )
        try:
            if step_handle is not None:
                # Inside the try: a refused use closes the step run `failed`.
                c.use_in_run(run_id, {"target": from_ref, "roles": [Role.OTHER.value], "provenance": catalog.STATED})
            if upload:
                def progress(n: int, total: int, f: Any) -> None:
                    typer.echo(f"uploading {n}/{total}: {f.relpath} ({catalog.human_bytes(f.size_bytes)})", err=True)

                answer = catalog.host(c, name, prepared, progress=progress, say=lambda line: typer.echo(line, err=True))
                have = len(answer.get("have") or [])
                if have:
                    typer.echo(f"{have} file(s) already hosted, not sent again", err=True)
                hosted = {"manifest_hash": prepared.content_hash}
                if run_id:
                    hosted["run_id"] = run_id  # the producing run, recorded as the version's step
                body = catalog.registration_body(name, hosted=hosted, **common)
            else:
                if prepared.manifest is not None:
                    c.put_manifest(prepared.content_hash, prepared.manifest.gz())
                if run_id:
                    body = catalog.registration_body(
                        name, run_file=catalog.run_file_spec(run_id, name, prepared), **common
                    )
                else:
                    body = catalog.registration_body(name, reference=catalog.reference_spec(prepared), **common)
            answer = c.register_dataset(body) or {}
        except catalog.CatalogRefused as exc:
            if step_handle is not None:
                _close_step(step_handle, ok=False)
            _refused(exc)
        except BaseException:
            if step_handle is not None:
                _close_step(step_handle, ok=False)
            raise
        if step_handle is not None:
            _close_step(step_handle, ok=True)
        # Never from the daemon: its precheck lets `dataset add` name paths
        # unscanned because their bytes never leave (`precheck.NOT_FILES`), and
        # a sample is bytes.
        if preview and run_id and not upload and not os.environ.get(DAEMON_SESSION_ENV):
            _preview_for_cli(c, run_id, name, prepared)
    if as_json:
        _print_json(answer)
        return
    version = answer.get("version") if isinstance(answer.get("version"), dict) else {}
    line = f"{version.get('ref') or name}  {catalog.human_bytes(prepared.size_bytes)}  identity {version.get('identity') or prepared.identity}"
    if run_name:
        line += f"  from run {run_name}" + (f" (project {run_project})" if run_project else "")
    if answer.get("created_version") is False:
        line += "  (same bytes as the current version: recorded as a check" + (" by this run" if run_id else "") + ")"
    typer.echo(line)


def _close_step(handle: Any, *, ok: bool) -> None:
    from ..sdk.durable import now_iso

    try:
        handle.set_status("completed" if ok else "failed", ended_at=now_iso(), strict=True)
    except Exception as exc:  # noqa: BLE001 - the registration's answer is what matters
        typer.echo(f"warning: the step run {handle.id} was not closed ({exc})", err=True)


def _preview_for_cli(c: Any, run_id: str, name: str, prepared: catalog.Prepared) -> None:
    """The sample `log_dataset` uploads, from the CLI: onto the producing run,
    named after its dataset file (found by name and identity)."""
    try:
        rows = c.list_run_artifacts(run_id, name=name, scope="own") or []
    except Exception:  # noqa: BLE001 - no preview, never a failure
        return
    row = next((r for r in rows if r.get("content_hash") == prepared.content_hash), None)
    if not row or not row.get("id"):
        return
    from ..sdk.anchors import Anchor

    def send(preview_name: str, path: str, meta: dict) -> None:
        c.upload_file(Anchor.RUN, run_id, preview_name, path, meta=meta)

    catalog.upload_preview(send, prepared, str(row["id"]))


def _use(run: str, body: dict) -> dict:
    main = _main()
    with _client() as c:
        run_id = main._ref(c, "run", run).id
        return c.use_in_run(run_id, body) or {}


def _use_body(ref: str, role: Role, reason: str | None, evidence: list[str] | None) -> dict[str, Any]:
    """`/uses` for one ref the caller names. A moving ref is refused here: the
    server resolves it when the link is MADE, and a link made from the CLI is
    made after the run used the data, so it could pin a newer version or save
    than the run read (D16)."""
    if catalog.is_moving_ref(ref):
        _fail(catalog.moving_ref_refusal(ref.strip()))
    body: dict[str, Any] = {"target": ref, "roles": [role.value], "provenance": catalog.STATED}
    if reason:
        body["reason"] = reason
    if evidence:
        # `{session, event}` per event id, exactly as `probe edge add --evidence`.
        body["evidence"] = _main()._edge_evidence(evidence)
    return body


def _roles(answer: dict, role: Role) -> str:
    return ", ".join(answer.get("roles") or [role.value])


_REASON_HELP = "why this run used it, in a sentence"
_EVIDENCE_HELP = (
    "repeatable: the id of a session event this use rests on "
    "(<stream>:<offset>:<index>, as the transcript shows it)"
)


@dataset_app.command("use")
def dataset_use(
    ref: str = typer.Argument(..., help="dataset:<name>@<N> or source:<id>"),
    run: str = typer.Option(..., "--run", help="the run that used it"),
    role: Role = typer.Option(Role.TRAIN, "--role"),
    share: Optional[float] = typer.Option(None, "--share", help="its weight in the run's training mix"),
    reason: Optional[str] = typer.Option(None, "--reason", help=_REASON_HELP),
    evidence: list[str] = typer.Option(None, "--evidence", metavar="EVENT_ID", help=_EVIDENCE_HELP),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    """Record that a run used a dataset version or a source. Name the version
    (`dataset:<name>@<N>`; `probe dataset show` lists them): a bare name or
    `@latest` is refused, because it would pin whatever is newest now."""
    body = _use_body(ref, role, reason, evidence)
    if share is not None:
        try:
            body["share"] = catalog.check_share(share)
        except catalog.CatalogRefused as exc:
            _refused(exc)
    answer = _use(run, body)
    if as_json:
        _print_json(answer)
        return
    target = answer.get("target") if isinstance(answer.get("target"), dict) else {}
    typer.echo(f"run {run} uses {target.get('ref') or ref} ({_roles(answer, role)})")


@dataset_app.command("list")
def dataset_list(
    query: str = typer.Option(None, "-q", "--query", help="text in the name"),
    project: str = typer.Option(None, "--project", help="made or used in this project"),
    registered: Registered = typer.Option(Registered.ALL, "--registered", help="all, yes (team datasets) or no"),
    limit: int = typer.Option(PAGE, "--limit"),
    cursor: str = typer.Option(None, "--cursor"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    """The team's datasets: registered ones with their latest version, and
    dataset files runs logged without registering."""
    with _client() as c:
        answer = c.list_datasets(
            q=query, project=project, registered=registered.value, limit=limit, cursor=cursor
        ) or {}
    if as_json:
        _print_json(answer)
        return
    rows = []
    for item in answer.get("items") or []:
        latest = item.get("latest") if isinstance(item.get("latest"), dict) else {}
        producer = latest.get("producer") if isinstance(latest.get("producer"), dict) else None
        made_by = "-"
        if producer:
            made_by = _label(producer.get("run"))
            if producer.get("project"):
                made_by += f" ({_label(producer.get('project'))})"
        used = item.get("used_by_runs")
        rows.append([
            str(item.get("name") or item.get("ref") or "-"),
            f"v{latest['n']}" if latest.get("n") is not None else "-",
            str(latest.get("identity") or "-"),
            catalog.human_bytes(latest.get("size_bytes")),
            made_by,
            f"{_count(used)} runs" if used is not None else "-",
        ])
    _table(["NAME", "LATEST", "IDENTITY", "SIZE", "MADE BY", "USED BY"], rows)
    _next(answer)


@dataset_app.command("show")
def dataset_show(ref: str = typer.Argument(..., help="dataset:<name>[@<N>]")) -> None:
    """One dataset: every version with its producer, change, sources and users (JSON)."""
    with _client() as c:
        _print_json(c.dataset(ref))


@dataset_app.command("download")
def dataset_download(
    ref: str = typer.Argument(..., help="dataset:<name>[@<N>]"),
    out: str = typer.Option(..., "-o", "--out", help="a new or empty folder"),
) -> None:
    """Download a version stored in Probe, file by file. A version kept
    outside Probe has no bytes here: its location is printed instead."""
    from ..sdk.checkpoints import _safe_target

    with _client() as c:
        files: list[dict] = []
        cursor = None
        while True:
            page = c.dataset_files(ref, cursor=cursor) or {}
            files.extend(f for f in page.get("items") or [] if isinstance(f, dict))
            cursor = page.get("next_cursor")
            if not cursor:
                break
        # A file Probe stores comes by its `artifact_id` (the batch door), or,
        # for an older version of a one-file team dataset, by `download`
        # (`POST /v1/artifacts/{artifact_id}/versions/{version}/download`).
        stored = [f for f in files if f.get("artifact_id")]
        by_version = [f for f in files if not f.get("artifact_id") and _version_download(f)]
        if not stored and not by_version:
            _print_location(c, ref)
            return
        dest = Path(os.path.abspath(out))
        if dest.exists() and (not dest.is_dir() or any(dest.iterdir())):
            _fail(f"{dest} exists and is not an empty folder")
        dest.mkdir(parents=True, exist_ok=True)
        total = 0
        failed: list[str] = []

        def fetch(f: dict, url: str) -> None:
            nonlocal total
            target = _safe_target(dest, str(f["relpath"]))
            target.parent.mkdir(parents=True, exist_ok=True)
            size, _digest = c.transport.download_to(url, str(target))
            if isinstance(f.get("size_bytes"), int) and size != f["size_bytes"]:
                failed.append(f"{f['relpath']} (got {size} bytes, expected {f['size_bytes']})")
            total += size

        for start in range(0, len(stored), DOWNLOAD_BATCH):
            chunk = stored[start : start + DOWNLOAD_BATCH]
            answer = c.presign_download_batch([str(f["artifact_id"]) for f in chunk]) or {}
            urls = answer.get("items") or {}
            refused = answer.get("refused") or {}
            for f in chunk:
                got = urls.get(str(f["artifact_id"])) or {}
                url = got.get("download_url") if isinstance(got, dict) else None
                if not url:
                    reason = refused.get(str(f["artifact_id"])) if isinstance(refused, dict) else None
                    failed.append(f"{f.get('relpath')}" + (f" ({reason})" if reason else ""))
                    continue
                fetch(f, url)
        for f in by_version:
            spec = _version_download(f)
            try:
                url = c.presign_version_download(spec[0], spec[1])
            except errors.RosError as exc:
                failed.append(f"{f.get('relpath')} ({exc})")
                continue
            fetch(f, url)
    fetched = len(stored) + len(by_version)
    kept_outside = len(files) - fetched
    typer.echo(f"downloaded {fetched - len(failed)} file(s), {catalog.human_bytes(total)}, to {dest}")
    if kept_outside:
        typer.echo(f"{kept_outside} file(s) of this version are not stored in Probe", err=True)
    if failed:
        _fail(f"{len(failed)} file(s) could not be downloaded: {', '.join(failed[:5])}")


def _version_download(item: dict) -> tuple[str, int] | None:
    """A files-list item's `download: {artifact_id, version}`, when it names one."""
    spec = item.get("download")
    if not isinstance(spec, dict) or not spec.get("artifact_id"):
        return None
    version = spec.get("version")
    if not isinstance(version, int) or isinstance(version, bool):
        return None
    return str(spec["artifact_id"]), version


def _print_location(c: Any, ref: str) -> None:
    detail = c.dataset(ref) or {}
    version = _version_of(detail, ref)
    meta = version.get("meta") if isinstance(version.get("meta"), dict) else {}
    where = meta.get("local_path") or version.get("uri") or "-"
    host = meta.get("host")
    typer.echo(
        f"{version.get('ref') or ref} is kept outside Probe: {where}" + (f" on {host}" if host else "")
        + " (nothing to download)"
    )


# ---------------------------------------------------------------------------
# probe checkpoint
# ---------------------------------------------------------------------------


@checkpoint_app.command("list")
def checkpoint_list(
    project: str = typer.Option(None, "--project"),
    experiment: str = typer.Option(None, "--experiment"),
    run: str = typer.Option(None, "--run"),
    best: bool = typer.Option(False, "--best", help="only the saves marked best"),
    stored: str = typer.Option(None, "--stored", help="stored or reference"),
    limit: int = typer.Option(PAGE, "--limit"),
    cursor: str = typer.Option(None, "--cursor"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    """Every checkpoint the team's runs saved: step, best, where it is, size.
    A save from a range a rewind abandoned says `rewound`."""
    with _client() as c:
        answer = c.list_checkpoints(
            project=project, experiment=experiment, run=run, best=True if best else None, stored=stored,
            limit=limit, cursor=cursor,
        ) or {}
    if as_json:
        _print_json(answer)
        return
    rows = []
    for item in answer.get("items") or []:
        if item.get("rewound"):
            mark = "rewound"
        elif isinstance(item.get("best"), dict):
            mark = f"best {item['best'].get('monitor') or ''}".strip()
        else:
            mark = ""
        location = item.get("location") if isinstance(item.get("location"), dict) else {}
        if item.get("stored") == Stored.STORED:
            # Probe holds the bytes: its storage address is no place to go.
            where = "in Probe"
        elif location.get("host") and location.get("local_path"):
            where = f"{location['host']}:{location['local_path']}"
        else:
            where = location.get("local_path") or location.get("uri") or "-"
        if item.get("locked"):
            mark, where = "locked", "-"
        rows.append([
            _label(item.get("run")),
            _count(item.get("step")),
            mark,
            str(item.get("stored") or "-"),
            where,
            catalog.human_bytes(item.get("size_bytes")),
        ])
    _table(["RUN", "STEP", "BEST", "STORED", "WHERE", "SIZE"], rows)
    totals = answer.get("totals") if isinstance(answer.get("totals"), dict) else {}
    if totals.get("bytes") is not None:
        typer.echo(f"total {catalog.human_bytes(totals['bytes'])}", err=True)
    _next(answer)


@checkpoint_app.command("use")
def checkpoint_use(
    ref: str = typer.Argument(..., help="checkpoint:<run>@step<N> or checkpoint:<id>"),
    run: str = typer.Option(..., "--run", help="the run that used it"),
    role: Role = typer.Option(Role.INIT, "--role", help="init: the weights it started from; eval: what it evaluated"),
    reason: Optional[str] = typer.Option(None, "--reason", help=_REASON_HELP),
    evidence: list[str] = typer.Option(None, "--evidence", metavar="EVENT_ID", help=_EVIDENCE_HELP),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    """Record a checkpoint a run used: the weights it started from (`--role
    init`, the default) or the one it evaluated (`--role eval`). Name the save
    (`checkpoint:<run>@step<N>`; `probe checkpoint list --run RUN` lists them):
    `@latest` and `@best` are refused, because they would pin whatever is newest
    or best now. Prints the save it pinned."""
    answer = _use(run, _use_body(ref, role, reason, evidence))
    if as_json:
        _print_json(answer)
        return
    target = answer.get("target") if isinstance(answer.get("target"), dict) else {}
    pinned = answer.get("pinned") if isinstance(answer.get("pinned"), dict) else {}
    shown = [f"step {pinned['step']}"] if pinned.get("step") is not None else []
    if pinned.get("uri"):
        shown.append(str(pinned["uri"]))
    save = f" ({', '.join(shown)})" if shown else ""
    typer.echo(f"run {run} uses {target.get('ref') or ref}{save} ({_roles(answer, role)})")


# ---------------------------------------------------------------------------
# probe provenance
# ---------------------------------------------------------------------------


def provenance(
    ref: str = typer.Argument(..., help="dataset:..., checkpoint:..., source:..., artifact:... or a run"),
    down: bool = typer.Option(False, "--down", help="what used it, instead of where it came from"),
    depth: int = typer.Option(4, "--depth", min=1, max=8),
    steps: bool = typer.Option(False, "--steps", help="the methods view: the steps from the sources, in order"),
    as_json: bool = typer.Option(False, "--json"),
) -> None:
    """Where a dataset, checkpoint or run came from (or, with --down, everything
    that used it), as far as Probe recorded."""
    if steps and down:
        _fail("--steps reads upstream only; leave out --down")
    with _client() as c:
        if steps:
            answer = c.provenance_steps(ref) or {}
        else:
            direction = Direction.DOWNSTREAM if down else Direction.UPSTREAM
            answer = c.provenance(ref, direction=direction.value, depth=depth) or {}
    if as_json:
        _print_json(answer)
        return
    if steps:
        _print_steps(answer)
    else:
        _print_graph(answer)


def _print_steps(answer: dict) -> None:
    rows: list[list[str]] = []
    n = 0
    for src in answer.get("sources") or []:
        n += 1
        if isinstance(src, dict):
            key = src.get("canonical_key") or src.get("ref") or src.get("uri") or "-"
            rev = src.get("revision")
            license_ = src.get("license")
            text = f"{key}{'@' + rev if rev else ''}" + (f"  ({license_})" if license_ else "")
        else:
            text = str(src)
        rows.append([str(n), "source", text, "", ""])
    for item in sorted(answer.get("steps") or [], key=lambda s: s.get("order") or 0):
        n += 1
        run = item.get("run") if isinstance(item.get("run"), dict) else {}
        name = _label(run)
        if item.get("recorded_after"):
            name += " (by hand)"
        # Each output on its own line with its own note; a server older than
        # `outputs_detail` sends one note for the step. A step's note no
        # output carries (a check's) goes on its first line.
        detail = [d for d in item.get("outputs_detail") or [] if isinstance(d, dict)]
        if detail:
            made = [(str(d.get("ref") or "-"), _note(d.get("change"))) for d in detail]
            if not any(note for _, note in made):
                made[0] = (made[0][0], _note(item.get("change")))
        else:
            outputs = ", ".join(str(o) for o in item.get("outputs") or []) or "-"
            made = [(outputs, _note(item.get("change")))]
        for i, (output, note) in enumerate(made):
            head = [str(n), "run", name] if i == 0 else ["", "", ""]
            rows.append([*head, f"-> {output}", note])
    if not rows:
        typer.echo("no recorded history")
        return
    width = [max(len(r[i]) for r in rows) for i in range(5)]
    for r in rows:
        typer.echo("  ".join(cell.ljust(width[i]) for i, cell in enumerate(r)).rstrip())


def _note(change: Any) -> str:
    """A change's note, quoted, or nothing."""
    return f'"{change["note"]}"' if isinstance(change, dict) and change.get("note") else ""


def _print_graph(answer: dict) -> None:
    nodes = {str(n.get("id")): n for n in answer.get("nodes") or [] if isinstance(n, dict)}

    def name(node_id: Any) -> str:
        node = nodes.get(str(node_id)) or {}
        if node.get("locked"):
            return f"{node.get('type') or 'node'} (locked)"
        label = node.get("ref") or node.get("label") or node_id
        return f"{node.get('type') or 'node'} {label}"

    edges = [e for e in answer.get("edges") or [] if isinstance(e, dict)]
    if not edges and len(nodes) <= 1:
        typer.echo("no recorded history")
    for e in edges:
        roles = e.get("roles") or []
        tags = [str(e.get("relation") or "")]
        if roles:
            tags.append("/".join(str(r) for r in roles))
        if e.get("derived"):
            tags.append("derived")
        typer.echo(f"{name(e.get('from'))}  --{' '.join(t for t in tags if t)}-->  {name(e.get('to'))}")
    if answer.get("hidden"):
        typer.echo(f"{answer['hidden']} item(s) you cannot see", err=True)
    if answer.get("truncated"):
        typer.echo(f"truncated: {answer.get('truncated_reason') or 'the walk hit its bounds'}", err=True)
