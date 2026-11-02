from agentic_devtools.cli.ci.dispatch_state import DispatchState


def test_dispatchstate_exposes_closed_state_vocabulary() -> None:
    assert {state.value for state in DispatchState} == {
        "intent",
        "reserved",
        "creating",
        "created",
        "linked",
        "succeeded",
        "needs_reconciliation",
        "abandoned",
        "aborted_after_final_dispatch",
    }
