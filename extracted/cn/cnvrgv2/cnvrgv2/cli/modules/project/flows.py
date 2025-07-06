import click

from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.errors import CnvrgFileError


@click.group(name='flow')
def flow_group():
    pass


@flow_group.command()
@click.option('-y', '--yaml-path', default=None, help=messages.FLOW_YAML_PATH)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def create(project, logger, yaml_path, project_slug):
    """
    Creates a flow from a predefined yaml file
    """
    try:
        flow = project.flows.create(yaml_path=yaml_path)
        success_message = messages.FLOW_CREATE_SUCCESS.format(flow.title)
        logger.log_and_echo(success_message)
    except CnvrgFileError as e:
        logger.log_and_echo(str(e), error=True)
