import asyncio


def __sandbox():
    pass


async def __async_sandbox():
    pass


if __name__ == '__main__':
    __sandbox()
    asyncio.run(__async_sandbox())
