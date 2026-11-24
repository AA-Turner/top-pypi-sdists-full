"""Pause and resume (D23): a job asked to `pause` holds at a step boundary once that step's metrics are sent (a
`run.log()` after its row, an integration's step once it logged, `probe.commands.sync()`, Harbor's next trial start),
until `resume` or `stop`.
The beat thread keeps beating and claiming meanwhile, so the run stays live; the server reads `paused` from the done
answer. An ask that arrives while it holds runs in place (a checkpoint, a config change); `stop` ends the hold, then
stops. Why: DESIGN.md "Pause and resume"."""

from __future__ import annotations

from collections.abc import Callable, Iterable

from ....generated.records import CommandKind

#: The kinds the SDK does itself at a safe point; a script declares them with `run.on(CommandKind.PAUSE)`.
PAUSE_KINDS = (CommandKind.PAUSE, CommandKind.RESUME)
#: How long one wait for an ask lasts while held: the ranks of a multi-process job meet at a collective this often
#: (each meeting is short, far inside any collective timeout), and a signal (`stop --force`'s SIGTERM) is handled
#: within it.
HOLD_POLL_SECONDS = 2.0
ALREADY_PAUSED = "it is already paused"
NOT_PAUSED = "it is not paused: nothing to resume"

#: Takes the asks claimed since, waiting at most this many seconds for one (every rank calls it at once).
TakeCommands = Callable[[float], list[dict]]
#: Does one ask that is not pause or resume, and answers it (rank 0).
ApplyCommand = Callable[[dict], None]
#: Answers a pause or resume: `done` with no reason, else `refused` with it (rank 0; a no-op on other ranks).
AnswerCommand = Callable[[dict, "str | None"], None]


def run_commands(commands: Iterable[dict], *, take: TakeCommands, apply: ApplyCommand, answer: AnswerCommand,
                 is_paused: bool = False) -> bool:
    """Do `commands` in order at this safe point. A `pause` among them (or `is_paused`: one `do_commands` already
    answered) holds here, taking and doing each ask as it comes, until a `resume` (answered, then the rest go on) or
    a `stop` (done, which ends the hold). Every rank of a multi-process job calls this with the same commands and the
    same `take`, so all hold and go on at the same step. Whether it held: the caller then restarts its progress clock
    (`restart_progress`), so the server's stall detector never reads the pause as a stall once the run reads running
    again."""
    was_held = is_paused = do_commands(commands, apply=apply, answer=answer, is_paused=is_paused)
    while is_paused:
        is_paused = do_commands(take(HOLD_POLL_SECONDS), apply=apply, answer=answer, is_paused=True)
    return was_held


def do_commands(commands: Iterable[dict], *, apply: ApplyCommand, answer: AnswerCommand, is_paused: bool) -> bool:
    """Do and answer `commands` in order, never waiting: whether the job is paused after them (a pause answered `done`,
    and no resume or stop after it). A trainer whose step's metrics are sent after the hook that takes the asks does
    them here at once, then holds later (`run_commands(is_paused=True)`)."""
    for command in commands:
        kind = command.get("kind")
        if kind == CommandKind.PAUSE.value:
            answer(command, ALREADY_PAUSED if is_paused else None)
            is_paused = True
        elif kind == CommandKind.RESUME.value:
            answer(command, None if is_paused else NOT_PAUSED)
            is_paused = False
        else:
            apply(command)
            if kind == CommandKind.STOP.value:
                is_paused = False  # the server reads it running again: it goes on to its stop
    return is_paused


def restart_progress(run: object) -> None:
    """After a hold: this writer's progress clock starts again from now, so the time held is neither an idle stretch
    on the next beat nor a gap the stall detector learns as normal (`closing/heartbeat._Progress`)."""
    progress = getattr(run, "_progress", None)
    if progress is not None:
        progress.restart()


__all__ = ["ALREADY_PAUSED", "HOLD_POLL_SECONDS", "NOT_PAUSED", "PAUSE_KINDS", "do_commands", "restart_progress",
           "run_commands"]
