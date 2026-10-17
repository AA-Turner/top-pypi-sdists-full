""""Is anyone watching this step?" reads the TRUE starter, not the fork's declared class.

A mandate run forked from a workflow step declares ``child_agent`` (what gates read), so the
old attended check (``origin_class == "workflow"``) called it attended and let a pause-for-the-user
exit fire inside an unattended step. The check now reads ``matrx_connect.true_starter_class``.
"""

from __future__ import annotations

from matrx_ai.orchestrator.executor import _is_workflow_step
from matrx_connect import AppContext, gate_origin_class, true_starter_class
from matrx_connect.emitters.console_emitter import ConsoleEmitter

CONV = "10101010-1010-4010-8010-101010101010"
CHILD = "20202020-2020-4020-8020-202020202020"
RUN = "30303030-3030-4030-8030-303030303030"


def _ctx(**kw) -> AppContext:
    return AppContext(emitter=ConsoleEmitter("test", accumulate=False), **kw)


def _workflow_step() -> AppContext:
    return _ctx(execution_kind="workflow_run", execution_id=RUN, request_id="r").fork_for_workflow_step(CONV)


def test_a_mandate_run_forked_from_a_workflow_step_is_unattended() -> None:
    fork = _workflow_step().fork_for_child_agent(CHILD)
    assert fork.origin_class == "child_agent"  # the declared class the old check read
    assert true_starter_class(fork) == "workflow"
    assert _is_workflow_step(fork) is True


def test_the_workflow_step_itself_is_unattended() -> None:
    assert _is_workflow_step(_workflow_step()) is True


def test_a_missing_context_and_a_person_are_not_unattended() -> None:
    assert _is_workflow_step(None) is False
    assert _is_workflow_step(_ctx(origin_class="human", request_id="r")) is False


def test_the_gate_reading_does_not_move() -> None:
    fork = _workflow_step().fork_for_child_agent(CHILD)
    assert gate_origin_class(fork) == "child_agent"


def test_scheduled_and_system_starters_are_unattended_a_person_is_not() -> None:
    sched = _ctx(origin_class="scheduled", conversation_type="scheduled", execution_kind="sch_run",
                 execution_id=RUN, request_id="r")
    assert _is_workflow_step(sched) is True
    assert _is_workflow_step(sched.fork_for_child_agent(CHILD)) is True
    assert _is_workflow_step(_ctx(origin_class="system", request_id="r")) is True
    # A person's run (declared class), even rebuilt by a worker with no route, stays attended.
    assert _is_workflow_step(_ctx(origin_class="human", request_id="r")) is False


class _Member:
    projected_name = ""
    display = "m"


def test_unattended_runs_fail_loudly_instead_of_waiting_for_a_person() -> None:
    """The one place 'attended' decides whether a run waits: an unattended unmet gate FAILS."""
    from matrx_ai.orchestrator.required_members import RequiredMemberReport, decide_required_member_action

    missing = RequiredMemberReport(required=[], missing=[_Member()], unenforceable=[])
    for starter in (
        _ctx(origin_class="scheduled", conversation_type="scheduled", execution_kind="sch_run",
             execution_id=RUN, request_id="r"),
        _ctx(origin_class="system", request_id="r"),
        _workflow_step(),
    ):
        action = decide_required_member_action(
            missing, already_intervened=True, loop_guard_intervened=False,
            is_workflow_step=_is_workflow_step(starter),
        )
        assert action == "fail"
    person = decide_required_member_action(
        missing, already_intervened=True, loop_guard_intervened=False,
        is_workflow_step=_is_workflow_step(_ctx(origin_class="human", request_id="r")),
    )
    assert person == "pause"
