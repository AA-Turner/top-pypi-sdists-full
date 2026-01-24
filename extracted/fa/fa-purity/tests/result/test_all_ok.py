from fa_purity import (
    Result,
    ResultTransform,
    Unsafe,
)
from fa_purity._core.frozen import NewFrozenList


def test_all_ok() -> None:
    success: NewFrozenList[Result[int, str]] = NewFrozenList.new(
        Result.success(1),
        Result.success(2),
    )
    assert (
        ResultTransform.all_ok_2(success)
        .alt(lambda _: Unsafe.raise_exception(Exception("failure")))
        .to_union()
    )
    failure: NewFrozenList[Result[int, str]] = NewFrozenList.new(
        Result.success(1),
        Result.failure("foo"),
    )
    assert (
        ResultTransform.all_ok_2(failure)
        .swap()
        .alt(lambda _: Unsafe.raise_exception(Exception("not failure")))
        .to_union()
    )
