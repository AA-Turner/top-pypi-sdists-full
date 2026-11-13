import pytest

from mistralai.workflows.core.auth import RunAs
from mistralai.workflows.core.auth import run_as as core_run_as
from mistralai.workflows.core.temporal.context_handler_interceptor import define_context
from mistralai.workflows.models import WorkflowContext
from mistralai.workflows.plugins.mistralai.connectors.run_as import use_executor_credentials_for

_CALLER = "<caller>"


@pytest.mark.parametrize(
    "module_name",
    [
        "mistralai.workflows.core.auth",
        "mistralai.workflows.core.auth.run_as",
        "mistralai.workflows.plugins.mistralai.connectors.run_as",
    ],
)
def test_connector_run_as_import_warns_at_caller(module_name: str) -> None:
    namespace: dict[str, object] = {}
    with pytest.warns(DeprecationWarning, match="use RunAs") as record:
        exec(compile(f"from {module_name} import ConnectorRunAs", _CALLER, "exec"), namespace)

    assert namespace["ConnectorRunAs"] is RunAs
    assert all(w.filename == _CALLER for w in record)


def test_unknown_attribute_still_raises() -> None:
    with pytest.raises(AttributeError):
        core_run_as.DoesNotExist  # noqa: B018


@pytest.mark.parametrize(
    ("run_as", "context", "expected"),
    [
        (RunAs.AUTO, WorkflowContext(namespace="ns", execution_id="exec", on_behalf_of=True), True),
        (RunAs.AUTO, WorkflowContext(namespace="ns", execution_id="exec", on_behalf_of=False), False),
        (RunAs.AUTO, None, False),
        (RunAs.DEPLOYMENT, WorkflowContext(namespace="ns", execution_id="exec", on_behalf_of=True), False),
    ],
)
def test_use_executor_credentials_for_warns_and_keeps_behavior(
    run_as: RunAs, context: WorkflowContext | None, expected: bool
) -> None:
    with define_context(context), pytest.warns(FutureWarning, match="removed in v4") as record:
        assert use_executor_credentials_for(run_as) is expected

    assert [w.filename for w in record] == [__file__]


def test_use_executor_credentials_for_rejects_executor() -> None:
    with pytest.warns(FutureWarning), pytest.raises(ValueError, match="for SDK clients only"):
        use_executor_credentials_for(RunAs.EXECUTOR)
