import logging
from dataclasses import (
    dataclass,
)

import boto3
from botocore.exceptions import (
    ClientError,
    EndpointConnectionError,
    NoCredentialsError,
    NoRegionError,
)
from fa_purity import (
    Cmd,
    Result,
    ResultE,
    cast_exception,
)
from mypy_boto3_redshift.type_defs import (
    ClusterCredentialsTypeDef,
)

from redshift_client.sql_client._core.connection import (
    Credentials,
)

LOG = logging.getLogger(__name__)


@dataclass(frozen=True)
class TempCredsUser:
    region: str | None
    cluster: str
    db_name: str
    user: str


def _decode(raw: ClusterCredentialsTypeDef) -> Credentials:
    return Credentials(raw["DbUser"], raw["DbPassword"])


# Redshift.Client.exceptions.ClusterNotFoundFault
# Redshift.Client.exceptions.UnsupportedOperationFault
def get_temp_creds(user: TempCredsUser) -> Cmd[ResultE[Credentials]]:
    def _action() -> ResultE[Credentials]:
        try:
            LOG.info("Using temporal DB credentials")
            client = boto3.client("redshift", region_name=user.region)
            raw = client.get_cluster_credentials(
                DbUser=user.user,
                DbName=user.db_name,
                ClusterIdentifier=user.cluster,
            )
            return Result.success(_decode(raw))
        except ClientError as err:  # type: ignore[misc]
            return Result.failure(cast_exception(err))
        except NoCredentialsError as err2:  # type: ignore[misc]
            return Result.failure(cast_exception(err2))
        except NoRegionError as err3:  # type: ignore[misc]
            return Result.failure(cast_exception(err3))
        except EndpointConnectionError as err4:  # type: ignore[misc]
            return Result.failure(cast_exception(err4))

    return Cmd.wrap_impure(_action)
