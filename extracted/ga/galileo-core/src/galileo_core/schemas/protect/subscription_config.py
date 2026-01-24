from functools import cached_property
from itertools import chain
from typing import List

from pydantic import BaseModel, Field, field_validator
from pydantic_core import Url

from galileo_core.helpers.logger import get_logger
from galileo_core.schemas.protect.execution_status import ExecutionStatus

logger = get_logger()


class SubscriptionConfig(BaseModel):
    statuses: List[ExecutionStatus] = Field(
        description="List of statuses that will cause a notification to be sent to the configured URL.",
        default=[ExecutionStatus.triggered],
    )
    url: Url = Field(
        description="URL to send the event to. This can be a webhook URL, a message queue URL, an event bus or "
        "a custom endpoint that can receive an HTTP POST request."
    )

    @cached_property
    def possible_statuses(self) -> List[str]:
        """
        List of possible statuses that will trigger a notification to be sent.

        This is a list of the cased and uncased versions of the statuses in the `statuses` list.

        Returns
        -------
        List[str]
            _description_
        """
        return list(chain.from_iterable([status, status.lower(), status.upper()] for status in self.statuses))

    @field_validator("statuses", mode="before")
    def warn_if_paused(cls, statuses: List[ExecutionStatus]) -> List[ExecutionStatus]:
        if ExecutionStatus.paused in statuses:
            logger.warning(
                "Only stages can have a `paused` status, rulesets cannot. The 'paused' status will be ignored."
            )
        return statuses
