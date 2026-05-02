import asyncio
from collections.abc import Callable
from ..interfaces.AzureClient import AzureClient
from ..interfaces.http import HTTPService
from .flow import FlowComponent


class Azure(AzureClient, HTTPService, FlowComponent):
    """
    Azure Component.

        Overview

        This component interacts with Azure services using the Azure SDK for Python.
        It requires valid Azure credentials to establish a connection.

        :widths: auto

    |  credentials (optional)  |   Yes    | Dictionary containing Azure credentials: "client_id", "tenant_id",         |
    |                          |          | and "client_secret". Credentials can be retrieved from environment         |
    |                          |          | variables.                                                                 |
    |  as_dataframe (optional) |    No    | Specifies if the response should be converted to a pandas DataFrame        |
    |                          |          | (default: False).                                                          |

        This component does not return any data directly. It interacts with
        Azure services based on the configuration and potentially triggers
        downstream components in a task.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Azure:
          # attributes here
        ```
    """
    _version = "1.0.0"
    accept: str = "application/json"
    no_host: bool = True

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.as_dataframe: bool = kwargs.get("as_dataframe", False)
        # Initialize parent classes explicitly
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        if 'secret_id' in self.credentials:
            self.credentials['client_secret'] = self.credentials.pop('secret_id')

    async def close(self, timeout: int = 5):
        """close.
        Closing the connection.
        """
        pass

    async def open(self, host: str, port: int, credentials: dict, **kwargs):
        """open.
        Starts (open) a connection to external resource.
        """
        self.app = self.get_msal_app()
        return self

    async def start(self, **kwargs):
        """Start.

        Processing variables and credentials.
        """
        await super(Azure, self).start(**kwargs)
        self.processing_credentials()
        try:
            self.client_id, self.tenant_id, self.client_secret = (
                self.credentials.get(key)
                for key in ["client_id", "tenant_id", "client_secret"]
            )
        except Exception as err:
            self._logger.error(err)
            raise

        return True
