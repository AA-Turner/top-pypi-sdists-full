import os
import platform
import PyInstaller.__main__
from pathlib import Path

ROOT = Path(__file__).parents[2].absolute()
HERE = Path(__file__).parent.relative_to(ROOT)
path_to_main = str(HERE / "cli.py")


def install() -> None:
    # this solves an issue on some python versions where the ipaddress module is not
    # added automatically.
    # See: https://github.com/pyinstaller/pyinstaller/issues/8912#issuecomment-2527548816
    PyInstaller.compat.PY3_BASE_MODULES.add("ipaddress")

    config_before = os.path.join("src", "db_contrib_tool", "config")
    config_after = os.path.join("db_contrib_tool", "config")

    bisect_scripts_before = os.path.join("src", "db_contrib_tool", "evg_aware_bisect", "*.sh")
    bisect_scripts_after = os.path.join("db_contrib_tool", "evg_aware_bisect")

    separator = ":"
    operating_system = platform.system().lower()
    if operating_system == "windows":
        separator = ";"

    PyInstaller.__main__.run(
        [
            path_to_main,
            "--onefile",
            "--name",
            "db-contrib-tool",
            # add configs
            "--add-data",
            f"{config_before}{separator}{config_after}",
            # add shell scripts for bisect tool
            "--add-data",
            f"{bisect_scripts_before}{separator}{bisect_scripts_after}",
        ]
    )
