from novita_sandbox.code_interpreter import AsyncSandbox


async def test_bash(async_sandbox: AsyncSandbox):
    result = await async_sandbox.run_code("!pwd")
    assert "".join(result.logs.stdout).strip() == "/home/user"
