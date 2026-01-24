import pytest
import copy
import apyds


@pytest.fixture
def r() -> apyds.Rule:
    return apyds.Rule("(a b c)")


def test_str(r: apyds.Rule) -> None:
    assert str(r) == "----\n(a b c)\n"

    with apyds.scoped_buffer_size(4):
        with pytest.raises(ValueError):
            str(r)


def test_repr(r: apyds.Rule) -> None:
    assert repr(r) == "Rule[\n----\n(a b c)\n]"


def test_copy_hash_and_equality(r: apyds.Rule) -> None:
    other = copy.copy(r)
    assert other == r
    assert hash(other) == hash(r)
    assert 1 != r


def test_create_from_same(r: apyds.Rule) -> None:
    rule = apyds.Rule(r)
    assert str(rule) == "----\n(a b c)\n"

    with pytest.raises(ValueError):
        rule = apyds.Rule(r, 100)


def test_create_from_base(r: apyds.Rule) -> None:
    rule = apyds.Rule(r.value)
    assert str(rule) == "----\n(a b c)\n"


def test_create_from_text() -> None:
    rule = apyds.Rule("(a b c)")
    assert str(rule) == "----\n(a b c)\n"

    # rule never fails


def test_create_from_bytes(r: apyds.Rule) -> None:
    rule = apyds.Rule(r.data())
    assert str(rule) == "----\n(a b c)\n"

    with pytest.raises(ValueError):
        rule = apyds.Rule(r.data(), 100)


def test_create_fail() -> None:
    with pytest.raises(TypeError):
        rule = apyds.Rule(100)


def test_len() -> None:
    r = apyds.Rule("(p -> q)\np\nq\n")
    assert len(r) == 2


def test_getitem() -> None:
    r = apyds.Rule("(p -> q)\np\nq\n")
    assert str(r[0]) == "(p -> q)"
    assert str(r[1]) == "p"

    with pytest.raises(TypeError):
        _ = r[-1]

    with pytest.raises(TypeError):
        _ = r[2]


def test_conclusion() -> None:
    r = apyds.Rule("(p -> q)\np\nq\n")
    assert str(r.conclusion) == "q"


def test_ground_simple() -> None:
    a = apyds.Rule("`a")
    b = apyds.Rule("((`a b))")
    assert str(a // b) == "----\nb\n"

    assert a // apyds.Rule("((`a b c d e))") is None


def test_ground_scope() -> None:
    a = apyds.Rule("`a")
    b = apyds.Rule("((x y `a `b) (y x `b `c))")
    assert str(a.ground(b, "x")) == "----\n`c\n"


def test_match() -> None:
    mp = apyds.Rule("(`p -> `q)\n`p\n`q\n")
    pq = apyds.Rule("((! (! `x)) -> `x)")
    assert str(mp @ pq) == "(! (! `x))\n----------\n`x\n"

    fail = apyds.Rule("`q <- `p")
    assert mp @ fail is None


def test_rename_simple() -> None:
    a = apyds.Rule("`x")
    b = apyds.Rule("((pre_) (_suf))")
    assert str(a.rename(b)) == "----\n`pre_x_suf\n"


def test_rename_empty_prefix() -> None:
    a = apyds.Rule("`x")
    b = apyds.Rule("(() (_suf))")
    assert str(a.rename(b)) == "----\n`x_suf\n"


def test_rename_empty_suffix() -> None:
    a = apyds.Rule("`x")
    b = apyds.Rule("((pre_) ())")
    assert str(a.rename(b)) == "----\n`pre_x\n"


def test_rename_with_premises() -> None:
    a = apyds.Rule("`p\n`q\n----------\n`r\n")
    b = apyds.Rule("((pre_) (_suf))")
    assert str(a.rename(b)) == "`pre_p_suf\n`pre_q_suf\n----------\n`pre_r_suf\n"


def test_rename_invalid() -> None:
    a = apyds.Rule("`x")
    b = apyds.Rule("item")
    assert a.rename(b) is None
