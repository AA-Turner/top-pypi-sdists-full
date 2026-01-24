from dataclasses import (
    dataclass,
    field,
)
from pathlib import (
    Path,
)
from typing import (
    IO,
    TypeVar,
)

from fa_purity import (
    Cmd,
    FrozenDict,
    ResultE,
)
from fa_purity.json import (
    JsonObj,
    UnfoldedFactory,
)

from fluidattacks_etl_utils.env_var import (
    get_environment,
)
from fluidattacks_etl_utils.process import (
    RunningSubprocess,
    StdValues,
    Subprocess,
)

_T = TypeVar("_T")


@dataclass(frozen=True)
class GenericSecret:
    value: str = field(repr=False)

    def __repr__(self) -> str:
        return "[MASKED]"

    def __str__(self) -> str:
        return "[MASKED]"


def _decrypt(env: FrozenDict[str, str], file_path: Path) -> Cmd[IO[str]]:
    def _assert_not_none(item: _T | None) -> _T:
        if item is not None:
            return item
        msg = "Unexpected None"
        raise TypeError(msg)

    return RunningSubprocess.run_universal_newlines(
        Subprocess(
            (
                "sops",
                "--aws-profile",
                "default",
                "--decrypt",
                "--output-type",
                "json",
                file_path.as_posix(),
            ),
            None,
            StdValues.PIPE,
            None,
            env,
        ),
    ).map(lambda p: _assert_not_none(p.stdout))


def get_secrets(file_path: Path) -> Cmd[ResultE[JsonObj]]:
    return get_environment().bind(lambda env: _decrypt(env, file_path)).map(UnfoldedFactory.load)
