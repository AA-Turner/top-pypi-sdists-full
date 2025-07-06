from __future__ import annotations

"""Basic TSAL opcode executor with meta-flag control."""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from .symbols import get_symbol
from ..tristar.handshake import handshake
from .rev_eng import Rev_Eng

@dataclass
class MetaFlagProtocol:
    """Execution flags controlling TSALExecutor behaviour."""

    dry_run: bool = False
    narrative_mode: bool = False
    resonance_threshold: float = 0.0
    fork_tracking: bool = False

class TSALExecutor:
    """Execute TSAL opcodes with logging and optional dry-run."""

    def __init__(
        self,
        meta: Optional[MetaFlagProtocol] = None,
        rev: Optional[Rev_Eng] = None,
    ) -> None:
        self.meta = meta or MetaFlagProtocol()
        self.rev = rev or Rev_Eng(origin="TSALExecutor")
        self.state: Dict[str, float] = {}
        self.op_log: List[int] = []
        self.forks: List[int] = []

    def execute(self, opcode: int, **kwargs) -> None:
        symbol, name, desc = get_symbol(opcode)
        if self.meta.narrative_mode:
            self.rev.log_event(
                "OP_NARRATIVE", opcode=opcode, name=name, desc=desc
            )
        if opcode == 0xA:  # SYNC
            local = kwargs.get("local", 0.0)
            remote = kwargs.get("remote", 0.0)
            metrics = handshake(local, remote, self.rev)
            if metrics["resonance"] >= self.meta.resonance_threshold:
                self.rev.log_event("RESONANCE_THRESHOLD", **metrics)
        if self.meta.fork_tracking and kwargs.get("fork"):
            fork_id = len(self.forks) + 1
            self.forks.append(fork_id)
            self.rev.log_event("FORK", id=fork_id, opcode=opcode)
        if not self.meta.dry_run:
            self.op_log.append(opcode)

    def execute_sequence(self, ops: List[int]) -> None:
        for op in ops:
            self.execute(op)

__all__ = ["MetaFlagProtocol", "TSALExecutor"]
