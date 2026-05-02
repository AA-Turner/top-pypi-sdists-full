import asyncio
import pandas as pd
from collections.abc import Callable
from urllib.parse import urljoin
from io import StringIO
from navconfig.logging import logging
from .flow import FlowComponent
from ..interfaces.http import HTTPService
from ..exceptions import ComponentError

class DialPad(FlowComponent, HTTPService):
    """
    DialPad

    Overview

        The DialPad class is a component for interacting with the DialPad API. It extends the FlowComponent and HTTPService
        classes, providing methods for authentication, fetching statistics, and handling API responses.

    :widths: auto

        | accept           |   No     | The accepted content type for API responses, defaults to "application/json".                     |
        | download         |   No     | The download flag indicating if a file download is required.                                     |
        | _credentials     |   Yes    | A dictionary containing the API key for authentication.                                          |
        | _base_url        |   Yes    | The base URL for the DialPad API.                                                                |
        | auth             |   Yes    | The authentication header for API requests.                                                      |
    Return

        The methods in this class manage the interaction with the DialPad API, including initialization, fetching statistics,
        processing results, and handling credentials.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          DialPad:
          # attributes here
        ```
    """
    _version = "1.0.0"
    accept: str = "text/csv"
    download = None
    _credentials: dict = {"APIKEY": str}

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        FlowComponent.__init__(self, loop=loop, job=job, stat=stat, **kwargs)
        HTTPService.__init__(self, **kwargs)

    async def start(self, **kwargs):
        self._base_url = "https://dialpad.com/api/v2/"

        self.processing_credentials()
        self.auth = {"apikey": self.credentials["APIKEY"]}

        if self.previous:
            self.data = self.input
        else:
            self.data = None
        return True

    async def dialpad_stats(self):
        # processing statistics asynchronously
        self.accept: str = "application/json"
        stats_url = urljoin(self._base_url, "stats/")
        processing_result, _ = await self.session(
            stats_url, "post", data=self.body_params, use_json=True
        )
        request_id = processing_result.get("request_id")

        count = 0
        while True:
            get_result_url = urljoin(stats_url, request_id)
            response_result, _ = await self.session(get_result_url, use_json=True)
            file_url = response_result.get("download_url", None)
            if file_url or count > 60:
                break
            count += 1
            logging.debug(f"Try: {count!s}")
            await asyncio.sleep(10)

        self.accept: str = "text/csv"
        self.download = False
        result, _ = await self.session(file_url)
        df_results = await self.from_csv(StringIO(result))
        return df_results

    async def dialpad_send_sms(self):
        # send SMS message
        url = urljoin(self._base_url, "sms")
        from_number = self.body_params.get("from_number")
        to_numbers = self.body_params.get("to_numbers")
        text = self.body_params.get("text")

        if self.data is not None and not self.data.empty:
            if text in self.data.columns:
                text = self.data.get(text).iloc[0]
            if from_number in self.data.columns:
                from_number = self.data.get(from_number).iloc[0]
            if not isinstance(to_numbers, list):
                if isinstance(to_numbers, str):
                    if to_numbers in self.data.columns:
                        to_numbers = self.data[to_numbers].tolist()
                    else:
                        to_numbers = [to_numbers]

        payload = {
            "infer_country_code": True,
            "text": text,
            "from_number": from_number,
            "to_numbers": to_numbers
        }

        self.accept: str = "application/json"
        stats_url = urljoin(self._base_url, "sms")
        result, _ = await self.session(
            stats_url, "post", data=payload, use_json=True
        )

        df_results = pd.DataFrame([result])
        return df_results

    async def run(self):
        try:
            method = getattr(self, f"dialpad_{self.type}")
        except AttributeError as ex:
            raise ComponentError(f"{__name__}: Wrong 'type' on task definition") from ex
        result = await method()
        self._result = result
        print(self._result)
        if self._debug:
            columns = list(self._result.columns)
            print(f"Debugging: {self.__name__} ===")
            for column in columns:
                t = self._result[column].dtype
                print(column, "->", t, "->", self._result[column].iloc[0])
        return self._result

    async def close(self):
        pass
