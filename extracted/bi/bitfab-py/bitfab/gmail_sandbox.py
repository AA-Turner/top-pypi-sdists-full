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
from bitfab.sandbox import Sandbox, SandboxStartCtx, sandbox_state
from bitfab.service_calls import ServiceCallHeldBackError

GMAIL_SANDBOX_NAME = "Gmail"
GET_METHOD = "gmail.users.messages.get"
LIST_METHOD = "gmail.users.messages.list"
PROFILE_METHOD = "gmail.users.getProfile"
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
_RELATIVE = re.compile(r"^(\d+)([dmy])$")


def _b64(text: str) -> str:
    return base64.urlsafe_b64encode(text.encode("utf-8")).decode("ascii").rstrip("=")


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
    (``gmail.users.messages.get`` replies) and each account's address from
    ``gmail.users.getProfile``, one mailbox per credential the calls used.
    """
    if ctx.recorded_state is not None:
        return as_mailboxes(ctx, ctx.recorded_state)
    by_credential: dict[str | None, dict[str, Any]] = {}
    for name in (GET_METHOD, PROFILE_METHOD, LIST_METHOD):
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
                    "searches": [],
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
    boxes = [
        {**box, "messages": list(box["messages"].values())}
        for box in by_credential.values()
    ]
    return as_mailboxes(ctx, {"mailboxes": boxes or [{}]})


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
            )
            for index, box in enumerate(boxes or [{}])
        ]
    }


def new_mailbox(
    ctx: SandboxStartCtx,
    index: int,
    messages: list[dict[str, Any]] | None = None,
    email_address: str | None = None,
    credential: str | None = None,
    drafts: list[dict[str, Any]] | None = None,
    details: dict[str, Any] | None = None,
    searches: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    normalized = [gmail_message(message) for message in messages or []]
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
        "clock": ctx.trace_started_at,
        "historyId": 1000,
        "nextId": index * 1_000_000 + 1,
        "messages": normalized,
        "drafts": list(drafts or []),
        "searches": list(searches or []),
        "notes": [],
    }


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
    return _millis(state.get("clock")) or int(
        datetime.datetime.now(datetime.timezone.utc).timestamp() * 1000
    )


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
        return wanted == "ANYWHERE" or wanted in labels or value in labels
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


def _is_free_text(term: str) -> bool:
    return bool(term) and not term.startswith("-") and not _OPERATOR.match(term)


_DATE_OPERATORS = ("after:", "before:", "newer_than:", "older_than:")


def search_key(query: str) -> str:
    return " ".join(
        sorted(
            t.lower()
            for t in _TOKEN.findall(query or "")
            if t != "AND" and not t.lower().startswith(_DATE_OPERATORS)
        )
    )


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


def _matches_every_term(
    state: dict[str, Any], message: dict[str, Any], terms: list[str]
) -> bool:
    return all(
        (not _term_matches(state, message, t[1:]))
        if t.startswith("-") and len(t) > 1
        else _term_matches(state, message, t)
        for t in terms
        if t
    )


def _search(
    state: dict[str, Any], query: str, include_spam_trash: bool
) -> list[dict[str, Any]]:
    terms = [t for t in _TOKEN.findall(query or "") if t not in {"(", ")", "AND"}]
    if "OR" in terms or any(t.startswith("{") or t.startswith("(") for t in terms):
        _note(
            state, "OR and grouped searches are matched as if every word were required"
        )
    terms = [t.strip("(){}") for t in terms if t != "OR"]
    same = _same_search(state, query)
    if same is not None:
        by_id = {m.get("id"): m for m in state["messages"]}
        created = [
            m
            for m in state["messages"]
            if m.get("bitfabCreated") and _matches_every_term(state, m, terms)
        ]
        dates = [t for t in terms if t.lower().startswith(_DATE_OPERATORS)]
        recorded = [
            by_id[i]
            for i in same
            if i in by_id and all(_term_matches(state, by_id[i], t) for t in dates)
        ]
        newest_first = sorted(
            created, key=lambda m: int(m.get("internalDate") or 0), reverse=True
        )
        return newest_first + recorded
    known = _known_results(state, _text_key(query))
    if known is not None:
        free = [t for t in terms if _is_free_text(t)]
        terms = [t for t in terms if not _is_free_text(t)]
    found = []
    for message in state["messages"]:
        labels = set(message.get("labelIds") or [])
        searching_everywhere = any(
            t.lower() in {"in:anywhere", "in:spam", "in:trash"} for t in terms
        )
        if (
            not include_spam_trash
            and not searching_everywhere
            and labels & {"SPAM", "TRASH"}
        ):
            continue
        if known is not None and (
            message.get("id") not in known
            if not message.get("bitfabCreated")
            else not all(_term_matches(state, message, t) for t in free)
        ):
            continue
        if _matches_every_term(state, message, terms):
            found.append(message)
    return sorted(found, key=lambda m: int(m.get("internalDate") or 0), reverse=True)


def _list(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    matched = _search(
        state,
        str(params.get("q") or ""),
        str(params.get("includeSpamTrash")).lower() == "true",
    )
    label_ids = params.get("labelIds") or []
    if isinstance(label_ids, str):
        label_ids = [label_ids]
    matched = [m for m in matched if set(label_ids) <= set(m.get("labelIds") or [])]
    size = min(int(params.get("maxResults") or 100), 500)
    offset = int(params.get("pageToken") or 0)
    page = matched[offset : offset + size]
    reply: dict[str, Any] = {"resultSizeEstimate": len(matched)}
    if page:
        reply["messages"] = [
            {"id": m["id"], "threadId": m.get("threadId")} for m in page
        ]
    if offset + size < len(matched):
        reply["nextPageToken"] = str(offset + size)
    return reply


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


def _from_raw(
    state: dict[str, Any], raw: str | None, thread_id: str | None, labels: list[str]
) -> dict[str, Any]:
    parsed = email.message_from_string(
        _unb64(raw) if raw else "", policy=email.policy.default
    )
    body_part = (
        parsed.get_body(preferencelist=("plain", "html"))
        if parsed.is_multipart()
        else parsed
    )
    body = body_part.get_content() if body_part is not None else ""
    fields = {
        key: parsed.get(header)
        for key, header in _PLAIN_HEADERS.items()
        if parsed.get(header)
    }
    message_id = _next_id(state, "sandbox")
    message = gmail_message(
        {
            **fields,
            "id": message_id,
            "threadId": thread_id or message_id,
            "body": str(body),
            "labelIds": labels,
            "internalDate": _clock_millis(state),
        }
    )
    message["historyId"] = _bump_history(state)
    message["bitfabCreated"] = True
    return message


def _send(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    body = params.get("body") or {}
    message = _from_raw(state, body.get("raw"), body.get("threadId"), ["SENT"])
    state["messages"].append(message)
    return {
        "id": message["id"],
        "threadId": message["threadId"],
        "labelIds": message["labelIds"],
    }


def _draft_create(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    inner = (params.get("body") or {}).get("message") or {}
    message = _from_raw(state, inner.get("raw"), inner.get("threadId"), ["DRAFT"])
    state["messages"].append(message)
    draft = {
        "id": _next_id(state, "r-sandbox"),
        "message": {
            "id": message["id"],
            "threadId": message["threadId"],
            "labelIds": ["DRAFT"],
        },
    }
    state["drafts"].append(draft)
    return draft


def _draft_send(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    draft_id = (params.get("body") or {}).get("id")
    draft = next((d for d in state["drafts"] if d.get("id") == draft_id), None)
    if draft is None:
        return _not_found(f"draft {draft_id}")
    state["drafts"].remove(draft)
    message = _find(state, draft["message"]["id"])
    if message is None:
        return _not_found(f"message {draft['message']['id']}")
    message["labelIds"] = [
        label for label in message.get("labelIds") or [] if label != "DRAFT"
    ] + ["SENT"]
    message["historyId"] = _bump_history(state)
    return {
        "id": message["id"],
        "threadId": message["threadId"],
        "labelIds": message["labelIds"],
    }


def _modify(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    message = _find(state, str(params.get("id")))
    if message is None:
        return _not_found(f"message {params.get('id')}")
    body = params.get("body") or {}
    labels = [
        label
        for label in message.get("labelIds") or []
        if label not in set(body.get("removeLabelIds") or [])
    ]
    labels += [label for label in body.get("addLabelIds") or [] if label not in labels]
    message["labelIds"] = labels
    message["historyId"] = _bump_history(state)
    return _shaped(message, "minimal", None)


def _thread(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    thread_id = str(params.get("id"))
    messages = [m for m in state["messages"] if m.get("threadId") == thread_id]
    if not messages:
        return _not_found(f"thread {thread_id}")
    fmt = str(params.get("format") or "full").lower()
    ordered = sorted(messages, key=lambda m: int(m.get("internalDate") or 0))
    return {
        "id": thread_id,
        "messages": [_shaped(m, fmt, params.get("metadataHeaders")) for m in ordered],
    }


def _history(state: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    start = int(params.get("startHistoryId") or 0)
    added = [m for m in state["messages"] if int(m.get("historyId") or 0) > start]
    reply: dict[str, Any] = {"historyId": str(state.get("historyId") or 1000)}
    if added:
        reply["history"] = [
            {
                "id": m["historyId"],
                "messagesAdded": [
                    {
                        "message": {
                            "id": m["id"],
                            "threadId": m.get("threadId"),
                            "labelIds": m.get("labelIds"),
                        }
                    }
                ],
            }
            for m in added
        ]
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


def _labels(_state: dict[str, Any], _params: dict[str, Any]) -> dict[str, Any]:
    return {
        "labels": [
            {"id": label, "name": label, "type": "system"} for label in SYSTEM_LABELS
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
    "gmail.users.messages.attachments.get": _attachment,
    "gmail.users.drafts.create": _draft_create,
    "gmail.users.drafts.send": _draft_send,
    "gmail.users.drafts.list": _drafts_list,
    "gmail.users.threads.get": _thread,
    "gmail.users.history.list": _history,
    "gmail.users.labels.list": _labels,
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
    mailbox for the rest of the replay item. It is on by default; pass it
    only to change where its mailbox comes from.

    Args:
        start: Builds the mailbox for one replay item from a
            ``SandboxStartCtx``. Return a list of messages, or
            ``{"messages": [...], "emailAddress": ..., "drafts": [...]}``.
            Each message is a Gmail API message or plain fields as
            ``gmail_message`` takes them; a plain ``account`` field puts the
            message in that account's mailbox. For several accounts, return
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


def default_sandboxes() -> list[Sandbox]:
    return [gmail_sandbox()]


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
