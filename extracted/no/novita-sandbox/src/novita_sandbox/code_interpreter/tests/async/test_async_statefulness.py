from novita_sandbox.code_interpreter import AsyncSandbox


async def test_stateful(async_sandbox: AsyncSandbox):
    await async_sandbox.run_code("async_test_stateful = 1")

    result = await async_sandbox.run_code("async_test_stateful+=1; async_test_stateful")
    assert result.text == "2"
