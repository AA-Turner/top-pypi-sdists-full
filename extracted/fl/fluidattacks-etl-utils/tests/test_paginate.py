from fa_purity import (
    Cmd,
    FrozenList,
    Maybe,
    Unsafe,
)
from fa_purity._core.pure_iter import (
    PureIterFactory,
)

from fluidattacks_etl_utils.paginate import (
    cursor_pagination,
)

data_pkg_1 = (1, 2, 3)
data_pkg_2: FrozenList[int] = ()
data_pkg_3 = (11, 22, 33, 44, 55)


def _get_page(page: str) -> Cmd[tuple[FrozenList[int], Maybe[str]]]:
    if page == "abc1":
        return Cmd.wrap_value((data_pkg_2, Maybe.some("abc2")))
    if page == "abc2":
        return Cmd.wrap_value((data_pkg_3, Maybe.empty()))
    msg = f"Page `{page}` not found"
    raise KeyError(msg)


def get_page(page: Maybe[str]) -> Cmd[tuple[FrozenList[int], Maybe[str]]]:
    return page.map(_get_page).value_or(Cmd.wrap_value((data_pkg_1, Maybe.some("abc1"))))


def test_cursor_pagination() -> None:
    expected = PureIterFactory.from_list([data_pkg_1, data_pkg_2, data_pkg_3]).to_list()
    assert expected == Unsafe.compute(cursor_pagination(get_page).to_list())
