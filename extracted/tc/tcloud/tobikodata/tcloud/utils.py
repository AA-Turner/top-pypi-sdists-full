from pathlib import Path

import tobikodata.tcloud.constants as c


def get_unpack_path(
    version: str,
    tcloud_path: Path = c.TCLOUD_PATH,
    python_version: str = c.DEFAULT_PYTHON_VERSION,
) -> Path:
    return Path(tcloud_path) / "artifacts" / version / "executors" / python_version


def get_unpacked_site_packages_path(
    version: str,
    tcloud_path: Path = c.TCLOUD_PATH,
    python_version: str = c.DEFAULT_PYTHON_VERSION,
) -> Path:
    path = get_unpack_path(version, tcloud_path, python_version)
    return path / "lib" / f"python{python_version}" / "site-packages"
