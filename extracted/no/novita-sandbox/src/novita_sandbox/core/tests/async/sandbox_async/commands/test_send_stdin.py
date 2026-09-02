import asyncio

from novita_sandbox.core import AsyncSandbox


async def test_send_stdin_to_process(async_sandbox: AsyncSandbox):
    ev = asyncio.Event()

    def handle_event(stdout: str):
        ev.set()

    cmd = await async_sandbox.commands.run(
        "cat",
        background=True,
        stdin=True,
        on_stdout=handle_event,
    )
    await async_sandbox.commands.send_stdin(cmd.pid, "Hello, World!")

    await ev.wait()

    assert cmd.stdout == "Hello, World!"


async def test_send_empty_stdin_to_process(async_sandbox: AsyncSandbox):
    cmd = await async_sandbox.commands.run("cat", background=True, stdin=True)
    await async_sandbox.commands.send_stdin(cmd.pid, "")
    await cmd.kill()
    assert cmd.stdout == ""


async def test_send_special_characters_to_process(async_sandbox: AsyncSandbox):
    ev = asyncio.Event()

    def handle_event(stdout: str):
        ev.set()

    cmd = await async_sandbox.commands.run(
        "cat",
        background=True,
        stdin=True,
        on_stdout=handle_event,
    )
    await async_sandbox.commands.send_stdin(cmd.pid, "!@#$%^&*()_+")

    await ev.wait()

    assert cmd.stdout == "!@#$%^&*()_+"


async def test_send_multiline_string_to_process(async_sandbox: AsyncSandbox):
    ev = asyncio.Event()

    def handle_event(stdout: str):
        ev.set()

    cmd = await async_sandbox.commands.run(
        "cat",
        background=True,
        stdin=True,
        on_stdout=handle_event,
    )
    await async_sandbox.commands.send_stdin(cmd.pid, "Hello,\nWorld!")

    await ev.wait()

    assert cmd.stdout == "Hello,\nWorld!"
