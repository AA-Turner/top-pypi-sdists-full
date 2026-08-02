import logging
import os
import subprocess
import sys

from python_agent import (
    __version__ as CURRENT_VERSION,
    __package_name__ as PACKAGE_NAME,
)
from python_agent.common.http.backend_proxy import BackendProxy
from python_agent.packages import semantic_version

log = logging.getLogger(__name__)


class StatusCodes:
    SUCCESS = 0
    ERROR = 1
    NO_MATCHES_FOUND = 23


class AutoUpgrade(object):
    def __init__(self, config_data):
        self.backend_proxy = BackendProxy(config_data)
        self.config_data = config_data

    def get_recommended_version(self):
        response = self.backend_proxy.get_recommended_version(self.config_data)
        if not response:
            return None, self.get_current_version()
        agent = response.get("agent", {})
        version = agent.get("version")
        url = agent.get("url")
        log.info("Recommended Agent Version: %s" % version)
        return url, semantic_version.Version(version)

    def get_current_version(self):
        try:
            current_version = semantic_version.Version(CURRENT_VERSION)
            return current_version
        except Exception:
            log.warning("Failed Getting Current Version. Pkg. %s" % PACKAGE_NAME)
        return semantic_version.Version("0.0.0")

    def upgrade(self):
        current_version = self.get_current_version()
        log.info("Current Agent Version: %s" % current_version)
        url, recommended_version = self.get_recommended_version()
        status = StatusCodes.NO_MATCHES_FOUND
        if recommended_version != current_version:
            log.info(
                "Current version %s is different from recommended version %s",
                current_version,
                recommended_version,
            )
            if self.is_version_exists_in_pypi(recommended_version):
                log.info("Found the version in pypi. Starting to install.")
                status = self.install_and_restart(
                    PACKAGE_NAME + "==" + str(recommended_version)
                )
            else:
                log.warn("Version wasn't found in pypi. Upgrade is skipped.")
        elif url:
            status = self.install_and_restart(url)
        return status

    def restart(self):
        os.execl(sys.executable, *([sys.executable] + sys.argv))

    def install_and_restart(self, recommended_version):
        status = StatusCodes.ERROR
        try:
            log.info("Installing Agent Version: %s" % recommended_version)
            status = subprocess.call(
                [
                    sys.executable,
                    "-m",
                    "pip",
                    "install",
                    recommended_version,
                    "--ignore-installed",
                ]
            )
            if status == StatusCodes.SUCCESS:
                log.info(
                    "Upgraded Agent Successfully. Restarting Agent With Version: %s"
                    % recommended_version
                )
                self.restart()
            return status
        except SystemExit as e:
            log.info("Failed Upgrading Or Restarting Agent. System Exit: %s" % str(e))
            return StatusCodes.ERROR
        except Exception as e:
            log.info("Failed Upgrading Or Restarting Agent. Error: %s" % str(e))
            return StatusCodes.ERROR

    def is_version_exists_in_pypi(self, recommended_version):
        return self.backend_proxy.check_version_exists_in_pypi(recommended_version)
