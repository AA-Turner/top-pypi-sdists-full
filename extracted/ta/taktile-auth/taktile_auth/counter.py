import time
import typing as t


@t.runtime_checkable
class SharedCounter(t.Protocol):
    """A distributed atomic counter shared across service instances."""

    def increment(self, key: str, amount: int, ttl_seconds: int) -> int:
        """Atomically add ``amount`` to the counter at ``key`` and
        return the post-increment value. Refreshes the TTL on every
        increment."""
        ...  # pragma: no cover

    def get(self, key: str) -> int:
        """Return the current counter value at ``key`` (0 if absent)."""
        ...  # pragma: no cover


class DynamoDBSharedCounter:
    """``SharedCounter`` backed by a DynamoDB table.

    The DynamoDB client is passed in — the caller owns its
    configuration (timeouts, retries, connection reuse).

    Expects the auth-cache table schema: hash key ``realm`` (S) and
    range key ``key`` (S). Counters accumulate in the ``value`` (N)
    attribute and expire via the table's ``ttl`` (N) attribute. The
    hash key is suffixed with the counter key (``<realm>_<key>``) so
    counters spread across partitions instead of hot-spotting a
    single realm partition.
    """

    def __init__(
        self,
        *,
        client: t.Any,
        table_name: str,
        realm: str,
        consistent_read: bool = True,
    ) -> None:
        self._client = client
        self._table_name = table_name
        self._realm = realm
        # Strongly-consistent reads by default so an abort check sees the
        # weight a concurrent hop just wrote; callers can relax to
        # eventually consistent to trade accuracy for read latency.
        self._consistent_read = consistent_read

    def increment(self, key: str, amount: int, ttl_seconds: int) -> int:
        response = self._client.update_item(
            TableName=self._table_name,
            Key={
                "realm": {"S": f"{self._realm}_{key}"},
                "key": {"S": key},
            },
            # ``value`` and ``ttl`` are DynamoDB reserved words.
            UpdateExpression="ADD #value :amount SET #ttl = :ttl",
            ExpressionAttributeNames={"#value": "value", "#ttl": "ttl"},
            ExpressionAttributeValues={
                ":amount": {"N": str(amount)},
                ":ttl": {"N": str(int(time.time()) + ttl_seconds)},
            },
            ReturnValues="ALL_NEW",
        )
        return int(response["Attributes"]["value"]["N"])

    def get(self, key: str) -> int:
        response = self._client.get_item(
            TableName=self._table_name,
            Key={
                "realm": {"S": f"{self._realm}_{key}"},
                "key": {"S": key},
            },
            ConsistentRead=self._consistent_read,
        )
        item = response.get("Item")
        if not item:
            return 0
        return int(item["value"]["N"])
