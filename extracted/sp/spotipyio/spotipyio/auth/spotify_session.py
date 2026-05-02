from __future__ import annotations
from typing import Optional, Dict, Any

from aiohttp import ClientSession, ClientResponse, ContentTypeError, ClientResponseError
from multidict import CIMultiDict

from spotipyio.auth.client_credentials import ClientCredentials
from spotipyio.logic.consts.api_consts import ACCESS_TOKEN, REFRESH_TOKEN, TOKEN_REQUEST_URL
from spotipyio.logic.consts.typing_consts import Json
from spotipyio.auth.session_cache_handler_interface import ISessionCacheHandler
from spotipyio.logic.authorization import AccessTokenGenerator
from spotipyio.auth.spotify_grant_type import SpotifyGrantType
from spotipyio.logic.utils.web_utils import create_client_session


class SpotifySession:
    def __init__(
        self,
        token_request_url: str = TOKEN_REQUEST_URL,
        credentials: Optional[ClientCredentials] = None,
        access_token_generator: Optional[AccessTokenGenerator] = None,
        session: Optional[ClientSession] = None,
        session_cache_handler: Optional[ISessionCacheHandler] = None,
    ):
        self._token_request_url = token_request_url
        self._credentials = credentials or ClientCredentials()
        self._access_token_generator = access_token_generator
        self._session = session
        self._cache_handler = session_cache_handler

    async def get(self, url: str, params: Optional[dict] = None) -> Optional[Json]:
        async with self._session.get(url=url, params=params) as response:
            return await self._handle_response(response)

    async def post(self, url: str, payload: dict) -> Optional[Json]:
        async with self._session.post(url=url, json=payload) as response:
            return await self._handle_response(response)

    async def put(self, url: str, data: Optional[Any] = None, payload: Optional[dict] = None) -> Optional[Json]:
        async with self._session.put(url=url, data=data, json=payload) as response:
            return await self._handle_response(response)

    async def delete(self, url: str, payload: Optional[dict] = None) -> Optional[Json]:
        async with self._session.delete(url=url, json=payload) as response:
            return await self._handle_response(response)

    async def refresh(self) -> None:
        if self._session is not None:
            await self._session.close()

        self._session = await self._build_client_session(use_cache=False)

    async def start(self) -> None:
        if self._session is None:
            self._session = await self._build_client_session(use_cache=True)

    async def stop(self) -> None:
        if self._session is not None:
            await self._session.close()

        if self._access_token_generator is not None:
            await self._access_token_generator.stop()

    def get_authorization_headers(self) -> CIMultiDict[str]:
        return self._session.headers

    async def _handle_response(self, response: ClientResponse) -> Optional[Json]:
        if self._is_2xx_successful(response):
            return await self._jsonify_response_if_possible(response)

        json_error_response = await self._jsonify_response_if_possible(response)
        if json_error_response is None:
            response.raise_for_status()

        raise ClientResponseError(
            request_info=response.request_info,
            history=response.history,
            status=response.status,
            message=f"Spotify request to URL `{response.request_info.url}` with method "
            f"`{response.request_info.method}` failed with the following JSON message:\n{json_error_response}",
        )

    @staticmethod
    def _is_2xx_successful(response: ClientResponse) -> bool:
        return 200 <= response.status < 300

    @staticmethod
    async def _jsonify_response_if_possible(response: ClientResponse) -> Optional[Json]:
        try:
            return await response.json()

        except ContentTypeError:
            return

    async def __aenter__(self) -> SpotifySession:
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.stop()

    async def _build_client_session(self, use_cache: bool) -> ClientSession:
        if self._access_token_generator is None:
            await self._init_token_generator()

        response = await self._fetch_access_token(use_cache)
        access_token = response[ACCESS_TOKEN]
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        }

        return create_client_session(headers)

    async def _fetch_access_token(self, use_cache: bool) -> Dict[str, str]:
        if use_cache and self._cache_handler is not None:
            response = await self._retrieve_access_token_from_cache()

            if response is not None:
                return response

        return await self._generate_access_token(
            grant_type=self._credentials.grant_type, access_code=self._credentials.access_code
        )

    async def _retrieve_access_token_from_cache(self) -> Optional[Dict[str, str]]:
        cached_response = self._cache_handler.get()

        if cached_response is not None:
            return await self._generate_access_token(
                grant_type=SpotifyGrantType.REFRESH_TOKEN, access_code=cached_response[REFRESH_TOKEN]
            )

    async def _generate_access_token(self, grant_type: SpotifyGrantType, access_code: str) -> Dict[str, str]:
        response = await self._access_token_generator.generate(grant_type=grant_type, access_code=access_code)

        if self._cache_handler is not None:
            self._cache_handler.set(response)

        return response

    async def _init_token_generator(self) -> None:
        self._access_token_generator = AccessTokenGenerator(
            token_request_url=self._token_request_url,
            client_id=self._credentials.client_id,
            client_secret=self._credentials.client_secret,
            redirect_uri=self._credentials.redirect_uri,
        )
        await self._access_token_generator.start()
