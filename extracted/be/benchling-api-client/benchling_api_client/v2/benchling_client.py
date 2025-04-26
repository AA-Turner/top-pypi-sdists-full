from abc import ABC, abstractmethod
from importlib.metadata import version
import sys
from typing import Dict

import attr

from benchling_api_client.v2.client import Client


class AuthorizationMethod(ABC):
    """An abstract class that defines how the Benchling Client will authorize with the server."""

    @abstractmethod
    def get_authorization_header(self, base_url: str) -> str:
        """
        Return a string that will be passed to the HTTP Authorization request header.

        The returned string is expected to contain both the scheme (e.g. Basic, Bearer) and parameters.
        """


@attr.s(auto_attribs=True)
class BenchlingApiClient(Client):
    auth_method: AuthorizationMethod
    _package: str = attr.ib(init=False, default="benchling-api-client")
    _user_agent: str = attr.ib(init=False, default="BenchlingAPIClient")

    @staticmethod
    def _get_user_agent(user_agent_name: str, package: str) -> str:
        python_version = ".".join(
            [str(x) for x in (sys.version_info.major, sys.version_info.minor, sys.version_info.micro)]
        )
        try:
            package_version = version(package)
        except:
            package_version = "Unknown"
        return f"{user_agent_name}/{package_version} (Python {python_version})"

    def get_headers(self) -> Dict[str, str]:
        """Get headers to be used in authenticated endpoints."""
        return {
            "User-Agent": self._get_user_agent(self._user_agent, self._package),
            "Authorization": self.auth_method.get_authorization_header(self.base_url),
        }
