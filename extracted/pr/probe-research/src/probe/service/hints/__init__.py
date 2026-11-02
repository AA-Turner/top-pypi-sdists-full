"""Hints: class HintLane composed of its tail, lookups and ledger, plus triggers and delivery.
Front door for the old `probe.service.hints`: names read live, a patch reaches every piece binding the name."""

from __future__ import annotations

from probe.foundation.front_door.front_door import serve_pieces

# Every piece loads here, in load order, as the old module ran whole on import (static, so the
# test gate's import graph sees this door use them).
import probe.service.hints.state as _piece_state  # noqa: F401
import probe.service.hints.triggers.window as _piece_window  # noqa: F401
import probe.service.hints.triggers.command as _piece_command  # noqa: F401
import probe.service.hints.triggers.peer as _piece_peer  # noqa: F401
import probe.service.hints.triggers.prompt as _piece_prompt  # noqa: F401
import probe.service.hints.triggers.search as _piece_search  # noqa: F401
import probe.service.hints.trigger as _piece_trigger  # noqa: F401
import probe.service.hints.request as _piece_request  # noqa: F401
import probe.service.hints.delivery as _piece_delivery  # noqa: F401
import probe.service.hints.tail as _piece_tail  # noqa: F401
import probe.service.hints.ledger as _piece_ledger  # noqa: F401
import probe.service.hints.lookups as _piece_lookups  # noqa: F401
import probe.service.hints.hints as _piece_hints  # noqa: F401

#: The old module's pieces, in load order: a write through the door reaches these only.
_PIECES = (
    "probe.service.hints.state",
    "probe.service.hints.triggers.window",
    "probe.service.hints.triggers.command",
    "probe.service.hints.triggers.peer",
    "probe.service.hints.triggers.prompt",
    "probe.service.hints.triggers.search",
    "probe.service.hints.trigger",
    "probe.service.hints.request",
    "probe.service.hints.delivery",
    "probe.service.hints.tail",
    "probe.service.hints.ledger",
    "probe.service.hints.lookups",
    "probe.service.hints.hints",
)

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    # probe.service.hints.state
    "BUCKET_BURST": "probe.service.hints.state",
    "Endpoint": "probe.service.hints.state",
    "Followed": "probe.service.hints.state",
    "HINTS_ENV": "probe.service.hints.state",
    "Lookup": "probe.service.hints.state",
    "Mode": "probe.service.hints.state",
    "OrderedDict": "probe.service.hints.state",
    "Skip": "probe.service.hints.state",
    "WINDOW_MAX_SEGMENTS": "probe.service.hints.state",
    "_Facts": "probe.service.hints.state",
    "_State": "probe.service.hints.state",
    "dataclass": "probe.service.hints.state",
    "deque": "probe.service.hints.state",
    "disabled": "probe.service.hints.state",
    "field": "probe.service.hints.state",
    "followed": "probe.service.hints.state",
    "threading": "probe.service.hints.state",
    # probe.service.hints.triggers.window
    "MAX_TEXT_CHARS": "probe.service.hints.triggers.window",
    "SCAN_MARGIN_CHARS": "probe.service.hints.triggers.window",
    "WINDOW_GAP_S": "probe.service.hints.triggers.window",
    "WINDOW_SEGMENT_CHARS": "probe.service.hints.triggers.window",
    "shows_mid_turn": "probe.service.hints.triggers.window",
    "window_due": "probe.service.hints.triggers.window",
    "window_segments": "probe.service.hints.triggers.window",
    "window_text": "probe.service.hints.triggers.window",
    # probe.service.hints.triggers.command
    "MAX_COMMAND_CHARS": "probe.service.hints.triggers.command",
    "_EXEC_OPENS": "probe.service.hints.triggers.command",
    "_EXEC_VALUES": "probe.service.hints.triggers.command",
    "_HELP": "probe.service.hints.triggers.command",
    "_HEREDOC": "probe.service.hints.triggers.command",
    "_QUOTED": "probe.service.hints.triggers.command",
    "_SHELL_OPERATORS": "probe.service.hints.triggers.command",
    "_WRAPPERS": "probe.service.hints.triggers.command",
    "_opens_with_exec": "probe.service.hints.triggers.command",
    "_probe_args": "probe.service.hints.triggers.command",
    "_segments": "probe.service.hints.triggers.command",
    "launches_run": "probe.service.hints.triggers.command",
    "os": "probe.service.hints.triggers.command",
    "re": "probe.service.hints.triggers.command",
    "shell_part": "probe.service.hints.triggers.command",
    "shlex": "probe.service.hints.triggers.command",
    # probe.service.hints.triggers.peer
    "Callable": "probe.service.hints.triggers.peer",
    "MAX_SENDERS": "probe.service.hints.triggers.peer",
    "MAX_SESSION_FILES": "probe.service.hints.triggers.peer",
    "MAX_SESSION_FILE_BYTES": "probe.service.hints.triggers.peer",
    "Path": "probe.service.hints.triggers.peer",
    "SENDER_KEEP_S": "probe.service.hints.triggers.peer",
    "SENDER_MISS_S": "probe.service.hints.triggers.peer",
    "Senders": "probe.service.hints.triggers.peer",
    "_ADDRESS": "probe.service.hints.triggers.peer",
    "_SESSION_ID": "probe.service.hints.triggers.peer",
    "_SOCKET_PID": "probe.service.hints.triggers.peer",
    "claude_sessions_dir": "probe.service.hints.triggers.peer",
    "sender_of": "probe.service.hints.triggers.peer",
    "time": "probe.service.hints.triggers.peer",
    # probe.service.hints.triggers.prompt
    "_NOT_PROMPTS": "probe.service.hints.triggers.prompt",
    # probe.service.hints.triggers.search
    "WEB_FETCH": "probe.service.hints.triggers.search",
    "WEB_SEARCH": "probe.service.hints.triggers.search",
    # probe.service.hints.trigger
    "MAIN_STREAM": "probe.service.hints.trigger",
    "Trigger": "probe.service.hints.trigger",
    "_ASKED_FIRST": "probe.service.hints.trigger",
    "trigger_of": "probe.service.hints.trigger",
    # probe.service.hints.request
    "Fetcher": "probe.service.hints.request",
    "HintFetcher": "probe.service.hints.request",
    "KEYS": "probe.service.hints.request",
    "ROUTE": "probe.service.hints.request",
    "TIMEOUT_S": "probe.service.hints.request",
    "WINDOW_TIMEOUT_S": "probe.service.hints.request",
    "_ENV_OVERRIDES": "probe.service.hints.request",
    "credentials": "probe.service.hints.request",
    "endpoint": "probe.service.hints.request",
    "json": "probe.service.hints.request",
    "names_trigger": "probe.service.hints.request",
    "scrubbed": "probe.service.hints.request",
    "urlsplit": "probe.service.hints.request",
    # probe.service.hints.delivery
    "CLAIM_LOG_TAIL_BYTES": "probe.service.hints.delivery",
    "DELIVERED_RECENTLY_S": "probe.service.hints.delivery",
    "DELIVERER_FRESH_DEFAULT_S": "probe.service.hints.delivery",
    "DELIVERER_FRESH_S": "probe.service.hints.delivery",
    "Deliverer": "probe.service.hints.delivery",
    "DeliveryState": "probe.service.hints.delivery",
    "LEDGER_TAIL_BYTES": "probe.service.hints.delivery",
    "LEDGER_WITHDRAWN": "probe.service.hints.delivery",
    "MISSED_AFTER_S": "probe.service.hints.delivery",
    "MISSED_TOOL_CALLS": "probe.service.hints.delivery",
    "MISSED_UNDELIVERABLE": "probe.service.hints.delivery",
    "SHOWN_AFTER_CLAIM_S": "probe.service.hints.delivery",
    "_DELIVERER_OF": "probe.service.hints.delivery",
    "_jsonl": "probe.service.hints.delivery",
    "_stamped": "probe.service.hints.delivery",
    "delivered_ids": "probe.service.hints.delivery",
    "delivery_facts": "probe.service.hints.delivery",
    "delivery_receipt": "probe.service.hints.delivery",
    "mailbox_ttl": "probe.service.hints.delivery",
    "post_message": "probe.service.hints.delivery",
    "record_keys": "probe.service.hints.delivery",
    "waiting_hints": "probe.service.hints.delivery",
    "withdraw_hints": "probe.service.hints.delivery",
    # probe.service.hints.tail
    "FRESH_S": "probe.service.hints.tail",
    "HINTS_LIVE_BEAT_S": "probe.service.hints.tail",
    "INITIAL_BACK_BYTES": "probe.service.hints.tail",
    "MAX_PENDING": "probe.service.hints.tail",
    "MAX_READ_BYTES": "probe.service.hints.tail",
    "RESOLVE_EVERY_S": "probe.service.hints.tail",
    "TailMixin": "probe.service.hints.tail",
    "UNDELIVERABLE_PROBE_S": "probe.service.hints.tail",
    "WINDOW_COVERS_S": "probe.service.hints.tail",
    "WINDOW_FAILURES_STOP": "probe.service.hints.tail",
    "WINDOW_READ_FRESH_S": "probe.service.hints.tail",
    "_Tail": "probe.service.hints.tail",
    "_epoch": "probe.service.hints.tail",
    "_safe": "probe.service.hints.tail",
    "_scopes": "probe.service.hints.tail",
    "contextlib": "probe.service.hints.tail",
    "datetime": "probe.service.hints.tail",
    "stat": "probe.service.hints.tail",
    # probe.service.hints.ledger
    "KEEP_LEDGER_S": "probe.service.hints.ledger",
    "LEDGER_DIR": "probe.service.hints.ledger",
    "LedgerMixin": "probe.service.hints.ledger",
    "MAX_EXCLUDE_DOC_IDS": "probe.service.hints.ledger",
    "SWEEP_EVERY_S": "probe.service.hints.ledger",
    "_SCOPE_NAMES": "probe.service.hints.ledger",
    "_number": "probe.service.hints.ledger",
    "_repeat_key": "probe.service.hints.ledger",
    "_window_scopes": "probe.service.hints.ledger",
    "exclude_doc_ids": "probe.service.hints.ledger",
    "hashlib": "probe.service.hints.ledger",
    "secrets": "probe.service.hints.ledger",
    # probe.service.hints.lookups
    "BUCKET_PER_MIN": "probe.service.hints.lookups",
    "LEGACY_EXCLUDE_DOC_IDS": "probe.service.hints.lookups",
    "LIMITED_S": "probe.service.hints.lookups",
    "LookupsMixin": "probe.service.hints.lookups",
    "MAX_HINT_CHARS": "probe.service.hints.lookups",
    "MISSING_S": "probe.service.hints.lookups",
    "OFF_RECHECK_S": "probe.service.hints.lookups",
    "REFUSED_S": "probe.service.hints.lookups",
    "REPEATS": "probe.service.hints.lookups",
    "SESSION_GAP_S": "probe.service.hints.lookups",
    "WINDOW_TOKEN_RESERVE": "probe.service.hints.lookups",
    # probe.service.hints.hints
    "Counter": "probe.service.hints.hints",
    "HintLane": "probe.service.hints.hints",
    "POLL_ENV": "probe.service.hints.hints",
    "POLL_S": "probe.service.hints.hints",
    "_poll_interval": "probe.service.hints.hints",
}

serve_pieces(__name__, _HOMES, pieces=_PIECES)
