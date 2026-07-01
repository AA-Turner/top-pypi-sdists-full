"""@testmu.test decorator.

Wraps test functions for lifecycle reporting (begin/pass/fail) and
verdict routing — reads testmu._test_state at exit to decide pass vs fail.

Does NOT own browser launch (testmu.run) or Locator overrides (heal patch).
"""
import asyncio
import functools

from testmu._reporter import reporter
from testmu import _test_state


def _find_page(args, kwargs):
    """Extract the page argument from args/kwargs."""
    if "page" in kwargs:
        return kwargs["page"]
    for arg in args:
        if hasattr(arg, "screenshot") and hasattr(arg, "locator"):
            return arg
    return None


def _format_remark(verdict) -> str:
    msg = str(verdict.first_error)
    if verdict.count == 1:
        return f"Step failed: {msg}"
    return f"Step failed: {msg} (and {verdict.count - 1} more steps failed)"


def test(fn):
    if asyncio.iscoroutinefunction(fn):
        @functools.wraps(fn)
        async def async_wrapper(*args, **kwargs):
            rep = reporter()
            await rep.begin_test(fn.__name__)
            _test_state.reset()
            try:
                result = await fn(*args, **kwargs)
                verdict = _test_state.get_verdict()
                if verdict.failed:
                    await rep.fail_test(RuntimeError(_format_remark(verdict)))
                else:
                    await rep.pass_test()
                return result
            except Exception as e:
                await rep.fail_test(e)
                raise
            finally:
                _test_state.reset()
        return async_wrapper
    else:
        @functools.wraps(fn)
        def sync_wrapper(*args, **kwargs):
            raise NotImplementedError(
                "Sync test functions are not yet supported. Use 'async def'."
            )
        return sync_wrapper
