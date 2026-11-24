"""Mandate-candidate taps — the host seam that lets a HOST observe real mandate runs.

A mandate *candidate* (common-docs/systems/intelligence/mandates/projects/mandate-candidates/REGISTER.md) re-runs a
real mandate run through a different Holder in the background. To do that the
host must see each real run: its input BEFORE the door mutates it, the ids it
ran under, the exact model-facing result of every tool call (so the candidate
can borrow them, P12), what the first provider call carried (the input digest,
P10), and how the run ended. matrx-ai never imports its host, so this module is
the seam, in three parts:

* :func:`tapped_door` — wraps one run DOOR (``run_mandated``, the Run Mandate
  workflow step, and the host's own doors). ``begin`` copies the input and must
  be synchronous and cheap; ``finish`` hands the outcome over and must be
  synchronous (the host schedules its own background work). No tap installed →
  the door runs untouched.
* :func:`observe_first_send` — called by ``send_once`` before the send boundary.
* :func:`observe_tool_results` — called by ``handle_tool_calls_v2`` after a
  batch, with the model-facing ``content`` dicts.

THE ONE RULE: a tap can never change, block, slow down or fail the run it
observes. Every host call here is wrapped; an exception is logged and
swallowed, and the run proceeds exactly as if no tap existed. The door's own
result and exception are passed through untouched.
"""

from __future__ import annotations

import json
import logging
import re
from collections.abc import Awaitable, Callable
from typing import Any, Protocol

logger = logging.getLogger(__name__)

class DoorTapHandle(Protocol):
    def finish(self, result: Any, error: BaseException | None) -> None: ...


class DoorTap(Protocol):
    def begin(
        self, door: str, mandate_key: str, snapshot: Callable[[], dict[str, Any]]
    ) -> DoorTapHandle | None: ...


class LiveRunObserver(Protocol):
    def first_send(self, request: Any, iteration: int | None) -> None: ...

    def tool_results(
        self,
        calls: list[dict[str, Any]],
        content_results: list[dict[str, Any]],
        full_results: list[Any],
    ) -> None: ...


#: The stable code of a test-mode refusal (a stand-in pass with nothing pinned overrides it with its own
#: ``no_stand_in``). Both are registered in ``providers/caller_refusal.py``.
MANDATE_REPLAY_REFUSED = "mandate_replay_refused"

MANDATE_REPLAY_REFUSED_USER_MESSAGE = (
    "Test mode refused this AI step: it has no saved answer to use here, and test mode never makes a real call."
)


class MandateReplayRefused(RuntimeError):
    """The host disallows test mode for this call. A real call must not follow.

    A CALLER REFUSAL (``providers/caller_refusal.py``): decided before anything was asked or bought, so a retry
    changes nothing and it is never an incident. Until 2026-11-16 it was unmarked, so every stand-in pass that
    reached an unpinned mandate inside a stream (ResearchSuggest) was filed as a ``stream_crash`` system_error
    while its own refused run row (code ``no_stand_in``) already named it. ``error_info`` carries the typed,
    non-retryable 409 the stream and HTTP layers answer with.
    """

    is_caller_refusal = True
    http_status = 409
    code = MANDATE_REPLAY_REFUSED

    @property
    def error_info(self) -> Any:
        from matrx_ai.providers.errors import RetryableError

        return RetryableError(
            error_type=str(getattr(self, "code", None) or MANDATE_REPLAY_REFUSED),
            message=str(self),
            status_code=self.http_status,
            is_retryable=False,
            user_message=MANDATE_REPLAY_REFUSED_USER_MESSAGE,
            details={"caller_refusal": True, "mandate_key": getattr(self, "mandate_key", None)},
        )


class MandateReplay(Protocol):
    """The host's TEST-MODE answer source for a mandate step (aidream: ``services/runtime/ai_test_mode.py``).

    Unlike a tap, this one CAN answer instead of the real run — so it is the opposite of silent: the
    host decides everything (who, when, which mode), and an answer it returns must carry its own loud
    ``ai_test_replay`` stamp. ``lookup`` returns an ``AiExecutionResult``-shaped dict or None (= run
    for real); ``store`` is offered the real result afterwards. Not installed (every package test,
    every host that never opts in) → both are skipped and the step is exactly the real one.
    """

    async def lookup(
        self, door: str, mandate_key: str, run_id: str | None, fingerprint: dict[str, Any]
    ) -> dict[str, Any] | None: ...

    async def store(
        self, door: str, mandate_key: str, run_id: str | None, fingerprint: dict[str, Any],
        result: dict[str, Any],
    ) -> None: ...

    # Optional: ``async def active(self, run_id) -> bool`` — whether this call may be answered or recorded at
    # all (a replay session, or AI test mode). Asked BEFORE any key is built, so a real call never builds one.


_DOOR_TAP: DoorTap | None = None
_OBSERVER: LiveRunObserver | None = None
_REPLAY: MandateReplay | None = None


def set_mandate_replay(replay: MandateReplay | None) -> None:
    """Install (or clear) the host's test-mode answer source. Called once at host startup."""
    global _REPLAY
    _REPLAY = replay


async def replay_lookup(
    door: str, mandate_key: str, run_id: str | None, fingerprint: dict[str, Any]
) -> dict[str, Any] | None:
    """Return the host's test-mode answer or None. An explicit host refusal stops the call."""
    replay = _REPLAY
    if replay is None:
        return None
    try:
        return await replay.lookup(door, mandate_key, run_id, fingerprint)
    except MandateReplayRefused:
        raise
    except Exception:  # noqa: BLE001 — a broken test seam is a miss, never a failed run
        logger.exception("[mandate replay] lookup failed for %s %s — the real run follows", door, mandate_key)
        return None


async def replay_store(
    door: str, mandate_key: str, run_id: str | None, fingerprint: dict[str, Any], result: dict[str, Any]
) -> None:
    replay = _REPLAY
    if replay is None:
        return
    try:
        await replay.store(door, mandate_key, run_id, fingerprint, result)
    except Exception:  # noqa: BLE001 — the real result is already in hand; never lose it
        logger.exception("[mandate replay] store failed for %s %s — result not saved", door, mandate_key)


#: THE ONE replay door (L-REPLAY, 2026-11-10). A mandate's answer is keyed on WHAT ran, never on which door
#: started it: the code path (the host runner's NamedAgent lane) and the Run Mandate workflow step build the
#: same fingerprint, so one side records and the other side replays. A second door key is a second home.
MANDATE_DOOR = "mandate"


#: The key's own version. Raising it retires every recorded answer on purpose (an answer recorded under a
#: narrower key must never be served to a wider one); it is part of the fingerprint, so nothing else changes.
FINGERPRINT_VERSION = 2


def _plain(value: Any) -> Any:
    """``value`` as order-free plain data: models dumped, mapping keys sorted, and nothing-values (None, "", [],
    {}) dropped, so a setting left out and a setting left empty are the same request."""
    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json", exclude_none=True)
    if isinstance(value, dict):
        out = {str(k): _plain(v) for k, v in sorted(value.items(), key=lambda kv: str(kv[0]))}
        return {k: v for k, v in out.items() if v not in (None, "", [], {})}
    if isinstance(value, (list, tuple)):
        return [_plain(v) for v in value]
    if isinstance(value, (set, frozenset)):
        return sorted((_plain(v) for v in value), key=repr)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return repr(value)


def _plain_overrides(value: Any) -> dict[str, Any]:
    """The model settings AFTER every override, in one spelling: a dict and an ``LLMParams`` holding the same
    settings are the same key (aliases folded by ``LLMParams`` itself); a dict it cannot read is kept as written."""
    if not value:
        return {}
    if isinstance(value, dict):
        from matrx_ai.config.llm_params import LLMParams

        try:
            value = LLMParams.model_validate(dict(value))
        except Exception:  # noqa: BLE001 — an unreadable override still keys on what was written
            pass
    plain = _plain(value)
    return plain if isinstance(plain, dict) else {"value": plain}


def answer_fingerprint(
    *,
    agent_id: str | None,
    is_version: bool,
    variables: dict[str, Any] | None,
    user_input: Any = None,
    config_overrides: Any = None,
    request: dict[str, Any] | None = None,
    holder_type: str = "agent",
) -> dict[str, Any]:
    """THE ONE KEY of a mandate answer, built from the FULLY RESOLVED request — any difference is a miss:

    * the Holder: ``holder_type``, ``agent_id`` (a workflow Holder's definition id) and ``is_version``;
    * ``variables`` — what the Holder runs on AFTER binding and every edge-fed value, coerced exactly as the
      template engine sees them (``to_template_value``: a dict and its JSON text are the same input); the
      order the variables are named in never matters, the text of each value does;
    * ``user_input`` — the turn as sent: the person's text, or its content blocks WITH attached media;
    * ``config_overrides`` — the model and settings after EVERY layer (binding, call site, step, run);
    * ``request`` — everything else on the request that can change the answer, by name (host turn, tools,
      a continued conversation, context...). The caller passes only what is set; nothing-values are dropped.

    No call counter and no order: two calls collide only when all of this is equal, and then they are the same
    question, whichever came first."""
    from matrx_ai.agents.named import to_template_value

    bound = {str(k): to_template_value(v) for k, v in sorted(dict(variables or {}).items(), key=lambda kv: str(kv[0]))}
    request = {k: v for k, v in dict(request or {}).items() if k not in _NEVER_THE_QUESTION}
    turn: Any = user_input if isinstance(user_input, str) else _plain(user_input)
    return {"v": FINGERPRINT_VERSION, "holder_type": holder_type, "agent_id": str(agent_id or ""),
            "is_version": bool(is_version), "variables": bound, "user_input": turn or "",
            "config_overrides": _plain_overrides(config_overrides), "request": _plain(dict(request or {}))}


#: Request fields that never reach the model, on EITHER door, dropped from every key in one place (research parity
#: 2026-11-10: every PBW analyze call keyed apart on these alone, variables and settings byte-equal):
#: * ``source_app`` / ``source_feature`` — attribution labels (the conversation's lane, the usage row). Each door
#:   writes its own ("workflow-studio" / "mandate:<key>" on a step; the NamedAgent lane its label), the prompt never
#:   carries them, and a run they refuse (an admission check) fails and is never recorded.
#: * ``allow_client_delegation`` — WHERE a tool runs (server, or a round trip to a client), never which question is
#:   asked. The code lane named it and the workflow request has no such field, so it could only ever split the doors.
_NEVER_THE_QUESTION = frozenset({"source_app", "source_feature", "allow_client_delegation"})


#: Fields of a host agent request that never change the answer (ids minted per run, transport and storage
#: switches, the organization — already part of the host's key) or that the key names itself.
_REQUEST_NOT_KEYED = frozenset({
    "variables", "user_input", "config_overrides", "is_version", "organization_id", "is_new", "store", "stream",
    "debug", "retry",
    # A ceiling on tool rounds, resolved per step from the platform's knobs: a run that hits it fails, and a
    # failed run is never recorded, so it cannot change a recorded answer (the code path has no such field).
    "max_iterations",
})


def request_fingerprint(request: Any, *, drop_overrides: tuple[str, ...] = ()) -> dict[str, Any]:
    """The key parts a fully built host agent request holds (a workflow AI step's ``AgentStartRequest``):
    ``variables``, ``user_input``, ``config_overrides`` and, under ``request``, every other field that is not
    at its default. A conversation the step itself just opened is not a difference; a continued one is.
    ``drop_overrides`` names settings that are the node type's own fixed contract, never a per-call choice."""
    if hasattr(request, "model_dump"):
        dumped = request.model_dump(mode="json", exclude_none=True, exclude_defaults=True)
    else:
        dumped = dict(request) if isinstance(request, dict) else dict(vars(request))
    read = request.get if isinstance(request, dict) else (lambda name: getattr(request, name, None))
    if read("is_new") is not False:
        dumped.pop("conversation_id", None)
    overrides = _plain_overrides(read("config_overrides"))
    # A private attribute (``_name``) is never on the wire a model_dump shows; a plain object's vars match that.
    keyed = {k: v for k, v in dumped.items() if k not in _REQUEST_NOT_KEYED and not str(k).startswith("_")}
    # The step's private opt-out of the ~5k-token org-catalog intro (``_include_org_catalog``) is NOT keyed: an
    # explicit false equals absent (Arman, 2026-11-13, research parity). Every mandate door sends no catalog
    # (``org_catalog_intro_wanted``: a mandate contract closes context), the code lane never names the switch,
    # so keying the step's explicit opt-out split the two doors on a field that changes nothing sent.
    return {"variables": dict(read("variables") or {}), "user_input": read("user_input"),
            "config_overrides": {k: v for k, v in overrides.items() if k not in drop_overrides},
            "request": keyed}


#: A row id as it appears in a request (any uuid spelling, any case).
ROW_ID_RE = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
#: The parts of a key that carry the QUESTION's data. The Holder (``agent_id``) and the settings are never mapped:
#: a different doer is a different question whatever its id spells.
_ROW_ID_PARTS = ("variables", "user_input", "request")


def _stable_marker(stable_key: str) -> str:
    return f"⟦{stable_key}⟧"


def _swap_in_json(value: Any, swap: Callable[[str], str]) -> Any:
    text = json.dumps(value, ensure_ascii=False, default=str)
    return json.loads(swap(text))


def row_ids_in(fingerprint: dict[str, Any]) -> set[str]:
    """Every row id the question carries (lowercase), in the parts :func:`with_stable_row_ids` maps."""
    text = json.dumps({k: fingerprint.get(k) for k in _ROW_ID_PARTS}, ensure_ascii=False, default=str)
    return {m.group(0).lower() for m in ROW_ID_RE.finditer(text)}


def with_stable_row_ids(fingerprint: dict[str, Any], stable: dict[str, str]) -> dict[str, Any]:
    """``fingerprint`` with every row id the host could name replaced by its stable key (``⟦source:<url>⟧``).

    Two copies of the same data (a side-by-side pair) hold equal content under different row ids, so a request that
    names a row never keyed equal across copies (research parity f437415a: the authority judge's ``sources``). The
    host passes ``stable``: row id -> a key that is the SAME for the same row on every copy and DIFFERENT for
    different rows. An id the host could not name stays as written, so it still differs — a real difference is never
    hidden. Only the question's data is mapped (:data:`_ROW_ID_PARTS`), never the Holder or the settings."""
    if not stable:
        return fingerprint
    table = {k.lower(): v for k, v in stable.items()}

    def swap(text: str) -> str:
        return ROW_ID_RE.sub(lambda m: (json.dumps(_stable_marker(table[m.group(0).lower()]), ensure_ascii=False)[1:-1]
                                        if m.group(0).lower() in table else m.group(0)), text)

    out = dict(fingerprint)
    for part in _ROW_ID_PARTS:
        if part in out and out[part] not in (None, "", {}, []):
            out[part] = _swap_in_json(out[part], swap)
    return out


def answer_with_stable_row_ids(answer: dict[str, Any], stable: dict[str, str]) -> dict[str, Any]:
    """A recorded answer with the recording copy's row ids replaced by stable keys (the same keys its request used)."""
    if not stable:
        return answer
    table = {k.lower(): v for k, v in stable.items()}
    return _swap_in_json(answer, lambda text: ROW_ID_RE.sub(
        lambda m: (json.dumps(_stable_marker(table[m.group(0).lower()]), ensure_ascii=False)[1:-1]
                   if m.group(0).lower() in table else m.group(0)), text))


def answer_with_copy_row_ids(answer: dict[str, Any], stable: dict[str, str]) -> dict[str, Any]:
    """A served answer with every stable key put back as THIS copy's row id (``stable``: this copy's id -> key), so
    the copy that replays writes its own rows, never the recording copy's."""
    if not stable:
        return answer
    back = {json.dumps(_stable_marker(v), ensure_ascii=False)[1:-1]: k for k, v in stable.items()}
    if not back:
        return answer
    pattern = re.compile("|".join(re.escape(m) for m in sorted(back, key=len, reverse=True)))
    return _swap_in_json(answer, lambda text: pattern.sub(lambda m: back[m.group(0)], text))


class ReplayKey:
    """A replay key built only when the host says this call may be replayed or recorded, at most once.

    A REAL call never builds it: the key reads the whole request, and a test seam must never fail a real run.
    A key that cannot be built is logged loudly and the call runs for real, unrecorded."""

    def __init__(self, build: Callable[[], dict[str, Any]], *, label: str = "") -> None:
        self._build = build
        self._label = label
        self._built = False
        self._value: dict[str, Any] | None = None

    def get(self) -> dict[str, Any] | None:
        if not self._built:
            self._built = True
            try:
                self._value = self._build()
            except Exception:  # noqa: BLE001 — a broken key is a miss, never a failed run
                logger.exception("🚨 [mandate replay] the replay key for %s could not be built — the REAL call "
                                 "runs and is not recorded", self._label or "this call")
                self._value = None
        return self._value


Fingerprint = dict[str, Any] | ReplayKey | Callable[[], dict[str, Any]]


def _key_of(fingerprint: Fingerprint, label: str) -> dict[str, Any] | None:
    if isinstance(fingerprint, dict):
        return fingerprint
    if isinstance(fingerprint, ReplayKey):
        return fingerprint.get()
    return ReplayKey(fingerprint, label=label).get()


async def _replay_active(replay: MandateReplay, run_id: str | None) -> bool:
    """Whether the host may answer or record this call at all; a host without ``active`` decides in ``lookup``.
    A broken check is "no" — the real call follows."""
    active = getattr(replay, "active", None)
    if active is None:
        return True
    try:
        return bool(await active(run_id))
    except Exception:  # noqa: BLE001 — a broken test seam is a real call, never a failed run
        logger.exception("[mandate replay] the test-mode check failed — the real call follows")
        return False


async def replay_may_answer(run_id: str | None) -> bool:
    """Whether the host may answer or record a mandate call for this run (a replay session or AI test mode). A call
    site that needs an async read to build its key asks this first, so a REAL call never pays for it."""
    replay = _REPLAY
    return replay is not None and await _replay_active(replay, run_id)


async def replay_answer(mandate_key: str, run_id: str | None, fingerprint: Fingerprint) -> dict[str, Any] | None:
    """The recorded ``AiExecutionResult``-shaped answer for this exact mandate run, or None (run for real).
    Pass a :class:`ReplayKey` (or a callable): the key is built only when the host is replaying."""
    replay = _REPLAY
    if replay is None or not await _replay_active(replay, run_id):
        return None
    key = _key_of(fingerprint, mandate_key)
    if key is None:
        return None
    return await replay_lookup(MANDATE_DOOR, mandate_key, run_id, key)


async def record_answer(mandate_key: str, run_id: str | None, fingerprint: Fingerprint, result: dict[str, Any]) -> None:
    replay = _REPLAY
    if replay is None or not await _replay_active(replay, run_id):
        return
    key = _key_of(fingerprint, mandate_key)
    if key is None:
        return
    await replay_store(MANDATE_DOOR, mandate_key, run_id, key, result)


def answer_from_agent_run(result: Any, *, agent_id: str | None = None) -> dict[str, Any] | None:
    """A code-path ``AgentRunResult`` in the one stored shape (``AiExecutionResult``) — the WHOLE answer: text,
    parsed value, the doer (``metadata.agent_id``), the model (``metadata.model_id``), the usage in both shapes
    (``usage`` by model name, ``metadata.code_usage`` as the code stores it). None when it failed."""
    if not getattr(result, "success", False):
        return None
    from matrx_ai.graph_nodes.shared import _extract_usage

    parsed = getattr(result, "parsed", None)
    if parsed is not None and hasattr(parsed, "model_dump"):
        parsed = parsed.model_dump(mode="json")
    if parsed is not None and not isinstance(parsed, (dict, list)):
        parsed = None
    try:
        usage = _extract_usage(getattr(result, "usage_aggregated", None)).model_dump(mode="json")
    except Exception:  # noqa: BLE001 — an unreadable usage object is recorded as none, never a lost answer
        usage = {}
    meta = {**dict(getattr(result, "metadata", None) or {}), "agent_id": agent_id,
            "model_id": getattr(result, "model_id", None), "code_usage": dict(getattr(result, "usage", None) or {})}
    return {"conversation_id": "", "request_id": "", "iterations": 1,
            "final_text": str(getattr(result, "output", "") or ""), "structured_output": parsed,
            "usage": usage, "metadata": {k: v for k, v in meta.items() if v is not None}}


def agent_run_from_answer(answer: dict[str, Any], output_cls: Any = None) -> Any:
    """A stored answer as the code path's ``AgentRunResult``, rebuilt EXACTLY as the live run built it: the same
    text, model and usage, and ``parsed`` set the way the executor sets it — a decision turn's ``decision_answers``
    part as the plain part (``executor.run_agent``: "a decision turn's answer is a typed part"), a declared
    response model (``output_cls``, a real ``BaseModel`` subclass) validated into that class, anything else the
    recorded value as is. ``parsed`` is ASSIGNED after construction, as the executor does: passed to the
    constructor, the unparametrized ``AgentRunResult[ParsedT]`` coerces a dict into bare ``BaseModel``
    ("BaseModel cannot be instantiated directly", L-REPLAY3). The replay's stamp rides ``metadata``."""
    from pydantic import BaseModel

    from matrx_ai.agents.executor import AgentRunResult

    structured = answer.get("structured_output")
    parsed: Any = structured
    parse_error = None
    decision_part = isinstance(structured, dict) and structured.get("__kind") == "decision_answers"
    declared = isinstance(output_cls, type) and issubclass(output_cls, BaseModel) and output_cls is not BaseModel
    if structured is not None and declared and not decision_part:
        try:
            parsed = output_cls.model_validate(structured)
        except (ValueError, TypeError) as exc:
            parsed, parse_error = None, str(exc)[:500]
    meta = dict(answer.get("metadata") or {})
    if answer.get("finish_reason") and not meta.get("finish_reason"):
        # The stored shape says HOW the answer ended at its top level (``AiExecutionResult.finish_reason``); the code
        # path reads it from ``metadata`` (``run_history``). Dropping it made a served refusal read as a clean answer
        # that failed its contract (live 2026-11-16: research.structured_page_summary drift rows).
        meta["finish_reason"] = answer["finish_reason"]
    usage = meta.get("code_usage") or dict(answer.get("usage") or {})
    result = AgentRunResult(success=True, output=str(answer.get("final_text") or ""),
                            parse_error=parse_error, error_kind="parse" if parse_error else None,
                            model_id=meta.get("model_id"), usage=dict(usage), metadata=meta)
    result.parsed = parsed
    if decision_part:
        result.metadata.setdefault("output_kind", "decision_answers")
    return result


def set_mandate_door_tap(tap: DoorTap | None) -> None:
    """Install (or clear) the host's door tap. Called once at host startup."""
    global _DOOR_TAP
    _DOOR_TAP = tap


def get_mandate_door_tap() -> DoorTap | None:
    return _DOOR_TAP


def set_live_run_observer(observer: LiveRunObserver | None) -> None:
    """Install (or clear) the host's send / tool-result observer."""
    global _OBSERVER
    _OBSERVER = observer


def get_live_run_observer() -> LiveRunObserver | None:
    return _OBSERVER


async def tapped_door[T](
    door: str,
    mandate_key: str,
    snapshot: Callable[[], dict[str, Any]],
    run: Callable[[], Awaitable[T]],
) -> T:
    """Run ``run()`` as one observed mandate door. Never alters the run."""
    tap = _DOOR_TAP
    if tap is None:
        return await run()
    handle: DoorTapHandle | None = None
    try:
        handle = tap.begin(door, mandate_key, snapshot)
    except Exception:  # noqa: BLE001 — a tap never touches the run
        logger.exception("[mandate taps] begin failed for %s %s — the run is untouched", door, mandate_key)
        handle = None
    if handle is None:
        return await run()
    try:
        result = await run()
    except BaseException as exc:
        _finish(handle, None, exc, door, mandate_key)
        raise
    _finish(handle, result, None, door, mandate_key)
    return result


def _finish(
    handle: DoorTapHandle, result: Any, error: BaseException | None, door: str, mandate_key: str
) -> None:
    try:
        handle.finish(result, error)
    except Exception:  # noqa: BLE001 — a tap never touches the run
        logger.exception("[mandate taps] finish failed for %s %s — the run is untouched", door, mandate_key)


def observe_first_send(request: Any, iteration: int | None) -> None:
    observer = _OBSERVER
    if observer is None:
        return
    try:
        observer.first_send(request, iteration)
    except Exception:  # noqa: BLE001 — observation never touches the send
        logger.exception("[mandate taps] first_send observer failed — the send is untouched")


def observe_tool_results(
    calls: list[dict[str, Any]],
    content_results: list[dict[str, Any]],
    full_results: list[Any],
) -> None:
    observer = _OBSERVER
    if observer is None:
        return
    try:
        observer.tool_results(calls, content_results, full_results)
    except Exception:  # noqa: BLE001 — observation never touches the tool loop
        logger.exception("[mandate taps] tool_results observer failed — the loop is untouched")


__all__ = [
    "DoorTap",
    "DoorTapHandle",
    "LiveRunObserver",
    "MandateReplay",
    "MANDATE_DOOR",
    "MandateReplayRefused",
    "ReplayKey",
    "FINGERPRINT_VERSION",
    "ROW_ID_RE",
    "agent_run_from_answer",
    "answer_with_copy_row_ids",
    "answer_with_stable_row_ids",
    "answer_fingerprint",
    "answer_from_agent_run",
    "get_live_run_observer",
    "get_mandate_door_tap",
    "observe_first_send",
    "observe_tool_results",
    "record_answer",
    "replay_answer",
    "replay_lookup",
    "replay_store",
    "request_fingerprint",
    "row_ids_in",
    "set_live_run_observer",
    "set_mandate_replay",
    "set_mandate_door_tap",
    "tapped_door",
    "with_stable_row_ids",
]
