"""Builders for dreamscale_transport wire types. ONLY this module constructs
transport Observations / decodes ActionChunks — transport drift lands here."""

from __future__ import annotations

import time
from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, replace
from typing import Any

import numpy as np
from dreamscale_transport import (
    BimanualEndEffectorState,
    BimanualRobotState,
    CameraFrame,
    Observation,
    ObservationFrame,
    RoboCasaRobotState,
    RobotState,
    RuntimeRequestContext,
)
from dreamscale_transport.images import (
    WireImage,
    encode_rgb_jpeg,
    prepare_policy_image,
    tile_frames,
)

from dreamscale.constants import (
    CAMERA_KEY_BIMANUAL_YAM_LEFT,
    CAMERA_KEY_BIMANUAL_YAM_RIGHT,
    CAMERA_KEY_BIMANUAL_YAM_TOP,
    CAMERA_KEY_DROID_EXTERIOR_1,
    CAMERA_KEY_DROID_EXTERIOR_2,
    CAMERA_KEY_DROID_WRIST,
    CAMERA_KEY_LIBERO_AGENT,
    CAMERA_KEY_LIBERO_WRIST,
    CAMERA_KEY_SO101,
    CAMERA_KEY_SO101_SIDE,
    CAMERA_KEY_SO101_WRIST,
    OBS_JPEG_QUALITY,
)

LIBERO_POLICY_IMAGE_SIZE = 224
_DREAMZERO_MAX_CAMERA_SKEW_NS = 50_000_000


def encode_jpeg(frame: np.ndarray, quality: int = OBS_JPEG_QUALITY) -> bytes:
    """Encode an RGB camera frame as JPEG bytes for worker-side PIL RGB decode."""
    return encode_rgb_jpeg(frame, quality=quality)


@dataclass(frozen=True)
class _Encoding:
    image: WireImage | None = None
    # Older frames per camera id (oldest first, already sized): tiled before this one.
    history: dict[str, list[np.ndarray]] | None = None
    # When set, frames are recorded here (sized) instead of being encoded.
    capture: dict[str, np.ndarray] | None = None
    # Capture keys of history frames already sent ahead (oldest first): each camera
    # sends only its newest frame and names these.
    history_keys: tuple[int, ...] | None = None
    # When set, frames are kept here raw (before the wire image) for the transport's
    # camera codec, which codes them itself (the hidden camera-codec mode).
    raw: dict[str, np.ndarray] | None = None


_ENCODING: ContextVar[_Encoding | None] = ContextVar("dreamscale_wire_encoding", default=None)


@contextmanager
def _encoding(**changes: object) -> Iterator[None]:
    token = _ENCODING.set(replace(_ENCODING.get() or _Encoding(), **changes))
    try:
        yield
    finally:
        _ENCODING.reset(token)


def wire_image(image: WireImage | None) -> Any:
    """Resize every camera in this scope to the model's wire image before encoding."""
    return _encoding(image=image)


@contextmanager
def raw_frames(enabled: bool = True) -> Iterator[None]:
    """Keep cameras raw for the transport's codec instead of resizing and encoding them."""
    if not enabled:
        yield
        return
    with _encoding(raw={}):
        yield


def _raw_frames() -> dict[str, np.ndarray] | None:
    encoding = _ENCODING.get()
    return None if encoding is None or not encoding.raw else dict(encoding.raw)


def history_frames(history: dict[str, list[np.ndarray]]) -> Any:
    """Send each camera as a strip: its older frames (oldest first), then this one."""
    return _encoding(history=history)


def history_keys(keys: tuple[int, ...]) -> Any:
    """Name history frames sent ahead (``send_history_frames``) instead of tiling them."""
    return _encoding(history_keys=tuple(keys), history=None)


def encoded_frames(observation: Any) -> dict[str, bytes]:
    """Each camera of an observation as it would be sent alone (sized, JPEG), by camera id."""
    encoding = _ENCODING.get() or _Encoding()
    quality = OBS_JPEG_QUALITY if encoding.image is None else encoding.image.quality
    with captured_frames() as frames:
        observation.to_wire(session_id="history", observation_id=0, instruction="history")
    return {camera: encode_jpeg(frame, quality) for camera, frame in frames.items()}


@contextmanager
def captured_frames() -> Iterator[dict[str, np.ndarray]]:
    """Record the (sized) frames an observation would send, without encoding them."""
    frames: dict[str, np.ndarray] = {}
    with _encoding(capture=frames, history=None, history_keys=None):
        yield frames


def _camera_frame(camera_id: str, frame: np.ndarray) -> tuple[CameraFrame, bytes]:
    """Encode one camera: the metadata-only wire CameraFrame + the JPEG bytes
    (carried separately in Observation.camera_payloads, keyed by camera_id)."""
    encoding = _ENCODING.get() or _Encoding()
    if encoding.raw is not None and encoding.capture is None:
        raw = np.ascontiguousarray(frame, dtype=np.uint8)
        encoding.raw[camera_id] = raw
        return CameraFrame(
            camera_id=camera_id,
            width=int(raw.shape[1]),
            height=int(raw.shape[0]),
            encoding="jpeg",  # the transport's codec sets the encoding it sends
            payload_bytes=0,
            raw_bytes=int(raw.nbytes),
        ), b""
    if encoding.image is not None:
        frame = encoding.image.apply(frame)
    frames, history_ns = 1, None
    if encoding.capture is not None:
        encoding.capture[camera_id] = frame
        payload = b""
    else:
        older = (encoding.history or {}).get(camera_id)
        if encoding.history_keys:
            history_ns = list(encoding.history_keys)
            frames = len(history_ns) + 1
        elif older:
            frame, frames = tile_frames([*older, frame]), len(older) + 1
        quality = OBS_JPEG_QUALITY if encoding.image is None else encoding.image.quality
        payload = encode_jpeg(frame, quality)
    return CameraFrame(
        camera_id=camera_id,
        width=int(frame.shape[1]),
        height=int(frame.shape[0]),
        encoding="jpeg",
        payload_bytes=len(payload),
        frames=frames,
        history_ns=history_ns,
    ), payload


def build_so101_observation(
    *,
    session_id: str,
    observation_id: int,
    joint_positions: list[float],
    instruction: str,
    actions_remaining: int,
    side_frame: np.ndarray | None = None,
    wrist_frame: np.ndarray | None = None,
    frame: np.ndarray | None = None,
    now_ns: int | None = None,
) -> Observation:
    now = time.time_ns() if now_ns is None else now_ns
    gripper = min(1.0, max(0.0, float(joint_positions[5]) / 100.0))
    if side_frame is None:
        side_frame = frame
    if side_frame is None:
        raise TypeError("side_frame is required")
    if wrist_frame is None:
        wrist_frame = frame if frame is not None else side_frame
    side_camera, side_payload = _camera_frame(CAMERA_KEY_SO101_SIDE, side_frame)
    wrist_camera, wrist_payload = _camera_frame(CAMERA_KEY_SO101_WRIST, wrist_frame)
    obs_frame = ObservationFrame(
        session_id=session_id,
        observation_id=observation_id,
        capture_time_ns=now,
        send_time_ns=now,
        cameras=[side_camera, wrist_camera],
        robot_state=RobotState(
            joint_positions=[float(v) for v in joint_positions],
            joint_velocities=[0.0] * 6,  # not read from the bus; policy ignores velocities
            gripper=gripper,
        ),
        actions_remaining=actions_remaining,
        instruction=instruction,
    )
    return Observation(
        frame=obs_frame,
        camera_payloads={
            CAMERA_KEY_SO101: side_payload,
            CAMERA_KEY_SO101_WRIST: wrist_payload,
        },
    )


def build_libero_observation(
    *,
    session_id: str,
    observation_id: int,
    agent_frame: np.ndarray,
    wrist_frame: np.ndarray,
    libero_state: list[float],
    instruction: str,
    actions_remaining: int = 0,
    now_ns: int | None = None,
    image_size: int = LIBERO_POLICY_IMAGE_SIZE,
    chunk_size: int | None = None,
) -> Observation:
    """Build a LIBERO observation from raw RGB sim frames.

    The builder applies the production image conversion: 180-degree rotation,
    letterbox to the checkpoint image size (224 by default), then RGB JPEG encoding.
    """
    now = time.time_ns() if now_ns is None else now_ns
    agent_image = prepare_policy_image(agent_frame, image_size)
    wrist_image = prepare_policy_image(wrist_frame, image_size)
    agent_camera, agent_payload = _camera_frame(CAMERA_KEY_LIBERO_AGENT, agent_image)
    wrist_camera, wrist_payload = _camera_frame(CAMERA_KEY_LIBERO_WRIST, wrist_image)
    obs_frame = ObservationFrame(
        session_id=session_id,
        observation_id=observation_id,
        capture_time_ns=now,
        send_time_ns=now,
        cameras=[agent_camera, wrist_camera],
        robot_state=RobotState(  # placeholder 6-dim state; LIBERO uses libero_state
            joint_positions=[0.0] * 6,
            joint_velocities=[0.0] * 6,
            gripper=0.0,
        ),
        actions_remaining=int(actions_remaining),
        instruction=instruction,
        libero_state=[float(v) for v in libero_state],
    )
    return Observation(
        frame=obs_frame,
        camera_payloads={
            CAMERA_KEY_LIBERO_AGENT: agent_payload,
            CAMERA_KEY_LIBERO_WRIST: wrist_payload,
        },
        **({"chunk_size": chunk_size} if chunk_size is not None else {}),
    )


def build_robocasa_observation(*, session_id: str, observation_id: int,
                              images: dict[str, np.ndarray], robot_state: dict,
                              robot_state_history: list[dict],
                              instruction: str, chunk_size: int = 16,
                              now_ns: int | None = None) -> Observation:
    """RoboCasa images already have the checkpoint's orientation and area resize."""
    from dreamscale_transport.robocasa import CAMERA_KEYS

    if set(images) != set(CAMERA_KEYS):
        raise ValueError("RoboCasa365 requires its three named cameras")
    cameras, payloads = [], {}
    for key in CAMERA_KEYS:
        image = images[key]
        if image.shape != (4, 256, 256, 3) or image.dtype != np.uint8:
            raise ValueError("RoboCasa365 requires four 256x256 RGB uint8 frames per camera")
        # A lossless horizontal strip keeps four aligned frames in each camera payload.
        # Both codecs preserve upstream pixels. Fast lossless WebP cuts upload
        # size by about a third; PNG remains compatible with Pillow without WebP.
        from io import BytesIO

        from PIL import Image, features

        packed = np.concatenate(list(image), axis=1)
        encoded = BytesIO()
        encoding = "webp" if features.check("webp") else "png"
        options = {"lossless": True, "method": 0} if encoding == "webp" else {"compress_level": 3}
        Image.fromarray(packed).save(encoded, format=encoding.upper(), **options)
        payload = encoded.getvalue()
        camera = CameraFrame(camera_id=key, width=1024, height=256, encoding=encoding,
                             payload_bytes=len(payload))
        cameras.append(camera)
        payloads[key] = payload
    now = time.time_ns() if now_ns is None else now_ns
    return Observation(frame=ObservationFrame(
        session_id=session_id, observation_id=observation_id,
        capture_time_ns=now, send_time_ns=now, cameras=cameras,
        robot_state=RoboCasaRobotState.model_validate(robot_state),
        robot_state_history=[RoboCasaRobotState.model_validate(state)
                             for state in robot_state_history],
        actions_remaining=0, instruction=instruction,
    ), camera_payloads=payloads, chunk_size=chunk_size)


def build_rldx_libero_observation(*, session_id: str, observation_id: int,
                                  agent_frames: np.ndarray, wrist_frames: np.ndarray,
                                  libero_state: list[float], instruction: str,
                                  chunk_size: int = 16, now_ns: int | None = None) -> Observation:
    """RLDX-1 LIBERO: four oriented 256px frames per camera as one JPEG strip each."""
    from dreamscale_transport.rldx import HISTORY_LENGTH, IMAGE_SIZE, LIBERO

    cameras, payloads = [], {}
    for key, frames in zip(LIBERO.camera_keys, (agent_frames, wrist_frames), strict=True):
        if frames.shape != (HISTORY_LENGTH, IMAGE_SIZE, IMAGE_SIZE, 3) or frames.dtype != np.uint8:
            raise ValueError("RLDX-1 LIBERO requires four 256x256 RGB uint8 frames per camera")
        # 256px frames tile JPEG's 16px blocks exactly, so frames never blur into each other.
        camera, payload = _camera_frame(key, np.ascontiguousarray(np.concatenate(frames, axis=1)))
        cameras.append(camera)
        payloads[key] = payload
    now = time.time_ns() if now_ns is None else now_ns
    return Observation(frame=ObservationFrame(
        session_id=session_id, observation_id=observation_id,
        capture_time_ns=now, send_time_ns=now, cameras=cameras,
        robot_state=RobotState(joint_positions=[0.0] * 6, joint_velocities=[0.0] * 6,
                               gripper=0.0),
        actions_remaining=0, instruction=instruction,
        libero_state=[float(value) for value in libero_state],
    ), camera_payloads=payloads, chunk_size=chunk_size)


def build_libero_history_observation(*, session_id: str, observation_id: int,
                                     agent_frames: np.ndarray, wrist_frames: np.ndarray,
                                     libero_state: list[float], instruction: str,
                                     chunk_size: int = 16, now_ns: int | None = None,
                                     frame_keys: tuple[int, ...] | None = None) -> Observation:
    """A LIBERO window: each camera's oriented 256px frames, oldest first, as one JPEG strip;
    or, with ``frame_keys`` (each frame's capture key, the older ones already sent ahead as
    ``history_frame`` messages), only the newest frame, naming the older ones."""
    cameras, payloads = [], {}
    keys = (CAMERA_KEY_LIBERO_AGENT, CAMERA_KEY_LIBERO_WRIST)
    for key, frames in zip(keys, (agent_frames, wrist_frames), strict=True):
        if frames.ndim != 4 or frames.shape[1:] != (256, 256, 3) or frames.dtype != np.uint8:
            raise ValueError("a LIBERO window needs 256x256 RGB uint8 frames per camera")
        if frame_keys is not None:
            if len(frame_keys) != len(frames):
                raise ValueError("a named LIBERO window needs one capture key per frame")
            payload = encode_jpeg(np.ascontiguousarray(frames[-1]))
            camera = CameraFrame(camera_id=key, width=256, height=256, encoding="jpeg",
                                 payload_bytes=len(payload), frames=len(frames),
                                 history_ns=list(frame_keys[:-1]))
        else:
            # 256px frames tile JPEG's 16px blocks exactly, so frames never blur into each other.
            camera, payload = _camera_frame(
                key, np.ascontiguousarray(np.concatenate(frames, axis=1)))
        cameras.append(camera)
        payloads[key] = payload
    now = time.time_ns() if now_ns is None else now_ns
    return Observation(frame=ObservationFrame(
        session_id=session_id, observation_id=observation_id,
        capture_time_ns=now, send_time_ns=now, cameras=cameras,
        robot_state=RobotState(joint_positions=[0.0] * 6, joint_velocities=[0.0] * 6,
                               gripper=0.0),
        actions_remaining=0, instruction=instruction,
        libero_state=[float(value) for value in libero_state],
    ), camera_payloads=payloads, chunk_size=chunk_size)


def build_lingbot_observation(*,session_id: str,observation_id: int,frames: np.ndarray,
                             instruction: str,now_ns: int | None = None) -> Observation:
    from dreamscale_transport.lingbot_contract import encode_lingbot_clip
    cameras,payloads=encode_lingbot_clip(frames)
    now=time.time_ns() if now_ns is None else now_ns
    return Observation(frame=ObservationFrame(session_id=session_id,observation_id=observation_id,
        capture_time_ns=now,send_time_ns=now,cameras=cameras,
        robot_state=RobotState(joint_positions=[0.0]*6,joint_velocities=[0.0]*6,gripper=0.0),
        actions_remaining=0,instruction=instruction),camera_payloads=payloads,chunk_size=16)


def build_yam_end_effector_observation(
    *, session_id: str, observation_id: int, top_frame: np.ndarray,
    left_frame: np.ndarray, right_frame: np.ndarray,
    robot_state: BimanualEndEffectorState, instruction: str,
    actions_remaining: int = 0, camera_capture_times_ns: tuple[int, int, int] | None = None,
) -> Observation:
    """Bound RGB uploads at the checkpoint's capture size, preserving orientation."""
    from dreamscale_transport.rho_checkpoints import RHO_YAM_BOX_MODEL_ID

    return build_rho_end_effector_observation(
        model=RHO_YAM_BOX_MODEL_ID, session_id=session_id, observation_id=observation_id,
        frames=(top_frame, left_frame, right_frame), robot_state=robot_state,
        instruction=instruction, actions_remaining=actions_remaining,
        camera_capture_times_ns=camera_capture_times_ns,
    )


def build_rho_end_effector_observation(
    *, model: str, session_id: str, observation_id: int, frames: tuple[np.ndarray, ...],
    robot_state: BimanualEndEffectorState, instruction: str,
    actions_remaining: int = 0, camera_capture_times_ns: tuple[int, ...] | None = None,
) -> Observation:
    """Any absolute end-effector Rho checkpoint; frames follow its camera_keys order."""
    from dreamscale_transport.rho_checkpoints import RHO_CHECKPOINTS

    checkpoint = RHO_CHECKPOINTS[model]
    encoded = [_camera_frame(key, prepare_policy_image(
        frame, checkpoint.wire_image_size, rotate_180=False,
    )) for key, frame in zip(checkpoint.camera_keys, frames, strict=True)]
    now = time.time_ns()
    cameras = [camera for camera, _ in encoded]
    if camera_capture_times_ns is not None:
        cameras = [camera.model_copy(update={"capture_time_ns": timestamp})
                   for camera, timestamp in zip(cameras, camera_capture_times_ns, strict=True)]
    return Observation(
        frame=ObservationFrame(
            session_id=session_id, observation_id=observation_id,
            capture_time_ns=now if camera_capture_times_ns is None
            else max(camera_capture_times_ns), send_time_ns=now,
            cameras=cameras, robot_state=robot_state, instruction=instruction,
            actions_remaining=actions_remaining,
        ),
        camera_payloads={key: payload for key, (_, payload) in zip(
            checkpoint.camera_keys, encoded, strict=True,
        )},
        chunk_size=checkpoint.action_horizon,
    )


def build_franka_observation(
    *,
    session_id: str,
    observation_id: int,
    exterior_frame: np.ndarray,
    wrist_frame: np.ndarray,
    joint_positions: list[float],
    gripper: float,
    instruction: str,
    actions_remaining: int = 0,
    second_exterior_frame: np.ndarray | None = None,
    now_ns: int | None = None,
    chunk_size: int | None = None,
) -> Observation:
    """Build a DROID-style Franka observation in checkpoint camera order."""
    now = time.time_ns() if now_ns is None else now_ns
    exterior_camera, exterior_payload = _camera_frame(
        CAMERA_KEY_DROID_EXTERIOR_1,
        exterior_frame,
    )
    cameras = [exterior_camera]
    payloads = {CAMERA_KEY_DROID_EXTERIOR_1: exterior_payload}
    if second_exterior_frame is not None:
        second_camera, second_payload = _camera_frame(
            CAMERA_KEY_DROID_EXTERIOR_2,
            second_exterior_frame,
        )
        cameras.append(second_camera)
        payloads[CAMERA_KEY_DROID_EXTERIOR_2] = second_payload
    wrist_camera, wrist_payload = _camera_frame(CAMERA_KEY_DROID_WRIST, wrist_frame)
    cameras.append(wrist_camera)
    payloads[CAMERA_KEY_DROID_WRIST] = wrist_payload
    return Observation(
        frame=ObservationFrame(
            session_id=session_id,
            observation_id=observation_id,
            capture_time_ns=now,
            send_time_ns=now,
            cameras=cameras,
            robot_state=RobotState(
                joint_positions=[float(value) for value in joint_positions],
                joint_velocities=[0.0] * 7,
                gripper=float(gripper),
            ),
            actions_remaining=actions_remaining,
            instruction=instruction,
        ),
        camera_payloads=payloads,
        **({"chunk_size": chunk_size} if chunk_size is not None else {}),
    )


def build_dreamzero_observation(
    *,
    session_id: str,
    observation_id: int,
    exterior_frame: np.ndarray,
    second_exterior_frame: np.ndarray,
    wrist_frame: np.ndarray,
    camera_capture_times_ns: tuple[int, int, int],
    joint_positions: list[float],
    gripper: float,
    instruction: str,
    source_action_step: int,
    next_action_step: int,
    control_tick: int,
    replan_epoch: int,
    cache_generation: int,
    sampling: str,
    now_ns: int | None = None,
) -> Observation:
    """Build one strict T1 DreamZero-DROID transport observation."""
    return _build_dreamzero_observation(
        session_id=session_id,
        observation_id=observation_id,
        camera_specs=(
            (
                CAMERA_KEY_DROID_EXTERIOR_1,
                exterior_frame,
                camera_capture_times_ns[0],
            ),
            (
                CAMERA_KEY_DROID_EXTERIOR_2,
                second_exterior_frame,
                camera_capture_times_ns[1],
            ),
            (CAMERA_KEY_DROID_WRIST, wrist_frame, camera_capture_times_ns[2]),
        ),
        robot_state=RobotState(
            joint_positions=[float(value) for value in joint_positions],
            joint_velocities=[0.0] * 7,
            gripper=float(gripper),
        ),
        instruction=instruction,
        source_action_step=source_action_step,
        next_action_step=next_action_step,
        control_tick=control_tick,
        replan_epoch=replan_epoch,
        cache_generation=cache_generation,
        sampling=sampling,
        now_ns=now_ns,
    )


def build_dreamzero_yam_observation(
    *,
    session_id: str,
    observation_id: int,
    top_frame: np.ndarray,
    left_frame: np.ndarray,
    right_frame: np.ndarray,
    camera_capture_times_ns: tuple[int, int, int],
    left_joint_positions: list[float],
    left_gripper: float,
    right_joint_positions: list[float],
    right_gripper: float,
    instruction: str,
    source_action_step: int,
    next_action_step: int,
    control_tick: int,
    replan_epoch: int,
    cache_generation: int,
    sampling: str,
    now_ns: int | None = None,
) -> Observation:
    """Build one strict T1 DreamZero-YAM transport observation."""
    return _build_dreamzero_observation(
        session_id=session_id,
        observation_id=observation_id,
        camera_specs=(
            (CAMERA_KEY_BIMANUAL_YAM_TOP, top_frame, camera_capture_times_ns[0]),
            (CAMERA_KEY_BIMANUAL_YAM_LEFT, left_frame, camera_capture_times_ns[1]),
            (CAMERA_KEY_BIMANUAL_YAM_RIGHT, right_frame, camera_capture_times_ns[2]),
        ),
        robot_state=BimanualRobotState(
            left_joint_positions=left_joint_positions,
            left_joint_velocities=[0.0] * 6,
            left_gripper=left_gripper,
            right_joint_positions=right_joint_positions,
            right_joint_velocities=[0.0] * 6,
            right_gripper=right_gripper,
        ),
        instruction=instruction,
        source_action_step=source_action_step,
        next_action_step=next_action_step,
        control_tick=control_tick,
        replan_epoch=replan_epoch,
        cache_generation=cache_generation,
        sampling=sampling,
        now_ns=now_ns,
        camera_encoding="h264",
        action_hz=30,
        chunk_size=24,
        max_camera_skew_ns=None,
    )


def _build_dreamzero_observation(
    *,
    session_id: str,
    observation_id: int,
    camera_specs: tuple[tuple[str, np.ndarray, int], ...],
    robot_state: RobotState | BimanualRobotState,
    instruction: str,
    source_action_step: int,
    next_action_step: int,
    control_tick: int,
    replan_epoch: int,
    cache_generation: int,
    sampling: str,
    now_ns: int | None,
    camera_encoding: str = "jpeg",
    action_hz: int = 15,
    chunk_size: int = 24,
    max_camera_skew_ns: int | None = _DREAMZERO_MAX_CAMERA_SKEW_NS,
) -> Observation:
    capture_times_ns = tuple(spec[2] for spec in camera_specs)
    if max_camera_skew_ns is not None and (
        max(capture_times_ns) - min(capture_times_ns) > max_camera_skew_ns
    ):
        raise ValueError("camera skew exceeds the 50 ms DreamZero limit")
    capture_start_ns = min(capture_times_ns)
    capture_end_ns = max(capture_times_ns)
    encode_start_ns = max(time.time_ns(), capture_end_ns) if now_ns is None else int(now_ns)
    cameras: list[CameraFrame] = []
    payloads: dict[str, bytes] = {}
    raw_frames: dict[str, object] = {}
    for camera_id, frame, capture_time_ns in camera_specs:
        if camera_encoding == "jpeg":
            camera, payload = _camera_frame(camera_id, frame)
            payloads[camera_id] = payload
        elif camera_encoding == "h264":
            values = np.asarray(frame)
            camera = CameraFrame(
                camera_id=camera_id,
                width=int(values.shape[1]),
                height=int(values.shape[0]),
                encoding="h264",
                payload_bytes=0,
                raw_bytes=int(values.nbytes),
            )
            raw_frames[camera_id] = values
        else:
            raise ValueError(f"unsupported DreamZero camera encoding: {camera_encoding}")
        cameras.append(camera.model_copy(update={"capture_time_ns": int(capture_time_ns)}))
    if camera_encoding == "jpeg":
        encode_end_ns = max(time.time_ns(), encode_start_ns) if now_ns is None else int(now_ns)
        send_time_ns = max(time.time_ns(), encode_end_ns) if now_ns is None else int(now_ns)
    else:
        encode_start_ns = None
        encode_end_ns = None
        send_time_ns = capture_end_ns
    return Observation(
        frame=ObservationFrame(
            session_id=session_id,
            observation_id=observation_id,
            capture_time_ns=capture_end_ns,
            send_time_ns=send_time_ns,
            capture_start_time_ns=capture_start_ns,
            capture_end_time_ns=capture_end_ns,
            encode_start_time_ns=encode_start_ns,
            encode_end_time_ns=encode_end_ns,
            cameras=cameras,
            robot_state=robot_state,
            actions_remaining=0,
            instruction=instruction,
            runtime_context=RuntimeRequestContext(
                queue={
                    "action_hz": action_hz,
                    "source_action_step": int(source_action_step),
                    "next_action_step": int(next_action_step),
                    "control_tick": int(control_tick),
                    "replan_epoch": int(replan_epoch),
                    "replan_stride": 8,
                    "sampling": sampling,
                    "cache_generation": int(cache_generation),
                }
            ),
        ),
        camera_payloads=payloads,
        chunk_size=chunk_size,
        raw_camera_frames=raw_frames or None,
    )


def build_yam_observation(
    *,
    session_id: str,
    observation_id: int,
    top_frame: np.ndarray,
    left_frame: np.ndarray,
    right_frame: np.ndarray,
    left_joint_positions: list[float],
    left_joint_velocities: list[float],
    left_gripper: float,
    right_joint_positions: list[float],
    right_joint_velocities: list[float],
    right_gripper: float,
    instruction: str,
    actions_remaining: int = 0,
    camera_capture_times_ns: tuple[int, int, int] | None = None,
    now_ns: int | None = None,
) -> Observation:
    """Build a BimanualYAM observation in checkpoint camera/state order.

    Inside ``raw_frames()`` the cameras stay raw (``raw_camera_frames``, no payloads) for
    the transport's camera codec.
    """
    top_camera, top_payload = _camera_frame(CAMERA_KEY_BIMANUAL_YAM_TOP, top_frame)
    left_camera, left_payload = _camera_frame(CAMERA_KEY_BIMANUAL_YAM_LEFT, left_frame)
    right_camera, right_payload = _camera_frame(CAMERA_KEY_BIMANUAL_YAM_RIGHT, right_frame)
    raw = _raw_frames()
    send_time_ns = time.time_ns() if now_ns is None else int(now_ns)
    capture_time_ns = send_time_ns
    if camera_capture_times_ns is not None:
        capture_time_ns = max(camera_capture_times_ns)
        top_camera = top_camera.model_copy(
            update={"capture_time_ns": camera_capture_times_ns[0]}
        )
        left_camera = left_camera.model_copy(
            update={"capture_time_ns": camera_capture_times_ns[1]}
        )
        right_camera = right_camera.model_copy(
            update={"capture_time_ns": camera_capture_times_ns[2]}
        )
    return Observation(
        frame=ObservationFrame(
            session_id=session_id,
            observation_id=observation_id,
            capture_time_ns=capture_time_ns,
            send_time_ns=send_time_ns,
            cameras=[top_camera, left_camera, right_camera],
            robot_state=BimanualRobotState(
                left_joint_positions=left_joint_positions,
                left_joint_velocities=left_joint_velocities,
                left_gripper=left_gripper,
                right_joint_positions=right_joint_positions,
                right_joint_velocities=right_joint_velocities,
                right_gripper=right_gripper,
            ),
            actions_remaining=actions_remaining,
            instruction=instruction,
        ),
        camera_payloads={} if raw else {
            CAMERA_KEY_BIMANUAL_YAM_TOP: top_payload,
            CAMERA_KEY_BIMANUAL_YAM_LEFT: left_payload,
            CAMERA_KEY_BIMANUAL_YAM_RIGHT: right_payload,
        },
        raw_camera_frames=raw,
    )


def build_three_view_bimanual_observation(
    *,
    session_id: str,
    observation_id: int,
    camera_keys: tuple[str, str, str],
    frames: tuple[np.ndarray, np.ndarray, np.ndarray],
    robot_state: BimanualRobotState,
    instruction: str,
    actions_remaining: int = 0,
    camera_capture_times_ns: tuple[int, int, int] | None = None,
    now_ns: int | None = None,
) -> Observation:
    """Build a bimanual observation from three views in the checkpoint's camera order."""
    keys = camera_keys
    encoded = [_camera_frame(key, frame) for key, frame in zip(keys, frames, strict=True)]
    send_time_ns = time.time_ns() if now_ns is None else int(now_ns)
    capture_time_ns = send_time_ns
    cameras = [camera for camera, _ in encoded]
    if camera_capture_times_ns is not None:
        capture_time_ns = max(camera_capture_times_ns)
        cameras = [
            camera.model_copy(update={"capture_time_ns": value})
            for camera, value in zip(cameras, camera_capture_times_ns, strict=True)
        ]
    return Observation(
        frame=ObservationFrame(
            session_id=session_id,
            observation_id=observation_id,
            capture_time_ns=capture_time_ns,
            send_time_ns=send_time_ns,
            cameras=cameras,
            robot_state=robot_state,
            actions_remaining=actions_remaining,
            instruction=instruction,
        ),
        camera_payloads={key: payload for key, (_, payload) in zip(keys, encoded, strict=True)},
    )


def chunk_actions(chunk) -> list[list[float]]:
    return [list(action.target) for action in chunk.actions]


def chunk_action_indices(chunk) -> list[int]:
    return [int(action.action_index) for action in chunk.actions]
