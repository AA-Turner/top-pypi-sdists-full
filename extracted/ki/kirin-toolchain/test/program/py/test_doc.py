import inspect

from kirin.prelude import basic_no_opt


def test_docstring():
    @basic_no_opt
    def some_func(x):
        "Some kernel function"
        return x + 1

    assert inspect.getdoc(some_func) == "Some kernel function"
    assert some_func(1) == 2
