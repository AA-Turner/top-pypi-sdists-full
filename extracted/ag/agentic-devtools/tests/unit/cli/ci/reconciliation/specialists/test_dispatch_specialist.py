from unittest.mock import Mock

from agentic_devtools.cli.ci.reconciliation.specialists import SpecialistProfile, SpecialistRole, dispatch_specialist


def test_dispatch_specialist_delegates_model_and_footprint() -> None:
    controller = Mock()
    controller.request_worker_admission.return_value = (Mock(), Mock())
    profile = SpecialistProfile(SpecialistRole.CODE_REPAIR, file_footprint=("src/a.py",))
    state, task = dispatch_specialist(
        controller,
        Mock(),
        profile=profile,
        request_id="request",
        pr_number=1,
        obligation_id="obligation",
        batch_id="batch",
        worker_id="worker",
    )
    assert state is controller.request_worker_admission.return_value[0]
    assert task.profile == profile
    controller.request_worker_admission.assert_called_once()
    with __import__("pytest").raises(TypeError):
        dispatch_specialist(
            controller,
            Mock(),
            profile=None,  # type: ignore[arg-type]
            request_id="r",
            pr_number=1,
            obligation_id="o",
            batch_id="b",
            worker_id="w",
        )
