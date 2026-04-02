import os

import click

from app.config import CONFIG

for key in CONFIG:
    os.environ[key] = CONFIG[key]


@click.group()
def cli():
    """Global CLI Group"""
    pass


import app.src.presentation.routers.auth
import app.src.presentation.routers.task


def main():
    cli(prog_name="esdd")


if __name__ == "__main__":
    main()
