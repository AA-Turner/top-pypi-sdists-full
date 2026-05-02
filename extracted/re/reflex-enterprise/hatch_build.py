"""Build hook to inject constants into the Reflex Enterprise package."""

import os
from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

REFLEX_NO_CALL_HOME = os.environ.get("REFLEX_NO_CALL_HOME", "False").lower() == "true"


class ConstantInjectionHook(BuildHookInterface):
    """A build hook to inject constants into the Reflex Enterprise package."""

    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict) -> None:
        """Initialize the hook."""
        if self.target_name == "wheel":
            self.inject_constants()

    def inject_constants(self):
        """Inject constants into the Reflex Enterprise package."""
        constants_path = Path("reflex_enterprise/constants.py")

        constants_path.write_text(
            constants_path.read_text().replace(
                "IS_OFFLINE = False", f"IS_OFFLINE = {REFLEX_NO_CALL_HOME}"
            )
        )
