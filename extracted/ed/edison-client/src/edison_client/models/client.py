from typing import Any, Generic, TypeAlias, TypeVar

from aviary.message import Message
from aviary.tools.base import Tool
from ldp.agent import Agent
from ldp.data_structures import Transition
from ldp.graph.ops import OpResult
from pydantic import BaseModel, ConfigDict, Field, SerializationInfo, field_serializer

from .app import Step

T = TypeVar("T")


# TODO: [PLA-1155] revisit this
# unsure what crow states will return
# need to revisit after we get more crows deployed
class BaseState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, extra="allow")


class BeforeTransitionState(BaseState):
    current_state: Any = Field()
    observations: list[Message] = Field()


class InitialState(BaseState):
    initial_state: Any = Field()


class ASVState(BaseState, Generic[T]):
    action: OpResult[T] = Field()
    next_state: Any = Field()
    value: float = Field()

    @field_serializer("action")
    def serialize_action(self, action: OpResult[T]) -> dict:  # noqa: PLR6301
        return action.to_dict()


class EnvResetState(BaseState):
    observations: list[Message] = Field()
    tools: list[Tool] = Field()


class EnvStepState(BaseState):
    observations: list[Message] = Field()
    reward: float = Field()
    done: bool = Field()
    trunc: bool = Field()


class TransitionState(BaseState):
    transition: Transition = Field()

    @field_serializer("transition")
    def serialize_transition(  # noqa: PLR6301
        self, transition: Transition, info: SerializationInfo
    ) -> dict:
        # Forward caller's serialization settings — the field_serializer
        # intercepts Pydantic's default nested serialization, so mode, aliases,
        # and context (notably include_info for Message.info metadata) must be
        # propagated explicitly.
        # Exclude action because OpResult is not Pydantic-serializable in
        # json mode — we serialize it manually via .to_dict() below.
        transition_data = transition.model_dump(
            mode=info.mode,
            by_alias=info.by_alias,
            context=info.context,
            exclude={"action"},
        )
        return transition_data | {
            "action": transition.action.to_dict() if transition.action else None,
        }


class GlobalState(BaseState):
    agent: Agent | None = None
    env: Any | None = None
    agent_state: Any | None = None
    next_agent_state: Any | None = None
    observations: list = []
    action: Any | None = None
    value: float = 0.0
    last_step_state: Transition | None = None

    def update_observations(self, obs: list[Message]) -> list[Message]:
        previous_observations = self.observations or []
        self.observations = obs
        return previous_observations

    def store_step_state(self, step_state: Transition) -> None:
        self.last_step_state = step_state

    def update_trajectory_data(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _get_safe_previous_observations(
        self, current_obs: list[Message] | None = None
    ) -> list[Message]:
        if self.last_step_state and self.last_step_state.next_observation:
            return self.last_step_state.next_observation
        if self.observations:
            return self.observations
        return current_obs or []

    def create_step_state(self, callback_type: Step, **kwargs) -> Transition:
        defaults = {
            "timestep": getattr(self.agent, "_timestep", 0) if self.agent else 0,
            "agent_state": self.agent_state,
            "next_agent_state": self.next_agent_state or self.agent_state,
            "observation": self._get_safe_previous_observations(),
            "next_observation": self.observations or [],
            "action": self.action,
            "reward": 0.0,
            "truncated": False,
            "done": False,
            "value": self.value or 0.0,
            "metadata": {"callback_type": callback_type},
        }

        for key, value in kwargs.items():
            if key == "metadata" and isinstance(value, dict):
                if isinstance(defaults["metadata"], dict):
                    defaults["metadata"].update(value)
            else:
                defaults[key] = value

        return Transition(**defaults)


StateType: TypeAlias = (
    BeforeTransitionState
    | InitialState
    | ASVState
    | EnvResetState
    | EnvStepState
    | TransitionState
    | GlobalState
)
