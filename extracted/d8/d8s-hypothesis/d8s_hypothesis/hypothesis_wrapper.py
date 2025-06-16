"""Democritus functions for working with hypothesis."""

from hypothesis import given, settings


def hypothesis_get_strategy_results(strategy, *args, n: int = 10, **kwargs):
    """Return the given n of results from the given hypothesis strategy.

    For a list of hypothesis strategies, see: https://hypothesis.readthedocs.io/en/latest/data.html.

    """

    class A:  # pylint: disable=R0903
        def __init__(self):
            self.l = []  # noqa:E741

        @given(strategy(*args))
        @settings(max_examples=n, **kwargs)
        def a(self, value):
            """."""
            self.l.append(value)

    obj = A()
    obj.a()  # pylint: disable=E1120
    return obj.l
