""" mcli modify api-key functions """
import argparse
import logging
import os
from typing import Optional

from mcli.api.engine.engine import MAPIConnection
from mcli.api.exceptions import InputDisabledError
from mcli.config import MOSAICML_API_KEY_ENV, MCLIConfig
from mcli.utils.utils_interactive import input_disabled, query_yes_no, secret_prompt
from mcli.utils.utils_logging import FAIL, OK
from mcli.utils.utils_string_functions import validate_api_plaintext

logger = logging.getLogger(__name__)
INPUT_DISABLED_MESSAGE = ('Incomplete set api-key call. Please provide api-key value if running with '
                          '`--no-input`. Check `mcli set api-key --help` for more information.')


def modify_api_key(
    api_key_value: Optional[str] = None,
    force: bool = False,
    no_input: bool = False,
    **kwargs,
) -> int:
    """Sets api key

    Args:
        api_key_value: Value to set the api key to
        force: If True, will overwrite existing API key values without asking

    Returns:
        0 if succeeded, else 1
    """
    del kwargs

    with input_disabled(no_input):
        if os.environ.get(MOSAICML_API_KEY_ENV, None):
            if not query_yes_no('An API key is already set in the environment. Would you like to override this?'):
                logger.error(f'{FAIL} Canceling setting the API key')
                return 1

        try:
            if api_key_value is None:
                api_key_value = secret_prompt('What value would you like to set?', validate=validate_api_plaintext)
        except InputDisabledError:
            logger.error(INPUT_DISABLED_MESSAGE)
            return 1

    # Get the current api key
    conf = MCLIConfig.load_config()

    current_api_key = conf.get_api_key(env_override=False)
    if current_api_key == api_key_value:
        logger.info(f"{OK} The API key has already been set with this value")
        return 0

    # Don't override existing values without confirmation
    if not force and not no_input and current_api_key:
        censored_api_key = f'{current_api_key[:3]}{(len(current_api_key) - 3)*"*"}'
        confirm = query_yes_no(f'The value of api-key is currently set to "{censored_api_key}". \n'
                               'Would you like to override this?')
        if not confirm:
            logger.error(f'{FAIL} Canceling setting the API key')
            return 1

    # Update the api key
    conf.api_key = api_key_value
    conf.save_config()

    # Reset mapi connection
    MAPIConnection.reset_connection()

    logger.info(f"{OK} Updated API Key")
    return 0


def set_api_key(api_key: str):
    """Set the api key for the MosaicML platform

    Arguments:
        api_key: value to set
    """
    return modify_api_key(api_key, force=True, no_input=True)


def configure_api_key_argparser(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        'api_key_value',
        nargs='?',
        help='API Key value',
    )
    parser.add_argument(
        '-y',
        '--force',
        dest='force',
        action='store_true',
        help='Skip confirmation dialog before overwriting existing api key value',
    )
    parser.add_argument('--no-input', action='store_true', help='Do not query for user input')
