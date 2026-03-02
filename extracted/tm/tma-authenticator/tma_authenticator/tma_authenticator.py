import base64
import hashlib
import hmac
import json
from typing import Callable, List, Optional, TypeVar
from urllib.parse import parse_qs, unquote

import httpx
from aiocache import cached, caches  # type: ignore
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from .storage_provider import StorageProvider
from .tma_authentication_router import TMAAuthenticationRouter
from .users import User, UserDB

T = TypeVar("T", bound=BaseModel)


class TMAAuthenticator:
    storage_provider: StorageProvider
    bot_token: Optional[str]
    auth_url: Optional[str]
    authentication_router: TMAAuthenticationRouter
    user_model: Callable[..., T]

    def __init__(
        self,
        service_name: str,
        storage_provider: StorageProvider,
        bot_token: Optional[str] = None,
        auth_url: Optional[str] = None,
        user_model: Optional[Callable[..., T]] = None,
        jwt_secret: Optional[str] = None,
        jwt_algorithm: str = "HS256",
    ):
        self.service_name = service_name
        self.bot_token = bot_token
        self.auth_url = auth_url
        self.storage_provider = storage_provider
        self.authenticator_router_provider = TMAAuthenticationRouter(
            auth_url=self.auth_url, storage_provider=self.storage_provider
        )
        self.user_model = user_model or UserDB  # type: ignore
        self._s2s_certificates = None  # Will hold JWKS data once loaded
        self.httpx_client = httpx.AsyncClient()
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm

    async def load_s2s_certificates(self) -> dict:
        """
        Fetches JWKS data once and caches it in self._s2s_certificates.
        If it's already loaded, just return it.
        """
        if self._s2s_certificates is None and self.auth_url:
            resp = await self.httpx_client.get(f"{self.auth_url}/.well-known/jwks.json")
            resp.raise_for_status()
            self._s2s_certificates = resp.json()
        return self._s2s_certificates  # type: ignore

    @property  # type: ignore
    def authentication_router(self):  # type: ignore
        return self.authenticator_router_provider

    async def oauth_verify_token(
        self,
        x_service_token: Optional[str] = Security(
            APIKeyHeader(name="X-Service-Token", auto_error=False)
        ),
        authorization: Optional[str] = Depends(
            OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)
        ),
        x_web3_token: Optional[str] = Security(APIKeyHeader(name="X-Web3-Token", auto_error=False)),
        # authorization=Security(APIKeyHeader(name="Authorization")), or /
    ):
        return await self.verify_token(
            authorization=authorization, x_service_token=x_service_token, x_web3_token=x_web3_token
        )

    async def refresh_user_cache(self, cache_key: str):
        """
        Invalidates the cached verify_token result for the given authorization and optional extra_tokens_validation.
        Call this method after updating the user's data to force cache renewal.
        """

        # Delete the cache entry so the next token verification will recompute and refresh the user data.
        cache = caches.get("default")
        # authorization.replace("Bearer ", ""), # we don't know if the user come with bearer pref
        await cache.delete(cache_key)
        await cache.delete(f"Bearer {cache_key}")

    @cached(
        key_builder=lambda f, *args, **kwargs: (
            f"{((kwargs.get('authorization') or '') + (kwargs.get('x_web3_token') or '')) or kwargs.get('x_service_token')}:{hashlib.sha256(json.dumps(kwargs.get('extra_tokens_validation') or []).encode()).hexdigest()}"
        ),
        ttl=300,
        alias="default",
    )
    async def verify_token(
        self,
        authorization: Optional[str] = None,
        x_service_token: Optional[str] = None,
        x_web3_token: Optional[str] = None,
        extra_tokens_validation: Optional[List[str]] = None,
    ) -> T:
        user = None
        web3_wallet_address = None
        should_update_user = False
        is_service: bool = False

        # First, handle web3 token if provided (can be standalone or additional)
        if x_web3_token:
            if not self.jwt_secret:
                raise HTTPException(
                    status_code=500,
                    detail="Web3 authentication is not configured. jwt_secret is missing.",
                )

            x_web3_token_clean = x_web3_token.replace("Bearer ", "")
            try:
                x_web3_token_decoded = jwt.decode(
                    x_web3_token_clean, self.jwt_secret, algorithms=[self.jwt_algorithm]
                )
            except JWTError as e:
                raise HTTPException(status_code=401, detail=f"Invalid Web3 token: {e}")

            # Extract wallet address from token
            web3_wallet_address = x_web3_token_decoded.get("address")
            if not web3_wallet_address:
                raise HTTPException(
                    status_code=401, detail="Web3 token must contain 'address' claim."
                )

        # Then handle TMA authorization token
        if authorization and self.bot_token:
            if "Bearer" in authorization:
                authorization = authorization.replace("Bearer ", "")
            is_service = False
            try:
                decoded_bytes = base64.b64decode(authorization)
                decoded_data = json.loads(decoded_bytes.decode("utf-8"))
            except Exception as e:
                raise HTTPException(
                    status_code=401, detail=f"You are not authorized to access this resource: {e}"
                )

            user = User(**decoded_data)
            valid = self.is_valid_user_info(
                web_app_data=decoded_data["initData"],
                bot_token=self.bot_token,
                extra_tokens_validation=extra_tokens_validation,
            )
            if not valid:
                raise HTTPException(
                    status_code=401,
                    detail="Invalid credentials.",
                    headers={"Authorization": "Bearer"},
                )
            user_data = self.get_user_data_dict(decoded_data["initData"])
            user.tg_language = user_data.get("language_code", "en")
            # Add wallet address if web3 token was also provided
            if web3_wallet_address:
                user.wallet_address = web3_wallet_address
            should_update_user = True  # Always update Telegram data
        elif x_service_token and self.auth_url:
            """
            Token must have scope with 'user:<TG_ID>' and '{SERVICE_NAME}',
            to provide access to all services, scope must have ['user:<TG_ID>', 'admin'] 
            """
            is_service = True
            jwks_data = await self.load_s2s_certificates()
            x_service_token = x_service_token.replace("Bearer ", "")
            try:
                x_service_token_decoded = jwt.decode(
                    x_service_token,
                    jwks_data,
                    options={
                        "verify_aud": False,
                        "verify_iss": False,
                    },
                )
            except Exception as e:
                raise HTTPException(
                    status_code=401, detail=f"You are not authorized to access this resource: {e}"
                )
            scope = x_service_token_decoded.get("scope", [])
            if self.service_name not in scope and "admin" not in scope:
                raise HTTPException(
                    status_code=401,
                    detail=f"You are not authorized to access {self.service_name}. Scope: {scope}.",
                )

            for scope in scope:
                if "user" in scope:
                    tg_id = int(scope.split("user:")[1])
                    user = User(
                        tg_id=tg_id,
                        first_name="Service",
                        last_name=f"User {tg_id}",
                        username=f"service_user_{tg_id}",
                        tg_language="en",
                    )
            if not user:
                raise HTTPException(
                    status_code=401, detail="You are not authorized to access this resource."
                )
            # Service token searches by tg_id, no need to update unless wallet is provided
            if web3_wallet_address:
                user.wallet_address = web3_wallet_address
                should_update_user = True
        elif web3_wallet_address:
            """
            Web3 token was provided standalone (without TMA authorization).
            Create a user based on the wallet address.
            Search by wallet_address.
            """
            is_service = False
            user = User(
                tg_id=None,
                first_name=None,
                last_name=None,
                username=None,
                tg_language=None,
                wallet_address=web3_wallet_address,
            )
        else:
            raise HTTPException(
                status_code=401,
                detail="Either 'authorization', 'x_service_token', or 'x_web3_token' must be provided.",
            )

        cache_key = f"{((authorization or '') + (x_web3_token or '')) or x_service_token}:{hashlib.sha256(json.dumps(extra_tokens_validation or []).encode()).hexdigest()}"

        # Determine search strategy based on what data we have
        # We need to handle potential account merging when both tg_id and wallet_address are provided
        db_user_by_tg_id = None
        db_user_by_wallet = None

        if user.tg_id and user.wallet_address:
            # Both credentials provided - check for both accounts separately
            db_user_by_tg_id = await self.storage_provider.retrieve_user({"tg_id": user.tg_id})
            db_user_by_wallet = await self.storage_provider.retrieve_user(
                {"wallet_address": user.wallet_address}
            )

            # Case 1: Both exist and are the same account - just update
            if (
                db_user_by_tg_id
                and db_user_by_wallet
                and db_user_by_tg_id["id"] == db_user_by_wallet["id"]
            ):
                db_user = db_user_by_tg_id

            # Case 2: Only tg_id account exists - update it with wallet_address
            elif db_user_by_tg_id and not db_user_by_wallet:
                db_user = db_user_by_tg_id

            # Case 3: Only wallet account exists - update it with tg_id info
            elif not db_user_by_tg_id and db_user_by_wallet:
                db_user = db_user_by_wallet

            # Case 4: Both exist but are different accounts - merge them
            elif (
                db_user_by_tg_id
                and db_user_by_wallet
                and db_user_by_tg_id["id"] != db_user_by_wallet["id"]
            ):
                # Merge: Keep tg_id account, transfer all data from wallet-only account
                # The tg_id account is primary since it has verified Telegram data
                await self.storage_provider.merge_accounts(
                    from_account_id=db_user_by_wallet["id"], to_account_id=db_user_by_tg_id["id"]
                )
                db_user = db_user_by_tg_id

            # Case 5: Neither exists - will create new below
            else:
                db_user = None

        elif user.tg_id:
            # Only tg_id provided (authorization or x_service_token)
            db_user = await self.storage_provider.retrieve_user({"tg_id": user.tg_id})
        elif user.wallet_address:
            # Only wallet_address provided (x_web3_token alone)
            db_user = await self.storage_provider.retrieve_user(
                {"wallet_address": user.wallet_address}
            )
        else:
            raise HTTPException(
                status_code=401,
                detail="Invalid authentication data: missing both tg_id and wallet_address",
            )

        if not db_user:
            # User doesn't exist, create new record
            insert_id = await self.storage_provider.insert_user(user_data=user.model_dump())
            return self.user_model(
                id=str(insert_id), **user.model_dump(), cache_key=cache_key, is_service=is_service
            )
        elif should_update_user:
            # User exists and we need to update attributes
            attributes_to_compare = [
                "tg_language",
                "first_name",
                "last_name",
                "username",
                "wallet_address",
                "tg_id",
            ]
            should_perform_update = False

            for attr in attributes_to_compare:
                user_value = getattr(user, attr)
                db_value = db_user.get(attr)
                # Update if values differ and user_value is not None
                if user_value is not None and user_value != db_value:
                    should_perform_update = True
                    break

            if should_perform_update:
                # Build update data with only non-None values
                update_data = {}
                for attr in attributes_to_compare:
                    user_value = getattr(user, attr)
                    if user_value is not None:
                        update_data[attr] = user_value

                await self.storage_provider.update_user(id=db_user["id"], update_data=update_data)

                # Refresh db_user with updated values for response
                db_user.update(update_data)

            return self.user_model(**db_user, cache_key=cache_key, is_service=is_service)
        else:
            # User exists, no updates needed
            return self.user_model(**db_user, is_service=is_service)

    def is_valid_user_info(
        self, web_app_data, bot_token: str, extra_tokens_validation: Optional[List[str]] = None
    ) -> bool:
        try:
            data_check_string = unquote(web_app_data)
            data_check_arr = data_check_string.split("&")
            needle = "hash="
            hash_item = next((item for item in data_check_arr if item.startswith(needle)), "")
            tg_hash = hash_item[len(needle) :]
            data_check_arr.remove(hash_item)
            data_check_arr.sort()
            data_check_string = "\n".join(data_check_arr)
            secret_key = hmac.new(
                "WebAppData".encode(), bot_token.encode(), hashlib.sha256
            ).digest()
            calculated_hash = hmac.new(
                secret_key, data_check_string.encode(), hashlib.sha256
            ).hexdigest()

            if calculated_hash != tg_hash:
                if extra_tokens_validation:
                    for token in extra_tokens_validation:
                        valid = self.is_valid_user_info(web_app_data=web_app_data, bot_token=token)
                        if valid:
                            return True
                return False
        except Exception:
            return False
        return True

    def get_user_data_dict(self, user_init_data: str) -> dict:
        unquoted_data = unquote(user_init_data)
        # 2) Parse it as a query string into a dict of lists
        #    Example: "user=...&chat_instance=...&auth_date=..."
        params = parse_qs(unquoted_data)
        # 3) Extract the 'user' key (if not present, return {})
        user_json_list = params.get("user")
        if not user_json_list:
            # 'user' is missing
            return {}
        # 4) parse_qs returns a list for each key, so we take the first item
        user_json = user_json_list[0]
        # 5) Convert the JSON string into a dictionary
        user_data = json.loads(user_json)
        return user_data
