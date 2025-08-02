import os
import shutil
from functools import wraps
from typing import List

from qwak.exceptions import QuietError
from qwak.inner.build_logic.interface.build_logger_interface import BuildLogger
from qwak.inner.build_logic.interface.step_inteface import Step


def step_exception_handler_decorator(step: Step):
    execute_func = step.execute

    @wraps(execute_func)
    def inner_function(*args, **kwargs):
        try:
            execute_func(*args, **kwargs)
        except BaseException as e:
            if not isinstance(e, QuietError):
                build_logger: BuildLogger = step.build_logger
                build_logger.error(
                    "Build failed with Exception. See the stack trace above."
                )
                cleaning_up_after_build(step)
            raise e

    return inner_function


def build_failure_handler():
    def _exception_handler(func):
        @wraps(func)
        def inner_function(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except BaseException as e:
                if not isinstance(e, QuietError):
                    build_logger: BuildLogger = args[0].build_logger
                    build_logger.error(
                        "Build failed with Exception. See the stack trace above."
                    )
                    cleaning_up_after_build(args[0])
                raise e
        return inner_function

    return _exception_handler


def cleaning_up_after_build(step: Step):
    if os.getenv("QWAK_DEBUG") != "true":
        step.build_logger.debug("Removing Qwak temp artifacts directory")
        shutil.rmtree(step.context.host_temp_local_build_dir, ignore_errors=True)


def add_decorator_to_steps(phase_steps: List[Step]):
    for step in phase_steps:
        if not hasattr(step.execute, '__wrapped__'):
            step_exception_handler_decorator(step)

    return phase_steps
