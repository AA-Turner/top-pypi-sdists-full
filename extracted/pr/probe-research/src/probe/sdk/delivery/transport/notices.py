"""NoticeWatcher: a new `X-Probe-Notices` set is read off the caller's thread, each notice shown once per
computer on a terminal and posted once per session to the agent's mailbox (plan T7, R14, R17, R19)."""

from __future__ import annotations

import atexit
import os
import sys
import threading
import time
from collections.abc import Callable, Mapping
from typing import Any

from probe.foundation.server_messages import (
    MESSAGES_PATH,
    Audience,
    Destination,
    MessageLedger,
    MessageList,
    ServerMessage,
    Surface,
    make_message_key,
    parse_message_list,
    read_set_revision,
    render_server_message,
)

from probe.foundation.request_identity.request_identity import CLIENT_KIND_HEADER, CLIENT_VERSION_HEADER

from ...agent_session import session_id_from_env

#: Posts a notice to a coding-agent session's mailbox (`probe.shared.mailbox.post_server_message`). The CLI
#: sets it (`set_agent_poster`): the mailbox is a layer above the SDK, so a bare `import probe` has none.
AgentPoster = Callable[[str, ServerMessage], object]
#: The transport a list is read with, from the caller's.
ReaderFactory = Callable[[Any], Any]

#: The list read's own budget: one try, never the caller's.
FETCH_TIMEOUT_S = 5.0
#: After a failed read, the next changed header waits this long (the route may be down).
RETRY_AFTER_FAILURE_S = 60.0
#: A process ending while a read is in flight waits this long for it, at most, once.
EXIT_WAIT_S = 2.0
TEXT_PERSON = "Probe: {message}"
PERSON_AUDIENCES = frozenset({Audience.PERSON, Audience.BOTH})
AGENT_AUDIENCES = frozenset({Audience.AGENT, Audience.BOTH})


class NoticeWatcher:
    """One per process. `handle_answer` runs on every answer and costs a header lookup unless the set changed;
    the read and the showing run on a thread of their own, and nothing here ever raises."""

    def __init__(self, reader_factory: "ReaderFactory | None" = None) -> None:
        #: Builds the transport the list is read with (`make_reader`; a test hands its own).
        self.reader_factory: ReaderFactory = reader_factory or make_reader
        self._lock = threading.Lock()
        #: Output (stderr, a mailbox post) and the exit flag: once `wait_at_exit` returns, nothing starts.
        self._output_lock = threading.Lock()
        #: (ledger folder name, agent session or "") -> the set revision handled: a host serving several
        #: sessions reads for each one's agent.
        self._handled: dict[tuple[str, str], str] = {}
        self._failed_at: dict[str, float] = {}
        self._thread: threading.Thread | None = None
        self._is_closing = False
        self._has_exit_hook = False
        self._agent_poster: AgentPoster | None = None

    def set_agent_poster(self, poster: AgentPoster | None) -> None:
        self._agent_poster = poster

    def reset_after_fork(self) -> None:
        """A forked child starts with fresh locks and no read: one its parent's thread held at the fork
        would never be released there, and the child's next answer would wait on it forever."""
        self._lock = threading.Lock()
        self._output_lock = threading.Lock()
        self._thread = None

    def handle_answer(self, transport: Any, headers: Mapping[str, str]) -> None:
        """An answer of this process's own transport: start a read when its notice set is new here."""
        try:
            revision = read_set_revision(headers)
            token = getattr(transport.settings, "token", None) if revision else None
            if not token:
                return
            ledger = MessageLedger.from_account(transport.settings.base_url, token)
            account = ledger.folder.name
            # A terminal is the person's; a pipe in an agent session is the agent's (a person's own
            # command in a shell that inherited a session id tells the person, not that agent).
            should_tell_person = _is_terminal(sys.stderr)
            session_id = (session_id_from_env() or "") if self._agent_poster is not None and not should_tell_person else ""
            with self._lock:
                if self._is_closing or self._handled.get((account, session_id)) == revision:
                    return
                if self._thread is not None and self._thread.is_alive():
                    return  # a read is running (this answer may be its own)
                if time.monotonic() - self._failed_at.get(account, float("-inf")) < RETRY_AFTER_FAILURE_S:
                    return
                if not should_tell_person and not session_id:
                    self._handled[(account, session_id)] = revision  # nobody here to show it to
                    return
                thread = threading.Thread(
                    target=self._run, args=(transport, ledger, revision, session_id, should_tell_person),
                    name="probe-notices", daemon=True,
                )
                self._thread = thread
                if not self._has_exit_hook:
                    self._has_exit_hook = True
                    atexit.register(self.wait_at_exit)
            thread.start()
        except Exception:  # noqa: BLE001 -- advice may never fail the answer it rode on
            pass

    def wait(self, timeout: float) -> None:
        """Wait for a read in flight, at most `timeout` seconds."""
        thread = self._thread
        if thread is not None and thread.is_alive():
            thread.join(timeout)

    def wait_at_exit(self, timeout: float = EXIT_WAIT_S) -> None:
        """Give a read in flight a moment to show, then let nothing start (an interpreter shutting down
        must not meet a thread writing to stderr)."""
        self.wait(timeout)
        with self._output_lock:
            self._is_closing = True

    def _run(self, transport: Any, ledger: MessageLedger, revision: str, session_id: str, should_tell_person: bool) -> None:
        account = ledger.folder.name
        try:
            listed = _load_list(transport, ledger, revision, self.reader_factory)
            surface = _to_surface(transport.surface)
            for message in listed.messages:
                if should_tell_person and message.audience in PERSON_AUDIENCES:
                    self._show_person(ledger, message, surface)
                if session_id and message.audience in AGENT_AUDIENCES:
                    self._post_agent(ledger, message, session_id)
        except Exception:  # noqa: BLE001 -- not read: the next changed header tries again
            with self._lock:
                self._failed_at[account] = time.monotonic()
            return
        with self._lock:
            self._handled[(account, session_id)] = revision

    def _show_person(self, ledger: MessageLedger, message: ServerMessage, surface: Surface) -> None:
        claim = ledger.claim(make_message_key(str(message.message_id), message.revision), Destination.PERSON)
        if claim is None:
            return
        with self._output_lock:
            try:
                if self._is_closing:
                    raise RuntimeError("closing")
                sys.stderr.write(TEXT_PERSON.format(message=render_server_message(message, surface)) + "\n")
                sys.stderr.flush()
            except Exception:  # noqa: BLE001 -- not shown: another client shows it
                claim.release()
                return
        claim.commit()

    def _post_agent(self, ledger: MessageLedger, message: ServerMessage, session_id: str) -> None:
        poster = self._agent_poster
        if poster is None:
            return
        claim = ledger.claim(make_message_key(str(message.message_id), message.revision), Destination.AGENT, session_id)
        if claim is None:
            return
        with self._output_lock:
            try:
                if self._is_closing:
                    raise RuntimeError("closing")
                poster(session_id, message)
            except Exception:  # noqa: BLE001 -- not posted: SessionStart or a later answer tells it
                claim.release()
                return
        claim.commit()


def make_reader(transport: Any) -> Any:
    """A transport of the read's own, like the caller's (which it may close meanwhile): one try, a short budget."""
    return type(transport)(
        transport.settings, timeout=FETCH_TIMEOUT_S, max_retries=0,
        surface=transport.surface, client_headers=transport._client_headers,
    )


def _load_list(transport: Any, ledger: MessageLedger, revision: str, reader_factory: ReaderFactory) -> MessageList:
    """The set named `revision`: the account's saved copy when another client read it already, else one read."""
    kind = transport._client_headers.get(CLIENT_KIND_HEADER, "")
    saved = ledger.load_list(kind)
    if saved is not None and saved.set_revision == revision:
        return parse_message_list({"set_revision": saved.set_revision, "messages": saved.items})
    reader = reader_factory(transport)
    try:
        body = reader.get(MESSAGES_PATH)
    finally:
        reader.close()
    listed = parse_message_list(body)
    items = body.get("messages") if isinstance(body, dict) and isinstance(body.get("messages"), list) else []
    ledger.save_list(listed.set_revision, items, kind, client_version=transport._client_headers.get(CLIENT_VERSION_HEADER))
    return listed


def _to_surface(value: str) -> Surface:
    try:
        return Surface(value)
    except ValueError:
        return Surface.SDK


def _is_terminal(stream: Any) -> bool:
    """A person is likely reading it: services, daemons, MCP servers and an agent's shell are not terminals."""
    try:
        return bool(stream.isatty())
    except Exception:  # noqa: BLE001
        return False


NOTICE_WATCHER = NoticeWatcher()
if hasattr(os, "register_at_fork"):  # POSIX: training code forks (data loaders, multiprocessing)
    os.register_at_fork(after_in_child=NOTICE_WATCHER.reset_after_fork)
