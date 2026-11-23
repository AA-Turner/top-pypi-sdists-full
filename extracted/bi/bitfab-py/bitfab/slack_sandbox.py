from __future__ import annotations

import copy
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable
from contextvars import ContextVar
from dataclasses import dataclass
from typing import Any

from bitfab import service_calls
from bitfab.mock_override import MockOverrideCtx, SpanNodeMeta
from bitfab.sandbox import (
    Sandbox,
    SandboxStartCtx,
    fail_replay_item,
    parse_timestamp,
    sandbox_now,
)

SLACK_SANDBOX_NAME = "Slack"
SLACK_INTEGRATION = "slack"
SLACK_SPAN_PREFIX = "slack."
READ_REAL_WRITE_FAKE = "read-real-write-fake"
RECORDED = "recorded"
SLACK_MODES = (READ_REAL_WRITE_FAKE, RECORDED)
MODELED_READS = ("conversations.history", "conversations.replies")
UNMATCHED_PARAMS = frozenset({"latest", "inclusive", "token"})
IDENTITY_PARAMS = (
    "channel",
    "ts",
    "user",
    "email",
    "query",
    "file",
    "types",
    "message_ts",
    "timestamp",
    "channel_id",
    "team_id",
    "name",
)
WEBHOOK_METHOD = "webhook.post"
DEFAULT_HISTORY_LIMIT = 100
CURSOR_PREFIX = "bitfab-offset:"
TOKEN_ENV = "BITFAB_SLACK_TOKEN"
DEFAULT_API_URL = "https://slack.com/api/"
TIMEOUT_SECONDS = 60.0
MAX_RATE_LIMIT_RETRIES = 3
MAX_RATE_LIMIT_WAIT_SECONDS = 30.0
MICROS_PER_SECOND = 1_000_000
TRUE_VALUES = (True, 1, "1", "true")

REFUSED_CREDENTIAL_ERRORS = frozenset(
    {
        "invalid_auth",
        "not_authed",
        "account_inactive",
        "token_revoked",
        "token_expired",
    }
)

READ_METHODS = frozenset(
    {
        "assistant.search.context",
        "dnd.teamInfo",
        "team.accessLogs",
        "team.billableInfo",
        "team.integrationLogs",
        "users.conversations",
        "users.identity",
    }
)

READ_SUFFIXES = (
    ".list",
    ".info",
    ".get",
    ".history",
    ".replies",
    ".members",
    ".lookupByEmail",
    ".getPresence",
    ".getPermalink",
    ".test",
)

WRITES_ANSWERED_OK = frozenset(
    {
        "assistant.threads.setStatus",
        "assistant.threads.setSuggestedPrompts",
        "assistant.threads.setTitle",
        "bookmarks.add",
        "bookmarks.edit",
        "bookmarks.remove",
        "chat.deleteScheduledMessage",
        "chat.unfurl",
        "conversations.archive",
        "conversations.close",
        "conversations.invite",
        "conversations.join",
        "conversations.kick",
        "conversations.leave",
        "conversations.mark",
        "conversations.rename",
        "conversations.setPurpose",
        "conversations.setTopic",
        "conversations.unarchive",
        "dnd.endDnd",
        "dnd.endSnooze",
        "dnd.setSnooze",
        "files.delete",
        "functions.completeError",
        "functions.completeSuccess",
        "pins.add",
        "pins.remove",
        "reminders.add",
        "reminders.complete",
        "reminders.delete",
        "stars.add",
        "stars.remove",
        "users.profile.set",
        "users.setPresence",
    }
)

Transport = Callable[[str, str, dict[str, Any]], tuple[int, float | None, Any]]

reading_slack: ContextVar[bool] = ContextVar("bitfab_reading_slack", default=False)


@dataclass(frozen=True)
class SlackCallAccess:
    token: str | None = None
    api_url: str | None = None


class SlackCredentialError(RuntimeError):
    pass


class SlackCallRefusedError(RuntimeError):
    pass


class SlackCutoffError(RuntimeError):
    pass


class SlackNotRecordedError(RuntimeError):
    pass


class SlackModeError(ValueError):
    pass


def _form_body(params: dict[str, Any]) -> bytes:
    form = {
        key: value if isinstance(value, str) else json.dumps(value)
        for key, value in params.items()
        if value is not None
    }
    return urllib.parse.urlencode(form).encode("utf-8")


def _decoded(raw: bytes) -> Any:
    try:
        return json.loads(raw.decode("utf-8")) if raw else {}
    except (UnicodeDecodeError, ValueError):
        return {}


def _retry_after(headers: Any) -> float | None:
    try:
        return float(headers.get("Retry-After"))
    except (TypeError, ValueError):
        return None


def urllib_transport(
    url: str, token: str, params: dict[str, Any]
) -> tuple[int, float | None, Any]:
    request = urllib.request.Request(
        url,
        data=_form_body(params),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
        },
    )
    reading = reading_slack.set(True)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.status, None, _decoded(response.read())
    except urllib.error.HTTPError as error:
        return error.code, _retry_after(error.headers), _decoded(error.read())
    finally:
        reading_slack.reset(reading)


def _text(value: Any) -> str | None:
    return value if isinstance(value, str) and value != "" else None


def _records(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [entry for entry in value if isinstance(entry, dict)]


def _structured(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except ValueError:
        return value


def _slack_ts(micros: int) -> str:
    return f"{micros // MICROS_PER_SECOND}.{micros % MICROS_PER_SECOND:06d}"


def _micros_of(ts: Any) -> int:
    return round(float(ts) * MICROS_PER_SECOND)


def _is_after(ts: Any, bound: str) -> bool:
    return isinstance(ts, str) and _micros_of(ts) > _micros_of(bound)


def is_slack_write(call: MockOverrideCtx) -> bool:
    return not _is_read(call.node.trace_function_key[len(SLACK_SPAN_PREFIX) :])


def _is_read(method: str) -> bool:
    return (
        method in READ_METHODS
        or method.startswith("search.")
        or method.endswith(READ_SUFFIXES)
    )


def start_state(ctx: SandboxStartCtx) -> dict[str, Any]:
    started_at = parse_timestamp(ctx.trace_started_at)
    if started_at is None:
        unknown = SlackCutoffError(
            "The Slack sandbox cannot read the real workspace for this replay: "
            "the original trace's start time is not known, so messages posted "
            "after it cannot be left out."
        )
        fail_replay_item(unknown)
        raise unknown
    return {
        **_empty_state(READ_REAL_WRITE_FAKE),
        "cutoff": _slack_ts(round(started_at.timestamp() * MICROS_PER_SECOND)),
    }


def _empty_state(mode: str) -> dict[str, Any]:
    return {
        "mode": mode,
        "cutoff": None,
        "lastTs": None,
        "identity": None,
        "messages": {},
        "edits": {},
        "deleted": {},
        "reactions": {},
        "channels": {},
        "files": [],
        "otherWrites": [],
        "liveReads": [],
    }


def _slack_method(span: Any) -> str | None:
    key = span.trace_function_key or span.span_name or ""
    return key[len(SLACK_SPAN_PREFIX) :] if key.startswith(SLACK_SPAN_PREFIX) else None


def _written_ts(output: dict[str, Any]) -> str | None:
    message = output.get("message") if isinstance(output.get("message"), dict) else {}
    return _text(output.get("ts")) or _text(message.get("ts"))


def _recorded_calls(ctx: SandboxStartCtx) -> list[tuple[str, dict[str, Any], Any]]:
    found = []
    for span in ctx.recorded_spans(prefix=SLACK_SPAN_PREFIX):
        method = _slack_method(span)
        if method is not None:
            params = span.input if isinstance(span.input, dict) else {}
            found.append((method, params, span.output))
    return found


def _modeled_channels(
    reads: list[dict[str, Any]], written: set[str]
) -> dict[str, list[dict[str, Any]]]:
    channels: dict[str, dict[str, dict[str, Any]]] = {}
    for read in reads:
        channel = _text(read["params"].get("channel"))
        if read["method"] not in MODELED_READS or channel is None:
            continue
        if read["response"].get("ok") is not True:
            continue
        bucket = channels.setdefault(channel, {})
        for message in _records(read["response"].get("messages")):
            ts = _text(message.get("ts"))
            if ts is not None and ts not in written:
                bucket[ts] = message
    return {
        channel: [bucket[ts] for ts in sorted(bucket, key=_micros_of)]
        for channel, bucket in channels.items()
    }


def _latest_seen(channels: dict[str, list[dict[str, Any]]]) -> str:
    seen = [_micros_of(m["ts"]) for messages in channels.values() for m in messages]
    return _slack_ts(max(seen, default=0))


def recorded_start_state(ctx: SandboxStartCtx) -> dict[str, Any]:
    """The Slack sandbox's ``start`` in ``"recorded"`` mode: the workspace the original run read.

    Takes every Slack read the original trace recorded. Messages from its
    ``conversations.history`` and ``conversations.replies`` replies make up
    each channel, leaving out messages the original run posted itself, so a
    replay that reads a channel or thread in a new way is still answered.
    Every other read is answered with the recorded reply to the same call.
    """
    calls = _recorded_calls(ctx)
    written = {
        ts
        for method, _params, output in calls
        if not _is_read(method) and isinstance(output, dict)
        for ts in [_written_ts(output)]
        if ts is not None
    }
    reads = [
        {"method": method, "params": params, "response": output}
        for method, params, output in calls
        if _is_read(method) and isinstance(output, dict)
    ]
    channels = _modeled_channels(reads, written)
    poster = next(
        (
            output["message"]
            for method, _params, output in calls
            if method == "chat.postMessage"
            and isinstance(output, dict)
            and isinstance(output.get("message"), dict)
            and _text(output["message"].get("user"))
        ),
        None,
    )
    if poster is not None and not any(r["method"] == "auth.test" for r in reads):
        reads.append(
            {
                "method": "auth.test",
                "params": {},
                "response": {
                    "ok": True,
                    "user_id": poster["user"],
                    **({"bot_id": poster["bot_id"]} if poster.get("bot_id") else {}),
                },
            }
        )
    started_at = parse_timestamp(ctx.trace_started_at)
    cutoff = (
        _slack_ts(round(started_at.timestamp() * MICROS_PER_SECOND))
        if started_at is not None
        else _latest_seen(channels)
    )
    return {
        **_empty_state(RECORDED),
        "cutoff": cutoff,
        "recordedReads": reads,
        "recordedChannels": channels,
        "readsFromTrace": [],
    }


def _recorded_reads_in(value: Any) -> list[dict[str, Any]]:
    return [
        {
            "method": read["method"],
            "params": read["params"] if isinstance(read.get("params"), dict) else {},
            "response": read["response"],
        }
        for read in _records(value)
        if isinstance(read.get("method"), str)
        and isinstance(read.get("response"), dict)
    ]


def load_slack_state(mode: str) -> Callable[[SandboxStartCtx, Any], dict[str, Any]]:
    def load(ctx: SandboxStartCtx, value: Any) -> dict[str, Any]:
        given = value if isinstance(value, dict) else {}
        stored = given.get("mode") or RECORDED
        if stored != mode:
            raise SlackModeError(
                f'The sandbox store holds a Slack workspace from mode="{stored}", '
                f'and this replay runs the Slack sandbox in mode="{mode}". Replay '
                f'in mode="{stored}", or seed the store\'s Slack entry again.'
            )
        started_at = parse_timestamp(ctx.trace_started_at)
        channels = {
            channel: sorted(_records(messages), key=lambda m: _micros_of(m["ts"]))
            for channel, messages in (given.get("recordedChannels") or {}).items()
        }
        cutoff = given.get("cutoff") or (
            _slack_ts(round(started_at.timestamp() * MICROS_PER_SECOND))
            if started_at is not None
            else _latest_seen(channels)
        )
        base = _empty_state(mode)
        loaded = {**base, **given, "cutoff": cutoff, "recordedChannels": channels}
        if mode == RECORDED:
            loaded["recordedReads"] = _recorded_reads_in(given.get("recordedReads"))
            loaded["readsFromTrace"] = _records(given.get("readsFromTrace"))
        return loaded

    return load


def _read_key(params: dict[str, Any]) -> str:
    kept = {
        k: v
        for k, v in params.items()
        if v is not None
        and k not in UNMATCHED_PARAMS
        and not (k == "cursor" and not _text(v))
    }
    return json.dumps(kept, sort_keys=True, default=str)


def _same_identity(asked: dict[str, Any], recorded: dict[str, Any]) -> bool:
    if not any(asked.get(name) is not None for name in IDENTITY_PARAMS):
        return False
    if _text(asked.get("cursor")) != _text(recorded.get("cursor")):
        return False
    return all(asked.get(name) == recorded.get(name) for name in IDENTITY_PARAMS)


def _in_range(ts: Any, params: dict[str, Any]) -> bool:
    latest = _text(params.get("latest"))
    oldest = _text(params.get("oldest"))
    return not (latest and _is_after(ts, latest)) and not (
        oldest and not _is_after(ts, oldest)
    )


def _offset(params: dict[str, Any]) -> int:
    cursor = _text(params.get("cursor")) or ""
    if not cursor.startswith(CURSOR_PREFIX):
        return 0
    try:
        offset = int(cursor[len(CURSOR_PREFIX) :])
    except ValueError:
        return 0
    return max(offset, 0)


def _limit(params: dict[str, Any]) -> int:
    value = params.get("limit")
    if value is None:
        return DEFAULT_HISTORY_LIMIT
    try:
        limit = float(value)
    except (TypeError, ValueError):
        return DEFAULT_HISTORY_LIMIT
    return int(limit) if limit.is_integer() and limit >= 1 else DEFAULT_HISTORY_LIMIT


def _page_of(messages: list[dict[str, Any]], params: dict[str, Any]) -> dict[str, Any]:
    start = _offset(params)
    end = start + _limit(params)
    page: dict[str, Any] = {
        "ok": True,
        "messages": messages[start:end],
        "has_more": end < len(messages),
    }
    if end < len(messages):
        page["response_metadata"] = {"next_cursor": f"{CURSOR_PREFIX}{end}"}
    return page


def _modeled_answer(
    state: dict[str, Any], method: str, params: dict[str, Any]
) -> dict[str, Any] | None:
    channel = _text(params.get("channel"))
    messages = (state.get("recordedChannels") or {}).get(channel or "")
    if messages is None:
        return None
    shown = [m for m in messages if _in_range(m.get("ts"), params)]
    if method == "conversations.history":
        top = [
            m
            for m in shown
            if m.get("thread_ts") in (None, m.get("ts"))
            or m.get("subtype") == "thread_broadcast"
        ]
        return _page_of(list(reversed(top)), params)
    root = _text(params.get("ts"))
    if root is None:
        return None
    thread = [m for m in shown if root in (m.get("ts"), m.get("thread_ts"))]
    if not thread:
        return None
    return _page_of(thread, params)


def recorded_answer(
    state: dict[str, Any], method: str, params: dict[str, Any]
) -> dict[str, Any] | None:
    if method in MODELED_READS:
        modeled = _modeled_answer(state, method, params)
        if modeled is not None:
            return modeled
    same_method = [
        read for read in state.get("recordedReads") or [] if read["method"] == method
    ]
    key = _read_key(params)
    exact = next((r for r in same_method if _read_key(r["params"]) == key), None)
    if exact is not None:
        return exact["response"]
    close = next((r for r in same_method if _same_identity(params, r["params"])), None)
    return close["response"] if close is not None else None


class SlackCall:
    def __init__(
        self,
        state: dict[str, Any],
        method: str,
        params: dict[str, Any],
        access: SlackCallAccess,
        token: str | None,
        api_url: str | None,
        transport: Transport,
    ) -> None:
        self.state = state
        self.method = method
        self.params = params
        self.access = access
        self.token_option = token
        self.api_url_option = api_url
        self.transport = transport

    def answer(self) -> dict[str, Any]:
        handler = self._handlers().get(self.method)
        if handler is not None:
            return handler()
        if _is_read(self.method):
            return self._live(self.method, self.params)
        if self.method in WRITES_ANSWERED_OK:
            return self._keep_write({"ok": True})
        refused = SlackCallRefusedError(
            f"The Slack sandbox does not know {self.method}, so it refused the "
            "call instead of sending it to Slack. Answer it with your own "
            "sandbox in replay's sandboxes, or mock the function that makes "
            "the call."
        )
        fail_replay_item(refused)
        raise refused

    def _handlers(self) -> dict[str, Callable[[], dict[str, Any]]]:
        return {
            "chat.postMessage": self._post_message,
            "chat.meMessage": self._post_message,
            "chat.postEphemeral": lambda: self._keep_write(
                {"ok": True, "message_ts": self._next_ts()}
            ),
            "chat.scheduleMessage": self._schedule_message,
            "chat.update": self._update_message,
            "chat.delete": self._delete_message,
            "chat.getPermalink": self._permalink,
            "chat.startStream": self._post_message,
            "chat.appendStream": self._append_stream,
            "chat.stopStream": self._append_stream,
            "reactions.add": lambda: self._change_reaction(False),
            "reactions.remove": lambda: self._change_reaction(True),
            "reactions.get": self._reactions_get,
            "conversations.history": self._history,
            "conversations.replies": self._replies,
            "conversations.open": self._open_conversation,
            "conversations.create": self._create_conversation,
            "conversations.info": self._conversation_info,
            "files.getUploadURLExternal": self._upload_url,
            "files.completeUploadExternal": self._complete_upload,
            "files.upload": self._legacy_upload,
            "files.info": self._file_info,
            "search.messages": self._search,
            "search.all": self._search,
            "views.open": self._view,
            "views.push": self._view,
            "views.update": self._view,
            "views.publish": self._view,
            WEBHOOK_METHOD: lambda: self._keep_write({"ok": True}),
        }

    def _token(self) -> str:
        token = (
            _text(self.token_option)
            or _text(os.environ.get(TOKEN_ENV))
            or _text(self.access.token)
        )
        if token:
            return token
        missing = SlackCredentialError(
            f"The Slack sandbox reads the real workspace in {READ_REAL_WRITE_FAKE} "
            f"mode, but has no token for {self.method}. Pass "
            f"slack_sandbox(token=...) or set {TOKEN_ENV}."
        )
        fail_replay_item(missing)
        raise missing

    def _from_trace(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        body = recorded_answer(self.state, method, params)
        read = {"method": method}
        for name in ("channel", "ts", "user", "query"):
            if _text(params.get(name)):
                read[name] = params[name]
        self.state["readsFromTrace"].append({**read, "found": body is not None})
        if body is not None:
            return copy.deepcopy(body)
        missing = SlackNotRecordedError(
            f"The Slack sandbox runs in {RECORDED} mode and the original trace "
            f"recorded no {method} read it can answer this call with "
            f"({_read_key(params)}). Replay with "
            f'sandbox_modes={{"slack": "{READ_REAL_WRITE_FAKE}"}} to read the '
            "real workspace, or seed the Slack entry of a sandbox store."
        )
        fail_replay_item(missing)
        raise missing

    def _live(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        if self.state.get("mode") == RECORDED:
            return self._from_trace(method, params)
        token = self._token()
        base = self.api_url_option or self.access.api_url or DEFAULT_API_URL
        url = f"{base if base.endswith('/') else base + '/'}{method}"
        attempt = 0
        while True:
            status, retry_after, body = self.transport(url, token, params)
            if status == 429 and attempt < MAX_RATE_LIMIT_RETRIES:
                attempt += 1
                time.sleep(min(retry_after or 1.0, MAX_RATE_LIMIT_WAIT_SECONDS))
                continue
            break
        body = body if isinstance(body, dict) else {}
        read = {"method": method}
        for name in ("channel", "ts", "user", "query"):
            if _text(params.get(name)):
                read[name] = params[name]
        self.state["liveReads"].append({**read, "ok": body.get("ok") is True})
        error = _text(body.get("error"))
        if error in REFUSED_CREDENTIAL_ERRORS:
            refused = SlackCredentialError(
                f"Slack refused the token the Slack sandbox read {method} with "
                f"({error}). Pass slack_sandbox(token=...) or set {TOKEN_ENV} to "
                "a token that can read this workspace."
            )
            fail_replay_item(refused)
            raise refused
        if status == 429:
            return {"ok": False, "error": "ratelimited"}
        return body

    def _keep_write(self, result: dict[str, Any]) -> dict[str, Any]:
        self.state["otherWrites"].append({"method": self.method, "params": self.params})
        return result

    def _next_ts(self) -> str:
        now = sandbox_now()
        now_micros = round(
            (now.timestamp() if now else time.time()) * MICROS_PER_SECOND
        )
        last = _micros_of(self.state["lastTs"]) if self.state["lastTs"] else 0
        ts = _slack_ts(max(now_micros, last + 1, _micros_of(self.state["cutoff"]) + 1))
        self.state["lastTs"] = ts
        return ts

    def _channel(self) -> str:
        return (
            _text(self.params.get("channel"))
            or _text(self.params.get("channel_id"))
            or ""
        )

    def _kept(self, channel: str) -> list[dict[str, Any]]:
        return self.state["messages"].setdefault(channel, [])

    def _kept_message(self, channel: str, ts: Any) -> dict[str, Any] | None:
        return next(
            (
                message
                for message in self.state["messages"].get(channel, [])
                if message.get("ts") == ts
            ),
            None,
        )

    def _in_sandbox_channel(self) -> bool:
        return self._channel() in self.state["channels"]

    def _identity(self) -> dict[str, Any]:
        if self.state["identity"]:
            return self.state["identity"]
        body = (
            recorded_answer(self.state, "auth.test", {}) or {}
            if self.state.get("mode") == RECORDED
            else self._live("auth.test", {})
        )
        identity = {"user_id": _text(body.get("user_id")) or "USANDBOX"}
        if _text(body.get("bot_id")):
            identity["bot_id"] = body["bot_id"]
        if _text(body.get("team_id")):
            identity["team"] = body["team_id"]
        self.state["identity"] = identity
        return identity

    def _content(self) -> dict[str, Any]:
        body: dict[str, Any] = {}
        written = _text(self.params.get("text")) or _text(
            self.params.get("markdown_text")
        )
        if written is not None:
            body["text"] = written
        for name in ("blocks", "attachments", "metadata"):
            if self.params.get(name) is not None:
                body[name] = _structured(self.params[name])
        return body

    def _post_message(self) -> dict[str, Any]:
        channel = self._channel()
        if channel == "":
            return {"ok": False, "error": "channel_not_found"}
        identity = self._identity()
        ts = self._next_ts()
        thread_ts = _text(self.params.get("thread_ts"))
        message: dict[str, Any] = {
            "type": "message",
            "user": identity["user_id"],
            **{name: identity[name] for name in ("bot_id", "team") if name in identity},
            "ts": ts,
            "text": "",
            **self._content(),
        }
        if thread_ts:
            message["thread_ts"] = thread_ts
            if _structured(self.params.get("reply_broadcast")) in TRUE_VALUES:
                message["subtype"] = "thread_broadcast"
        self._kept(channel).append(message)
        return {"ok": True, "channel": channel, "ts": ts, "message": message}

    def _append_stream(self) -> dict[str, Any]:
        channel = self._channel()
        message = self._kept_message(channel, self.params.get("ts"))
        if message is None:
            return {"ok": False, "error": "message_not_found"}
        added = self._content()
        message["text"] = f"{message.get('text') or ''}{added.get('text') or ''}"
        if "blocks" in added:
            message["blocks"] = added["blocks"]
        return {"ok": True, "channel": channel, "ts": message["ts"], "message": message}

    def _schedule_message(self) -> dict[str, Any]:
        post_at = self.params.get("post_at")
        return self._keep_write(
            {
                "ok": True,
                "channel": self._channel(),
                "scheduled_message_id": f"Q0SANDBOX{len(self.state['otherWrites']) + 1}",
                "post_at": int(post_at) if str(post_at).isdigit() else post_at,
                "message": {"type": "message", "text": "", **self._content()},
            }
        )

    def _update_message(self) -> dict[str, Any]:
        channel = self._channel()
        ts = _text(self.params.get("ts"))
        if not ts:
            return {"ok": False, "error": "message_not_found"}
        identity = self.state["identity"] or {}
        edited = {
            **self._content(),
            "edited": {"user": identity.get("user_id"), "ts": self._next_ts()},
        }
        message = self._kept_message(channel, ts)
        if message is not None:
            message.update(edited)
        else:
            edits = self.state["edits"].setdefault(channel, {})
            edits[ts] = {**edits.get(ts, {}), **edited}
        return {
            "ok": True,
            "channel": channel,
            "ts": ts,
            "text": edited.get("text"),
            "message": {"type": "message", "ts": ts, **(message or edited)},
        }

    def _delete_message(self) -> dict[str, Any]:
        channel = self._channel()
        ts = _text(self.params.get("ts"))
        if not ts:
            return {"ok": False, "error": "message_not_found"}
        if self._kept_message(channel, ts) is not None:
            self.state["messages"][channel] = [
                message for message in self._kept(channel) if message.get("ts") != ts
            ]
        else:
            self.state["deleted"].setdefault(channel, []).append(ts)
        return {"ok": True, "channel": channel, "ts": ts}

    def _permalink(self) -> dict[str, Any]:
        channel = self._channel()
        ts = _text(self.params.get("message_ts")) or ""
        if self._kept_message(channel, ts) is None:
            return self._live(self.method, self.params)
        return {
            "ok": True,
            "channel": channel,
            "permalink": f"https://slack.com/archives/{channel}/p{ts.replace('.', '')}",
        }

    def _change_reaction(self, removed: bool) -> dict[str, Any]:
        channel = self._channel()
        ts = _text(self.params.get("timestamp"))
        name = _text(self.params.get("name"))
        if not ts or not name:
            return {"ok": False, "error": "no_item_specified"}
        identity = self._identity()
        self.state["reactions"].setdefault(channel, {}).setdefault(ts, []).append(
            {"name": name, "user": str(identity["user_id"]), "removed": removed}
        )
        return {"ok": True}

    def _reactions_get(self) -> dict[str, Any]:
        channel = self._channel()
        kept = self._kept_message(channel, self.params.get("timestamp"))
        if kept is not None:
            return {
                "ok": True,
                "type": "message",
                "channel": channel,
                "message": self._shown(channel, kept),
            }
        body = self._live(self.method, self.params)
        if isinstance(body.get("message"), dict):
            body["message"] = self._shown(channel, body["message"]) or body["message"]
        return body

    def _shown(self, channel: str, message: dict[str, Any]) -> dict[str, Any] | None:
        ts = _text(message.get("ts"))
        if not ts:
            return message
        if ts in self.state["deleted"].get(channel, []):
            return None
        shown = {**message, **self.state["edits"].get(channel, {}).get(ts, {})}
        changes = self.state["reactions"].get(channel, {}).get(ts, [])
        if changes:
            reactions = [
                {
                    **reaction,
                    "users": [str(user) for user in reaction.get("users") or []],
                }
                for reaction in _records(shown.get("reactions"))
            ]
            for change in changes:
                reaction = next(
                    (
                        entry
                        for entry in reactions
                        if entry.get("name") == change["name"]
                    ),
                    None,
                )
                if reaction is None and not change["removed"]:
                    reaction = {"name": change["name"], "users": []}
                    reactions.append(reaction)
                if reaction is None:
                    continue
                reaction["users"] = [
                    user for user in reaction["users"] if user != change["user"]
                ]
                if not change["removed"]:
                    reaction["users"].append(change["user"])
            left = [
                {**reaction, "count": len(reaction["users"])}
                for reaction in reactions
                if reaction["users"]
            ]
            if left:
                shown["reactions"] = left
            else:
                shown.pop("reactions", None)
        replies_kept = [
            reply
            for reply in self._kept(channel)
            if reply.get("thread_ts") == ts and reply.get("ts") != ts
        ]
        if replies_kept:
            shown["thread_ts"] = ts
            shown["reply_count"] = int(shown.get("reply_count") or 0) + len(
                replies_kept
            )
            shown["latest_reply"] = replies_kept[-1].get("ts")
        return shown

    def _shown_all(self, channel: str, messages: Any) -> list[dict[str, Any]]:
        shown = (self._shown(channel, message) for message in _records(messages))
        return [message for message in shown if message is not None]

    def _up_to_cutoff(self) -> dict[str, Any]:
        cutoff = self.state["cutoff"]
        latest = _text(self.params.get("latest"))
        if latest and not _is_after(latest, cutoff):
            return self.params
        return {**self.params, "latest": cutoff, "inclusive": True}

    def _within_asked_range(self, message: dict[str, Any]) -> bool:
        latest = _text(self.params.get("latest"))
        oldest = _text(self.params.get("oldest"))
        return not (latest and _is_after(message.get("ts"), latest)) and not (
            oldest and not _is_after(message.get("ts"), oldest)
        )

    def _history(self) -> dict[str, Any]:
        channel = self._channel()
        body = (
            {"ok": True, "messages": [], "has_more": False}
            if self._in_sandbox_channel()
            else self._live(self.method, self._up_to_cutoff())
        )
        if body.get("ok") is not True:
            return body
        live = self._shown_all(channel, body.get("messages"))
        if _text(self.params.get("cursor")):
            return {**body, "messages": live}
        posted = self._shown_all(
            channel,
            [
                message
                for message in self._kept(channel)
                if (
                    message.get("thread_ts") in (None, message.get("ts"))
                    or message.get("subtype") == "thread_broadcast"
                )
                and self._within_asked_range(message)
            ],
        )
        return {**body, "messages": [*reversed(posted), *live]}

    def _replies(self) -> dict[str, Any]:
        channel = self._channel()
        root = _text(self.params.get("ts")) or ""
        kept_root = self._kept_message(channel, root)
        if kept_root is not None or self._in_sandbox_channel():
            body: dict[str, Any] = {
                "ok": True,
                "messages": [kept_root] if kept_root is not None else [],
                "has_more": False,
            }
        else:
            body = self._live(self.method, self._up_to_cutoff())
        if body.get("ok") is not True:
            return body
        live = self._shown_all(channel, body.get("messages"))
        if body.get("has_more") is True:
            return {**body, "messages": live}
        posted = self._shown_all(
            channel,
            [
                message
                for message in self._kept(channel)
                if message.get("thread_ts") == root
                and message.get("ts") != root
                and self._within_asked_range(message)
            ],
        )
        return {**body, "messages": [*live, *posted]}

    def _search(self) -> dict[str, Any]:
        body = self._live(self.method, self.params)
        found = body.get("messages")
        if isinstance(found, dict) and isinstance(found.get("matches"), list):
            found["matches"] = [
                match
                for match in _records(found["matches"])
                if not _is_after(match.get("ts"), self.state["cutoff"])
            ]
        return body

    def _sandbox_channel(self, prefix: str, fields: dict[str, Any]) -> dict[str, Any]:
        channel_id = f"{prefix}0SANDBOX{len(self.state['channels']) + 1}"
        channel = {
            "id": channel_id,
            "created": _micros_of(self._next_ts()) // MICROS_PER_SECOND,
            **fields,
        }
        self.state["channels"][channel_id] = channel
        return channel

    def _open_conversation(self) -> dict[str, Any]:
        given = _text(self.params.get("channel"))
        if given:
            return {"ok": True, "channel": {"id": given}}
        users = _text(self.params.get("users")) or ""
        already = next(
            (
                channel
                for channel in self.state["channels"].values()
                if channel.get("users") == users
            ),
            None,
        )
        if already is not None:
            return {"ok": True, "already_open": True, "channel": already}
        existing = self._live(self.method, {**self.params, "prevent_creation": True})
        if existing.get("ok") is True:
            return existing
        members = [user for user in users.split(",") if user]
        kind = (
            {"is_mpim": True}
            if len(members) > 1
            else {"is_im": True, "user": members[0] if members else None}
        )
        return {
            "ok": True,
            "channel": self._sandbox_channel(
                "G" if len(members) > 1 else "D", {"users": users, **kind}
            ),
        }

    def _create_conversation(self) -> dict[str, Any]:
        return {
            "ok": True,
            "channel": self._sandbox_channel(
                "C",
                {
                    "name": _text(self.params.get("name")) or "",
                    "is_channel": True,
                    "is_private": _structured(self.params.get("is_private"))
                    in TRUE_VALUES,
                    "is_member": True,
                },
            ),
        }

    def _conversation_info(self) -> dict[str, Any]:
        channel = self.state["channels"].get(self._channel())
        if channel is not None:
            return {"ok": True, "channel": channel}
        return self._live(self.method, self.params)

    def _sandbox_file(self, fields: dict[str, Any]) -> dict[str, Any]:
        file = {"id": f"F0SANDBOX{len(self.state['files']) + 1}", **fields}
        self.state["files"].append(file)
        return file

    def _file_info(self) -> dict[str, Any]:
        wanted = _text(self.params.get("file"))
        file = next(
            (kept for kept in self.state["files"] if kept["id"] == wanted), None
        )
        if file is not None:
            return {"ok": True, "file": file}
        return self._live(self.method, self.params)

    def _upload_url(self) -> dict[str, Any]:
        length = self.params.get("length")
        file = self._sandbox_file(
            {
                "name": self.params.get("filename"),
                "size": int(length) if str(length).isdigit() else length,
            }
        )
        return {
            "ok": True,
            "file_id": file["id"],
            "upload_url": f"https://files.slack.com/upload/v1/{file['id']}",
        }

    def _share_files(self, files: list[dict[str, Any]], channel: str) -> None:
        identity = self._identity()
        message: dict[str, Any] = {
            "type": "message",
            "user": identity["user_id"],
            "ts": self._next_ts(),
            "text": _text(self.params.get("initial_comment")) or "",
            "files": files,
        }
        thread_ts = _text(self.params.get("thread_ts"))
        if thread_ts:
            message["thread_ts"] = thread_ts
        self._kept(channel).append(message)

    def _shared_channels(self) -> list[str]:
        named = _text(self.params.get("channels")) or self._channel()
        return [channel for channel in named.split(",") if channel]

    def _complete_upload(self) -> dict[str, Any]:
        completed = []
        for entry in _records(_structured(self.params.get("files"))):
            file = next(
                (kept for kept in self.state["files"] if kept["id"] == entry.get("id")),
                None,
            )
            if file is not None and entry.get("title") is not None:
                file["title"] = entry["title"]
            completed.append(file or entry)
        for channel in self._shared_channels():
            self._share_files(completed, channel)
        return {"ok": True, "files": completed}

    def _legacy_upload(self) -> dict[str, Any]:
        file = self._sandbox_file(
            {"name": self.params.get("filename"), "title": self.params.get("title")}
        )
        for channel in self._shared_channels():
            self._share_files([file], channel)
        return {"ok": True, "file": file}

    def _view(self) -> dict[str, Any]:
        view = _structured(self.params.get("view"))
        return self._keep_write(
            {
                "ok": True,
                "view": {
                    "id": f"V0SANDBOX{len(self.state['otherWrites']) + 1}",
                    **(view if isinstance(view, dict) else {}),
                },
            }
        )


def is_slack_call(node: SpanNodeMeta) -> bool:
    call = service_calls.current_call()
    return (
        call is not None
        and call.integration == SLACK_INTEGRATION
        and node.trace_function_key.startswith(SLACK_SPAN_PREFIX)
    )


def answer_slack_call(
    state: dict[str, Any],
    call: MockOverrideCtx,
    token: str | None,
    api_url: str | None,
    transport: Transport,
) -> dict[str, Any]:
    held = service_calls.current_call()
    access = held.request if held is not None else None
    if not isinstance(access, SlackCallAccess):
        raise RuntimeError(
            f"The Slack sandbox was handed {call.node.trace_function_key}, which "
            "is not a Slack call the SDK held back."
        )
    return SlackCall(
        state,
        call.node.trace_function_key[len(SLACK_SPAN_PREFIX) :],
        dict(call.kwargs),
        access,
        token,
        api_url,
        transport,
    ).answer()


def build_slack_sandbox(
    token: str | None,
    api_url: str | None,
    transport: Transport,
    mode: str = READ_REAL_WRITE_FAKE,
    start: Callable[[SandboxStartCtx], Any] | None = None,
) -> Sandbox:
    if mode not in SLACK_MODES:
        raise SlackModeError(
            f"The Slack sandbox has no mode {mode!r}. Its modes are "
            f"{', '.join(repr(m) for m in SLACK_MODES)}."
        )
    load = load_slack_state(mode)
    chosen = start or (recorded_start_state if mode == RECORDED else start_state)
    return Sandbox(
        name=SLACK_SANDBOX_NAME,
        match=is_slack_call,
        handle=lambda state, call: answer_slack_call(
            state, call, token, api_url, transport
        ),
        start=chosen if start is None else lambda ctx: load(ctx, chosen(ctx)),
        mode=mode,
        load=load,
        is_write=is_slack_write,
    )
