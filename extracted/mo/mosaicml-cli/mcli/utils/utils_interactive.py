"""Util Functions for Interactive User Prompting"""
import functools
import logging
from typing import Any, Callable, List, Optional, TypeVar, Union, overload

import questionary
from typing_extensions import Literal

from mcli.api.exceptions import InputDisabledError, ValidationError
from mcli.utils.utils_logging import err_console

T_Option = TypeVar('T_Option')  # pylint: disable=invalid-name

logger = logging.getLogger(__name__)


def validate_true(_: Any) -> bool:
    return True


# pylint: disable-next=invalid-name
STYLE = questionary.Style([
    ('qmark', 'fg:ansigreen'),
    ('question', 'nobold'),
    ('answer', 'fg:ansibrightblue'),
    ('pointer', 'fg:ansibrightblue'),
    ('highlighted', 'fg:ansibrightblue'),
])

_INPUT_DISABLED: bool = False
_INPUT_DISABLED_MESSAGE: str = 'Found missing arguments when using `--no-input`'


def _get_validation_callback(validation_fun: Callable[[str], bool]) -> Callable[[str], Union[bool, str]]:
    """Convert a validation function to a valid interactive prompt callback

    Validation functions should take in a string and return True or False. If the input
    is invalid, they can optionally raise a ``ValidationError`` with the appropriate
    error message that will be presented to the user.

    Args:
        validation_fun: Validation function. Takes a string and returns a bool or raises ValidationError

    Returns:
        An interactive validation callback function
    """

    def validator(option: str) -> Union[bool, str]:
        try:
            success = validation_fun(option)
            return True if success else 'Invalid value'
        except ValidationError as e:
            return str(e)

    return validator


class input_disabled():
    """Context manager for enabling or disabling input

    If interactive prompts are requested while input has been disabled, an `InputDisabledError` will be thrown.

    Args:
        disabled (bool, optional): If True, disable input within the context. Defaults to True.
    """

    def __init__(self, disabled: bool = True):
        self.disabled = disabled
        self.prev: Optional[bool] = None

    @staticmethod
    def set_disabled(disabled: bool):
        globals()['_INPUT_DISABLED'] = disabled

    def __enter__(self):
        self.prev = _INPUT_DISABLED
        self.set_disabled(self.disabled)
        return self

    def __exit__(self, exc_type, value, traceback):
        assert self.prev is not None
        self.set_disabled(self.prev)
        return False


def check_input_disabled(func):
    """Decorator to check if input is disabled and error

    Args:
        func: Function to be wrapped

    Raises:
        InputDisabledError: Raised if the function is called when user inputs are disabled

    Returns:
        The wrapped function
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if _INPUT_DISABLED:
            raise InputDisabledError(_INPUT_DISABLED_MESSAGE)
        return func(*args, **kwargs)

    return wrapper


@check_input_disabled
def query_yes_no(
    message: str,
    default: bool = False,
):
    """A simple yes or no question for the user

    Args:
        message: Prompt to provide the user
        default: The default answer to provide if the users puts no response in

    Returns:
        Returns a true or false answer
    """

    question = questionary.confirm(message, default=default, auto_enter=False, style=STYLE)
    return question.unsafe_ask()


def _mandate_answer(question: questionary.Question, mandatory: bool = True) -> Optional[str]:
    """If mandatory is True, continually prompt the user until they provide an answer"""
    while True:
        answer = question.unsafe_ask()
        if answer == '':
            answer = None
        if answer or not mandatory:
            break
        err_console.print('Question is mandatory. Please provide an answer. Use Ctrl+C to exit.')
    return answer


def _make_question(question_type,
                   message: str,
                   default: Optional[str] = None,
                   validate: Optional[Callable[[str], bool]] = None) -> questionary.Question:
    """Create a questionary ``Question`` for the provided question type"""
    if not default:
        default = ''
    wrapped_validate = _get_validation_callback(validate) if validate else None
    return question_type(message, default=default, validate=wrapped_validate, style=STYLE)


@overload
def simple_prompt(message: str,
                  default: Optional[str] = None,
                  mandatory: Literal[True] = True,
                  validate: Optional[Callable[[str], bool]] = None) -> str:
    ...


@overload
def simple_prompt(message: str,
                  default: Optional[str] = None,
                  mandatory: Literal[False] = False,
                  validate: Optional[Callable[[str], bool]] = None) -> Optional[str]:
    ...


@check_input_disabled
def simple_prompt(message: str,
                  default: Optional[str] = None,
                  mandatory: bool = True,
                  validate: Optional[Callable[[str], bool]] = None) -> Optional[str]:
    """Prompt the user for response

    Args:
        message: Prompt to provide the user
        default: Default value for the user input. Defaults to None.
        mandatory: If True, the user will be required to answer the question. Defaults to True.
        validate: Validation function called on the user's input. The function should
            raise a ValidatinonError if the input is not valid and the error message will
            be presented to the user. Defaults to None for no validation.

    Returns:
        The response provided by the user
    """
    question = _make_question(questionary.text, message, default=default, validate=validate)
    return _mandate_answer(question, mandatory=mandatory)


@overload
def secret_prompt(message: str,
                  mandatory: Literal[True] = True,
                  validate: Optional[Callable[[str], bool]] = None) -> str:
    ...


@overload
def secret_prompt(message: str,
                  mandatory: Literal[False] = False,
                  validate: Optional[Callable[[str], bool]] = None) -> Optional[str]:
    ...


@check_input_disabled
def secret_prompt(message: str,
                  mandatory: bool = True,
                  validate: Optional[Callable[[str], bool]] = None) -> Optional[str]:
    """Prompt the user for a secret response

    Secret responses are printed as ****, masking the user's response in the CLI

    Args:
        message: Prompt to provide the user
        mandatory: If True, the user will be required to answer the question. Defaults to True.
        validate: Validation function called on the user's input. The function should
            raise a ValidatinonError if the input is not valid and the error message will
            be presented to the user. Defaults to None for no validation.

    Returns:
        The response provided by the user
    """
    question = _make_question(questionary.password, message, validate=validate)
    return _mandate_answer(question, mandatory=mandatory)


@overload
def file_prompt(message: str,
                default: Optional[str] = None,
                mandatory: Literal[True] = True,
                validate: Optional[Callable[[str], bool]] = None) -> str:
    ...


@overload
def file_prompt(message: str,
                default: Optional[str] = None,
                mandatory: Literal[False] = False,
                validate: Optional[Callable[[str], bool]] = None) -> Optional[str]:
    ...


@check_input_disabled
def file_prompt(message: str,
                default: Optional[str] = None,
                mandatory: bool = True,
                validate: Optional[Callable[[str], bool]] = None) -> Optional[str]:
    """Prompt the user for a file path on their current file-system

    Args:
        message: Prompt to provide the user
        default: Default value for the user input. Defaults to None.
        mandatory: If True, the user will be required to answer the question. Defaults to True.
        validate: Validation function called on the user's input. The function should
            raise a ValidationError if the input is not valid and the error message will
            be presented to the user. Defaults to None for no validation.

    Returns:
        The response provided by the user
    """
    question = _make_question(questionary.path, message, default=default, validate=validate)
    return _mandate_answer(question, mandatory=mandatory)


def _make_choices(options: List[T_Option],
                  formatter: Callable[[T_Option], str] = str,
                  defaults: Optional[List[T_Option]] = None) -> List[questionary.Choice]:
    """Make a list of questionary ``Choice``s from a list of options

    Each option will be formatted using the formatter function and the default values
    will be "checked".

    Args:
        options: List of options to choose from. Should be str or objects that can be
            formatted as strings using ``formatter``
        formatter: Formatting function to convert each option to a ``str``. Defaults to ``str``.
        defaults: Default values chosen if the user just presses Enter. Defaults to the first option.

    Raises:
        ValueError: Raised if options is not a non-empty list

    Returns:
        List of questionary ``Choice``s
    """
    if not options:
        raise ValueError(f'options must be a non-empty list. Got: {type(options)}')

    if defaults is None:
        defaults = [options[0]]

    def _make_choice(option: T_Option) -> questionary.Choice:
        return questionary.Choice(formatter(option), value=option, checked=option in defaults)

    return [_make_choice(option) for option in options]


@check_input_disabled
def choose_one(message: str,
               options: List[T_Option],
               formatter: Callable[[T_Option], str] = str,
               default: Optional[T_Option] = None) -> T_Option:
    """Choose one item from a list of options

    Args:
        message: Prompt to provide the user before options are listed
        options: List of options to choose from. Should be str or objects that can be
            formatted as strings using ``formatter``
        formatter: Formatting function to convert each option to a ``str``. Defaults to ``str``.
        default: Default value chosen if the user just presses Enter. Defaults to the first option.

    Returns:
        The option chosen by the user
    """

    choices = _make_choices(options, formatter, [default] if default else None)
    return questionary.select(
        message,
        choices,
        style=STYLE,
        pointer='➤',
        qmark='? ',
    ).unsafe_ask()
