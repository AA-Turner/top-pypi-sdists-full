from collections.abc import Callable
import asyncio
from aiohttp.resolver import AsyncResolver
import aiohttp
import logging
import backoff
import pandas as pd
from datamodel.parsers.json import json_encoder
from ..conf import GOOGLE_PLACES_API_KEY
from ..components import FlowComponent
from ..exceptions import ComponentError


logging.getLogger("aiohttp").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


class GoogleGeoCoding(FlowComponent):
    """
    Google GeoCoding

    Overview

    This component retrieves geographical coordinates (latitude and longitude)
    for a given set of addresses using Google Maps Geocoding API.
    It utilizes asynchronous processing to handle multiple requests concurrently and
    offers error handling for various scenarios.

    :widths: auto

        | data (pd.DataFrame)   |   Yes    | Pandas DataFrame containing the addresses. Requires a column with the address information.           |
        | columns (list)        |   Yes    | List of column names in the DataFrame that contain the address components (e.g., ["street", "city"]).|

    Return

        The component modifies the input DataFrame by adding new columns named
        'latitude', 'longitude', 'formatted_address', 'place_id' and 'zipcode' containing the retrieved
        geocoding information for each address. The original DataFrame is returned.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          GoogleGeoCoding:
          skipError: skip
          place_prefix: account_name
          use_find_place: true
          return_pluscode: true
          chunk_size: 50
          keywords:
          - electronics_store
          columns:
          - street_address
          - city
          - state_code
          - zipcode
        ```
    """
    _version = "1.0.0"
    base_url: str = "https://maps.googleapis.com/maps/api/geocode/json"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        self.chunk_size: int = kwargs.get('chunk_size', 100)
        self.check_field = kwargs.get('comparison_field', 'formatted_address')
        self.use_find_place: bool = kwargs.get('use_find_place', False)
        self.return_pluscode: bool = kwargs.get('return_pluscode', False)
        self.place_prefix: str = kwargs.get('place_prefix', None)
        self._wait_time: float = kwargs.get('wait_time', 0.1)
        self.api_key: str = kwargs.get('api_key', GOOGLE_PLACES_API_KEY)
        super(GoogleGeoCoding, self).__init__(loop=loop, job=job, stat=stat, **kwargs)
        self.semaphore = asyncio.Semaphore(10)

    async def start(self, **kwargs):
        self._counter: int = 0
        if self.previous:
            self.data = self.input
        if not hasattr(self, 'columns'):
            raise RuntimeError(
                'GoogleGeoCoding requires a Column Attribute'
            )
        if not isinstance(self.columns, list):
            raise RuntimeError(
                'GoogleGeoCoding requires a Column Attribute as list'
            )
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError(
                "Incompatible Pandas Dataframe", status=404
            )
        if not self.api_key:
            raise ComponentError(
                "Google API Key is missing", status=404
            )
        return True

    async def find_place(
        self,
        address: str,
        place_prefix: str = None,
        fields: str = "name,place_id,plus_code,formatted_address,geometry,type",
        get_plus_code: bool = True
    ) -> dict:
        """Searches for a place using the Google Places API.

        Args:
            idx: row index
            row: pandas row
            return_pluscode: return the Google +Code
            place_prefix: adding a prefix to address

        Returns:
            The Place ID of the first matching result, or None if no results are found.
        """
        base_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
        params = {
            "input": f"{place_prefix}, {address}",
            "inputtype": "textquery",
            "fields": fields,
            "key": self.api_key
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    result = await response.json()
                    if result['status'] == 'OK' and result.get("candidates"):
                        data = result["candidates"][0]
                        if not data.get('geometry'):
                            self._logger.error(
                                f"No geometry found for {address}"
                            )
                            return None
                        # Extract all the same info as in get_coordinates
                        postal_code = None
                        result = {
                            "latitude": data['geometry']['location']['lat'],
                            "longitude": data['geometry']['location']['lng'],
                            "formatted_address": data.get('formatted_address'),
                            "place_id": data.get('place_id'),
                            "zipcode": postal_code,
                        }
                        if get_plus_code:
                            result |= {
                                "plus_code": data.get("plus_code", {}).get('compound_code'),
                                "global_code": data.get("plus_code", {}).get('global_code')
                            }
                        return result
                    else:
                        error_message = result.get('error_message', 'No results found')
                        self._logger.error(
                            f"No results found for {address}: error_message: {error_message}"
                        )
                        return None
        return None

    @backoff.on_exception(
        backoff.expo,
        (aiohttp.ClientError, asyncio.TimeoutError),
        max_tries=2
    )
    async def get_coordinates(
        self,
        idx,
        row,
        return_pluscode: bool = False,
        place_prefix: str = None
    ):
        async with self.semaphore:
            street_address = self.columns[0]
            if pd.notnull(row[street_address]):
                try:
                    address = ', '.join(
                        [
                            str(row[column]) for column in self.columns
                            if column is not None and pd.notna(row[column])
                        ]
                    )
                except (ValueError, TypeError, KeyError):
                    address = row[street_address]
                if not address:
                    return idx, None
                if place_prefix:
                    try:
                        place_prefix = row[place_prefix]
                    except (ValueError, KeyError):
                        pass
                    search_address = f"{place_prefix}, {address}"
                else:
                    search_address = address
                more_params = {}
                if hasattr(self, 'keywords'):
                    keywords = []
                    for element in self.keywords:
                        keywords.append(f"keyword:{element}")
                    more_params = {
                        "components": "|".join(keywords)
                    }
                params = {
                    "address": search_address,
                    **more_params,
                    "key": self.api_key
                }
                self._logger.notice(
                    f"Looking for {search_address}"
                )
                try:
                    # Total timeout for the request
                    timeout = aiohttp.ClientTimeout(total=20)
                    resolver = AsyncResolver(
                        nameservers=["1.1.1.1", "8.8.8.8"]
                    )
                    connector = aiohttp.TCPConnector(
                        limit=100,
                        resolver=resolver
                    )
                    session_args = {
                        "connector": connector,
                        "timeout": timeout,
                        "json_serialize": json_encoder
                    }
                    async with aiohttp.ClientSession(**session_args) as session:
                        async with session.get(self.base_url, params=params) as response:
                            if response.status == 200:
                                result = await response.json()
                                if result['status'] == 'OK':
                                    data = result['results'][0]
                                    more_args = {}
                                    plus_code = None
                                    global_code = None
                                    result_types = set(data.get('types', []))
                                    # Define what constitutes a specific, acceptable address type
                                    specific_address_types = {
                                        'street_address', 'premise', 'subpremise',
                                        'store', 'convenience_store', 'gas_station',
                                        'establishment'
                                    }
                                    # If the result is not a specific address type, try to refine it.
                                    if not result_types.intersection(specific_address_types):
                                        self._logger.notice(
                                            f"Initial result is too broad ({', '.join(result_types)}). Refining with find_place."
                                        )
                                        # Refine the search:
                                        if self.use_find_place is True:
                                            place = await self.find_place(
                                                address, place_prefix=place_prefix, get_plus_code=self.return_pluscode
                                            )
                                            if not place:
                                                self._logger.error(
                                                    f"Could not find a specific place for {address}"
                                                )
                                                return idx, None
                                            return idx, place
                                        else:
                                            place_id = data.get('place_id', None)
                                    else:
                                        # The result is specific enough, proceed as before
                                        place_id = data.get('place_id', None)
                                        try:
                                            plus_code = data.get("plus_code", {}).get('compound_code')
                                            global_code = data.get("plus_code", {}).get('global_code')
                                        except KeyError:
                                            pass
                                    # extract all information:
                                    if return_pluscode is True:
                                        more_args = {
                                            "plus_code": plus_code,
                                            "global_code": global_code
                                        }
                                    # Extract postal code
                                    postal_code = None
                                    for component in data['address_components']:
                                        if 'postal_code' in component['types']:
                                            postal_code = component['long_name']
                                            break
                                    latitude = data['geometry']['location']['lat']
                                    longitude = data['geometry']['location']['lng']
                                    formatted_address = data['formatted_address']
                                    self._counter += 1
                                    # Avoid overwhelming Google APIs
                                    await asyncio.sleep(self._wait_time)
                                    return idx, {
                                        "latitude": latitude,
                                        "longitude": longitude,
                                        "formatted_address": formatted_address,
                                        "place_id": place_id,
                                        "zipcode": postal_code,
                                        **more_args
                                    }
                                else:
                                    error = result.get('error_message', result)
                                    status = result.get('status', 'Unknown')
                                    self._logger.error(
                                        f"{status}: {error}"
                                    )
                except asyncio.TimeoutError as exc:
                    self._logger.error(
                        f"TimeoutException: {exc}"
                    )
                    return idx, None
                except TypeError as exc:
                    self._logger.error(
                        f"TypeError: {exc}"
                    )
                    return idx, None
            return idx, None

    def column_exists(self, column: str):
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

    async def run(self):
        # initialize columns:
        self.column_exists('place_id')
        self.column_exists('latitude')
        self.column_exists('longitude')
        self.column_exists('formatted_address')
        self.column_exists('zipcode')
        self._counter = 0
        tasks = [
            self.get_coordinates(
                idx,
                row,
                return_pluscode=self.return_pluscode,
                place_prefix=self.place_prefix
            ) for idx, row in self.data.iterrows()
            if pd.isnull(row[self.check_field])
        ]
        results = []
        for chunk in self.chunkify(tasks, self.chunk_size):
            result = await asyncio.gather(*chunk, return_exceptions=True)
            if result:
                for res in result:
                    if isinstance(res, Exception):
                        # Handle the exception
                        self._logger.error(
                            f"Task failed with exception: {res}"
                        )
                        continue
                    results.append(res)
                # else:
                #     results += result
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
        self.add_metric("DOWNLOADED", self._counter)
        # if self._debug is True:
        print(self.data)
        print("::: Printing Column Information === ")
        for column, t in self.data.dtypes.items():
            print(column, "->", t, "->", self.data[column].iloc[0])
        self._result = self.data
        return self._result

    async def close(self):
        pass
