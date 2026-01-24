import logging
from dataclasses import (
    dataclass,
)

from fa_purity import (
    Cmd,
    CmdUnwrapper,
    FrozenList,
)

from fluidattacks_utils_logger.levels import (
    LoggingLvl,
)


@dataclass(frozen=True)
class _Logger:
    logger: logging.Logger


@dataclass(frozen=True)
class Logger:
    _inner: _Logger

    def critical(self, formatted_msg: str, values: FrozenList[str]) -> Cmd[None]:
        return Cmd.wrap_impure(lambda: self._inner.logger.critical(formatted_msg, *values))

    def debug(self, formatted_msg: str, values: FrozenList[str]) -> Cmd[None]:
        return Cmd.wrap_impure(lambda: self._inner.logger.debug(formatted_msg, *values))

    def info(self, formatted_msg: str, values: FrozenList[str]) -> Cmd[None]:
        return Cmd.wrap_impure(lambda: self._inner.logger.info(formatted_msg, *values))

    def warning(self, formatted_msg: str, values: FrozenList[str]) -> Cmd[None]:
        return Cmd.wrap_impure(lambda: self._inner.logger.warning(formatted_msg, *values))


def get_logger(name: str) -> Cmd[Logger]:
    def _action() -> Logger:
        log = _Logger(logging.getLogger(name))
        return Logger(log)

    return Cmd.wrap_impure(_action)


def set_logger(name: str, lvl: LoggingLvl, handlers: FrozenList[Cmd[logging.Handler]]) -> Cmd[None]:
    def _action(unwrapper: CmdUnwrapper) -> None:
        log = logging.getLogger(name)
        log.setLevel(lvl.value)
        for item in handlers:
            log.addHandler(unwrapper.act(item))

    return Cmd.new_cmd(_action)
