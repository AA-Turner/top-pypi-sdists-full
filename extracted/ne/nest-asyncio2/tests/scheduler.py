# /// script
# requires-python = ">=3.5"
# dependencies = [
#     "nest-asyncio2",
#     "wrapt~=2.0",
# ]
#
# [tool.uv.sources]
# nest-asyncio2 = { path = "../", editable = true }
# ///
import asyncio
import nest_asyncio2

nest_asyncio2.apply()

async def f1():
    await asyncio.sleep(0.1)
    return 1

async def f2():
    await asyncio.sleep(0.1)
    return 2

coroutines = []
coroutines.append(f1())
coroutines.append(f2())
async def main():
    for co in coroutines:
        await co
asyncio.run(main())
asyncio.TaskGroup().create_task
