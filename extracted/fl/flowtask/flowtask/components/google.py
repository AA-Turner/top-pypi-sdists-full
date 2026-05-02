from typing import Union
from collections.abc import Callable
from functools import partial
import asyncio
import aiohttp
import base64
import struct
from aiohttp.resolver import AsyncResolver
import pandas as pd
import ssl
from datamodel.parsers.json import json_encoder
from proxylists import check_address
from proxylists.proxies import (
    FreeProxy,
    Oxylabs
)
from ..conf import GOOGLE_PLACES_API_KEY
from ..exceptions import ComponentError
from ..components import FlowComponent


# Monkey-Patching for <3.11 TLS Support
setattr(
    asyncio.sslproto._SSLProtocolTransport,
    "_start_tls_compatible", True
)


class GoogleBase(FlowComponent):
    """
    GoogleBase.

        Overview: A base class for Google API components.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          GoogleBase:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self._type: str = kwargs.pop('type', None)
        self.api_key: str = kwargs.pop('api_key', GOOGLE_PLACES_API_KEY)
        self.use_proxies: bool = kwargs.pop('use_proxies', False)
        self.paid_proxy: bool = kwargs.pop('paid_proxy', False)
        # Chrome profile persistence support
        self.chrome_user_data_dir: str = kwargs.pop('chrome_user_data_dir', None)
        # Concurrency limit: 1 for persistent profiles, 10 for ephemeral
        concurrent_limit = kwargs.pop('concurrent_limit', 1 if self.chrome_user_data_dir else 10)
        super(GoogleBase, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        self.semaphore = asyncio.Semaphore(concurrent_limit)

    async def close(self):
        pass

    def _evaluate_input(self):
        if self.previous:
            self.data = self.input
        elif self.input is not None:
            self.data = self.input

    async def start(self, **kwargs):
        self._counter: int = 0
        self._evaluate_input()
        if not self._type:
            raise RuntimeError(
                'Google requires a Type Function'
            )
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Incompatible Pandas Dataframe", status=404
            )
        if not self.api_key:
            self.api_key = GOOGLE_PLACES_API_KEY
            if not self.api_key:
                raise ComponentError(
                    "Google API Key is missing", status=404
                )
        return True

    def _get_session_args(self) -> dict:
        """Get aiohttp Session arguments."""
        # Total timeout for the request
        timeout = aiohttp.ClientTimeout(total=20)
        resolver = AsyncResolver(
            nameservers=["1.1.1.1", "8.8.8.8"]
        )
        connector = aiohttp.TCPConnector(
            limit=100,
            resolver=resolver
        )
        return {
            "connector": connector,
            "timeout": timeout,
            "json_serialize": json_encoder,
            "trust_env": True
        }

    async def get_proxies(self):

        if self.paid_proxy is True:
            proxies = await Oxylabs().get_proxy_list()
            return proxies.get('https')
        else:
            p = []
            proxies = await FreeProxy().get_list()
            for address in proxies:
                host, port = address.split(':')
                if await check_address(host=host, port=port) is True:
                    p.append(f"http://{address}")
        return p[0]

    async def _google_session(
        self,
        url: str,
        session_args: dict,
        params: dict = None,
        method: str = 'GET',
        use_json: bool = False,
        as_json: bool = True,
        use_proxies: bool = False,
        google_search: bool = False,
        **kwargs
    ) -> Union[aiohttp.ClientResponse, dict]:
        """Make a Google API request using aiohttp Session."""
        _proxies = None
        if use_proxies is True or self.use_proxies is True:
            _proxies = await self.get_proxies()

        ssl_context = ssl.create_default_context()
        # Ensure at least TLS 1.2 is used
        ssl_context.minimum_version = ssl.TLSVersion.TLSv1_2
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        async with aiohttp.ClientSession(**session_args) as session:
            if method.upper() == 'GET':
                request = partial(
                    session.request,
                    method.upper(),
                    url,
                    params=params,
                    proxy=_proxies,
                    ssl=ssl_context,
                    **kwargs
                )
            else:
                if use_json is True:
                    request = partial(
                        session.request,
                        method.upper(),
                        url,
                        json=params,
                        proxy=_proxies,
                        ssl=ssl_context,
                        **kwargs
                    )
                else:
                    request = partial(
                        session.request,
                        method.upper(),
                        url, data=params,
                        proxy=_proxies,
                        ssl=ssl_context,
                        **kwargs
                    )
            async with request() as response:
                print(response)
                if response.status == 200:
                    if as_json is True:
                        result = await response.json()
                        if result['status'] == 'OK':
                            # TODO: Check if it's a premise or subpremise
                            return result
                    else:
                        if google_search is True:
                            return await response.read()
                        else:
                            return await response.text()
                else:
                    if google_search is True:
                        await self.check_response_search(response)
                    else:
                        await self.google_response_code(response)
                    return None

    async def check_response_search(self, response: aiohttp.ClientResponse):
        if response.status == 429:
            error = await response.text()
            self._logger.error(
                "Google Search: Too many requests"
            )
            return None
        elif response.status > 299:
            error = await response.text()
            self._logger.error(
                f"Raw response Error: {error}"
            )
            raise ComponentError(
                f"Google Places Error {response.status}",
                f"Error: {error}"
            )

    async def google_response_code(self, response: aiohttp.ClientResponse):
        """
        check if query quota has been surpassed or other errors that can happen.
        :param resp: json response
        :return:
        """
        if response.status == 429:
            error = await response.text()
            self._logger.error(
                "Google Search: Too many requests"
            )
            return None
        else:
            result = await response.json()
            status = result.get('status', 'Unknown')
            if status == "OK" or status == "ZERO_RESULTS":
                return
            # Error:
            error = result.get('error', result)
            status = error.get('status', 'Unknown')
            message = error.get('message', error)

            self._logger.error(
                f"{status}: {message}: {error}"
            )

            if status == "REQUEST_DENIED":
                raise ComponentError(
                    (
                        f"Google Places {status}: "
                        "Request was denied, maybe the API key is invalid."
                    )
                )

            if status == "OVER_QUERY_LIMIT":
                raise ComponentError(
                    (
                        f"Google Places {status}: "
                        "You exceeded your Query Limit for Google Places API Web Service, "
                        "check https://developers.google.com/places/web-service/usage "
                        "to upgrade your quota."
                    )
                )

            if status == "INVALID_REQUEST":
                raise ComponentError(
                    (
                        f"Google Places {status}: "
                        "Invalid Request: "
                        "The query string is malformed, "
                        "check if your formatting for lat/lng and radius is correct."
                        f"Error: {error}"
                    )
                )

            if status == "NOT_FOUND":
                raise ComponentError(
                    (
                        f"Google Places {status}: "
                        "The place ID was not found and either does not exist or was retired."
                    )
                )

            raise ComponentError(
                (
                    f"Google Places {status}: "
                    "Unidentified error with the Places API, please check the response code"
                    f"error: {error}"
                )
            )

    def column_exists(self, column: str):
        """Returns True if the column exists in the DataFrame."""
        if column not in self.data.columns:
            self._logger.warning(
                f"Column {column} does not exist in the dataframe"
            )
            self.data[column] = None
            return False
        return True

    def chunkify(self, lst, n):
        """Split list lst into chunks of size n."""
        for i in range(0, len(lst), n):
            yield lst[i:i + n]

    async def _processing_tasks(self, tasks: list) -> pd.DataFrame:
        """Process tasks concurrently."""
        results = []
        for chunk in self.chunkify(tasks, self.chunk_size):
            result = await asyncio.gather(*chunk, return_exceptions=True)
            if result:
                for res in result:
                    if isinstance(res, Exception):
                        # Handle the exception
                        self._logger.error(
                            f"Task failed with exception: {res}. Type: {type(res)}"
                        )
                        self._logger.error(
                            f"Exception type: {type(res)}, Task input types: {type(chunk)}"
                        )
                        continue
                    results.append(res)
        results_list = []
        for idx, result in results:
            if result:
                result['idx'] = idx  # Add the index to the result dictionary
                results_list.append(result)
        if results_list:
            results_df = pd.DataFrame(results_list)
            results_df.set_index('idx', inplace=True)
            # If necessary, reindex results_df to match self.data
            results_df = results_df.reindex(self.data.index)
            # Directly assign columns from results_df to self.data
            for column in results_df.columns:
                mask = results_df[column].notnull()
                indices = results_df.index[mask]
                self.data.loc[indices, column] = results_df.loc[indices, column]
        return self.data

    async def run(self):
        """Run the Google Places API."""
        tasks = []
        fn = getattr(self, self._type)
        tasks = [
            fn(
                idx,
                row,
            ) for idx, row in self.data.iterrows()
        ]
        # Execute tasks concurrently
        df = await self._processing_tasks(tasks)
        if self._debug is True:
            print(df)
            print("::: Printing Column Information === ")
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])
        self.add_metric("GOOGLE_PLACES_DOWNLOADED", self._counter)
        self._result = df
        return self._result

    def convert_place_id(self, place_id):
        """
        Convert a Google Place ID to CID formats.
        Args:
            place_id: The Google Place ID string.
        Returns:
            a dictionary with decimal and hexadecimal formats.
        """
        try:
            # 1. Adjust Base64 format to be decodable
            # Google uses URL-safe Base64: '-' is '+' and '_' is '/'
            place_id_safe = place_id.replace('-', '+').replace('_', '/')

            # Add padding '=' if necessary to make the length a multiple of 4
            place_id_safe += '=' * ((4 - len(place_id_safe) % 4) % 4)

            # 2. Decode the bytes
            decoded_bytes = base64.b64decode(place_id_safe)

            # 3. Unpack the data (Reverse Engineering of Protobuf)
            # Business Place IDs (ChIJ...) usually end with two 64-bit integers (unsigned long long)
            # The format '<QQ' means: Little Endian (<), two unsigned long long (Q, Q)
            # We take the last 16 bytes of the buffer
            if len(decoded_bytes) < 16:
                return {"error": "Invalid Place ID format"}

            raw_data = decoded_bytes[-16:]
            location_id, cid = struct.unpack('<QQ', raw_data)

            # Formatting outputs:
            cid_hex = f"0x{cid:x}"
            loc_hex = f"0x{location_id:x}"

            # Build full hex format (combined)
            full_hex_id = f"{loc_hex}:{cid_hex}"

            return {
                "place_id": place_id,
                "cid_decimal": str(cid),
                "cid_hex": cid_hex,
                "location_hex": loc_hex,
                "full_hex_format": full_hex_id,
                "maps_link": f"https://www.google.com/maps?cid={cid}"
            }

        except Exception as e:
            return {
                "error": f"Error extracting from Place ID: {str(e)}"
            }
