"""Copilot model discovery over the Agent Client Protocol (ACP).

The Copilot CLI exposes an ACP responder on stdio (``copilot --acp``).  The
authoritative, entitlement-aware model inventory is the
``result.models.availableModels`` list returned by the ``session/new``
response — not a hardcoded list and not a catalogue endpoint.

Wire contract (verified against the ACP specification and a live
``copilot --acp`` transcript)::

    --> {"jsonrpc":"2.0","id":1,"method":"initialize",
         "params":{"protocolVersion":1,
                   "clientCapabilities":{"fs":{"readTextFile":true,
                                               "listDirectory":true},
                                         "terminal":false}}}
    <-- {"jsonrpc":"2.0","id":1,"result":{...}}
    --> {"jsonrpc":"2.0","id":2,"method":"session/new",
         "params":{"cwd":"<absolute cwd>","mcpServers":[]}}
    <-- {"jsonrpc":"2.0","id":2,"result":{"sessionId":"...",
         "models":{"availableModels":[{"modelId":"gpt-5-mini", ...,
             "_meta":{"copilotUsage":"0x", "copilotPriceCategory":"low",
                      "copilotEnablement":"enabled"}}]}}}

Reply ordering is enforced: the ``session/new`` request is written only after
the ``initialize`` reply carrying id ``1`` has been read and validated, and the
process is kept open until the authoritative id ``2`` response has been parsed
(or discovery is declared failed).  Intervening notifications and unrelated
messages are ignored.

Discovery failures are never fatal for callers.  :func:`discover_copilot_models`
implements the deterministic degradation chain:

1. live ACP discovery,
2. a valid cache within the TTL,
3. a stale cache retained after a failed refresh,
4. an empty inventory with a warning.

The cache lives at ``<user-config-dir>/agdt/caches/copilot-models.json``, is
written atomically, and expires after :data:`CACHE_TTL_SECONDS` seconds.
"""

from __future__ import annotations

import json
import math
import os
import queue
import shlex
import subprocess
import sys
import tempfile
import threading
import time
from collections.abc import Callable, Mapping, Sequence
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from .errors import ProviderError
from .models import ModelRecord
from .provider import ModelDiscovery
from .serialization import redact_credentials, thaw_json

__all__ = [
    "ACP_PROTOCOL_VERSION",
    "CACHE_TTL_SECONDS",
    "DEFAULT_CONTEXT_WINDOW",
    "DEFAULT_INITIALIZE_READ_TIMEOUT",
    "DEFAULT_OVERALL_TIMEOUT",
    "DEFAULT_SESSION_NEW_READ_TIMEOUT",
    "DEFAULT_SESSION_NEW_WRITE_TIMEOUT",
    "PROVIDER_NAME",
    "CopilotACPDiscovery",
    "discover_copilot_models",
    "extract_acp_pricing",
    "extract_available_models",
    "get_cache_path",
    "normalize_acp_model",
    "read_model_cache",
    "resolve_acp_command",
    "user_config_dir",
    "write_model_cache",
]

PROVIDER_NAME = "copilot"

ACP_PROTOCOL_VERSION = 1
_INITIALIZE_REQUEST_ID = 1
_SESSION_NEW_REQUEST_ID = 2

DEFAULT_INITIALIZE_READ_TIMEOUT = 10.0
DEFAULT_SESSION_NEW_WRITE_TIMEOUT = 5.0
DEFAULT_SESSION_NEW_READ_TIMEOUT = 10.0
DEFAULT_OVERALL_TIMEOUT = 30.0
_TERMINATE_TIMEOUT = 5.0

CACHE_TTL_SECONDS = 900
_CACHE_FILENAME = "copilot-models.json"
_CACHE_VERSION = 1

# ACP model entries do not advertise a context window.  Records therefore carry
# this placeholder until the metadata-normalization work supplies real values.
DEFAULT_CONTEXT_WINDOW = 128_000

_ACP_COMMAND_ENV_VAR = "AGDT_COPILOT_ACP_COMMAND"


def _reject_non_json_constant(value: str) -> None:
    """Reject ``NaN``/``Infinity`` tokens that Python's decoder accepts by default."""
    raise ValueError(f"Non-standard JSON constant {value!r} is not supported")


def _split_windows_command_line(command_line: str) -> list[str]:
    """Split a Windows command line into argv using CreateProcess-compatible rules."""
    args: list[str] = []
    length = len(command_line)
    index = 0
    while True:
        while index < length and command_line[index] in {" ", "\t"}:
            index += 1
        if index >= length:
            return args

        current: list[str] = []
        in_quotes = False
        while index < length:
            char = command_line[index]
            if char in {" ", "\t"} and not in_quotes:
                break
            if char == "\\":
                slash_start = index
                while index < length and command_line[index] == "\\":
                    index += 1
                slash_count = index - slash_start
                if index < length and command_line[index] == '"':
                    current.append("\\" * (slash_count // 2))
                    if slash_count % 2:
                        current.append('"')
                    else:
                        in_quotes = not in_quotes
                    index += 1
                    continue
                current.append("\\" * slash_count)
                continue
            if char == '"':
                if in_quotes and index + 1 < length and command_line[index + 1] == '"':
                    current.append('"')
                    index += 2
                    continue
                in_quotes = not in_quotes
                index += 1
                continue
            current.append(char)
            index += 1
        if in_quotes:
            raise ValueError("No closing quotation")
        args.append("".join(current))
        while index < length and command_line[index] in {" ", "\t"}:
            index += 1


def user_config_dir() -> Path:
    """Return the per-user configuration directory for the current platform."""
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA")
        if appdata:
            return Path(appdata)
        return Path.home() / "AppData" / "Roaming"
    xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
    if xdg_config_home:
        configured_path = Path(xdg_config_home).expanduser()
        if configured_path.is_absolute():
            return configured_path
    return Path.home() / ".config"


def get_cache_path() -> Path:
    """Return ``<user-config-dir>/agdt/caches/copilot-models.json``."""
    return user_config_dir() / "agdt" / "caches" / _CACHE_FILENAME


def resolve_acp_command() -> list[str] | None:
    """Resolve the argv used to spawn the Copilot ACP responder.

    The ``AGDT_COPILOT_ACP_COMMAND`` environment variable overrides the default
    ``<copilot binary> --acp`` invocation.  Returns ``None`` when no Copilot
    binary can be located.
    """
    override = os.environ.get(_ACP_COMMAND_ENV_VAR, "")
    try:
        parts = _split_windows_command_line(override) if os.name == "nt" else shlex.split(override)
    except ValueError as exc:
        raise ProviderError(
            f"AGDT_COPILOT_ACP_COMMAND could not be parsed: {exc}",
            category="validation_error",
        ) from exc
    if parts:
        return parts

    from agentic_devtools.cli.copilot.session import _get_copilot_binary  # noqa: PLC0415

    binary = _get_copilot_binary()
    if binary is None:
        return None
    return [binary, "--acp"]


def _positive_int_or_none(value: Any) -> int | None:
    """Return *value* when it is a positive, non-boolean integer."""
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        return None
    return value


def normalize_acp_model(
    entry: Any,
    *,
    source: str = "acp-live",
    observed_at: str | None = None,
) -> ModelRecord | None:
    """Normalize one ACP ``availableModels`` entry into a :class:`ModelRecord`.

    The complete ACP entry — including the ``_meta`` object carrying
    ``copilotUsage``, ``copilotPriceCategory`` and ``copilotEnablement`` — is
    preserved verbatim in ``raw_metadata``.  Returns ``None`` for entries that
    are not usable (non-mapping entries or entries without a ``modelId``).
    """
    if not isinstance(entry, Mapping):
        return None
    raw_model_id = entry.get("modelId")
    if not isinstance(raw_model_id, str) or not raw_model_id.strip():
        return None
    model_id = raw_model_id.strip()

    raw_name = entry.get("name")
    name = raw_name.strip() if isinstance(raw_name, str) and raw_name.strip() else model_id

    context_window = _positive_int_or_none(entry.get("contextWindow"))
    supports_tools = entry.get("supportsTools")

    return ModelRecord(
        name=name,
        model_id=model_id,
        provider=PROVIDER_NAME,
        context_window=context_window if context_window is not None else DEFAULT_CONTEXT_WINDOW,
        max_output_tokens=_positive_int_or_none(entry.get("maxOutputTokens")),
        supports_tools=supports_tools if isinstance(supports_tools, bool) else True,
        raw_metadata=dict(entry),
        raw_metadata_verbatim=True,
        source=source,
        observed_at=observed_at,
    )


_ACP_PRICING_FIELDS = (
    "inputRatePerM",
    "outputRatePerM",
    "currency",
    "rateUnit",
    "assumedInputTokens",
    "assumedOutputTokens",
    "costDataAsOf",
)

_CANONICAL_RATE_UNIT = "USD per 1M tokens"


def _acp_decimal(value: Any, field_name: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (Decimal, int, float, str)):
        raise ValueError(f"{field_name} must be numeric")
    try:
        result = value if isinstance(value, Decimal) else Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise ValueError(f"{field_name} must be a valid decimal") from exc
    if not result.is_finite() or result < 0:
        raise ValueError(f"{field_name} must be finite and non-negative")
    return result


def _acp_timestamp(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("costDataAsOf must be a timezone-aware ISO-8601 string")
    timestamp = value.strip()
    if timestamp.endswith("Z"):
        timestamp = timestamp[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(timestamp)
    except ValueError as exc:
        raise ValueError("costDataAsOf must be a timezone-aware ISO-8601 string") from exc
    if parsed.tzinfo is None:
        raise ValueError("costDataAsOf must be a timezone-aware ISO-8601 string")
    try:
        normalized = parsed.astimezone(UTC)
    except (OverflowError, OSError, ValueError) as exc:
        raise ValueError("costDataAsOf must be a timezone-aware ISO-8601 string") from exc
    if normalized > datetime.now(UTC):
        raise ValueError("costDataAsOf must not be in the future")
    return normalized.isoformat()


def extract_acp_pricing(record: Mapping[str, Any]) -> dict[str, Any] | None:
    """Extract explicit ACP monetary metadata without deriving rates.

    The model record is checked before its ``_meta`` mapping.  If either
    location contains any pricing field, that location must contain a complete
    valid payload; a category or usage value is never treated as a rate.
    ``None`` means no explicit monetary fields were supplied, while
    ``ValueError`` means a supplied payload was incomplete or malformed.
    """
    if not isinstance(record, Mapping):
        raise ValueError("ACP model record must be a mapping")
    locations: list[Mapping[str, Any]] = [record]
    metadata = record.get("_meta")
    if isinstance(metadata, Mapping):
        locations.append(metadata)
    for location in locations:
        supplied = {field for field in _ACP_PRICING_FIELDS if field in location}
        if not supplied:
            continue
        missing = set(_ACP_PRICING_FIELDS) - supplied
        if missing:
            raise ValueError(f"ACP pricing metadata is incomplete; missing {sorted(missing)}")
        currency = location["currency"]
        rate_unit = location["rateUnit"]
        if not isinstance(currency, str) or not currency.strip():
            raise ValueError("currency must be a non-empty string")
        if currency.strip() != "USD":
            raise ValueError(f"currency must be 'USD' for the canonical rate unit; got {currency.strip()!r}")
        if not isinstance(rate_unit, str) or not rate_unit.strip():
            raise ValueError("rateUnit must be a non-empty string")
        if rate_unit.strip() != _CANONICAL_RATE_UNIT:
            raise ValueError(
                f"rateUnit must be {_CANONICAL_RATE_UNIT!r}; got {rate_unit.strip()!r} — "
                "non-canonical units cannot be safely converted to per-million-token rates"
            )
        input_tokens = location["assumedInputTokens"]
        output_tokens = location["assumedOutputTokens"]
        if (
            isinstance(input_tokens, bool)
            or not isinstance(input_tokens, int)
            or input_tokens < 0
            or isinstance(output_tokens, bool)
            or not isinstance(output_tokens, int)
            or output_tokens < 0
        ):
            raise ValueError("token assumptions must be non-negative integers")
        return {
            "inputRatePerM": format(_acp_decimal(location["inputRatePerM"], "inputRatePerM"), "f"),
            "outputRatePerM": format(_acp_decimal(location["outputRatePerM"], "outputRatePerM"), "f"),
            "currency": currency.strip(),
            "rateUnit": rate_unit.strip(),
            "assumedInputTokens": input_tokens,
            "assumedOutputTokens": output_tokens,
            "costDataAsOf": _acp_timestamp(location["costDataAsOf"]),
        }
    return None


def _normalize_entries(
    entries: Sequence[Any],
    *,
    redact: bool = False,
    source: str = "acp-live",
    observed_at: str | None = None,
) -> list[ModelRecord]:
    """Normalize *entries*, dropping the ones that cannot be represented."""
    records = []
    for entry in entries:
        normalized_entry = redact_credentials(entry) if redact and isinstance(entry, Mapping) else entry
        record = normalize_acp_model(normalized_entry, source=source, observed_at=observed_at)
        if record is not None:
            records.append(record)
    return records


def extract_available_models(message: Mapping[str, Any]) -> list[Any]:
    """Return ``result.models.availableModels`` from a ``session/new`` response.

    Raises:
        ProviderError: when the authoritative model list is missing or empty.
    """
    result = message.get("result")
    if not isinstance(result, Mapping):
        raise ProviderError(
            "ACP session/new response has no result object.",
            category="provider_error",
        )
    models = result.get("models")
    if not isinstance(models, Mapping):
        raise ProviderError(
            "ACP session/new result has no models object.",
            category="provider_error",
        )
    available = models.get("availableModels")
    if not isinstance(available, list) or not available:
        raise ProviderError(
            "ACP session/new result has no availableModels list.",
            category="provider_error",
        )
    return available


def write_model_cache(
    records: Sequence[ModelRecord],
    *,
    cache_path: Path | None = None,
    now: float | None = None,
) -> bool:
    """Atomically write *records* to the model cache.

    Returns ``True`` on success and ``False`` when the cache could not be
    written; cache failures never abort discovery.
    """
    path = cache_path if cache_path is not None else get_cache_path()
    payload = {
        "version": _CACHE_VERSION,
        "fetchedAt": now if now is not None else time.time(),
        "models": [redact_credentials(thaw_json(record.raw_metadata)) for record in records],
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        handle, temp_name = tempfile.mkstemp(dir=str(path.parent), prefix=".copilot-models-", suffix=".tmp")
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as stream:
                json.dump(payload, stream, indent=2, sort_keys=True)
            os.replace(temp_name, path)
        except OSError:
            Path(temp_name).unlink(missing_ok=True)
            raise
    except OSError:
        return False
    return True


def read_model_cache(
    *,
    cache_path: Path | None = None,
    ttl_seconds: float = CACHE_TTL_SECONDS,
    allow_stale: bool = False,
    now: float | None = None,
) -> list[ModelRecord] | None:
    """Read cached model records.

    Returns ``None`` when the cache is missing, unreadable, malformed, empty,
    or older than *ttl_seconds* (unless *allow_stale* is ``True``).

    Raises:
        ValueError: If *ttl_seconds* is boolean, non-numeric, non-finite, or
            negative.
    """
    if (
        isinstance(ttl_seconds, bool)
        or not isinstance(ttl_seconds, (int, float))
        or not math.isfinite(ttl_seconds)
        or ttl_seconds < 0
    ):
        raise ValueError(f"ttl_seconds must be a finite non-negative number, got {ttl_seconds!r}")
    path = cache_path if cache_path is not None else get_cache_path()
    try:
        payload = json.loads(
            path.read_text(encoding="utf-8"),
            parse_constant=_reject_non_json_constant,
        )
    except (OSError, UnicodeDecodeError, ValueError):
        return None
    if not isinstance(payload, Mapping):
        return None
    version = payload.get("version")
    if isinstance(version, bool) or not isinstance(version, int) or version != _CACHE_VERSION:
        return None
    entries = payload.get("models")
    if not isinstance(entries, list):
        return None
    fetched_at = payload.get("fetchedAt")
    if isinstance(fetched_at, bool) or not isinstance(fetched_at, (int, float)) or not math.isfinite(fetched_at):
        return None
    age = (now if now is not None else time.time()) - float(fetched_at)
    if age < 0:
        return None
    if not allow_stale and age > ttl_seconds:
        return None
    try:
        observed_at = datetime.fromtimestamp(float(fetched_at), UTC).isoformat()
        return _normalize_entries(entries, redact=True, source="acp-cache", observed_at=observed_at) or None
    except (OSError, OverflowError, TypeError, ValueError):
        return None


class _MessageReader:
    """Reads newline-delimited JSON-RPC messages from a stream on a thread.

    Fragments are buffered, so a message split across several reads is
    reassembled before it is handed to the caller.
    """

    def __init__(self, stream: Any) -> None:
        self._stream = stream
        self._queue: queue.Queue[str | None] = queue.Queue()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def _run(self) -> None:
        buffer = ""
        while True:
            try:
                fragment = self._stream.readline()
            except (OSError, ValueError):
                break
            if not fragment:
                break
            buffer += fragment
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                if line.strip():
                    self._queue.put(line)
        if buffer.strip():
            self._queue.put(buffer)
        self._queue.put(None)

    def next_message(self, timeout: float) -> str | None:
        """Return the next raw message, or ``None`` when the stream ended.

        Raises:
            ProviderError: when no message arrives within *timeout* seconds.
        """
        try:
            return self._queue.get(timeout=timeout)
        except queue.Empty as exc:
            raise ProviderError(
                f"Timed out after {timeout:.1f}s waiting for an ACP message.",
                category="transport_error",
            ) from exc

    def stop(self) -> None:
        """Close the underlying stream and stop reading."""
        try:
            self._stream.close()
        except (OSError, ValueError):
            pass


def _time_budget(deadline: float, step_timeout: float) -> float:
    """Return the smaller of *step_timeout* and the time left until *deadline*.

    Raises:
        ProviderError: when the overall discovery budget is exhausted.
    """
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise ProviderError(
            "The overall ACP discovery timeout was exceeded.",
            category="transport_error",
        )
    return min(step_timeout, remaining)


def _write_message(process: Any, payload: Mapping[str, Any], timeout: float) -> None:
    """Write one JSON-RPC message to *process* stdin within *timeout* seconds."""
    data = json.dumps(payload, separators=(",", ":")) + "\n"
    failures: list[BaseException] = []

    def _write() -> None:
        try:
            process.stdin.write(data)
            process.stdin.flush()
        except (OSError, ValueError, AttributeError) as exc:
            failures.append(exc)

    worker = threading.Thread(target=_write, daemon=True)
    worker.start()
    worker.join(timeout)
    if worker.is_alive():
        raise ProviderError(
            f"Timed out after {timeout:.1f}s writing an ACP request.",
            category="transport_error",
        )
    if failures:
        raise ProviderError(
            f"Failed to write an ACP request: {failures[0]}",
            category="transport_error",
        )


def _terminate_process(process: Any, *, deadline: float | None = None) -> None:
    """Stop the ACP process and then close stdin, ignoring teardown failures.

    Terminating before closing stdin is intentional: if a daemon write-worker is
    blocked inside ``process.stdin.write()`` while holding the stream lock,
    closing stdin first would also block — preventing ``terminate()``/``kill()``
    from ever running and making the overall timeout ineffective.  Killing the
    child process unblocks any such stalled writer immediately, after which
    ``stdin.close()`` completes quickly.
    """
    try:
        if process.poll() is None:
            process.terminate()
            wait_timeout = _TERMINATE_TIMEOUT
            if deadline is not None:
                wait_timeout = min(wait_timeout, max(0.0, deadline - time.monotonic()))
            if wait_timeout > 0:
                process.wait(timeout=wait_timeout)
            elif process.poll() is None:
                process.kill()
                try:
                    process.wait(timeout=0.0)  # non-blocking reap; avoids zombies without extending the timeout budget
                except (OSError, ValueError, subprocess.TimeoutExpired):
                    pass
    except (OSError, ValueError, subprocess.TimeoutExpired):
        try:
            process.kill()
            try:
                process.wait(timeout=0.0)  # non-blocking reap; avoids zombies without extending the timeout budget
            except (OSError, ValueError, subprocess.TimeoutExpired):
                pass
        except (OSError, ValueError):
            pass
    try:
        process.stdin.close()
    except (OSError, ValueError, AttributeError):
        pass


def _spawn_acp_process(command: Sequence[str], cwd: str) -> Any:
    """Spawn the ACP responder with pipes wired for JSON-RPC over stdio."""
    try:
        return subprocess.Popen(
            list(command),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            cwd=cwd,
            text=True,
            encoding="utf-8",
            errors="strict",
            bufsize=1,
            shell=False,
        )
    except OSError as exc:
        raise ProviderError(
            f"Failed to spawn the Copilot ACP process: {exc}",
            category="transport_error",
        ) from exc


class CopilotACPDiscovery(ModelDiscovery):
    """Discovers Copilot models through an ACP stdio handshake."""

    def __init__(
        self,
        *,
        command: Sequence[str] | None = None,
        cwd: str | Path | None = None,
        initialize_read_timeout: float = DEFAULT_INITIALIZE_READ_TIMEOUT,
        session_new_write_timeout: float = DEFAULT_SESSION_NEW_WRITE_TIMEOUT,
        session_new_read_timeout: float = DEFAULT_SESSION_NEW_READ_TIMEOUT,
        overall_timeout: float = DEFAULT_OVERALL_TIMEOUT,
        spawn: Callable[[Sequence[str], str], Any] = _spawn_acp_process,
    ) -> None:
        self._command = list(command) if command is not None else None
        self._cwd = str(Path(cwd).resolve()) if cwd is not None else str(Path.cwd().resolve())
        for _name, _value in (
            ("initialize_read_timeout", initialize_read_timeout),
            ("session_new_write_timeout", session_new_write_timeout),
            ("session_new_read_timeout", session_new_read_timeout),
            ("overall_timeout", overall_timeout),
        ):
            if (
                isinstance(_value, bool)
                or not isinstance(_value, (int, float))
                or not math.isfinite(_value)
                or _value <= 0
            ):
                raise ValueError(f"{_name} must be a finite positive number, got {_value!r}")
        self._initialize_read_timeout = initialize_read_timeout
        self._session_new_write_timeout = session_new_write_timeout
        self._session_new_read_timeout = session_new_read_timeout
        self._overall_timeout = overall_timeout
        self._spawn = spawn

    def _initialize_request(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": _INITIALIZE_REQUEST_ID,
            "method": "initialize",
            "params": {
                "protocolVersion": ACP_PROTOCOL_VERSION,
                "clientCapabilities": {
                    "fs": {"readTextFile": True, "listDirectory": True},
                    "terminal": False,
                },
                "clientInfo": {"name": "agentic-devtools", "version": "1"},
            },
        }

    def _session_new_request(self) -> dict[str, Any]:
        return {
            "jsonrpc": "2.0",
            "id": _SESSION_NEW_REQUEST_ID,
            "method": "session/new",
            "params": {"cwd": self._cwd, "mcpServers": []},
        }

    def _validate_initialize_response(self, message: Mapping[str, Any]) -> None:
        """Validate ``initialize`` handshake fields before opening a session."""
        result = message.get("result")
        if not isinstance(result, Mapping):
            raise ProviderError(
                "ACP initialize response has no result object.",
                category="provider_error",
            )
        negotiated_protocol = result.get("protocolVersion")
        if isinstance(negotiated_protocol, bool) or not isinstance(negotiated_protocol, int):
            raise ProviderError(
                "ACP initialize response has an invalid protocolVersion.",
                category="provider_error",
            )
        if negotiated_protocol != ACP_PROTOCOL_VERSION:
            raise ProviderError(
                f"ACP initialize protocolVersion mismatch: expected {ACP_PROTOCOL_VERSION}, got {negotiated_protocol}.",
                category="provider_error",
            )

    def _read_response(
        self,
        reader: _MessageReader,
        expected_id: int,
        step_timeout: float,
        deadline: float,
    ) -> Mapping[str, Any]:
        """Read messages until the response carrying *expected_id* arrives."""
        step_deadline = min(deadline, time.monotonic() + step_timeout)
        while True:
            raw = reader.next_message(_time_budget(step_deadline, step_timeout))
            if raw is None:
                raise ProviderError(
                    f"The ACP stream ended before the response with id {expected_id} arrived.",
                    category="transport_error",
                )
            try:
                message = json.loads(raw, parse_constant=_reject_non_json_constant)
            except (json.JSONDecodeError, ValueError) as exc:
                raise ProviderError(
                    f"The ACP responder emitted malformed JSON: {exc}",
                    category="transport_error",
                ) from exc
            if not isinstance(message, Mapping):
                raise ProviderError(
                    "The ACP responder emitted a JSON message that is not an object.",
                    category="transport_error",
                )
            msg_id = message.get("id")
            if "method" in message or not isinstance(msg_id, int) or isinstance(msg_id, bool) or msg_id != expected_id:
                # Notifications, agent-initiated requests, replies to other
                # requests, and replies whose id is not a plain integer (Python
                # equality treats True==1 and 2.0==2, so the isinstance guards
                # are required for exact JSON-RPC id matching) are all skipped
                # while waiting for the authoritative response.
                continue
            if message.get("jsonrpc") != "2.0":
                raise ProviderError(
                    f"The ACP responder returned a non-JSON-RPC-2.0 response for id {expected_id}.",
                    category="transport_error",
                )
            if "error" in message:
                raise ProviderError(
                    f"The ACP responder returned a JSON-RPC error for id {expected_id}: {message['error']!r}",
                    category="provider_error",
                )
            return message

    def _discover_models(self) -> list[ModelRecord]:
        command = self._command if self._command is not None else resolve_acp_command()
        if command is None:
            raise ProviderError(
                "No Copilot binary is available for ACP model discovery.",
                category="transport_error",
            )

        deadline = time.monotonic() + self._overall_timeout
        process: Any | None = None
        reader: _MessageReader | None = None
        try:
            failures: list[BaseException] = []
            spawned: list[Any] = []
            cancelled = threading.Event()

            def _spawn() -> None:
                try:
                    result = self._spawn(command, self._cwd)
                    spawned.append(result)
                    # If the caller already timed out while we were spawning,
                    # terminate the process immediately to avoid leaving an
                    # orphaned ACP child.
                    if cancelled.is_set() and result is not None:
                        _terminate_process(result, deadline=time.monotonic() + _TERMINATE_TIMEOUT)
                except BaseException as exc:  # pragma: no cover - coverage.py does not trace daemon-thread execution
                    failures.append(exc)

            worker = threading.Thread(target=_spawn, daemon=True)
            worker.start()
            worker.join(_time_budget(deadline, self._overall_timeout))
            if worker.is_alive():
                cancelled.set()
                raise ProviderError(
                    f"Timed out after {self._overall_timeout:.1f}s spawning the Copilot ACP process.",
                    category="transport_error",
                )
            if failures:
                exc = failures[0]
                if isinstance(exc, ProviderError):
                    raise exc
                raise ProviderError(
                    f"Failed to spawn the Copilot ACP process: {exc}",
                    category="transport_error",
                ) from exc
            process = spawned[0]
            if process is None:
                raise ProviderError(
                    "Failed to spawn the Copilot ACP process: no process handle was returned.",
                    category="transport_error",
                )
            reader = _MessageReader(process.stdout)
            _write_message(
                process,
                self._initialize_request(),
                _time_budget(deadline, self._session_new_write_timeout),
            )
            # Reply ordering: session/new is written only after the initialize
            # reply with id 1 has been read and validated.
            initialize_reply = self._read_response(
                reader, _INITIALIZE_REQUEST_ID, self._initialize_read_timeout, deadline
            )
            self._validate_initialize_response(initialize_reply)
            _write_message(
                process,
                self._session_new_request(),
                _time_budget(deadline, self._session_new_write_timeout),
            )
            message = self._read_response(reader, _SESSION_NEW_REQUEST_ID, self._session_new_read_timeout, deadline)
            records = _normalize_entries(
                extract_available_models(message),
                source="acp-live",
                observed_at=datetime.now(UTC).isoformat(),
            )
            if not records:
                raise ProviderError(
                    "The ACP availableModels list contained no usable model entries.",
                    category="provider_error",
                )
            return records
        finally:
            if process is not None:
                _terminate_process(process, deadline=deadline)
            elif spawned and spawned[0] is not None:  # pragma: no cover
                # The spawn worker produced a process handle after the caller
                # timed out (narrow race between spawned.append and the
                # cancelled check in the worker).  Clean it up now.
                _terminate_process(spawned[0], deadline=time.monotonic() + _TERMINATE_TIMEOUT)
            if reader is not None:
                reader.stop()


def _default_warn(message: str) -> None:
    """Print a non-fatal discovery warning to stderr."""
    print(f"  ⚠ {message}", file=sys.stderr)


def discover_copilot_models(
    *,
    refresh: bool = True,
    allow_stale: bool = True,
    cache_path: Path | None = None,
    ttl_seconds: float = CACHE_TTL_SECONDS,
    discovery: ModelDiscovery | None = None,
    warn: Callable[[str], None] | None = None,
) -> list[ModelRecord]:
    """Return the Copilot model inventory, degrading gracefully when offline.

    The chain is: live ACP discovery (skipped when *refresh* is ``False``) →
    valid cache within the TTL → stale cache (when *allow_stale* is ``True``) →
    empty inventory.  This function never raises: an unreachable ACP responder
    yields a warning and whatever inventory is still available.
    """
    emit = warn if warn is not None else _default_warn
    path = cache_path if cache_path is not None else get_cache_path()

    if refresh:
        provider = discovery if discovery is not None else CopilotACPDiscovery()
        try:
            records = provider.discover_models()
        except ProviderError as exc:
            emit(f"Copilot ACP model discovery failed: {exc}")
        else:
            if not write_model_cache(records, cache_path=path):
                emit(f"Could not write the Copilot model cache at {path}")
            return records

    fresh = read_model_cache(cache_path=path, ttl_seconds=ttl_seconds)
    if fresh is not None:
        return fresh

    if allow_stale:
        stale = read_model_cache(cache_path=path, ttl_seconds=ttl_seconds, allow_stale=True)
        if stale is not None:
            emit(f"Using the stale Copilot model cache at {path}")
            return stale

    emit("No Copilot model inventory is available — continuing with an empty inventory.")
    return []
