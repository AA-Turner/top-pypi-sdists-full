from __future__ import annotations

import copy
import datetime
import json
import os
import re
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from typing import Any

from bitfab.gmail_sandbox import (
    PROFILE_METHOD,
    GmailAccountError,
    _attachment,
    _batch_modify,
    _clock_millis,
    _conflict,
    _delete,
    _draft_create,
    _draft_delete,
    _draft_get,
    _draft_ref,
    _draft_send,
    _draft_update,
    _find,
    _find_draft,
    _get,
    _history,
    _label_create,
    _leaves,
    _matches,
    _matching,
    _millis,
    _modify,
    _not_found,
    _note,
    _relative_millis,
    _same_address,
    _send,
    _shaped,
    _term_matches,
    _thread_modify,
    _thread_trash,
    _trash,
    _untrash,
    as_mailboxes,
    parse_query,
)
from bitfab.google_calls import CREDENTIAL_PARAM, HTTP_ERROR_KEY, request_credentials
from bitfab.mock_override import MockOverrideCtx
from bitfab.sandbox import SandboxStartCtx, fail_replay_item

READ_REAL_WRITE_FAKE = "read-real-write-fake"
API_URL = "https://gmail.googleapis.com/gmail/v1/users/me"
TOKEN_URL = "https://oauth2.googleapis.com/token"
CREDENTIALS_ENV = "BITFAB_GMAIL_CREDENTIALS"
CLIENT_ID_ENV = "BITFAB_GMAIL_CLIENT_ID"
CLIENT_SECRET_ENV = "BITFAB_GMAIL_CLIENT_SECRET"
TIMEOUT_SECONDS = 60.0
TOKEN_MARGIN_SECONDS = 60.0
HIDDEN_LABELS = frozenset({"SPAM", "TRASH"})
SANDBOX_ID_PREFIX = "sandbox"
LABEL_OPERATORS = ("in:", "label:", "is:")
RATE_LIMIT_REASONS = ("ratelimit", "quota")
_RELATIVE_TERM = re.compile(
    r"(?<![^\s(){}])(-?)(newer_than|older_than):(\d+[dmy])(?![^\s(){}])", re.I
)

Transport = Callable[[str, str, dict[str, str], bytes | None], tuple[int, bytes]]
GmailCredentials = Mapping[str, Any] | Callable[[str], Any]


class GmailCredentialError(RuntimeError):
    pass


class GmailReadError(RuntimeError):
    pass


class GmailCutoffError(RuntimeError):
    pass


@dataclass(frozen=True)
class RefreshCredential:
    client_id: str
    token_uri: str
    refresh_token: str = field(repr=False)
    client_secret: str = field(repr=False)


def urllib_transport(
    method: str, url: str, headers: dict[str, str], body: bytes | None
) -> tuple[int, bytes]:
    request = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as error:
        return error.code, error.read()


def _decoded(raw: bytes) -> Any:
    try:
        return json.loads(raw.decode("utf-8")) if raw else {}
    except (UnicodeDecodeError, ValueError):
        return {}


def _env_credentials() -> dict[str, Any]:
    raw = os.environ.get(CREDENTIALS_ENV)
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except ValueError:
        raise ValueError(
            f"{CREDENTIALS_ENV} must be a JSON object mapping each Gmail address "
            "to its OAuth refresh token or to {refresh_token, client_id, "
            "client_secret}."
        ) from None
    if not isinstance(parsed, dict):
        raise ValueError(f"{CREDENTIALS_ENV} must be a JSON object keyed by address.")
    return parsed


def _missing(address: str) -> GmailCredentialError:
    return GmailCredentialError(
        f"The Gmail sandbox reads {address}'s real mailbox in "
        f"{READ_REAL_WRITE_FAKE} mode, but has no credential for it. Pass "
        f'gmail_sandbox(mode="{READ_REAL_WRITE_FAKE}", credentials=...) with '
        f"an OAuth refresh token for {address}, or add it to {CREDENTIALS_ENV}."
    )


def _field(given: Any, name: str) -> Any:
    if isinstance(given, Mapping):
        return given.get(name)
    return getattr(given, name, None)


def refresh_credential(given: Any, address: str) -> RefreshCredential:
    if given is None:
        raise _missing(address)
    token = given if isinstance(given, str) else _field(given, "refresh_token")
    client_id = (
        None if isinstance(given, str) else _field(given, "client_id")
    ) or os.environ.get(CLIENT_ID_ENV)
    client_secret = (
        None if isinstance(given, str) else _field(given, "client_secret")
    ) or os.environ.get(CLIENT_SECRET_ENV)
    token_uri = (None if isinstance(given, str) else _field(given, "token_uri")) or (
        TOKEN_URL
    )
    if not token:
        raise GmailCredentialError(
            f"The Gmail credential for {address} has no refresh token."
        )
    if not client_id or not client_secret:
        raise GmailCredentialError(
            f"The Gmail credential for {address} needs the OAuth client it was "
            "issued to: give client_id and client_secret with it, or set "
            f"{CLIENT_ID_ENV} and {CLIENT_SECRET_ENV}."
        )
    return RefreshCredential(
        client_id=str(client_id),
        token_uri=str(token_uri),
        refresh_token=str(token),
        client_secret=str(client_secret),
    )


def _google_error(status: int, payload: Any) -> dict[str, Any]:
    error = payload.get("error") if isinstance(payload, dict) else None
    if isinstance(error, dict):
        return {"code": status, **error}
    return {
        "code": status,
        "message": f"Gmail answered HTTP {status}",
        "status": "UNKNOWN",
        "errors": [],
    }


def _is_rate_limit(payload: Any) -> bool:
    reasons = [
        str(entry.get("reason") or "").lower()
        for entry in _google_error(0, payload).get("errors") or []
        if isinstance(entry, dict)
    ]
    return any(word in reason for reason in reasons for word in RATE_LIMIT_REASONS)


@dataclass
class LiveGmail:
    credentials: GmailCredentials | None
    transport: Transport | None = None
    _tokens: dict[str, tuple[str, float]] = field(default_factory=dict)
    _lock: threading.Lock = field(default_factory=threading.Lock)

    def _source(self) -> GmailCredentials:
        return self.credentials if self.credentials is not None else _env_credentials()

    def addresses(self) -> list[str]:
        source = self._source()
        return [str(key) for key in source] if isinstance(source, Mapping) else []

    def credential(self, address: str) -> RefreshCredential:
        source = self._source()
        if isinstance(source, Mapping):
            given = next(
                (v for k, v in source.items() if _same_address(str(k), address)),
                None,
            )
        else:
            given = source(address)
        return refresh_credential(given, address)

    def _send(
        self, method: str, url: str, headers: dict[str, str], body: bytes | None
    ) -> tuple[int, Any]:
        send = self.transport or urllib_transport
        try:
            status, raw = send(method, url, headers, body)
        except OSError as error:
            raise GmailReadError(
                f"The Gmail sandbox could not reach Google ({type(error).__name__}: "
                f"{error})."
            ) from None
        return status, _decoded(raw)

    def _token(self, address: str) -> str:
        key = address.lower()
        with self._lock:
            cached = self._tokens.get(key)
            if cached is not None and cached[1] > time.time() + TOKEN_MARGIN_SECONDS:
                return cached[0]
            credential = self.credential(address)
            body = urllib.parse.urlencode(
                {
                    "grant_type": "refresh_token",
                    "refresh_token": credential.refresh_token,
                    "client_id": credential.client_id,
                    "client_secret": credential.client_secret,
                }
            ).encode("ascii")
            status, payload = self._send(
                "POST",
                credential.token_uri,
                {"Content-Type": "application/x-www-form-urlencoded"},
                body,
            )
            token = payload.get("access_token") if isinstance(payload, dict) else None
            if status != 200 or not token:
                reason = (
                    payload.get("error_description") or payload.get("error")
                    if isinstance(payload, dict)
                    else None
                ) or f"HTTP {status}"
                raise GmailCredentialError(
                    f"Google refused the Gmail credential for {address} ({reason}). "
                    "Check that the refresh token is current and was issued to "
                    "the OAuth client given with it."
                )
            expires_in = float(payload.get("expires_in") or 3600)
            self._tokens[key] = (str(token), time.time() + expires_in)
            return str(token)

    def get(self, address: str, path: str, query: dict[str, Any]) -> tuple[int, Any]:
        url = f"{API_URL}/{path}"
        if query:
            url = f"{url}?{urllib.parse.urlencode(query, doseq=True)}"
        for attempt in range(2):
            headers = {
                "Authorization": f"Bearer {self._token(address)}",
                "Accept": "application/json",
            }
            status, payload = self._send("GET", url, headers, None)
            if status == 401 and attempt == 0:
                with self._lock:
                    self._tokens.pop(address.lower(), None)
                continue
            break
        if status == 401 or (status == 403 and not _is_rate_limit(payload)):
            message = _google_error(status, payload).get("message") or ""
            raise GmailCredentialError(
                f"Gmail refused to read {address}'s mailbox (HTTP {status}: "
                f"{message}). The credential needs the "
                "https://www.googleapis.com/auth/gmail.readonly scope."
            )
        return status, payload


def _now_iso() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%S.%fZ"
    )


def _read_summary(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    summary: dict[str, Any] = {}
    if payload.get("id"):
        summary["id"] = str(payload["id"])
    if payload.get("historyId"):
        summary["historyId"] = str(payload["historyId"])
    for key in ("messages", "threads", "drafts"):
        entries = payload.get(key)
        if isinstance(entries, list):
            summary[key] = [
                {
                    "id": entry.get("id"),
                    **(
                        {"historyId": str(entry["historyId"])}
                        if entry.get("historyId")
                        else {}
                    ),
                }
                for entry in entries
                if isinstance(entry, dict)
            ]
    return summary


@dataclass(frozen=True)
class Reads:
    live: LiveGmail
    box: dict[str, Any]
    method: str

    def get(self, path: str, query: dict[str, Any] | None = None) -> dict[str, Any]:
        address = str(self.box["emailAddress"])
        status, payload = self.live.get(address, path, query or {})
        entry: dict[str, Any] = {
            "method": self.method,
            "path": path,
            "readAt": _now_iso(),
            "status": status,
        }
        if query:
            entry["query"] = query
        self.box.setdefault("liveReads", []).append({**entry, **_read_summary(payload)})
        if status >= 400:
            return {HTTP_ERROR_KEY: _google_error(status, payload)}
        return payload if isinstance(payload, dict) else {}


def _quoted(value: Any) -> str:
    return urllib.parse.quote(str(value), safe="")


def _cutoff(box: dict[str, Any]) -> int:
    cutoff = _millis(box.get("cutoff"))
    if cutoff is None:
        raise GmailCutoffError(
            f"The Gmail sandbox cannot read {box.get('emailAddress')}'s real "
            "mailbox: the original trace's start time is not known, so mail "
            "that arrived after it cannot be hidden."
        )
    return cutoff // 1000 * 1000


def _before_cutoff(box: dict[str, Any], message: dict[str, Any]) -> bool:
    return int(message.get("internalDate") or 0) < _cutoff(box)


def absolute_dates(query: str, now_millis: int) -> str:
    def swap(matched: re.Match[str]) -> str:
        span = _relative_millis(matched.group(3)) or 0
        operator = "after" if matched.group(2).lower() == "newer_than" else "before"
        return f"{matched.group(1)}{operator}:{(now_millis - span) // 1000}"

    return _RELATIVE_TERM.sub(swap, query)


def live_query(box: dict[str, Any], query: Any) -> str:
    text = absolute_dates(str(query or ""), _clock_millis(box)).strip()
    bound = f"before:{_cutoff(box) // 1000}"
    return f"({text}) {bound}" if text else bound


def _imported(box: dict[str, Any]) -> dict[str, str]:
    return box.setdefault("imported", {})


def _imported_drafts(box: dict[str, Any]) -> list[str]:
    return box.setdefault("importedDrafts", [])


def _adopt(box: dict[str, Any], message: dict[str, Any]) -> dict[str, Any]:
    adopted = {**copy.deepcopy(message), "bitfabFromLive": True}
    box["messages"].append(adopted)
    _imported(box)[str(adopted["id"])] = str(adopted.get("threadId") or adopted["id"])
    return adopted


def _gone(box: dict[str, Any], message_id: str) -> bool:
    return message_id in _imported(box) and _find(box, message_id) is None


def _import(reads: Reads, message_id: str) -> dict[str, Any]:
    box = reads.box
    local = _find(box, message_id)
    if local is not None:
        return local
    if message_id in _imported(box):
        return _not_found(f"message {message_id}")
    payload = reads.get(f"messages/{_quoted(message_id)}", {"format": "full"})
    if HTTP_ERROR_KEY in payload:
        return payload
    if not _before_cutoff(box, payload):
        return _not_found(f"message {message_id}")
    return _adopt(box, payload)


def _import_thread(reads: Reads, thread_id: str) -> dict[str, Any] | None:
    box = reads.box
    payload = reads.get(f"threads/{_quoted(thread_id)}", {"format": "full"})
    if HTTP_ERROR_KEY in payload:
        return None if payload[HTTP_ERROR_KEY].get("code") == 404 else payload
    for message in payload.get("messages") or []:
        message_id = str(message.get("id"))
        if message_id in _imported(box) or _find(box, message_id) is not None:
            continue
        if _before_cutoff(box, message):
            _adopt(box, message)
    return None


def _import_draft(reads: Reads, draft_id: Any) -> dict[str, Any] | None:
    box = reads.box
    if draft_id is None or _find_draft(box, draft_id) is not None:
        return None
    if str(draft_id) in _imported_drafts(box):
        return None
    payload = reads.get(f"drafts/{_quoted(draft_id)}", {"format": "full"})
    if HTTP_ERROR_KEY in payload:
        return payload
    message = payload.get("message") or {}
    if not _before_cutoff(box, message):
        return _not_found(f"draft {draft_id}")
    _imported_drafts(box).append(str(draft_id))
    message_id = str(message.get("id"))
    local = _find(box, message_id)
    if local is None and message_id in _imported(box):
        return _not_found(f"draft {draft_id}")
    local = local or _adopt(box, message)
    box["drafts"].append({"id": str(draft_id), "message": _draft_ref(local)})
    return None


def _overlay(box: dict[str, Any], message: dict[str, Any]) -> dict[str, Any] | None:
    message_id = str(message.get("id"))
    if message_id not in _imported(box):
        return message
    local = _find(box, message_id)
    if local is None:
        return None
    return {
        **message,
        "labelIds": list(local.get("labelIds") or []),
        "historyId": local.get("historyId") or message.get("historyId"),
    }


def _label_verdict(
    box: dict[str, Any], message: dict[str, Any], query: tuple[str, Any]
) -> bool | None:
    kind, value = query
    if kind == "term":
        if not str(value).lower().startswith(LABEL_OPERATORS):
            return None
        return _term_matches(box, message, value)
    if kind == "not":
        inner = _label_verdict(box, message, value)
        return None if inner is None else not inner
    verdicts = [_label_verdict(box, message, q) for q in value]
    if kind == "or":
        if any(v is True for v in verdicts):
            return True
        return None if any(v is None for v in verdicts) else False
    if any(v is False for v in verdicts):
        return False
    return None if any(v is None for v in verdicts) else True


def _requested_labels(params: dict[str, Any]) -> list[str]:
    given = params.get("labelIds") or []
    return [given] if isinstance(given, str) else [str(label) for label in given]


def _searches_hidden(params: dict[str, Any], query: tuple[str, Any]) -> bool:
    return str(params.get("includeSpamTrash")).lower() == "true" or any(
        leaf.lower() in {"in:anywhere", "in:spam", "in:trash"}
        for leaf in _leaves(query)
    )


def _still_listed(
    box: dict[str, Any],
    message: dict[str, Any],
    query: tuple[str, Any],
    params: dict[str, Any],
) -> bool:
    labels = set(message.get("labelIds") or [])
    if not set(_requested_labels(params)) <= labels:
        return False
    if labels & HIDDEN_LABELS and not _searches_hidden(params, query):
        return False
    return _label_verdict(box, message, query) is not False


def _own_label_ids(box: dict[str, Any]) -> set[str]:
    return {str(label.get("id")) for label in box.get("labels") or []}


def _list_query(
    box: dict[str, Any], params: dict[str, Any], size: int
) -> dict[str, Any]:
    query: dict[str, Any] = {"q": live_query(box, params.get("q")), "maxResults": size}
    for key in ("pageToken", "labelIds", "includeSpamTrash"):
        if params.get(key) not in (None, "", []):
            query[key] = params[key]
    return query


def _page_size(params: dict[str, Any]) -> int:
    return min(int(params.get("maxResults") or 100), 500)


def _live_page(
    reads: Reads, path: str, params: dict[str, Any], size: int
) -> dict[str, Any]:
    if set(_requested_labels(params)) & _own_label_ids(reads.box):
        return {}
    return reads.get(path, _list_query(reads.box, params, size))


def _known_date(box: dict[str, Any], message_id: str) -> int | None:
    local = _find(box, message_id)
    if local is not None:
        return int(local.get("internalDate") or 0)
    checked = box.get("checkedDates") or {}
    return int(checked[message_id]) if message_id in checked else None


def _newest_date(reads: Reads, kind: str, item_id: str) -> int | None:
    box = reads.box
    if kind == "messages":
        known = _known_date(box, item_id)
        if known is not None:
            return known
    payload = reads.get(f"{kind}/{_quoted(item_id)}", {"format": "minimal"})
    if HTTP_ERROR_KEY in payload:
        return None
    dated = payload.get("messages") if kind == "threads" else [payload]
    before = [
        int(m.get("internalDate") or 0) for m in dated or [] if _before_cutoff(box, m)
    ]
    newest = max(before) if before else _cutoff(box)
    if kind == "messages":
        box.setdefault("checkedDates", {})[item_id] = newest
    return newest


def _drop_after_cutoff(
    reads: Reads, kind: str, items: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    cutoff = _cutoff(reads.box)
    for index, item in enumerate(items):
        newest = _newest_date(reads, kind, str(item.get("id")))
        if newest is None or newest < cutoff:
            return items[index:]
    return []


def _live_page_before_cutoff(
    reads: Reads, kind: str, params: dict[str, Any], size: int
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    reply = _live_page(reads, kind, params, size)
    fetched = [] if HTTP_ERROR_KEY in reply else reply.get(kind) or []
    if params.get("pageToken") or HTTP_ERROR_KEY in reply:
        return reply, fetched, fetched
    live = _drop_after_cutoff(reads, kind, fetched)
    dropped = len(fetched) - len(live)
    if dropped == 0 or not reply.get("nextPageToken"):
        return reply, fetched, live
    fuller = _live_page(reads, kind, params, size + dropped)
    if HTTP_ERROR_KEY in fuller:
        return reply, fetched, live
    fuller_fetched = fuller.get(kind) or []
    return fuller, fuller_fetched, _drop_after_cutoff(reads, kind, fuller_fetched)


def _messages_list(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
    box = reads.box
    first_page = not params.get("pageToken")
    matched = _matching(box, params)
    local = matched if first_page else []
    reply, fetched, live = _live_page_before_cutoff(
        reads, "messages", params, max(1, _page_size(params) - len(local))
    )
    if HTTP_ERROR_KEY in reply:
        return reply
    query = parse_query(str(params.get("q") or ""))
    shown_first = {m["id"] for m in matched}
    kept: list[dict[str, Any]] = []
    for ref in live:
        message_id = str(ref.get("id"))
        if message_id in _imported(box):
            copied = _find(box, message_id)
            if copied is None or not _still_listed(box, copied, query, params):
                continue
            if not first_page and message_id in shown_first:
                continue
        kept.append({"id": message_id, "threadId": ref.get("threadId")})
    listed = {ref["id"] for ref in kept}
    added = [
        {"id": m["id"], "threadId": m.get("threadId")}
        for m in local
        if m["id"] not in listed
    ]
    estimate = int(reply.get("resultSizeEstimate") or 0) + len(added)
    result: dict[str, Any] = {
        "resultSizeEstimate": max(0, estimate - (len(fetched) - len(kept)))
    }
    if added or kept:
        result["messages"] = added + kept
    if reply.get("nextPageToken"):
        result["nextPageToken"] = reply["nextPageToken"]
    return result


def _thread_touched(box: dict[str, Any], thread_id: str) -> bool:
    return thread_id in _imported(box).values() or any(
        m.get("threadId") == thread_id for m in box["messages"]
    )


def _thread_still_listed(
    reads: Reads,
    thread_id: str,
    query: tuple[str, Any],
    params: dict[str, Any],
) -> bool:
    box = reads.box
    payload = reads.get(f"threads/{_quoted(thread_id)}", {"format": "minimal"})
    if HTTP_ERROR_KEY in payload:
        return True
    for message in payload.get("messages") or []:
        if not _before_cutoff(box, message):
            continue
        if str(message.get("id")) not in _imported(box):
            return True
        copied = _find(box, str(message.get("id")))
        if copied is not None and _still_listed(box, copied, query, params):
            return True
    return any(
        m.get("bitfabCreated") and m.get("threadId") == thread_id
        for m in _matching(box, params)
    )


def _thread_entry(box: dict[str, Any], thread_id: str) -> dict[str, Any]:
    messages = [m for m in box["messages"] if m.get("threadId") == thread_id]
    newest = max(messages, key=lambda m: int(m.get("internalDate") or 0))
    return {
        "id": thread_id,
        "snippet": newest.get("snippet") or "",
        "historyId": str(
            max(int(m.get("historyId") or 0) for m in messages) or box.get("historyId")
        ),
    }


def _threads_list(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
    box = reads.box
    first_page = not params.get("pageToken")
    local_threads = list(
        dict.fromkeys(
            str(m.get("threadId") or m["id"])
            for m in (_matching(box, params) if first_page else [])
        )
    )
    reply, fetched, live = _live_page_before_cutoff(
        reads, "threads", params, max(1, _page_size(params) - len(local_threads))
    )
    if HTTP_ERROR_KEY in reply:
        return reply
    query = parse_query(str(params.get("q") or ""))
    matched_locally = set(
        str(m.get("threadId") or m["id"]) for m in _matching(box, params)
    )
    kept = []
    for thread in live:
        thread_id = str(thread.get("id"))
        if not _thread_touched(box, thread_id):
            kept.append(thread)
            continue
        if not first_page and thread_id in matched_locally:
            continue
        if _thread_still_listed(reads, thread_id, query, params):
            kept.append(thread)
    listed = {str(thread.get("id")) for thread in kept}
    added = [_thread_entry(box, t) for t in local_threads if t not in listed]
    estimate = int(reply.get("resultSizeEstimate") or 0) + len(added)
    result: dict[str, Any] = {
        "resultSizeEstimate": max(0, estimate - (len(fetched) - len(kept)))
    }
    if added or kept:
        result["threads"] = added + kept
    if reply.get("nextPageToken"):
        result["nextPageToken"] = reply["nextPageToken"]
    return result


def _format_query(params: dict[str, Any]) -> dict[str, Any]:
    return {
        key: params[key]
        for key in ("format", "metadataHeaders")
        if params.get(key) not in (None, "", [])
    }


def _messages_get(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
    box = reads.box
    message_id = str(params.get("id"))
    local = _find(box, message_id)
    if local is not None and local.get("bitfabCreated"):
        return _get(box, params)
    if _gone(box, message_id):
        return _not_found(f"message {message_id}")
    payload = reads.get(f"messages/{_quoted(message_id)}", _format_query(params))
    if HTTP_ERROR_KEY in payload:
        return _get(box, params) if local is not None else payload
    if not _before_cutoff(box, payload):
        return _not_found(f"message {message_id}")
    return _overlay(box, payload) or _not_found(f"message {message_id}")


def _threads_get(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
    box = reads.box
    thread_id = str(params.get("id"))
    payload = reads.get(f"threads/{_quoted(thread_id)}", _format_query(params))
    failed = HTTP_ERROR_KEY in payload
    if failed and payload[HTTP_ERROR_KEY].get("code") != 404:
        return payload
    fmt = str(params.get("format") or "full").lower()
    headers = params.get("metadataHeaders")
    messages = [
        shown
        for message in ([] if failed else payload.get("messages") or [])
        if _before_cutoff(box, message)
        and (shown := _overlay(box, message)) is not None
    ]
    messages.extend(
        _shaped(m, fmt, [headers] if isinstance(headers, str) else headers)
        for m in box["messages"]
        if m.get("bitfabCreated") and m.get("threadId") == thread_id
    )
    if not messages:
        return _not_found(f"thread {thread_id}")
    messages.sort(key=lambda m: int(m.get("internalDate") or 0))
    thread = {} if failed else {k: v for k, v in payload.items() if k != "messages"}
    return {
        **thread,
        "id": thread_id,
        "historyId": str(max(int(m.get("historyId") or 0) for m in messages)),
        "messages": messages,
    }


def _attachments_get(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
    box = reads.box
    message_id = str(params.get("messageId"))
    local = _find(box, message_id)
    if local is not None and local.get("bitfabCreated"):
        return _attachment(box, params)
    if _gone(box, message_id):
        return _not_found(f"message {message_id}")
    if local is None:
        message = reads.get(f"messages/{_quoted(message_id)}", {"format": "minimal"})
        if HTTP_ERROR_KEY in message:
            return message
        if not _before_cutoff(box, message):
            return _not_found(f"message {message_id}")
    return reads.get(
        f"messages/{_quoted(message_id)}/attachments/{_quoted(params.get('id'))}"
    )


def _live_labels(reads: Reads) -> list[dict[str, Any]] | dict[str, Any]:
    payload = reads.get("labels")
    if HTTP_ERROR_KEY in payload:
        return payload
    return list(payload.get("labels") or [])


def _labels_list(reads: Reads, _params: dict[str, Any]) -> dict[str, Any]:
    live = _live_labels(reads)
    if isinstance(live, dict):
        return live
    known = {str(label.get("id")) for label in live}
    own = [label for label in reads.box.get("labels") or [] if label["id"] not in known]
    return {"labels": live + copy.deepcopy(own)}


def _labels_get(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
    wanted = str(params.get("id"))
    own = next((lb for lb in reads.box.get("labels") or [] if lb["id"] == wanted), None)
    if own is not None:
        return copy.deepcopy(own)
    return reads.get(f"labels/{_quoted(wanted)}")


def _labels_create(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
    live = _live_labels(reads)
    if isinstance(live, dict):
        return live
    name = str((params.get("body") or {}).get("name") or "").strip().lower()
    if name and any(str(label.get("name") or "").lower() == name for label in live):
        return _conflict("Label name exists or conflicts")
    return _label_create(reads.box, params)


def _deleted_count(box: dict[str, Any]) -> int:
    return sum(1 for message_id in _imported(box) if _find(box, message_id) is None)


def _profile(reads: Reads, _params: dict[str, Any]) -> dict[str, Any]:
    box = reads.box
    profile = box.get("profile") or {}
    created = [m for m in box["messages"] if m.get("bitfabCreated")]
    new_threads = len(
        {
            str(m.get("threadId"))
            for m in created
            if str(m.get("threadId")).startswith(SANDBOX_ID_PREFIX)
        }
    )
    _note(
        box,
        "getProfile reports the real mailbox's message and thread totals as they "
        "are now, so they can count mail that arrived after the original trace",
    )
    return {
        "emailAddress": profile.get("emailAddress") or box.get("emailAddress"),
        "messagesTotal": max(
            0,
            int(profile.get("messagesTotal") or 0) + len(created) - _deleted_count(box),
        ),
        "threadsTotal": int(profile.get("threadsTotal") or 0) + new_threads,
        "historyId": str(box.get("historyId") or 1000),
    }


def _send_as(reads: Reads, _params: dict[str, Any]) -> dict[str, Any]:
    return reads.get("settings/sendAs")


def _local_drafts(box: dict[str, Any], params: dict[str, Any]) -> list[dict[str, Any]]:
    query = parse_query(str(params.get("q") or ""))
    shown = []
    for draft in box["drafts"]:
        message = _find(box, str((draft.get("message") or {}).get("id")))
        if message is None or not _matches(box, message, query):
            continue
        hidden = set(message.get("labelIds") or []) & HIDDEN_LABELS
        if hidden and not _searches_hidden(params, query):
            continue
        shown.append(copy.deepcopy(draft))
    return shown


def _drafts_list(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
    box = reads.box
    first_page = not params.get("pageToken")
    local = _local_drafts(box, params) if first_page else []
    query: dict[str, Any] = {
        "q": live_query(box, params.get("q")),
        "maxResults": max(1, _page_size(params) - len(local)),
    }
    for key in ("pageToken", "includeSpamTrash"):
        if params.get(key) not in (None, ""):
            query[key] = params[key]
    reply = reads.get("drafts", query)
    if HTTP_ERROR_KEY in reply:
        return reply
    shadowed = {*_imported_drafts(box), *(str(d.get("id")) for d in box["drafts"])}
    live = reply.get("drafts") or []
    kept = [d for d in live if str(d.get("id")) not in shadowed]
    result: dict[str, Any] = {
        "resultSizeEstimate": max(
            0,
            int(reply.get("resultSizeEstimate") or 0)
            + len(local)
            - (len(live) - len(kept)),
        )
    }
    if local or kept:
        result["drafts"] = local + kept
    if reply.get("nextPageToken"):
        result["nextPageToken"] = reply["nextPageToken"]
    return result


def _drafts_get(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
    box = reads.box
    draft_id = params.get("id")
    if _find_draft(box, draft_id) is not None or str(draft_id) in _imported_drafts(box):
        return _draft_get(box, params)
    payload = reads.get(f"drafts/{_quoted(draft_id)}", _format_query(params))
    if HTTP_ERROR_KEY in payload:
        return payload
    message = payload.get("message") or {}
    if not _before_cutoff(box, message):
        return _not_found(f"draft {draft_id}")
    shown = _overlay(box, message)
    if shown is None:
        return _not_found(f"draft {draft_id}")
    return {**payload, "message": shown}


Handler = Callable[[Reads, dict[str, Any]], dict[str, Any]]
LocalHandler = Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]]


def _local(handler: LocalHandler) -> Handler:
    return lambda reads, params: handler(reads.box, params)


def _on_message(handler: LocalHandler) -> Handler:
    def run(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
        found = _import(reads, str(params.get("id")))
        if HTTP_ERROR_KEY in found:
            return found
        return handler(reads.box, params)

    return run


def _on_messages(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
    for message_id in (params.get("body") or {}).get("ids") or []:
        found = _import(reads, str(message_id))
        error = found.get(HTTP_ERROR_KEY)
        if error is not None and error.get("code") != 404:
            return found
    return _batch_modify(reads.box, params)


def _on_thread(handler: LocalHandler) -> Handler:
    def run(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
        failed = _import_thread(reads, str(params.get("id")))
        return failed if failed is not None else handler(reads.box, params)

    return run


def _on_draft(
    handler: LocalHandler, draft_id: Callable[[dict[str, Any]], Any]
) -> Handler:
    def run(reads: Reads, params: dict[str, Any]) -> dict[str, Any]:
        failed = _import_draft(reads, draft_id(params))
        return failed if failed is not None else handler(reads.box, params)

    return run


LIVE_HANDLERS: dict[str, Handler] = {
    "gmail.users.messages.list": _messages_list,
    "gmail.users.messages.get": _messages_get,
    "gmail.users.messages.attachments.get": _attachments_get,
    "gmail.users.messages.send": _local(_send),
    "gmail.users.messages.modify": _on_message(_modify),
    "gmail.users.messages.trash": _on_message(_trash),
    "gmail.users.messages.untrash": _on_message(_untrash),
    "gmail.users.messages.delete": _on_message(_delete),
    "gmail.users.messages.batchModify": _on_messages,
    "gmail.users.threads.list": _threads_list,
    "gmail.users.threads.get": _threads_get,
    "gmail.users.threads.modify": _on_thread(_thread_modify),
    "gmail.users.threads.trash": _on_thread(_thread_trash),
    "gmail.users.drafts.list": _drafts_list,
    "gmail.users.drafts.get": _drafts_get,
    "gmail.users.drafts.create": _local(_draft_create),
    "gmail.users.drafts.update": _on_draft(_draft_update, lambda p: p.get("id")),
    "gmail.users.drafts.delete": _on_draft(_draft_delete, lambda p: p.get("id")),
    "gmail.users.drafts.send": _on_draft(
        _draft_send, lambda p: (p.get("body") or {}).get("id")
    ),
    "gmail.users.history.list": _local(_history),
    "gmail.users.labels.list": _labels_list,
    "gmail.users.labels.get": _labels_get,
    "gmail.users.labels.create": _labels_create,
    "gmail.users.settings.sendAs.list": _send_as,
    PROFILE_METHOD: _profile,
}


def live_box(
    index: int,
    address: str,
    credential: str | None,
    details: dict[str, Any] | None,
    started_at: str | None,
) -> dict[str, Any]:
    return {
        "emailAddress": address,
        "credential": credential,
        "details": dict(details or {}),
        "clock": started_at,
        "cutoff": started_at,
        "historyId": 1000,
        "nextId": index * 1_000_000 + 1,
        "messages": [],
        "drafts": [],
        "searches": [],
        "labels": [],
        "sendAs": None,
        "history": [],
        "notes": [],
        "imported": {},
        "importedDrafts": [],
        "profile": None,
        "liveReads": [],
    }


def _recorded_accounts(ctx: SandboxStartCtx) -> list[dict[str, Any]]:
    found: list[dict[str, Any]] = []
    if ctx.recorded_state is not None:
        for box in as_mailboxes(ctx, ctx.recorded_state)["mailboxes"]:
            found.append(
                {
                    "emailAddress": box.get("emailAddress"),
                    "credential": box.get("credential"),
                    "details": box.get("details"),
                }
            )
    for span in ctx.recorded_spans(PROFILE_METHOD):
        output = span.output if isinstance(span.output, dict) else {}
        given = span.input if isinstance(span.input, dict) else {}
        if output.get("emailAddress"):
            found.append(
                {
                    "emailAddress": output["emailAddress"],
                    "credential": given.get(CREDENTIAL_PARAM),
                    "details": None,
                }
            )
    return found


def live_start(ctx: SandboxStartCtx, live: LiveGmail) -> dict[str, Any]:
    if _millis(ctx.trace_started_at) is None:
        raise GmailCutoffError(
            "The Gmail sandbox cannot read the real mailbox for this replay: "
            "the original trace's start time is not known, so mail that "
            "arrived after it cannot be hidden."
        )
    accounts = [
        *_recorded_accounts(ctx),
        *({"emailAddress": a, "credential": None} for a in live.addresses()),
    ]
    boxes: list[dict[str, Any]] = []
    for account in accounts:
        address = account.get("emailAddress")
        if not address:
            continue
        existing = next(
            (b for b in boxes if _same_address(b["emailAddress"], address)), None
        )
        if existing is None:
            boxes.append(
                live_box(
                    len(boxes),
                    str(address),
                    account.get("credential"),
                    account.get("details"),
                    ctx.trace_started_at,
                )
            )
            continue
        existing["credential"] = existing["credential"] or account.get("credential")
        existing["details"] = {**(account.get("details") or {}), **existing["details"]}
    return {
        "mode": READ_REAL_WRITE_FAKE,
        "traceStartedAt": ctx.trace_started_at,
        "mailboxes": boxes,
    }


def live_mailbox(
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
        if found is None:
            found = live_box(
                len(boxes), str(wanted), None, None, state.get("traceStartedAt")
            )
            boxes.append(found)
        return found
    credential = params.get(CREDENTIAL_PARAM)
    found = next(
        (b for b in boxes if credential and b.get("credential") == credential), None
    )
    if found is not None:
        return found
    if len(boxes) == 1:
        return boxes[0]
    known = ", ".join(str(b.get("emailAddress")) for b in boxes) or "none"
    raise GmailAccountError(
        f"The Gmail sandbox reads real mailboxes and cannot tell which account "
        f"this call is for (known accounts: {known}). Pass "
        "gmail_sandbox(account=...) to name the account from the call's "
        "credentials, call Gmail with userId set to the account's address, or "
        "give credentials for exactly one address."
    )


def _ready(reads: Reads) -> None:
    box = reads.box
    if box.get("profile") is not None:
        return
    address = str(box["emailAddress"])
    payload = reads.get("profile")
    if HTTP_ERROR_KEY in payload:
        error = payload[HTTP_ERROR_KEY]
        raise GmailReadError(
            f"The Gmail sandbox could not read {address}'s profile from Gmail "
            f"(HTTP {error.get('code')}: {error.get('message')})."
        )
    actual = payload.get("emailAddress")
    if actual and not _same_address(actual, address):
        raise GmailCredentialError(
            f"The Gmail credential given for {address} opens {actual}'s mailbox."
        )
    box["profile"] = {
        key: payload.get(key)
        for key in ("emailAddress", "messagesTotal", "threadsTotal", "historyId")
    }
    live_history = str(payload.get("historyId") or "")
    if live_history.isdigit():
        box["historyId"] = max(int(box.get("historyId") or 0), int(live_history))


LOUD_ERRORS = (
    GmailCredentialError,
    GmailReadError,
    GmailCutoffError,
    GmailAccountError,
)


def answer_live_gmail_call(
    state: dict[str, Any],
    call: MockOverrideCtx,
    account: Callable[[Any], str | None] | None,
    live: LiveGmail,
) -> Any:
    method = call.node.trace_function_key
    handler = LIVE_HANDLERS.get(method)
    if handler is None:
        raise NotImplementedError(
            f"The Gmail sandbox does not answer {method} in {READ_REAL_WRITE_FAKE} "
            f"mode yet, and never sends it to Google. It answers "
            f"{', '.join(sorted(LIVE_HANDLERS))}."
        )
    params = dict(call.kwargs)
    try:
        reads = Reads(live, live_mailbox(state, params, account), method)
        _ready(reads)
        return handler(reads, params)
    except LOUD_ERRORS as error:
        fail_replay_item(error)
        raise


def start_live(live: LiveGmail) -> Callable[[SandboxStartCtx], Any]:
    def start(ctx: SandboxStartCtx) -> Any:
        try:
            return live_start(ctx, live)
        except LOUD_ERRORS as error:
            fail_replay_item(error)
            raise

    return start
