from fa_purity import (
    Cmd,
    Maybe,
    PureIterFactory,
    StreamFactory,
    Unsafe,
)
from tests.stream._utils import (
    assert_different_iter,
    rand_int,
)


def test_from_commands() -> None:
    items = PureIterFactory.from_range(range(10)).map(lambda _: rand_int())
    stm = StreamFactory.from_commands(items)
    assert_different_iter(stm)


def test_generate() -> None:
    def _cmd(prev: int) -> Cmd[int]:
        return Cmd.wrap_impure(lambda: prev + 1)

    stm = StreamFactory.generate(_cmd, lambda x: Maybe.from_optional(None if x >= 9 else x), 0)
    assert_different_iter(stm)
    assert Unsafe.compute(stm.to_list()) == tuple(range(1, 10))
