import click

from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command


@click.group(name='library')
def library_group():
    pass


@library_group.command()
@click.option('-l', '--library', prompt=messages.LIBRARY_PROMPT_CLONE, help=messages.PROJECT_PROMPT_CLONE)
@click.option('-o', '--override', is_flag=True, default=False, help=messages.PROJECT_HELP_CLONE_OVERRIDE)
@click.option('-d', '--working-dir', default=None, help=messages.OUTPUT_DIR_LOCATION)
@prepare_command()
def clone(cnvrg, logger, library, working_dir, override):
    """
    Clones the given project to local folder
    """
    if "==" in library:
        name = library.split("==")[0]
        version = library.split("==")[1]
    else:
        name = library
        version = "latest"

    library = cnvrg.libraries.get(name)
    library_version = library.versions.get(version)

    click.echo(messages.LOG_CLONING_LIBRARY.format(name, version))
    library_version.clone(progress_bar_enabled=True, working_dir=working_dir)

    success_message = messages.LIBRARY_CLONE_SUCCESS.format(name)
    logger.log_and_echo(success_message)
