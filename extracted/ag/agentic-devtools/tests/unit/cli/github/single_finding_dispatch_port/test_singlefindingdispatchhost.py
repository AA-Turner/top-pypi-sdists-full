from agentic_devtools.cli.github.single_finding_dispatch_port import SingleFindingDispatchHost


def test_protocol_exposes_full_reservation_create_persist_lifecycle() -> None:
    assert callable(SingleFindingDispatchHost.reserve_branch_write)
    assert callable(SingleFindingDispatchHost.release_branch_write)
    assert callable(SingleFindingDispatchHost.create_task_if_head)
    assert callable(SingleFindingDispatchHost.persist_acceptance)
