from contextlib import asynccontextmanager
from typing import AsyncGenerator

import structlog

from mistralai.workflows.core.activity import context_var_task_queue
from mistralai.workflows.core.execution.sticky_session.get_sticky_worker_session import get_sticky_worker_session
from mistralai.workflows.core.execution.sticky_session.sticky_worker_session import StickyWorkerSession
from mistralai.workflows.core.utils.contextvars import reset_contextvar

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def run_sticky_worker_session(
    sticky_worker_session: StickyWorkerSession | None = None,
) -> AsyncGenerator[None, None]:
    """
    Route sticky activities to the same worker instance.

    All sticky activities (marked with sticky_to_worker=True) called within this context
    will execute on the same worker, enabling resource reuse and data locality.

    ## Usage Patterns

    Explicit session (can reuse across multiple scopes):
    ```python
    session = await get_sticky_worker_session()
    async with run_sticky_worker_session(session):
        await sticky_activity_1()
        await sticky_activity_2()

    # Later, same worker:
    async with run_sticky_worker_session(session):
        await sticky_activity_3()
    ```

    Implicit session (auto-created):
    ```python
    async with run_sticky_worker_session():
        await sticky_activity_1()
        await sticky_activity_2()
    ```

    ## Nesting Support

    Context managers can be nested. The inner scope temporarily overrides the outer:
    ```python
    async with run_sticky_worker_session(session_a):
        await activity()  # Uses session_a

        async with run_sticky_worker_session(session_b):
            await activity()  # Uses session_b

        await activity()  # Back to session_a
    ```

    Args:
        sticky_worker_session: Worker session to use. If None, automatically creates one
                              by calling get_sticky_worker_session().

    Yields:
        None. The context manager establishes routing state via context variables.
    """
    if sticky_worker_session is None:
        sticky_worker_session = await get_sticky_worker_session()
    token = context_var_task_queue.set(sticky_worker_session.task_queue)
    try:
        yield
    finally:
        reset_contextvar(context_var_task_queue, token)
