import os

import click

from cnvrgv2.cli.logger.logger import CnvrgLogger


@click.command()
def logs():
    """
    Print last 50 log files
    """
    log_file_path = os.path.join(CnvrgLogger.LOGS_DIR, CnvrgLogger.LOG_FILE_NAME)
    try:
        with open(log_file_path, 'r') as f:
            lines = f.readlines()
            if len(lines) > 50:
                lines = lines[-50:]
            for line in lines:
                click.echo(line)

        click.echo(click.style("Full logs can be seen at {}".format(CnvrgLogger.LOGS_DIR), fg="magenta", italic=True))

    except FileNotFoundError:
        click.echo("There are currently no logs available. Logs will be generated after using cli commands")
