from kirin.prelude import basic_no_opt


@basic_no_opt
def not_in(x, y):
    return x not in y


@basic_no_opt
def in_(x, y):
    return x in y


@basic_no_opt
def is_(x, y):
    return x is y


@basic_no_opt
def is_not(x, y):
    return x is not y


def test_is():
    class Foo:
        pass

    a, b = Foo(), Foo()
    assert is_(a, b) == (a is b)
    assert is_(a, a) == (a is a)


def test_is_not():
    class Foo:
        pass

    a, b = Foo(), Foo()
    assert is_not(a, b) == (a is not b)
    assert is_not(a, a) == (a is not a)


def test_in():
    assert in_(1, [1, 2, 3]) == (1 in [1, 2, 3])
    assert in_(4, [1, 2, 3]) == (4 in [1, 2, 3])
    assert in_("a", "abc") == ("a" in "abc")
    assert in_("d", "abc") == ("d" in "abc")


def test_not_in():
    assert not_in(1, [1, 2, 3]) == (1 not in [1, 2, 3])
    assert not_in(4, [1, 2, 3]) == (4 not in [1, 2, 3])
    assert not_in("a", "abc") == ("a" not in "abc")
    assert not_in("d", "abc") == ("d" not in "abc")
