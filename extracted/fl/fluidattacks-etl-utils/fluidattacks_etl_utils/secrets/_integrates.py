import inspect
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

from ._core import (
    GenericSecret,
)


def decode_fluid_org_id(secrets: Path, raw: JsonObj) -> ResultE[GenericSecret]:
    decoded = JsonUnfolder.require(
        raw,
        "FLUID_ORG_ID",
        lambda v: Unfolder.to_primitive(v).bind(JsonPrimitiveUnfolder.to_str),
    ).map(GenericSecret)
    return decoded.alt(
        lambda e: Bug.new(
            "decode_fluid_org_id",
            inspect.currentframe(),
            e,
            (str(secrets),),
        ),
    )
