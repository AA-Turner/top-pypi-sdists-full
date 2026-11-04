from __future__ import annotations

from typing_extensions import Annotated

from wireup import Inject, injectable


class RedisConnection:
    def __init__(self, dsn: Annotated[str, Inject(config="infra.redis.url")]) -> None:
        self.dsn = dsn


@injectable
def make_redis_connection(
    dsn: Annotated[str, Inject(config="infra.redis.url")],
) -> RedisConnection | None:
    return RedisConnection(dsn)


@injectable
class MetricsClient:
    def __init__(self, endpoint: Annotated[str, Inject(config="infra.metrics.endpoint")]) -> None:
        self.endpoint = endpoint


@injectable
class ShelterStore:
    def __init__(self, redis: RedisConnection | None, metrics: MetricsClient) -> None:
        self.redis = redis
        self.metrics = metrics

    def describe(self) -> dict[str, str]:
        return {
            "redis": self.redis.dsn if self.redis is not None else "disabled",
            "metrics": self.metrics.endpoint,
        }
