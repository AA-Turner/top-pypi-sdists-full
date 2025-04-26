""" m init Entrypoint"""
import logging
import textwrap
import webbrowser
from typing import Optional

from mcli import config
from mcli.cli.m_set_unset.api_key import set_api_key
from mcli.config import MCLIConfig
from mcli.utils.utils_interactive import secret_prompt
from mcli.utils.utils_logging import OK
from mcli.utils.utils_string_functions import validate_api_plaintext

logger = logging.getLogger(__name__)

DOCS_URL = 'https://mcli.docs.mosaicml.com'
ACCOUNT_URL = 'https://console.mosaicml.com/account'


def initialize_mcli_config() -> MCLIConfig:
    """Initialize the MCLI config directory and file, if necessary

    Returns:
        True if MCLI needed to be initialized. False if initialization was already done.
    """

    if not config.MCLI_CONFIG_DIR.exists():
        config.MCLI_CONFIG_DIR.mkdir(parents=True, exist_ok=True)

    mcli_config = MCLIConfig.load_config()

    return mcli_config


def no_input_init(has_api_key: bool) -> int:
    logger.info(f'{OK} MCLI successfully initialized')
    logger.info('')

    if has_api_key:
        next_steps = f"""
        For next steps, follow the "Getting Started" section at
        [blue][link=URL]{DOCS_URL}[/][/]:

        * [cyan]Quick Start[/] - Run the Hello World example
        * [cyan]First Model[/] - Train your first 1-Billion parameter Language Model
        * [cyan]Environment Setup[/] - Set up your git, docker, and other API keys
        * [cyan]Common Commands[/] - Typical commands for users of MosaicML platform

        The MosaicML CLI can also be navigated with:

        [bold]mcli --help[/]
        """
    else:
        next_steps = f"""
    To setup access, first create your API key at: [green bold]{ACCOUNT_URL}[/].
    Then, provide your credentials to mcli with:

    [bold]mcli set api-key <value>[/]
    """

    logger.info(textwrap.dedent(next_steps).lstrip())
    return 0


def interative_init(conf: MCLIConfig) -> int:

    if not bool(conf.api_key):
        msg = f"""
        👋 Welcome to MCLI, the command line interface to the MosaicML platform

        To setup MCLI, you'll need an API key that is attached to your MosaicML account
        
        Your browser should have opened to the Mosaicml login screen screen:
        [blue][link=URL]{ACCOUNT_URL}[/][/] 
        
        Login through your company email. Click the "Add" button, enter a key 
        name, and click the create button. Copy the value of this secret key 
        and paste into the prompt below.
        """
        logger.info(textwrap.dedent(msg).lstrip())

        webbrowser.open_new_tab(ACCOUNT_URL)
        conf.api_key = secret_prompt(
            'What API key should we configure for MCLI?',
            validate=validate_api_plaintext,
        )

        conf.save_config()
        logger.info(f"{OK} Successfully updated your API key")

    return 0


def initialize_mcli(
    no_input: bool = False,
    **kwargs,
) -> int:
    del kwargs

    conf = initialize_mcli_config()

    if no_input:
        return no_input_init(bool(conf.api_key))

    if interative_init(conf):
        return 1

    msg = f"""
    You are set up and ready to start training your own models!

    For next steps, check out the MCLI docs: [blue bold][link=URL]{DOCS_URL}[/][/]

    * [cyan]First Model[/] - Train your first 1-Billion parameter Language Model
    * [cyan]Environment Setup[/] - Set up your git, docker, and other API keys
    * [cyan]Common Commands[/] - Typical commands for users of MosaicML platform

    The MosaicML CLI can also be navigated with:
    [bold]mcli --help[/]
    """
    logger.info(textwrap.dedent(msg).lstrip().rstrip())
    return 0


def initialize(api_key: Optional[str] = None):
    """Initialize the MosaicML platform

    Arguments:
        api_key: Optional value to set
    """
    initialize_mcli(mcloud_mode=True, no_input=True)

    if api_key:
        set_api_key(api_key)
