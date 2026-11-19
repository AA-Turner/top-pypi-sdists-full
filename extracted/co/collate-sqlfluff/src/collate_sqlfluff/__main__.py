"""Export cli to __main__ for use like python -m collate_sqlfluff."""

from collate_sqlfluff.cli.commands import cli  # pragma: no cover

if __name__ == "__main__":  # pragma: no cover
    cli()  # pragma: no cover
