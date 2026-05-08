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


def _resolve_task_path(options):
    """Resolve ``--program`` / ``--task`` to a file path without parsing it.

    Mirrors the suffix loop in
    ``flowtask/storages/tasks/filesystem.py:44-58`` but stops at the path
    rather than opening and parsing the file.

    Args:
        options: The ``argparse.Namespace`` produced by ``ConfigParser.parse()``.

    Returns:
        :class:`~pathlib.Path` of the first matching file, or ``None`` if no
        matching file is found.
    """
    from pathlib import Path
    from .conf import TASK_PATH

    program = getattr(options, "program", None) or "navigator"
    task_name = getattr(options, "task", None)
    if not task_name:
        return None
    base = Path(TASK_PATH) / program / "tasks"
    for ext in ("json", "yaml", "yml", "toml"):
        candidate = base / f"{task_name}.{ext}"
        if candidate.exists():
            return candidate
    return None


def _handle_syntax_command(options) -> int:
    """Run the static syntax checker for a task definition.

    Lazy-imports the syntax checker so that ``--syntax`` startup avoids
    loading the heavy TaskRunner dependency tree.  Never imports
    ``flowtask.runner.TaskRunner``.

    Args:
        options: The ``argparse.Namespace`` produced by ``ConfigParser.parse()``.

    Returns:
        Exit code: ``0`` when no errors found, ``1`` when errors found,
        ``2`` on invocation problems (bad path, missing arguments, etc.).
    """
    from .parsers.syntax import SyntaxChecker  # noqa: PLC0415 — lazy import

    logger = logging.getLogger("flowtask.syntax")
    checker = SyntaxChecker(strict=getattr(options, "syntax_strict", False))
    fmt = getattr(options, "syntax_format", "text")
    path = getattr(options, "syntax_path", None)

    try:
        if path == "-":
            content = sys.stdin.read()
            report = asyncio.run(
                checker.check_content(content, source_label="<stdin>")
            )
        elif path:
            report = asyncio.run(checker.check_file(path))
        elif getattr(options, "task", None):
            file_path = _resolve_task_path(options)
            if file_path is None:
                logger.error(
                    "Could not resolve task %r in program %r",
                    getattr(options, "task", None),
                    getattr(options, "program", None),
                )
                return 2
            report = asyncio.run(checker.check_file(file_path))
        else:
            logger.error(
                "Usage: task --syntax <path> | "
                "-p PROGRAM -t TASK --syntax | "
                "--syntax -"
            )
            return 2
    except (ValueError, OSError) as err:
        logger.error("Syntax check setup error: %s", err)
        return 2

    if fmt == "json":
        print(report.to_json(), end="")
    else:
        print(report.to_text())
    return 1 if report.has_errors() else 0


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

    # ── Route --syntax (static check, no TaskRunner) ──────────────────────
    if getattr(options, "syntax", False):
        sys.exit(_handle_syntax_command(options))

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
