from collections.abc import Mapping, Sequence

from mistralai.workflows.exceptions import ErrorCode, WorkflowsException
from mistralai.workflows.models import WorkflowSpecWithTaskQueue
from mistralai.workflows.protocol.v1.workflow import WorkflowRegistrationRef

_worker_registrations: dict[str, WorkflowRegistrationRef] = {}


def build_worker_registrations(
    workflow_definitions: Sequence[WorkflowSpecWithTaskQueue],
    registration_refs: Sequence[WorkflowRegistrationRef],
) -> dict[str, WorkflowRegistrationRef]:
    """Zip the specs a worker submitted with the refs the API returned for them.

    The API returns refs in submission order, so a length mismatch means the pairing
    would be wrong.
    """
    if len(workflow_definitions) != len(registration_refs):
        raise WorkflowsException(
            code=ErrorCode.WORKER_REGISTRATION_ERROR,
            message=(
                f"Registration returned {len(registration_refs)} refs for "
                f"{len(workflow_definitions)} submitted workflow definitions"
            ),
        )
    return {spec.name: ref for spec, ref in zip(workflow_definitions, registration_refs)}


def set_worker_registrations(registrations: Mapping[str, WorkflowRegistrationRef]) -> None:
    _worker_registrations.clear()
    _worker_registrations.update(registrations)


def get_workflow_registration_ref(workflow_name: str) -> WorkflowRegistrationRef | None:
    """Return the registration this worker obtained for `workflow_name`.

    Workers register their workflow definitions at startup and refresh them from the
    heartbeat loop, so activities can read the resulting ids from process memory.

    Returns None outside a running worker, or for a workflow this worker does not host.
    """
    return _worker_registrations.get(workflow_name)


def get_registered_workflow_names() -> list[str]:
    return sorted(_worker_registrations)
