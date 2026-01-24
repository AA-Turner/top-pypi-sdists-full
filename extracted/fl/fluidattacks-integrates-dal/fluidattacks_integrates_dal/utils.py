from __future__ import annotations

from typing import TYPE_CHECKING

from boto3 import (
    Session,
)
from fa_purity import (
    Cmd,
)

if TYPE_CHECKING:
    from mypy_boto3_dynamodb import (
        DynamoDBClient,
        DynamoDBServiceResource,
    )


def new_session() -> Cmd[Session]:
    # This impure procedure gets inputs (credentials) through the environment
    # e.g. AWS_DEFAULT_REGION
    return Cmd.wrap_impure(lambda: Session())


def new_resource(session: Session) -> Cmd[DynamoDBServiceResource]:
    return Cmd.wrap_impure(
        lambda: session.resource(service_name="dynamodb", use_ssl=True, verify=True),
    )


def new_client(session: Session) -> Cmd[DynamoDBClient]:
    return Cmd.wrap_impure(lambda: session.client("dynamodb"))
