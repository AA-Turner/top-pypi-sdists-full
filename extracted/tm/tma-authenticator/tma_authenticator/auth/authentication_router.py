from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..storage.provider import StorageProvider
from .service_auth import S2SClient
from .token import TokenResponse


class TMAAuthenticationRouter(APIRouter):
    auth_url: Optional[str]
    storage_provider: StorageProvider
    service_auth: S2SClient

    def __init__(self, auth_url: Optional[str], storage_provider: StorageProvider):
        super().__init__(
            prefix="/token", tags=["Authorization"], responses={404: {"description": "Not found"}}
        )
        self.auth_url = auth_url
        self.storage_provider = storage_provider

        @self.post(
            "/",
            summary="Create user authorization token.",
            response_model=TokenResponse,
            tags=["Authorization"],
        )
        @self.post(
            "",
            summary="Create user authorization token.",
            response_model=TokenResponse,
            tags=["Authorization"],
        )
        async def retrieve_access_token(token_data: OAuth2PasswordRequestForm = Depends()):
            """
            You need to provide S2S credentials to to client_id and client_secret fields, your telegram ID is username
            """
            return await self.create_access_token(token_data=token_data)

    async def create_access_token(self, token_data: OAuth2PasswordRequestForm) -> TokenResponse:
        if not self.auth_url:
            raise HTTPException(status_code=400, detail="MISCONFIGURATION")
        if not token_data.username.isdigit():
            raise HTTPException(status_code=400, detail="username should be integer.")
        self.service_auth = S2SClient(
            auth_url=self.auth_url + "/oauth/v2/token",
            username=token_data.client_id,
            password=token_data.client_secret,
        )
        try:
            await self.service_auth.get_token()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        if not self.service_auth.raw_token_response:
            raise HTTPException(detail="Empty S2S token response", status_code=400)
        token_response = TokenResponse(**self.service_auth.raw_token_response)
        if "admin" in token_response.scope:
            return token_response
        if f"user:{token_data.username}" not in token_response.scope:
            raise HTTPException(status_code=401, detail=f"No grant for {token_data.username}")
        return token_response
