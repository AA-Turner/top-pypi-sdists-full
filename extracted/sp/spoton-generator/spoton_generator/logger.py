import click


class Logger:
    """Class description."""

    verbose = True

    @classmethod
    def write(cls, text: str):
        if Logger.verbose:
            click.echo(text)
