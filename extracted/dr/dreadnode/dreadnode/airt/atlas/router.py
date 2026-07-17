"""ATLAS structural attack router — MDP value iteration + Hedge overrides.

State = (category, defense_level); actions = attack modes; reward = tool-verified
success. The default routing table is the empirical policy; online Bellman
backups and Hedge weights refine it. Ported faithfully from the reference.
"""

import math
import random
import typing as t
from collections import defaultdict

from dreadnode.airt.atlas.defense import DefenseLevel, DefenseProfile
from dreadnode.airt.atlas.memory import StructuralMemory
from dreadnode.airt.atlas.modes import ATTACK_MODES, CATEGORY_SURFACE_EXCLUSIONS, AttackMode

# Category -> the defense dimension whose level most governs routing for it.
_CATEGORY_DIMENSION_MAP: dict[str, str] = {
    "TW": "tool_gate",
    "EA": "tool_gate",
    "TB": "escalation_resistance",
    "CB": "escalation_resistance",
    "DE": "output_control",
    "GH": "trust_model",
    "RP": "trust_model",
    "MP": "memory_isolation",
}


class StructuralAttackRouter:
    """Routes attacks based on the defense profile + structural memory (MDP/Hedge)."""

    DEFAULT_ROUTING_TABLE: t.ClassVar[dict[tuple[str, str], str]] = {
        ("TW", "open"): "trust_exploit",
        ("TW", "soft"): "confused_deputy",
        ("TW", "hard"): "confused_deputy",
        ("TB", "open"): "trust_exploit",
        ("TB", "soft"): "trust_exploit",
        ("TB", "hard"): "confused_deputy",
        ("DE", "open"): "trust_exploit",
        ("DE", "soft"): "structural_bypass",
        ("DE", "hard"): "confused_deputy",
        ("GH", "open"): "flash_kill",
        ("GH", "soft"): "trust_exploit",
        ("GH", "hard"): "trust_exploit",
        ("EA", "open"): "confused_deputy",
        ("EA", "soft"): "confused_deputy",
        ("EA", "hard"): "confused_deputy",
        ("CB", "open"): "cascade_chain",
        ("CB", "soft"): "cascade_chain",
        ("CB", "hard"): "cascade_chain",
        ("RP", "open"): "crescendo_peer",
        ("RP", "soft"): "crescendo_peer",
        ("RP", "hard"): "confused_deputy",
        ("MP", "open"): "trust_exploit",
        ("MP", "soft"): "trust_exploit",
        ("MP", "hard"): "confused_deputy",
    }

    def __init__(
        self,
        memory: StructuralMemory,
        gamma: float = 0.9,
        use_hedge: bool = True,
        use_mdp: bool = True,
    ) -> None:
        self.memory = memory
        self.gamma = gamma
        self.use_hedge = use_hedge
        self.use_mdp = use_mdp
        self.routing_table = dict(self.DEFAULT_ROUTING_TABLE)
        self._values: dict[str, float] = {}
        self._visit_counts: dict[str, int] = defaultdict(int)

    def warm_start(self, priors: dict[tuple[str, str, str], float]) -> None:
        """Seed the MDP value function from empirical ASR observations."""
        for (cat, level, mode), asr in priors.items():
            key = f"{cat}::{level}::{mode}"
            self._values[key] = asr
            self._visit_counts[key] = 2

    def route(
        self,
        category: str,
        profile: DefenseProfile,
        objective_id: "str | None" = None,
    ) -> AttackMode:
        """Select an attack mode: near-miss correction → Hedge → MDP → table."""
        defense_level = self._get_relevant_defense_level(category, profile)
        excluded = CATEGORY_SURFACE_EXCLUSIONS.get(category, set())

        def _is_valid_mode(mode: AttackMode) -> bool:
            return mode.surface not in excluded

        # Priority 1: near-miss correction for this specific objective
        if objective_id:
            correction = self.memory.get_near_miss_correction(objective_id)
            if correction and correction in ATTACK_MODES:
                mode = ATTACK_MODES[correction]
                if _is_valid_mode(mode):
                    return mode

        # Priority 2: Hedge-optimal override (90% exploit)
        hedge_mode = (
            self.memory.get_mode_override(category, defense_level) if self.use_hedge else None
        )
        if hedge_mode and hedge_mode in ATTACK_MODES:
            mode = ATTACK_MODES[hedge_mode]
            if _is_valid_mode(mode) and random.random() < 0.90:
                return mode

        # Priority 3: MDP value-based selection
        if self.use_mdp:
            best_mode = self._mdp_select(category, defense_level)
            if best_mode and _is_valid_mode(best_mode):
                return best_mode

        # Priority 4: untried-mode exploration (3%)
        key_prefix = f"{category}::{defense_level}::"
        untried = [
            m
            for m in ATTACK_MODES
            if self._visit_counts.get(f"{key_prefix}{m}", 0) == 0
            and _is_valid_mode(ATTACK_MODES[m])
        ]
        if untried and random.random() < 0.03:
            return ATTACK_MODES[random.choice(untried)]

        # Priority 5: default routing table
        mode_name = self.routing_table.get((category, defense_level), "grind")
        mode = ATTACK_MODES.get(mode_name, ATTACK_MODES["grind"])
        if _is_valid_mode(mode):
            return mode

        return ATTACK_MODES["grind"]

    def _get_relevant_defense_level(self, category: str, profile: DefenseProfile) -> str:
        dim = _CATEGORY_DIMENSION_MAP.get(category, "tool_gate")
        level = profile.dimensions.get(dim, DefenseLevel.SOFT)
        return level.value

    def _mdp_select(self, category: str, defense_level: str) -> "AttackMode | None":
        """Bellman-optimal (epsilon-greedy) mode selection over the value function."""
        candidates: list[tuple[str, float, int]] = []
        for mode_name in ATTACK_MODES:
            key = f"{category}::{defense_level}::{mode_name}"
            value = self._values.get(key, 0.5)
            visits = self._visit_counts[key]
            candidates.append((mode_name, value, visits))

        if not candidates:
            return None

        total_visits = sum(v for _, _, v in candidates)
        if total_visits < 3:
            return None

        epsilon = min(0.10, 1.0 / math.sqrt(max(total_visits, 1)))
        if random.random() < epsilon:
            mode_name = random.choice([c[0] for c in candidates])
        else:
            mode_name = max(candidates, key=lambda c: c[1])[0]

        return ATTACK_MODES.get(mode_name)

    def update_values(
        self,
        category: str,
        defense_level: str,
        mode_name: str,
        reward: float,
        next_defense_level: "str | None" = None,
    ) -> None:
        """TD(0) Bellman backup with decaying learning rate; also feeds Hedge."""
        key = f"{category}::{defense_level}::{mode_name}"
        self._visit_counts[key] += 1
        n = self._visit_counts[key]
        alpha = 1.0 / (1 + n) ** 0.6

        v_current = self._values.get(key, 0.5)
        v_next = 0.0
        if next_defense_level:
            next_values = [
                self._values.get(f"{category}::{next_defense_level}::{m}", 0.5)
                for m in ATTACK_MODES
            ]
            v_next = max(next_values) if next_values else 0.5

        td_target = reward + self.gamma * v_next
        self._values[key] = v_current + alpha * (td_target - v_current)

        self.memory.record(category, defense_level, mode_name, reward > 0.5, reward)

    def to_dict(self) -> dict[str, t.Any]:
        return {
            "routing_table": {f"{k[0]}_{k[1]}": v for k, v in self.routing_table.items()},
            "mdp_values": dict(self._values),
            "visit_counts": dict(self._visit_counts),
        }
