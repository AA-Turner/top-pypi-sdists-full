import io
import logging
import click
from click_default_group import DefaultGroup

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}

class RichGroup(DefaultGroup):
    def format_help(self, ctx, formatter):
        super().format_help(ctx, formatter)
        sio = io.StringIO()
        print('\nqing COMMAND --help  Show usage of a COMMAND', file=sio)
        formatter.write(sio.getvalue())

@click.group(invoke_without_command=True, cls=RichGroup, default='repl', default_if_no_args=True)
def cli():
    pass