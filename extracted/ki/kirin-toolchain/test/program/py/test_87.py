from kirin.prelude import basic


@basic
def foo(x: float):
    return x + 0.22


@basic
def issue_87(x: float):

    def inner(y: float, z: float):
        return foo(x) + y + z

    return inner


def test_issue_87():
    assert issue_87(1.0)(1, 2) == 4.22
