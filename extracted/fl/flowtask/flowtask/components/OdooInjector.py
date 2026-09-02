import asyncio
import math
from collections.abc import Callable
from urllib.parse import urljoin
import numpy as np
import pandas as pd
from ..interfaces.flow import FlowComponent
from ..interfaces.http import HTTPService
from ..exceptions import ComponentError, TaskError


class OdooInjector(HTTPService, FlowComponent):
    """
    OdooInjector

        Overview

            The OdooInjector class is a component for injecting data into an Odoo server.
            This component takes data from a Pandas DataFrame (or a direct list of dicts),
            formats it as payload, and sends it to an Odoo endpoint specified in the
            credentials.

            Two authentication methods are supported:

            **APIKEY** (Odoo v16 and earlier):
            Pass an ``APIKEY`` credential. The component sends an ``api-key`` header.

            **Bearer Token** (Odoo v18+, e.g. Assurant):
            Pass a ``BEARER_TOKEN`` credential. The component sends an
            ``Authorization: Bearer <token>`` header.

            **Precedence rule**: when both ``APIKEY`` and ``BEARER_TOKEN`` are present,
            ``APIKEY`` takes precedence. If neither is provided, ``start()`` raises a
            ``ComponentError`` before any HTTP call.

        :widths: auto

            | credentials    |   Yes    | A dictionary containing connection details for the Odoo server:          |
            |                |          | "HOST", "PORT", "INJECTOR_URL", and either "APIKEY" or "BEARER_TOKEN". |
            | model          |   Yes    | The Odoo model into which data will be injected.                         |
            | headers        |   No     | Optional headers for the API request. Set automatically from auth creds. |
            | data           |   Yes    | The data to inject (list of dicts or DataFrame via pipeline predecessor). |

        Returns

            This component returns a Boolean indicating whether the data injection was
            successful. In case of errors, detailed logging is provided and an exception
            is raised with the error message. The component tracks successful API
            interactions and logs any unsuccessful payload deliveries.

        Example:

        ```yaml
        # Using APIKEY (Odoo v16 and earlier)
        OdooInjector:
          credentials:
            APIKEY: ODOO_APIKEY
            HOST: ODOO_HOST
            PORT: ODOO_PORT
            INJECTOR_URL: ODOO_INJECTOR_URL
          model: fsm.location
          chunk_size: 10

        # Using Bearer Token (Odoo v18+, e.g. Assurant)
        OdooInjector:
          credentials:
            BEARER_TOKEN: ODOO_ASSURANT_BEARER_TOKEN
            HOST: ODOO_ASSURANT_HOST
            PORT: ODOO_ASSURANT_PORT
            INJECTOR_URL: ODOO_INJECTOR_URL
          model: res.users
          chunk_size: 10
        ```
    """
    _version = "1.1.0"

    accept: str = "application/json"
    auth_type: str = "api_key"
    download = None
    chunk_size: int = 2000
    _credentials: dict = {
        "HOST": str,
        "PORT": str,
        "INJECTOR_URL": str,
        "APIKEY": str,
        "BEARER_TOKEN": str,
    }

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        super().__init__(
            loop=loop,
            job=job,
            stat=stat,
            **kwargs
        )

    async def start(self, **kwargs):
        if self.previous and isinstance(self.input, pd.DataFrame):
            self.data = self.split_chunk_df(self.input, self.chunk_size)
        elif isinstance(getattr(self, 'data', None), list):
            self.data = self.split_chunk_df(pd.DataFrame(self.data), self.chunk_size)

        self.processing_credentials()

        if self.credentials.get("APIKEY"):
            self.headers = {"api-key": self.credentials["APIKEY"]}
        elif self.credentials.get("BEARER_TOKEN"):
            self.headers = {"Authorization": f"Bearer {self.credentials['BEARER_TOKEN']}"}
        else:
            raise ComponentError(
                "Either APIKEY or BEARER_TOKEN must be provided in credentials"
            )

        self.url = self.get_url()

        return True

    async def run(self):
        total_rows = 0
        error_count = 0
        errors = []

        for idx, chunk in enumerate(self.data):
            payload = self.get_payload(chunk.to_dict(orient="records"))

            try:
                self._logger.info(f"Sending chunk {idx} ...")
                result, error = await self.session(
                    url=self.url, method="post", data=payload, use_json=True
                )

                if isinstance(result, dict) and result.get("ids"):
                    self._logger.debug(result)
                    total_rows += len(result["ids"])
                else:
                    self._logger.error(f"Chunk {idx} failed: result: {result} :: error: {error}")
                    error_count += len(chunk)  # Assuming the whole chunk failed
                    errors.append(f"Chunk {idx} failed with error: {error}")

            except Exception as e:
                self._logger.error(f"Error while sending chunk {idx}: {str(e)}. Continuing with next chunk...")
                error_count += len(chunk)  # Assuming the whole chunk failed
                errors.append(f"Chunk {idx} exception: {str(e)}")

        # Register metrics
        self.add_metric("PROCESSED ROWS", total_rows)
        self.add_metric("FAILED ROWS", error_count)

        # Raise error if there were any failures
        if errors:
            errors.append(f"PROCESSED ROWS: {total_rows}, FAILED ROWS: {error_count}")
            raise TaskError("\n".join(errors))

        return True


    async def close(self):
        return True

    def get_url(self):
        port = (
            f":{self.credentials['PORT']}" if self.credentials["PORT"] != "80" else ""
        )
        base_url = f"{self.credentials['HOST']}{port}"
        url = urljoin(base_url, self.credentials["INJECTOR_URL"])
        return url

    def get_payload(self, chunk_data):
        return {
            "model": self.model,
            "options": {
                # 'has_headers': True,
                "advanced": False,
                "keep_matches": False,
                "name_create_enabled_fields": getattr(self, "name_create_enabled_fields", {}),
                "import_set_empty_fields": [],
                "import_skip_records": [],
                "fallback_values": {},
                "skip": 0,
                "limit": self.chunk_size,
                # 'encoding': '',
                # 'separator': '',
                "quoting": '"',
                # 'sheet': 'Sheet1',
                "date_format": "",
                "datetime_format": "",
                "float_thousand_separator": ",",
                "float_decimal_separator": ".",
                "fields": [],
            },
            "data": chunk_data,
        }

    def split_chunk_df(self, df: pd.DataFrame, chunk_size: int):
        """
        Splits a DataFrame into chunks of a specified size.

        Parameters:
        df (pd.DataFrame): The DataFrame to be split.
        chunk_size (int): The maximum number of rows per chunk.

        Returns:
        list: A list of DataFrame chunks.
            If the DataFrame is empty, returns an empty list.
        """
        if df.empty:
            return []

        split_n = math.ceil(len(df) / chunk_size)

        # Split into chunks of n rows
        return np.array_split(df, split_n)  # Returns list of DataFrames
