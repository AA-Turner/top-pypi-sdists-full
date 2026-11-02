"""`dreamscale robots xarm7 setup`: write the rig file from what's plugged in.

Reads both arms and grippers read-only, finds the cameras and saves one preview per camera,
then asks the operator what a computer can't know: each arm's address and gripper, and which
camera plays which role.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path

from .camera_sources import discover_cameras, one_per_camera, usb_link_mbps
from .franka_setup import _choose, save_previews
from .xarm7_config import ARMS, DEFAULT_CONFIG_PATH, ROLES, ArmConfig, load_config, save_config
from .xarm7_doctor import arm_checks, probe_arm
from .xarm_arm import GRIPPER_LABELS, GRIPPER_TYPES

DEFAULT_HOSTS = {"aft": "192.168.1.236", "fore": "192.168.1.201"}
_ROLE_TEXT = {
    "top": "Top, the scene camera above the bench",
    "left": "Left, the camera on the fore arm's wrist",
    "right": "Right, the camera on the aft arm's wrist",
}
# Recordings on these rigs are 1280x720; any 16:9 stream keeps the models' view, and frames
# go up at capture size, so the smallest D435 16:9 mode keeps the uplink light.
WIDTH, HEIGHT = 640, 360


def hardware_checks(config, *, arm_probe=probe_arm):
    results = []
    for name in ARMS:
        arm = config.arms[name]
        results += arm_checks(config, name, arm_probe(arm.host, arm.gripper))
    return results


def run_xarm7_setup(
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
    print_fn("xArm 7 setup. Nothing moves; the arms and grippers are only read.")
    arms = {}
    for name in ARMS:
        current = config.arms.get(name) or ArmConfig(DEFAULT_HOSTS[name])
        host = input_fn(f"{name.title()} arm control box address [{current.host}]: ").strip()
        gripper = GRIPPER_TYPES[_choose(
            f"{name.title()} gripper:", [GRIPPER_LABELS[g] for g in GRIPPER_TYPES],
            default=GRIPPER_TYPES.index(current.gripper) + 1, input_fn=input_fn,
            print_fn=print_fn,
        ) - 1]
        arms[name] = ArmConfig(host or current.host, gripper)
    config = replace(config, arms=arms).validate()
    print_fn("Reading the arms…")
    for check in checks(config):
        print_fn(f"  {check.status:>4}  {check.name}: {check.detail}")

    cameras = one_per_camera(config.cameras, discover(), link_speed=link_speed)
    if not cameras:
        print_fn("No cameras found. Check USB cables and power, then rerun setup.")
        save_config(config, config_path)
        return config
    cameras = [replace(spec, width=WIDTH, height=HEIGHT) for spec in cameras]
    directory = config_path.with_name("xarm7-previews")
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
    print_fn(f"Saved {config_path}. Next: dreamscale doctor xarm7")
    return config
