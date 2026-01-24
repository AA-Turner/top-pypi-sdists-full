from fa_purity._core.maybe import Maybe


def test_maybe_from_optional() -> None:
    value = 32
    assert Maybe.from_optional(value) == Maybe.some(value)
    assert Maybe.from_optional(None) == Maybe.empty()
