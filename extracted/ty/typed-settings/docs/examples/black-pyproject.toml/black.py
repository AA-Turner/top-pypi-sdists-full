from enum import Enum

import click

import typed_settings as ts


class PyVersion(Enum):
    """
    Python versions that we support.
    """

    py313 = "3.13"
    py314 = "3.14"
    py315 = "3.15"


@ts.settings
class Settings:
    """
    Black settings.

    We limit ourselves to three options.
    """

    line_length: int = 88
    skip_string_normalization: bool = False
    target_version: PyVersion = PyVersion.py315  # Better: Auto-detect


@click.command()
@ts.click_options(
    Settings,
    ts.default_loaders(
        appname="black",
        config_files=[ts.find("pyproject.toml")],
        config_file_section="tool.black",
        env_prefix=None,
    ),
)
def cli(settings: Settings) -> None:
    print(settings)


if __name__ == "__main__":
    cli()
