"""Flip a MR's state line on its Slack review message (Ouverte → Mergée / Fermée).

Finds the review/AI-validation message for a GitLab MR (by its structured
metadata, like ``slack ask-review``) and rewrites the MR-state line — posted as
``:large_green_circle: Ouverte`` — to ``:twisted_rightwards_arrows: Mergée``
(default) or ``:red_circle: Fermée`` (``--state closed``). The line is flipped in
place so the message keeps a stable line count. Idempotent: re-running does
nothing once the line already shows the target state. No-op (not an error) when no
message exists.

Usage:
    pysae-ai-tools slack mark-merged \\
        --channel C0123ABCDEF \\
        --project-url https://gitlab.com/pysae/api \\
        --mr-iid 42 [--state merged|closed]

Output (JSON, one line):
    {"ok": true, "updated": true, "ts": "..."}
    {"ok": true, "updated": false, "reason": "already-marked"}
    {"ok": true, "found": false}
"""

import json
import urllib.error
from typing import Annotated

import typer

from .ask_review import fetch_and_search
from .common import describe_slack_error, get_slack_token, log_not_posted
from .update_message import update_message

OPEN_LINE = ":large_green_circle: Ouverte"
MERGED_LINE = ":twisted_rightwards_arrows: Mergée"
CLOSED_LINE = ":red_circle: Fermée"

# The three MR-state segments, longest-first so a future overlap can't shadow a
# longer match. The state lives inline in the header line (``… — :…: Ouverte``),
# so we replace the *segment* wherever it sits, not a whole line.
_MR_STATE_SEGMENTS = (OPEN_LINE, MERGED_LINE, CLOSED_LINE)


def set_mr_state_line(text: str, new_line: str) -> str:
    """Flip the MR-state segment (Ouverte/Mergée/Fermée) to ``new_line`` in place.

    The state ``:picto: Label`` is embedded in the header line after an em dash;
    we swap that exact segment so the surrounding text ("MR pour <project> — …")
    is preserved and the line/character layout stays stable. Idempotent (returns
    ``text`` unchanged when it already shows ``new_line``). Legacy fallback for
    messages posted before the state segment existed: insert ``new_line`` just
    above the MR-link line.
    """
    if new_line in text:
        return text
    for segment in _MR_STATE_SEGMENTS:
        if segment in text:
            return text.replace(segment, new_line, 1)
    # Legacy (no state segment): insert just above the MR link.
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if "/-/merge_requests/" in line:
            lines.insert(i, new_line)
            return "\n".join(lines)
    lines.insert(1 if len(lines) > 1 else len(lines), new_line)
    return "\n".join(lines)


def set_mr_state_in_blocks(blocks: list[dict[str, object]], new_line: str) -> list[dict[str, object]] | None:
    """Return a copy of ``blocks`` with the MR-state line flipped to ``new_line``
    inside the first ``section`` block (the message body), or ``None`` if nothing
    to do.

    The review message is posted by ``slack post-message --ai-footer`` as
    ``[section(body), divider, context(footer)]``. We must edit the ``section`` in
    place and re-send **all** blocks on ``chat.update`` — sending only ``text``
    would drop the blocks and flatten the message. Returns ``None`` when the line
    already shows ``new_line`` (idempotent) or when no editable section block is
    found (caller then falls back to the text path).
    """
    import copy

    out = copy.deepcopy(blocks)
    for block in out:
        if block.get("type") != "section":
            continue
        text_obj = block.get("text")
        if not (isinstance(text_obj, dict) and isinstance(text_obj.get("text"), str)):
            continue
        if new_line in text_obj["text"]:
            return None
        text_obj["text"] = set_mr_state_line(text_obj["text"], new_line)
        return out
    return None


cli = typer.Typer()


@cli.command()
def main(
    channel: Annotated[str, typer.Option("--channel", help="Slack channel ID")],
    project_url: Annotated[
        str, typer.Option("--project-url", help="GitLab project URL (e.g. https://gitlab.com/pysae/api)")
    ],
    mr_iid: Annotated[int, typer.Option("--mr-iid", help="GitLab MR IID")],
    state: Annotated[str, typer.Option("--state", help="Target MR state: 'merged' (default) or 'closed'.")] = "merged",
) -> None:
    """Flip the MR-state line on the MR's Slack message (merged / closed)."""
    token = get_slack_token()
    if not token:
        log_not_posted("no Slack token available — cannot update the MR's Slack message")
        print(json.dumps({"ok": False, "error": "no Slack token available"}))
        raise typer.Exit(code=1)

    if not channel.strip():
        log_not_posted(
            "target channel is empty — is the tech channel configured? "
            "(check `pysae-ai-tools project show slack.tech_channel_id`)"
        )
        print(json.dumps({"ok": False, "error": "empty channel"}))
        raise typer.Exit(code=1)

    if state not in ("merged", "closed"):
        print(json.dumps({"ok": False, "error": "--state must be 'merged' or 'closed'"}))
        raise typer.Exit(code=1)
    new_line = CLOSED_LINE if state == "closed" else MERGED_LINE

    try:
        match = fetch_and_search(token, channel, project_url, mr_iid)
    except (RuntimeError, urllib.error.URLError) as e:
        log_not_posted(f"could not search Slack for the MR message: {e}")
        print(json.dumps({"ok": False, "error": str(e)}))
        raise typer.Exit(code=1) from None

    if not match.found:
        # No Slack message for this MR — nothing to update, not an error.
        log_not_posted(f"no existing Slack review message found for MR !{mr_iid} — nothing to update")
        print(json.dumps({"ok": True, "found": False}))
        return

    new_text = set_mr_state_line(match.text, new_line)

    # Preserve the message's blocks: the review message lives in blocks
    # (section + divider + AI-footer context). Updating with `text` only would
    # drop them and flatten the rendering. Edit the section block and re-send
    # all blocks; fall back to text only when the message has no blocks.
    payload: dict[str, object] = {"channel": channel, "ts": match.ts, "text": new_text}
    new_blocks = set_mr_state_in_blocks(match.blocks, new_line) if match.blocks else None
    if new_blocks is not None:
        payload["blocks"] = new_blocks
    elif new_text == match.text:
        # No blocks to edit and the text already carries the merged line.
        print(json.dumps({"ok": True, "updated": False, "reason": "already-marked", "ts": match.ts}))
        return

    try:
        result = update_message(token, payload)
    except urllib.error.URLError as e:
        log_not_posted(f"network error reaching Slack: {e}")
        print(json.dumps({"ok": False, "error": str(e)}))
        raise typer.Exit(code=1) from None

    if not result.get("ok"):
        code = str(result.get("error", "unknown"))
        log_not_posted(f"Slack rejected the update: {describe_slack_error(code)}")
        print(json.dumps({"ok": False, "error": code}))
        raise typer.Exit(code=1)

    print(json.dumps({"ok": True, "updated": True, "ts": match.ts}))


if __name__ == "__main__":
    cli()
