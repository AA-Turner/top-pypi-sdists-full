import inspect
from dataclasses import (
    dataclass,
)
from pathlib import (
    Path,
)

from fa_purity import (
    ResultE,
)
from fa_purity.json import (
    JsonObj,
    JsonPrimitiveUnfolder,
    JsonUnfolder,
    Unfolder,
)

from fluidattacks_etl_utils.bug import (
    Bug,
)


@dataclass(frozen=True)
class SnowflakeCredentials:
    user: str
    private_key: str
    account: str

    def __repr__(self) -> str:
        return "[MASKED]"

    def __str__(self) -> str:
        return "[MASKED]"


def decode_snowflake_creds(secrets: Path, raw: JsonObj) -> ResultE[SnowflakeCredentials]:
    _account = JsonUnfolder.require(raw, "SNOWFLAKE_ACCOUNT", Unfolder.to_primitive).bind(
        JsonPrimitiveUnfolder.to_str,
    )
    _key = JsonUnfolder.require(raw, "SNOWFLAKE_ETL_PRIVATE_KEY", Unfolder.to_primitive).bind(
        JsonPrimitiveUnfolder.to_str,
    )
    decoded = _account.bind(
        lambda account: _key.map(
            lambda key: SnowflakeCredentials(
                user="ETL_USER",
                private_key=key,
                account=account,
            ),
        ),
    )
    return decoded.alt(
        lambda e: Bug.new(
            "decode_snowflake_creds",
            inspect.currentframe(),
            e,
            (str(secrets),),
        ),
    )
