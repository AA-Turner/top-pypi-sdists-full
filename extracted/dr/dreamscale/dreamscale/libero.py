from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from dreamscale_transport import Observation
from dreamscale_transport.rho_checkpoints import RHO_CHECKPOINTS, RHO_LIBERO_MODEL_ID

from dreamscale import wire
from dreamscale.errors import observation_error
from dreamscale.model_names import internal_model, public_model
from dreamscale.observation_checks import (
    check_actions_remaining,
    check_capture_time_ns,
    check_frame,
    check_values,
)

LIBERO_STATE_SIZE = 8
LIBERO_STATE = (
    "end-effector position x, y, z in metres, orientation as an axis-angle vector in "
    "radians, then the two gripper finger positions"
)
LIBERO_MODELS = (
    "molmoact2-libero", "gr00t-n17-3b-libero", RHO_LIBERO_MODEL_ID, "fastwam-libero",
    "pi05-libero",
)


@dataclass(frozen=True)
class LiberoObservation:
    agent_frame: np.ndarray
    wrist_frame: np.ndarray
    state: tuple[float, ...]
    actions_remaining: int = 0
    model: str | None = None
    # time.time_ns() when the frames and state were read; None: when the request is built.
    capture_time_ns: int | None = None

    def to_wire(
        self,
        *,
        session_id: str,
        observation_id: int,
        instruction: str,
    ) -> Observation:
        return wire.build_libero_observation(
            session_id=session_id,
            observation_id=observation_id,
            agent_frame=self.agent_frame,
            wrist_frame=self.wrist_frame,
            libero_state=list(self.state),
            instruction=instruction,
            actions_remaining=self.actions_remaining,
            **({"image_size": RHO_CHECKPOINTS[self.model].wire_image_size,
                "chunk_size": RHO_CHECKPOINTS[self.model].action_horizon}
               if self.model == RHO_LIBERO_MODEL_ID else
               {"image_size": 256, "chunk_size": 16}
               if self.model == "gr00t-n17-3b-libero" else
               {"image_size": 256, "chunk_size": 20}
               if self.model in ("fastwam-libero", "pi05-libero") else {}),
        )


def observation(
    *,
    agent_frame: np.ndarray,
    wrist_frame: np.ndarray,
    state: Sequence[float],
    actions_remaining: int = 0,
    model: str | None = None,
    capture_time_ns: int | None = None,
) -> LiberoObservation:
    """One LIBERO observation: the agent-view and wrist cameras plus the 8-value state.

    ``model`` is optional: the connected policy stamps its own model on the observation at
    send time and prepares the frames for it. Passing a model that is not the connected
    one raises when the observation is used.
    """
    model = internal_model(model) if model else model
    model = None if model is None else internal_model(model)
    if model not in (None, *LIBERO_MODELS):
        raise ValueError("model must be a supported LIBERO checkpoint")
    return LiberoObservation(
        agent_frame=check_frame("agent_frame", agent_frame),
        wrist_frame=check_frame("wrist_frame", wrist_frame),
        state=_validate_state(state),
        actions_remaining=check_actions_remaining(actions_remaining),
        model=model,
        capture_time_ns=check_capture_time_ns(capture_time_ns),
    )


def stamped_for_model(observation: LiberoObservation, model: str) -> LiberoObservation:
    """The observation prepared for the connected ``model``: an unstamped one takes it; a
    matching ``model=`` (either name) passes through; a different one raises."""
    from dataclasses import replace

    session_model = internal_model(model)
    if session_model not in LIBERO_MODELS:
        return observation
    if observation.model is None:
        return replace(observation, model=session_model)
    if internal_model(observation.model) != session_model:
        raise observation_error(
            "observation",
            f"built for {public_model(observation.model)}",
            f"one for the connected model {public_model(session_model)} "
            "(omit model= in libero.observation)",
        )
    return observation


def _validate_state(state: Sequence[float]) -> tuple[float, ...]:
    return check_values("state", state, LIBERO_STATE_SIZE, LIBERO_STATE)


# The earlier name, kept working (the same function).
observe = observation
