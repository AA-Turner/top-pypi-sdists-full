import structlog
import temporalio
import temporalio.workflow

from mistralai.workflows.core.activity import activity

from .sticky_worker_session import StickyWorkerSession

logger = structlog.get_logger(__name__)

GET_STICKY_WORKER_SESSION_ACTIVITY_NAME = "get_sticky_worker_session"


@activity(name=GET_STICKY_WORKER_SESSION_ACTIVITY_NAME, _skip_registering=True)
async def get_sticky_worker_session() -> StickyWorkerSession:
    """
    Template activity replaced by workers to return their sticky task queue name.

    Each worker replaces this template at startup with its own implementation that returns
    a unique task queue name. This enables sticky routing: once invoked, you get a task
    queue bound to that specific worker instance.

    ## How It Works

    At worker startup, each worker generates a unique sticky task queue and creates
    its own implementation:

    ```python
    sticky_task_queue = f"{base}-sticky-worker-session-{uuid4().hex}"

    @activity(name=GET_STICKY_WORKER_SESSION_ACTIVITY_NAME, _skip_registering=True)
    async def get_sticky_worker_session() -> StickyWorkerSession:
        return StickyWorkerSession(task_queue=sticky_task_queue)
    ```

    When invoked from a workflow:
    1. Temporal routes the activity to any available worker
    2. That worker returns its unique sticky task queue name
    3. Subsequent activities can target that specific task queue
    4. Since only that worker listens on that queue, they execute on the same instance

    ## Usage

    ```python
    # Get a sticky task queue from whichever worker executes this
    session = await get_sticky_worker_session()

    # Route subsequent activities to that same worker via its task queue
    async with run_sticky_worker_session(session):
        await sticky_activity_1()  # Routed to the captured worker
        await sticky_activity_2()  # Same worker
    ```

    Returns:
        StickyWorkerSession containing a worker-specific task queue name.

    Raises:
        NotImplementedError: If called directly in workflow context without being
                           replaced by worker-specific implementation.
    """
    if temporalio.workflow.in_workflow():
        raise NotImplementedError(
            "This template should never execute directly. Workers create their own implementation."
        )

    # Fallback for local/test execution
    return StickyWorkerSession(task_queue="local")
