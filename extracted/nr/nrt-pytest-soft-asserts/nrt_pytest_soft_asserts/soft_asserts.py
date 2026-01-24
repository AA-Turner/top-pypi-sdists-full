import functools
import linecache
import os
from contextvars import ContextVar
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Optional, List
import inspect


class DuplicatedErrorsEnum(Enum):

    NO_DUPLICATED_ERRORS_CODE_SOURCE = 1
    NO_DUPLICATED_ERRORS_CODE_SOURCE_AND_ERROR = 2

    @property
    def is_no_duplicated_errors_code_source(self) -> bool:
        return self == DuplicatedErrorsEnum.NO_DUPLICATED_ERRORS_CODE_SOURCE

    @property
    def is_no_duplicated_errors_code_source_and_error(self) -> bool:
        return self == DuplicatedErrorsEnum.NO_DUPLICATED_ERRORS_CODE_SOURCE_AND_ERROR


@dataclass
class Failure:
    error: str
    step: str
    file_path: str
    code_line: str
    line_number: int
    count: int = 1

    def __str__(self):
        return f'[{self.count}] {self.error}'\
               f' [{self.file_path}: {self.line_number}] {self.code_line}'


class SoftAsserts:
    """
    Soft asserts class.

    @author: Eyal Tuzon.
    """

    __failures_context: ContextVar[List[Failure]] = ContextVar('soft-asserts-context', default=None)

    __logger = None
    __print_method: Optional[Callable] = None
    __current_step: Optional[str] = None
    __failure_steps: List[str] = None
    __on_failure: Callable = None
    __print_duplicate_errors: DuplicatedErrorsEnum

    def __init__(self):
        self.__validate_params()
        self.__failure_steps = []
        self.__print_duplicate_errors = DuplicatedErrorsEnum.NO_DUPLICATED_ERRORS_CODE_SOURCE

    def assert_true(self, condition, message=None, on_failure: Callable = None) -> bool:
        """"
        Asserts that the condition is True.

        :param condition: Condition to evaluate.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if the condition is True, False otherwise.
        """
        if not condition:
            error = message or 'Expected True, got False.'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_false(self, condition, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that the condition is False.

        :param condition: Condition to evaluate.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if the condition is False, False otherwise.
        """

        if condition:
            error = message or 'Expected False, got True.'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_equal(self, first, second, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that first is equal to second.

        :param first: First value.
        :param second: Second value.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if first is equal to second, False otherwise.
        """

        if first != second:
            error = message or f'{first} != {second}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_not_equal(self, first, second, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that first is not equal to second.

        :param first: First value.
        :param second: Second value.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if first is not equal to second, False otherwise.
        """

        if first == second:
            error = message or f'{first} == {second}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_greater(self, first, second, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that first is greater than second.

        :param first: First value.
        :param second: Second value.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if first is greater than second, False otherwise.
        """

        if first <= second:
            error = message or f'{first} is not greater than {second}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_greater_equal(
            self, first, second, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that first is greater than or equal to second.

        :param first: First value.
        :param second: Second value.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if first is greater than or equal to second, False otherwise.
        """

        if first < second:
            error = message or f'{first} is not greater than or equal to {second}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_less(self, first, second, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that first is less than second.

        :param first: First value.
        :param second: Second value.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if first is less than second, False otherwise.
        """

        if first >= second:
            error = message or f'{first} is not less than {second}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_less_equal(self, first, second, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that first is less than or equal to second.

        :param first: First value.
        :param second: Second value.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if first is less than or equal to second, False otherwise.
        """

        if first > second:
            error = message or f'{first} is not less than or equal to {second}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_is(self, first, second, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that first is second.

        :param first: First value.
        :param second: Second value.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if first is second, False otherwise.
        """

        if first is not second:
            error = message or f'{first} is not {second}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_is_not(self, first, second, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that first is not second.

        :param first: First value.
        :param second: Second value.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if first is not second, False otherwise.
        """

        if first is second:
            error = message or f'{first} is {second}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_is_none(self, obj, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that the object is None.

        :param obj: Object to evaluate.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if the object is None, False otherwise.
        """

        if obj is not None:
            error = message or f'{obj} is not None'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_is_not_none(self, obj, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that the object is not None.

        :param obj: Object to evaluate.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if the object is not None, False otherwise.
        """

        if obj is None:
            error = message or 'obj is None'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_in(self, obj, container, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that the object is in the container.

        :param obj: Object to evaluate.
        :param container: Container to check.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if the object is in the container, False otherwise.
        """

        if obj not in container:
            error = message or f'{obj} not in {container}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_not_in(self, obj, container, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that the object is not in the container.

        :param obj: Object to evaluate.
        :param container: Container to check.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if the object is not in the container, False otherwise.
        """

        if obj in container:
            error = message or f'{obj} in {container}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_len_equal(
            self, obj, expected_length, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that the length of the object is equal to the expected length.

        :param obj: Object to evaluate.
        :param expected_length: Expected length.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if the length of the object is equal to the expected length, False otherwise.
        """

        if len(obj) != expected_length:
            error = message or f'Length of {obj} is {len(obj)}, expected {expected_length}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_is_instance(self, obj, cls, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that the object is an instance of the specified class.

        :param obj: Object to evaluate.
        :param cls: Class to check.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if the object is an instance of the specified class, False otherwise.
        """

        if not isinstance(obj, cls):
            error = message or f'{obj} is not instance of {cls}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_not_is_instance(self, obj, cls, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that the object is not an instance of the specified class.

        :param obj: Object to evaluate.
        :param cls: Class to check.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if the object is not an instance of the specified class, False otherwise.
        """

        if isinstance(obj, cls):
            error = message or f'{obj} is instance of {cls}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_almost_equal(
            self, first, second, delta, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that first is almost equal to second within the given delta.

        :param first: First value.
        :param second: Second value.
        :param delta: Maximum difference for which first and second are considered almost equal.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if first is almost equal to second, False otherwise.
        """

        if not self.__is_almost_equal(first, second, delta):
            error = message or f'Assertion failed: {first} not almost equal to {second}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_not_almost_equal(
            self, first, second, delta, message=None, on_failure: Callable = None) -> bool:
        """
        Asserts that first is not almost equal to second within the given delta.

        :param first: First value.
        :param second: Second value.
        :param delta: Maximum difference for which first and second are considered almost equal.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: True if first is not almost equal to second, False otherwise.
        """

        if self.__is_almost_equal(first, second, delta):
            error = message or f'Assertion failed: {first} almost equal to {second}'
            self.__append_to_failures(error)
            self.__execute_on_failure(on_failure)
            return False

        return True

    def assert_raises(self, exception, method: Callable, *args, **kwargs) -> bool:
        """
        Asserts that the specified exception is raised when calling
        the method with the given arguments.

        :param exception: Exception class to check.
        :param method: Method to call.
        :param args: Positional arguments to pass to the method.
        :param kwargs: Keyword arguments to pass to the method.

        :return: True if the exception is raised, False otherwise.
        """

        try:
            method(*args, **kwargs)
            error = f'{exception} not raised'
            self.__append_to_failures(error)
            return False
        except Exception as e:
            if not isinstance(e, exception):
                error = f'{e} is not instance of {exception}'
                self.__append_to_failures(error)
                return False

        return True

    def assert_raised_with(self, exception, message=None, on_failure: Callable = None):
        """
        Context manager to assert that the specified exception is raised.

        :param exception: Exception class to check.
        :param message: Optional message to display on failure.
        :param on_failure: Optional callable to execute on failure.

        :return: Context manager.
        """

        on_failure = on_failure or self.__on_failure

        class AssertRaises:

            __exception = None
            __append_to_failures: Callable = None

            def __init__(self, e, append_to_failures: Callable):
                self.__exception = e
                self.__append_to_failures = append_to_failures

            def __enter__(self):
                return self

            async def __aenter__(self):
                return self

            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type is None:
                    error = message or f'{self.__exception} not raised'
                    self.__append_to_failures(error)
                    self.__execute_on_failure()
                elif exc_type != self.__exception:
                    error = message or f'{exc_type} is not type of {self.__exception}'
                    self.__append_to_failures(error)
                    self.__execute_on_failure()

                return True

            async def __aexit__(self, exc_type, exc_val, exc_tb):
                return self.__exit__(exc_type, exc_val, exc_tb)

            @classmethod
            def __execute_on_failure(cls):
                if callable(on_failure):
                    on_failure()

        return AssertRaises(exception, self.__append_to_failures)

    def assert_all(self):
        """
        Asserts that there are no failures.
        Raises an AssertionError with all failures if there are any.

        :raises AssertionError: If there are any failures.
        """

        self.unset_step()

        if self.failures:
            failures = self.failures.copy()
            self.__failures_context.set([])

            self.failure_steps = (
                list(
                    dict.fromkeys(
                        [failure.step for failure in failures if failure.step is not None]
                    )
                )
            )

            errors = '\n'.join([str(failure) for failure in failures])

            ex = AssertionError(f'\n{errors}')
            ex.failures = failures
            raise ex

    def init_failure_steps(self):
        """
        Initializes the failure steps list.
        """

        self.failure_steps = []

    def is_in_failure_steps(self, step: str) -> bool:
        """
        Checks if the given step is in the failure steps list.

        :param step: Step to check.

        :return: True if the step is in the failure steps list, False otherwise.
        """

        return step in self.failure_steps

    def set_on_failure(self, on_failure: Callable):
        """
        Sets the on_failure callable to be executed on each failure.
        This callable will be used if no on_failure is provided
        in the individual assert methods.

        :param on_failure: Callable to execute on failure.
        """

        self.__on_failure = on_failure

    def set_step(self, step: str):
        """
        Sets the current step for failures.

        :param step: Step to set.
        """

        self.__current_step = step

    def unset_step(self):
        """
        Unsets the current step for failures.
        """

        self.__current_step = None

    @property
    def failures(self):
        """
        Gets the list of failures.
        """

        return self.__failures_context.get() or []

    @property
    def failure_steps(self):
        """
        Gets the list of failure steps.
        """

        return self.__failure_steps

    @failure_steps.setter
    def failure_steps(self, value):
        """
        Sets the list of failure steps.
        """

        self.__failure_steps = value

    @property
    def print_duplicate_errors(self) -> DuplicatedErrorsEnum:
        """
        Gets the print duplicate errors setting.
        """

        return self.__print_duplicate_errors

    @print_duplicate_errors.setter
    def print_duplicate_errors(self, value: DuplicatedErrorsEnum):
        """
        Sets the print duplicate errors setting.

        :param value: DuplicatedErrorsEnum value.
        """

        self.__print_duplicate_errors = value

    def __enter__(self):
        return self

    async def __aenter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.assert_all()

    async def __aexit__(self, exc_type, exc_value, traceback):
        self.assert_all()

    def __append_to_failures(self, error):

        file_path, code_line, line_number = \
            self.__get_failure_file_path_and_line_code_and_line_number()

        failure = \
            Failure(
                error=error,
                step=self.__current_step,
                file_path=file_path,
                code_line=code_line,
                line_number=line_number
            )

        if self.__is_append_failure(failure):
            failures = self.failures + [failure]
            self.__failures_context.set(failures)
            self.__print_error_to_log(failure)

    def __is_append_failure(self, failure: Failure) -> bool:

        if self.print_duplicate_errors.is_no_duplicated_errors_code_source:
            return not self.__is_code_source_failure_in_failures(failure)

        if self.print_duplicate_errors.is_no_duplicated_errors_code_source_and_error:
            return not self.__is_code_source_and_error_failure_in_failures(failure)

        raise ValueError(f'Unknown duplicated errors validation: {self.print_duplicate_errors}')

    def __is_code_source_failure_in_failures(self, failure: Failure) -> bool:
        for f in self.failures:
            if f.file_path == failure.file_path and f.line_number == failure.line_number \
                    and f.code_line == failure.code_line:

                f.count += 1
                return True

        return False

    def __is_code_source_and_error_failure_in_failures(self, failure: Failure) -> bool:
        for f in self.failures:
            if f.error == failure.error and f.file_path == failure.file_path \
                    and f.line_number == failure.line_number and f.code_line == failure.code_line:

                f.count += 1
                return True

        return False

    def __execute_on_failure(self, on_failure: Callable):

        on_failure = on_failure or self.__on_failure

        if callable(on_failure):
            on_failure()

    @classmethod
    def set_logger(cls, logger):
        """
        Sets the logger to be used for logging errors.
        """

        cls.__logger = logger

    @classmethod
    def unset_logger(cls):
        """
        Unsets the logger.
        """

        cls.__logger = None

    @classmethod
    def set_print_method(cls, print_method: Callable):
        """
        Sets the print method to be used for printing errors.

        :param print_method: Callable to use for printing errors.
        """

        cls.__print_method = print_method

    @classmethod
    def unset_print_method(cls):
        """
        Unsets the print method.
        """

        cls.__print_method = None

    @classmethod
    def __print_error_to_log(cls, failure: Failure):
        cls.__validate_params()

        error = str(failure)

        if cls.__print_method:
            cls.__print_method(error)
        elif cls.__logger:
            cls.__logger.error(error)

    @classmethod
    def __validate_params(cls):
        if cls.__logger and cls.__print_method:
            raise ValueError('Cannot set both logger and print_method')

    @classmethod
    def __is_almost_equal(cls, first, second, delta):
        return abs(first - second) <= delta

    @classmethod
    def __get_failure_file_path_and_line_code_and_line_number(cls):

        frame = inspect.currentframe()
        frame = frame.f_back.f_back.f_back
        file_path = os.path.relpath(frame.f_code.co_filename)
        line_number = frame.f_lineno
        code_line = linecache.getline(file_path, line_number).strip()

        return file_path, code_line, line_number


def soft_asserts(sa: SoftAsserts):
    """
    Decorator to wrap a function with soft asserts.
    Supports both synchronous and asynchronous functions.

    Example:
        @soft_asserts(sa=sa)
        def test_function():
            sa.assert_true(False, "This will not raise immediately")

    :param sa: SoftAsserts instance.

    :return: Wrapped function.
    """
    def soft_asserts_wrapper(func):

        if inspect.iscoroutinefunction(func):
            @functools.wraps(func)
            async def soft_asserts_func_wrapper(*args, **kwargs):
                result = await func(*args, **kwargs)
                sa.assert_all()
                return result
        else:
            @functools.wraps(func)
            def soft_asserts_func_wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                sa.assert_all()
                return result

        return soft_asserts_func_wrapper

    return soft_asserts_wrapper
