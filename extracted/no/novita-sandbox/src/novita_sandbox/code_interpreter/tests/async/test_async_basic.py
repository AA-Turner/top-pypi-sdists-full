from novita_sandbox.code_interpreter import AsyncSandbox


async def test_basic(async_sandbox: AsyncSandbox):
    result = await async_sandbox.run_code("x =1; x")
    assert result.text == "1"
