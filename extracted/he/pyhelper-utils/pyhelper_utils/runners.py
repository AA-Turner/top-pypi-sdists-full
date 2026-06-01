import datetime
import sys
import time
from collections.abc import Callable
from typing import Any

import rich
from simple_logger.logger import get_logger

LOGGER = get_logger(name="runners")


def function_runner_with_pdb(func: Callable, dry_run: bool = False, *args: Any, **kwargs: Any) -> Any:
    """
    Run function with support to drop into pdb.

    In order to use this function you need to have --pdb in sys.argv

    Example:
        @click.option(
            "--pdb",
            help="Drop to `ipdb` shell on exception",
            is_flag=True,
            show_default=True,
            )
        def main(pdb):
            <code>

        if __name__ == "__main__":
            function_runner_with_pdb(func=main)

    Args:
        func (Callable): Function to run
        dry_run (bool, optional): Run without drop into pdb. Defaults to False.

    Returns:
        None: if execution was successful.

    Raises:
        SystemExit: If --pdb is not in sys.argv and execution failed
    """
    start_time = time.time()
    should_raise = False

    try:
        return func(*args, **kwargs)
    except Exception as ex:  # noqa: BLE001
        if "--pdb" in sys.argv:
            _, _, tb = sys.exc_info()
            if not dry_run:
                ipdb = __import__("ipdb")  # Bypass debug-statements pre-commit hook
                ipdb.post_mortem(tb)
        else:
            rich.print(f"Failed to execute with Error {ex}")
            should_raise = True

    finally:
        total_time = datetime.timedelta(seconds=time.time() - start_time)
        rich.print(f"Total execution time: {total_time}")
        if should_raise:
            sys.exit(1)
