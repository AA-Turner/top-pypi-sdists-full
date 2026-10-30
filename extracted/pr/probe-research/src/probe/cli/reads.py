"""The `probe` reads the Probe daemon host answers in its own process (R38).

Each command here is ONE function, `(Api, the command's arguments) -> Printed`,
and two callers: the CLI command (`probe.cli.main`) prints what it returns, and
the daemon host (`probe.daemon.host_reads`) hands it to the model as the
output of a `probe` command it no longer starts a process for. One body, one
renderer: the daemon reads what the CLI prints, byte for byte.

    run get · run check · notes find · outbox status · run reproduce (no
    --export / --materialize) · project get · experiment get

Nothing here takes a caller's key, URL, session or settings from `os.environ`,
prints to the process's streams, or keeps anything between calls. What a call
needs comes in `Api`: its client (built from ITS caller's key and URL), how its
settings resolve (`config.resolve` over its caller's environment) and that
environment itself. What it prints goes back in `Printed`; `report_error`
writes to the stream its caller names. One daemon host answers reads for every
session it records at once, each under its own key: a value read from the
process here would be another session's. (The config file's location is read
as always: the host keeps it the session's, `runctx`.)

The helpers the moved commands share with other CLI commands (resolving a ref,
a note's target, an outbox's held credentials, how an error is reported) live
here too, and `probe.cli.main` calls them, so each has one implementation.

Light on purpose: the daemon host imports this module, never `probe.cli.main`
and the whole CLI behind it (plan M1).
"""

from __future__ import annotations

import json
import re
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

import typer

from . import refs

#: C1 controls + bidi overrides: the display-manipulation characters JSON
#: leaves raw under ensure_ascii=False. They only ever occur inside string
#: values (JSON structure is ASCII), so re-escaping them keeps the output
#: valid JSON byte-for-byte parse-equivalent.
DISPLAY_CONTROLS = re.compile("[\u0080-\u009f\u202a-\u202e\u2066-\u2069]")

def render_json(obj: Any, pretty: bool) -> str:
    """One output policy for every read command (`probe.cli.main._print_json`
    prints it and says why): indented for a terminal (`pretty`), compact for a
    pipe, display controls escaped either way."""
    if pretty:
        rendered = json.dumps(obj, indent=2, ensure_ascii=False, default=str)
    else:
        rendered = json.dumps(obj, separators=(",", ":"), ensure_ascii=False, default=str)
    return DISPLAY_CONTROLS.sub(lambda m: "\\u%04x" % ord(m.group()), rendered)


@dataclass
class Printed:
    """What a command printed, in order, and its exit code. Each part is
    `(to stderr, the line, whether it is one rendered JSON value)`: the CLI
    prints JSON with its legacy-locale fallback (`main._emit`)."""

    parts: list[tuple[bool, str, bool]] = field(default_factory=list)
    code: int = 0

    @property
    def out(self) -> str:
        return "".join(f"{text}\n" for err, text, _ in self.parts if not err)

    @property
    def err(self) -> str:
        return "".join(f"{text}\n" for err, text, _ in self.parts if err)


class Out:
    """Where one call prints: its own list, never a stream."""

    def __init__(self, pretty: bool) -> None:
        self.pretty = pretty
        self.printed = Printed()

    def json(self, value: Any) -> None:
        self.printed.parts.append((False, render_json(value, self.pretty), True))

    def say(self, text: str) -> None:
        self.printed.parts.append((False, text, False))

    def warn(self, text: str) -> None:
        self.printed.parts.append((True, text, False))

    def done(self, code: int = 0) -> Printed:
        self.printed.code = code
        return self.printed


@dataclass(frozen=True)
class Api:
    """One caller's Probe, as arguments.

    `client`: an open SDK `Client` built from the caller's key and URL (None for
    a command that reads no API). `resolve`: `config.resolve` over the caller's
    environment (the CLI's own; for the daemon host, the one the session's CLI
    would have had). `env`: that environment. `pretty`: JSON laid out for a
    terminal. `base_url`: the CLI's `--base-url`. `ambient_project`: the CLI's
    own `_ambient_project` (a test may stand one in); None reads it through
    `resolve`."""

    client: Any
    resolve: Callable[..., Any]
    env: Mapping[str, str]
    pretty: bool = False
    base_url: str | None = None
    ambient_project: Callable[..., str | None] | None = None

    def ambient(self, explicit: str | None, **kw: Any) -> str | None:
        if self.ambient_project is not None:
            return self.ambient_project(explicit, **kw)
        return ambient_project(self.resolve, explicit, **kw)

    def ref(self, kind: str, ref: str) -> refs.Ref:
        return resolve_ref(self.client, kind, ref, hint=lambda k, r: active_project_id(self.ambient, k, r),
                           limit=lambda: limit_quietly(self.resolve, self.base_url))


# -- refs -------------------------------------------------------------------------


def select_fields(obj: Any, fields: str | None) -> Any:
    """Project a read down to the named top-level fields (comma-separated).

    The CLI-side answer to response bloat: a `--fields` flag is written ONCE
    into a skill or script and reused, so the selection is authored where a
    mistake is visible immediately — the property that makes declarative field
    selection safe here and unsafe as an MCP query language, where a model
    would re-derive it on every call.

    Applies to the object itself, or to each element of `items` when the read
    is a page envelope (`next_cursor` always survives — a projection must never
    hide that a page was a page). An unknown field is a loud 422-style error,
    never a silently-absent key: `--fields slgu` returning `{}` would read as
    "the run has no slug", which is a claim the projection has no right to make.
    """
    if not fields:
        return obj
    wanted = [f.strip() for f in fields.split(",") if f.strip()]
    if not wanted:
        # `--fields ","` parses to zero names; projecting to nothing would
        # print `{}` for every row — exactly the silent-empty answer this
        # helper exists to forbid.
        raise typer.BadParameter("--fields names no fields")

    def _pick(row: Any) -> Any:
        if not isinstance(row, dict):
            return row
        missing = [f for f in wanted if f not in row]
        if missing:
            raise typer.BadParameter(
                f"unknown field(s) {', '.join(sorted(missing))}; "
                f"this read carries: {', '.join(sorted(row))}"
            )
        return {f: row[f] for f in wanted}

    if isinstance(obj, dict) and isinstance(obj.get("items"), list):
        out = {"items": [_pick(row) for row in obj["items"]]}
        if "next_cursor" in obj:
            out["next_cursor"] = obj["next_cursor"]
        return out
    return _pick(obj)


def resolve_ref(
    client: Any,
    kind: str,
    ref: str,
    *,
    hint: Callable[[str, str], str | None],
    limit: Callable[[], Any],
) -> refs.Ref:
    """Resolve a ref, reporting both failure modes as CLI errors.

    The one adapter between :mod:`probe.cli.refs` (which raises library errors so
    the SDK and tests can use it) and Typer's exit codes. Ambiguity and absence
    both surface as ``BadParameter``: each means "this ref does not identify one
    thing", and neither is something a retry of the same command fixes.
    `hint`: the active project for an experiment slug (`active_project_id`);
    `limit`: this caller's workspace limit, for the hint on a miss.
    """
    from ..sdk.errors import NotFoundError, UnfilteredListing

    if kind not in refs.SLUG_KINDS and kind not in ("run", "workspace"):
        # Kinds with no second spelling (artifacts: no item GET, no by-name
        # index, and a name that is anchor-scoped rather than unique). The id is
        # passed through -- but the verb still routes through here so it gets the
        # same prompt and the same "deleted" line as everything else.
        return refs.Ref(ref, f"{kind} {ref}")
    try:
        if kind == "run":
            return refs.resolve_run(client, ref)
        if kind == "workspace":
            return refs.resolve_workspace(client, ref)
        return refs.resolve(client, kind, ref, project_hint=hint(kind, ref))
    except NotFoundError as exc:
        # Under a workspace limit a miss may be a thing in another workspace:
        # say so, rather than let it read as gone.
        from ..sdk.workspace_limit import maybe_hidden_hint, with_hint

        message = "" if exc.workspace_limit_applied else maybe_hidden_hint(limit())
        raise typer.BadParameter(with_hint(str(exc), message)) from None
    except (
        UnfilteredListing,
        refs.AmbiguousName,
        refs.NameFilterUnsupported,
    ) as exc:
        raise typer.BadParameter(str(exc)) from None


def limit_quietly(resolve: Callable[..., Any], base_url: str | None):
    """This caller's workspace limit, or None (also when it cannot be read)."""
    try:
        return resolve(base_url=base_url).workspace_limit
    except Exception:  # noqa: BLE001 - a hint only
        return None


def filed_under(target: refs.Ref) -> str | None:
    """The project a resolved experiment ref is filed under, when its row says
    (so the experiment API's routes need no second lookup)."""
    row = target.row if isinstance(target.row, dict) else {}
    project = row.get("project_id")
    return str(project) if project and refs.is_uuid(str(project)) else None


def active_project_id(ambient: Callable[..., str | None], kind: str, ref: str) -> str | None:
    """The active project's id, when it costs nothing to know, for an
    experiment SLUG: looking there first answers in one request (refs.resolve
    falls back tenant-wide on a miss). None for anything else, and when the
    active project is stored as a slug (resolving it would be a request of
    its own)."""
    if kind != "experiment" or refs.split_selector(ref)[1] != "slug":
        return None
    try:
        project = ambient(None)
    except Exception:  # noqa: BLE001 - a hint only; the lookup works without it
        return None
    if not project:
        return None
    bare, how = refs.split_selector(project)
    return bare if how == "id" and refs.is_uuid(bare) else None


def ambient_project(resolve: Callable[..., Any], explicit: str | None, **kw: Any) -> str | None:
    """The project ref to use, canonicalising ONLY the ambient one.

    ``from_ambient`` reads a bare UUID as an id, which is right for a value the
    TOOL stored and catastrophically wrong for one a person typed: rewriting an
    explicit ``--project <uuid-shaped-slug>`` to ``id:`` is the original bug, back.
    ``resolve()`` merges flag/env/context into one string and forgets which won,
    so the provenance has to be decided here, before it is lost.
    """
    merged = resolve(project=explicit, **kw).project
    if explicit is not None:
        return explicit  # typed by a person: a bare ref is a slug, full stop.
    return refs.from_ambient(merged)


def project_slug(api: Api, ref: str | None) -> str | None:
    """The inverse of :func:`main._project_id`, for the slug-resolving paths.

    ``Client.run`` resolves a project by *slug* and raises when it is absent, so
    handing it an id makes the lookup miss a project that genuinely exists. The
    ambient anchor stores an id (stable across renames), so it has to be
    translated on the way in -- as does an explicit ``--project id:<uuid>``.

    A bare ref is returned untouched: it is already a slug by definition now, and
    absence is ``run start``'s to report, whose near-miss guard names the slugs a
    typo was close to. Resolving it here would replace that with a bare
    "not found".
    """
    if ref is None:
        return None
    bare, how = refs.split_selector(ref)
    if how == "slug":
        return bare
    return api.ref("project", ref).row.get("slug", bare)


# -- notes ------------------------------------------------------------------------

#: The entity kinds that carry a note (`entity_notes_row`).
NOTE_TARGETS = ("project", "experiment", "run")


def notes_project(api: Api, project: str | None) -> tuple[str, str]:
    """(project_id, label) for a notes read/write. Explicit beats the active one."""
    resolved = api.ambient(project, base_url=api.base_url)
    if not resolved:
        raise typer.BadParameter(
            "pass --project, or set an active project with `probe project use <slug>`"
        )
    return api.ref("project", resolved).id, project_slug(api, resolved) or resolved


def note_target(
    api: Api,
    *,
    project: str | None,
    experiment: str | None,
    run: str | None,
) -> tuple[str, str, str]:
    """(kind, id, label) for a notes write. Exactly one target, or the default.

    Refusing two targets rather than picking one: "wrote the note" is the same
    sentence whichever entity received it, so a silent preference order would
    put prose on the wrong row and say nothing.
    """
    chosen = [
        (kind, value)
        for kind, value in (("experiment", experiment), ("run", run))
        if value is not None
    ]
    if project is not None:
        chosen.append(("project", project))
    if len(chosen) > 1:
        raise typer.BadParameter("pass exactly one of --project/--experiment/--run")
    if not chosen:
        # No flag at all: the project, which is what `notes` has always meant.
        project_id, label = notes_project(api, None)
        return "project", project_id, label
    kind, value = chosen[0]
    if kind == "project":
        project_id, label = notes_project(api, value)
        return "project", project_id, label
    if kind == "run":
        # Runs resolve by petname OR id -- the one polymorphic ref in the CLI.
        return "run", refs.resolve_run(api.client, value).id, value
    return "experiment", refs.resolve(api.client, "experiment", value).id, value


def entity_notes_row(client: Any, kind: str, entity_id: str) -> dict:
    """The whole entity row, one explicit branch per kind — the parity check
    reads paths statically, so no f-string may compute its segment.

    Returns the ROW, not just its `notes`: the headroom pair the read advisory
    is derived from travels beside the document, and re-fetching to get it would
    double every `notes show`.
    """
    if kind == "project":
        return client.get_project(entity_id)
    if kind == "experiment":
        # The experiment API's detail: it carries the notes, their version and
        # the headroom (`notes_limit_tokens`, `notes_remaining_tokens`) the
        # read advisory and the over-cap refusal below need (server X21).
        return client.get_experiment(entity_id)
    if kind == "run":
        return client.get_run(entity_id)
    raise ValueError(f"{kind!r} carries no notes; expected one of {', '.join(NOTE_TARGETS)}")


def sub_notes_supported(exc: Any, warn: Callable[[str], None]) -> None:
    """Map a ROUTE-shaped 404 to the honest self-host answer (said through `warn`).

    The hosted backend always has these routes; a self-hosted server one
    release behind answers FastAPI's bare `Not Found` — which is not "no such
    note", it is "no such door". Saying so beats handing the caller an id hunt.
    An ENTITY 404 names what is missing ("run not found", "no sub-note
    titled ...") and passes through untouched.
    """
    if exc.status == 404 and str(exc.detail or "").strip() == "Not Found":
        # A bare `Not Found` is a ROUTE miss, and there are two ways to miss a
        # route: a server without it, or a request that never reached it (a
        # malformed id spliced into the path lands here too, against a fully
        # current server). Name both rather than diagnose confidently.
        warn(
            "error: the sub-notes route answered a bare 404 — this server may "
            "predate sub-notes (self-hosted needs research-os >= 0.231.0.0; "
            "hosted backends already have them), or the target id may be "
            "malformed"
        )
        raise typer.Exit(1) from exc


def sub_note_id_ref(note: str) -> str | None:
    """The uuid inside an `id:<uuid>` --note value, or None for a plain title.

    The escape hatch for duplicated titles: titles are legal to duplicate
    (tabs key on id), so every command that refuses an ambiguous title must
    also take the id the refusal printed — otherwise the advised repair
    (`probe notes rename`) resolves through the same refusal and the
    duplicates are unreachable from the CLI entirely.
    """
    if note.startswith("id:"):
        return note[3:].strip()
    return None


def resolve_sub_note_by_title(
    client: Any, kind: str, entity_id: str, title: str, warn: Callable[[str], None]
) -> dict:
    """The one sub-note `title` (or `id:<uuid>`) names, via the list read; a
    refusal is said through `warn` and exits 1.

    For the ID-ADDRESSED commands (show/rename/delete), which need the id in
    hand. Writes never come here — append/edit send the title IN the request
    and the server resolves at apply time, which is what lets them queue.
    Same exactly-once contract, spoken client-side: zero matches lists what
    exists, two-plus lists the ids. An `id:<uuid>` value resolves through the
    SAME entity-scoped list, so an id from some other entity is a miss here,
    never a cross-entity read that mislabels its output.
    """
    from ..sdk import errors

    try:
        page = client.list_sub_notes(kind, entity_id)
    except errors.RosError as exc:
        sub_notes_supported(exc, warn)
        raise
    id_ref = sub_note_id_ref(title)
    if id_ref is not None:
        matches = [row for row in page.get("sub_notes", []) if row.get("id") == id_ref]
        if len(matches) == 1:
            return matches[0]
        warn(
            f"error: no sub-note with id {id_ref!r} on this {kind} "
            "(`probe notes list` shows its sub-notes and their ids)"
        )
        raise typer.Exit(1)
    matches = [row for row in page.get("sub_notes", []) if row.get("title") == title.strip()]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        titles = [row.get("title") for row in page.get("sub_notes", [])]
        warn(
            f"error: no sub-note titled {title!r} on this {kind}; "
            f"existing titles: {titles or '(none)'}"
        )
        raise typer.Exit(1)
    ids = [row.get("id") for row in matches]
    warn(
        f"error: {len(matches)} sub-notes are titled {title!r}: {ids}. "
        "Address one as `--note id:<uuid>`, or rename one first "
        "(`probe notes rename --note id:<uuid> --to ...`)."
    )
    raise typer.Exit(1)


# -- the outbox's held credentials -----------------------------------------------


def stored_login(name: str | None):
    """Settings carrying context ``name``'s stored login alone (never an env
    token), or None when it stores no token."""
    from ..sdk.config import DEFAULT_BASE_URL, Settings, load_context

    try:
        stored = load_context(name)
    except Exception:  # noqa: BLE001 -- an unreadable config stores nothing
        return None
    if not stored.get("token"):
        return None
    return Settings(
        base_url=(stored.get("base_url") or DEFAULT_BASE_URL).rstrip("/"),
        token=stored["token"],
        ingest_token=stored.get("ingest_token"),
    )


def login_account(name: str | None, *, network: bool) -> tuple[str, str] | None:
    """(customer_id, user_id) of context ``name``'s stored login: as the
    sign-in recorded it for THIS token, else (``network``) `GET /v1/me`.
    None when unknown. Raises what `/v1/me` raised."""
    from ..sdk.config import load_context
    from ..sdk.journal import _identity_of, credential_fingerprint

    login = stored_login(name)
    if login is None:
        return None
    recorded = load_context(name).get("identity")
    if (
        isinstance(recorded, dict)
        and recorded.get("fingerprint") == credential_fingerprint(login.token, None)
        and recorded.get("customer_id")
        and recorded.get("user_id")
    ):
        return str(recorded["customer_id"]), str(recorded["user_id"])
    return _identity_of(login) if network else None


def credentials_here(name: str | None, env: Mapping[str, str]) -> set[str]:
    """The credentials a shell with `env` sends with: its environment's and the stored login."""
    from ..sdk import outbox_worker
    from ..sdk.journal import credential_fingerprint

    here = set(outbox_worker.env_fingerprints(env))
    login = stored_login(name)
    if login is not None:
        here.add(credential_fingerprint(login.token, None))
    return here


def held_credentials(ops: list, status: dict, *, network: bool, env: Mapping[str, str]) -> list[dict]:
    """Per env/code credential whose queued writes nothing here holds: how
    many, its latest refusal, who holds it (`journal.credential_holders`) and
    what to do next -- restart its process, `adopt` its writes (only when
    that would pass: the same team and user as the login stored here), or
    `discard` them. ``network``: ask `/v1/me` when the login's account was not
    recorded at sign-in. ``env``: the caller's environment (its credentials)."""
    from ..sdk.config import current_context_name
    from ..sdk.journal import HolderState, Refusal, credential_holders, held_credentials as held

    name = current_context_name() or None
    entries = held(ops, here=credentials_here(name, env))
    if not entries:
        return []
    try:
        mine = login_account(name, network=network)
    except Exception:  # noqa: BLE001 -- unknown: adopt checks it itself
        mine = None
    refused = status.get("refused_fingerprints") if isinstance(status, dict) else None
    refused = refused if isinstance(refused, dict) else {}
    out = []
    for entry in entries:
        fp = entry["fingerprint"]
        account = entry.get("account")
        holders = [
            {key: h.get(key) for key in ("pid", "state", "program", "script", "sdk")}
            for h in credential_holders(fp)
        ]
        alive = [h for h in holders if h["state"] == HolderState.ALIVE]
        refused_at = refused.get(fp)
        if entry.get("adopted"):
            step = (
                "adopted: its writes go out with your login. Still queued means that login is "
                "another account's or server's, its token was refused, or these are DELETEs or "
                "writes refused for scope, which go only with their own credential: "
                "`probe outbox drain` says which"
            )
        elif entry.get("refusal") == Refusal.SCOPE:
            step = (
                "Probe refused its writes for a missing scope: they may not be sent with a "
                "login that has it. Give the job a token with that scope, or "
                f"`probe outbox discard --held --credential {fp}` drops them"
            )
        elif alive and not refused_at:
            step = f"pid {alive[-1]['pid']} holds it and sends them itself"
        elif account is None:
            step = (
                "the account behind it was never recorded here, so nothing can match it to "
                f"your login: `probe outbox discard --held --credential {fp}` drops them"
            )
        elif mine is not None and account != mine:
            step = (
                "another account's (team or user): sign in as it here, or "
                f"`probe outbox discard --held --credential {fp}` drops them"
            )
        else:
            step = (
                f"`probe outbox adopt --credential {fp}` sends them with your login"
                + ("" if mine is not None else " (it checks the account first)")
            )
        if alive and refused_at and entry.get("refusal") != Refusal.SCOPE:
            step = (
                f"its token was refused: restart pid {alive[-1]['pid']} with a valid token. "
                f"For what it queued: {step}"
            )
        out.append(
            {
                "fingerprint": fp,
                "source": entry.get("source"),
                "writes": entry["writes"],
                "refused_at": refused_at,
                "account_known": account is not None,
                "same_account": None if (account is None or mine is None) else account == mine,
                "holders": holders,
                "next": step,
            }
        )
    return out


# -- the commands -------------------------------------------------------------------


def _exits(out: Out, body: Callable[[], int | None]) -> Printed:
    """`body`'s output and exit code; a `typer.Exit` a helper raised after
    saying why is that code."""
    try:
        code = body() or 0
    except typer.Exit as exc:
        code = int(exc.exit_code)
    return out.done(code)


def run_get(api: Api, run: str, fields: str | None = None) -> Printed:
    """`probe run get`: one run."""
    out = Out(api.pretty)
    out.json(select_fields(api.client.get_run(run), fields))
    return out.done()


def run_check(api: Api, run: str, verify: bool = False) -> Printed:
    """`probe run check`: capture completeness, exit 2 if incomplete."""
    out = Out(api.pretty)
    result = api.client.check_run(api.ref("run", run).id, verify=verify)
    out.json(result)
    return out.done(2 if result.get("state") == "incomplete" else 0)


def reproduce_record(api: Api, run: str) -> tuple[str, dict]:
    """`(run id, the server-assembled reproduction record)`."""
    run_id = api.ref("run", run).id
    return run_id, api.client.run_reproduce(run_id)


def run_reproduce(api: Api, run: str) -> Printed:
    """`probe run reproduce` without --export / --materialize: the record."""
    out = Out(api.pretty)
    out.json(reproduce_record(api, run)[1])
    return out.done()


def project_get(api: Api, project_id: str, fields: str | None = None) -> Printed:
    """`probe project get`: one project."""
    out = Out(api.pretty)
    out.json(select_fields(api.client.get_project(api.ref("project", project_id).id), fields))
    return out.done()


def experiment_get(api: Api, experiment_id: str) -> Printed:
    """`probe experiment get`: one experiment."""
    out = Out(api.pretty)
    target = api.ref("experiment", experiment_id)
    out.json(api.client.get_experiment(target.id, project_id=filed_under(target)))
    return out.done()


def notes_find(
    api: Api,
    words: list[str],
    project: str | None = None,
    experiment: str | None = None,
    run: str | None = None,
    note: str | None = None,
) -> Printed:
    """`probe notes find`: the paragraphs of an entity's note that mention any of `words`."""
    from . import notes_find as finder

    out = Out(api.pretty)

    def body() -> None:
        kind, entity_id, label = note_target(api, project=project, experiment=experiment, run=run)
        if note is not None:
            found = resolve_sub_note_by_title(api.client, kind, entity_id, note, out.warn)
            document = api.client.get_sub_note(found["id"])
            text = document.get("body") or ""
            label = f"{label} › {note}"
        else:
            document = entity_notes_row(api.client, kind, entity_id)
            text = document.get("notes") or ""
        if not text:
            out.warn(f"{label} has no notes yet")
            return
        out.say(finder.report(label, document.get("notes_version"), text, words))

    return _exits(out, body)


def outbox_status(api: Api, journal: Any, others: list, verbose: bool = False, run: str | None = None) -> Printed:
    """`probe outbox status`: `journal` (this caller's outbox) summarised, with
    `others` (every other outbox of this user here) counted. Exit 0 when
    everything is delivered, 2 otherwise."""
    from ..sdk.journal import Journal, auth_blocked_since

    out = Out(api.pretty)
    pending = [item for namespace in journal.namespaces() for item in namespace.pending()]
    failed = [item for namespace in journal.namespaces() for item in namespace.failed()]
    pending.sort(key=lambda item: item[1].get("enqueued_at") or "")
    if run is not None:
        pending = [(p, op) for p, op in pending if op.get("run_ref") == run]
        failed = [(p, op) for p, op in failed if op.get("run_ref") == run]
    status = Journal.read_status(journal.dir) or {}
    summary = {
        "dir": str(journal.dir),
        **({"run": run} if run is not None else {}),
        "pending": len(pending),
        # Uploads queued before their credential scan: they become pending ops
        # once the worker (or `probe run end`) has scanned them.
        "waiting": len(journal.waiting(run_ref=run)),
        "failed": len(failed),
        "paused": status.get("paused", journal.paused),
        # When the pause ends by itself; null while paused means until `resume`.
        "paused_until": status.get("paused_until"),
        # The queue-wide block, or a credential the drain set aside (#2041).
        "auth_blocked_since": auth_blocked_since(status),
        "oldest_pending": pending[0][1].get("enqueued_at") if pending else None,
        "last_error": status.get("last_error"),
        # Ops the journal declined to stage because the disk was near full. They
        # still deliver -- the drainer reads the source in place -- but they now
        # depend on that source still existing at drain time, which is a fact an
        # operator should be able to see rather than infer from a dead letter.
        "unstaged_low_disk": status.get("unstaged_low_disk"),
    }
    try:
        # Writes that wait for a credential no process here holds: whose,
        # who holds it, and the command that moves them (#2041 follow-up).
        held = held_credentials([op for _, op in pending], status, network=False, env=api.env)
    except Exception:  # noqa: BLE001 -- advice only; the counts stand
        held = []
    if held:
        summary["held_credentials"] = held
    producers = journal.producer_report()
    if producers:
        summary["producers"] = [
            {
                "producer_id": p.get("producer_id"),
                "role": p.get("role"),
                "last_sequence": p.get("last_sequence"),
                # A FLOOR, written after the op file is unlinked. Beside
                # last_sequence it answers the only question worth asking of a
                # writer that has gone away: did what it queued actually land.
                "delivered": p.get("delivered"),
                "state": p.get("state"),
                "gaps": p.get("gaps") or [],
            }
            for p in producers
        ]
    if verbose:

        def row(op: dict, state: str) -> dict:
            return {
                "op_id": op.get("op_id"),
                "state": state,
                "kind": op.get("kind"),
                "run_ref": op.get("run_ref"),
                "detail": (
                    f"{op.get('method')} {op.get('path')}"
                    if op.get("kind") == "http"
                    else (op.get("upload") or {}).get("name")
                ),
                "attempts": op.get("attempts"),
                "last_error": op.get("last_error"),
            }

        summary["ops"] = [row(op, "pending") for _, op in pending] + [
            row(op, "failed") for _, op in failed
        ]
    undelivered = bool(pending or failed or summary["waiting"])
    if others:
        # Every other outbox of this user on this machine: a distributed job's
        # `rank-*` queues and the $TMPDIR fallback used to be invisible here
        # (plan 1.5). Banner-grade counts (status.json), never a parse.
        dirs = [
            {
                "dir": str(summary["dir"]),
                "pending": summary["pending"],
                "failed": summary["failed"],
                "waiting": summary["waiting"],
            }
        ]
        for other in others:
            counts = Journal.read_status(other.dir) or {}
            dirs.append(
                {
                    "dir": str(other.dir),
                    "pending": int(counts.get("pending") or 0),
                    "failed": int(counts.get("failed") or 0),
                    "waiting": int(counts.get("waiting") or 0),
                }
            )
        summary["dirs"] = dirs
        summary["total"] = {
            key: sum(entry[key] for entry in dirs) for key in ("pending", "failed", "waiting")
        }
        undelivered = undelivered or any(summary["total"].values())
    out.json(summary)
    return out.done(2 if undelivered else 0)


# -- errors -------------------------------------------------------------------------

#: typer's own click (`typer._click`) raises these; see `main.ClickException`.
ClickException = next(
    (base for base in typer.BadParameter.__mro__ if base.__name__ == "ClickException"),
    type("_NoClickException", (Exception,), {}),
)
#: 402 `limit`s whose figures are sizes (the storage meters).
BYTE_LIMITS = frozenset({"storage_bytes", "hosted_data_bytes"})
#: The data catalog's hosted-data cap (C8, D2).
HOSTED_DATA_LIMIT = "hosted_data_bytes"


def key_refused(exc: Any) -> bool:
    """Did Probe refuse the credential itself (not a scope, a lock, a route)?"""
    from ..sdk import errors
    from ..sdk.key_refusal import credential_refused

    if isinstance(exc, (errors.WorkspaceLockedError, errors.UnroutableEndpointError)):
        return False
    return isinstance(exc, (errors.AuthError, errors.ScopeError)) and credential_refused(exc.status, str(exc))


def report_error(exc: BaseException, file: Any = None, *, daemon_session: bool) -> int | None:
    """Say on `file` (default: the process's stderr) what `probe` says when a
    command raised `exc`, and return its exit code: a usage error (2), a CLI
    string the wire model refused (2), a plan limit (1), any other Probe error
    (1; under a Probe daemon -- `daemon_session` -- a refused key adds
    `KEY_REFUSED_LINE`, the line the daemon stops on), a local path (1).
    None for anything else: a bug, which the caller reports as one."""
    from pydantic import ValidationError

    from ..sdk import errors
    from ..sdk.key_refusal import KEY_REFUSED_LINE

    stream = sys.stderr if file is None else file
    if isinstance(exc, ClickException):  # usage / bad-parameter errors
        exc.show(file=file)
        return exc.exit_code or 2
    if isinstance(exc, ValidationError):
        # A CLI string that fails the generated model's validation is a usage error,
        # not a crash: `--older-than 2026-07-01` is valid ISO 8601 but not an aware
        # datetime, and `--id abc` is not a UUID. Report it like one (exit 2).
        for err in exc.errors():
            name = ".".join(str(p) for p in err["loc"]) or exc.title
            print(f"error: invalid {name}: {err['msg']}", file=stream)
        return 2
    if isinstance(exc, errors.LimitReachedError):
        # Ahead of RosError because a plan refusal is the one error here that is
        # not a mistake. The generic branch would print a single line that reads
        # like a failure; this one has to say what the ceiling is, that the
        # existing work is safe, and how to lift it -- the CTA is the whole reason
        # the limit exists.
        print(f"error: {exc}", file=stream)
        if exc.current is not None and exc.maximum is not None:
            if exc.limit in BYTE_LIMITS:
                # Sizes, not bare numbers: the storage refusals send GiB.
                from ..sdk.catalog import bytes_figure

                print(f"       at {bytes_figure(exc.current)} of {bytes_figure(exc.maximum)}.", file=stream)
            else:
                print(f"       at {exc.current} of {exc.maximum}.", file=stream)
        if exc.limit == HOSTED_DATA_LIMIT:
            # The data catalog's own cap (C8, D2): one figure over hosted
            # datasets and checkpoints. A reference costs it nothing.
            print(
                "       That cap is hosted datasets and checkpoints together. Record the data as a "
                "reference instead (leave out --upload): Probe then stores no bytes of it.",
                file=stream,
            )
        print(
            "       Nothing was deleted and everything already recorded stays readable.",
            file=stream,
        )
        # The server's message already ENDS with the booking link, because it has
        # to stand alone for any client that does not special-case 402 (including
        # the generic RosError branch). Printing our own copy under it put the
        # same URL on screen twice, which reads like a mistake rather than
        # emphasis. Only add the line when the message somehow lacks the link.
        if exc.booking_url and exc.booking_url not in str(exc):
            print(f"       Book 30 minutes: {exc.booking_url}", file=stream)
        return 1
    if isinstance(exc, errors.RosError):
        print(f"error: {exc}", file=stream)
        if daemon_session and key_refused(exc):
            print(KEY_REFUSED_LINE, file=stream)
        return 1
    if isinstance(exc, OSError):
        # A bad local path is a usage error, not a crash. The upload commands take a
        # path and hash it before any request, and the anchored path is strict (no
        # fail-open spool to absorb it), so a typo would otherwise print a traceback.
        print(f"error: {exc}", file=stream)
        return 1
    return None
