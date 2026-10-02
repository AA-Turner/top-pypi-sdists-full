"""math() — safe arithmetic expression evaluation over the variable store."""
import pytest

from testmu_appium._helpers.math import math
from testmu_appium._vars import _variable_store, clear_state, set_var, var


@pytest.fixture(autouse=True)
def _clear_vars():
    clear_state()
    yield
    clear_state()


@pytest.mark.parametrize(
    "expression,expected",
    [
        ("2 + 3", 5),
        ("10 - 4", 6),
        ("3 * 4", 12),
        ("2 ** 5", 32),
        ("7 % 2", 1),
        ("-(3 + 4)", -7),
        ("+5", 5),
        ("(2 + 3) * 4", 20),
        ("2 + 3 * 4", 14),
    ],
)
def test_arithmetic_expressions(expression, expected):
    result = math(expression)
    assert result == expected


@pytest.mark.parametrize(
    "expression,expected_type",
    [
        ("2 + 3", int),
        ("10 / 2", float),  # true division always promotes to float
        ("3.5 + 1", float),
    ],
)
def test_result_type_follows_python_numeric_promotion(expression, expected_type):
    assert isinstance(math(expression), expected_type)


def test_division_result():
    assert math("10 / 4") == 2.5


def test_variable_resolution_embedded_in_expression():
    set_var("x", 5)
    set_var("y", 2)
    assert math("{{x}} + {{y}} * 3") == 11


def test_variable_resolution_whole_expression_preserves_native_type():
    set_var("x", 5)
    assert math("{{x}}") == 5
    assert isinstance(math("{{x}}"), int)


def test_variable_resolution_whole_expression_float():
    set_var("x", 2.5)
    assert math("{{x}}") == 2.5


def test_output_variable_is_written():
    result = math("2 + 3", output_variable="total")
    assert var("{{total}}") == result
    assert _variable_store["total"] == 5


def test_no_output_variable_does_not_write():
    math("2 + 3")
    assert "total" not in _variable_store


@pytest.mark.parametrize("expression", ["5 / 0", "5 % 0"])
def test_division_and_modulo_by_zero_raise(expression):
    with pytest.raises(ZeroDivisionError):
        math(expression)


@pytest.mark.parametrize(
    "expression",
    [
        "",
        "not an expression",
        "1 +",
        "__import__('os').system('echo hacked')",
        "os.getcwd()",
        "[1, 2, 3]",
        "1; 2",
        "lambda: 1",
    ],
)
def test_non_arithmetic_expression_raises_value_error(expression):
    with pytest.raises(ValueError):
        math(expression)


class TestExponentiationIsBounded:
    """int ** int is exact and unbounded in Python: it does not overflow, it
    allocates. `9 ** 9 ** 9` asks for a ~370-million-digit integer, which pegs a
    core and grows memory until the process dies — no exception, no timeout, and a
    whole test run wedged by one recorded expression."""

    #: Generous ceiling: the guard should reject in microseconds, so anything near
    #: this means the process is actually computing the power.
    TIMEOUT_S = 5.0

    def _run_with_timeout(self, expression):
        """Evaluate on a worker thread and fail if it does not finish.

        A plain call would hang the whole session on a regression; a daemon thread
        leaves the runaway computation behind but lets the suite report and exit.
        """
        import threading

        outcome = {}

        def _target():
            try:
                outcome["value"] = math(expression)
            except BaseException as exc:  # noqa: BLE001 — the raise IS the pass condition
                outcome["error"] = exc

        worker = threading.Thread(target=_target, daemon=True)
        worker.start()
        worker.join(self.TIMEOUT_S)
        assert not worker.is_alive(), (
            f"math({expression!r}) did not finish within {self.TIMEOUT_S}s — the "
            f"exponentiation guard is not bounding the operands"
        )
        return outcome

    @pytest.mark.parametrize(
        "expression",
        ["9**9**9", "9 ** 9 ** 9", "10**10**10", "2**100000000", "(-9)**9**9"],
    )
    def test_a_runaway_integer_power_is_refused_promptly(self, expression):
        outcome = self._run_with_timeout(expression)
        assert isinstance(outcome.get("error"), ValueError)
        assert "digits" in str(outcome["error"]) or "overflow" in str(outcome["error"])

    @pytest.mark.parametrize(
        "expression,expected",
        [
            ("2 ** 5", 32),
            ("2 ** 10", 1024),
            ("9 ** 9", 387420489),
            ("10 ** 99", 10 ** 99),
            ("2 ** 0", 1),
            ("0 ** 5", 0),
            ("1 ** 999999999", 1),
            ("(-2) ** 3", -8),
            ("2 ** -2", 0.25),
        ],
    )
    def test_ordinary_powers_still_evaluate(self, expression, expected):
        assert math(expression) == expected

    def test_a_float_power_that_overflows_raises_a_value_error(self):
        """Float powers overflow in constant time; the guard turns that into the
        same clean failure rather than an OverflowError escaping."""
        outcome = self._run_with_timeout("9.0 ** 999999999")
        assert isinstance(outcome.get("error"), ValueError)

    def test_the_digit_limit_is_the_documented_one(self):
        from testmu_appium._helpers import math as math_module

        assert math_module._MAX_POW_RESULT_DIGITS == 100


def test_never_calls_bare_eval():
    """AST-based guard (regex on source text would false-positive on this very
    docstring's mention of 'eval'), so walk the module's own AST for eval() calls."""
    import ast
    import inspect

    from testmu_appium._helpers import math as math_module

    tree = ast.parse(inspect.getsource(math_module))
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            assert node.func.id != "eval", "math.py must never call bare eval()"
