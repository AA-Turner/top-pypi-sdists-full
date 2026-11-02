"""Owned fixed-size rank execution with event-driven restoration and completion barriers."""

import multiprocessing
import time
from dataclasses import replace
from multiprocessing.connection import wait

from labqoat.training.distributed.rank_event import RankEvent
from labqoat.training.distributed.rank_execution import RankExecution
from labqoat.training.distributed.rank_failure_error import RankFailureError
from labqoat.training.distributed.rank_process import RankProcess


class RankProcesses:
    """Spawn fresh interpreters and terminate every owned peer whenever one rank fails."""

    def __init__(self) -> None:
        """Keep construction inert; own all handles created during a later start."""
        self.members: list[RankProcess] = []
        self._completed: set[int] = set()

    def start(self, execution: RankExecution) -> None:
        """Use spawn, never fork mutable accelerator/framework state from the root invocation."""
        if self.members:
            raise RuntimeError("Distributed rank processes cannot be started twice")
        context = multiprocessing.get_context("spawn")
        for rank in range(len(execution.group.ranks)):
            parent, child = context.Pipe()
            owned = replace(execution, rank=rank)
            process = context.Process(target=owned.run, args=(child,), name=f"labqoat-rank-{rank}")
            self.members.append(RankProcess(rank, process, parent))
            try:
                process.start()
            except Exception as error:
                raise RankFailureError(rank, "Rank process startup failed") from error
            finally:
                child.close()

    def receive(self, pending: set[int], deadline: float | None) -> RankEvent:
        """Wait on rank channels and process exits; the fixed restore deadline never resets on progress."""
        members = [member for member in self.members if member.rank in pending]
        timeout = None if deadline is None else max(0.0, deadline - time.monotonic())
        if timeout == 0:
            raise RankFailureError(min(pending), "Distributed restoration deadline expired")
        active = [member for member in self.members if member.rank not in self._completed]
        ready = wait([member.channel for member in members] + [member.process.sentinel for member in active], timeout)
        for member in members:
            if member.channel in ready:
                event = self._event(member)
                if event.phase == "completed":
                    self._completed.add(event.rank)
                return event
        rank = next((member.rank for member in active if member.process.sentinel in ready), min(pending))
        raise RankFailureError(rank, "Rank exited or distributed restoration deadline expired")

    @staticmethod
    def _event(member: RankProcess) -> RankEvent:
        """Reject closed channels and mismatched rank messages before advancing either barrier."""
        try:
            event: object = member.channel.recv()
        except EOFError as error:
            raise RankFailureError(member.rank, "Rank channel closed before completion") from error
        if not isinstance(event, RankEvent) or event.rank != member.rank:
            raise RankFailureError(member.rank, "Invalid rank event")
        if event.phase == "failed":
            raise RankFailureError(member.rank, event.reason)
        return event

    def permit(self) -> None:
        """Release all ranks only after the caller commits aggregate restoration and arms fit supervision."""
        for member in self.members:
            if member.process.exitcode is not None:
                raise RankFailureError(member.rank, "Restored rank exited before group fit")
            try:
                member.channel.send("fit")
            except OSError as error:
                raise RankFailureError(member.rank, "Rank start channel closed") from error

    def close(self) -> None:
        """Reap all peers even if one owned handle fails to close."""
        from contextlib import ExitStack

        with ExitStack() as stack:
            for member in self.members:
                stack.callback(member.close)
        self.members.clear()
        self._completed.clear()
