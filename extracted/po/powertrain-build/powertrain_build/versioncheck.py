# Copyright 2024 Volvo Car Corporation
# Licensed under Apache 2.0.

"""Version compatibility check."""

import re

from powertrain_build import __config_version__


class Version:
    """Class encapsulating version numbers."""

    _RE = re.compile(r'^([0-9]+)\.([0-9]+)\.([0-9]+)$')
    _app_version = (0, 0, 0)

    def __init__(self, version):
        """Init."""
        if isinstance(version, float):
            version = f'{version}.0'
        elif isinstance(version, int):
            version = f'{version}.0.0'
        if isinstance(version, str):
            match = Version._RE.match(version)
            if match:
                self._version = (int(match.group(1)), int(match.group(2)), int(match.group(3)))
            else:
                raise ValueError(f'Not a valid version string: {version}')
        else:
            raise ValueError(f'Not a valid version: {version}')

    def __len__(self):
        """Get length of object."""
        return 3

    def __getitem__(self, i):
        """Get item with index i."""
        return self._version[i]

    @classmethod
    def is_compatible(cls, version):
        """Check version compatibility.

        Args:
            version (str/int/float): The version to be compared with the version of powertrain_build.

        Returns:
            bool: True/False based on version compatibility.

        Raises:
            ValueError: If the provided version is not a valid version string, integer, or float.
        """
        version_is_compatible = False
        if version is not None:
            version_cls = Version(version)

            check_major = cls._app_version[0] == version_cls[0]
            check_minor = cls._app_version[1] >= version_cls[1]
            check_patch = cls._app_version[2] >= version_cls[2]

            version_is_compatible = check_major and check_minor and check_patch

        return version_is_compatible


Version._app_version = Version(__config_version__)
