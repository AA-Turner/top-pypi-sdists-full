import base64
import hashlib
import hmac
import json
import logging
from typing import TYPE_CHECKING, Callable, Optional, TypeVar
from urllib.parse import parse_qs, unquote

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncEngine

    from .enablers import AuthEnablers

import httpx
from aiocache import cached, caches  # type: ignore
from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel

from ..storage.provider import StorageProvider
from .authentication_router import TMAAuthenticationRouter
from .evm_wallet_connect import WalletConnectAuthError, verify_wallet_connect_header
from .users import User, UserDB

T = TypeVar("T", bound=BaseModel)

_USER_ATTRS = ["sub", "tg_language", "first_name", "last_name", "username", "wallet_address", "tg_id"]


def _normalize_bearer(token: Optional[str]) -> str:
    """Strip 'Bearer ' prefix for consistent cache key computation."""
    return (token or "").replace("Bearer ", "")


def _cache_key(authorization, x_web3_token, x_wallet_connect, x_service_token, extra_tokens_validation):
    identity = (
        _normalize_bearer(authorization)
        + _normalize_bearer(x_web3_token)
        + (x_wallet_connect or "")
    ) or _normalize_bearer(x_service_token)
    extras = hashlib.sha256(json.dumps(extra_tokens_validation or []).encode()).hexdigest()
    return f"{identity}:{extras}"


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
        # context-getter config
        engine: Optional["AsyncEngine"] = None,
        jwks_uri: Optional[str] = None,
        enablers: Optional["AuthEnablers"] = None,
        logger: Optional[logging.Logger] = None,
        context_key: str = "user",
        soft_auth: bool = False,
    ):
        self.service_name = service_name
        self.bot_token = bot_token
        self.auth_url = auth_url
        self.storage_provider = storage_provider
        self.authenticator_router_provider = TMAAuthenticationRouter(
            auth_url=self.auth_url, storage_provider=self.storage_provider
        )
        self.user_model = user_model or UserDB  # type: ignore
        self._s2s_certificates = None
        self.httpx_client = httpx.AsyncClient()
        self.jwt_secret = jwt_secret
        self.jwt_algorithm = jwt_algorithm
        self._engine = engine
        self._jwks_uri = jwks_uri
        self._enablers = enablers
        self._logger = logger
        self._context_key = context_key
        self._soft_auth = soft_auth

    async def get_context(
        self,
        request,
        response,
        existing_context: Optional[dict] = None,
    ) -> dict:
        from .context import _build_context  # local import avoids circular dependency
        if self._engine is None:
            raise RuntimeError(
                "TMAAuthenticator.get_context requires 'engine' to be set at construction time."
            )
        return await _build_context(
            request,
            response,
            existing_context if existing_context is not None else {},
            engine=self._engine,
            user_model=self.user_model,
            tma_auth=self,
            jwks_uri=self._jwks_uri,
            enablers=self._enablers,
            logger=self._logger,
            context_key=self._context_key,
            soft_auth=self._soft_auth,
        )

    async def load_s2s_certificates(self) -> dict:
        """Fetches JWKS data once and caches it in self._s2s_certificates."""
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
        x_wallet_connect: Optional[str] = Security(
            APIKeyHeader(name="X-Evm-Connect", auto_error=False)
        ),
    ):
        return await self.verify_token(
            authorization=authorization,
            x_service_token=x_service_token,
            x_web3_token=x_web3_token,
            x_wallet_connect=x_wallet_connect,
        )

    async def refresh_user_cache(self, cache_key: str):
        """Invalidate the cached verify_token result for the given token."""
        cache = caches.get("default")
        await cache.delete(cache_key)
        await cache.delete(f"Bearer {cache_key}")

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    async def _resolve_wallet_address(
        self,
        x_web3_token: Optional[str],
        x_wallet_connect: Optional[str],
    ) -> Optional[str]:
        """Resolve and cross-validate wallet address from WalletConnect and/or Web3 JWT.

        When both tokens are provided, their addresses must match.
        Returns the confirmed wallet address, or None if neither token was given.
        """
        address_from_connect: Optional[str] = None
        address_from_token: Optional[str] = None

        if x_wallet_connect:
            try:
                address_from_connect = verify_wallet_connect_header(x_wallet_connect)
            except WalletConnectAuthError as e:
                raise HTTPException(
                    status_code=401, detail=f"Invalid WalletConnect token: {e}"
                ) from e

        if x_web3_token:
            if not self.jwt_secret:
                raise HTTPException(
                    status_code=500,
                    detail="Web3 authentication is not configured. jwt_secret is missing.",
                )
            try:
                decoded = jwt.decode(
                    x_web3_token.replace("Bearer ", ""),
                    self.jwt_secret,
                    algorithms=[self.jwt_algorithm],
                )
            except JWTError as e:
                raise HTTPException(status_code=401, detail=f"Invalid Web3 token: {e}")

            address_from_token = decoded.get("address")
            if not address_from_token:
                raise HTTPException(
                    status_code=401, detail="Web3 token must contain 'address' claim."
                )
            if address_from_connect and address_from_token != address_from_connect:
                raise HTTPException(
                    status_code=401,
                    detail="Wallet address mismatch between Web3 token and WalletConnect.",
                )

        return address_from_token or address_from_connect

    def _verify_tg_token(
        self,
        authorization: str,
        extra_tokens_validation: Optional[list[str]] = None,
    ) -> User:
        """Decode and HMAC-verify a Telegram Mini App initData token. Returns a User."""
        authorization = authorization.replace("Bearer ", "")
        try:
            decoded_bytes = base64.b64decode(authorization)
            decoded_data = json.loads(decoded_bytes.decode("utf-8"))
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=f"You are not authorized to access this resource: {e}",
            )

        user = User(**decoded_data)
        if not self.is_valid_user_info(decoded_data["initData"], self.bot_token, extra_tokens_validation):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials.",
                headers={"Authorization": "Bearer"},
            )
        user.tg_language = self.get_user_data_dict(decoded_data["initData"]).get("language_code", "en")
        return user

    async def _verify_service_token(self, x_service_token: str) -> User:
        """Decode and validate a service-to-service JWT. Returns a User built from scope claims."""
        jwks_data = await self.load_s2s_certificates()
        try:
            decoded = jwt.decode(
                x_service_token.replace("Bearer ", ""),
                jwks_data,
                options={"verify_aud": False, "verify_iss": False},
            )
        except Exception as e:
            raise HTTPException(
                status_code=401,
                detail=f"You are not authorized to access this resource: {e}",
            )

        scope = decoded.get("scope", [])
        if self.service_name not in scope and "admin" not in scope:
            raise HTTPException(
                status_code=401,
                detail=f"You are not authorized to access {self.service_name}. Scope: {scope}.",
            )

        tg_id: Optional[int] = None
        for s in scope:
            if "user:" in s:
                tg_id = int(s.split("user:")[1])
                break
        if tg_id is None:
            raise HTTPException(
                status_code=401, detail="You are not authorized to access this resource."
            )

        return User(
            tg_id=tg_id,
            first_name="Service",
            last_name=f"User {tg_id}",
            username=f"service_user_{tg_id}",
            tg_language="en",
        )

    async def _resolve_user_identity(
        self,
        authorization: Optional[str],
        x_service_token: Optional[str],
        wallet_address: Optional[str],
        extra_tokens_validation: Optional[list[str]],
    ) -> tuple[User, bool, bool]:
        """Resolve user identity from exactly one auth path.

        Priority: TMA token → service token → wallet-only.
        Wallet address is merged onto the user when both TMA/service and wallet are present.

        Returns (user, should_update_user, is_service).
        """
        if authorization and self.bot_token:
            user = self._verify_tg_token(authorization, extra_tokens_validation)
            if wallet_address:
                user.wallet_address = wallet_address
            return user, True, False

        if x_service_token and self.auth_url:
            user = await self._verify_service_token(x_service_token)
            if wallet_address:
                user.wallet_address = wallet_address
            return user, bool(wallet_address), True

        if wallet_address:
            return (
                User(tg_id=None, first_name=None, last_name=None, username=None, tg_language=None, wallet_address=wallet_address),
                False,
                False,
            )

        raise HTTPException(
            status_code=401,
            detail="Either 'authorization', 'x_service_token', or 'x_web3_token'/'x_wallet_connect' must be provided.",
        )

    async def _find_in_storage(self, user: User) -> Optional[dict]:
        """Look up the user in storage, merging accounts when tg_id and wallet both resolve to different records.

        Returns the primary db_user dict, or None if not found.
        """
        if user.tg_id and user.wallet_address:
            db_by_tg = await self.storage_provider.retrieve_user({"tg_id": user.tg_id})
            db_by_wallet = await self.storage_provider.retrieve_user(
                {"wallet_address": user.wallet_address}
            )
            if db_by_tg and db_by_wallet and db_by_tg["id"] != db_by_wallet["id"]:
                # Two separate accounts — wallet merges into tg (tg is primary)
                await self.storage_provider.merge_accounts(
                    from_account_id=db_by_wallet["id"],
                    to_account_id=db_by_tg["id"],
                )
            return db_by_tg or db_by_wallet

        if user.tg_id:
            return await self.storage_provider.retrieve_user({"tg_id": user.tg_id})

        if user.wallet_address:
            return await self.storage_provider.retrieve_user({"wallet_address": user.wallet_address})

        raise HTTPException(
            status_code=401,
            detail="Invalid authentication data: missing both tg_id and wallet_address",
        )

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @cached(
        key_builder=lambda f, *args, **kwargs: _cache_key(
            kwargs.get("authorization"),
            kwargs.get("x_web3_token"),
            kwargs.get("x_wallet_connect"),
            kwargs.get("x_service_token"),
            kwargs.get("extra_tokens_validation"),
        ),
        ttl=300,
        alias="default",
    )
    async def verify_token(
        self,
        authorization: Optional[str] = None,
        x_service_token: Optional[str] = None,
        x_web3_token: Optional[str] = None,
        x_wallet_connect: Optional[str] = None,
        extra_tokens_validation: Optional[list[str]] = None,
    ) -> T:
        # 1. Resolve wallet address (from any wallet source, cross-validated)
        wallet_address = await self._resolve_wallet_address(x_web3_token, x_wallet_connect)

        # 2. Determine user identity (TMA / service token / wallet-only)
        user, should_update_user, is_service = await self._resolve_user_identity(
            authorization, x_service_token, wallet_address, extra_tokens_validation
        )

        if user.tg_id is not None:
            user.sub = f"tg:{user.tg_id}"

        cache_key = _cache_key(authorization, x_web3_token, x_wallet_connect, x_service_token, extra_tokens_validation)

        # 3. Find or create in storage
        db_user = await self._find_in_storage(user)

        if not db_user:
            insert_id = await self.storage_provider.insert_user(user_data=user.model_dump())
            return self.user_model(
                id=str(insert_id), **user.model_dump(), cache_key=cache_key, is_service=is_service
            )

        if should_update_user:
            update_data = {
                attr: getattr(user, attr)
                for attr in _USER_ATTRS
                if getattr(user, attr) is not None and getattr(user, attr) != db_user.get(attr)
            }
            if update_data:
                await self.storage_provider.update_user(id=db_user["id"], update_data=update_data)
                db_user.update(update_data)
            return self.user_model(**db_user, cache_key=cache_key, is_service=is_service)

        # No update needed — sync sub if it was missing
        if user.sub and not db_user.get("sub"):
            await self.storage_provider.update_user(
                id=db_user["id"], update_data={"sub": user.sub}
            )
            db_user["sub"] = user.sub

        return self.user_model(**db_user, is_service=is_service)

    def is_valid_user_info(
        self, web_app_data, bot_token: str, extra_tokens_validation: Optional[list[str]] = None
    ) -> bool:
        try:
            data_check_string = unquote(web_app_data)
            data_check_arr = data_check_string.split("&")
            needle = "hash="
            hash_item = next((item for item in data_check_arr if item.startswith(needle)), "")
            tg_hash = hash_item[len(needle):]
            data_check_arr.remove(hash_item)
            data_check_arr.sort()
            data_check_string = "\n".join(data_check_arr)
            secret_key = hmac.new(
                b"WebAppData", bot_token.encode(), hashlib.sha256
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
        params = parse_qs(unquoted_data)
        user_json_list = params.get("user")
        if not user_json_list:
            return {}
        return json.loads(user_json_list[0])
