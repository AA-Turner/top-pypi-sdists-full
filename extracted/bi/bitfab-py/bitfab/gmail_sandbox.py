from __future__ import annotations

import base64
import copy
import datetime
import email
import email.policy
import email.utils
import re
from collections.abc import Callable
from typing import Any

from bitfab.google_calls import CREDENTIAL_PARAM, HTTP_ERROR_KEY, request_credentials
from bitfab.mock_override import MockOverrideCtx, SpanNodeMeta
from bitfab.sandbox import (
    Sandbox,
    SandboxStartCtx,
    sandbox_elapsed_ms,
    sandbox_state,
)
from bitfab.service_calls import ServiceCallHeldBackError

GMAIL_SANDBOX_NAME = "Gmail"
GET_METHOD = "gmail.users.messages.get"
LIST_METHOD = "gmail.users.messages.list"
PROFILE_METHOD = "gmail.users.getProfile"
LABELS_LIST_METHOD = "gmail.users.labels.list"
LABEL_GET_METHOD = "gmail.users.labels.get"
SEND_AS_LIST_METHOD = "gmail.users.settings.sendAs.list"
DRAFT_GET_METHOD = "gmail.users.drafts.get"
DRAFT_LIST_METHOD = "gmail.users.drafts.list"
DRAFT_CREATE_METHOD = "gmail.users.drafts.create"
SYSTEM_LABELS = (
    "INBOX",
    "SENT",
    "DRAFT",
    "UNREAD",
    "STARRED",
    "IMPORTANT",
    "SPAM",
    "TRASH",
    "CATEGORY_PERSONAL",
    "CATEGORY_UPDATES",
    "CATEGORY_PROMOTIONS",
    "CATEGORY_SOCIAL",
    "CATEGORY_FORUMS",
)
_PLAIN_HEADERS = {
    "from": "From",
    "to": "To",
    "cc": "Cc",
    "bcc": "Bcc",
    "subject": "Subject",
    "date": "Date",
}
_TOKEN = re.compile(r'-?[A-Za-z_]+:"[^"]*"|-?[A-Za-z_]+:\S+|-?"[^"]*"|\S+')
_OPERATOR = re.compile(r"^[A-Za-z_]+:")
_QUERY_TOKEN = re.compile(
    r'-?[A-Za-z_]+:\(|-?[A-Za-z_]+:"[^"]*"|-?[A-Za-z_]+:[^\s(){}]+|-?"[^"]*"'
    r'|-?[({]|[)}]|-?[^\s(){}"]+'
)
_HISTORY_TYPES = {
    "messageAdded": "messagesAdded",
    "messageDeleted": "messagesDeleted",
    "labelAdded": "labelsAdded",
    "labelRemoved": "labelsRemoved",
}
_RELATIVE = re.compile(r"^(\d+)([dmy])$")


def _b64(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("ascii")


def _unb64(data: str) -> str:
    padded = data + "=" * (-len(data) % 4)
    return base64.urlsafe_b64decode(padded.encode("ascii")).decode(
        "utf-8", errors="replace"
    )


def _millis(value: Any) -> int | None:
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).strip()
    if text.isdigit():
        return int(text)
    parsed: datetime.datetime | None = None
    try:
        parsed = email.utils.parsedate_to_datetime(text)
    except (TypeError, ValueError):
        try:
            parsed = datetime.datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError:
            return None
    if parsed is None:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=datetime.timezone.utc)
    return int(parsed.timestamp() * 1000)


def _headers(message: dict[str, Any]) -> list[dict[str, str]]:
    return list((message.get("payload") or {}).get("headers") or [])


def _header(message: dict[str, Any], name: str) -> str:
    lowered = name.lower()
    return next(
        (
            str(h.get("value") or "")
            for h in _headers(message)
            if str(h.get("name") or "").lower() == lowered
        ),
        "",
    )


def _body_text(part: dict[str, Any]) -> str:
    texts: list[str] = []
    data = (part.get("body") or {}).get("data")
    if data and str(part.get("mimeType") or "text/plain").startswith("text/"):
        texts.append(_unb64(data))
    for child in part.get("parts") or []:
        texts.append(_body_text(child))
    return "\n".join(text for text in texts if text)


def _attachments(part: dict[str, Any]) -> list[dict[str, Any]]:
    found = [part] if part.get("filename") else []
    for child in part.get("parts") or []:
        found.extend(_attachments(child))
    return found


def gmail_message(fields: dict[str, Any]) -> dict[str, Any]:
    """Build a Gmail API message from plain fields, for a Gmail sandbox's ``start``.

    Args:
        fields: ``id`` (required), ``threadId`` (defaults to ``id``), ``from``,
            ``to``, ``cc``, ``bcc``, ``subject``, ``date`` (RFC 2822 or ISO
            8601), ``snippet``, ``body`` (plain text), ``unread`` (adds
            ``UNREAD``), ``labelIds`` (defaults to ``["INBOX"]``), and
            ``internalDate`` (milliseconds; defaults to ``date``). A dict that
            already has a ``payload`` is returned as Gmail sent it.

    When ``body`` is missing, the snippet stands in for it, and the message is
    marked so the replay trace shows the body was not recorded.
    """
    if "payload" in fields:
        return copy.deepcopy(fields)
    message_id = str(fields["id"])
    labels = list(fields.get("labelIds") or ["INBOX"])
    if fields.get("unread") and "UNREAD" not in labels:
        labels.append("UNREAD")
    if fields.get("unread") is False and "UNREAD" in labels:
        labels.remove("UNREAD")
    body = fields.get("body")
    snippet = str(fields.get("snippet") or (body or "")[:200])
    headers = [
        {"name": header, "value": str(fields[key])}
        for key, header in _PLAIN_HEADERS.items()
        if fields.get(key)
    ]
    text = str(body if body is not None else snippet)
    message: dict[str, Any] = {
        "id": message_id,
        "threadId": str(fields.get("threadId") or message_id),
        "labelIds": labels,
        "snippet": snippet,
        "internalDate": str(
            _millis(fields.get("internalDate")) or _millis(fields.get("date")) or 0
        ),
        "sizeEstimate": len(text),
        "payload": {
            "mimeType": "text/plain",
            "headers": headers,
            "body": {"size": len(text.encode("utf-8")), "data": _b64(text)},
        },
    }
    if body is None:
        message["bitfabBodyFromSnippet"] = True
    return message


def _fields_from_raw(raw: str | None) -> dict[str, Any]:
    parsed = email.message_from_string(
        _unb64(raw) if raw else "", policy=email.policy.default
    )
    body_part = (
        parsed.get_body(preferencelist=("plain", "html"))
        if parsed.is_multipart()
        else parsed
    )
    body = body_part.get_content() if body_part is not None else ""
    return {
        **{
            key: str(parsed.get(header))
            for key, header in _PLAIN_HEADERS.items()
            if parsed.get(header)
        },
        "body": str(body),
    }


def _richer(
    existing: dict[str, Any] | None, candidate: dict[str, Any]
) -> dict[str, Any]:
    if existing is None:
        return candidate
    has_body = bool(_body_text(candidate.get("payload") or {}))
    had_body = bool(_body_text(existing.get("payload") or {}))
    return candidate if has_body and not had_body else existing


def mailbox_from_recorded_calls(ctx: SandboxStartCtx) -> dict[str, Any]:
    """The Gmail sandbox's default ``start``: mailboxes built from the original trace.

    Uses the state recorded with ``record_sandbox_state("Gmail", ...)`` when
    there is one. Otherwise takes every message the original run read
    (``gmail.users.messages.get`` replies), each account's address from
    ``gmail.users.getProfile``, and the drafts the run found
    (``gmail.users.drafts.list`` and ``gmail.users.drafts.get`` replies, the
    first read of each draft), one mailbox per credential the calls used.
    Drafts the original run created are left out.
    """
    if ctx.recorded_state is not None:
        return as_mailboxes(ctx, ctx.recorded_state)
    created = {
        str(span.output.get("id"))
        for span in ctx.recorded_spans(DRAFT_CREATE_METHOD)
        if isinstance(span.output, dict) and span.output.get("id")
    }
    by_credential: dict[str | None, dict[str, Any]] = {}
    for name in (
        GET_METHOD,
        PROFILE_METHOD,
        LIST_METHOD,
        LABELS_LIST_METHOD,
        LABEL_GET_METHOD,
        SEND_AS_LIST_METHOD,
        DRAFT_GET_METHOD,
        DRAFT_LIST_METHOD,
    ):
        for span in ctx.recorded_spans(name):
            output = span.output
            if not isinstance(output, dict) or HTTP_ERROR_KEY in output:
                continue
            given = span.input if isinstance(span.input, dict) else {}
            credential = given.get(CREDENTIAL_PARAM)
            box = by_credential.setdefault(
                credential,
                {
                    "credential": credential,
                    "emailAddress": None,
                    "messages": {},
                    "drafts": {},
                    "searches": [],
                    "labels": {},
                    "sendAs": None,
                    "historyId": None,
                },
            )
            if name == LIST_METHOD and not given.get("pageToken"):
                box["searches"].append(
                    {
                        "q": str(given.get("q") or ""),
                        "ids": [m.get("id") for m in output.get("messages") or []],
                    }
                )
            if name == GET_METHOD and output.get("id"):
                box["messages"][output["id"]] = _richer(
                    box["messages"].get(output["id"]), output
                )
            if name == PROFILE_METHOD:
                box["emailAddress"] = output.get("emailAddress") or box["emailAddress"]
                box["historyId"] = output.get("historyId") or box["historyId"]
            if name == LABELS_LIST_METHOD:
                for label in output.get("labels") or []:
                    _keep_user_label(box["labels"], label)
            if name == LABEL_GET_METHOD:
                _keep_user_label(box["labels"], output)
            if name == SEND_AS_LIST_METHOD and isinstance(output.get("sendAs"), list):
                box["sendAs"] = output["sendAs"]
            drafts = (
                [output]
                if name == DRAFT_GET_METHOD
                else output.get("drafts") or []
                if name == DRAFT_LIST_METHOD
                else []
            )
            for draft in drafts:
                draft_id = str(draft.get("id") or "")
                if draft_id and draft_id not in created:
                    box["drafts"].setdefault(draft_id, draft)
    boxes = [
        {
            **box,
            "messages": list(box["messages"].values()),
            "labels": list(box["labels"].values()),
            "drafts": list(box["drafts"].values()),
        }
        for box in by_credential.values()
    ]
    return as_mailboxes(ctx, {"mailboxes": boxes or [{}]})


def _keep_user_label(into: dict[str, dict[str, Any]], label: Any) -> None:
    if not isinstance(label, dict) or not label.get("id"):
        return
    if label.get("type") == "system" or label["id"] in SYSTEM_LABELS:
        return
    into[str(label["id"])] = label


def as_mailboxes(ctx: SandboxStartCtx, started: Any) -> dict[str, Any]:
    if isinstance(started, dict) and isinstance(started.get("mailboxes"), list):
        boxes = started["mailboxes"]
        if boxes and all(isinstance(box, dict) and "nextId" in box for box in boxes):
            return started
    elif isinstance(started, list):
        grouped: dict[str | None, list[dict[str, Any]]] = {}
        for message in started:
            grouped.setdefault(message.get("account"), []).append(message)
        boxes = [
            {"emailAddress": account, "messages": messages}
            for account, messages in grouped.items()
        ]
        if not boxes:
            boxes = [{}]
    elif isinstance(started, dict):
        boxes = [started]
    else:
        raise TypeError(
            "A Gmail sandbox start must return a list of messages, a dict with "
            "messages, emailAddress and drafts, or {'mailboxes': [...]}, not "
            f"{type(started).__name__}."
        )
    return {
        "mailboxes": [
            new_mailbox(
                ctx,
                index,
                messages=box.get("messages"),
                email_address=box.get("emailAddress") or box.get("email_address"),
                credential=box.get("credential"),
                drafts=box.get("drafts"),
                details=box.get("details"),
                searches=box.get("searches"),
                labels=box.get("labels"),
                send_as=box.get("sendAs"),
                clock=box.get("clock"),
                history_id=box.get("historyId"),
            )
            for index, box in enumerate(boxes or [{}])
        ]
    }


def _history_number(value: Any) -> int:
    text = str(value or "").strip()
    return int(text) if text.isdigit() else 0


def _starting_history_id(messages: list[dict[str, Any]], recorded: Any) -> int:
    return max(
        [1000, _history_number(recorded)]
        + [_history_number(m.get("historyId")) for m in messages]
    )


def new_mailbox(
    ctx: SandboxStartCtx,
    index: int,
    messages: list[dict[str, Any]] | None = None,
    email_address: str | None = None,
    credential: str | None = None,
    drafts: list[dict[str, Any]] | None = None,
    details: dict[str, Any] | None = None,
    searches: list[dict[str, Any]] | None = None,
    labels: list[dict[str, Any] | str] | None = None,
    send_as: list[dict[str, Any]] | None = None,
    clock: str | None = None,
    history_id: Any = None,
) -> dict[str, Any]:
    normalized = [gmail_message(message) for message in messages or []]
    notes: list[str] = []
    started_drafts = [
        _start_draft(draft, position, normalized, notes)
        for position, draft in enumerate(drafts or [])
        if isinstance(draft, dict)
    ]
    for message in normalized:
        if (
            message.get("payload")
            and not _body_text(message["payload"])
            and message.get("snippet")
        ):
            message["payload"] = {
                **message["payload"],
                "body": {
                    "size": len(message["snippet"]),
                    "data": _b64(message["snippet"]),
                },
            }
            message["bitfabBodyFromSnippet"] = True
    return {
        "emailAddress": email_address,
        "credential": credential,
        "details": dict(details or {}),
        "clock": clock or ctx.trace_started_at,
        "historyId": _starting_history_id([*(messages or []), *normalized], history_id),
        "nextId": index * 1_000_000 + 1,
        "messages": normalized,
        "drafts": started_drafts,
        "searches": list(searches or []),
        "labels": [_user_label(label) for label in labels or []],
        "sendAs": None if send_as is None else [dict(entry) for entry in send_as],
        "history": [],
        "notes": notes,
    }


def _user_label(label: dict[str, Any] | str) -> dict[str, Any]:
    given = {"name": label} if isinstance(label, str) else dict(label)
    name = str(given.get("name") or given.get("id") or "")
    return {
        "id": str(given.get("id") or name),
        "name": name,
        "type": "user",
        "messageListVisibility": "show",
        "labelListVisibility": "labelShow",
        **given,
    }


def _draft_label(labels: Any) -> list[str]:
    kept = [label for label in labels or [] if label != "DRAFT"]
    return ["DRAFT", *kept]


def _draft_ref(message: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": message["id"],
        "threadId": message.get("threadId"),
        "labelIds": message.get("labelIds"),
    }


def _start_draft(
    draft: dict[str, Any],
    position: int,
    messages: list[dict[str, Any]],
    notes: list[str],
) -> dict[str, Any]:
    draft_id = str(draft.get("id") or f"r-start{position}")
    given = dict(draft.get("message") or {})
    message_id = str(given.get("id") or f"m-{draft_id}")
    if given.get("raw") and "payload" not in given:
        given = {**given, **_fields_from_raw(given.pop("raw"))}
    existing = next((m for m in messages if m.get("id") == message_id), None)
    carries_content = bool(set(given) - {"id", "threadId", "labelIds", "historyId"})
    if carries_content:
        built = gmail_message({"labelIds": ["DRAFT"], **given, "id": message_id})
        message = _richer(existing, built) if existing else built
    elif existing is not None:
        message = existing
    else:
        message = gmail_message(
            {
                "id": message_id,
                "threadId": given.get("threadId"),
                "labelIds": ["DRAFT"],
                "body": "",
            }
        )
    message["labelIds"] = _draft_label(
        message.get("labelIds") if given.get("labelIds") is None else given["labelIds"]
    )
    if not _body_text(message.get("payload") or {}) and not message.get("snippet"):
        notes.append(
            f"draft {draft_id} was never read in full in the original run, so its message is empty"
        )
    if existing is None:
        messages.append(message)
    elif message is not existing:
        messages[messages.index(existing)] = message
    return {"id": draft_id, "message": _draft_ref(message)}


def _note(state: dict[str, Any], text: str) -> None:
    notes = state.setdefault("notes", [])
    if text not in notes:
        notes.append(text)


def _not_found(what: str) -> dict[str, Any]:
    return {
        HTTP_ERROR_KEY: {
            "code": 404,
            "message": f"Requested entity was not found. ({what})",
            "status": "NOT_FOUND",
            "errors": [
                {
                    "message": "Requested entity was not found.",
                    "domain": "global",
                    "reason": "notFound",
                }
            ],
        }
    }


def _public(message: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value for key, value in message.items() if not key.startswith("bitfab")
    }


def _find(state: dict[str, Any], message_id: str) -> dict[str, Any] | None:
    return next((m for m in state["messages"] if m.get("id") == message_id), None)


def _shaped(
    message: dict[str, Any], fmt: str, metadata_headers: list[str] | None
) -> dict[str, Any]:
    public = _public(message)
    if fmt == "minimal":
        return {key: value for key, value in public.items() if key != "payload"}
    if fmt == "metadata":
        wanted = {name.lower() for name in metadata_headers or []}
        payload = public.get("payload") or {}
        headers = [
            h
            for h in payload.get("headers") or []
            if not wanted or str(h.get("name") or "").lower() in wanted
        ]
        return {
            **public,
            "payload": {"mimeType": payload.get("mimeType"), "headers": headers},
        }
    if fmt == "raw":
        lines = [f"{h.get('name')}: {h.get('value')}" for h in _headers(message)]
        raw = "\r\n".join(lines) + "\r\n\r\n" + _body_text(message.get("payload") or {})
        return {**{k: v for k, v in public.items() if k != "payload"}, "raw": _b64(raw)}
    return public


def _clock_millis(state: dict[str, Any]) -> int:
    started = _millis(state.get("clock"))
    if started is None:
        return int(datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000)
    return started + sandbox_elapsed_ms()


def _created_millis(state: dict[str, Any]) -> int:
    created = max(_clock_millis(state), int(state.get("lastCreatedAt") or 0) + 1)
    state["lastCreatedAt"] = created
    return created


def _date_bound(value: str) -> int | None:
    text = value.strip()
    if text.isdigit():
        return int(text) * 1000
    for pattern in ("%Y/%m/%d", "%Y-%m-%d", "%m/%d/%Y"):
        try:
            day = datetime.datetime.strptime(text, pattern).replace(
                tzinfo=datetime.timezone.utc
            )
        except ValueError:
            continue
        return int(day.timestamp() * 1000)
    return None


def _relative_millis(value: str) -> int | None:
    matched = _RELATIVE.match(value.strip().lower())
    if matched is None:
        return None
    days = int(matched.group(1)) * {"d": 1, "m": 30, "y": 365}[matched.group(2)]
    return days * 86_400_000


def _search_name(name: str) -> str:
    return re.sub(r"[\s/&]+", "-", name.strip().lower())


def _label_ids_named(state: dict[str, Any], value: str) -> set[str]:
    wanted = _search_name(value)
    return {
        str(label.get("id"))
        for label in state.get("labels") or []
        if _search_name(str(label.get("name") or "")) == wanted
    }


def _contains(haystack: str, needle: str) -> bool:
    return needle.lower() in haystack.lower()


def _term_matches(state: dict[str, Any], message: dict[str, Any], term: str) -> bool:
    operator, _, value = (
        term.partition(":") if re.match(r"^[A-Za-z_]+:", term) else ("", "", term)
    )
    value = value.strip('"')
    operator = operator.lower()
    labels = set(message.get("labelIds") or [])
    internal = int(message.get("internalDate") or 0)
    if operator in {"from", "to", "cc", "bcc", "subject"}:
        return _contains(_header(message, operator), value)
    if operator == "after":
        bound = _date_bound(value)
        return bound is None or internal >= bound
    if operator == "before":
        bound = _date_bound(value)
        return bound is None or internal < bound
    if operator in {"newer_than", "older_than"}:
        span = _relative_millis(value)
        if span is None:
            return True
        cutoff = _clock_millis(state) - span
        return internal >= cutoff if operator == "newer_than" else internal < cutoff
    if operator == "is":
        wanted = value.lower()
        if wanted == "unread":
            return "UNREAD" in labels
        if wanted == "read":
            return "UNREAD" not in labels
        return wanted.upper() in labels
    if operator in {"in", "label"}:
        wanted = value.upper().replace("-", "_")
        return (
            wanted == "ANYWHERE"
            or wanted in labels
            or value in labels
            or bool(_label_ids_named(state, value) & labels)
        )
    if operator == "has":
        return value.lower() != "attachment" or bool(
            _attachments(message.get("payload") or {})
        )
    if operator == "filename":
        return any(
            _contains(str(p.get("filename")), value)
            for p in _attachments(message.get("payload") or {})
        )
    _note(
        state,
        "free-text search is matched as plain words in sender, recipients, subject, snippet and body",
    )
    text = " ".join(
        [
            _header(message, "from"),
            _header(message, "to"),
            _header(message, "cc"),
            _header(message, "subject"),
            str(message.get("snippet") or ""),
            _body_text(message.get("payload") or {}),
        ]
    )
    return _contains(text, term.strip('"'))


Query = tuple[str, Any]


def _negated(negate: bool, query: Query) -> Query:
    return ("not", query) if negate else query


def _leaf(token: str, field: str | None) -> Query:
    negate = token.startswith("-") and len(token) > 1
    text = token[1:] if negate else token
    if field and not _OPERATOR.match(text):
        text = f"{field}:{text}"
    return _negated(negate, ("term", text))


class _QueryParser:
    def __init__(self, query: str) -> None:
        self.tokens = _QUERY_TOKEN.findall(query or "")
        self.at = 0

    def peek(self) -> str | None:
        return self.tokens[self.at] if self.at < len(self.tokens) else None

    def take(self) -> str:
        token = self.tokens[self.at]
        self.at += 1
        return token

    def conjunction(self, closer: str | None, field: str | None) -> Query:
        items: list[Query] = []
        while (token := self.peek()) is not None and token != closer:
            if token in {"AND", ")", "}"}:
                self.take()
                continue
            items.append(self.disjunction(closer, field))
        if self.peek() == closer and closer is not None:
            self.take()
        return items[0] if len(items) == 1 else ("and", items)

    def disjunction(self, closer: str | None, field: str | None) -> Query:
        items = [self.unary(field)]
        while self.peek() == "OR":
            self.take()
            if self.peek() in {None, closer, "OR"}:
                continue
            items.append(self.unary(field))
        return items[0] if len(items) == 1 else ("or", items)

    def unary(self, field: str | None) -> Query:
        token = self.take()
        negate = token.startswith("-") and len(token) > 1
        bare = token[1:] if negate else token
        if bare == "(":
            return _negated(negate, self.conjunction(")", field))
        if bare == "{":
            return _negated(negate, self.braced(field))
        if bare.endswith(":("):
            return _negated(negate, self.conjunction(")", bare[:-2]))
        return _leaf(token, field)

    def braced(self, field: str | None) -> Query:
        items: list[Query] = []
        while (token := self.peek()) is not None and token != "}":
            if token in {"AND", "OR", ")"}:
                self.take()
                continue
            items.append(self.unary(field))
        if self.peek() == "}":
            self.take()
        return items[0] if len(items) == 1 else ("or", items)


def _flattened(query: Query) -> Query:
    kind, value = query
    if kind == "term":
        return query
    if kind == "not":
        return ("not", _flattened(value))
    items: list[Query] = []
    for child in (_flattened(q) for q in value):
        items.extend(child[1] if child[0] == kind else [child])
    return items[0] if len(items) == 1 else (kind, items)


def parse_query(query: str) -> Query:
    return _flattened(_QueryParser(query).conjunction(None, None))


def _matches(state: dict[str, Any], message: dict[str, Any], query: Query) -> bool:
    kind, value = query
    if kind == "term":
        return _term_matches(state, message, value)
    if kind == "not":
        return not _matches(state, message, value)
    if kind == "or":
        return any(_matches(state, message, q) for q in value)
    return all(_matches(state, message, q) for q in value)


def _leaves(query: Query) -> list[str]:
    kind, value = query
    if kind == "term":
        return [value]
    if kind == "not":
        return []
    return [leaf for q in value for leaf in _leaves(q)]


def _required(query: Query) -> list[Query]:
    kind, value = query
    return list(value) if kind == "and" else [query]


def _is_plain(query: Query) -> bool:
    return all(
        q[0] == "term" or (q[0] == "not" and q[1][0] == "term")
        for q in _required(query)
    )


def _is_free_text(term: str) -> bool:
    return bool(term) and not term.startswith("-") and not _OPERATOR.match(term)


_DATE_OPERATORS = ("after:", "before:", "newer_than:", "older_than:")


def _canonical(query: Query) -> str:
    kind, value = query
    if kind == "term":
        return str(value).lower()
    if kind == "not":
        return "-" + _canonical(value)
    joined = f" {kind.upper()} ".join(sorted(_canonical(q) for q in value))
    return f"({joined})"


def _is_date_bound(query: Query) -> bool:
    return query[0] == "term" and query[1].lower().startswith(_DATE_OPERATORS)


def search_key(query: str) -> str:
    kept = [q for q in _required(parse_query(query)) if not _is_date_bound(q)]
    return " ".join(sorted(_canonical(q) for q in kept))


def _text_key(query: str) -> str:
    words = [
        t.strip('"').lower()
        for t in _TOKEN.findall(query or "")
        if _is_free_text(t) and t not in {"(", ")", "AND", "OR"}
    ]
    return " ".join(sorted(words))


def _recorded_searches(state: dict[str, Any]) -> list[tuple[str, list[str]]]:
    return [
        (str(s.get("q") or s.get("text") or ""), [str(i) for i in s.get("ids") or []])
        for s in state.get("searches") or []
        if isinstance(s, dict)
    ]


def _same_search(state: dict[str, Any], query: str) -> list[str] | None:
    key = search_key(query)
    found = [ids for q, ids in _recorded_searches(state) if search_key(q) == key]
    if not found:
        return None
    return list(dict.fromkeys(i for ids in found for i in ids))


def _known_results(state: dict[str, Any], key: str) -> set[str] | None:
    if not key:
        return None
    found = [ids for q, ids in _recorded_searches(state) if _text_key(q) == key]
    if not found:
        return None
    return {i for ids in found for i in ids}


def _search(
    state: dict[str, Any], query: str, include_spam_trash: bool
) -> list[dict[str, Any]]:
    parsed = parse_query(query)
    searching_everywhere = any(
        t.lower() in {"in:anywhere", "in:spam", "in:trash"} for t in _leaves(parsed)
    )
    visible = {
        m.get("id"): m
        for m in state["messages"]
        if include_spam_trash
        or searching_everywhere
        or not set(m.get("labelIds") or []) & {"SPAM", "TRASH"}
    }
    same = _same_search(state, query)
    if same is not None:
        created = [
            m
            for m in visible.values()
            if m.get("bitfabCreated") and _matches(state, m, parsed)
        ]
        dates = [q for q in _required(parsed) if _is_date_bound(q)]
        recorded = [
            visible[i]
            for i in same
            if i in visible and all(_matches(state, visible[i], q) for q in dates)
        ]
        newest_first = sorted(
            created, key=lambda m: int(m.get("internalDate") or 0), reverse=True
        )
        return newest_first + recorded
    known = _known_results(state, _text_key(query)) if _is_plain(parsed) else None
    rest = parsed
    free: Query = ("and", [])
    if known is not None:
        required = _required(parsed)
        free = ("and", [q for q in required if q[0] == "term" and _is_free_text(q[1])])
        rest = ("and", [q for q in required if q not in free[1]])
    found = []
    for message in visible.values():
        if known is not None and (
            message.get("id") not in known
            if not message.get("bitfabCreated")
            else not _matches(state, message, free)
        ):
            continue
        if _matches(state, message, rest):
            found.append(message)
    return sorted(found, key=lambda m: int(m.get("internalDate") or 0), reverse=True)


def _matching(state: dict[str, Any], params: dict[str, Any]) -> list[dict[str, Any]]:
    matched = _search(
        state,
        str(params.get("q") or ""),
        str(params.get("includeSpamTrash")).lower() == "true",
    )
    label_ids = params.get("labelIds") or []
    if isinstance(label_ids, str):
        label_ids = [label_ids]
    return [m for m in matched if set(label_ids) <= set(m.get("labelIds") or [])]


def _paged(
    params: dict[str, Any], items: list[Any], key: str, shape: Callable[[Any], Any]
) -> dict[str, Any]:
    size = min(int(params.get("maxResults") or 100), 500)
    offset = int(params.get("pageToken") or 0)
    page = items[offset : offset + size]
    reply: dict[str, Any] = {"resultSizeEstimate": len(items)}
    if page:
        reply[key] = [shape(item) for item in page]
    if offset + size < len(items):
        reply["nextPageToken"] = str(offset + size)
    return reply


def _list(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    return _paged(
        params,
        _matching(state, params),
        "messages",
        lambda m: {"id": m["id"], "threadId": m.get("threadId")},
    )


def _thread_messages(state: dict[str, Any], thread_id: str) -> list[dict[str, Any]]:
    return [m for m in state["messages"] if m.get("threadId") == thread_id]


def _threads_list(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    newest: dict[str, dict[str, Any]] = {}
    for message in _matching(state, params):
        newest.setdefault(str(message.get("threadId") or message["id"]), message)

    def shape(thread_id: str) -> dict[str, Any]:
        latest = max(
            _thread_messages(state, thread_id) or [newest[thread_id]],
            key=lambda m: int(m.get("historyId") or 0),
        )
        return {
            "id": thread_id,
            "snippet": newest[thread_id].get("snippet") or "",
            "historyId": str(latest.get("historyId") or state.get("historyId")),
        }

    return _paged(params, list(newest), "threads", shape)


def _get(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    message = _find(state, str(params.get("id")))
    if message is None:
        return _not_found(f"message {params.get('id')}")
    fmt = str(params.get("format") or "full").lower()
    if fmt in {"full", "raw"} and message.get("bitfabBodyFromSnippet"):
        _note(
            state,
            f"message {message['id']} was never opened in the original run, so its body is its snippet",
        )
    headers = params.get("metadataHeaders")
    return _shaped(message, fmt, [headers] if isinstance(headers, str) else headers)


def _next_id(state: dict[str, Any], prefix: str) -> str:
    value = int(state.get("nextId") or 1)
    state["nextId"] = value + 1
    return f"{prefix}{value:012x}"


def _bump_history(state: dict[str, Any]) -> str:
    state["historyId"] = int(state.get("historyId") or 1000) + 1
    return str(state["historyId"])


def _message_ref(message: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": message["id"],
        "threadId": message.get("threadId"),
        "labelIds": list(message.get("labelIds") or []),
    }


def _record_change(
    state: dict[str, Any], message: dict[str, Any], changes: dict[str, Any]
) -> None:
    history_id = _bump_history(state)
    message["historyId"] = history_id
    ref = _message_ref(message)
    entry: dict[str, Any] = {
        "id": history_id,
        "messages": [{"id": ref["id"], "threadId": ref["threadId"]}],
    }
    for key, labels in changes.items():
        if key in {"messagesAdded", "messagesDeleted"}:
            entry[key] = [{"message": ref}]
        elif labels:
            entry[key] = [{"message": ref, "labelIds": list(labels)}]
    state.setdefault("history", []).append(entry)


def _relabel(
    state: dict[str, Any],
    message: dict[str, Any],
    add: list[str],
    remove: list[str],
) -> None:
    before = list(message.get("labelIds") or [])
    removed = [label for label in before if label in set(remove)]
    kept = [label for label in before if label not in set(remove)]
    added = list(dict.fromkeys(label for label in add if label not in kept))
    message["labelIds"] = kept + added
    if added or removed:
        _record_change(state, message, {"labelsAdded": added, "labelsRemoved": removed})


def _from_raw(
    state: dict[str, Any], raw: str | None, thread_id: str | None, labels: list[str]
) -> dict[str, Any]:
    message_id = _next_id(state, "sandbox")
    message = gmail_message(
        {
            **_fields_from_raw(raw),
            "id": message_id,
            "threadId": thread_id or message_id,
            "labelIds": labels,
            "internalDate": _created_millis(state),
        }
    )
    message["bitfabCreated"] = True
    state["messages"].append(message)
    _record_change(state, message, {"messagesAdded": True})
    return message


def _send(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    body = params.get("body") or {}
    message = _from_raw(state, body.get("raw"), body.get("threadId"), ["SENT"])
    return {
        "id": message["id"],
        "threadId": message["threadId"],
        "labelIds": message["labelIds"],
    }


def _bad_request(text: str) -> dict[str, Any]:
    return {
        HTTP_ERROR_KEY: {
            "code": 400,
            "message": text,
            "status": "INVALID_ARGUMENT",
            "errors": [
                {"message": text, "domain": "global", "reason": "invalidArgument"}
            ],
        }
    }


def _find_draft(state: dict[str, Any], draft_id: Any) -> dict[str, Any] | None:
    return next((d for d in state["drafts"] if d.get("id") == draft_id), None)


def _new_draft_message(
    state: dict[str, Any], inner: dict[str, Any], thread_id: str | None
) -> dict[str, Any]:
    message = _from_raw(
        state, inner.get("raw"), inner.get("threadId") or thread_id, ["DRAFT"]
    )
    return message


def _draft_create(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    inner = (params.get("body") or {}).get("message") or {}
    message = _new_draft_message(state, inner, None)
    draft = {"id": _next_id(state, "r-sandbox"), "message": _draft_ref(message)}
    state["drafts"].append(draft)
    return copy.deepcopy(draft)


def _draft_get(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    draft = _find_draft(state, params.get("id"))
    if draft is None:
        return _not_found(f"draft {params.get('id')}")
    message = _find(state, draft["message"]["id"])
    if message is None:
        return _not_found(f"message {draft['message']['id']}")
    fmt = str(params.get("format") or "full").lower()
    return {"id": draft["id"], "message": _shaped(message, fmt, None)}


def _replace_draft_message(
    state: dict[str, Any], draft: dict[str, Any], inner: dict[str, Any]
) -> None:
    old = _find(state, draft["message"]["id"])
    if old is not None:
        _remove_message(state, old)
    message = _new_draft_message(
        state, inner, (old or draft["message"]).get("threadId")
    )
    draft["message"] = _draft_ref(message)


def _draft_update(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    draft = _find_draft(state, params.get("id"))
    if draft is None:
        return _not_found(f"draft {params.get('id')}")
    inner = (params.get("body") or {}).get("message") or {}
    if not inner.get("raw"):
        return _bad_request("Missing draft message")
    _replace_draft_message(state, draft, inner)
    return copy.deepcopy(draft)


def _draft_delete(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    draft = _find_draft(state, params.get("id"))
    if draft is None:
        return _not_found(f"draft {params.get('id')}")
    state["drafts"].remove(draft)
    message = _find(state, draft["message"]["id"])
    if message is not None:
        _remove_message(state, message)
    return {}


def _mark_sent(state: dict[str, Any], message: dict[str, Any]) -> dict[str, Any]:
    _relabel(state, message, ["SENT"], ["DRAFT"])
    return {
        "id": message["id"],
        "threadId": message["threadId"],
        "labelIds": message["labelIds"],
    }


def _draft_send(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    body = params.get("body") or {}
    inner = body.get("message") or {}
    draft_id = body.get("id")
    if draft_id is None:
        if not inner.get("raw"):
            return _bad_request("Missing draft id or message")
        return _mark_sent(state, _new_draft_message(state, inner, None))
    draft = _find_draft(state, draft_id)
    if draft is None:
        return _not_found(f"draft {draft_id}")
    if inner.get("raw"):
        _replace_draft_message(state, draft, inner)
    state["drafts"].remove(draft)
    message = _find(state, draft["message"]["id"])
    if message is None:
        return _not_found(f"message {draft['message']['id']}")
    return _mark_sent(state, message)


def _modify(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    message = _find(state, str(params.get("id")))
    if message is None:
        return _not_found(f"message {params.get('id')}")
    body = params.get("body") or {}
    _relabel(
        state,
        message,
        list(body.get("addLabelIds") or []),
        list(body.get("removeLabelIds") or []),
    )
    return _shaped(message, "minimal", None)


def _trash(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    message = _find(state, str(params.get("id")))
    if message is None:
        return _not_found(f"message {params.get('id')}")
    _relabel(state, message, ["TRASH"], [])
    return _shaped(message, "minimal", None)


def _untrash(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    message = _find(state, str(params.get("id")))
    if message is None:
        return _not_found(f"message {params.get('id')}")
    _relabel(state, message, [], ["TRASH"])
    return _shaped(message, "minimal", None)


def _remove_message(state: dict[str, Any], message: dict[str, Any]) -> None:
    state["messages"].remove(message)
    _record_change(state, message, {"messagesDeleted": True})


def _delete(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    message = _find(state, str(params.get("id")))
    if message is None:
        return _not_found(f"message {params.get('id')}")
    state["drafts"] = [
        d for d in state["drafts"] if d.get("message", {}).get("id") != message["id"]
    ]
    _remove_message(state, message)
    return {}


def _batch_modify(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    body = params.get("body") or {}
    for message_id in body.get("ids") or []:
        message = _find(state, str(message_id))
        if message is None:
            _note(
                state,
                f"batchModify skipped message {message_id}, which is not in the mailbox",
            )
            continue
        _relabel(
            state,
            message,
            list(body.get("addLabelIds") or []),
            list(body.get("removeLabelIds") or []),
        )
    return {}


def _thread_modify(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    thread_id = str(params.get("id"))
    messages = _thread_messages(state, thread_id)
    if not messages:
        return _not_found(f"thread {thread_id}")
    body = params.get("body") or {}
    for message in messages:
        _relabel(
            state,
            message,
            list(body.get("addLabelIds") or []),
            list(body.get("removeLabelIds") or []),
        )
    return _minimal_thread(thread_id, messages)


def _thread_trash(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    thread_id = str(params.get("id"))
    messages = _thread_messages(state, thread_id)
    if not messages:
        return _not_found(f"thread {thread_id}")
    for message in messages:
        _relabel(state, message, ["TRASH"], [])
    return _minimal_thread(thread_id, messages)


def _minimal_thread(thread_id: str, messages: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(messages, key=lambda m: int(m.get("internalDate") or 0))
    return {
        "id": thread_id,
        "historyId": str(max(int(m.get("historyId") or 0) for m in ordered)),
        "messages": [_shaped(m, "minimal", None) for m in ordered],
    }


def _thread(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    thread_id = str(params.get("id"))
    messages = _thread_messages(state, thread_id)
    if not messages:
        return _not_found(f"thread {thread_id}")
    fmt = str(params.get("format") or "full").lower()
    ordered = sorted(messages, key=lambda m: int(m.get("internalDate") or 0))
    return {
        "id": thread_id,
        "messages": [_shaped(m, fmt, params.get("metadataHeaders")) for m in ordered],
    }


def _wanted_types(params: dict[str, Any]) -> set[str]:
    given = params.get("historyTypes") or []
    names = [given] if isinstance(given, str) else list(given)
    chosen = {_HISTORY_TYPES[n] for n in names if n in _HISTORY_TYPES}
    return chosen or set(_HISTORY_TYPES.values())


def _touches_label(entry: dict[str, Any], label: str) -> bool:
    return any(
        label in (change["message"].get("labelIds") or [])
        or label in (change.get("labelIds") or [])
        for key in _HISTORY_TYPES.values()
        for change in entry.get(key) or []
    )


def _history(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    start = int(params.get("startHistoryId") or 0)
    wanted = _wanted_types(params)
    label = params.get("labelId")
    entries = []
    for entry in state.get("history") or []:
        if int(entry["id"]) <= start:
            continue
        kept = {
            key: copy.deepcopy(value)
            for key, value in entry.items()
            if key in {"id", "messages"} or key in wanted
        }
        if len(kept) == 2:
            continue
        if label and not _touches_label(kept, str(label)):
            continue
        entries.append(kept)
    size = min(int(params.get("maxResults") or 100), 500)
    offset = int(params.get("pageToken") or 0)
    reply: dict[str, Any] = {"historyId": str(state.get("historyId") or 1000)}
    page = entries[offset : offset + size]
    if page:
        reply["history"] = page
    if offset + size < len(entries):
        reply["nextPageToken"] = str(offset + size)
    return reply


def _attachment(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    message = _find(state, str(params.get("messageId")))
    if message is None:
        return _not_found(f"message {params.get('messageId')}")
    part = next(
        (
            p
            for p in _attachments(message.get("payload") or {})
            if (p.get("body") or {}).get("attachmentId") == params.get("id")
        ),
        None,
    )
    data = (part or {}).get("body", {}).get("data") if part else None
    if not data:
        _note(
            state,
            f"attachment {params.get('id')} on message {params.get('messageId')} was not recorded",
        )
        return _not_found(f"attachment {params.get('id')}")
    return {
        "attachmentId": params.get("id"),
        "size": part["body"].get("size", 0),
        "data": data,
    }


def _profile(state: dict[str, Any], _params: dict[str, Any]) -> dict[str, Any]:
    threads = {m.get("threadId") for m in state["messages"]}
    return {
        "emailAddress": state.get("emailAddress"),
        "messagesTotal": len(state["messages"]),
        "threadsTotal": len(threads),
        "historyId": str(state.get("historyId") or 1000),
    }


def _all_labels(state: dict[str, Any]) -> list[dict[str, Any]]:
    found = [{"id": label, "name": label, "type": "system"} for label in SYSTEM_LABELS]
    known = set(SYSTEM_LABELS)
    for label in state.setdefault("labels", []):
        if label["id"] not in known:
            known.add(label["id"])
            found.append(label)
    for message in state["messages"]:
        for label_id in message.get("labelIds") or []:
            if label_id in known:
                continue
            known.add(label_id)
            _note(
                state,
                f"label {label_id} was only seen on messages, so its name is its id",
            )
            found.append(_user_label({"id": label_id, "name": label_id}))
    return found


def _labels(state: dict[str, Any], _params: dict[str, Any]) -> dict[str, Any]:
    return {"labels": _all_labels(state)}


def _label_get(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    wanted = str(params.get("id"))
    label = next((lb for lb in _all_labels(state) if lb["id"] == wanted), None)
    if label is None:
        return _not_found(f"label {wanted}")
    return copy.deepcopy(label)


def _conflict(message: str) -> dict[str, Any]:
    return {
        HTTP_ERROR_KEY: {
            "code": 409,
            "message": message,
            "status": "ABORTED",
            "errors": [{"message": message, "domain": "global", "reason": "aborted"}],
        }
    }


def _invalid(message: str) -> dict[str, Any]:
    return {
        HTTP_ERROR_KEY: {
            "code": 400,
            "message": message,
            "status": "INVALID_ARGUMENT",
            "errors": [{"message": message, "domain": "global", "reason": "invalid"}],
        }
    }


def _label_create(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    body = params.get("body") or {}
    name = str(body.get("name") or "").strip()
    if not name:
        return _invalid("Invalid label name")
    if any(lb["name"].lower() == name.lower() for lb in _all_labels(state)):
        return _conflict("Label name exists or conflicts")
    label = _user_label(
        {
            **{k: v for k, v in body.items() if k not in {"id", "type"}},
            "id": _next_id(state, "Label_sandbox"),
            "name": name,
        }
    )
    state["labels"].append(label)
    return copy.deepcopy(label)


def _send_as(state: dict[str, Any], _params: dict[str, Any]) -> dict[str, Any]:
    recorded = state.get("sendAs")
    if recorded is not None:
        return {"sendAs": copy.deepcopy(recorded)}
    address = state.get("emailAddress")
    if not address:
        _note(
            state,
            "the account's address was never recorded, so it has no send-as addresses",
        )
        return {"sendAs": []}
    _note(
        state,
        "send-as settings were never recorded, so the account's own address is "
        "listed with no display name or signature",
    )
    return {
        "sendAs": [
            {
                "sendAsEmail": address,
                "displayName": "",
                "replyToAddress": "",
                "signature": "",
                "isPrimary": True,
                "isDefault": True,
                "treatAsAlias": False,
                "verificationStatus": "accepted",
            }
        ]
    }


def _drafts_list(state: dict[str, Any], _params: dict[str, Any]) -> dict[str, Any]:
    return {
        "drafts": copy.deepcopy(state["drafts"]),
        "resultSizeEstimate": len(state["drafts"]),
    }


HANDLERS: dict[str, Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]] = {
    LIST_METHOD: _list,
    GET_METHOD: _get,
    "gmail.users.messages.send": _send,
    "gmail.users.messages.modify": _modify,
    "gmail.users.messages.batchModify": _batch_modify,
    "gmail.users.messages.trash": _trash,
    "gmail.users.messages.untrash": _untrash,
    "gmail.users.messages.delete": _delete,
    "gmail.users.messages.attachments.get": _attachment,
    DRAFT_CREATE_METHOD: _draft_create,
    DRAFT_GET_METHOD: _draft_get,
    "gmail.users.drafts.update": _draft_update,
    "gmail.users.drafts.delete": _draft_delete,
    "gmail.users.drafts.send": _draft_send,
    DRAFT_LIST_METHOD: _drafts_list,
    "gmail.users.threads.get": _thread,
    "gmail.users.threads.list": _threads_list,
    "gmail.users.threads.modify": _thread_modify,
    "gmail.users.threads.trash": _thread_trash,
    "gmail.users.history.list": _history,
    LABELS_LIST_METHOD: _labels,
    LABEL_GET_METHOD: _label_get,
    "gmail.users.labels.create": _label_create,
    SEND_AS_LIST_METHOD: _send_as,
    PROFILE_METHOD: _profile,
}


class GmailAccountError(LookupError):
    pass


def _same_address(left: Any, right: Any) -> bool:
    return (
        isinstance(left, str)
        and isinstance(right, str)
        and left.lower() == right.lower()
    )


def choose_mailbox(
    state: dict[str, Any],
    params: dict[str, Any],
    account: Callable[[Any], str | None] | None,
) -> dict[str, Any]:
    boxes = state["mailboxes"]
    credentials = request_credentials()
    wanted = (
        account(credentials)
        if account is not None
        else getattr(credentials, "account", None) or None
    )
    user_id = params.get("userId")
    if wanted is None and isinstance(user_id, str) and "@" in user_id:
        wanted = user_id
    if wanted is not None:
        found = next(
            (b for b in boxes if _same_address(b.get("emailAddress"), wanted)), None
        )
        if found is not None:
            return found
        if len(boxes) == 1 and not boxes[0].get("emailAddress"):
            return boxes[0]
        empty = _empty_mailbox_for(boxes, wanted)
        boxes.append(empty)
        return empty
    credential = params.get(CREDENTIAL_PARAM)
    found = next(
        (b for b in boxes if credential and b.get("credential") == credential), None
    )
    if found is not None:
        return found
    if len(boxes) == 1:
        return boxes[0]
    known = ", ".join(str(b.get("emailAddress") or b.get("credential")) for b in boxes)
    raise GmailAccountError(
        f"The Gmail sandbox has {len(boxes)} mailboxes ({known}) and cannot tell "
        f"which one this call is for{f' ({wanted})' if wanted else ''}. Pass "
        "gmail_sandbox(account=...) to name the account from the call's "
        "credentials, or call Gmail with userId set to the account's address."
    )


def _empty_mailbox_for(boxes: list[dict[str, Any]], address: str) -> dict[str, Any]:
    clock = next((b.get("clock") for b in boxes if b.get("clock")), None)
    return {
        "emailAddress": address,
        "credential": None,
        "details": {},
        "clock": clock,
        "historyId": 1000,
        "nextId": len(boxes) * 1_000_000 + 1,
        "messages": [],
        "drafts": [],
        "searches": [],
        "labels": [],
        "sendAs": None,
        "history": [],
        "notes": [f"{address} had no mailbox in the original run, so it starts empty"],
    }


def answer_gmail_call(
    state: dict[str, Any],
    call: MockOverrideCtx,
    account: Callable[[Any], str | None] | None = None,
) -> Any:
    method = call.node.trace_function_key
    handler = HANDLERS.get(method)
    if handler is None:
        raise NotImplementedError(
            f"The Gmail sandbox does not answer {method} yet. It answers "
            f"{', '.join(sorted(HANDLERS))}."
        )
    params = dict(call.kwargs)
    return handler(choose_mailbox(state, params, account), params)


def is_gmail_call(node: SpanNodeMeta) -> bool:
    return node.trace_function_key.startswith("gmail.")


def gmail_sandbox(
    start: Callable[[SandboxStartCtx], Any] | None = None,
    account: Callable[[Any], str | None] | None = None,
) -> Sandbox:
    """The Gmail sandbox: answers Gmail API calls during replay from a mailbox.

    It answers calls made through Google's Python client
    (``googleapiclient``), keeping sends, drafts and label changes in the
    mailbox for the rest of the replay item, along with trashed, deleted
    and relabeled messages and threads. It is on by default; pass it
    only to change where its mailbox comes from.

    Args:
        start: Builds the mailbox for one replay item from a
            ``SandboxStartCtx``. Return a list of messages, or
            ``{"messages": [...], "emailAddress": ..., "drafts": [...],
            "labels": [...], "sendAs": [...]}``. ``labels`` are the account's
            own labels, each a Gmail label or a name; ``sendAs`` are Gmail
            send-as entries (``sendAsEmail``, ``displayName``, ``signature``,
            ...). Without ``sendAs``, the account's address is listed with no
            signature.
            ``clock`` (ISO 8601) is where the mailbox's time starts, in place
            of the original trace's start time.
            Each message is a Gmail API message or plain fields as
            ``gmail_message`` takes them; a plain ``account`` field puts the
            message in that account's mailbox. Each draft is
            ``{"id": ..., "message": ...}``, where the message is a Gmail API
            message (as ``drafts.get`` returns it, ``raw`` included), plain
            fields, or only the ``id`` of a message in ``messages``. For several accounts, return
            ``{"mailboxes": [{"emailAddress": ..., "messages": [...]}]}``.
            ``None`` uses ``mailbox_from_recorded_calls``.
        account: With several mailboxes, names the account a call is for
            from the Google credentials it was made with, returning the
            account's address. ``None`` routes by a ``userId`` that is an
            address, then by the credential the original calls used, then
            to the only mailbox; a call it cannot place fails the item.
    """
    chosen = start or mailbox_from_recorded_calls
    return Sandbox(
        name=GMAIL_SANDBOX_NAME,
        match=is_gmail_call,
        handle=lambda state, call: answer_gmail_call(state, call, account),
        start=lambda ctx: as_mailboxes(ctx, chosen(ctx)),
        integration="gmail",
    )


class SandboxGoogleCredentials:
    def __init__(self, account: str | None) -> None:
        self.account = account
        self.token = None
        self.refresh_token = None


class GoogleSandboxHttp:
    def __init__(self, account: str | None) -> None:
        self.credentials = SandboxGoogleCredentials(account)

    def request(self, uri: str, *args: Any, **kwargs: Any) -> Any:
        raise ServiceCallHeldBackError(
            f"{uri} was sent through bitfab.google_sandbox_http, which never "
            "reaches Google; only a replay item with a sandbox for this service "
            "can answer it."
        )


def google_sandbox_http(account: str | None = None) -> GoogleSandboxHttp:
    """A transport for building a Google API client with no credentials during replay.

    ``build("gmail", "v1", http=bitfab.google_sandbox_http(account="me@x.com"))``
    builds a client whose calls the Gmail sandbox answers from ``account``'s
    mailbox. Nothing sent through it ever reaches Google: outside a sandboxed
    replay each call raises. Use it where a replay has no real Google
    credentials to build the client from.

    Args:
        account: The address whose mailbox answers this client's calls.
            ``None`` uses the only mailbox.
    """
    return GoogleSandboxHttp(account)


def gmail_sandbox_accounts() -> list[dict[str, Any]]:
    """The accounts the Gmail sandbox has mailboxes for in this replay item.

    Each is ``{"emailAddress": ..., **details}``, where ``details`` is what
    ``start`` put on that mailbox. Empty outside a replay item or when the
    Gmail sandbox is off. Use it to list connected accounts during a replay
    that holds no real ones.
    """
    state = sandbox_state(GMAIL_SANDBOX_NAME)
    if not isinstance(state, dict):
        return []
    return [
        {**(box.get("details") or {}), "emailAddress": box.get("emailAddress")}
        for box in state.get("mailboxes") or []
    ]
