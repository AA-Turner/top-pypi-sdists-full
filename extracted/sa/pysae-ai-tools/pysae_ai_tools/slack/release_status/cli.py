"""`pysae-ai-tools slack release-status` command and its Slack transport.

Instead of spamming #mep with one message per release milestone, every CI job
calls this command to update *one* message that tracks the release as it
progresses. The message is found by an exact ``(app, version)`` match on its
Slack metadata, its structured state lives in that metadata (``state.py``) except
for the release notes — which are read back from the message's own blocks, keeping
the payload under the size past which Slack silently discards it — and the rendered
blocks are a pure function of the state (``render.py``). So each call reads the
state, applies one update, re-renders, and edits the message in place (creating it
on first call).

Release content is split across the thread: the **main message** carries only the
first configured language's user-facing notes (FR), while every other language and
the changelog land as **thread replies** under it — EN, then IT, then the changelog
last. Each language opens under its flag header (🇫🇷 Français / 🇬🇧 English /
🇮🇹 Italiano). Pass ``--root`` so this command reads the checked-out repo and assembles all
of it itself (``release_slack_content``); the replies are tracked by their kind in
the message metadata, so a re-run edits them in place instead of duplicating them.

Usage:
    # Create / update the web track, generating the FR main content + EN/IT/changelog
    # thread replies straight from the checked-out repo at --root.
    pysae-ai-tools slack release-status --app info --version "$CI_COMMIT_TAG" \\
        --channel mep --track web --state deploying --root .

    # Later milestone (different pipeline) — content + replies preserved from metadata
    pysae-ai-tools slack release-status --app info --version "$CI_COMMIT_TAG" \\
        --channel mep --track apple --state awaiting-store-review

    # Content only, no track (still generated from the repo)
    pysae-ai-tools slack release-status --app info --version "$CI_COMMIT_TAG" \\
        --channel mep --root .

    # Seed job: attach content AND show every declared release.tracks at once
    # (each at its initial 'building' state). CI milestones then advance each track.
    pysae-ai-tools slack release-status --app info --version "$CI_COMMIT_TAG" \\
        --channel mep --root . --init-tracks

    # Legacy: attach a single pre-rendered body to the main message (no replies)
    pysae-ai-tools code release-content "$CI_COMMIT_TAG" --render slack \\
        | pysae-ai-tools slack release-status --app info --version "$CI_COMMIT_TAG" \\
            --channel mep --content -

A call that carries no content of its own (``--track``/``--state`` alone, as every
post-release CI milestone does) may only *update* an existing message: it has nothing
to fill a new one with, so creating one would post a contentless duplicate next to the
real announce. When no ``(app, version)`` message is found, such a call reports the
anomaly and exits 2 instead.

Pass ``--best-effort`` on a job whose real work is something else (building an APK,
deploying) so a failed announce never brings it down: the failure is still reported on
stdout and stderr, but the command exits 0. A *usage* error — an unknown ``--track``, an
invalid ``--state``, an invocation with nothing to do — ignores the flag and still exits
non-zero, since a tolerated typo in a pipeline would never get fixed.

    # Milestone from a build job: report a failed announce, but keep the job green.
    pysae-ai-tools slack release-status --app driver --version "$CI_COMMIT_TAG" \\
        --channel mep --track android --state building --best-effort

Output (JSON, one line):
    {"ok": true, "ts": "...", "channel": "...", "created": true|false}
    {"ok": false, "error": "..."}                       # exit 1
    {"ok": false, "error": "...", "created": false}     # exit 2 — nothing to update
    {"ok": false, "error": "...", "best_effort": true}  # exit 0 — --best-effort
"""

import json
import sys
import time
from pathlib import Path
from typing import Annotated, NoReturn

import typer

from ...code.release_content import release_slack_content
from ...common.project_config import load_project_config, slack_enabled
from ..client import SlackApiError, slack_paginate, slack_post
from ..common import get_slack_token, resolve_channel
from .render import _reply_blocks, content_from_blocks, render_blocks, render_text
from .state import METADATA_EVENT_TYPE, METADATA_PAYLOAD_SAFE_BYTES, TRACKS, ReleaseState, apply_update

REPLY_LABELS: dict[str, str] = {
    "en": "Notes de version (EN)",
    "it": "Notes de version (IT)",
    "changelog": "Changelog",
}
"""Short notification fallback (the Slack ``text`` field) per reply kind."""


class MissingReleaseMessage(RuntimeError):
    """No ``(app, version)`` message to update, and the caller has no content to create one.

    Raised instead of posting a message that would be empty by construction — the
    caller passed only ``--track``/``--state``, so there are no release notes and no
    changelog to put in it.
    """


def find_release_message(token: str, channel: str, app: str, version: str) -> tuple[str, ReleaseState] | None:
    """Scan recent channel history for the message whose metadata matches (app, version).

    Returns ``(ts, state)`` or ``None``. Matching is on the structured metadata —
    exact and immune to substring collisions (e.g. v3.9.4 vs v3.9.40).

    The metadata carry the identity and the bookkeeping; the release notes are read
    back from the message's own blocks, so the payload stays small enough for Slack to
    keep it (see :data:`..state.METADATA_PAYLOAD_SAFE_BYTES`).
    """
    oldest = str(int(time.time()) - 30 * 86400)
    params = {"channel": channel, "oldest": oldest, "limit": "200", "include_all_metadata": "true"}
    for msg in slack_paginate(token, "conversations.history", params, items_key="messages"):
        meta = msg.get("metadata")
        if not isinstance(meta, dict) or meta.get("event_type") != METADATA_EVENT_TYPE:
            continue
        payload = meta.get("event_payload")
        if isinstance(payload, dict) and payload.get("app") == app and payload.get("version") == version:
            state = ReleaseState.from_payload(payload)
            body = content_from_blocks(msg.get("blocks"))
            if body:
                state.content = body
            return str(msg.get("ts", "")), state
    return None


def _publish(token: str, method: str, payload: dict[str, object]) -> dict[str, object]:
    """POST chat.postMessage/chat.update via the shared client; raises on a Slack-level error."""
    return slack_post(token, method, payload)


def _warn_on_oversized_payload(metadata: dict[str, object]) -> None:
    """Warn on stderr when the metadata payload reaches the size Slack silently drops.

    Slack answers ``ok: true`` and discards the metadata, which costs the message the
    identity it is found by — so the next call posts a duplicate. Making the crossing
    audible in the job log is what turns that into a diagnosable failure rather than a
    surprise duplicate announce days later.
    """
    size = len(json.dumps(metadata.get("event_payload"), ensure_ascii=False).encode("utf-8"))
    if size < METADATA_PAYLOAD_SAFE_BYTES:
        return
    print(
        f"release-status: WARNING metadata payload is {size} bytes, at or past the "
        f"{METADATA_PAYLOAD_SAFE_BYTES}-byte ceiling where Slack drops it silently — this message "
        "is about to lose the (app, version) identity it is found by",
        file=sys.stderr,
    )


def _write(token: str, chan: str, state: ReleaseState, ts: str) -> dict[str, object]:
    """Post (no ts) or edit (ts) the message; self-join #mep once on not_in_channel."""
    metadata = state.to_metadata()
    _warn_on_oversized_payload(metadata)
    payload: dict[str, object] = {
        "channel": chan,
        "text": render_text(state),
        "blocks": render_blocks(state),
        "metadata": metadata,
    }
    if ts:
        payload["ts"] = ts
        return _publish(token, "chat.update", payload)
    try:
        return _publish(token, "chat.postMessage", payload)
    except SlackApiError as e:
        if e.code != "not_in_channel":
            raise
        try:
            slack_post(token, "conversations.join", {"channel": chan})
        except SlackApiError:
            pass
        return _publish(token, "chat.postMessage", payload)


def _sync_replies(token: str, chan: str, parent_ts: str, state: ReleaseState, replies: list[tuple[str, str]]) -> bool:
    """Post or update each thread reply under ``parent_ts``; record its ts in ``state.replies``.

    Idempotent across re-runs: a reply already recorded for its kind is edited in
    place (``chat.update``); a new one is posted (``chat.postMessage`` with
    ``thread_ts``) and its ts stored. Returns ``True`` when a new reply ts was
    recorded, so the caller re-writes the parent message to persist the metadata.
    """
    changed = False
    for kind, text in replies:
        payload: dict[str, object] = {
            "channel": chan,
            "text": REPLY_LABELS.get(kind, kind),
            "blocks": _reply_blocks(text),
        }
        existing_ts = state.replies.get(kind)
        if existing_ts:
            payload["ts"] = existing_ts
            _publish(token, "chat.update", payload)
        else:
            payload["thread_ts"] = parent_ts
            res = _publish(token, "chat.postMessage", payload)
            state.replies[kind] = str(res.get("ts", ""))
            changed = True
    return changed


MAX_SYNC_ATTEMPTS = 5
"""Read-modify-write retries to absorb a concurrent writer clobbering our track."""


def sync_release_status(
    token: str,
    chan: str,
    app: str,
    version: str,
    *,
    track: str | None,
    state_key: str | None,
    content_text: str,
    replies: list[tuple[str, str]] | None = None,
    init_tracks: dict[str, str] | None = None,
    allow_create: bool = True,
) -> tuple[dict[str, object], bool]:
    """Find-or-create the message, apply one update, write it; returns (result, created).

    chat.update has no compare-and-swap, so two jobs updating *different* tracks
    on the same message can race (last-writer-wins). We re-read the message right
    before writing and, after writing, verify our track survived; if a concurrent
    writer clobbered it we re-read their latest state, re-merge our track and write
    again — converging without losing anyone's update. Content-only updates and
    the content itself are not track-specific, so they skip the verify step.

    At most one message is ever posted per call: once a retry has written one, the
    following ones edit *that* ts even if the re-read fails to find it, so a flaky
    read can never turn a retry into a duplicate announce.

    ``init_tracks`` ({track -> initial state}) seeds the tracks a repo declares so
    they all show up at once when the message is first created. It is applied
    **set-if-absent**: a track already present (advanced by a CI job) is never
    regressed to its initial state, so seeding stays safe even if it races a
    milestone update or is re-run.

    Once the main message is settled, any ``replies`` (ordered ``(kind, mrkdwn)``
    pairs — EN, IT, changelog) are posted/updated as thread replies under it
    (idempotent on their kind), and the parent is re-written once if a new reply
    ts had to be recorded in its metadata.

    ``allow_create`` guards the *create* half of find-or-create: pass ``False`` when
    the caller brings no content, so a missing message raises
    :class:`MissingReleaseMessage` instead of posting an empty one.
    """
    result: dict[str, object] = {}
    created = False
    final_state: ReleaseState | None = None
    final_ts = ""
    for _ in range(MAX_SYNC_ATTEMPTS):
        existing = find_release_message(token, chan, app, version)
        if existing is None and final_state is not None and final_ts:
            # This attempt already wrote the message: a read that then misses it is a
            # transient (Slack replication, throttling), never a licence to post a second
            # one. Retry against the ts we hold, with our own last view of the state.
            existing = (final_ts, final_state)
        if existing is None and not allow_create:
            raise MissingReleaseMessage(
                f"no #mep release-status message found for ({app}, {version}) — this call carries no "
                "content (no --root / --content / --init-tracks), so creating one would post an empty "
                "duplicate next to the release announce"
            )
        ts = "" if existing is None else existing[0]
        state = ReleaseState(app=app, version=version) if existing is None else existing[1]
        if content_text:
            state.content = content_text
        for seed_track, seed_state in (init_tracks or {}).items():
            if seed_track not in state.tracks:  # seed only — never regress a track the CI already advanced
                apply_update(state, seed_track, seed_state)
        apply_update(state, track, state_key)
        result = _write(token, chan, state, ts)
        created = created or not ts  # a later retry updates what an earlier one created
        final_state = state
        final_ts = str(result.get("ts") or ts)
        if track is None:
            break
        check = find_release_message(token, chan, app, version)
        if check is not None and check[1].tracks.get(track) == state_key:
            break

    if replies and final_state is not None and final_ts:
        if _sync_replies(token, chan, final_ts, final_state, replies):
            _write(token, chan, final_state, final_ts)
    return result, created


def _fail(error: str, *, code: int, best_effort: bool, **extra: object) -> NoReturn:
    """Report a failure as the one-line JSON plus a stderr line, then exit.

    ``best_effort`` turns the exit code into 0. The #mep announce is accessory to the
    job that posts it — a build has no business failing because Slack was unreachable —
    so the failure stays fully reported (``ok: false`` on stdout, the message on stderr)
    while the pipeline keeps going. Only a *usage* error ignores the flag: an invalid
    track or an unusable invocation is a pipeline bug that would never fix itself if
    silently tolerated.
    """
    payload: dict[str, object] = {"ok": False, "error": error, **extra}
    if best_effort:
        payload["best_effort"] = True
    print(json.dumps(payload))
    print(f"release-status: {error}", file=sys.stderr)
    raise typer.Exit(code=0 if best_effort else code) from None


cli = typer.Typer()


@cli.command()
def main(
    app: Annotated[str, typer.Option("--app", help="App / service name (e.g. info, op).")],
    version: Annotated[str, typer.Option("--version", help="Release version / tag (e.g. v3.9.4).")],
    channel: Annotated[str, typer.Option("--channel", help="Slack channel ID or name (e.g. mep).")] = "mep",
    track: Annotated[
        str,
        typer.Option("--track", help=f"Status track to update, one of {sorted(TRACKS)} (omit for changelog-only)."),
    ] = "",
    state: Annotated[
        str,
        typer.Option("--state", help="New state for --track (see the track's states, or 'failed')."),
    ] = "",
    content: Annotated[
        str,
        typer.Option(
            "--content",
            help="Legacy: a single pre-rendered mrkdwn body to attach to the main message (no replies). "
            "'-' reads stdin. Prefer --root, which also generates the EN/IT/changelog thread replies.",
        ),
    ] = "",
    root: Annotated[
        Path | None,
        typer.Option(
            "--root",
            help="Repo to read the release notes + changelog from: attaches the primary-language (FR) "
            "notes to the main message and posts EN, IT, then the changelog as thread replies.",
        ),
    ] = None,
    init_tracks: Annotated[
        bool,
        typer.Option(
            "--init-tracks",
            help="Seed every track declared in release.tracks (config from --root, else cwd) at its initial "
            "state, so they all appear on the message at once. Set-if-absent: never regresses a track a CI "
            "job already advanced. Use on the release seed job; CI milestones then advance each track.",
        ),
    ] = False,
    best_effort: Annotated[
        bool,
        typer.Option(
            "--best-effort",
            help="Exit 0 even when the announce fails, so a build job is never brought down by Slack "
            "being unreachable, a missing token, or no message to update. The failure is still reported "
            "(ok: false on stdout, the message on stderr). A usage error — invalid --track/--state, or an "
            "invocation with nothing to do — still exits non-zero: that is a pipeline bug, not a transient.",
        ),
    ] = False,
) -> None:
    """Create or update the single #mep release-status message for (app, version)."""
    if not track and not content and root is None and not init_tracks:
        # Usage error: --best-effort deliberately does not cover it (see _fail).
        _fail(
            "nothing to do: pass --track/--state, --content, --root and/or --init-tracks",
            code=1,
            best_effort=False,
        )

    # Honour the per-repo #mep flag: skip cleanly when slack.enabled / notifications.mep
    # is off for this repo (config read from --root, else cwd).
    if not slack_enabled(root if root is not None else Path.cwd(), "mep"):
        print(json.dumps({"ok": True, "skipped": "slack.notifications.mep disabled"}))
        raise typer.Exit(code=0)

    # --root assembles the main content + thread replies from the repo; otherwise
    # --content (if any) is the single legacy main-message body, with no replies.
    replies: list[tuple[str, str]] = []
    if root is not None:
        slack_content = release_slack_content(root, version)
        content_text = slack_content.primary
        replies = slack_content.replies
    else:
        content_text = sys.stdin.read().strip() if content == "-" else content
    track_key = track or None

    # --init-tracks: seed the repo's declared release.tracks at each track's initial state
    # (TRACKS[<track>][0]) so the whole set shows up at once; CI jobs then advance them.
    seed_tracks: dict[str, str] = {}
    if init_tracks:
        cfg = load_project_config(root if root is not None else Path.cwd())
        if cfg is not None:
            seed_tracks = {t.value: TRACKS[t.value][0][0] for t in cfg.release.tracks if t.value in TRACKS}

    # A milestone call (--track/--state alone) brings neither release notes nor changelog:
    # let it update the (app, version) message, never create one. Only a call carrying
    # content — or the track seed — has something to fill a fresh message with.
    allow_create = root is not None or bool(content) or init_tracks

    token = get_slack_token()
    if not token:
        _fail("no Slack token available", code=1, best_effort=best_effort)
    chan = resolve_channel(channel)

    try:
        result, created = sync_release_status(
            token,
            chan,
            app,
            version,
            track=track_key,
            state_key=state or None,
            content_text=content_text,
            replies=replies,
            init_tracks=seed_tracks or None,
            allow_create=allow_create,
        )
    except MissingReleaseMessage as e:
        _fail(str(e), code=2, best_effort=best_effort, created=False)
    except ValueError as e:
        # Unknown track or invalid state: the caller's arguments are wrong, so this stays
        # loud even under --best-effort — nobody would ever notice a tolerated typo.
        _fail(str(e), code=1, best_effort=False)
    except SlackApiError as e:
        _fail(str(e), code=1, best_effort=best_effort)

    print(json.dumps({"ok": True, "ts": result.get("ts"), "channel": result.get("channel"), "created": created}))


if __name__ == "__main__":
    cli()
