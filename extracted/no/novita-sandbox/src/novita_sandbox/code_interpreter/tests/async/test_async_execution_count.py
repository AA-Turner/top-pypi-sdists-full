import pytest

from novita_sandbox.code_interpreter import AsyncSandbox


@pytest.mark.skip_debug()
async def test_execution_count(async_sandbox: AsyncSandbox):
    await async_sandbox.run_code("echo 'Hello!'")
    result = await async_sandbox.run_code("!pwd")
    assert result.execution_count == 2
