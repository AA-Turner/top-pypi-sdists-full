"""Proxy to get data from resmoke."""

from __future__ import annotations

import os
import subprocess
from typing import List, Optional

import structlog
import yaml
from pydantic import BaseModel

LOGGER = structlog.get_logger(__name__)


class MultiversionConfig(BaseModel):
    """
    Multiversion Configuration obtained from resmoke.

    * last_lts_fcv: Version of the last LTS release.
    * last_continuous_fcv: Version of the last continuous release.
    * last_patch_version: Version of the last patch release (populated only when
      resmoke is invoked with `--include-last-patch`).
    """

    last_lts_fcv: str
    last_continuous_fcv: str
    last_patch_version: Optional[str] = None


class ResmokeProxy:
    """A proxy for interacting with resmoke."""

    def __init__(self, resmoke_cmd: List[str]) -> None:
        """
        Initialize the service.

        :param resmoke_cmd: Command to invoke resmoke.py.
        """
        self.resmoke_cmd = resmoke_cmd
        self.multiversion_constants: Optional[MultiversionConfig] = None
        self.include_last_patch: bool = False

    def enable_last_patch(self) -> None:
        """Request that multiversion-config be invoked with --include-last-patch."""
        if (
            self.multiversion_constants is not None
            and self.multiversion_constants.last_patch_version is None
        ):
            self.multiversion_constants = None
        self.include_last_patch = True

    @classmethod
    def with_cmd(cls, resmoke_cmd: str) -> ResmokeProxy:
        """
        Create an instance of ResmokeProxy that invokes the given command.

        :param resmoke_cmd: Command to invoke resmoke.
        :return: Instance of ResmokeProxy using the given command.
        """
        return cls([part.strip() for part in resmoke_cmd.split(" ")])

    def _lazy_load(self) -> None:
        """Import multiversionconstants from resmoke."""
        if self.multiversion_constants is None:
            cmd = self.resmoke_cmd
            file_name = "multiversion-config.yml"
            subcmd = f"multiversion-config --config-file-output={file_name}"
            if self.include_last_patch:
                subcmd += " --include-last-patch"
            cmd.append(subcmd)
            try:
                subprocess.run(" ".join(cmd), capture_output=True, check=True, shell=True)
            except subprocess.CalledProcessError as e:
                LOGGER.error(
                    "Error invoking resmoke",
                    exc_info=True,
                    stderr=e.stderr.decode(),
                    stdout=e.stdout.decode(),
                )
                LOGGER.error(
                    "This command should be run from the root of the mongo repo and the resmoke "
                    "virtualenv should be activated."
                )
                LOGGER.error(
                    "If you're running it from the root of the mongo repo and still seeing"
                    " this error, please reach out in #server-testing slack channel."
                )
                raise
            with open(file_name, "r") as file:
                config_contents = file.read()
            os.remove(file_name)
            self.multiversion_constants = MultiversionConfig(**yaml.safe_load(config_contents))
            LOGGER.debug(
                "Received multiversion constants from resmoke",
                multiversion_constants=self.multiversion_constants.dict(),
            )

    def get_multiversion_constants(self) -> MultiversionConfig:
        """
        Get the multiversion constants from resmoke.

        :return: Multiversion config.
        """
        self._lazy_load()
        assert self.multiversion_constants
        return self.multiversion_constants
