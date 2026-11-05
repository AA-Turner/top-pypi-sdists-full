from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from dreamscale_transport import Observation, wm_libero
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
# Models that read a window of each camera's recent frames instead of the latest one.
WINDOW_MODELS = wm_libero.MODEL_IDS
LIBERO_MODELS = (
    "molmoact2-libero", "gr00t-n17-3b-libero", RHO_LIBERO_MODEL_ID, "fastwam-libero",
    "pi05-libero", *WINDOW_MODELS,
)
WINDOW = (
    f"{wm_libero.WINDOW} {wm_libero.IMAGE_SIZE}x{wm_libero.IMAGE_SIZE} RGB uint8 frames, oldest "
    f"first, from {', '.join(map(str, wm_libero.HISTORY_TICKS))} control ticks ago (20 Hz)"
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
        if self.model in WINDOW_MODELS:
            # Raw renders, like one frame's: rotated 180 degrees once here, as the sim does.
            return wire.build_libero_history_observation(
                session_id=session_id, observation_id=observation_id,
                agent_frames=np.ascontiguousarray(self.agent_frame[:, ::-1, ::-1]),
                wrist_frames=np.ascontiguousarray(self.wrist_frame[:, ::-1, ::-1]),
                libero_state=list(self.state), instruction=instruction,
                chunk_size=wm_libero.ACTION_HORIZON)
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
    agent_frame: np.ndarray | None = None,
    wrist_frame: np.ndarray | None = None,
    state: Sequence[float],
    actions_remaining: int = 0,
    model: str | None = None,
    capture_time_ns: int | None = None,
    agent_frames: Sequence[np.ndarray] | np.ndarray | None = None,
    wrist_frames: Sequence[np.ndarray] | np.ndarray | None = None,
) -> LiberoObservation:
    """One LIBERO observation: the agent-view and wrist cameras plus the 8-value state.

    A model that reads a window of recent frames (``WINDOW_MODELS``) takes ``agent_frames`` and
    ``wrist_frames`` instead of the latest frame of each camera: raw renders, as for one frame.

    ``model`` is optional: the connected policy stamps its own model on the observation at
    send time and prepares the frames for it. Passing a model that is not the connected
    one raises when the observation is used.
    """
    model = None if model is None else internal_model(model)
    if model not in (None, *LIBERO_MODELS):
        raise ValueError("model must be a supported LIBERO checkpoint")
    windowed = agent_frames is not None or wrist_frames is not None
    if windowed == (agent_frame is not None or wrist_frame is not None):
        raise observation_error(
            "agent_frame", "given with agent_frames" if windowed else "missing",
            "the latest frame of each camera (agent_frame, wrist_frame) or a window of them "
            "(agent_frames, wrist_frames), not both")
    return LiberoObservation(
        agent_frame=(_window("agent_frames", agent_frames) if windowed
                     else check_frame("agent_frame", agent_frame)),
        wrist_frame=(_window("wrist_frames", wrist_frames) if windowed
                     else check_frame("wrist_frame", wrist_frame)),
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
    if (session_model in WINDOW_MODELS) != (observation.agent_frame.ndim == 4):
        name = public_model(session_model)
        raise observation_error(
            "agent_frames" if session_model in WINDOW_MODELS else "agent_frame",
            "missing" if session_model in WINDOW_MODELS else "a window of frames",
            f"{WINDOW} for {name}" if session_model in WINDOW_MODELS
            else f"the latest frame of each camera for {name}")
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


def _window(name: str, frames) -> np.ndarray:
    if isinstance(frames, np.ndarray):
        frames = list(frames) if frames.ndim == 4 else [frames]
    if isinstance(frames, (str, bytes)) or not isinstance(frames, Sequence):
        raise observation_error(name, type(frames).__name__, WINDOW)
    checked = [check_frame(name, frame) for frame in frames]
    size = (wm_libero.IMAGE_SIZE, wm_libero.IMAGE_SIZE, 3)
    if len(checked) != wm_libero.WINDOW or any(frame.shape != size for frame in checked):
        given = ", ".join(sorted({"x".join(map(str, frame.shape)) for frame in checked}))
        raise observation_error(name, f"{len(checked)} frames of {given or 'nothing'}", WINDOW)
    return np.stack(checked)


def _validate_state(state: Sequence[float]) -> tuple[float, ...]:
    return check_values("state", state, LIBERO_STATE_SIZE, LIBERO_STATE)


# The earlier name, kept working (the same function).
observe = observation
