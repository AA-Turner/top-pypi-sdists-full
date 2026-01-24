from dataclasses import dataclass
from typing import (
    TypeVar,
)

from fa_purity._core.cmd import (
    Cmd,
)

_A = TypeVar("_A")
_B = TypeVar("_B")
_C = TypeVar("_C")
_D = TypeVar("_D")
_E = TypeVar("_E")


@dataclass(frozen=True)
class CmdSmash:
    @staticmethod
    def smash_cmds_2(
        cmd_1: Cmd[_A],
        cmd_2: Cmd[_B],
    ) -> Cmd[tuple[_A, _B]]:
        return cmd_1.bind(lambda a: cmd_2.map(lambda b: (a, b)))

    @classmethod
    def smash_cmds_3(
        cls,
        cmd_1: Cmd[_A],
        cmd_2: Cmd[_B],
        cmd_3: Cmd[_C],
    ) -> Cmd[tuple[_A, _B, _C]]:
        return cls.smash_cmds_2(cmd_1, cmd_2).bind(lambda t: cmd_3.map(lambda c: (*t, c)))

    @classmethod
    def smash_cmds_4(
        cls,
        cmd_1: Cmd[_A],
        cmd_2: Cmd[_B],
        cmd_3: Cmd[_C],
        cmd_4: Cmd[_D],
    ) -> Cmd[tuple[_A, _B, _C, _D]]:
        return cls.smash_cmds_3(cmd_1, cmd_2, cmd_3).bind(lambda t: cmd_4.map(lambda d: (*t, d)))

    @classmethod
    def smash_cmds_5(
        cls,
        cmd_1: Cmd[_A],
        cmd_2: Cmd[_B],
        cmd_3: Cmd[_C],
        cmd_4: Cmd[_D],
        cmd_5: Cmd[_E],
    ) -> Cmd[tuple[_A, _B, _C, _D, _E]]:
        return cls.smash_cmds_4(cmd_1, cmd_2, cmd_3, cmd_4).bind(
            lambda t: cmd_5.map(lambda e: (*t, e)),
        )
