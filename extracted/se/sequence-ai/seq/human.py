"""
`seq.ask_human(reason=..., hold=...)`, what a policy's `@seq.plan` returns to hand its robot to a person, and
`seq.planner(...)`, which is gone: planning is a `@seq.plan` method of the policy itself.
"""
from __future__ import annotations

from typing import Any

from seq.errors import PolicyDefinitionError


def planner(*args: Any, **kwargs: Any) -> Any:
    """`@seq.planner` is gone: planning is part of the policy now (sequence_base.contract.planner.PLANNERS_GONE, the
    one sentence the platform says too)."""
    from sequence_base.contract.planner import PLANNERS_GONE

    raise PolicyDefinitionError(PLANNERS_GONE)




ASK_HUMAN = "ask_human"

REASON_MOST = 500


def ask_human(reason: str, *, hold: bool = True) -> dict:
    """What a policy's `@seq.plan` returns for a robot it hands to a person - `return seq.ask_human(reason="...")` - in
    place of a plan: the robot joins its help queue, and each operator watching it hears it from `op.requests()` (the
    robot, the reason, its newest frame) until one takes it (`op.take()`). With hold (the default) the robot stops until
    then; hold=False lets its model drive on while it waits. A plan that asks again for the same robot updates its
    reason.

        @seq.plan(every_s=2.0)
        def plan_user(self, robot):
            if bin_full_user(robot.state):
                return seq.ask_human(reason="the bin is full")

    WHY a mark, not a call: a plan only returns what it says its robot gets; the platform hands a marked one to the
    robot's worker, which queues it for its operators.
"""
    if not isinstance(reason, str) or not reason.strip():
        raise ValueError("seq.ask_human(reason=...) says why in a sentence its operator reads, e.g. "
                         'seq.ask_human(reason="the bin is full")')
    if len(reason.strip()) > REASON_MOST:
        raise ValueError(f"seq.ask_human's reason is at most {REASON_MOST} characters; it had {len(reason.strip())}")
    if not isinstance(hold, bool):
        raise ValueError("seq.ask_human(hold=...) is True - the robot stops until a person takes it - or False - its "
                         "model drives on meanwhile")
    return {"__seq__": ASK_HUMAN, "reason": reason.strip(), "hold": hold}
