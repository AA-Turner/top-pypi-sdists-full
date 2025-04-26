import asyncio


def clack():
    print("wowez. fick")


async def slave():
    try:
        print("hello there")
        print("starting A")
        while True:
            print("B")
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("stopped A")


async def master():
    while True:
        task = asyncio.create_task(slave())
        await asyncio.sleep(4)
        task.cancel()


async def main():
    await asyncio.create_task(master())
    # async with asyncio.TaskGroup() as tg:
    #     tg.create_task(master(tg))


def mayn():
    asyncio.run(main())


# # import jurigged


# if __name__ == "__main__":
#     # jurigged.watch(str(Path.cwd() / "baddo.py"))
#     asyncio.run(main())
