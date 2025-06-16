# Raise warnings for python versions that are not tested
import platform

from packaging import version

from ._logger import logger

py_version = version.parse(platform.python_version())


def py_version_warning(min_v: str, max_v: str):
    """Print warning for python versions that are not tested in CI."""
    max_v_plus_1 = (
        ".".join(max_v.split(".")[:-1]) + "." + str(int(max_v.split(".")[-1]) + 1)
    )

    if py_version >= version.parse(max_v_plus_1) or py_version < version.parse(min_v):
        logger.warning(
            f"You are running {py_version}\nOnly python versions {min_v}~"
            f"{max_v} are currently tested, use at your own risk."
        )
