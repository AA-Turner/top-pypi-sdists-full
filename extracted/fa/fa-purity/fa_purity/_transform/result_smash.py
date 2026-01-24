from dataclasses import dataclass
from typing import (
    TypeVar,
)

from fa_purity._core.result import (
    Result,
)

_A = TypeVar("_A")
_B = TypeVar("_B")
_C = TypeVar("_C")
_D = TypeVar("_D")
_E = TypeVar("_E")
_Err = TypeVar("_Err")


@dataclass(frozen=True)
class ResultSmash:
    @staticmethod
    def smash_result_2(
        result_1: Result[_A, _Err],
        result_2: Result[_B, _Err],
    ) -> Result[tuple[_A, _B], _Err]:
        return result_1.bind(lambda a: result_2.map(lambda b: (a, b)))

    @classmethod
    def smash_result_3(
        cls,
        result_1: Result[_A, _Err],
        result_2: Result[_B, _Err],
        result_3: Result[_C, _Err],
    ) -> Result[tuple[_A, _B, _C], _Err]:
        return cls.smash_result_2(result_1, result_2).bind(
            lambda t: result_3.map(lambda e: (*t, e)),
        )

    @classmethod
    def smash_result_4(
        cls,
        result_1: Result[_A, _Err],
        result_2: Result[_B, _Err],
        result_3: Result[_C, _Err],
        result_4: Result[_D, _Err],
    ) -> Result[tuple[_A, _B, _C, _D], _Err]:
        return cls.smash_result_3(result_1, result_2, result_3).bind(
            lambda t: result_4.map(lambda e: (*t, e)),
        )

    @classmethod
    def smash_result_5(
        cls,
        result_1: Result[_A, _Err],
        result_2: Result[_B, _Err],
        result_3: Result[_C, _Err],
        result_4: Result[_D, _Err],
        result_5: Result[_E, _Err],
    ) -> Result[tuple[_A, _B, _C, _D, _E], _Err]:
        return cls.smash_result_4(result_1, result_2, result_3, result_4).bind(
            lambda t: result_5.map(lambda e: (*t, e)),
        )
