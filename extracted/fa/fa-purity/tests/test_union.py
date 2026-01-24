from fa_purity import (
    Coproduct,
    CoproductFactory,
    CoproductTransform,
)


def test_equality() -> None:
    x: Coproduct[int, str] = Coproduct.inl(23)
    y: Coproduct[str, int] = Coproduct.inr(23)
    assert x == CoproductTransform(y).swap()


def test_composite() -> None:
    x: Coproduct[int, Coproduct[str, bool]] = Coproduct.inl(23)
    y: Coproduct[Coproduct[int, bool], str] = Coproduct.inl(Coproduct.inl(23))
    f: CoproductFactory[int, Coproduct[bool, str]] = CoproductFactory()
    k: Coproduct[int, Coproduct[bool, str]] = x.map(
        lambda x: f.inl(x),
        lambda c: f.inr(CoproductTransform(c).swap()),
    )
    z = CoproductTransform.permute(k)
    assert z == y
