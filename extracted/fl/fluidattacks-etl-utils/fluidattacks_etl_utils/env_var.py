import os

from fa_purity import (
    Cmd,
    FrozenDict,
    Maybe,
    ResultE,
)


def get_env_var(var: str) -> Cmd[Maybe[str]]:
    return Cmd.wrap_impure(lambda: Maybe.from_optional(os.environ.get(var)))


def require_env_var(var: str) -> Cmd[ResultE[str]]:
    return get_env_var(var).map(lambda m: m.to_result().alt(lambda _: KeyError(var)))


def get_environment() -> Cmd[FrozenDict[str, str]]:
    return Cmd.wrap_impure(lambda: FrozenDict(dict(os.environ)))
