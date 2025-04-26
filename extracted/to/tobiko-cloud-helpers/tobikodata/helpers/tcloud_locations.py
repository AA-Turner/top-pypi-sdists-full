import os
import site
import sys
from pathlib import Path

DEFAULT_PYTHON_VERSION = f"{sys.version_info[0]}.{sys.version_info[1]}"
TCLOUD_PYTHON_PATH_ENV_VAR = "TCLOUD_PYTHON_PATH"
TCLOUD_PATH = Path(os.environ.get("TCLOUD_HOME", Path.home() / ".tcloud"))


def get_unpack_path(
    version: str,
    tcloud_path: Path = TCLOUD_PATH,
    python_version: str = DEFAULT_PYTHON_VERSION,
) -> Path:
    return Path(tcloud_path) / "artifacts" / version / "executors" / python_version


def get_unpacked_site_packages_path(
    version: str,
    tcloud_path: Path = TCLOUD_PATH,
    python_version: str = DEFAULT_PYTHON_VERSION,
) -> Path:
    path = get_unpack_path(version, tcloud_path, python_version)
    return path / "lib" / f"python{python_version}" / "site-packages"


def get_default_python_path() -> str:
    return ":".join(site.getsitepackages())
