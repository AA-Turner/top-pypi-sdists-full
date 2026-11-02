from typing import Type
from celery import Celery
from celery.backends.redis import RedisBackend

from pytest import mark
import pytest


from celery_redis_poll_backend import (
    PollingRedisBackend,
    PollingRedisClusterBackend,
)


def install_redis_poll_backend():
    """Explicitly install.  Useful for local unit tests."""
    from celery.app.backends import BACKEND_ALIASES

    BACKEND_ALIASES["redis"] = "celery_redis_poll.backend:choose_redis_backend"
    BACKEND_ALIASES["rediss"] = "celery_redis_poll.backend:choose_rediss_backend"


@mark.parametrize(
    "protocol, expected_backend",
    [
        ("redis", RedisBackend),
        ("rediss", RedisBackend),
        ("redis+poll", PollingRedisBackend),
        ("rediss+poll", PollingRedisBackend),
        ("redis+cluster_poll", PollingRedisClusterBackend),
        ("rediss+cluster_poll", PollingRedisClusterBackend),
    ],
)
def test_redis_cluster_backend_installation(
    protocol: str,
    expected_backend: Type,
):
    install_redis_poll_backend()

    # Initialize Celery app with RedisClusterBackend
    options = "?ssl_cert_reqs=CERT_NONE" if "rediss" in protocol else ""
    app = Celery(
        "test_app",
        broker="redis://localhost:6379/0",
        backend=f"{protocol}://localhost:6379{options}",
    )

    # Check if the backend is set correctly
    assert isinstance(app.backend, expected_backend), (
        f"Backend is not set to {expected_backend}"
    )


if __name__ == "__main__":
    pytest.main()
