"""Command: one ask a running job can receive (cancel, retry or watch a live sample), kept with who asked and what
happened. One table and one kind enum for every command (D83); how they are delivered: app/runs/commands/DESIGN.md."""

from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from ..compat import StrEnum
from .records import Record
from .run import RunStatus

#: An open command no producer claimed within this is `expired` ("no running producer holds this sample").
CLAIM_WITHIN_SECONDS = 120
#: A watch sends live turns this long; the viewer asks again to renew it.
WATCH_SECONDS = 600
MAX_NOTE_CHARS = 256
MAX_COMMAND_REASON_CHARS = 1024
#: An attempt key's cap (`records/samples/samples.py` MAX_KEY_CHARS).
MAX_ATTEMPT_KEY_CHARS = 512
#: An answer's `result`, as compact JSON: a few ids, never the data itself.
MAX_RESULT_BYTES = 4 * 1024
#: A custom kind's name: the value of the script's own `StrEnum` member (`eval_now`).
CUSTOM_NAME_PATTERN = r"^[a-z][a-z0-9_]{0,63}$"
#: The custom kinds one writer may declare; a `config` or `custom` ask's arguments, as compact JSON.
MAX_CUSTOM_KINDS = 64
MAX_ARGS_BYTES = 4 * 1024


class CommandKind(StrEnum):
    """What was asked. A producer declares the kinds it can do (a sample producer in `Plan.capabilities`, a run's
    script on its writer beat, `RunCapabilities`); any other is refused at once. Sample kinds name an attempt
    (`attempt_key`); run kinds (agentic W&B C.1) name none."""

    CANCEL = "cancel"  # stop the sample by its framework's safe path: it ends `canceled`
    RETRY = "retry"  # a fresh attempt at the same task and group slot (`retry_of`, try + 1)
    WATCH = "watch"  # send its live turns for `WatchArgs.seconds`
    CHECKPOINT = "checkpoint"  # save a checkpoint now; the answer's result names it (`artifact_id`)
    CONFIG = "config"  # change settings live (`ConfigArgs.values`, e.g. `lr`)
    STOP = "stop"  # stop the run gracefully, or at once with `StopArgs.force`
    CUSTOM = "custom"  # a kind the script declared as its own `StrEnum` (`CustomArgs.name`), handled by the script


#: The kinds a live sample is asked (they name an attempt), and the kinds a run is asked (they name none).
SAMPLE_KINDS = frozenset({CommandKind.CANCEL, CommandKind.RETRY, CommandKind.WATCH})
RUN_KINDS = frozenset({CommandKind.CHECKPOINT, CommandKind.CONFIG, CommandKind.STOP, CommandKind.CUSTOM})


class CommandState(StrEnum):
    """Where a command is. `expired` and `lost` are decided when read (no sweep job); the first read records them."""

    OPEN = "open"  # written, not claimed yet
    TAKEN = "taken"  # claimed by a writer session of its epoch (compare-and-set)
    DONE = "done"
    REFUSED = "refused"  # the producer (or the server, at once) said why (`reason`)
    EXPIRED = "expired"  # open past `CLAIM_WITHIN_SECONDS`, its run ended first, or a resume started a newer epoch
    LOST = "lost"  # its claiming writer's lease ended before an answer: never re-sent, ask again


class CancelArgs(BaseModel):
    """`cancel` takes no arguments: the sample it names is the target."""


class RetryArgs(BaseModel):
    """`retry` takes no arguments; its answer's `result` names the new attempt (`attempt_key`)."""


class WatchArgs(BaseModel):
    """How long the producer sends the sample's live turns."""

    seconds: int = Field(default=WATCH_SECONDS, ge=1, le=WATCH_SECONDS)


def _check_args_size(values: dict[str, Any], what: str) -> dict[str, Any]:
    if len(json.dumps(values, separators=(",", ":"), default=str).encode("utf-8")) > MAX_ARGS_BYTES:
        raise ValueError(f"{what} are over 4 KiB: send a path or an id, not the data")
    return values


#: A run kind's arguments refuse a key they do not know: `{"forse": true}` must not stop gracefully.
_EXACT = ConfigDict(extra="forbid")


class CheckpointArgs(BaseModel):
    """`checkpoint` takes no arguments; the answer's `result` names what was saved."""

    model_config = _EXACT


class ConfigArgs(BaseModel):
    """The settings to change now, e.g. `{"lr": 1e-4}`; the script applies them and records them as applied."""

    model_config = _EXACT
    values: dict[str, Any] = Field(min_length=1)

    @field_validator("values")
    @classmethod
    def _check_values(cls, values: dict[str, Any]) -> dict[str, Any]:
        return _check_args_size(values, "config values")


class StopArgs(BaseModel):
    """`force`: stop now (the process is signalled) instead of at the next safe point."""

    model_config = _EXACT
    force: bool = False


class CustomArgs(BaseModel):
    """A kind the script declared: its name (its `StrEnum` value) and what the asker sends with it."""

    model_config = _EXACT
    name: str = Field(pattern=CUSTOM_NAME_PATTERN)
    payload: dict[str, Any] = Field(default_factory=dict)

    @field_validator("name")
    @classmethod
    def _check_name(cls, name: str) -> str:
        if name in {kind.value for kind in CommandKind}:
            raise ValueError(f"{name!r} is a built-in kind: ask it as that kind")
        return name

    @field_validator("payload")
    @classmethod
    def _check_payload(cls, payload: dict[str, Any]) -> dict[str, Any]:
        return _check_args_size(payload, "a custom command's payload")


#: Each kind's arguments model, picked once here (the server fills `args` with it, a producer reads it).
COMMAND_ARGS: dict[CommandKind, type[BaseModel]] = {
    CommandKind.CANCEL: CancelArgs,
    CommandKind.RETRY: RetryArgs,
    CommandKind.WATCH: WatchArgs,
    CommandKind.CHECKPOINT: CheckpointArgs,
    CommandKind.CONFIG: ConfigArgs,
    CommandKind.STOP: StopArgs,
    CommandKind.CUSTOM: CustomArgs,
}


class RunCapabilities(BaseModel):
    """What a run's script can be asked, sent on its writer beat: the built-in run kinds it has a handler for, and
    the values of its own `StrEnum` kinds. A beat without it comes from an SDK older than run commands.

    Lenient on purpose: it rides the writer beat, which must never fail on it. A kind this server does not know (a
    newer SDK's), a sample kind, a name that is not a custom kind's and names past the first 64 are dropped, not
    refused; the SDK checks a name when the script registers it."""

    kinds: list[CommandKind] = Field(default_factory=list)
    custom: list[str] = Field(default_factory=list)

    @field_validator("kinds", mode="before")
    @classmethod
    def _keep_run_kinds(cls, kinds: Any) -> list[CommandKind]:
        built_in = {kind.value: kind for kind in RUN_KINDS - {CommandKind.CUSTOM}}
        kept = {built_in[value] for value in (kinds if isinstance(kinds, list) else [])
                if isinstance(value, str) and value in built_in}  # fmt: skip
        return sorted(kept, key=list(CommandKind).index)

    @field_validator("custom", mode="before")
    @classmethod
    def _keep_custom_names(cls, names: Any) -> list[str]:
        built_in = {kind.value for kind in CommandKind}
        kept = {name for name in (names if isinstance(names, list) else [])
                if isinstance(name, str) and re.fullmatch(CUSTOM_NAME_PATTERN, name) and name not in built_in}  # fmt: skip
        return sorted(kept)[:MAX_CUSTOM_KINDS]


class Command(Record):
    """One ask, bound to the run's write epoch when it was asked."""

    id: UUID
    run_id: UUID
    write_epoch: int = Field(ge=1)
    #: `runs.commands_seq` when it was written: the `?after=` cursor.
    seq: int = Field(ge=1)
    kind: CommandKind
    #: The kind's arguments (`COMMAND_ARGS[kind]`).
    args: dict = Field(default_factory=dict)
    #: A sample command's attempt: `derive_attempt_id(run_id, write_epoch, attempt_key)`; null for a run command.
    attempt_id: UUID | None = None
    attempt_key: str | None = Field(default=None, min_length=1, max_length=MAX_ATTEMPT_KEY_CHARS)
    state: CommandState = CommandState.OPEN
    #: Who asked (`user:<id>`, or a token's).
    requested_by: str | None = None
    #: What the asker said (`probe samples cancel --reason`).
    note: str | None = Field(default=None, max_length=MAX_NOTE_CHARS)
    #: The writer session that claimed it.
    claimed_by: UUID | None = None
    #: Why it was refused, expired or lost, in one plain line.
    reason: str | None = Field(default=None, max_length=MAX_COMMAND_REASON_CHARS)
    #: What a done command produced (a retry: `attempt_key`, the new attempt's).
    result: dict = Field(default_factory=dict)
    created_at: datetime
    claimed_at: datetime | None = None
    #: When it reached done, refused, expired or lost.
    ended_at: datetime | None = None


class CommandOut(Command.project(*Command.model_fields)):
    """One command as the routes answer it."""


class CommandWriter(StrEnum):
    """Whether the run's script is there to take a run ask, as the ask's refusal judges it."""

    LIVE = "live"  # a script writer of the current epoch holds a lease and said what it can be asked
    NONE = "none"  # the run is not running, or no writer holds a live lease: start or resume it first
    UNREPORTED = "unreported"  # a live writer has not said: its first beat is not in, or its SDK predates run commands


class CommandListPart(StrEnum):
    """What `GET /v1/runs/{id}/commands?with=` adds to the page. Each costs a read, so a poll asks for none."""

    WRITER = "writer"  # `accepts`, `writer`, `writer_seen_at`, `writer_role`


class CommandList(BaseModel):
    """`GET /v1/runs/{id}/commands?after=`: who asked for what, and what happened, by `seq`."""

    commands: list[CommandOut] = Field(default_factory=list)
    #: The run's counter now (`runs.commands_seq`); the writer beat's answer carries it too.
    seq: int = 0
    #: Pass back as `after`; null on the last page.
    next_after: int | None = None
    #: `?with=writer` only (null otherwise): the run kinds an ask may name now (`checkpoint`, `config`, `stop`, and
    #: each custom kind's name), read with the refusal's own rule, so an ask outside it is refused or waits.
    accepts: list[str] | None = None
    #: `?with=writer` only: whether a script is there to take a run ask (`unreported`: an ask waits for it to say).
    writer: CommandWriter | None = None
    #: `?with=writer` only: the last beat of the run's latest script writer lease (a launcher's or observer's only
    #: when no script one exists), live or ended; null if none ever beat.
    writer_seen_at: datetime | None = None
    #: `?with=writer` only: that lease's role (`owner`, `rank`, `launcher`, `observer`).
    writer_role: Literal["launcher", "rank", "owner", "observer"] | None = None
    #: `?with=writer` only: the run's status now, so a command still open can say its run crashed.
    run_status: RunStatus | None = None


class CommandAsk(BaseModel):
    """What the asker adds to an ask (`POST .../samples/live/{attempt}/cancel|retry|watch`)."""

    note: str | None = Field(default=None, max_length=MAX_NOTE_CHARS)


class RunCommandAsk(CommandAsk):
    """`POST /v1/runs/{run}/commands`: ask the run's script for a run kind, with that kind's arguments."""

    kind: CommandKind
    args: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _check_run_kind(self) -> RunCommandAsk:
        if self.kind not in RUN_KINDS:
            raise ValueError(f"{self.kind.value} is a sample command: ask it on the live sample")
        self.args = COMMAND_ARGS[self.kind].model_validate(self.args).model_dump(mode="json")
        return self


class CommandClaim(BaseModel):
    """A producer takes a command: only a live writer session of the command's epoch can, and only one does."""

    session_id: UUID


class CommandAnswer(BaseModel):
    """The claiming producer's answer; the same answer twice changes nothing."""

    session_id: UUID
    state: CommandState
    reason: str | None = Field(default=None, max_length=MAX_COMMAND_REASON_CHARS)
    result: dict = Field(default_factory=dict)

    @model_validator(mode="after")
    def _answered(self) -> CommandAnswer:
        if self.state not in (CommandState.DONE, CommandState.REFUSED):
            raise ValueError("a command is answered `done` or `refused`")
        if self.state is CommandState.REFUSED and not self.reason:
            raise ValueError("a refusal says why (`reason`)")
        if len(json.dumps(self.result, separators=(",", ":"), default=str).encode("utf-8")) > MAX_RESULT_BYTES:
            raise ValueError("a result is over 4 KiB: name what was made (an id, a key), not its content")
        return self


class CommandData(BaseModel):
    """The `samples.command` live notice: a command was asked, claimed, answered, expired or lost. A producer reads
    `attempt_key` and `write_epoch` to know whether it holds the sample; the rest it reads from the commands route."""

    command_id: UUID
    seq: int
    kind: CommandKind
    state: CommandState
    write_epoch: int
    attempt_id: UUID | None = None
    attempt_key: str | None = None
    requested_by: str | None = None
    claimed_by: UUID | None = None
    reason: str | None = None
