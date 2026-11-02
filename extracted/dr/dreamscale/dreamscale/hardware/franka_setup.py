"""`dreamscale robots franka setup`: write the rig file from what's plugged in.

Probes the arm read-only, finds the cameras and saves one preview image per camera, then
asks the operator the only thing a computer can't know: which camera plays which role.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from . import rig_setup
from .camera_sources import (
    CameraReaders,
    camera_error_text,
    discover_cameras,
    one_per_camera,
    usb_link_mbps,
    wait_for_frames,
)
from .franka_config import (
    ARM_MODELS,
    DEFAULT_CONFIG_PATH,
    GRIPPER_TYPES,
    ROLES,
    ArmConfig,
    GripperConfig,
    load_config,
    save_config,
)
from .franka_doctor import arm_checks, probe_arm
from .rig_setup import RigSetupProfile

DEFAULT_HOST = "172.16.0.2"
_ROLE_TEXT = {
    "exterior_1": "Exterior 1, the main scene view (single-view models get this one)",
    "exterior_2": "Exterior 2, a second scene view (optional)",
    "wrist": "Wrist, the camera on the hand",
}


def save_previews(cameras, directory: Path, *, readers_factory=CameraReaders) -> dict:
    """One JPEG per camera, so the operator can tell them apart: camera id -> its path,
    or the reason it has none."""
    import cv2

    directory.mkdir(parents=True, exist_ok=True)
    saved = {}
    for index, spec in enumerate(cameras, 1):
        readers = None
        try:
            readers = readers_factory([spec])
            readers.open()
            frame = wait_for_frames(readers, [spec.id], timeout_s=8.0)[spec.id]
            path = directory / f"camera-{index}.jpg"
            cv2.imwrite(str(path), frame.rgb[:, :, ::-1])
            saved[spec.id] = path
        except Exception as exc:
            saved[spec.id] = camera_error_text(exc)
        finally:
            if readers is not None:
                try:
                    readers.close()
                except Exception:
                    pass
    return saved


def _ask(prompt, *, default, input_fn):
    reply = input_fn(f"{prompt} [{default}]: ").strip()
    return reply or default


def _choose(prompt, options, *, default, input_fn, print_fn):
    print_fn(prompt)
    for index, text in enumerate(options, 1):
        print_fn(f"  {index}. {text}")
    while True:
        reply = input_fn(f"Number [{default or 'Enter to skip'}]: ").strip()
        if not reply:
            return default
        if reply.isdecimal() and 1 <= int(reply) <= len(options):
            return int(reply)
        print_fn("Choose a listed number.")


def run_franka_setup(
    config_path=DEFAULT_CONFIG_PATH,
    *,
    discover=discover_cameras,
    probe=probe_arm,
    previews=save_previews,
    link_speed=usb_link_mbps,
    input_fn=input,
    print_fn=print,
):
    config_path = Path(config_path)
    config = load_config(config_path)
    print_fn("Franka setup. Nothing moves; the arm is only read.")

    saved_model = config.arm.model if config.arm else "fr3"
    model = ARM_MODELS[_choose(
        "Arm model:", [m.upper() for m in ARM_MODELS],
        default=ARM_MODELS.index(saved_model) + 1, input_fn=input_fn, print_fn=print_fn,
    ) - 1]
    host = _ask(
        "Arm FCI address", default=config.arm.host if config.arm else DEFAULT_HOST,
        input_fn=input_fn,
    )
    gripper = GRIPPER_TYPES[_choose(
        "Gripper:", list(GRIPPER_TYPES),
        default=GRIPPER_TYPES.index(config.gripper.type) + 1, input_fn=input_fn,
        print_fn=print_fn,
    ) - 1]
    config = replace(config, arm=ArmConfig(model, host), gripper=GripperConfig(gripper))
    print_fn(f"Reading the arm at {host}…")
    for check in arm_checks(config, probe(host)):
        print_fn(f"  {check.status:>4}  {check.name}: {check.detail}")

    cameras = one_per_camera(config.cameras, discover(), link_speed=link_speed)
    if not cameras:
        print_fn("No cameras found. Check USB cables and power, then rerun setup.")
        save_config(config, config_path)
        return config
    directory = config_path.with_name("franka-previews")
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
        saved = by_id.get(config.roles.get(role))
        choice = _choose(
            _ROLE_TEXT[role] + ":", labels, default=saved, input_fn=input_fn, print_fn=print_fn,
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
    print_fn(f"Saved {config_path}. Next: dreamscale doctor franka")
    return config


class FrankaSetupProfile(RigSetupProfile):
    """Franka on the shared setup page (dreamscale.hardware.rig_setup)."""

    name = "franka"
    label = "Franka"
    roles = (
        ("exterior_1", "Exterior 1", "The main scene camera beside the table. "
         "Models that read one view get this one."),
        ("wrist", "Wrist", "On the hand. Not sure? Cover it with your hand."),
        ("exterior_2", "Exterior 2", "A second scene camera, for models that "
         "read two."),
    )
    required_roles = ("exterior_1", "wrist")
    cli_command = "dreamscale robots franka setup --cli"

    def __init__(self, probe=probe_arm):
        from .franka_config import FrankaConfig

        self.probe, self.config_cls = probe, FrankaConfig

    def load(self, path):
        return load_config(path)

    def save(self, config, path):
        save_config(config, path)

    def remaining_hardware(self, config):
        return None if config.arm is not None else "Set the arm's model and FCI address."

    def hardware_state(self, draft, saved):
        return {
            "arm_models": list(ARM_MODELS),
            "gripper_types": list(GRIPPER_TYPES),
            "default_arm": {"model": "fr3", "host": DEFAULT_HOST},
        }

    def routes(self):
        return {"/api/probe": self._probe}

    def _probe(self, server):
        """Read-only checks of the draft's arm, as doctor shows them."""
        with server.lock:
            config = server.config
        if config.arm is None:
            raise ValueError("Set the arm's model and FCI address first.")
        return [
            {"name": r.name, "status": r.status, "detail": r.detail}
            for r in arm_checks(config, self.probe(config.arm.host))
        ]



def run_franka_page(config_path=DEFAULT_CONFIG_PATH, *, host="0.0.0.0", port=8765, **options):
    """`dreamscale robots franka setup`: the shared setup page with Franka's panel."""
    return rig_setup.run_setup(FrankaSetupProfile(), config_path,
                               default_path=DEFAULT_CONFIG_PATH, host=host, port=port, **options)
