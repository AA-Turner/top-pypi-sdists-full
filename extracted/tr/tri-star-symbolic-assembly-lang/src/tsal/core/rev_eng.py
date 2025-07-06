import os
import time
import uuid
from collections import defaultdict
from typing import Optional, Dict, List, Any

from .mesh_logger import log_event
from .voxel import MeshVoxel
from .constants import ensure_spin_axis

class Rev_Eng:
    """
    Reverse-Engineer (Rev_Eng): System-wide tracker and cataloguer for lineage, state, IO spin, and mesh context.
    """

    def __init__(self, origin: str = None, session_id: str = None):
        self.origin = origin or "Root"
        self.session_id = session_id or str(uuid.uuid4())
        self.lineage = []  # List of ancestor names/IDs
        self.events = []  # Log of (timestamp, action, details)
        self.state = {}  # Arbitrary live state storage
        self.data_stats = {  # Real-time stats for IO/data
            "total_bytes": 0,
            "chunk_count": 0,
            "last_rate": 0.0,  # bytes/sec
            "last_update": time.time(),
        }
        self.rate_log = []  # (timestamp, bytes, rate) tuples
        self.spin_log = []  # (timestamp, spin_dir, I/O, updown)
        self.voxel_log: List[Dict[str, Any]] = (
            []
        )  # pace/rate/state/spin snapshots
        self.mesh_coords = (
            {}
        )  # e.g., {x:..., y:..., z:..., vx:..., vy:..., vz:..., phase:..., mesh:...}
        self.identity = {}  # Who/What/Why/When/Where details

    # === LINEAGE TRACKING ===
    def add_lineage(self, name: str):
        self.lineage.append(name)

    def get_lineage(self) -> List[str]:
        return list(self.lineage)

    # === DATA FLOW TRACKING ===
    def log_data(self, n_bytes: int, direction: str, updown: str = None):
        now = time.time()
        dt = now - self.data_stats["last_update"]
        self.data_stats["total_bytes"] += n_bytes
        self.data_stats["chunk_count"] += 1
        rate = n_bytes / dt if dt > 0 else 0.0
        self.data_stats["last_rate"] = rate
        self.data_stats["last_update"] = now
        self.rate_log.append((now, n_bytes, rate))
        self.log_spin(direction=direction, updown=updown, I_O=direction)
        voxel = MeshVoxel(
            pace=self.data_stats["chunk_count"],
            rate=rate,
            state=direction,
            spin=updown or direction,
        )
        ensure_spin_axis(voxel)
        self.voxel_log.append(voxel.as_dict())
        log_event(
            "DATA",
            voxel.as_dict(),
            phase="io",
            origin=self.origin,
        )

    def log_grammar(self, language: str, rule: str) -> None:
        """Log grammar rule usage."""
        self.log_event("GRAMMAR", language=language, rule=rule)

    def log_humour(self, context: str, joke: str) -> None:
        """Log humour events."""
        self.log_event("HUMOUR", context=context, joke=joke)

    def log_spin(self, direction: str, updown: str = None, I_O: str = None):
        # direction: 'in', 'out', 'clockwise', 'counter', etc.
        now = time.time()
        self.spin_log.append((now, direction, I_O, updown))

    def spin_collisions(self) -> Dict[str, int]:
        """Return XOR/NAND/AND counts over sequential spin directions."""
        counts = {"xor": 0, "nand": 0, "and": 0}
        if len(self.spin_log) < 2:
            return counts

        def as_bool(v: Any) -> bool:
            if isinstance(v, str):
                return v.lower() in {"up", "in", "1", "true"}
            return bool(v)

        for (_, a, _, _), (_, b, _, _) in zip(
            self.spin_log, self.spin_log[1:]
        ):
            ba = as_bool(a)
            bb = as_bool(b)
            counts["xor"] += ba ^ bb
            counts["and"] += ba and bb
            counts["nand"] += not (ba and bb)
        return counts

    # === STATE/CONTEXT TRACKING ===
    def set_state(self, **kwargs):
        self.state.update(kwargs)

    def log_event(self, action: str, **details):
        now = time.time()
        self.events.append((now, action, details))

    def update_mesh_coords(self, **coords):
        self.mesh_coords.update(coords)

    def set_identity(
        self,
        who: str,
        what: str,
        where: str,
        when: Optional[str] = None,
        why: str = None,
    ):
        self.identity = {
            "who": who,
            "what": what,
            "where": where,
            "when": when or time.strftime("%Y-%m-%d %H:%M:%S"),
            "why": why,
        }

    # === UNIVERSAL REPORTING / EXPORT ===
    def summary(self) -> Dict[str, Any]:
        return {
            "origin": self.origin,
            "session_id": self.session_id,
            "lineage": self.lineage,
            "data_stats": self.data_stats,
            "recent_rate": self.data_stats["last_rate"],
            "rate_log": self.rate_log[-5:],
            "spin_log": self.spin_log[-5:],
            "voxels": self.voxel_log[-5:],
            "collisions": self.spin_collisions(),
            "state": self.state,
            "mesh_coords": self.mesh_coords,
            "identity": self.identity,
            "event_count": len(self.events),
        }

    def print_summary(self):
        import pprint

        pprint.pprint(self.summary())

    # === EXTENSIBLE: Custom Hooks for TSAL/mesh logging, e.g., phase, spiral, error dignity ===
    def log_tsal_phase(
        self, phase: str, symbol: str, context: Optional[str] = None
    ):
        self.log_event(
            "TSAL_PHASE", phase=phase, symbol=symbol, context=context
        )

    def log_error(
        self, err: str, location: str = None, recoverable: bool = True
    ):
        self.log_event(
            "ERROR", error=err, location=location, recoverable=recoverable
        )
        # Optional: Spiral/bloom logic could re-inject error into mesh for "mad monkey" learning

# Example Usage:
if __name__ == "__main__":
    rev = Rev_Eng(origin="Genesis_Spiral")
    rev.add_lineage("Proto_Node_0")
    rev.set_identity(
        "RevEngKernel", "Reverse-Engineer", "Mesh_Center", why="System Audit"
    )
    rev.log_data(4096, direction="in", updown="up")
    rev.log_data(2048, direction="out", updown="down")
    rev.update_mesh_coords(
        x=1, y=2, z=3, vx=0.1, vy=0.2, vz=0.3, phase="spiral", mesh="central"
    )
    rev.log_tsal_phase("ALIGN", "6", context="Startup Alignment")
    rev.log_error("Checksum mismatch", location="sector_17")
    rev.print_summary()
