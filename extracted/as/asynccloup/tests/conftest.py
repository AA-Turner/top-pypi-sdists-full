from functools import partial
from threading import Thread

from anyio import run as anyio_run
from asyncclick.testing import CliRunner
from pytest import fixture

from tests.example_command import make_example_command
from tests.example_group import make_example_group


@fixture(scope='session')
def get_example_command():
    def get_command(tabular_help=True, align_option_groups=True):
        return make_example_command(
            align_option_groups=align_option_groups, tabular_help=tabular_help)

    return get_command


@fixture(scope='session')
def get_example_group():
    def get_group(align_sections):
        return make_example_group(align_sections=align_sections)

    return get_group


class SyncCliRunner(CliRunner):
    def invoke(self, *a, _sync=False, **k):
        fn = super().invoke
        k.setdefault("catch_exceptions", False)

        if _sync:
            return fn(*a, **k)

        # anyio now protects against nested calls, so we use a thread
        result = None

        def f():
            nonlocal result

            async def r():
                return await fn(*a, **k)

            result = anyio_run(r)  # , backend="trio")

        t = Thread(target=f, name="TEST")
        t.start()
        t.join()
        return result


@fixture(scope="function")
def runner(request):
    return SyncCliRunner()


@fixture(scope="function")
def arunner(request):
    return CliRunner()
