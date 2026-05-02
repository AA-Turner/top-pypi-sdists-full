import asyncio
import pandas as pd
from collections.abc import Callable
from ..utils import is_empty
from ..exceptions import ComponentError, DataNotFound
from .DownloadFrom import DownloadFromBase
from ..interfaces.d2l import D2LClient

class DownloadFromD2L(D2LClient, DownloadFromBase):
    """
    DownloadFromD2L

    Overview

        Download Data from D2L.

    Properties (inherited from D2LClient and DownloadFromBase)

        :widths: auto

        | credentials        |   Yes    | Credentials to establish connection with Polestar site (user and password)       |
        |                    |          | get credentials from environment if null.                                        |
        | filename           |   Yes    | The filename to use for the downloaded file.                                     |
        | Action             |   No     | Select 'download' or 'awards'. (Default: download)                               |
        | schema             |   No     | The ID of the Schema to download. Required if action is 'download'               |
        | org_units          |   No     | A list of ID of Organization Units. Required if action is 'awards'               |
        | column             |   No     | A column name to extract the list of Organization Units. Required if action is   |
        |                    |          | 'awards' and depends of a Pandas DataFrame.                                      |
        | create_destination |   No     | Boolean flag indicating whether to create the destination directory if it        |
        |                    |          | doesn't exist (default: True).                                                   |

        Save the downloaded files on the new destination.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          DownloadFromD2L:
          domain: POLESTAR_DOMAIN
          schema: c0b0740f-896e-4afa-bfd9-81d8e43006d9
          credentials:
          username: POLESTAR_USERNAME
          password: POLESTAR_PASSWORD
          destination:
          directory: /home/ubuntu/symbits/polestar/files/organizational_unit_ancestors/
          filename: organizational_unit_ancestors_{yesterday}.zip
          overwrite: true
          masks:
          yesterday:
          - yesterday
          - mask: '%Y-%m-%d'
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        self.action = kwargs.get('action', 'download')
        if self.action == 'awards':
            if hasattr(self, 'org_units'):
                self.data = self.org_units
            elif self.previous:
                if not isinstance(self.input, pd.DataFrame):
                    raise ComponentError(
                        "DownloadFromD2L: Incompatible Pandas Dataframe", status=404
                    )
                else:
                    if not hasattr(self, 'column'):
                        raise ComponentError(
                            'DownloadFromD2L: requires a "column" Attribute'
                        )
                self.data = self.input[self.column].to_numpy()
        await self.get_bearer_token()
        await super(DownloadFromD2L, self).start(**kwargs)
        return True

    async def close(self):
        pass

    async def run(self):
        if self.action == 'download':
            await self.download_file()
            self._result = self.filename
            self.add_metric("D2L_FILE", self.filename)
            return self._result
        elif self.action == 'awards':
            self._result = await self.create_dataframe(await self.awards(org_units=self.data))
            if is_empty(self._result):
                raise DataNotFound(f"{self.__name__}: Data Not Found")
            return self._result
        else:
            raise ComponentError(
                'DownloadFromD2L: Action not defined'
            )
