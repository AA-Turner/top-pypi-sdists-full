from novita_sandbox.core import AsyncSandbox


async def test_exists(async_sandbox: AsyncSandbox):
    filename = "test_exists.txt"

    await async_sandbox.files.write(filename, "test")
    assert await async_sandbox.files.exists(filename)


async def test_does_not_exist(async_sandbox: AsyncSandbox):
    assert not await async_sandbox.files.exists("/nonexistent/path")
