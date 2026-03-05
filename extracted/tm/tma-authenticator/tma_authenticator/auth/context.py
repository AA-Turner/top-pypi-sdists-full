import logging
import traceback

from fastapi import HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlmodel import select

from ..utils.jwks import load_jwks
from .authenticator import TMAAuthenticator
from .enablers import AuthEnablers
from .keycloak import get_or_create_user_from_keycloak, verify_keycloak_token

# ---------------------------------------------------------------------------
# Canonical header names — all aliases are resolved here and nowhere else.
# ---------------------------------------------------------------------------
_H_KEYCLOAK = "x-kc-authorization"
_H_TELEGRAM = "X-TG-Authorization"       # alias: X-Telegram-Auth
_H_TELEGRAM_ALIAS = "X-Telegram-Auth"
_H_SERVICE_TOKEN = "X-Service-Token"
_H_WEB3 = "X-Web3-Token"                 # alias: X-Web3-Auth
_H_WEB3_ALIAS = "X-Web3-Auth"
_H_WALLET_CONNECT = "X-Evm-Connect"
_H_WALLET_ADDRESS = "X-Wallet-Address"


def _get_header(request: Request, canonical: str, alias: str | None = None) -> str | None:
    return request.headers.get(canonical) or (
        request.headers.get(alias) if alias else None
    )


async def _authenticate_keycloak(
    request: Request,
    existing_context: dict,
    *,
    engine: AsyncEngine,
    user_model: type,
    jwks: dict,
    logger: logging.Logger,
    context_key: str = "user",
) -> dict:
    user_kc_token = _get_header(request, _H_KEYCLOAK)
    if not user_kc_token:
        return existing_context

    try:
        logger.debug("Processing Keycloak token")

        payload = await verify_keycloak_token(user_kc_token, jwks, logger)
        user = await get_or_create_user_from_keycloak(payload, engine, user_model)

        if user:
            existing_context[context_key] = user
            request.scope[context_key] = user
            identifier = getattr(user, "tg_id", None) or getattr(user, "email", None)
            logger.info("User authenticated via Keycloak: %s", identifier)
        else:
            logger.warning(
                "Token verified but no usable identifier (tg_id or email) found in payload"
            )
            raise HTTPException(status_code=401, detail="No usable identifier found in token")

    except HTTPException:
        logger.error("HTTPException during Keycloak auth: %s", traceback.format_exc())
        raise

    except Exception as e:
        logger.error("Unexpected error processing Keycloak token: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Authentication error: {e!s}") from e

    return existing_context


async def _lookup_local_user(
    user,
    request: Request,
    existing_context: dict,
    *,
    engine: AsyncEngine,
    user_model: type,
    context_key: str = "user",
) -> dict:
    """Look up the authenticated user in the local app DB and inject into context.

    Search priority: sub (tg:<tg_id>) → tg_id → wallet_address.
    Updates sub on the DB record when it is missing or stale.
    """
    sub = f"tg:{user.tg_id}" if getattr(user, "tg_id", None) is not None else None

    async with AsyncSession(engine, expire_on_commit=False) as session:
        db_user = None

        if sub and hasattr(user_model, "sub"):
            result = await session.execute(
                select(user_model).where(getattr(user_model, "sub") == sub)
            )
            db_user = result.scalars().first()

        if not db_user and getattr(user, "tg_id", None) is not None:
            result = await session.execute(
                select(user_model).where(getattr(user_model, "tg_id") == user.tg_id)
            )
            db_user = result.scalars().first()

        if not db_user and getattr(user, "wallet_address", None):
            result = await session.execute(
                select(user_model).where(
                    getattr(user_model, "wallet_address") == user.wallet_address
                )
            )
            db_user = result.scalars().first()

        if db_user and sub and getattr(db_user, "sub", None) != sub:
            db_user.sub = sub
            session.add(db_user)
            await session.commit()
            await session.refresh(db_user)

    existing_context[context_key] = db_user
    request.scope[context_key] = db_user
    return existing_context


async def _authenticate_tma(
    request: Request,
    existing_context: dict,
    *,
    engine: AsyncEngine,
    user_model: type,
    tma_auth: TMAAuthenticator,
    tg_token: str | None,
    service_token: str | None,
    web3_token: str | None = None,
    wallet_connect: str | None = None,
    context_key: str = "user",
) -> dict:
    """Authenticate via Telegram Mini App token or service token.

    When wallet tokens are also present they are treated as additive: the
    wallet address is merged into the authenticated user's record, rather
    than producing a separate wallet-only context.
    """
    user = await tma_auth.verify_token(
        authorization=tg_token,
        x_service_token=service_token,
        x_web3_token=web3_token,
        x_wallet_connect=wallet_connect,
    )
    return await _lookup_local_user(
        user, request, existing_context, engine=engine, user_model=user_model,
        context_key=context_key,
    )


async def _authenticate_wallet(
    request: Request,
    existing_context: dict,
    *,
    engine: AsyncEngine,
    user_model: type,
    tma_auth: TMAAuthenticator,
    web3_token: str | None,
    wallet_connect: str | None,
    context_key: str = "user",
) -> dict:
    """Authenticate via wallet tokens only (no user auth present).

    Produces a wallet-only context when called without a prior user auth
    step, or enriches an existing context when a user was already resolved.
    """
    user = await tma_auth.verify_token(
        x_web3_token=web3_token,
        x_wallet_connect=wallet_connect,
    )
    return await _lookup_local_user(
        user, request, existing_context, engine=engine, user_model=user_model,
        context_key=context_key,
    )


async def _authenticate_service_wallet(
    request: Request,
    existing_context: dict,
    *,
    engine: AsyncEngine,
    user_model: type,
    tma_auth: TMAAuthenticator,
    service_token: str,
    wallet_address: str,
    context_key: str,
    logger: logging.Logger,
) -> dict:
    """Validate a service token then look up (or create) a user by raw wallet address.

    Unlike the wallet-connect path this does not verify a cryptographic signature —
    the caller's identity is established solely by the service token. The wallet
    address is used as a lookup / creation key.
    """
    await tma_auth.verify_token(x_service_token=service_token)
    logger.info("Service token authenticated for wallet address lookup: %s", wallet_address)

    async with AsyncSession(engine, expire_on_commit=False) as session:
        result = await session.execute(
            select(user_model).where(getattr(user_model, "wallet_address") == wallet_address)
        )
        user = result.scalars().first()

        if not user:
            user = user_model(wallet_address=wallet_address)
            session.add(user)
            await session.commit()
            await session.refresh(user)

    existing_context[context_key] = user
    request.scope[context_key] = user
    return existing_context


async def _build_context(
    request: Request,
    response,
    existing_context: dict,
    *,
    engine: AsyncEngine,
    user_model: type,
    tma_auth: TMAAuthenticator | None,
    jwks_uri: str | None = None,
    jwks: dict | None = None,
    enablers: AuthEnablers | None = None,
    logger: logging.Logger | None = None,
    soft_auth: bool = False,
    context_key: str = "user",
) -> dict:
    _logger = logger or logging.getLogger(__name__)
    _enablers = enablers or AuthEnablers()

    # --- 1. Keycloak (highest precedence — returns immediately in all modes) ---
    if _enablers.keycloak and _get_header(request, _H_KEYCLOAK):
        if not jwks and not jwks_uri:
            raise HTTPException(status_code=500, detail="Keycloak JWKS is not configured")
        jwks_data = jwks or await load_jwks(jwks_uri)  # type: ignore[arg-type]
        return await _authenticate_keycloak(
            request,
            existing_context,
            engine=engine,
            user_model=user_model,
            jwks=jwks_data,
            logger=_logger,
            context_key=context_key,
        )

    # Resolve all TMA-family tokens (one canonical place per auth type).
    tg_token = _get_header(request, _H_TELEGRAM, _H_TELEGRAM_ALIAS) if _enablers.tma else None
    service_token = _get_header(request, _H_SERVICE_TOKEN) if _enablers.service_token else None
    web3_token = _get_header(request, _H_WEB3, _H_WEB3_ALIAS) if _enablers.web3_jwt else None
    wallet_connect = _get_header(request, _H_WALLET_CONNECT) if _enablers.wallet_connect else None

    # --- 2. Telegram / TMA or service token ---
    # In non-soft mode: returns immediately on success.
    # In soft mode: logs failure and falls through so later paths can still run.
    if tg_token or service_token:
        if not tma_auth:
            raise HTTPException(status_code=500, detail="TMA authenticator is not configured")
        if soft_auth:
            try:
                existing_context = await _authenticate_tma(
                    request, existing_context,
                    engine=engine, user_model=user_model, tma_auth=tma_auth,
                    tg_token=tg_token, service_token=service_token,
                    web3_token=web3_token, wallet_connect=wallet_connect,
                    context_key=context_key,
                )
            except Exception as e:
                _logger.error("TMA auth failed: %s", e)
        else:
            return await _authenticate_tma(
                request, existing_context,
                engine=engine, user_model=user_model, tma_auth=tma_auth,
                tg_token=tg_token, service_token=service_token,
                web3_token=web3_token, wallet_connect=wallet_connect,
                context_key=context_key,
            )

    # --- 3. Wallet-only auth (Web3 JWT / EVM Connect) ---
    # Runs when: no user token present (non-soft), OR user auth failed (soft, context_key unset).
    if (web3_token or wallet_connect) and not existing_context.get(context_key):
        if not tma_auth:
            raise HTTPException(status_code=500, detail="TMA authenticator is not configured")
        if soft_auth:
            try:
                existing_context = await _authenticate_wallet(
                    request, existing_context,
                    engine=engine, user_model=user_model, tma_auth=tma_auth,
                    web3_token=web3_token, wallet_connect=wallet_connect,
                    context_key=context_key,
                )
            except Exception as e:
                _logger.error("Wallet auth failed: %s", e)
        else:
            return await _authenticate_wallet(
                request, existing_context,
                engine=engine, user_model=user_model, tma_auth=tma_auth,
                web3_token=web3_token, wallet_connect=wallet_connect,
                context_key=context_key,
            )

    # --- 4. Service-token + raw wallet address (highest-priority override) ---
    # Runs last so it can override any previous auth result. Only active when
    # enablers.wallet_address=True. Reads the service-token header independently
    # of the service_token enabler, so the two paths do not interfere.
    if _enablers.wallet_address:
        raw_wallet_address = _get_header(request, _H_WALLET_ADDRESS)
        raw_service_token = _get_header(request, _H_SERVICE_TOKEN)
        if raw_wallet_address and raw_service_token:
            if not tma_auth:
                raise HTTPException(
                    status_code=500, detail="TMA authenticator is not configured"
                )
            if soft_auth:
                try:
                    existing_context = await _authenticate_service_wallet(
                        request, existing_context,
                        engine=engine, user_model=user_model, tma_auth=tma_auth,
                        service_token=raw_service_token, wallet_address=raw_wallet_address,
                        context_key=context_key, logger=_logger,
                    )
                except Exception as e:
                    _logger.error("Service-wallet auth failed: %s", e)
            else:
                return await _authenticate_service_wallet(
                    request, existing_context,
                    engine=engine, user_model=user_model, tma_auth=tma_auth,
                    service_token=raw_service_token, wallet_address=raw_wallet_address,
                    context_key=context_key, logger=_logger,
                )

    return existing_context


async def get_context(
    request: Request,
    response,
    existing_context: dict,
) -> dict:
    raise HTTPException(
        status_code=500,
        detail=(
            "Calling tma_authenticator.auth.context.get_context() as a standalone function "
            "is deprecated. Pass engine/jwks_uri/enablers/logger to TMAAuthenticator() "
            "and use tma_auth.get_context as your context_getter instead."
        ),
    )
