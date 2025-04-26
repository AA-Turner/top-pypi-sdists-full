""" MCLI Entrypoint mcli config """

from mcli.api.exceptions import cli_error_handler
from mcli.config import MCLIConfig


@cli_error_handler('mcli config')
def m_get_config(**kwargs) -> int:
    """Gets the current mcli config details and prints it out

    Args:
        **kwargs:
    """
    del kwargs

    conf = MCLIConfig.load_config()

    spacer = '-' * 20

    def print_padded(text: str):
        print(f'{spacer} {text: ^20} {spacer}')

    print_padded('MCLI Config')
    print(conf)
    print_padded('END')

    return 0
