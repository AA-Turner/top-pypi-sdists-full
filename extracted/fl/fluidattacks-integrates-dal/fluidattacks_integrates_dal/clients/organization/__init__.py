from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from fa_purity import (
    Cmd,
    FrozenList,
    PureIterFactory,
    Result,
    ResultE,
    Stream,
    StreamFactory,
    StreamTransform,
    Unsafe,
    cast_exception,
)
from fa_purity.json import (
    JsonPrimitive,
    JsonPrimitiveFactory,
    JsonPrimitiveUnfolder,
)

from fluidattacks_integrates_dal._typing import (
    Dict,
    Iterable,
    TypeVar,
)
from fluidattacks_integrates_dal.client import (
    OrgsClient,
)
from fluidattacks_integrates_dal.core import (
    OrganizationId,
)

if TYPE_CHECKING:
    from mypy_boto3_dynamodb import (
        DynamoDBClient,
    )
    from mypy_boto3_dynamodb.type_defs import (
        QueryOutputTypeDef,
    )
LOG = logging.getLogger(__name__)
_T = TypeVar("_T")
_K = TypeVar("_K")
_DB_TABLE = "integrates_vms"


def _require_key(item: Dict[_K, _T], key: _K) -> ResultE[_T]:
    try:
        return Result.success(item[key])
    except KeyError as err:
        return Result.failure(err).alt(cast_exception)


def _decode_dynamo_str(item: _T) -> ResultE[JsonPrimitive]:
    if isinstance(item, dict):
        return _require_key(item, "S").bind(  # type: ignore[misc]
            JsonPrimitiveFactory.from_any,
        )
    return Result.failure(TypeError(f"Expected `dict` instance; got `{type(item)}`")).alt(
        cast_exception,
    )


def _decode_dynamo_key_str(item: Dict[str, _T], key: str) -> ResultE[JsonPrimitive]:
    return _require_key(item, key).bind(_decode_dynamo_str)


def _decode_org_id(raw: Dict[str, _T]) -> ResultE[OrganizationId]:
    _pk = _decode_dynamo_key_str(raw, "pk").bind(JsonPrimitiveUnfolder.to_str)
    _sk = _decode_dynamo_key_str(raw, "sk").bind(JsonPrimitiveUnfolder.to_str)
    return _pk.bind(lambda pk: _sk.bind(lambda sk: OrganizationId.new(pk, sk)))


def _to_items(page: QueryOutputTypeDef) -> FrozenList[OrganizationId]:
    return tuple(  # type: ignore[misc]
        _decode_org_id(item)  # type: ignore[misc]
        .alt(Unsafe.raise_exception)
        .to_union()
        for item in page["Items"]  # type: ignore[misc]
    )


def _all_orgs(client: DynamoDBClient) -> Stream[OrganizationId]:
    def _new_iter() -> Iterable[Cmd[QueryOutputTypeDef]]:
        LOG.debug("Getting all orgs")
        exp_attrs_values: Dict[str, Dict[str, str]] = {
            ":pk": {"S": "ORG#all"},
            ":sk": {"S": "ORG#"},
        }
        response = client.get_paginator("query").paginate(  # type: ignore[misc]
            ExpressionAttributeNames={
                "#pk": "pk_2",
                "#sk": "sk_2",
            },
            ExpressionAttributeValues=exp_attrs_values,
            KeyConditionExpression=("#pk = :pk and begins_with(#sk, :sk)"),
            TableName=_DB_TABLE,
            IndexName="gsi_2",
        )
        LOG.debug("all orgs retrieved!")
        return map(Cmd.wrap_value, response)  # type: ignore[misc]

    data = StreamFactory.from_commands(  # type: ignore[misc]
        Unsafe.pure_iter_from_cmd(Cmd.wrap_impure(_new_iter)),  # type: ignore[misc]
    )
    return (
        data.map(lambda x: _to_items(x))  # type: ignore[misc]
        .map(lambda x: PureIterFactory.from_list(x))
        .transform(lambda s: StreamTransform.chain(s))
    )


def new_client(client: DynamoDBClient) -> OrgsClient:
    return OrgsClient(_all_orgs(client))
