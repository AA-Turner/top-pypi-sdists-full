from __future__ import (
    annotations,
)

import logging
from collections.abc import (
    Mapping,
    Sequence,
)
from dataclasses import (
    dataclass,
)
from decimal import (
    Decimal,
)
from typing import TYPE_CHECKING

from boto3.dynamodb.conditions import (
    Attr,
    Key,
)
from fa_purity import (
    Cmd,
    FrozenList,
    PureIterFactory,
    Stream,
    StreamFactory,
    StreamTransform,
    UnionFactory,
    Unsafe,
)
from fa_purity.json import (
    JsonPrimitiveFactory,
    JsonPrimitiveUnfolder,
)

from fluidattacks_integrates_dal.client import (
    GroupsClient,
)
from fluidattacks_integrates_dal.core import (
    GroupId,
    OrganizationId,
)

if TYPE_CHECKING:
    from mypy_boto3_dynamodb import (
        DynamoDBServiceResource,
    )
    from mypy_boto3_dynamodb.service_resource import (
        Table,
    )
    from mypy_boto3_dynamodb.type_defs import (
        QueryOutputTableTypeDef,
    )
LOG = logging.getLogger(__name__)
_ORGS_TABLE = "integrates_vms"
_LastObjKey = Mapping[
    str,
    bytes
    | bytearray
    | str
    | int
    | Decimal
    | bool
    | set[int]
    | set[Decimal]
    | set[str]
    | set[bytes]
    | set[bytearray]
    | Sequence[object]
    | Mapping[str, object]
    | None,
]


@dataclass(frozen=True)
class _Page:
    response: QueryOutputTableTypeDef
    last_index: _LastObjKey | None


def _to_group(pag: _Page) -> FrozenList[GroupId]:
    return tuple(
        GroupId.new(
            JsonPrimitiveFactory.from_any(i["pk"])
            .bind(JsonPrimitiveUnfolder.to_str)
            .alt(Unsafe.raise_exception)
            .to_union()
            .split("#")[1],
        )
        .alt(Unsafe.raise_exception)
        .to_union()
        for i in pag.response["Items"]
    )


def _get_groups_page(
    table: Table,
    org: OrganizationId,
    last_index: _LastObjKey | None,
) -> Cmd[_Page]:
    def _action() -> _Page:
        LOG.debug("Getting groups of %s", org)
        condition = Key("sk").eq(f"ORG#{org.uuid}") & Key("pk").begins_with("GROUP#")
        filter_exp = Attr("deletion_date").not_exists()
        response_items = (
            table.query(
                KeyConditionExpression=condition,
                FilterExpression=filter_exp,
                ExclusiveStartKey=last_index,
                IndexName="inverted_index",
            )
            if last_index
            else table.query(
                KeyConditionExpression=condition,
                FilterExpression=filter_exp,
                IndexName="inverted_index",
            )
        )
        LOG.debug("Groups of %s retrieved!", org)
        page = _Page(
            response_items,
            response_items.get("LastEvaluatedKey"),
        )
        LOG.debug(page)
        return page

    return Cmd.wrap_impure(_action)


def _get_groups(table: Table, org: OrganizationId) -> Stream[GroupId]:
    init = _get_groups_page(table, org, None)
    _union: UnionFactory[_Page, None] = UnionFactory()
    return (
        PureIterFactory.infinite_gen(
            lambda wp: wp.bind(
                lambda p: _get_groups_page(table, org, p.last_index).map(_union.inl)
                if p and p.last_index
                else Cmd.wrap_value(None).map(_union.inr),
            ),
            init.map(_union.inl),
        )
        .transform(lambda s: StreamFactory.from_commands(s))
        .transform(lambda s: StreamTransform.until_none(s))
        .map(lambda x: _to_group(x))
        .map(lambda x: PureIterFactory.from_list(x))
        .transform(lambda s: StreamTransform.chain(s))
    )


def new_client(resource: DynamoDBServiceResource) -> GroupsClient:
    return GroupsClient(lambda o: _get_groups(resource.Table(_ORGS_TABLE), o))
