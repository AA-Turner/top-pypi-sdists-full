"""`dreamscale robots ur setup`: write the rig file from what's plugged in.

Reads the arm and gripper read-only, finds the cameras and saves one preview per camera,
then asks the operator what a computer can't know: the arm's model, its gripper, and which
camera plays which role.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from . import rig_setup
from .camera_sources import discover_cameras, one_per_camera, usb_link_mbps
from .franka_setup import _choose, save_previews
from .rig_setup import RigSetupProfile
from .ur_arm import ARM_MODELS, ARM_SPECS
from .ur_config import (
    DEFAULT_CONFIG_PATH,
    GRIPPER_LABELS,
    GRIPPER_TYPES,
    ROLES,
    ArmConfig,
    GripperConfig,
    load_config,
    save_config,
)
from .ur_doctor import arm_checks, gripper_checks, probe_arm, probe_gripper

DEFAULT_HOST = "192.168.100.10"
_ROLE_TEXT = {
    "scene": "Scene, the over-the-shoulder view of the table",
    "wrist": "Wrist, the camera on the gripper",
}


def hardware_checks(config, *, arm_probe=probe_arm, gripper_probe=probe_gripper):
    arm = config.arm
    results = arm_checks(config, arm_probe(arm.host, arm.model))
    probed = gripper_probe(arm.host) if config.gripper.type != "none" else {}
    return results + gripper_checks(config, probed)


def run_ur_setup(
    config_path=DEFAULT_CONFIG_PATH,
    *,
    discover=discover_cameras,
    checks=hardware_checks,
    previews=save_previews,
    link_speed=usb_link_mbps,
    input_fn=input,
    print_fn=print,
):
    config_path = Path(config_path)
    config = load_config(config_path)
    print_fn("Universal Robots setup. Nothing moves; the arm and gripper are only read.")
    arm = config.arm or ArmConfig(DEFAULT_HOST)
    model = ARM_MODELS[_choose(
        "Arm:", [ARM_SPECS[m].label for m in ARM_MODELS],
        default=ARM_MODELS.index(arm.model) + 1, input_fn=input_fn, print_fn=print_fn,
    ) - 1]
    host = input_fn(f"Control box address [{arm.host}]: ").strip() or arm.host
    gripper = GRIPPER_TYPES[_choose(
        "Gripper:", [GRIPPER_LABELS[g] for g in GRIPPER_TYPES],
        default=GRIPPER_TYPES.index(config.gripper.type) + 1, input_fn=input_fn,
        print_fn=print_fn,
    ) - 1]
    config = replace(
        config, arm=replace(arm, host=host, model=model), gripper=GripperConfig(gripper),
    )
    print_fn(f"Reading the arm at {host}…")
    for check in checks(config):
        print_fn(f"  {check.status:>4}  {check.name}: {check.detail}")

    cameras = one_per_camera(config.cameras, discover(), link_speed=link_speed)
    if not cameras:
        print_fn("No cameras found. Check USB cables and power, then rerun setup.")
        save_config(config, config_path)
        return config
    directory = config_path.with_name("ur-previews")
    shots = previews(cameras, directory)

    def label(spec):
        shot = shots.get(spec.id)
        if isinstance(shot, Path):
            return f"{spec.backend} {spec.id} · preview {shot}"
        return f"{spec.backend} {spec.id}" + (f" · no preview: {shot}" if shot else "")

    labels = [label(spec) for spec in cameras]
    if any(isinstance(shot, Path) for shot in shots.values()):
        print_fn(f"Saved a preview of each camera in {directory}. Open them to tell views apart.")
    roles, used = {}, set()
    by_id = {spec.id: index for index, spec in enumerate(cameras, 1)}
    for role in ROLES:
        choice = _choose(
            _ROLE_TEXT[role] + ":", labels, default=by_id.get(config.roles.get(role)),
            input_fn=input_fn, print_fn=print_fn,
        )
        while choice is not None and choice in used:
            print_fn("That camera already has a role. Choose another, or Enter to skip.")
            choice = _choose(
                _ROLE_TEXT[role] + ":", labels, default=None, input_fn=input_fn,
                print_fn=print_fn,
            )
        if choice is not None:
            roles[role] = cameras[choice - 1].id
            used.add(choice)
    chosen = [spec for spec in cameras if spec.id in roles.values()]
    config = replace(config, cameras=chosen, roles=roles).validate()
    save_config(config, config_path)
    print_fn(f"Saved {config_path}. Next: dreamscale doctor ur")
    return config


class URSetupProfile(RigSetupProfile):
    """A UR arm on the shared setup page (dreamscale.hardware.rig_setup)."""

    name = "ur"
    label = "Universal Robots"
    roles = (
        ("scene", "Scene", "Behind and above the arm, looking at the table."),
        ("wrist", "Wrist", "On the gripper. Not sure? Cover it with your hand."),
    )
    required_roles = ("scene", "wrist")
    cli_command = "dreamscale robots ur setup --cli"

    def __init__(self, checks=hardware_checks):
        from .ur_config import URConfig

        self.checks, self.config_cls = checks, URConfig

    def load(self, path):
        return load_config(path)

    def save(self, config, path):
        save_config(config, path)

    def remaining_hardware(self, config):
        return None if config.arm is not None else "Set the control box's address."

    def hardware_state(self, draft, saved):
        return {
            "arm_models": list(ARM_MODELS), "gripper_types": list(GRIPPER_TYPES),
            "labels": {**{m: ARM_SPECS[m].label for m in ARM_MODELS}, **GRIPPER_LABELS},
            "default_arm": {"host": DEFAULT_HOST, "model": ArmConfig(DEFAULT_HOST).model},
        }

    def routes(self):
        return {"/api/probe": self._probe}

    def _probe(self, server):
        """Read-only checks of the draft's arm and gripper, as doctor shows them."""
        with server.lock:
            config = server.config
        if config.arm is None:
            raise ValueError("Set the control box's address first.")
        return [
            {"name": r.name, "status": r.status, "detail": r.detail}
            for r in self.checks(config)
        ]


def run_ur_page(config_path=DEFAULT_CONFIG_PATH, *, host="0.0.0.0", port=8765, **options):
    """`dreamscale robots ur setup`: the shared setup page with the UR panel."""
    return rig_setup.run_setup(URSetupProfile(), config_path,
                               default_path=DEFAULT_CONFIG_PATH, host=host, port=port, **options)
