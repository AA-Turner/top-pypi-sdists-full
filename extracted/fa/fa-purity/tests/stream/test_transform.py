import pytest

from fa_purity import (
    Cmd,
    FrozenList,
    PureIterFactory,
    Stream,
    StreamFactory,
    StreamTransform,
)
from tests.stream._utils import (
    assert_different_iter,
    rand_int,
)


def _equal(a: int, b: int) -> None:
    assert a == b


def _mock_stream_opt(size: int, none_at: int | None) -> Stream[int | None]:
    items = PureIterFactory.from_range(range(size)).map(
        lambda i: rand_int().map(lambda r: r if none_at != i else None),
    )
    return StreamFactory.from_commands(items)


def test_chain_1() -> None:
    base = PureIterFactory.from_list((1, 2, 3))
    items = base.map(lambda i: Cmd.wrap_impure(lambda: i))
    stm = StreamFactory.from_commands(items)
    unchained = stm.map(lambda _: base)
    chained = StreamTransform.chain(unchained)
    assert_different_iter(chained)

    def _verify(elements: FrozenList[int]) -> None:
        assert elements == (1, 2, 3) * 3

    with pytest.raises(SystemExit):
        chained.to_list().map(_verify).compute()


def test_chain_2() -> None:
    base = PureIterFactory.from_list((1, 2, 3))
    items = base.map(lambda i: Cmd.wrap_impure(lambda: i))
    stm = StreamFactory.from_commands(items)
    unchained = base.map(lambda _: stm)
    chained = StreamTransform.chain(unchained)
    assert_different_iter(chained)

    def _verify(elements: FrozenList[int]) -> None:
        assert elements == (1, 2, 3) * 3

    with pytest.raises(SystemExit):
        chained.to_list().map(_verify).compute()


def test_consume() -> None:
    mutable = [0]

    def _mutate(i: int) -> Cmd[None]:
        def _action() -> None:
            mutable[0] = i

        return Cmd.wrap_impure(_action)

    items = PureIterFactory.from_range(range(10)).map(lambda i: Cmd.wrap_impure(lambda: i))
    stm = StreamFactory.from_commands(items).map(lambda i: _mutate(i))
    result = StreamTransform.consume(stm)

    def _verify() -> None:
        assert mutable[0] == 9

    assert mutable[0] == 0
    with pytest.raises(SystemExit):
        result.map(lambda _: _verify()).compute()


def test_squash() -> None:
    items = PureIterFactory.from_range(range(10)).map(lambda _: rand_int())
    stm = StreamFactory.from_commands(items).map(lambda _: rand_int())
    result = StreamTransform.squash(stm)
    assert_different_iter(result)


def test_filter_opt() -> None:
    stm = _mock_stream_opt(10, 5)
    stm_len = StreamTransform.filter_opt(stm).to_list().map(len)
    with pytest.raises(SystemExit):
        stm_len.map(lambda n: _equal(n, 9)).compute()


def test_until_none() -> None:
    stm = _mock_stream_opt(10, 5)
    stm_len = StreamTransform.until_none(stm).to_list().map(len)
    with pytest.raises(SystemExit):
        stm_len.map(lambda n: _equal(n, 5)).compute()
