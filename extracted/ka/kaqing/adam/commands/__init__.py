from collections.abc import Callable
from adam.commands.command import ExtractAllOptionsHandler, ExtractOptionsHandler, ExtractSequenceOptionsHandler, ExtractTrailingOptionsHandler, ValidateArgCountHandler
from adam.repl_state import ReplState
from adam.commands.app.utils_app import AppHandler

def app(state: ReplState) -> AppHandler:
    return AppHandler(state)

def extract_options(args: list[str], options: list[str]):
    return ExtractOptionsHandler(args, options = options)

def extract_trailing_options(args: list[str], trailing: list[str]):
    return ExtractTrailingOptionsHandler(args, trailing = trailing)

def extract_all_options(args: list[str], trailing = None, sequence = None, options = None):
    return ExtractAllOptionsHandler(args, trailing = trailing, sequence = sequence, options = options)

def extract_sequence(args: list[str], sequence: list[str]):
    return ExtractSequenceOptionsHandler(args, sequence = sequence)

def validate_args(args: list[str], state: ReplState, at_least: int = 1, exactly: int = -1,
                  name: str = None, msg: Callable[[], None] = None, default: str = None,
                  separator=None):
    return ValidateArgCountHandler(args, state, at_least=at_least, exactly=exactly, name=name, msg=msg, default=default, separator=separator)