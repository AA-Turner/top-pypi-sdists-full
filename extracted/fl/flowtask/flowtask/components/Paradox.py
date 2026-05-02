import asyncio
from collections.abc import Callable
from typing import Optional, Dict, Any
import pandas as pd
from .flow import FlowComponent
from ..interfaces.http import HTTPService
from ..interfaces.cache import CacheSupport
from ..exceptions import ComponentError
from ..conf import PARADOX_ACCOUNT_ID, PARADOX_API_SECRET

class Paradox(HTTPService, CacheSupport, FlowComponent):
    """
    Paradox Component

    **Overview**

    This component interacts with the Paradox API to perform various operations.
    The first step is to handle authentication and obtain an access token.
    The token is cached in Redis to avoid requesting a new one on each execution.

       :widths: auto

    |   type                     | Yes      | Type of operation to perform with the API                                                    |

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          Paradox:
          # attributes here
        ```
    """
    _version = "1.0.0"

    accept: str = "application/json"
    BASE_URL = "https://api.paradox.ai"
    CACHE_KEY = "_paradox_authentication"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        self.type: str = kwargs.get('type')
        self._access_token: Optional[str] = None
        self.max_pages: Optional[int] = kwargs.get('max_pages')
        super().__init__(
            loop=loop, job=job, stat=stat, **kwargs
        )

    async def get_cached_token(self) -> Optional[str]:
        """
        Retrieves the cached authentication token from Redis if it exists.
        """
        try:
            async with self as cache:
                token = await cache._redis.get(self.CACHE_KEY)
                if token and isinstance(token, str) and len(token) > 10:
                    self._logger.info(f"Using cached authentication token: {token[:10]}...")
                    return token
                else:
                    self._logger.debug(f"Invalid or no token in cache: {token}")
        except Exception as e:
            self._logger.warning(f"Error getting cached token: {str(e)}")
        return None

    def set_auth_headers(self, token: str) -> None:
        """Set authentication token and headers"""
        self._access_token = token
        if "Authorization" not in self.headers:
            self.headers = {}  # Asegurarnos de que headers está inicializado
        self.headers["Authorization"] = f"Bearer {token}"
        self._logger.debug(f"Headers set: {self.headers}")  # Agregar log para verificar

    async def start(self, **kwargs):
        """
        Initialize the component and authenticate with the API.
        Handles authentication flow including token caching in Redis.
        """
        if not PARADOX_ACCOUNT_ID or not PARADOX_API_SECRET:
            raise ComponentError(f"{__name__}: Missing required credentials")

        if token := await self.get_cached_token():
            self.set_auth_headers(token)
            self._logger.debug("Using cached authentication token")
            return True

        try:
            auth_url = f"{self.BASE_URL}/api/v1/public/auth/token"
            
            payload = {
                'client_id': PARADOX_ACCOUNT_ID,
                'client_secret': PARADOX_API_SECRET,
                'grant_type': 'client_credentials'
            }

            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            }

            result, error = await self.session(
                url=auth_url,
                method="post",
                data=payload,
                headers=headers,
                use_json=True,
                follow_redirects=True
            )

            if error:
                raise ComponentError(f"Authentication request failed: {error}")

            if 'access_token' not in result:
                raise ComponentError("No access token in authentication response")

            token = result['access_token']
            
            # Primero guardar en caché
            async with self as cache:
                await cache.setex(
                    self.CACHE_KEY,
                    token,
                    timeout=f"{result.get('expires_in', 86400)}s"
                )
                cached_token = await cache._redis.get(self.CACHE_KEY)
                if not cached_token:
                    raise ComponentError("Failed to store token in cache")
                
                self._logger.debug(f"Token successfully stored in cache")

            # Después establecer los headers
            self.set_auth_headers(token)
            self._logger.debug(f"Headers after cache: {self.headers}")

            # Verificación final
            if not self._access_token or "Authorization" not in self.headers:
                raise ComponentError("Authentication headers not properly set")

            self._logger.info("Successfully authenticated with Paradox API")
            return True

        except Exception as e:
            self._logger.error(f"Authentication failed: {str(e)}")
            raise ComponentError(f"Authentication failed: {str(e)}") from e

    async def run(self):
        """
        Execute the main component logic based on the specified type.
        Currently supports authentication as the initial implementation.
        """
        if not self._access_token or "Authorization" not in self.headers:
            self._logger.error(f"{__name__}: Not authenticated or missing Authorization header")
            raise ComponentError(f"{__name__}: Not authenticated. Call start() first")

        if not hasattr(self, self.type):
            raise ComponentError(f"{__name__}: Invalid operation type: {self.type}")

        try:
            method = getattr(self, self.type)
            result = await method()

            if isinstance(result, pd.DataFrame):
                self.add_metric("NUMROWS", len(result.index))
                self.add_metric("NUMCOLS", len(result.columns))

                if self._debug:
                    print("\n=== DataFrame Info ===")
                    print(result.head())
                    print("\n=== Column Information ===")
                    for column, dtype in result.dtypes.items():
                        print(f"{column} -> {dtype} -> {result[column].iloc[0] if not result.empty else 'N/A'}")

            self._result = result
            return self._result

        except Exception as e:
            self._logger.error(f"Error executing {self.type}: {str(e)}")
            raise

    async def close(self):
        """Cleanup any resources"""
        self._access_token = None
        return True

    async def candidates(self) -> pd.DataFrame:
        """
        Retrieves candidates from Paradox API using efficient pandas operations.
        Uses pagination to fetch all available candidates up to the maximum offset.
        Includes a delay between requests to avoid API rate limits.

        Kwargs:
            offset_start (int): Starting offset for pagination (default: 0)

        Returns:
            pd.DataFrame: DataFrame containing candidate information

        Raises:
            ComponentError: If the request fails or returns invalid data
        """
        try:
            offset = getattr(self, 'offset_start', 0)
            count = 0
            limit = getattr(self, 'limit', 50)
            all_candidates_data = []
            current_page = offset
            pages_processed = 0
            max_retries = 3
            retry_delay = 2.0

            base_params = {
                'limit': limit,
                'note': 'true',
                'include_attributes': 'Yes'
            }

            while True:
                params = {
                    **base_params,
                    'offset': offset,
                }

                self._logger.debug(
                    f"Fetching candidates page {current_page + 1} with offset {offset}"
                )

                # Implement retry logic
                data = None
                for retry in range(max_retries):
                    try:
                        data = await self.api_get(
                            url=self.BASE_URL + "/api/v1/public/candidates",
                            params=params,
                            headers=self.headers,
                            use_proxy=False
                        )

                        if data and 'candidates' in data:
                            break

                    except Exception as e:
                        if retry < max_retries - 1:
                            self._logger.warning(
                                f"Attempt {retry + 1} failed, retrying in {retry_delay} seconds... Error: {str(e)}"
                            )
                            await asyncio.sleep(retry_delay)
                            retry_delay *= 2
                            continue
                        raise

                candidates = data.get('candidates', [])
                if not candidates:
                    self._logger.warning(f"No candidates found for offset {offset * limit}")
                    break

                # Obtener el offset de la respuesta de la API y verificar
                response_offset = data.get('offset', 0)
                # Añadir el offset actual y orden global a cada candidato
                for idx, candidate in enumerate(candidates, 1):
                    candidate['response_offset'] = response_offset
                    candidate['global_order'] = response_offset + idx

                if count == 0:
                    count = data.get('count', 0)
                    # El último offset válido será el múltiplo de limit más cercano 
                    # que no exceda count - limit
                    max_offset = ((count - 1) // limit) * limit
                    self._logger.info(
                        f"Total candidates: {count}, Max offset: {max_offset}, Current offset: {offset}"
                    )
                    if self.max_pages:
                        self._logger.info(f"Will retrieve maximum {self.max_pages} pages")


                all_candidates_data.extend(candidates)
                current_page += 1
                pages_processed += 1

                self._logger.debug(
                    f"Retrieved {len(all_candidates_data)} candidates so far (Offset: {offset * limit}, "
                    f"Page: {pages_processed}"
                )

                if offset >= max_offset:
                    break

                if self.max_pages and pages_processed >= self.max_pages:
                    self._logger.info(f"Reached configured page limit: {self.max_pages}")
                    break

                offset += limit

            # Convert to DataFrame and process using pandas operations
            df = pd.DataFrame(all_candidates_data)

            if df.empty:
                self._logger.warning("No candidates data found")
                return df

            # Extract nested data using pandas operations
            candidates = df['candidate'].apply(pd.Series)
            stage = df['stage'].apply(pd.Series)
            notes = df.pop('note')

            # Remove processed columns and join the extracted data
            df = df.drop(columns=['candidate', 'stage'])
            df = df.join(candidates).join(stage)
            df['notes'] = notes

            # Extract fields from attributes
            atribute = df['attributes'].apply(
                lambda x: pd.Series({
                    "first_name": x.get('first_name'),
                    "last_name": x.get('last_name'),
                    "address": x.get('address'),
                    "address_2": x.get('address_2'),
                    "city": x.get('city'),
                    "state": x.get('state'),
                    "zipcode": x.get('zip_code'),
                    "birth_date": x.get('__birthdate'),
                    "gender": x.get('__gender'),
                    "offer_created_date": x.get('offer_created_date'),
                    "offer_accepted_date": x.get('offer_accepted_date'),
                    "current_employee": x.get('current_employee'),
                    "previously_employed_at_troc": x.get('previously_employed_at_troc')
                })
            )
            df = pd.concat([df, atribute], axis=1)

            self._logger.info(
                f"Retrieved total of {len(df)} candidates out of {count} (Pages: {current_page})"
            )
            return df

        except Exception as e:
            self._logger.error(
                f"Error fetching candidates: {str(e)}"
            )
            raise ComponentError(
                f"Failed to fetch candidates: {str(e)}"
            ) from e