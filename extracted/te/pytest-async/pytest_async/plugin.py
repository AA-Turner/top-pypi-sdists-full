import asyncio
import inspect

from _pytest.config import hookimpl


@hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem):
    testfunction = pyfuncitem.obj
    is_coroutine = False
    if inspect.iscoroutinefunction(testfunction):
        is_coroutine = True
    funcargs = pyfuncitem.funcargs
    testargs = {arg: funcargs[arg] for arg in pyfuncitem._fixtureinfo.argnames}
    result = testfunction(**testargs)
    if is_coroutine:
        asyncio.run(result)
    return True
