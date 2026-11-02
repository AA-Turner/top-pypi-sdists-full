"""YAM on the shared setup page: cameras, then arms identified by replugging.

Setup never opens CAN or moves motors: arms are identified passively, by watching which
adapter disappears. Everything else is dreamscale.hardware.rig_setup.
"""

from __future__ import annotations

from pathlib import Path

from . import rig_setup
from .camera_sources import one_per_camera, usb_cameras_present  # noqa: F401 (re-export)
from .rig_setup import RigSetupProfile, lan_address  # noqa: F401 (re-export)
from .yam_can import bring_up_arms, discover_can_interfaces, locate_arms, pin_arms
from .yam_config import (
    ARM_TYPES,
    DEFAULT_CONFIG_PATH,
    GRIPPER_TYPES,
    YamConfig,
    load_config,
    save_config,
)

# The page assumes the standard rig; other variants stay one click away.
DEFAULT_ARM = {"arm_type": "YAM", "gripper_type": "LINEAR_4310"}


class YamSetupProfile(RigSetupProfile):
    name = "yam"
    label = "YAM"
    roles = (
        ("top", "Top", "The one that sees the whole workspace."),
        ("left", "Left wrist", "On the robot's left arm. Not sure? Cover it with your hand."),
        ("right", "Right wrist", "On the robot's right arm. Not sure? Cover it with your hand."),
    )
    required_roles = ("top", "left", "right")
    cli_command = "dreamscale robots yam setup --cli"
    config_cls = YamConfig

    def __init__(self, discover_can=discover_can_interfaces, bring_up=bring_up_arms):
        self.discover_can, self.bring_up = discover_can, bring_up

    def load(self, path):
        return load_config(path)

    def save(self, config, path):
        save_config(config, path)

    def remaining_hardware(self, config):
        sides = [side for side in ("left", "right") if side not in config.arms]
        if sides:
            return f"Identify the {rig_setup.listed(sides)} arm{'s' if len(sides) > 1 else ''}."
        return None

    def hardware_state(self, draft, saved):
        inventory = self.discover_can()
        connected = {i.name for i in inventory.interfaces}
        # Rigs saved before pinning save again to lock arms to their adapters.
        unpinned = any(
            arm.adapter_id is None and arm.can_interface in connected
            for arm in saved.arms.values()
        )
        located, _ = locate_arms(draft, inventory)
        known, _ = locate_arms(saved, inventory)
        return {
            # Show each pinned arm under today's name; saving re-pins by that name.
            "config": located.to_dict(),
            "changed": (
                pin_arms(located, inventory).to_dict() != pin_arms(known, inventory).to_dict()
            ),
            "unpinned": unpinned,
            "can": inventory.to_dict(),
            "arm_types": ARM_TYPES,
            "gripper_types": GRIPPER_TYPES,
            "default_arm": DEFAULT_ARM,
        }

    def prepare_save(self, config):
        """Each arm pinned to the adapter it is on now."""
        return pin_arms(config, self.discover_can())

    def routes(self):
        return {"/api/can": lambda _server: self.discover_can().to_dict()}

    def after_save(self, path, *, print_fn, interactive):
        try:
            self.bring_up(
                load_config(path), discover_can=self.discover_can, print_fn=print_fn,
                interactive=interactive,
            )
        except KeyboardInterrupt:
            print_fn("Skipped bringing up the CAN buses.")


def remaining(config: YamConfig) -> str | None:
    """What is left before the YAM rig can be saved, or None when it is complete."""
    return rig_setup.remaining(YamSetupProfile(), config)


class SetupServer(rig_setup.SetupServer):
    """The shared setup page with YAM's profile; see rig_setup.SetupServer."""

    def __init__(self, config_path: Path = DEFAULT_CONFIG_PATH, *,
                 discover_can=discover_can_interfaces, **options):
        self.discover_can = discover_can
        super().__init__(YamSetupProfile(discover_can), config_path, **options)


def run_setup(
    config_path: Path = DEFAULT_CONFIG_PATH,
    *,
    host="0.0.0.0",
    port=8765,
    readers_factory=None,
    discover=None,
    print_url=print,
    discover_can=discover_can_interfaces,
    input_fn=input,
    bring_up=bring_up_arms,
):
    """Blocking: Save on the page or Enter here saves; Ctrl-C discards. After a save,
    arm buses that are not up at 1 Mbit/s are brought up, sudo asking here."""
    return rig_setup.run_setup(
        YamSetupProfile(discover_can, bring_up), config_path, default_path=DEFAULT_CONFIG_PATH,
        host=host, port=port, readers_factory=readers_factory, discover=discover,
        print_url=print_url, input_fn=input_fn,
    )
