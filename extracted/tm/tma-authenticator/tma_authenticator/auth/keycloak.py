import logging
from typing import Any

import jwt
from fastapi import HTTPException
from jwt.algorithms import RSAAlgorithm
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlmodel import select


def get_signing_key_from_jwks(token: str, jwks: dict) -> Any:
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")

    if not kid:
        raise ValueError("Token header missing 'kid' (key ID)")

    if not jwks:
        raise ValueError("Keycloak certificates not loaded")

    keys = jwks.get("keys", [])
    for key in keys:
        if key.get("kid") == kid:
            return RSAAlgorithm.from_jwk(key)

    raise ValueError(f"Unable to find matching key with kid: {kid}")


async def verify_keycloak_token(token: str, jwks: dict, logger: logging.Logger) -> dict:
    try:
        public_key = get_signing_key_from_jwks(token, jwks)

        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            audience=None,
            options={"verify_aud": False},
        )

        logger.info(
            "Successfully verified token for user: %s",
            payload.get("tg_id") or payload.get("email"),
        )
        return payload

    except jwt.ExpiredSignatureError as e:
        logger.warning("Token verification failed: Token has expired")
        raise HTTPException(status_code=401, detail="Token has expired") from e

    except jwt.InvalidTokenError as e:
        logger.warning("Token verification failed: Invalid token - %s", e)
        raise HTTPException(status_code=401, detail=f"Invalid token: {e!s}") from e

    except ValueError as e:
        logger.error("Token verification failed: %s", e)
        raise HTTPException(status_code=500, detail=f"Certificate error: {e!s}") from e

    except Exception as e:
        logger.error("Token verification failed with unexpected error: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail=f"Token verification failed: {e!s}") from e


async def get_or_create_user_from_keycloak(
    payload: dict,
    engine: AsyncEngine,
    user_model: type,
) -> Any | None:
    sub = payload.get("sub")
    tg_id = payload.get("tg_id")
    email = payload.get("email")

    if not sub and not tg_id and not email:
        return None

    async with AsyncSession(engine, expire_on_commit=False) as session:
        if sub:
            statement = select(user_model).where(getattr(user_model, "sub") == sub)
        elif tg_id:
            statement = select(user_model).where(getattr(user_model, "tg_id") == int(tg_id))
        else:
            statement = select(user_model).where(getattr(user_model, "email") == email)

        result = await session.execute(statement)
        user = result.scalars().first()

        if user:
            updated = False
            username = payload.get("preferred_username")
            first_name = payload.get("given_name")
            last_name = payload.get("family_name")

            if sub and getattr(user, "sub", None) != sub:
                user.sub = sub
                updated = True
            if username and getattr(user, "username", None) != username:
                user.username = username
                updated = True
            if first_name and getattr(user, "first_name", None) != first_name:
                user.first_name = first_name
                updated = True
            if last_name and getattr(user, "last_name", None) != last_name:
                user.last_name = last_name
                updated = True
            if email and getattr(user, "email", None) != email:
                user.email = email
                updated = True

            if updated:
                session.add(user)
                await session.commit()
                await session.refresh(user)
        else:
            user = user_model(
                sub=sub,
                tg_id=int(tg_id) if tg_id else None,
                email=email,
                username=payload.get("preferred_username"),
                first_name=payload.get("given_name"),
                last_name=payload.get("family_name"),
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

    return user
