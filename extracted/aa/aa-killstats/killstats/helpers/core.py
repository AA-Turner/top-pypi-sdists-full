"""JSON related utilities."""

# Third Party
from redis import Redis

# Django
from django.core.cache import caches

try:
    # Third Party
    import django_redis
except ImportError:
    django_redis = None


def get_redis_client() -> Redis:
    """
    Return configured redis client used for Django caching in Alliance Auth.

    Taken from the `allianceauth-app-utils` package.
    Credits to: Erik Kalkoken
    """
    try:
        return django_redis.get_redis_connection("default")
    except AttributeError:
        default_cache = caches["default"]
        return default_cache.get_master_client()
