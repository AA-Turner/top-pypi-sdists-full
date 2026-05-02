from typing import Dict
from navconfig.logging import logging
from querysource.exceptions import DataNotFound as QSNotFound
from ..exceptions import ComponentError, DataNotFound
from .QSBase import QSBase


class SuiteCRM(QSBase):
    """
    SuiteCRM

    Overview

           This component captures the data from the SuiteCRM API to be
           processed and stored in Navigator.

       :widths: auto

    | type         |   Yes    |  Type of query                                                    |
    | username     |   Yes    |  Credential Username                                              |
    | password     |   Yes    |  Credential Password                                              |
    | main_url     |   Yes    |  URL Base of the API                                              |
    | module_name  |   Yes    |  Module to list                                                   |

    Return the entry list of module

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          SuiteCRM:
          # attributes here
        ```
    """
    _version = "1.0.0"

    type = "entry_list"
    _driver = "suitecrm"

    async def entry_list(self):
        try:
            resultset = await self._qs.entry_list()
            return resultset
        except QSNotFound as err:
            raise DataNotFound(f"CourseMerchant Not Found: {err}") from err
        except Exception as err:
            logging.exception(err)
            raise ComponentError(f"CourseMerchant ERROR: {err!s}") from err
