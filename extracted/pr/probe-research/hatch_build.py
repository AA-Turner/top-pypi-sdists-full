"""Vendor probe-contracts (`../contracts/probe_contracts`) into the built wheel as `probe/_vendor/probe_contracts`.

One source, copied only inside the built artifact, until probe-contracts is on PyPI. The sdist
carries it as `contracts/probe_contracts` so a wheel built from the sdist (`python -m build`)
vendors it too. A build context without it (the MCP image) builds without it: nothing imports
the vendored copy yet. Editable installs skip it.
"""

from __future__ import annotations

from pathlib import Path

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

#: Where the package sits inside the wheel.
VENDORED_AS = "probe/_vendor/probe_contracts"
#: Where the sdist keeps it, so a wheel built from the sdist finds it.
IN_SDIST = "contracts/probe_contracts"


def find_contracts(root: Path) -> Path | None:
    """The package folder: beside the agent in a checkout, inside an unpacked sdist, or none."""
    for candidate in (root.parent / IN_SDIST, root / IN_SDIST):
        if candidate.is_dir():
            return candidate
    return None


class ContractsVendorHook(BuildHookInterface):
    PLUGIN_NAME = "custom"

    def initialize(self, version: str, build_data: dict) -> None:
        if version == "editable":
            return
        source = find_contracts(Path(self.root))
        if source is None:
            return
        destination = IN_SDIST if self.target_name == "sdist" else VENDORED_AS
        for path in sorted(source.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts:
                build_data["force_include"][str(path)] = f"{destination}/{path.relative_to(source).as_posix()}"
