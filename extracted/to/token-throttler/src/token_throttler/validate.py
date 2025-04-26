from inspect import formatannotation, signature
from typing import Any, Dict, List


def validate_bucket(bucket: Any, bucket_type: Any) -> None:
    if not isinstance(bucket, bucket_type):
        raise TypeError("Invalid `bucket` type")


def validate_bucket_config(
    bucket_config: List[Dict[str, Any]], bucket_type: Any
) -> None:
    token_bucket_params: Dict = {
        p.name: p.annotation for p in signature(bucket_type).parameters.values()
    }
    if not all(
        key in bucket for key in token_bucket_params.keys() for bucket in bucket_config
    ):
        raise KeyError(
            f"Invalid configuration. Required keys for each bucket: {', '.join(token_bucket_params)}"
        )
    if not all(
        isinstance(bucket[param], token_bucket_params.get(param, ""))
        for param in token_bucket_params
        for bucket in bucket_config
    ):
        raise TypeError(
            f"Invalid configuration. Required types for each bucket: {', '.join([f'{x} - {formatannotation(y)}' for x, y in token_bucket_params.items()])}"
        )


def validate_bucket_key(bucket_key: str) -> None:
    if not isinstance(bucket_key, str):
        raise TypeError("Invalid `bucket_key` type")


def validate_cost(cost: int) -> None:
    if not isinstance(cost, int):
        raise TypeError("Invalid `cost` type")


def validate_identifier(identifier: str) -> None:
    if not isinstance(identifier, str):
        raise TypeError("Invalid `identifier` type")


def validate_max_tokens(max_tokens: int) -> None:
    if not isinstance(max_tokens, int):
        raise TypeError("Invalid `max_tokens` type")


def validate_replenish_time(replenish_time: int) -> None:
    if not isinstance(replenish_time, int):
        raise TypeError("Invalid `replenish_time` type")


def validate_storage(storage: Any, storage_type: Any) -> None:
    if not isinstance(storage, storage_type):
        raise TypeError("Invalid `storage` class")
