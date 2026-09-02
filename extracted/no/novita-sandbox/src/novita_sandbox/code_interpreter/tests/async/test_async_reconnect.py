from novita_sandbox.code_interpreter import AsyncSandbox


async def test_reconnect(async_sandbox: AsyncSandbox):
    sandbox_id = async_sandbox.sandbox_id

    sandbox2 = await AsyncSandbox.connect(sandbox_id)
    result = await sandbox2.run_code("x =1; x")
    assert result.text == "1"
