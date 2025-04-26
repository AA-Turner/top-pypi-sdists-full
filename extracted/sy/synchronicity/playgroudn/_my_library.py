import typing

async def foo() -> typing.AsyncGenerator[int, None]:
    yield 1
