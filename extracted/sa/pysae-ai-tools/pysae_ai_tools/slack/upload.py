"""Slack external file-upload flow + delete — shared by ``upload-file`` and ``release-file``.

Slack sunset the old single-shot ``files.upload`` (March 2025). Uploads now go through
three steps, all wrapped by :func:`upload_file`:

1. ``files.getUploadURLExternal`` (filename + exact byte length) → a one-shot
   ``upload_url`` + ``file_id``,
2. a plain ``POST`` of the raw file bytes to that ``upload_url`` (no multipart, no
   special headers — same as the official slack_sdk ``files_upload_v2``),
3. ``files.completeUploadExternal`` (``file_id`` + title, ``channel_id``, optional
   ``thread_ts`` / ``initial_comment``) → posts the message carrying the file, in the
   thread when ``thread_ts`` is given.

The token needs the ``files:write`` scope.
"""

import urllib.request
from pathlib import Path

from .client import SlackApiError, slack_get, slack_post

# files.completeUploadExternal can be slow to acknowledge a large binary; allow more
# than the 10s the chat helpers use, since an APK is several tens of MB.
UPLOAD_TIMEOUT = 180


def _post_bytes(upload_url: str, data: bytes) -> None:
    """POST the raw file bytes to the pre-issued Slack upload URL (no special headers)."""
    req = urllib.request.Request(upload_url, data=data, method="POST")
    with urllib.request.urlopen(req, timeout=UPLOAD_TIMEOUT) as resp:
        resp.read()


def upload_file(
    token: str,
    file_path: Path,
    *,
    channel: str,
    filename: str = "",
    title: str = "",
    initial_comment: str = "",
    thread_ts: str = "",
    join: bool = False,
) -> dict[str, object]:
    """Upload one file via the external flow; return the ``completeUploadExternal`` response.

    ``filename`` / ``title`` default to the file's basename. With ``thread_ts`` the file
    message lands in that thread. With ``join``, self-join the (public) channel on
    ``not_in_channel`` and retry the finalize once — the same self-healing broadcast
    pattern as :func:`post_message_joining`. The returned dict carries the Slack
    ``file_id`` under the ``file_id`` key (so callers can later delete/replace it).
    """
    content = file_path.read_bytes()
    name = filename or file_path.name

    url_resp = slack_get(token, "files.getUploadURLExternal", {"filename": name, "length": str(len(content))})
    upload_url = str(url_resp["upload_url"])
    file_id = str(url_resp["file_id"])

    _post_bytes(upload_url, content)

    payload: dict[str, object] = {"files": [{"id": file_id, "title": title or name}], "channel_id": channel}
    if initial_comment:
        payload["initial_comment"] = initial_comment
    if thread_ts:
        payload["thread_ts"] = thread_ts

    try:
        result = slack_post(token, "files.completeUploadExternal", payload)
    except SlackApiError as e:
        if not (join and e.code == "not_in_channel"):
            raise
        try:
            slack_post(token, "conversations.join", {"channel": channel})
        except SlackApiError:
            pass
        result = slack_post(token, "files.completeUploadExternal", payload)

    result["file_id"] = file_id
    return result


def delete_file(token: str, file_id: str) -> None:
    """Best-effort delete of a previously uploaded file (used to replace a file by kind).

    Swallows Slack/transport errors: a failed delete must never abort the fresh upload
    that follows it — at worst the thread keeps a stale copy, which the new file supersedes.
    """
    try:
        slack_post(token, "files.delete", {"file": file_id})
    except SlackApiError:
        pass


def delete_message(token: str, channel: str, ts: str) -> None:
    """Best-effort delete of a message the bot posted (e.g. a superseded file reply).

    Deleting the file alone leaves a "this file was deleted" tombstone reply in the
    thread, so a replace also removes the message that carried it. Swallows Slack/transport
    errors for the same reason as :func:`delete_file`.
    """
    try:
        slack_post(token, "chat.delete", {"channel": channel, "ts": ts})
    except SlackApiError:
        pass
