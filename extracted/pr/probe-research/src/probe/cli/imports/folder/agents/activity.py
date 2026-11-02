"""fold an agent's event stream into live activity: reads, uploads, usage, refusals of a model or effort."""

from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path


#: Spinner frames. Something has to MOVE while the agent is thinking, or a long
#: quiet turn is indistinguishable from a hang -- the bug this replaced.
_SPIN = "⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏"

#: How an upload is recognised in either agent's event stream.
#:
#: It no longer happens, and that is the point of the comment. Agents stopped
#: running `artifact add` when the two-pass split landed -- the classify pass
#: uploads nothing by design, and an import unit writes a manifest that ONE
#: process enqueues afterwards. So the counter this drove sat at `0/204` for
#: entire runs, in both passes, and looked like a hang on a working import.
#: Kept because a stray `artifact add` is still worth counting if one appears.
_UPLOAD_MARKER = "artifact add"

#: Reads before an ETA is offered. An estimate from two files is noise wearing
#: a number's clothes -- file sizes vary by orders of magnitude and the first
#: reads include the agent's start-up.
_ETA_FLOOR = 5


@dataclass
class Activity:
    """Live state of one agent run, folded from its event stream.

    PROGRESS IS FILES READ, not files uploaded. The denominator is the unit's
    own file list -- exactly what the agent was told to read -- so the fraction
    is real and the ETA derived from it means something. Counting uploads gave
    a permanent zero (see `_UPLOAD_MARKER`).

    `seen` is a set, not a counter: an agent re-reading a file it already read
    must not advance the bar past what it has actually covered.
    """

    total: int
    uploaded: int = 0
    doing: str = "starting up"
    ticks: int = 0
    seen: set = field(default_factory=set)
    queued: bool = False
    #: The agent process was started (and registered): only then is this a
    #: launch to count, and its outcome the agent's.
    started: bool = False
    #: Tokens summed from the run's usage events (`USAGE_FIELDS`), or None while
    #: none has arrived. None is not 0: a run killed before its terminal event
    #: spent tokens nobody counted, and must not read as free.
    usage: dict | None = None
    #: A tool call or a work item has happened, so the run may have written
    #: something (a plan decision, a note). A relaunch is never safe after it.
    acted: bool = False
    #: The setting the agent refused, from its own structured error: "model" or
    #: "effort" (`_refusal`). None for every other failure.
    refused: str | None = None
    #: The effort this launch carried: an effort error is recognised by naming it.
    sent_effort: str | None = None

    @property
    def done(self) -> int:
        """Files covered so far, never more than the denominator.

        Clamped because an agent may legitimately read something outside its
        unit -- a shared config, a README one directory up -- and `14/8` reads
        as a bug in the tool rather than curiosity in the agent.
        """
        return min(len(self.seen) or self.uploaded, self.total) if self.total else 0

    def eta(self, elapsed: float) -> str:
        """`~2:05 left`, or "" when there is not enough to say.

        Deliberately blank rather than optimistic: no reads yet, nothing left
        to do, or too few samples all produce a number that would be invented.
        """
        done = self.done
        if done < _ETA_FLOOR or done >= self.total or elapsed <= 0:
            return ""
        remaining = elapsed * (self.total - done) / done
        mins, secs = divmod(int(remaining), 60)
        return f"~{mins}:{secs:02d} left" if mins < 60 else "~over an hour left"

    def line(self, elapsed: float, width: int = 46) -> str:
        if self.queued:
            return f"  ·  queued · 0/{self.total}" if self.total else "  ·  queued"
        mins, secs = divmod(int(elapsed), 60)
        parts = [
            _SPIN[self.ticks % len(_SPIN)],
            f"{mins}:{secs:02d}",
        ]
        if self.total:
            parts.append(f"· {self.done}/{self.total}")
        eta = self.eta(elapsed)
        if eta:
            parts.append(f"· {eta}")
        head = "  " + " ".join(parts) + " · "
        room = max(12, width - (len(head) - len(f"  {_SPIN[0]} 0:00 · 0/0 · ")))
        doing = self.doing if len(self.doing) <= room else self.doing[: room - 1] + "…"
        return head + doing


#: Commands that mean "the agent looked at this file". Codex has no Read tool
#: event, so its progress has to be read out of the shell it runs.
_READ_COMMANDS = ("cat", "head", "tail", "less", "more", "bat", "sed", "nl")


def _read_target(command: str) -> str | None:
    """The file a read-shaped shell command names, or None.

    Conservative on purpose. Over-counting inflates the bar and the ETA with
    it, so anything ambiguous -- a pipeline, a glob, a flag where the path
    should be -- returns None and simply does not count. An under-reported bar
    catches up; an over-reported one strands at "almost done".
    """
    text = " ".join(command.split())
    for wrapper in ("/bin/zsh -lc ", "/bin/bash -lc ", "/bin/sh -c "):
        if text.startswith(wrapper):
            text = text[len(wrapper) :].strip("'\"")
    if any(ch in text for ch in "|><*?"):
        return None
    parts = text.split()
    if len(parts) < 2 or Path(parts[0]).name not in _READ_COMMANDS:
        return None
    targets = [p for p in parts[1:] if not p.startswith("-")]
    return targets[-1] if len(targets) == 1 else None


def _shorten(command: str) -> str:
    """A shell command as a phrase worth showing on one line.

    The interesting part of `probe artifact add --project <uuid> /long/path`
    is the filename, and the uuid is the least interesting thing in it.
    """
    text = " ".join(command.split())
    for wrapper in ("/bin/zsh -lc ", "/bin/bash -lc ", "/bin/sh -c "):
        if text.startswith(wrapper):
            text = text[len(wrapper) :].strip("'\"")
    if _UPLOAD_MARKER in text:
        parts = [
            p
            for p in text.split()
            if not p.startswith("--") and p not in ("probe", "artifact", "add")
        ]
        # Drop the project id; keep the path.
        paths = [p for p in parts if "/" in p or "." in p]
        return f"uploading {Path(paths[-1]).name}" if paths else "uploading"
    return text


#: The token counts an import records per launch and lane
#: (`import_agent_settings.Meter`). Codex's `turn.completed` carries exactly
#: these; Claude's `result` is mapped onto them (`_usage`) so the two read the
#: same way: input is every prompt token, cache reads and writes included, and
#: output includes reasoning, as both providers bill it.
USAGE_FIELDS = (
    "input_tokens",
    "cached_input_tokens",
    "cache_write_input_tokens",
    "output_tokens",
    "reasoning_output_tokens",
)


def _count(value) -> int:
    """A token count, or 0 for anything that is not a non-negative integer."""
    return value if isinstance(value, int) and not isinstance(value, bool) and value > 0 else 0


def _usage(kind, event: dict) -> dict[str, int] | None:
    """The token counts one terminal event reports, or None if it has none.

    Codex: `{"type":"turn.completed","usage":{"input_tokens":30047,
    "cached_input_tokens":12288,"cache_write_input_tokens":0,"output_tokens":5,
    "reasoning_output_tokens":0}}` (codex-cli 0.164.0). Claude: the `result`
    event's `usage`, whose `input_tokens` EXCLUDES cache reads and writes and
    whose thinking sits in `output_tokens_details` (2.1.296).
    """
    usage = event.get("usage")
    if not isinstance(usage, dict):
        return None
    if kind == "turn.completed":
        return {name: _count(usage.get(name)) for name in USAGE_FIELDS}
    read = _count(usage.get("cache_read_input_tokens"))
    written = _count(usage.get("cache_creation_input_tokens"))
    details = usage.get("output_tokens_details")
    return {
        "input_tokens": _count(usage.get("input_tokens")) + read + written,
        "cached_input_tokens": read,
        "cache_write_input_tokens": written,
        "output_tokens": _count(usage.get("output_tokens")),
        "reasoning_output_tokens": _count(details.get("thinking_tokens")) if isinstance(details, dict) else 0,
    }


def _refusal(kind, event: dict, sent_effort: str | None) -> str | None:
    """"model" or "effort" when this event is the agent refusing that setting.

    Only the agents' structured errors, never prose matching on the tail, and
    only the shapes measured on 2026-10-25:

    * Codex, a model this account cannot use: an `error` and then a
      `turn.failed` whose message is the API's JSON,
      `{"error":{"type":"invalid_request_error","code":"model_not_found",...}}`.
    * Codex, an effort the model does not take: the same two events with
      `invalid_request_error`, "Invalid value: '<effort>'. Supported values
      are: ..." -- recognised by naming the effort this launch sent, or by
      naming reasoning (`param` `reasoning.effort`).
    * Claude, an unknown model: `result` with `is_error` and
      `api_error_status` 404. An effort: 400 naming effort.

    Whether the refused setting was actually SENT is `launch_agent`'s call.
    """
    import json

    if kind == "result":
        if event.get("is_error") is not True:
            return None
        status = event.get("api_error_status")
        if status == 404:
            return "model"
        if status == 400 and "effort" in str(event.get("result") or "").lower():
            return "effort"
        return None
    if kind == "error":
        message = event.get("message")
    elif kind == "turn.failed" and isinstance(event.get("error"), dict):
        message = event["error"].get("message")
    else:
        return None
    try:
        body = json.loads(message) if isinstance(message, str) else None
    except ValueError:
        return None
    error = body.get("error") if isinstance(body, dict) else None
    if not isinstance(error, dict):
        return None
    if error.get("code") == "model_not_found":
        return "model"
    text = f"{error.get('message') or ''} {error.get('param') or ''}"
    if error.get("type") == "invalid_request_error" and (
        "reasoning" in text.lower() or (sent_effort and f"value: '{sent_effort}'" in text)
    ):
        return "effort"
    return None


def _account(kind, event: dict, state: Activity) -> None:
    """The cost and safety half of folding: usage, work done, refusals.

    Separate from the display half below, which returns early on most events.
    """
    if kind in ("assistant", "user"):
        # Claude: a tool call, or the tool result that answers one.
        message = event.get("message")
        content = message.get("content") if isinstance(message, dict) else None
        if isinstance(content, list) and any(
            isinstance(block, dict) and block.get("type") in ("tool_use", "tool_result")
            for block in content
        ):
            state.acted = True
    elif kind in ("item.started", "item.completed"):
        # Codex's own warnings arrive as `error` items before the turn starts
        # ("Model metadata for `x` not found"); every other item is work.
        item = event.get("item")
        if not (isinstance(item, dict) and item.get("type") == "error"):
            state.acted = True
    if kind in ("turn.completed", "result"):
        usage = _usage(kind, event)
        if usage is not None:
            state.usage = {
                name: (state.usage or {}).get(name, 0) + usage[name] for name in USAGE_FIELDS
            }
    refused = _refusal(kind, event, state.sent_effort)
    if refused is not None:
        state.refused = refused


def fold_event(raw: str, state: Activity) -> bool:
    """Fold one stdout line into `state`. True if it said something new.

    Tolerant by construction: both agents interleave NON-JSON on stdout (Claude
    prints the connectors warning there, Codex a stdin notice and tracing), and
    a parser that treated that as fatal would blank the display for the rest of
    the run.

    Also counts what the run cost and whether it refused a setting
    (`_account`); neither changes what the display shows.
    """
    import json

    line = raw.strip()
    if not line or not line.startswith("{"):
        return False
    try:
        event = json.loads(line)
    except ValueError:
        return False
    if not isinstance(event, dict):
        return False

    kind = event.get("type")
    _account(kind, event, state)

    # Claude: assistant turns carry tool_use blocks.
    if kind == "assistant":
        for block in event.get("message", {}).get("content", []) or []:
            if block.get("type") != "tool_use":
                continue
            args = block.get("input") or {}
            name = block.get("name", "")
            if name == "Bash":
                command = str(args.get("command", ""))
                if _UPLOAD_MARKER in command:
                    state.uploaded += 1
                state.doing = str(args.get("description") or _shorten(command))
            elif args.get("file_path"):
                # THE PROGRESS SIGNAL. A unit is told to read a known list of
                # files, so distinct reads against that list is a real fraction
                # -- and the only one available, since agents no longer upload.
                path = str(args["file_path"])
                state.seen.add(path)
                state.doing = f"reading {Path(path).name}"
            elif args.get("pattern"):
                state.doing = f"searching {args['pattern']}"
            else:
                state.doing = name.lower() or "working"
            return True
        return False

    # Codex: item.started / item.completed carry command_execution + messages.
    if kind in ("item.started", "item.completed"):
        item = event.get("item") or {}
        if item.get("type") == "command_execution":
            command = str(item.get("command", ""))
            if kind == "item.started":
                if _UPLOAD_MARKER in command:
                    state.uploaded += 1
                # Codex reads by shelling out, so its progress signal is the
                # file a read-shaped command names -- there is no Read tool
                # event to count. Same denominator, same fraction.
                read = _read_target(command)
                if read:
                    state.seen.add(read)
                state.doing = _shorten(command)
                return True
        elif item.get("type") == "agent_message" and kind == "item.completed":
            text = " ".join(str(item.get("text", "")).split())
            if text:
                state.doing = text
                return True
        return False

    if kind == "turn.started":
        state.doing = "thinking"
        return True
    return False
