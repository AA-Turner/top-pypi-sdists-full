"""The integrations take a run's built-in commands for the script (agentic W&B C.1): HF Trainer and Lightning
register checkpoint, config, stop, pause and resume on rank 0's run (so its beat declares them), and at a step every
rank reaches hand rank 0's claimed commands to every rank (`RankChannel`), so a collective save or an LR change
happens on every rank at the same step, and a pause holds every rank there (D23). Rank 0 answers. A kind the script registered itself (`run.on(TrainerCommand.EVAL_NOW, fn)`)
runs on rank 0 at the same point. Why: sdk/run/commands/DESIGN.md "Every rank"."""

from __future__ import annotations

import os
from collections.abc import Callable, Iterable
from typing import Any

from probe.sdk.run.commands.pause import do_commands, restart_progress, run_commands
from probe.sdk.run.commands.ranks import RankChannel, get_world

#: The run kinds an integration does itself.
BUILT_IN = ("checkpoint", "config", "stop", "pause", "resume")
#: The config keys an integration applies: the optimizer's learning rate (`learning_rate` is HF's name for it).
LR_KEYS = ("lr", "learning_rate")


def _refuse_outside_step_end(*_args: Any) -> None:
    raise RuntimeError("the integration takes this command at its step end, on every rank")


class TrainerCommands:
    """One integration's commands, on every rank. `run` is rank 0's handle (None elsewhere)."""

    def __init__(self) -> None:
        self.channel = RankChannel()
        #: Checkpoints asked for, answered once the framework saved (rank 0).
        self.pending_saves: list[dict] = []
        #: A pause was answered at a step end and holds at `hold`, once the step's metrics were sent.
        self.is_hold_due = False
        #: The run that pause was answered on (rank 0): the run reads paused until the job holds and resumes.
        self._paused_run_id: str | None = None

    def begin(self, run: Any) -> None:
        """At train begin, on every rank: say this rank takes commands; on rank 0, declare the built-in kinds, all
        three on one beat (one at a time put a beat saying only `checkpoint` on the wire, and it could land last)."""
        self.channel.announce()
        if self.is_hold_due:
            self.is_hold_due = self._should_keep_hold(run)
        if run is None or not hasattr(run, "_add_handlers"):
            return
        from probe.sdk.run.commands.commands import RUN_KINDS

        run._add_handlers({kind.value: _refuse_outside_step_end for kind in RUN_KINDS}, should_replace=False)
        run._commands.is_shared = True

    def take(self, run: Any, step: int) -> list[dict]:
        """At a step every rank reaches: the commands to act on here (rank 0's, handed to every rank)."""
        if not self.channel.is_handoff(step):
            return []
        return self._exchange(run, run._take_due_commands() if self._is_claimer(run) else [])

    def run(self, run: Any, step: int, apply: Callable[[dict], None]) -> None:
        """At a step every rank reaches: do and answer this step's commands with `apply` now (a pause reads paused at
        once); a pause among them holds every rank at `hold`, which the integration calls once the step's metrics
        are sent (D23)."""
        self.is_hold_due = do_commands(self.take(run, step), apply=apply, answer=self._make_answer(run),
                                       is_paused=self.is_hold_due)  # fmt: skip
        if self.is_hold_due and self._is_claimer(run):
            self._paused_run_id = str(run.id)

    def hold(self, run: Any, apply: Callable[[dict], None]) -> None:
        """Every rank, once the step's metrics were sent: a pause `run` answered holds here until a resume or a stop,
        the ranks meeting every `HOLD_POLL_SECONDS` to take what was asked since (a no-op without one)."""
        if self.is_hold_due:
            self._hold_now(run, [], apply, self._make_answer(run))

    def _hold_now(self, run: Any, commands: list[dict], apply: Callable[[dict], None], answer: Callable) -> None:
        is_paused, self.is_hold_due = self.is_hold_due, False
        if run_commands(commands, take=lambda timeout: self._take_held(run, timeout), apply=apply, answer=answer,
                        is_paused=is_paused):  # fmt: skip
            restart_progress(run)

    def _should_keep_hold(self, run: Any) -> bool:
        """At a train() after one that ended between a pause's answer and its hold (it raised): the run still reads
        paused, so this train() holds at its start when it writes that run; a new run drops it. Rank 0 knows which;
        every rank is told, so all hold or none."""
        is_same_run = self._is_claimer(run) and str(run.id) == self._paused_run_id
        kept, _reason = self.channel.exchange([{"kind": "pause"}] if is_same_run else [])
        return bool(kept)

    def _make_answer(self, run: Any) -> Callable[[dict, "str | None"], None]:
        return lambda command, reason: self.answer(run, command, reason=reason)

    def _take_held(self, run: Any, timeout: float) -> list[dict]:
        """While held: rank 0's asks once one arrives or `timeout` passed, handed to every rank."""
        return self._exchange(run, run._wait_for_due(timeout) if self._is_claimer(run) else [])

    def _is_claimer(self, run: Any) -> bool:
        return run is not None and get_world()[0] == 0 and hasattr(run, "_commands")

    def _exchange(self, run: Any, mine: list[dict]) -> list[dict]:
        commands, refused = self.channel.exchange(mine)
        if refused and mine:
            run._refuse_commands(mine, refused)
        return commands

    def answer(self, run: Any, command: dict, *, result: dict | None = None, reason: str | None = None) -> None:
        """Rank 0's answer: `done` with `result`, or `refused` with `reason`."""
        if run is not None:
            run._send_answer(command, "refused" if reason else "done", reason, result or {})

    def run_declared(self, run: Any, command: dict) -> None:
        """A kind the script registered itself: its handler, on rank 0."""
        if run is not None:
            run._answer_command(command)

    def apply_config(self, run: Any, command: dict, optimizers: Iterable[Any], schedulers: Iterable[Any]) -> None:
        """Set the asked learning rate on every optimizer and scheduler of this rank, so the schedule's shape
        continues from the new base; rank 0 answers and records what was applied on `run.config`."""
        values = dict((command.get("args") or {}).get("values") or {})
        lr_key = next((key for key in LR_KEYS if key in values), None)
        if lr_key is not None:
            set_learning_rate(float(values[lr_key]), optimizers, schedulers)
        if run is None:
            return
        if lr_key is None:
            self.answer(run, command, reason=f"this integration applies {' or '.join(LR_KEYS)}; register "
                                             "run.on(CommandKind.CONFIG, ...) for the others")  # fmt: skip
            return
        # Asked for by a person: a change, never a surprise to warn about.
        run.update_config({lr_key: values[lr_key]}, allow_val_change=True)
        self.answer(run, command, result={"applied": [lr_key], "not_applied": sorted(set(values) - {lr_key})})

    @property
    def save_command_id(self) -> str | None:
        """The checkpoint command the next save answers (the first, when two were asked at one step): its artifact
        carries it as `meta.command_id`."""
        return str(self.pending_saves[0]["id"]) if self.pending_saves else None

    def answer_saves(self, run: Any, path: str | None, step: int, artifact_id: str | None = None) -> None:
        """Rank 0, once the framework saved and the save was recorded: answer the checkpoints asked for with the
        checkpoint's artifact id (none when it was not recorded, or its row is still queued), its step and path."""
        for command in self.pending_saves:
            self.answer(run, command, result=get_save_result(step, path, artifact_id))
        self.pending_saves.clear()


def get_save_result(step: int, path: str | None, artifact_id: str | None) -> dict[str, Any]:
    """A commanded checkpoint's answer: its artifact id (agentic W&B C.1), and the step and path it was saved at."""
    result: dict[str, Any] = {"step": step}
    if path:
        result["path"] = os.path.abspath(path)
    if artifact_id:
        result["artifact_id"] = artifact_id
    return result


def apply_resume_overrides(run: Any, optimizers: Iterable[Any], schedulers: Iterable[Any]) -> dict[str, Any]:
    """After the framework loaded the checkpoint (its optimizer state brings the old learning rate back): set the
    learning rate `probe run resume --config` asked for on this rank's optimizers and schedulers; rank 0 records it
    as applied (`confirm_resume_overrides`). Other keys stay asked for the script to apply. What was applied."""
    from probe.sdk.run.resume.resume import read_resume_env

    _checkpoint, overrides = read_resume_env()
    lr_key = next((key for key in LR_KEYS if key in overrides), None)
    if lr_key is None:
        return {}
    set_learning_rate(float(overrides[lr_key]), optimizers, schedulers)
    applied = {lr_key: overrides[lr_key]}
    if run is not None and hasattr(run, "confirm_resume_overrides"):
        run.confirm_resume_overrides(applied)
    return applied


def set_learning_rate(lr: float, optimizers: Iterable[Any], schedulers: Iterable[Any]) -> None:
    """Every param group's `lr` (and `initial_lr`), and each scheduler's `base_lrs`: a LambdaLR-shaped schedule
    (HF's, Lightning's usual) then multiplies the new base."""
    for optimizer in optimizers:
        for group in getattr(optimizer, "param_groups", []):
            group["lr"] = lr
            if "initial_lr" in group:
                group["initial_lr"] = lr
    for scheduler in schedulers:
        if hasattr(scheduler, "base_lrs"):
            scheduler.base_lrs = [lr for _ in scheduler.base_lrs]


__all__ = ["BUILT_IN", "LR_KEYS", "TrainerCommands", "apply_resume_overrides", "get_save_result", "set_learning_rate"]
