import pytest

from novita_sandbox.code_interpreter.code_interpreter_sync import Sandbox


@pytest.mark.skip_debug()
def test_execution_count(sandbox: Sandbox):
    sandbox.run_code("echo 'Hello!'")
    result = sandbox.run_code("!pwd")
    assert result.execution_count == 2
