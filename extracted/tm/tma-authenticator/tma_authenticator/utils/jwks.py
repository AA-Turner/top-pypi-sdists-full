import httpx

_jwks_cache: dict[str, dict] = {}


async def load_jwks(jwks_uri: str) -> dict:
    if jwks_uri in _jwks_cache:
        return _jwks_cache[jwks_uri]

    async with httpx.AsyncClient() as client:
        response = await client.get(jwks_uri)
        response.raise_for_status()
        jwks = response.json()
        _jwks_cache[jwks_uri] = jwks
        return jwks
