"""Flowtask Data Integration Executor."""
import os
os.environ.setdefault("GIT_PYTHON_REFRESH", "quiet")

import sys
import logging
import asyncio


def _check_fast_exit() -> bool:
    """Handle --help and --version before loading heavy dependencies."""
    from .parsers.argparser import ConfigParser
    parser = ConfigParser()
    # argparse exits the process on --help / --version
    parser.parse()
    return True


def _handle_workers_command(options) -> int:
    """Route the ``workers`` subcommand to the appropriate handler.

    This function is called when ``options.workers_command == "workers"``
    is detected in the parsed CLI namespace.  It dispatches based on
    ``options.workers_action``.

    Args:
        options: The ``argparse.Namespace`` produced by
            ``ConfigParser.parse()``.

    Returns:
        Exit code — ``0`` on success, ``1`` on error.
    """
    workers_action = getattr(options, "workers_action", None)
    if workers_action == "queues":
        return _handle_workers_queues()
    # Unknown / missing action — print a helpful message
    logging.error(
        "Unknown workers action %r. Try: flowtask workers queues", workers_action
    )
    return 1


def _handle_workers_queues() -> int:
    """Execute the ``flowtask workers queues`` command.

    Instantiates :class:`~flowtask.tasks.workers.WorkerQueueInspector`,
    inspects both multiprocessing worker queues and the asyncio queue
    (if the scheduler is running in-process), formats the results as
    human-readable tables, and prints them to stdout.

    Returns:
        ``0`` on success, ``1`` when an unrecoverable error occurs.
    """
    logger = logging.getLogger("flowtask.workers.queues")
    logger.debug("Running 'flowtask workers queues'")
    try:
        from .tasks.workers import WorkerQueueInspector  # noqa: PLC0415
        inspector = WorkerQueueInspector()
        mp_workers = inspector.inspect_multiprocessing_queues()
        asyncio_tasks = inspector.inspect_asyncio_queues()
        output = inspector.format_output(mp_workers, asyncio_tasks)
        print(output)
        return 0
    except Exception as exc:  # pylint: disable=broad-except
        logging.error("Error running 'workers queues': %s", exc, exc_info=True)
        return 1


async def task(loop):
    from .runner import TaskRunner
    runner = None
    try:
        runner = TaskRunner(loop=loop)
        async with runner as job:
            if await job.start():
                await job.run()
    except Exception as e:  # pylint: disable=W0718
        logging.exception(e, stack_info=False)
    finally:
        return runner


def main():
    # Parse args first — exits immediately on --help/--version
    # without importing the heavy dependency tree.
    from .parsers.argparser import ConfigParser
    parser = ConfigParser()
    parser.parse()
    options = parser.options

    # ── Route workers subcommand (early return, no async context needed) ──
    if getattr(options, "workers_command", None) == "workers":
        sys.exit(_handle_workers_command(options))

    from .utils.uv import install_uvloop
    from .utils import cPrint
    install_uvloop()
    loop = asyncio.get_event_loop()
    loop.slow_callback_duration = 0.2
    try:
        result = loop.run_until_complete(task(loop))
        if result:
            cPrint(" === RESULT === ", level="DEBUG")
            print(result.result)
            cPrint("== Task stats === ", level="INFO")
            print(result.stats)
    finally:
        loop.stop()


if __name__ == "__main__":
    main()
