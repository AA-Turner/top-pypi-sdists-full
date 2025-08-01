# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
from dataclasses import dataclass
from functools import cached_property
from collections import namedtuple

from contrast.agent import scope

from contrast_vendor.importlib_metadata import metadata, PackageMetadata
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

Version = namedtuple("Version", ["major", "minor", "patch"])
DEFAULT_FRAMEWORK = "wsgi"
SUPPORTED_SERVERS = ["uwsgi", "gunicorn", "uvicorn", "mod_wsgi"]
DEFAULT_SERVER = "Unknown"


class DiscoverablePackage:
    def __init__(self, framework_name, default_package):
        self._name = ""
        self.version = None
        self.packages = framework_name if framework_name else DEFAULT_FRAMEWORK
        self.default_package = default_package
        self.set_info()

    @property
    def name(self):
        return self._name.capitalize()

    @property
    def name_lower(self):
        return self._name.lower()

    @property
    def full_version(self):
        return f"{self.version.major}.{self.version.minor}.{self.version.patch}"

    def set_info(self):
        raise NotImplementedError("Must implement set_info")

    def discover_server(self) -> PackageMetadata | None:
        """
        Except in the agent's own testing environment, the assumption here is
        that all environments using the agent will have only
        one supported framework or server.
        """
        with scope.contrast_scope():
            for framework_name in self.packages:
                try:
                    return metadata(framework_name)
                except Exception:  # noqa: PERF203
                    continue

        return None

    def __repr__(self):
        return f"{self.name} {self.full_version}"


class _ServerTypeFramework(DiscoverablePackage):
    """
    Unless you're reporting server type on startup, use `Framework` instead.

    This is only kept because it is used as the server type sent on startup, which the backend includes in
    its server identifier. It's not displayed anywhere in the UI, but changing this value would create new
    servers, leading to loss of settings, more license usage, and more pressure on the backend.
    """

    def __init__(self, framework_name):
        super().__init__(framework_name, DEFAULT_FRAMEWORK)

    def discover_framework(self, framework_name: str) -> PackageMetadata | None:
        """
        Except in the agent's own testing environment, the assumption here is
        that all environments using the agent will have only
        one supported framework or server.
        """
        with scope.contrast_scope():
            try:
                return metadata(framework_name)
            except Exception:
                return None

    def set_info(self):
        framework_metadata = (
            self.discover_framework(self.packages) if self.packages != "wsgi" else None
        )
        if framework_metadata:
            version = framework_metadata.get("Version").split(".")
            patch = version[2] if len(version) > 2 else "0"
            self.version = Version(major=version[0], minor=version[1], patch=patch)
            self._name = framework_metadata.get("Name")
        else:
            self._name = "wsgi"
            self.version = Version(major="0", minor="0", patch="0")


class Server(DiscoverablePackage):
    """
    A class to store information about the current web server used in an application
    """

    def __init__(self):
        super().__init__(SUPPORTED_SERVERS, DEFAULT_SERVER)

    def set_info(self):
        server_metadata = self.discover_server()
        if server_metadata:
            version = server_metadata.get("Version").split(".")
            patch = version[2] if len(version) > 2 else "0"
            self.version = Version(major=version[0], minor=version[1], patch=patch)
            self._name = server_metadata.get("Name")
        else:
            logger.debug(
                "Did not find the current %s. Assuming it's %s.",
                self.__class__.__name__,
                self.default_package,
            )
            self._name = self.default_package
            self.version = Version(major="0", minor="0", patch="0")


@dataclass
class Framework:
    name: str

    def __post_init__(self):
        self.name = self.name.capitalize()

    @cached_property
    def version(self) -> Version | None:
        """
        Get the version of the package by its distribution name.
        """
        if self == UNKNOWN_FRAMEWORK:
            return None
        if dist := metadata(self.name):
            version_parts = dist.get("Version", "0.0.0").split(".")
            return Version(
                major=version_parts[0],
                minor=version_parts[1],
                patch=version_parts[2] if len(version_parts) > 2 else "0",
            )
        return None

    def __str__(self):
        return (
            f"{self.name} {self.version.major}.{self.version.minor}.{self.version.patch}"
            if self.version
            else self.name
        )


UNKNOWN_FRAMEWORK = Framework("UNKNOWN")
