"""SO-101 on the shared setup page: side and wrist cameras, then its serial port."""

from __future__ import annotations

from pathlib import Path

from . import rig_setup
from .rig_setup import RigSetupProfile
from .so101_config import So101Config, default_config_path, load_config, save_config


class So101SetupProfile(RigSetupProfile):
    """SO-101 on the shared setup page (dreamscale.hardware.rig_setup)."""

    name = "so101"
    label = "SO-101"
    roles = (
        ("side", "Side", "The one beside the arm that sees it and the table."),
        ("wrist", "Wrist", "On the gripper. Not sure? Cover it with your hand."),
    )
    required_roles = ("side", "wrist")
    cli_command = "dreamscale robots so101 setup --cli"
    config_cls = So101Config

    def __init__(self, comports=None):
        self.comports = comports

    def load(self, path):
        return load_config(path)

    def save(self, config, path):
        save_config(config, path)

    def from_dict(self, value):
        config = So101Config.from_dict(value)
        if config.calibration_path is None:
            from dreamscale.config import default_calibration_path

            config.calibration_path = default_calibration_path()
        return config

    def remaining_hardware(self, config):
        return None if config.port else "Choose the arm's serial port."

    def changed(self, draft, saved):
        return draft.to_dict() != saved.to_dict() or saved.migrated

    def _ports(self):
        from .ports import list_candidate_ports

        found = (list_candidate_ports(comports=self.comports) if self.comports
                 else list_candidate_ports())
        return [{"device": p.device, "description": getattr(p, "description", "") or ""}
                for p in found]

    def hardware_state(self, draft, saved):
        from dreamscale.config import default_calibration_path
        from dreamscale.doctor import calibration_format

        calibration = Path(draft.calibration_path or default_calibration_path()).expanduser()
        return {
            "ports": self._ports(),
            "calibration": {"path": str(calibration),
                            "format": calibration_format(calibration)},
            "migrated": saved.migrated,
        }

    def routes(self):
        return {"/api/ports": lambda _server: self._ports()}

    def after_save(self, path, *, print_fn, interactive):
        # config.toml now keeps only the account: drop its pre-rig-file robot keys.
        from dreamscale.config import load_config as load_account
        from dreamscale.config import save_config as save_account

        save_account(load_account())



def run_so101_page(config_path=None, *, host="0.0.0.0", port=8765, **options):
    """`dreamscale robots so101 setup`: the shared setup page with SO-101's panel."""
    path = config_path or default_config_path()
    return rig_setup.run_setup(So101SetupProfile(), path, default_path=default_config_path(),
                               host=host, port=port, **options)
