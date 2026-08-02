"""Attach a file (e.g. a built APK) to the #mep release-status thread of (app, version).

This is the file-upload sibling of ``slack release-status``: it finds the single
release-status message for ``(app, version)`` by its metadata — creating a minimal
header-only parent on demand if no milestone job has posted it yet — and uploads the
file as a reply in that message's thread, so the binaries sit next to the release notes
and the per-track status.

Each file is keyed by a ``--kind`` tag (e.g. ``apk-prod``, ``apk-dev``) recorded in the
parent message metadata. Re-running for the same kind (a retried ``build_apk_<env>`` job)
deletes the previously uploaded file and re-uploads — the thread stays free of duplicates
and always shows the latest binary. Different kinds coexist as separate replies.

Usage:
    pysae-ai-tools slack release-file --app driver --version "$CI_COMMIT_TAG" \\
        --channel mep --file build/app-prod.apk --kind apk-prod \\
        --title "Driver prod" --comment ":package: APK prod"

Uses :func:`pysae_ai_tools.slack.common.get_slack_token` for authentication (user token
locally, bot token in CI); the token must hold the ``files:write`` scope.

Output (JSON, one line):
    {"ok": true, "file_id": "F...", "ts": "<parent ts>", "channel": "C...", "replaced": false}
    {"ok": false, "error": "..."}
"""

import json
from pathlib import Path
from typing import Annotated

import typer

from ..common.project_config import slack_enabled
from .client import SlackApiError, slack_get
from .common import get_slack_token, resolve_channel
from .release_status.cli import MAX_SYNC_ATTEMPTS, _write, find_release_message
from .release_status.state import ReleaseState
from .upload import delete_file, delete_message, upload_file


def _find_file_reply_ts(token: str, channel: str, parent_ts: str, file_id: str) -> str | None:
    """Find the ts of the thread reply that carries ``file_id``, or None.

    Used to remove a superseded file *message* (not just the file) on replace: a deleted
    file leaves a tombstone reply that still lists its id, so we scan the thread for the
    message referencing ``file_id`` and hand its ts to ``chat.delete``. Best-effort —
    returns None on any Slack/transport error so a replace never aborts the new upload.
    """
    try:
        data = slack_get(token, "conversations.replies", {"channel": channel, "ts": parent_ts, "limit": "200"})
    except SlackApiError:
        return None
    messages = data.get("messages")
    if not isinstance(messages, list):
        return None
    for msg in messages:
        if not isinstance(msg, dict):
            continue
        files = msg.get("files")
        if isinstance(files, list) and any(isinstance(f, dict) and f.get("id") == file_id for f in files):
            ts = msg.get("ts")
            return str(ts) if ts is not None else None
    return None


def attach_release_file(
    token: str,
    chan: str,
    app: str,
    version: str,
    *,
    file_path: Path,
    kind: str,
    title: str,
    comment: str,
) -> tuple[dict[str, object], bool, str]:
    """Find-or-create the (app, version) parent, then upload ``file_path`` into its thread.

    Returns ``(result, replaced, parent_ts)`` where ``result`` is the completeUploadExternal
    response (with ``file_id``), ``replaced`` is True when a previous file of the same
    ``kind`` was deleted first, and ``parent_ts`` is the thread the file was attached to.

    The new file id is persisted under ``kind`` in the parent message metadata with the
    same read-modify-write retry as ``sync_release_status``: we re-read the latest state
    right before writing so a track update racing on the same message is preserved instead
    of being clobbered by our metadata write.
    """
    existing = find_release_message(token, chan, app, version)
    if existing is None:
        # No milestone job has posted the release message yet — create a minimal
        # header-only parent (no tracks, no content) to anchor the thread. _write
        # self-joins the channel on not_in_channel.
        seed = ReleaseState(app=app, version=version)
        created = _write(token, chan, seed, "")
        parent_ts = str(created.get("ts", ""))
        state = seed
    else:
        parent_ts, state = existing

    old_id = state.files.get(kind)
    replaced = bool(old_id)

    # Upload the new file first so the thread never sits empty for this kind, then
    # remove the superseded one.
    result = upload_file(
        token,
        file_path,
        channel=chan,
        title=title,
        initial_comment=comment,
        thread_ts=parent_ts,
        join=True,
    )
    file_id = str(result.get("file_id", ""))

    # Replace: drop the previous file *and* the reply that carried it (else a tombstone
    # "this file was deleted" message lingers in the thread). Delete the message first —
    # chat.delete also unshares its file — then files.delete as a belt-and-suspenders.
    if old_id:
        old_reply_ts = _find_file_reply_ts(token, chan, parent_ts, old_id)
        if old_reply_ts:
            delete_message(token, chan, old_reply_ts)
        delete_file(token, old_id)

    # Persist file_id -> kind in the parent metadata, re-reading to absorb a concurrent
    # track writer (chat.update has no compare-and-swap).
    for _ in range(MAX_SYNC_ATTEMPTS):
        fresh = find_release_message(token, chan, app, version)
        cur_state = fresh[1] if fresh is not None else state
        cur_ts = fresh[0] if fresh is not None else parent_ts
        cur_state.files[kind] = file_id
        _write(token, chan, cur_state, cur_ts)
        check = find_release_message(token, chan, app, version)
        if check is not None and check[1].files.get(kind) == file_id:
            break

    return result, replaced, parent_ts


cli = typer.Typer()


@cli.command()
def main(
    app: Annotated[str, typer.Option("--app", help="App / service name (e.g. driver, info).")],
    version: Annotated[str, typer.Option("--version", help="Release version / tag (e.g. v6.0.0).")],
    file: Annotated[
        Path,
        typer.Option("--file", help="Path to the file to attach.", exists=True, dir_okay=False, readable=True),
    ],
    channel: Annotated[str, typer.Option("--channel", help="Slack channel ID or name (e.g. mep).")] = "mep",
    kind: Annotated[
        str,
        typer.Option(
            "--kind",
            help="Stable tag identifying this file slot (e.g. apk-prod, apk-dev). Re-running with the same "
            "kind replaces the previous file. Defaults to the file's basename without extension.",
        ),
    ] = "",
    title: Annotated[
        str,
        typer.Option("--title", help="File title shown in Slack (defaults to the filename)."),
    ] = "",
    comment: Annotated[
        str,
        typer.Option("--comment", help="Optional message text posted alongside the file (initial_comment)."),
    ] = "",
) -> None:
    """Attach a file to the #mep release-status thread for (app, version)."""
    # Honour the per-repo #mep flag: skip cleanly when slack.enabled / notifications.mep
    # is off for this repo (same gate as release-status).
    if not slack_enabled(Path.cwd(), "mep"):
        print(json.dumps({"ok": True, "skipped": "slack.notifications.mep disabled"}))
        raise typer.Exit(code=0)

    token = get_slack_token()
    if not token:
        print(json.dumps({"ok": False, "error": "no Slack token available"}))
        raise typer.Exit(code=1)

    chan = resolve_channel(channel)
    file_kind = kind or file.stem

    try:
        result, replaced, parent_ts = attach_release_file(
            token,
            chan,
            app,
            version,
            file_path=file,
            kind=file_kind,
            title=title,
            comment=comment,
        )
    except (SlackApiError, OSError) as e:
        print(json.dumps({"ok": False, "error": str(e)}))
        raise typer.Exit(code=1) from None

    print(
        json.dumps(
            {
                "ok": True,
                "file_id": result.get("file_id"),
                "ts": parent_ts,
                "channel": chan,
                "replaced": replaced,
            }
        )
    )


if __name__ == "__main__":
    cli()
