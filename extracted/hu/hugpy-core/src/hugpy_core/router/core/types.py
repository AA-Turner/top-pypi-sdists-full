"""The router's data contract — plain frozen values the decision reads (no I/O)."""
from __future__ import annotations

from dataclasses import dataclass, field
import json
from typing import Dict, FrozenSet, List, Optional, Tuple


@dataclass(frozen=True)
class Resident:
    """A model loaded on a box right now (the box's residents table)."""
    key: str
    state: str = "idle"              # idle | serving | loading | error | dead
    healthy: bool = True
    busy: bool = False
    last_used: float = 0.0


@dataclass(frozen=True)
class Box:
    """One box as its link last saw it."""
    name: str
    online: bool = True
    pool: str = ""
    blocked: bool = False
    wildcard: bool = False         # last route for a catalog model with no allocation
    residents: Tuple[Resident, ...] = ()
    models: FrozenSet[str] = frozenset()      # the box's catalog (what it can load)
    room_gpu: Optional[int] = None            # bytes the box could place now (its own view)
    last_picked: float = 0.0
    observation_identity: Optional[Tuple[str, str]] = None  # store ID, process epoch
    observation_generation: Optional[int] = None


@dataclass(frozen=True)
class CallSpec:
    """What a call asks for."""
    model: str                                 # the base model key
    options: Optional[str] = None              # the model@options part, passed through to the box
    pin: Optional[str] = None                  # a box name: a contract, never rerouted
    pool: str = ""
    knobs_json: str = "{}"                    # canonical, immutable JSON preference snapshot

    @property
    def contract_key(self) -> tuple:
        return (self.options, self.knobs_json)

    def execution_request(self) -> dict:
        """Routing evidence, not a resolved worker plan or reservation."""
        return {"schema": "hugpy.execution-request", "version": 1,
                "model": self.model, "options": self.options,
                "knobs": json.loads(self.knobs_json)}


@dataclass
class Decision:
    """The ranked boxes for a call (best first), or none with every box's reason."""
    boxes: List[str] = field(default_factory=list)
    why: Dict[str, str] = field(default_factory=dict)        # box -> why it is first / ranked
    refused: Dict[str, str] = field(default_factory=dict)    # box -> why it cannot take the call
    path: str = ""                                            # pin | serving | load | refused

    @property
    def ok(self) -> bool:
        return bool(self.boxes)
