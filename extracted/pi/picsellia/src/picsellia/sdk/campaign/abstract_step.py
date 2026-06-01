import abc
import logging
from typing import ClassVar
from uuid import UUID

from beartype import beartype
from orjson import orjson

from picsellia.decorators import exception_handler
from picsellia.sdk.dao import Dao
from picsellia.sdk.user import User
from picsellia.sdk.worker import Worker
from picsellia.services.campaign import parse_user_weights_to_assignees
from picsellia.types.enums import CampaignStepType
from picsellia.types.schemas import CampaignStepSchema
from picsellia.utils import filter_payload

logger = logging.getLogger("picsellia")


class AbstractCampaignStep(Dao):
    _base_path: ClassVar[str]

    @property
    @abc.abstractmethod
    def campaign_id(self) -> UUID:
        pass

    @property
    def name(self) -> str:
        """Name of the step"""
        return self._name

    @property
    def order(self) -> int:
        """Order of the step"""
        return self._order

    @property
    def type(self) -> CampaignStepType:
        """Type of the step"""
        return self._type

    @exception_handler
    @beartype
    def refresh(self, data: dict):
        schema = CampaignStepSchema(**data)
        self._name = schema.name
        self._order = schema.order
        self._type = schema.type
        return schema

    @exception_handler
    @beartype
    def sync(self) -> dict:
        r = self.connection.get(f"{self._base_path}/{self.id}").json()
        self.refresh(r)
        return r

    @exception_handler
    @beartype
    def update(
        self,
        name: str | None = None,
        assignees: list[tuple[User | UUID | Worker, float | int]] | None = None,
        sample_rate: float | None = None,
    ) -> None:
        """Update this campaign step parameters.

        `assignees` changed signature in 6.24, we now except a User or a user UUID.
        Worker will still be accepted until 6.26

        Examples:
            ```python
            foo_step.update(name="another-name")
            ```

        Arguments:
            name (str, optional): name of the step. Defaults to None.
            assignees (list of tuple of (User or UUID), float, optional): Can be used to assign users to this step.
                Defaults to None.
            sample_rate (float, optional): sample rate of  this step. Defaults to None.
        """
        payload = {"name": name, "sample_rate": sample_rate}
        if assignees:
            payload["assignees"] = parse_user_weights_to_assignees(assignees)

        filtered_payload = filter_payload(payload)
        r = self.connection.patch(
            f"{self._base_path}/{self.id}",
            data=orjson.dumps(filtered_payload),
        ).json()
        self.refresh(r)
        logger.info(f"{self} updated")

    @exception_handler
    @beartype
    def redistribute_assignments(self) -> None:
        """Distribute again all the assignments to the step assignees according to weights settings previously defined.
        Useful if you add workers to this step and want them to have as many tasks as the others.
        """
        self.connection.post(f"{self._base_path}/{self.id}/assignments/redistribute")
        logger.info(f"{self} assignments have been redistributed")

    @exception_handler
    @beartype
    def delete(self, pending_assignments_destination_step_id: UUID | str) -> None:
        """Delete this step from the campaign.
        It will move all assignments from this step to given destination step id.

        :warning: **DANGER ZONE**: Be very careful here!

        Arguments:
            pending_assignments_destination_step_id (str or UUID): step on which deleted step assignments will be moved.
        """
        payload = {
            "destination_step_id_for_pending_assignments": pending_assignments_destination_step_id
        }
        self.connection.delete(
            f"{self._base_path}/{self.id}", data=orjson.dumps(payload)
        )
        logger.info(
            f"Assignments of {self} have been moved to {pending_assignments_destination_step_id}."
        )
        logger.info(f"{self} have been deleted.")
