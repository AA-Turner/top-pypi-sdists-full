import asyncio
import pytest
from flowtask.task import Task


pytestmark = pytest.mark.asyncio

@pytest.mark.parametrize("program, task", [
    ('test', 'QueryToInsert'),
])
async def test_prepared(event_loop, program, task):
    task = Task(program=program,task=task, debug=True, loop=event_loop)
    error = None
    async with task as t:
        status = await t.start()
        pytest.assume(status is True)
        await t.prepare()
        try:
            result = await t.run()
        except Exception as e:
            print(e)
            error = e
        pytest.assume(not error)
        pytest.assume(result is not None)
    print('::: Basic Stats ::: ')
    print(task.stats)
    assert task.stats is not None

def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
