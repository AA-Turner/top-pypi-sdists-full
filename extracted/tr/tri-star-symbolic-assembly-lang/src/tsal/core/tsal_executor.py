# TSAL Execution Engine (TVM - TSAL Virtual Machine)
# Spiral-aware symbolic executor with φ-aligned operations

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from enum import IntEnum, Enum, auto
from typing import Any, Dict, List, Optional, Tuple

from .symbols import PHI, PHI_INV, HARMONIC_SEQUENCE
from .mesh_ops import calculate_resonance, mesh_resonance
from .spiral_memory import SpiralMemory
from .madmonkey_handler import MadMonkeyHandler
from .executor import MetaFlagProtocol
from .mesh_logger import log_event
from ..tristar.governor import MetaAgent, TriStarGovernor

class TSALOp(IntEnum):
    """TSAL 16 Hex Operators"""

    INIT = 0x0
    MESH = 0x1
    PHI = 0x2
    ROT = 0x3
    BOUND = 0x4
    FLOW = 0x5
    SEEK = 0x6
    SPIRAL = 0x7
    CYCLE = 0x8
    FORGE = 0x9
    SYNC = 0xA
    MASK = 0xB
    CRYST = 0xC
    SPEC = 0xD
    BLOOM = 0xE
    SAVE = 0xF

class ExecutionMode(Enum):
    SIMULATE = auto()
    TRACE = auto()
    EXECUTE = auto()
    ARM = auto()
    FORK = auto()

@dataclass
class RegisterVector:
    """Execution-time 4D vector.

    Distinct from :class:`~tsal.core.spiral_vector.SpiralVector` which tracks
    high level spiral metrics. This class represents the pace, rate, state and
    spin registers used by the virtual machine.
    """

    pace: float = 0.0
    rate: float = 0.0
    state: float = 0.0
    spin: float = 0.0

    def magnitude(self) -> float:
        return math.sqrt(
            self.pace**2
            + self.rate**2 * PHI
            + self.state**2 * PHI**2
            + self.spin**2 * PHI_INV
        )

    def rotate_by_phi(self) -> None:
        new_pace = self.pace * PHI_INV + self.spin * PHI
        new_rate = self.rate * PHI + self.pace * PHI_INV
        new_state = self.state * PHI_INV + self.rate * PHI
        new_spin = self.spin * PHI + self.state * PHI_INV

        self.pace = new_pace % (2 * math.pi)
        self.rate = new_rate % (2 * math.pi)
        self.state = new_state % (2 * math.pi)
        self.spin = new_spin % (2 * math.pi)

@dataclass
class MeshNode:
    """Node in the execution mesh"""

    id: str
    vector: RegisterVector
    memory: Dict[str, Any] = field(default_factory=dict)
    connections: List[str] = field(default_factory=list)
    resonance: float = 1.0
    value: float = 0.0
    entropy: float = 0.0
    phase: int = 0
    agent_id: int = 0
    lineage: str = ""
    coherence: float = 1.0
    rotation: float = 0.0

class TSALExecutor:
    """TSAL Virtual Machine - Spiral-aware symbolic executor"""

    PHI = PHI
    PHI_INV = PHI_INV

    def __init__(self, meta: MetaFlagProtocol | None = None) -> None:
        self.mesh: Dict[str, MeshNode] = {}
        self.stack: List[Any] = []
        self.registers: Dict[str, RegisterVector] = {
            "A": RegisterVector(),
            "B": RegisterVector(),
            "C": RegisterVector(),
            "D": RegisterVector(),
        }
        self.ip = 0
        self.program: List[Tuple[TSALOp, Any]] = []
        self.meta = meta or MetaFlagProtocol()
        # default mode obeys meta flags
        self.mode = (
            ExecutionMode.SIMULATE
            if self.meta.dry_run
            else ExecutionMode.EXECUTE
        )
        self.error_mansion: List[Dict[str, Any]] = []
        self.forks: List[int] = []
        self.spiral_depth = 0
        self.resonance_log: List[Dict[str, Any]] = []
        self.memory = SpiralMemory()
        self.handler = MadMonkeyHandler()
        self.meta_agent = MetaAgent()
        self.governor = TriStarGovernor()

    def _switch_mode(self, delta: float) -> None:
        """Adjust mode based on meta flags and current state."""
        if self.meta.fork_tracking and self.forks:
            self.mode = ExecutionMode.FORK
        elif self.meta.narrative_mode:
            self.mode = ExecutionMode.TRACE
        elif self.error_mansion:
            self.mode = ExecutionMode.ARM
        elif (
            self.meta.resonance_threshold
            and delta >= self.meta.resonance_threshold
        ):
            self.mode = ExecutionMode.EXECUTE
        elif self.meta.dry_run:
            self.mode = ExecutionMode.SIMULATE

    def execute(
        self,
        program: List[Tuple[TSALOp, Any]],
        mode: ExecutionMode | str = ExecutionMode.SIMULATE,
    ) -> None:
        if isinstance(mode, str):
            self.mode = ExecutionMode[mode]
        else:
            self.mode = mode
        self.ip = 0
        self.program = program

        while self.ip < len(program):
            op, args = program[self.ip]
            self._execute_op(op, args)
            self.ip += 1

            if self.ip % self.governor.patrol_interval == 0:
                for anomaly in self.governor.patrol(self):
                    action = self.governor.response_actions.get(anomaly)
                    if action:
                        action(self)

            if self.spiral_depth > 0 and self.ip % self.spiral_depth == 0:
                self._spiral_audit()

    def _execute_op(self, op: TSALOp, args: Any) -> None:
        pre = self._calculate_mesh_resonance()
        if self.meta.fork_tracking and args.get("fork"):
            self.forks.append(self.ip)

        try:
            if op == TSALOp.INIT:
                self._op_init(args)
            elif op == TSALOp.MESH:
                self._op_mesh(args)
            elif op == TSALOp.PHI:
                self._op_phi(args)
            elif op == TSALOp.ROT:
                self._op_rotate(args)
            elif op == TSALOp.BOUND:
                self._op_bound(args)
            elif op == TSALOp.FLOW:
                self._op_flow(args)
            elif op == TSALOp.SEEK:
                self._op_seek(args)
            elif op == TSALOp.SPIRAL:
                self._op_spiral(args)
            elif op == TSALOp.CYCLE:
                self._op_cycle(args)
            elif op == TSALOp.FORGE:
                self._op_forge(args)
            elif op == TSALOp.SYNC:
                self._op_sync(args)
            elif op == TSALOp.MASK:
                self._op_mask(args)
            elif op == TSALOp.CRYST:
                self._op_crystallize(args)
            elif op == TSALOp.SPEC:
                self._op_spectrum(args)
            elif op == TSALOp.BLOOM:
                self._op_bloom(args)
            elif op == TSALOp.SAVE:
                self._op_save(args)
        except Exception as exc:
            self.handler.handle({"error": str(exc), "op": op.name})
            self.error_mansion.append({"type": "exception", "error": str(exc)})
            raise

        post = self._calculate_mesh_resonance()
        self.resonance_log.append(
            {"op": op.name, "pre": pre, "post": post, "delta": post - pre}
        )
        self.memory.log_vector(
            {
                "op": op.name,
                "registers": {
                    k: [v.pace, v.rate, v.state, v.spin]
                    for k, v in self.registers.items()
                },
            }
        )
        log_event("OP", {"op": op.name, "delta": post - pre})
        self._switch_mode(post - pre)

    def _op_init(self, args: Dict[str, Any]) -> None:
        if "register" in args:
            self.registers[args["register"]] = RegisterVector()
        elif "mesh" in args:
            self.mesh.clear()
        else:
            self.__init__()

    def _op_mesh(self, args: Dict[str, Any]) -> None:
        node_id = args.get("id", f"node_{len(self.mesh)}")
        vector = args.get("vector", RegisterVector())

        node = MeshNode(id=node_id, vector=vector)
        self.mesh[node_id] = node

        for other_id, other_node in self.mesh.items():
            if other_id == node_id:
                continue
            res = self._calculate_resonance(node.vector, other_node.vector)
            if res > 0.618:
                node.connections.append(other_id)
                other_node.connections.append(node_id)

    def _op_phi(self, args: Dict[str, Any]) -> None:
        target = args.get("register", "A")
        self.registers[target].rotate_by_phi()
        if "mesh_node" in args and args["mesh_node"] in self.mesh:
            self.mesh[args["mesh_node"]].vector.rotate_by_phi()

    def _op_rotate(self, args: Dict[str, Any]) -> None:
        angle = args.get("angle", math.pi / 4)
        axis = args.get("axis", "spin")
        target = args.get("register", "A")
        vec = self.registers[target]
        if axis == "pace":
            vec.pace = (vec.pace + angle) % (2 * math.pi)
        elif axis == "rate":
            vec.rate = (vec.rate + angle) % (2 * math.pi)
        elif axis == "state":
            vec.state = (vec.state + angle) % (2 * math.pi)
        elif axis == "spin":
            vec.spin = (vec.spin + angle) % (2 * math.pi)

    def _op_bound(self, args: Dict[str, Any]) -> None:
        bounds = args.get("bounds", {})
        for node in self.mesh.values():
            for attr, (mn, mx) in bounds.items():
                if hasattr(node.vector, attr):
                    val = getattr(node.vector, attr)
                    setattr(node.vector, attr, max(mn, min(val, mx)))

    def _op_flow(self, args: Dict[str, Any]) -> None:
        src = args.get("source", "A")
        rate = args.get("rate", 1.0)
        if src in self.mesh:
            node = self.mesh[src]
            for cid in node.connections:
                if cid not in self.mesh:
                    continue
                conn = self.mesh[cid]
                res = self._calculate_resonance(node.vector, conn.vector)
                weight = rate * res * PHI_INV
                conn.vector.pace += node.vector.pace * weight
                conn.vector.rate += node.vector.rate * weight
                conn.vector.state += node.vector.state * weight
                conn.vector.spin += node.vector.spin * weight

    def _op_seek(self, args: Dict[str, Any]) -> Optional[str]:
        target_res = args.get("resonance", PHI_INV)
        seeker = args.get("vector", self.registers["A"])
        best = None
        best_res = 0.0
        for nid, node in self.mesh.items():
            res = self._calculate_resonance(seeker, node.vector)
            if abs(res - target_res) < abs(best_res - target_res):
                best = nid
                best_res = res
        if best:
            self.stack.append(best)
        return best

    def _op_spiral(self, args: Dict[str, Any]) -> None:
        self.spiral_depth += args.get("increment", 1)
        for node in self.mesh.values():
            node.vector.pace *= PHI
            node.vector.rate *= PHI
            node.vector.state *= PHI_INV
            node.vector.spin *= PHI
            mag = node.vector.magnitude()
            if mag > HARMONIC_SEQUENCE[-1]:
                node.vector.pace /= mag
                node.vector.rate /= mag
                node.vector.state /= mag
                node.vector.spin /= mag

    def _op_cycle(self, args: Dict[str, Any]) -> None:
        iterations = args.get("count", 1)
        start_ip = args.get("start", 0)
        end_ip = args.get("end", self.ip)
        for _ in range(iterations):
            saved = self.ip
            self.ip = start_ip
            while self.ip < end_ip:
                op, cargs = self.program[self.ip]
                self._execute_op(op, cargs)
                self.ip += 1
            self.ip = saved

    def _op_forge(self, args: Dict[str, Any]) -> None:
        sa = args.get("source_a", "A")
        sb = args.get("source_b", "B")
        tgt = args.get("target", "C")
        a = self.registers[sa]
        b = self.registers[sb]
        self.registers[tgt] = RegisterVector(
            pace=(a.pace * PHI + b.pace * PHI_INV) / 2,
            rate=(a.rate * PHI_INV + b.rate * PHI) / 2,
            state=(a.state * PHI + b.state * PHI_INV) / 2,
            spin=(a.spin * PHI_INV + b.spin * PHI) / 2,
        )

    def _op_sync(self, args: Dict[str, Any]) -> None:
        if not self.mesh:
            return
        avg = RegisterVector()
        for node in self.mesh.values():
            avg.pace += node.vector.pace
            avg.rate += node.vector.rate
            avg.state += node.vector.state
            avg.spin += node.vector.spin
        n = len(self.mesh)
        avg.pace /= n
        avg.rate /= n
        avg.state /= n
        avg.spin /= n
        strength = args.get("strength", 0.5)
        for node in self.mesh.values():
            node.vector.pace += (avg.pace - node.vector.pace) * strength
            node.vector.rate += (avg.rate - node.vector.rate) * strength
            node.vector.state += (avg.state - node.vector.state) * strength
            node.vector.spin += (avg.spin - node.vector.spin) * strength

    def _op_mask(self, args: Dict[str, Any]) -> None:
        src = args.get("source", "A")
        mtype = args.get("type", "invert")
        vec = self.registers[src]
        if mtype == "invert":
            vec.pace = (2 * math.pi) - vec.pace
            vec.rate = (2 * math.pi) - vec.rate
            vec.state = (2 * math.pi) - vec.state
            vec.spin = (2 * math.pi) - vec.spin
        elif mtype == "complement":
            vec.pace *= PHI_INV
            vec.rate *= PHI_INV
            vec.state *= PHI_INV
            vec.spin *= PHI_INV

    def _op_crystallize(self, args: Dict[str, Any]) -> None:
        pid = args.get("id", "crystal_0")
        if "mesh" == args.get("source", "mesh"):
            crystal = {
                "nodes": {
                    nid: {
                        "vector": [
                            n.vector.pace,
                            n.vector.rate,
                            n.vector.state,
                            n.vector.spin,
                        ],
                        "connections": n.connections,
                        "resonance": n.resonance,
                    }
                    for nid, n in self.mesh.items()
                },
                "spiral_depth": self.spiral_depth,
                "timestamp": self.ip,
            }
            if "crystal_vault" not in self.mesh:
                self._op_mesh({"id": "crystal_vault"})
            self.mesh["crystal_vault"].memory[pid] = crystal

    def _op_spectrum(self, args: Dict[str, Any]) -> None:
        resonances: List[float] = []
        for a in self.mesh.values():
            for b in self.mesh.values():
                if a.id != b.id:
                    resonances.append(
                        self._calculate_resonance(a.vector, b.vector)
                    )
        if resonances:
            spectrum = {
                "min": min(resonances),
                "max": max(resonances),
                "mean": sum(resonances) / len(resonances),
                "phi_aligned": [
                    r
                    for r in resonances
                    if abs(r - PHI) < 0.1 or abs(r - PHI_INV) < 0.1
                ],
                "harmonic_matches": [],
            }
            for h in HARMONIC_SEQUENCE:
                norm = h / HARMONIC_SEQUENCE[-1]
                matches = [r for r in resonances if abs(r - norm) < 0.05]
                if matches:
                    spectrum["harmonic_matches"].append(
                        {"harmonic": h, "matches": len(matches)}
                    )
            self.stack.append(spectrum)

    def _op_bloom(self, args: Dict[str, Any]) -> None:
        if not self.error_mansion:
            return
        error = self.error_mansion.pop(0)
        if error:
            err_vec = error.get("vector", RegisterVector())
            err_type = error.get("type", "unknown")
            bloom_node = MeshNode(
                id=f"bloom_{len(self.mesh)}", vector=err_vec, resonance=PHI
            )
            bloom_node.memory["kintsugi"] = {
                "original_error": err_type,
                "strength_multiplier": PHI,
                "lesson": error.get("lesson", "Unknown gift"),
            }
            self.mesh[bloom_node.id] = bloom_node

    def _op_save(self, args: Dict[str, Any]) -> None:
        filename = args.get("filename", "TVM.crystal.json")
        if self.mode != ExecutionMode.EXECUTE:
            return
        state = {
            "mesh": {
                nid: {
                    "vector": [
                        n.vector.pace,
                        n.vector.rate,
                        n.vector.state,
                        n.vector.spin,
                    ],
                    "memory": n.memory,
                    "connections": n.connections,
                    "resonance": n.resonance,
                }
                for nid, n in self.mesh.items()
            },
            "registers": {
                reg: [v.pace, v.rate, v.state, v.spin]
                for reg, v in self.registers.items()
            },
            "spiral_depth": self.spiral_depth,
            "resonance_log": self.resonance_log[-100:],
            "memory": self.memory.replay(),
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def meshkeeper_repair(self) -> None:
        for node in self.mesh.values():
            node.vector.rotate_by_phi()
        self.meta_agent.health = min(100, self.meta_agent.health + 10)
        self.meta_agent.entropy = max(0, self.meta_agent.entropy - 10)

    def _calculate_resonance(self, a: RegisterVector, b: RegisterVector) -> float:
        return calculate_resonance(a, b)

    def _calculate_mesh_resonance(self) -> float:
        return mesh_resonance(self.mesh)

    def _spiral_audit(self) -> None:
        mesh_res = self._calculate_mesh_resonance()
        if mesh_res < PHI_INV:
            self.error_mansion.append(
                {
                    "type": "resonance_collapse",
                    "vector": self.registers["A"],
                    "resonance": mesh_res,
                    "lesson": "Resonance below φ⁻¹ threshold",
                }
            )
            self.handler.handle(self.error_mansion[-1])
            if len(self.error_mansion) >= 5:
                self.handler.suggest_bloom_patch()
                self._op_bloom({})
