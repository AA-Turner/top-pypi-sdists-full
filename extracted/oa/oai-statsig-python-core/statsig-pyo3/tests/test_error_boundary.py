import pytest
from statsig_python_core import Statsig, StatsigUser
from statsig_python_core.error_boundary import ErrorBoundary


def test_error_boundary_handles_wrong_types():
    statsig = Statsig("secret-test-key")

    result = statsig.check_gate(123, "gate_name")  # Invalid user type
    assert result is None

    user = StatsigUser("user_123")
    result = statsig.check_gate(user, 123)  # Invalid gate name type
    assert result is None

    result = statsig.get_dynamic_config(123, "config_name")
    assert result is None

    result = statsig.get_experiment(user, 123)
    assert result is None

    statsig.log_event(123, "event_name")  # Should not raise
    statsig.log_event(user, 123)  # Should not raise


class _BoundaryTarget:
    def __init__(self):
        self.calls = []
        self.result = object()
        self.error = None

    def first(self, *args, **kwargs):
        self.calls.append(("first", args, kwargs))
        if self.error is not None:
            raise self.error
        return self.result

    def second(self, *args, **kwargs):
        self.calls.append(("second", args, kwargs))
        if self.error is not None:
            raise self.error
        return self.result


@pytest.mark.parametrize("method_name", ["first", "second"])
def test_error_boundary_forwards_arguments_and_return_identity(method_name):
    target = _BoundaryTarget()
    ErrorBoundary.wrap(target)
    token = object()

    result = getattr(target, method_name)(token, 17, flag=True)

    assert result is target.result
    assert target.calls == [(method_name, (token, 17), {"flag": True})]


@pytest.mark.parametrize("method_name", ["first", "second"])
def test_error_boundary_reports_the_failing_method(method_name, monkeypatch):
    target = _BoundaryTarget()
    error = RuntimeError("failed call")
    target.error = error
    failures = []
    monkeypatch.setattr(
        ErrorBoundary, "_on_error", lambda tag, caught: failures.append((tag, caught))
    )
    ErrorBoundary.wrap(target)

    assert getattr(target, method_name)() is None
    assert failures == [(method_name, error)]


@pytest.mark.parametrize("method_name", ["first", "second"])
def test_error_boundary_propagates_base_exceptions(method_name, monkeypatch):
    class Abort(BaseException):
        pass

    target = _BoundaryTarget()
    target.error = Abort("abort call")
    failures = []
    monkeypatch.setattr(
        ErrorBoundary, "_on_error", lambda tag, caught: failures.append((tag, caught))
    )
    ErrorBoundary.wrap(target)

    with pytest.raises(Abort) as caught:
        getattr(target, method_name)()

    assert caught.value is target.error
    assert failures == []


def test_error_boundary_wrapping_twice_is_idempotent():
    target = _BoundaryTarget()
    ErrorBoundary.wrap(target)
    first = target.first
    second = target.second

    ErrorBoundary.wrap(target)

    assert target.first is first
    assert target.second is second
    assert target.first() is target.result
    assert target.calls == [("first", (), {})]
