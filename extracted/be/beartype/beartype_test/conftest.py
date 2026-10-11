#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2026 Beartype authors.
# See "LICENSE" for further details.

'''
:mod:`pytest` **global test configuration** (i.e., early-time configuration
guaranteed to be run by :mod:`pytest` *after* passed command-line arguments are
parsed).

:mod:`pytest` implicitly imports *all* functionality defined by this module
into *all* submodules of this subpackage.

See Also
--------
https://github.com/pytest-dev/pytest-asyncio/blob/master/pytest_asyncio/plugin.py
    :mod:`pytest` plugin strongly inspiring this implementation. Despite its
    popularity, pytest-asyncio is mostly unmaintained, poorly commented and
    documented, overly obfuscatory, has an extreme number of unresolved issues
    and unmerged pull requests, and just generally exhibits code smells.
'''

# ....................{ TODO                               }....................
#FIXME: Consider refactoring the pytest_pyfunc_call() hook defined below into:
#* A pull request against pytest itself. Pytest absolutely requires support for
#  asynchronous test functions. This is 2021, people.
#* A new competing "pytest-async" plugin. This is substantially easier but less
#  ideal, as pytest *REALLY* both wants and needs this functionality.

# ....................{ IMPORTS                            }....................
from collections.abc import Coroutine
from inspect import iscoroutinefunction
from pytest import hookimpl
from warnings import (
    catch_warnings,
    simplefilter,
)

# ....................{ HOOKS ~ configure                  }....................
# This function hooks the same pytest plugin API as the function of the same
# name in the higher-level "conftest" plugin. These two functions are intended
# to be run at opposite times during the test execution process and thus
# *CANNOT* be aggregated into a single function hooking this pytest plugin API.
# These functions *MUST* thus be preserved as independent. However, they share
# the same name and thus *CANNOT* be defined in the same submodule. Each of
# these functions *MUST* be defined in a unique "conftest" plugin. *sigh*
@hookimpl(hookwrapper=True, tryfirst=True)
def pytest_pyfunc_call(pyfuncitem: 'pytest.Function') -> None:
    '''
    Hook wrapper called immediately *before* calling the passed test function.

    Specifically, this hook wrapper:

    * If this test function is synchronous (i.e., declared with ``def``),
      preserves this test function as is.
    * If this test function is asynchronous (i.e., declared with ``async
      def``), wraps this test function in a synchronous wrapper function
      synchronously running this test function under an event loop uniquely
      isolated to this test function. For safety, each asynchronous test
      function is run under a new event loop.

    This wrapper wraps all non-wrapper ``pytest_pyfunc_call()`` hooks and is
    hopefully called *before* all wrapper ``pytest_pyfunc_call()`` hooks. See
    also `the official pytest hook wrapper documentation <hook wrapper_>`__.

    Parameters
    ----------
    pyfuncitem : Function
        :mod:`pytest` object encapsulating the test function to be run.

    .. _hook wrapper:
       https://docs.pytest.org/en/6.2.x/writing_plugins.html#hookwrapper-executing-around-other-hooks
    '''

    # Test function to be called by this hook.
    test_func = pyfuncitem.obj

    # If this test function is an asynchronous coroutine function (i.e.,
    # callable declared with "async def" whose body contains *NO* "yield"
    # expressions)...
    #
    # Note that we intentionally prefer calling this well-tested tester of the
    # well-tested "inspect" module rather than our comparable
    # beartype._util.func.utilfunctest.is_func_coro() tester, which is only
    # hopefully (but *NOT* necessarily) known to be working here.
    if iscoroutinefunction(test_func):
        # Defer hook-specific imports.
        from functools import partial

        # Partial object encapsulating the _test_coro_synchronously() helper
        # bound to the current "pyfuncitem" object encapsulating this test.
        #
        # Note that this logic is robust under POSIX-compliant platforms (e.g.,
        # Linux, macOS) but *EXTREMELY* fragile under Windows, where the
        # "multiprocessing.Process" class sadly leverages the mostly unusable
        # "pickle" module rather than the mostly usable third-party "dill"
        # module. Notably, we intentionally:
        # * Leverage a "partial" object (which "pickle" silently supports)
        #   rather than a closure (which "pickle" rejects with
        #   non-human-readable exceptions).
        # * Pass the actual low-level test function being tested (which "pickle"
        #   silently supports) rather than the high-level "pyfuncitem" object
        #   encapsulating that function (which "pickle" rejects with
        #   non-human-readable exceptions).
        #
        # Why does the "multiprocessing.Process" class matter? Because our
        # sibling hook of the same name defined in the higher-level "conftest"
        # plugin implements our custom @pytest.mark.run_in_subprocess mark by
        # deferring to that class, which internally defers to "pickle".
        # Previously, this implementation preferred a straightforward closure
        # approach, which prevented @pytest.mark.run_in_subprocess from being
        # applied to test coroutines. Although cumbersome, the current
        # partial()-based approach transparently supports that custom mark.
        test_coro_synchronously = partial(_test_coro_synchronously, test_func)

        # Replace the original asynchronous test coroutine unsupported by pytest
        # by this synchronous test wrapper supported by pytest.
        pyfuncitem.obj = test_coro_synchronously

    # Perform this test by calling this test function.
    yield

# ....................{ PRIVATE ~ functions                }....................
def _test_coro_synchronously(test_coro: Coroutine, *args, **kwargs) -> object:
    '''
    Synchronously run the passed :mod:`pytest` **asynchronous test coroutine**
    (i.e., callable defined as ``async def test_{test_name}(...):`` whose body
    contains *no* ``yield`` expressions) in a unique :mod:`asyncio` event loop
    isolated to the execution of this test.

    Parameters
    ----------
    test_coro: Coroutine
        Asynchronous test coroutine to be run synchronously.

    All remaining parameters are passed as is to this test coroutine.

    Returns
    -------
    object
        Arbitrary object returned by this test if any *or* :data:`None`.
    '''
    #FIXME: Raises exceptions, oddly. Go figure, huh!? Who cares. lol -> *sigh*
    # assert isinstance(test_coro, Coroutine), f'{repr(test_coro)} not coroutine.'

    # Defer package-specific imports.
    from asyncio import (
        new_event_loop,
        set_event_loop,
    )
    from beartype._util.py.utilpyversion import IS_PYTHON_AT_LEAST_3_14

    # If the active Python interpreter targets Python >= 3.14, avoid calling the
    # deprecated get_event_loop_policy() getter preferred under Python <= 3.13.
    # Instead...
    if IS_PYTHON_AT_LEAST_3_14:
        # Defer version-specific imports.
        from asyncio import get_event_loop

        # Attempt to...
        try:
            # Current event loop for the current threading context if any *OR*
            # raise a "RuntimeError" otherwise.
            event_loop_old = get_event_loop()

            # Close this loop.
            event_loop_old.close()
        # If attempting to retrieve the current event loop raised a
        # "RuntimeError", there is *NO* current event loop to be closed. In this
        # case, silently reduce to a noop.
        except RuntimeError:
            pass
    # Else, the active Python interpreter targets Python <= 3.13. In this case,
    # prefer calling the get_event_loop_policy() getter deprecated under Python
    # >= 3.14. Specifically...
    else:
        # Defer version-specific imports.
        from asyncio import get_event_loop_policy

        # With a warning context manager...
        with catch_warnings():
            # Ignore *ALL* deprecating warnings emitted by the get_event_loop()
            # function called below. For unknown reasons, CPython 3.11 devs
            # thought that emitting a "There is no current event loop" warning
            # (erroneously classified as a "deprecation") was a wonderful idea.
            # "asyncio" is arduous enough to portably support as it is.
            simplefilter('ignore', DeprecationWarning)

            # Current event loop for the current threading context if any *OR*
            # create a new event loop otherwise. Note that the higher-level
            # asyncio.get_event_loop() getter is intentionally *NOT* called
            # here, as Python 3.10 broke backward compatibility by refactoring
            # that getter to be an alias for the wildly different
            # asyncio.get_running_loop() getter, which *MUST* be called only
            # from within either an asynchronous callable or running event loop.
            # In either case, asyncio.get_running_loop() and thus
            # asyncio.get_event_loop() is useless in this context. Instead, we
            # call the lower-level get_event_loop_policy().get_event_loop()
            # getter -- which asyncio.get_event_loop() used to wrap. *facepalm*
            #
            # This getter should ideally return "None" rather than creating a
            # new event loop without our permission if no loop has been set.
            # This getter instead does the latter, implying that this closure
            # will typically instantiate two event loops per asynchronous
            # coroutine test function:
            # * The first useless event loop implicitly created by this
            #   get_event_loop() call.
            # * The second useful event loop explicitly created by the
            #   subsequent new_event_loop() call.
            #
            # Since there exists *NO* other means of querying the current event
            # loop, we reluctantly bite the bullet and pay the piper. Work with
            # me here, guys!
            event_loop_old = get_event_loop_policy().get_event_loop()

            # Close this loop, regardless of whether the prior get_event_loop()
            # call just implicitly created this loop, because the "asyncio" API
            # offers *NO* means of differentiating these two common edge cases.
            event_loop_old.close()

    # New event loop isolated to this coroutine.
    #
    # Note that this event loop has yet to be set as the current event loop for
    # the current threading context. Explicit is better than implicit.
    event_loop = new_event_loop()

    # Set this as the current event loop for this threading context.
    set_event_loop(event_loop)

    # Attempt to...
    try:
        # Awaitable coroutine object implicitly created and returned by this
        # asynchronous coroutine test function factory. Technically, coroutine
        # functions are *NOT* actually coroutines; they're just syntactic sugar
        # implemented as standard synchronous functions dynamically creating and
        # returning asynchronous coroutine objects on each call. Python, huh?
        test_coro_awaitable = test_coro(*args, **kwargs)

        # Synchronously run a new asynchronous task implicitly scheduled to run
        # this coroutine, ignoring the value returned by this coroutine (if any)
        # while reraising any exception raised by this coroutine back up the
        # call stack to pytest itself.
        test_coro_result = event_loop.run_until_complete(test_coro_awaitable)

        # Return the result returned by awaiting this test coroutine.
        return test_coro_result
    # Regardless of whether doing so raises an exception, close this event loop.
    finally:
        event_loop.close()
