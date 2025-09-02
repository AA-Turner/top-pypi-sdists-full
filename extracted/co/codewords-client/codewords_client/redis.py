from contextlib import asynccontextmanager
from structlog.contextvars import get_contextvars
from .codewords_client import AsyncCodewordsClient

@asynccontextmanager
async def redis_client():
    """
    Async context manager that provides a Redis client with automatic 
    CodeWords configuration and returns the namespace for manual key prefixing.
    
    Returns:
        tuple[redis.Redis, str]: Redis client and namespace prefix (without colon)
        
    Usage:
        async with redis_client() as (redis, ns):
            await redis.hset(f"{ns}:user_data:123", mapping=data)
    """
    try:
        import redis.asyncio as redis
    except ImportError:
        raise ImportError("redis package is required. Add 'redis>=5.0.0' to your dependencies.")
    
    client = None
    try:
        # Fetch credentials from redis_coordinator
        async with AsyncCodewordsClient() as cw_client:
            response = await cw_client.run(
                service_id="redis_coordinator",
                correlation_id=get_contextvars().get("correlation_id")
            )
            response.raise_for_status()
            creds = response.json()

        # Create Redis client
        client = redis.Redis(
            host=creds["redis_host"],
            port=creds["redis_port"],
            username=creds["redis_user"],
            password=creds["redis_password"],
            decode_responses=True,
            ssl=True,
            ssl_cert_reqs="none"
        )
        
        # Extract namespace without the colon
        namespace = creds["namespace"].replace(":*", "")
        
        yield client, namespace
        
    finally:
        if client:
            await client.aclose()