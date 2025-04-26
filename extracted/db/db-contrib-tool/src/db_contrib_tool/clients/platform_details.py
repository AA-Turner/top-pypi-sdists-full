"""A client to proxy platform details."""

import platform

import distro


class PlatformDetailsClient:
    """A client to get details about the platform being run on."""

    @staticmethod
    def get_platform_system() -> str:
        """
        Get the system that is being run on.

        :return: System name.
        """
        return platform.system()

    @staticmethod
    def get_distro_id() -> str:
        """
        Get the id of the distro being run on.

        :return: Distro id.
        """
        return distro.id()

    @staticmethod
    def get_distro_major_version() -> str:
        """
        Get the major version of the distro being run on.

        :return: Distro major version.
        """
        return distro.major_version()

    @staticmethod
    def get_distro_minor_version() -> str:
        """
        Get the minor version of the distro being run on.

        :return: Distro minor version.
        """
        return distro.minor_version()
