from secrets import (
    randbelow,
)

import pytest

from fa_purity import (
    Cmd,
    FrozenList,
    PureIterFactory,
    StreamFactory,
    StreamTransform,
)


def _rand_val(count: int, none_index: int) -> Cmd[int | None]:
    return Cmd.wrap_impure(lambda: randbelow(11) if count != none_index else None)


def test_use_case_1() -> None:
    none_index = 7
    data = (
        PureIterFactory.infinite_range(0, 1)
        .map(lambda x: _rand_val(x, none_index))
        .transform(lambda x: StreamFactory.from_commands(x))
    )
    result = data.transform(lambda x: StreamTransform.until_none(x)).map(lambda n: n * -1)

    def _verify(items: FrozenList[int]) -> None:
        assert len(items) == none_index
        for n in items:
            assert n <= 0

    verification: Cmd[None] = result.to_list().map(_verify)
    with pytest.raises(SystemExit):
        verification.compute()
