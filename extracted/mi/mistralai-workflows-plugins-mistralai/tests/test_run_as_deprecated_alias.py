import pytest

from mistralai.workflows.core.auth import RunAs
from mistralai.workflows.core.auth import run_as as core_run_as

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
