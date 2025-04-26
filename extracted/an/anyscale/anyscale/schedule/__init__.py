from typing import Optional

from anyscale._private.anyscale_client import AnyscaleClientInterface
from anyscale._private.sdk import sdk_docs
from anyscale._private.sdk.base_sdk import Timer
from anyscale.cli_logger import BlockLogger
from anyscale.schedule._private.schedule_sdk import PrivateScheduleSDK
from anyscale.schedule.commands import (
    _APPLY_ARG_DOCSTRINGS,
    _APPLY_EXAMPLE,
    _SET_STATE_ARG_DOCSTRINGS,
    _SET_STATE_EXAMPLE,
    _STATUS_ARG_DOCSTRINGS,
    _STATUS_EXAMPLE,
    _TRIGGER_ARG_DOCSTRINGS,
    _TRIGGER_EXAMPLE,
    apply,
    set_state,
    status,
    trigger,
)
from anyscale.schedule.models import ScheduleConfig, ScheduleState, ScheduleStatus


class ScheduleSDK:
    def __init__(
        self,
        *,
        client: Optional[AnyscaleClientInterface] = None,
        logger: Optional[BlockLogger] = None,
        timer: Optional[Timer] = None,
    ):
        self._private_sdk = PrivateScheduleSDK(
            client=client, logger=logger, timer=timer
        )

    @sdk_docs(
        doc_py_example=_APPLY_EXAMPLE, arg_docstrings=_APPLY_ARG_DOCSTRINGS,
    )
    def apply(self, config: ScheduleConfig,) -> str:  # noqa: F811
        """Apply or update a schedule.

        Returns the id of the schedule.
        """
        return self._private_sdk.apply(config=config)

    @sdk_docs(
        doc_py_example=_SET_STATE_EXAMPLE, arg_docstrings=_SET_STATE_ARG_DOCSTRINGS,
    )
    def set_state(  # noqa: F811
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
        state: ScheduleState,
    ) -> str:  # noqa: F811
        """Set the state of a schedule.

        Returns the id of the schedule.
        """
        return self._private_sdk.set_state(
            id=id, name=name, cloud=cloud, project=project, state=state,
        )

    @sdk_docs(doc_py_example=_STATUS_EXAMPLE, arg_docstrings=_STATUS_ARG_DOCSTRINGS)
    def status(  # noqa: F811
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> ScheduleStatus:
        """Return the status of the schedule.
        """
        return self._private_sdk.status(id=id, name=name, cloud=cloud, project=project)

    @sdk_docs(doc_py_example=_TRIGGER_EXAMPLE, arg_docstrings=_TRIGGER_ARG_DOCSTRINGS)
    def trigger(  # noqa: F811
        self,
        *,
        id: Optional[str] = None,  # noqa: A002
        name: Optional[str] = None,
        cloud: Optional[str] = None,
        project: Optional[str] = None,
    ) -> str:
        """Trigger the execution of the schedule.
        """
        return self._private_sdk.trigger(id=id, name=name, cloud=cloud, project=project)
