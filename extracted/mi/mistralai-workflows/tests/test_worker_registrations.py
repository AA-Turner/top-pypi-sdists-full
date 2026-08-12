from collections.abc import Iterator
from uuid import uuid4

import pytest

from mistralai.workflows.core.worker_registrations import (
    build_worker_registrations,
    get_registered_workflow_names,
    get_workflow_registration_ref,
    set_worker_registrations,
)
from mistralai.workflows.exceptions import WorkflowsException
from mistralai.workflows.models import WorkflowSpecWithTaskQueue
from mistralai.workflows.protocol.v1.workflow import WorkflowRegistrationRef


def _make_spec(name: str) -> WorkflowSpecWithTaskQueue:
    return WorkflowSpecWithTaskQueue(name=name, description=name, input_schema={}, task_queue="tq")


def _make_ref() -> WorkflowRegistrationRef:
    return WorkflowRegistrationRef(workflow_id=uuid4(), workflow_registration_id=uuid4())


@pytest.fixture(autouse=True)
def _clean_registrations() -> Iterator[None]:
    set_worker_registrations({})
    yield
    set_worker_registrations({})


class TestBuildWorkerRegistrations:
    def test_pairs_specs_with_refs_in_submission_order(self) -> None:
        specs = [_make_spec("alpha"), _make_spec("beta")]
        refs = [_make_ref(), _make_ref()]

        result = build_worker_registrations(specs, refs)

        assert result == {"alpha": refs[0], "beta": refs[1]}

    @pytest.mark.parametrize("ref_count", [0, 1, 3])
    def test_raises_when_counts_disagree(self, ref_count: int) -> None:
        specs = [_make_spec("alpha"), _make_spec("beta")]
        refs = [_make_ref() for _ in range(ref_count)]

        with pytest.raises(WorkflowsException, match=f"Registration returned {ref_count} refs for 2"):
            build_worker_registrations(specs, refs)


class TestWorkerRegistrationLookup:
    def test_returns_none_when_no_worker_is_running(self) -> None:
        assert get_workflow_registration_ref("alpha") is None

    def test_returns_ref_for_hosted_workflow(self) -> None:
        ref = _make_ref()
        set_worker_registrations({"alpha": ref})

        assert get_workflow_registration_ref("alpha") == ref

    def test_returns_none_for_workflow_the_worker_does_not_host(self) -> None:
        set_worker_registrations({"alpha": _make_ref()})

        assert get_workflow_registration_ref("beta") is None

    def test_set_replaces_previous_registrations(self) -> None:
        set_worker_registrations({"alpha": _make_ref()})
        refreshed = _make_ref()

        set_worker_registrations({"beta": refreshed})

        assert get_workflow_registration_ref("alpha") is None
        assert get_workflow_registration_ref("beta") == refreshed

    def test_clear_drops_registrations_on_worker_shutdown(self) -> None:
        set_worker_registrations({"alpha": _make_ref()})

        set_worker_registrations({})

        assert get_registered_workflow_names() == []
