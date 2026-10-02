import inspect
import logging
import os
import sys
import urllib.request
import warnings
from pathlib import Path
from time import time
from types import ModuleType
from typing import Any

from azlocal import __version__
from azlocal.constants import LOCALSTACK_HOST_ENV, get_localstack_host

ENV_AZURE_AUTHORITY_HOST = "AZURE_AUTHORITY_HOST"

HEALTH_CHECK_TIMEOUT = 5
# Identifies the health requests that originate from the Python SDK, to distinguish them from
# the requests made by the `azlocal`/`azdlocal` CLI wrappers
HEALTH_CHECK_USER_AGENT = f"azlocal-python-sdk/{__version__}"

LOG = logging.getLogger(__name__)


class EmulatorNotAvailableError(RuntimeError):
    """Raised when the LocalStack Emulator does not respond on the configured host."""


def check_emulator_is_running() -> None:
    """
    Verify that the LocalStack Emulator responds on the configured host.

    :raises EmulatorNotAvailableError: if the health endpoint cannot be reached, or does not return a 200
    """
    health_endpoint = f"{get_localstack_host()}/_localstack/health"
    error_hint = (
        f"Error: LocalStack Emulator did not respond on {health_endpoint}!\n"
        f"Make sure that the LocalStack Emulator is running, or configure the correct endpoint using the {LOCALSTACK_HOST_ENV} environment variable."
    )
    request = urllib.request.Request(health_endpoint, headers={"User-Agent": HEALTH_CHECK_USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=HEALTH_CHECK_TIMEOUT) as response:
            if response.status != 200:
                raise EmulatorNotAvailableError(
                    f"{error_hint}\nThe health endpoint returned status {response.status}."
                )
    # OSError covers urllib.error.URLError (connection/TLS failures), urllib.error.HTTPError (non-2xx
    # responses, as it is a subclass of URLError) and the TimeoutError raised by the socket itself
    except OSError as e:
        raise EmulatorNotAvailableError(error_hint) from e


class PythonLocalSdk:
    def __init__(self) -> None:
        self._started = False

        self._clients_to_mock = self._find_azure_mgmt_clients()
        self._default_worldwide_endpoint: str | None = None
        self._existing_authority_host: str | None = None

    def start_interception(self) -> None:
        """
        Start intercepting all Azure requests.

         Invoking this method will:
          - inspect the current modules
          - load all `azure.mgmt` modules
          - find the latest client in every module
          - update the client to point to the LocalStack host

        Use the environment variable `LOCALSTACK_HOST` to configure the host.

        .. warning
              This only affects Clients that are created after this method is invoked

        :raises EmulatorNotAvailableError: if the LocalStack Emulator is not running on the configured host
        :return:
        """
        if self._started:
            LOG.debug("start_interception already started - ignoring")
            return

        # Only patch anything if the Emulator is actually up - otherwise the SDK would silently
        # point every client at an endpoint that does not exist
        check_emulator_is_running()

        # Set custom login endpoint
        # There are two ways that Azure SDK Clients determine which endpoint to call to login:
        #  - Using an environment variable
        #  - Using hardcoded values in the 'msal' module
        # Which method is used depends on the SDK, so we override both to be sure
        self._existing_authority_host = os.environ.get(ENV_AZURE_AUTHORITY_HOST)
        os.environ[ENV_AZURE_AUTHORITY_HOST] = get_localstack_host()
        try:
            from msal import authority  # type: ignore[import-untyped,import-not-found]

            self._default_worldwide_endpoint = authority.WORLD_WIDE
            authority.WORLD_WIDE = get_localstack_host().replace("https://", "")
        except ImportError:
            warnings.warn(
                "Unable to import 'msal' - Authorization calls will not be intercepted", stacklevel=2
            )

        # Use Custom Client
        custom_endpoint = get_localstack_host()
        for client in self._clients_to_mock:
            self.prepare_client_for_interception(client, custom_endpoint)

        self._started = True

    def stop_interception(self) -> None:
        if not self._started:
            LOG.debug("stop_interception already stopped - ignoring")
            return

        # Instrument client to stop interception
        for client in self._clients_to_mock:
            self.revert_client_interception(client)

        # Revert the login endpoints
        if self._existing_authority_host:
            os.environ[ENV_AZURE_AUTHORITY_HOST] = self._existing_authority_host
        if self._default_worldwide_endpoint:
            from msal import authority

            authority.WORLD_WIDE = self._default_worldwide_endpoint

        self._started = False

    def _find_azure_mgmt_clients(self) -> list[Any]:
        """
        Finds a list of all SDK clients that are defined in the `azure.mgmt` namespace.

        :return: A list of classes: [CosmosManagementClient, StorageManagementClient, ..]
        """

        from azure import mgmt  # type: ignore[import-untyped]  # noqa

        azure_mod = sys.modules["azure.mgmt"]
        azure_path = azure_mod.__path__

        clients = []

        total_start_time = time()

        for p in azure_path:
            mgmt_modules = sorted(os.listdir(p))

            for module_name in mgmt_modules:
                module = self._import_module(module_name)

                if module and hasattr(module, "__all__"):
                    for attr_name in module.__all__:
                        if attr_name.endswith("Client"):
                            clients.append(getattr(module, attr_name))

                # some modules (datalake, rdbms, resource, maybe others) use have several clients in subdirectories
                sub_modules = sorted(os.listdir(os.path.join(p, module_name)))

                for submodule_name in sub_modules:
                    if not Path(os.path.join(p, module_name, submodule_name)).is_dir():
                        continue
                    submodule = self._import_module(module_name, submodule_name)

                    if submodule and hasattr(submodule, "__all__"):
                        for attr_name in submodule.__all__:
                            if attr_name.endswith("Client"):
                                clients.append(getattr(submodule, attr_name))

        LOG.debug("PythonSDK: finding all clients took \t%s s", (time() - total_start_time))

        return clients

    def _import_module(self, module_name: str, submodule_name: str | None = None) -> ModuleType | None:
        if submodule_name and submodule_name.startswith("_"):
            return None
        module_location = (
            f"azure.mgmt.{module_name}.{submodule_name}" if submodule_name else f"azure.mgmt.{module_name}"
        )
        try:
            module_start_time = time()
            module = __import__(module_location, fromlist=["__init__"])
        except ModuleNotFoundError:
            LOG.debug("PythonSDK: unable to import module %s", module_location)
            return None
        LOG.debug("PythonSDK: importing %s took: \t%s s", module_location, (time() - module_start_time))
        return module

    @staticmethod
    def prepare_client_for_interception(client: Any, custom_endpoint: str) -> None:
        # There are three ways for a client to determine which endpoint to call
        # 1. Provided by the user: AzureServiceClient(base_url="..")
        # 2. Determined by the AzureCloud that is configured (env variable AZURE_CLOUD=AZURE_PUBLIC_CLOUD/AZURE_CHINA_CLOUD
        # 3. Use a hardcoded default
        #
        # Solutions:
        # 1. Asking the user to configure the base_url manually. Very laborious and prone to errors
        # 2. Override the AzureCloud. This is not feasible for a few reasons:
        #    - We can pass in an env variable, but there are only three Azure Clouds (Public/US GOV/China)
        #    - We cannot override the available AzureClouds, as that is an Enum (which is immutable by design)
        #    - We cannot override the method used to determine the endpoint
        #      1. Location of this method: from azure.mgmt.core.tools import get_arm_endpoints
        #      2. This is typically already imported at the top, so each client already has a direct reference to the `get_arm_endpoints` method.
        #         Overriding the method in the `azure.mgmt.core.tools`-module has therefore no effect.
        #
        # 3. We _can_ override the hardcoded default - which is what we do here

        # Determine (and store) the existing default values for the `__init__`-method
        # This is either None or a tuple
        # If a parameter does not have a default value, it is not part of the tuple - so the length of this list is not guaranteed the same as the number of parameters
        # __init__(a, b = None, c = "sth") --> _defaults__ == (None, "sth")
        client.__init__.__olddefaults = client.__init__.__defaults__

        if not client.__init__.__olddefaults:
            return

        # Get the default values as a dictionary
        # We skip the 'empty' Parameters, so parameters without a default value
        # __init__(a, b = None, c = "sth") --> [("b", None), ("c", "sth")]
        # We have to ignore Keyword-Only parameters, as those are not part of the __defaults__ tuple and the base_url is always a positional parameter
        # We ran into a bug where Azure added a keyword only parameter to the __init__ in some clients which broke our previous logic
        client_signature = inspect.signature(client.__init__)
        init_params = [
            (name, value.default)
            for name, value in client_signature.parameters.items()
            if value.default != inspect.Parameter.empty
            and value.kind in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.POSITIONAL_ONLY)
        ]

        updated_default_values = tuple(
            custom_endpoint if name == "base_url" else value for name, value in init_params
        )
        LOG.debug("Configured base_url for %s to be %s", client, custom_endpoint)

        client.__init__.__defaults__ = updated_default_values

    @staticmethod
    def revert_client_interception(client: Any) -> None:
        LOG.debug("Reverting base url of %s...", client)
        client.__init__.__defaults__ = client.__init__.__olddefaults
