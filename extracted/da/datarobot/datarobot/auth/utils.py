#
# Copyright 2025 DataRobot, Inc. and its affiliates.
#
# All rights reserved.
#
# DataRobot, Inc.
#
# This is proprietary source code of DataRobot, Inc. and its
# affiliates.
#
# Released under the terms of DataRobot Tool and Utility Agreement.
# limitations under the License.
import asyncio
import functools
from typing import Any, Callable, Coroutine, TypeVar

from typing_extensions import ParamSpec

T_Retval = TypeVar("T_Retval")
T_ParamSpec = ParamSpec("T_ParamSpec")


def syncify(
    async_func: Callable[T_ParamSpec, Coroutine[Any, Any, T_Retval]],
) -> "Callable[T_ParamSpec, T_Retval]":
    """
    Decorator to run an async function in a synchronous context.
    """

    @functools.wraps(async_func)
    def sync_wrapper(*args: T_ParamSpec.args, **kwargs: T_ParamSpec.kwargs) -> T_Retval:
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                raise RuntimeError("Cannot call a synchronous method from a running event loop.")
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(async_func(*args, **kwargs))

    return sync_wrapper
