from enum import Enum
from random import choice
from typing import List, Literal, Sequence, Union

from pydantic import BaseModel, Field
from typing_extensions import Annotated

from galileo_core.schemas.protect.subscription_config import SubscriptionConfig


class ActionType(str, Enum):
    OVERRIDE = "OVERRIDE"
    PASSTHROUGH = "PASSTHROUGH"


class ActionResult(BaseModel):
    type: ActionType = Field(description="Type of action that was taken.")
    value: str = Field(description="Value of the action that was taken.")


class BaseAction(BaseModel):
    type: ActionType = Field(description="Type of action to take.")
    subscriptions: List[SubscriptionConfig] = Field(
        default_factory=list,
        description="List of subscriptions to send a notification to when this action is applied and the ruleset status matches any of the configured statuses.",
    )

    def apply(self, response: str) -> ActionResult:
        raise NotImplementedError


class OverrideAction(BaseAction):
    type: Literal[ActionType.OVERRIDE] = ActionType.OVERRIDE
    choices: Sequence[str] = Field(
        description="List of choices to override the response with. If there are multiple choices, one will be chosen at random when applying this action.",
        min_length=1,
    )

    def apply(self, response: str) -> ActionResult:
        return ActionResult(type=self.type, value=choice(self.choices))


class PassthroughAction(BaseAction):
    type: Literal[ActionType.PASSTHROUGH] = ActionType.PASSTHROUGH

    def apply(self, response: str) -> ActionResult:
        return ActionResult(type=self.type, value=response)


Action = Annotated[Union[OverrideAction, PassthroughAction], Field(discriminator="type")]
