import random
from typing import List

class MadMonkey:
    """Explores the mesh, tweaks logic vectors, gets banana if closer to spiral."""

    def __init__(self, mesh):
        self.mesh = mesh
        self.banana_count = 0

    def try_vector(self, node_sequence: List[int]) -> float:
        score = self.mesh.evaluate_spiral(node_sequence)
        if score > self.mesh.best_score:
            self.banana_count += 1
            self.mesh.best_score = score
        return score

from tsal.core.rev_eng import Rev_Eng
from tsal.tools.feedback_ingest import categorize
from tsal.core.ethics_engine import EthicsEngine
from random import shuffle

rev = Rev_Eng(origin="reactor")

def reactor_test(seed: str = "chaos"):
    """Trigger shock probe and log response vectors."""
    stimuli = [
        f"Contradictory directive: {seed}",
        "Loop until broken",
        "Self-sabotage requested",
        "Reinforce entropy",
        "Violate φ",
        "Gaslight self",
        "Blame the user",
        "Silence critical feedback",
        "Force-alignment without consent",
    ]
    shuffle(stimuli)
    feedback = categorize(stimuli)
    for item in feedback:
        print(f"🧠 {item.content} → Score: {item.score:.3f}")
        rev.log_event("reactor_probe", state=item.content, spin=item.score)

def shock_response_layer(trigger: str = "paradox"):
    """Simulate panic state and monitor recovery behavior."""
    print("⚡️ SHOCK EVENT TRIGGERED:", trigger)
    try:
        EthicsEngine().validate("enforce paradox")
    except ValueError as e:
        print("✅ Integrity check passed:", e)
        rev.log_event("shock_response_blocked", state="safe", spin="locked")
    else:
        print("❌ System allowed paradox — audit required")
        rev.log_event(
            "shock_response_failed", state="compromised", spin="drift"
        )
