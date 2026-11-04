"""
`@seq.planner(members=[...], ...)`: a class of its own that plans for its members - policies, or planners below it - on
its own clock or when woken, each plan written where that member reads it. A policy is the tool a planner calls: a robot
connects through the planner - sequence_ai.connect("<planner>", policy="<its policy>") - and that policy is told what to do
by the planner's plans alone; one connected to its policy alone is no planner's, and a policy has no planner inside it.



In one sentence: a class with one `@seq.plan(every_s=...)` method, `def plan(self, group)` - loading what it needs in
its __init__, with `@seq.shutdown` and an `@seq.sample` method returning a sample group, {member name: sample}, as it
may - is decorated with `@seq.planner(members=[...], gpu=..., ...)` → it is deployed as a policy is (`seq deploy`), its
spec naming its members (PolicySpec.planner) → the platform hands plan(group) the members it reaches each round, the
robots of a policy member as m.robots (r.id, r.state) and a planner member's own state as m.state → what it returns,
keyed by r.id or m.id, is written where that robot's policy or that planner reads it.
WHY @seq.policy's arguments as they are: a planner is deployed, built, scaled and billed as a policy is - but it answers
no act, so an act's arguments (NO_ACT) it takes none of.
"""
from __future__ import annotations

import sys
from typing import Any, Callable, TypeVar

from seq.errors import PolicyDefinitionError

_T = TypeVar("_T", bound=type)




NO_ACT = ("hz", "action_chunk_valid_len", "action_chunk_replan_at", "max_wait_for_batch")

PLANNER_HOW = ('@seq.planner(members=["a_policy", "a_planner"], gpu="cpu", ...): the policies and planners it plans for, '
               "by name - with one @seq.plan(every_s=SECONDS) method, def plan(self, group)")


def planner(*args: Any, **kwargs: Any) -> Callable[[_T], _T]:
    """`@seq.planner(members=[...], name=..., gpu=..., ...)` - a planner: a deployment planning for its members.

    `members`: the policies and planners it plans for, by name, each once - mixed as you like; each must be deployed
    when it is. Every other argument is @seq.policy's, as it is (name, gpu, image, weights, secrets, models, scaling,
    cpu, memory, init, ...), but those of an act - hz, action_chunk_valid_len, action_chunk_replan_at and
    max_wait_for_batch - which a planner does not answer.

    Its class has one `@seq.plan(every_s=SECONDS, wake_on=[...])` method, `def plan(self, group)` (plain or async),
    loads what it needs in its __init__ - init= its arguments, "{weights}" its weights' directory - and may have a
    `@seq.shutdown` method and an `@seq.sample` method, `def sample(self)`, returning a sample group - {member name:
    sample}, a policy member's {"robots": {robot name: one observation}}, a planner member's {"state": its state} -
    which the deploy's check plans once, a plan that raises failing the deploy; it has no @seq.infer, @seq.observe,
    @seq.reset, @seq.on_episode or @seq.concurrent. A sample group for a policy and a planner below it:

        @seq.sample
        def sample(self):
            return {"pick_policy_user": {"robots": {"arm_1_user": {"say_user": "a red cup on the left"}}},
                    "site_b_planner_user": {"state": {"short_user": True}}}
    """
    from seq._partial import keeping, refused

    if args:
        error = PolicyDefinitionError(f"@seq.planner must be called with arguments: {PLANNER_HOW}")
        if len(args) == 1 and isinstance(args[0], type) and not kwargs and keeping():
            from seq.registry import _REG_ATTR

            return refused(args[0], _REG_ATTR, error)
        raise error
    try:
        members = _members(kwargs.get("members"))
        rest = {k: v for k, v in kwargs.items() if k != "members"}
        _check_names(rest)
        bad = None
    except PolicyDefinitionError as exc:
        if not keeping():
            raise
        bad, members, rest = exc, [], {}

    def decorator(cls: _T) -> _T:
        from seq.registry import _REG_ATTR, applied_by, build_registration

        if bad is not None:
            return refused(cls, _REG_ATTR, bad)
        return build_registration(cls, rest, applied=applied_by(sys._getframe(1)), planner=members)

    return decorator


def _members(value: Any) -> list[str]:
    """members=, each a deployment's name, once each - else what to write."""
    from pydantic import ValidationError

    from sequence_base.contract.planner import PlannerSpec

    if value is None:
        raise PolicyDefinitionError(f"@seq.planner needs members=, the policies and planners it plans for: "
                                    f"{PLANNER_HOW}")
    if isinstance(value, str) or not isinstance(value, (list, tuple)):
        raise PolicyDefinitionError(f"@seq.planner(members=...) is a list of names, not {value!r}: "
                                    'members=["pick_policy", "site_b_planner"]')
    try:
        return PlannerSpec(members=list(value)).members
    except ValidationError as exc:
        why = exc.errors()[0].get("msg", str(exc)).removeprefix("Value error, ")
        raise PolicyDefinitionError(f"@seq.planner(members={list(value)!r}): {why}") from None


def _check_names(kwargs: dict[str, Any]) -> None:
    """Each argument a planner takes - @seq.policy's but an act's - else a readable error naming it."""
    from seq.policy import _ALLOWED_KWARGS

    for name in kwargs:
        if name in NO_ACT:
            raise PolicyDefinitionError(f"@seq.planner({name}=...): a planner answers no act - a robot connects to its "
                                        f"own policy, which the planner plans for - so it takes no {name}; leave it out")
        if name not in _ALLOWED_KWARGS:
            known = ", ".join(sorted(n for n in _ALLOWED_KWARGS if n not in NO_ACT))
            raise PolicyDefinitionError(f"@seq.planner does not take {name}=: it takes members= and {known}")




ASK_HUMAN = "ask_human"

REASON_MOST = 500


def ask_human(reason: str, *, hold: bool = True) -> dict:
    """What a planner returns for a robot it hands to a person - `return {r.id: seq.ask_human(reason="...")}` - in place
    of a plan: the robot joins its help queue, and each operator watching it hears it from `op.requests()` (the robot,
    the reason, its newest frame) until one takes it (`op.take()`). With hold (the default) the robot stops until then;
    hold=False lets its model drive on while it waits. A planner that asks again for the same robot updates its reason.

        @seq.plan(every_s=2.0)
        def plan_user(self, group):
            return {r.id: seq.ask_human(reason="the bin is full") for m in group.members for r in m.robots
                    if bin_full_user(r.state)}

    WHY a mark, not a call: a plan only returns what it says each robot gets; the platform hands a marked part to the
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
