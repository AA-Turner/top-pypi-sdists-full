"""`dreamscale run so101 --model <LLM>`: a managed LLM drives the SO-101 through bounded
gripper tools. Model, options and access are resolved before the motors arm."""

from decimal import Decimal
from uuid import uuid4

from dreamscale_transport.llm import SessionRequest

from dreamscale import errors
from dreamscale.config import API_KEY_ENV, LEGACY_API_KEY_ENV, dreamscale_home, env_with_legacy
from dreamscale.config import load_config as account_config
from dreamscale.embodiments import SO101
from dreamscale.model_names import resolve_llm_model

from .attended import run_attended_llm
from .client import Gateway
from .so101 import So101Adapter, profile


def run_so101_llm(
    *,
    model,
    instruction,
    effort="medium",
    speed="standard",
    max_cost=None,
    max_joint_step=45.0,
    max_joint_velocity=150.0,
    robot_factory=None,
    rig_options=None,
    input_fn=input,
    print_fn=print,
):
    from dreamscale.hardware.so101_rig import So101Rig
    from dreamscale.homing import _valid_pose
    from dreamscale.so101_runner import (
        COMMAND,
        _default_robot_factory,
        rig_cameras,
        so101_preflight,
    )

    if not instruction or not instruction.strip():
        raise ValueError("LLM tasks need --instruction.")
    request = SessionRequest(
        request_id=str(uuid4()),
        model=resolve_llm_model(model),
        profile=profile(),
        instruction=instruction,
        effort=effort,
        speed=speed,
        max_cost=Decimal(str(max_cost)) if max_cost is not None else None,
    )
    account = account_config()
    key = env_with_legacy(API_KEY_ENV, LEGACY_API_KEY_ENV) or account.api_key
    if not key:
        raise ValueError("Run dreamscale login before starting a managed LLM task.")
    factory = robot_factory or _default_robot_factory
    cameras = rig_cameras(factory)
    if account.robot_port is None or (
        cameras is None and None in (account.camera_index, account.wrist_camera_index)
    ):
        raise errors.catalog("so101_not_set_up")
    home = account.home_position
    home = [float(v) for v in home] if _valid_pose(home) else None
    so101_preflight(account, home, cameras=cameras, print_fn=print_fn)

    return run_attended_llm(
        request=request,
        embodiment=SO101,
        make_gateway=lambda: Gateway(account.control_plane_url, key),
        make_rig=lambda: So101Rig(
            factory,
            calibration_path=account.calibration_path,
            home=home,
            max_joint_step=max_joint_step,
            max_joint_velocity=max_joint_velocity,
            cameras={"side": account.camera_index, "wrist": account.wrist_camera_index},
            camera_config=cameras,
            retry_command=COMMAND,
            print_fn=print_fn,
            **(rig_options or {}),
        ),
        make_adapter=lambda rig: So101Adapter(rig, owns_rig=False),
        journal_dir=dreamscale_home() / "llm-runs",
        input_fn=input_fn,
        print_fn=print_fn,
    )
