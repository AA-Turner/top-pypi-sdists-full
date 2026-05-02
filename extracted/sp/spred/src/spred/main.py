import click
from .commands.analyze import analyze
from .commands.enrich import enrich
from .commands.plot import plot_volcano, plot_manhan
from .commands.run_all import run_all

try:
    from importlib.metadata import version, PackageNotFoundError
except ImportError:
    # For Python <3.8, fallback to importlib-metadata package
    from importlib_metadata import version, PackageNotFoundError

try:
    __version__ = version("spred")  # 这里用的是 pyproject.toml 中的项目名
except PackageNotFoundError:
    __version__ = "unknown"

@click.group()
@click.version_option(version=__version__)
def cli():
    """Splicing-regulatory Driver Genes (SDG) Identification Tool"""
    pass

cli.add_command(analyze)
cli.add_command(enrich)
cli.add_command(plot_volcano)
cli.add_command(plot_manhan)
cli.add_command(run_all)

if __name__ == '__main__':
    cli()
