import click

from cnvrgv2 import EndpointKind, EndpointEnvSetup
from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.utils.log_utils import LOGS_TYPE_OUTPUT, LOGS_TYPE_ERROR, LOGS_TYPE_INFO, LOGS_TYPE_WARNING
from cnvrgv2.cli.utils.helpers import pretty_print_predictions


@click.group(name='endpoint')
def endpoint_group():
    pass


@endpoint_group.command()
@click.option('-t', '--title', prompt=messages.ENDPOINT_PROMPT_TITLE_NAME, help=messages.ENDPOINT_HELP_TITLE,
              required=True)
@click.option('-f', '--file_name', help=messages.ENDPOINT_HELP_FILE_NAME,
              default=None)
@click.option('-fn', '--function_name',
              help=messages.ENDPOINT_HELP_FUNCTION_NAME,
              default=None)
@click.option('-k', '--kind', default=EndpointKind.WEB_SERVICE, help=messages.ENDPOINT_HELP_KIND)
@click.option('-e', '--env_setup', default=EndpointEnvSetup.PYTHON3, help=messages.ENDPOINT_HELP_ENV_SETUP)
@click.option('-te', '--templates', default=None, help=messages.ENDPOINT_HELP_TEMPLATES)
@click.option('-kb', '--kafka_brokers', default=None, help=messages.ENDPOINT_HELP_KAFKA_BROKERS)
@click.option('-kit', '--kafka_input_topics', default=None,
              help=messages.ENDPOINT_HELP_KAFKA_INPUT_TOPICS)
@click.option('-a', '--args', multiple=True, default=None, help=messages.ENDPOINT_HELP_ARGS)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def create(project,
           logger,
           title,
           file_name,
           function_name,
           kind, env_setup,
           templates,
           kafka_brokers,
           kafka_input_topics,
           args,
           project_slug):
    """
        create an endpoint
    """
    param_args = {}
    if args:
        param_args = dict([p.split('=') for p in args])

    kwargs = {
        "kind": kind,
        "env_setup": env_setup,
        "templates": templates,
        **param_args
    }

    if kind == EndpointKind.STREAM:
        kwargs["kafka_brokers"] = kafka_brokers
        kwargs["kafka_input_topics"] = kafka_input_topics

    endpoint = project.endpoints.create(title, file_name, function_name, **kwargs)

    success_message = messages.ENDPOINT_CREATE_SUCCESS.format(endpoint.title, endpoint.full_href)
    logger.log_and_echo(success_message)


@endpoint_group.command()
@click.option('-s', '--slug', default=None, help=messages.ENDPOINT_SLUG)
@click.option('-n', '--name', prompt=messages.ENDPOINT_PROMPT_METRIC_NAME, help=messages.ENDPOINT_METRIC_NAME)
@click.option('-x', '--x', prompt=messages.ENDPOINT_PROMPT_METRIC_X, help=messages.ENDPOINT_METRIC_X)
@click.option('-y', '--y', prompt=messages.ENDPOINT_PROMPT_METRIC_Y, help=messages.ENDPOINT_METRIC_Y)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def log_metric(endpoint, logger, slug, name, y, x, project_slug):
    """
        logs a metric to the endpoint
    """
    if endpoint is None:
        logger.log_and_echo(messages.ENDPOINT_DOES_NOT_EXIST, error=True)

    endpoint.log_metric(name=name, y=y, x=x)


@endpoint_group.command()
@click.option('-s', '--slug', default=None, help=messages.ENDPOINT_SLUG)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def start(endpoint, logger, slug, project_slug):
    """
      starts the current endpoint
    """
    if endpoint is None:
        logger.log_and_echo(messages.ENDPOINT_DOES_NOT_EXIST, error=True)

    endpoint.start()
    logger.log_and_echo('Endpoint {} started!'.format(slug))


@endpoint_group.command()
@click.option('-s', '--slug', default=None, help=messages.ENDPOINT_SLUG)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def stop(endpoint, logger, slug, project_slug):
    """
      stop the current endpoint
    """
    if endpoint is None:
        logger.log_and_echo(messages.ENDPOINT_DOES_NOT_EXIST, error=True)

    endpoint.stop()
    logger.log_and_echo('Endpoint {} stopped!'.format(slug))


@endpoint_group.command()
@click.option('-s', '--slug', default=None, help=messages.ENDPOINT_SLUG)
@click.option('-vs', '--version_slug', help=messages.ENDPOINT_HELP_VERSION_SLUG, required=True)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def rollback(endpoint, logger, slug, version_slug, project_slug):
    """
        Rollback an endpoint version
    """
    if endpoint is None:
        logger.log_and_echo(messages.Endpoint_DOES_NOT_EXIST, error=True)

    endpoint.rollback_version(version_slug=version_slug)

    logger.log_and_echo(messages.ENDPOINT_ROLLBACK_SUCCESS.format(slug, version_slug))


@endpoint_group.command()
@click.option('-s', '--slug', default=None, help=messages.ENDPOINT_SLUG)
@click.option('-f', '--file_name', default=None, help=messages.ENDPOINT_HELP_FILE_NAME)
@click.option('-fn', '--function_name', default=None, help=messages.ENDPOINT_HELP_FUNCTION_NAME)
@click.option('-p', '--prep_file', default=None, help=messages.ENDPOINT_HELP_PREP_FILE)
@click.option('-pf', '--prep_function', default=None, help=messages.ENDPOINT_HELP_PREP_FUNCTION)
@click.option('-mt', '--max_timeout', default=None, help=messages.ENDPOINT_HELP_MAX_TIMEOUT)
@click.option('-a', '--args', multiple=True, default=None, help=messages.ENDPOINT_HELP_ARGS)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def update(endpoint,
           slug,
           logger,
           file_name,
           function_name,
           prep_file,
           prep_function,
           max_timeout,
           args,
           project_slug):
    """
        update an endpoint
    """

    if endpoint is None:
        logger.log_and_echo(messages.Endpoint_DOES_NOT_EXIST, error=True)

    param_args = {}
    if args:
        param_args = dict([p.split('=') for p in args])

    kwargs = {
        "prep_file": prep_file,
        "prep_function": prep_function,
        "max_timeout": max_timeout,
        "file_name": file_name,
        "function_name": function_name,
        **param_args
    }
    logger.log_and_echo(messages.ENDPOINT_UPDATE_IN_PROGRESS)
    endpoint = endpoint.update_version(**kwargs)

    success_message = messages.ENDPOINT_UPDATE_SUCCESS.format(endpoint.title)
    logger.log_and_echo(success_message)


@endpoint_group.command()
@click.option('-s', '--slug', default=None, help=messages.ENDPOINT_SLUG)
@click.option('-l', '--logs', prompt=messages.ENDPOINT_PROMPT_LOG_MESSAGE,
              help=messages.ENDPOINT_HELP_LOG_MESSAGE)
@click.option('-lv', '--log_level', default=LOGS_TYPE_OUTPUT, help=messages.ENDPOINT_HELP_LOGS_TYPE)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def log(endpoint, logger, slug, logs, log_level, project_slug):
    """
        send log to the endpoint
    """
    split_logs = logs.split(",")

    if endpoint is None:
        logger.log_and_echo(messages.ENDPOINT_DOES_NOT_EXIST, error=True)

    if log_level not in (LOGS_TYPE_OUTPUT, LOGS_TYPE_ERROR, LOGS_TYPE_INFO, LOGS_TYPE_WARNING):
        logger.log_and_echo(messages.ENDPOINT_LOG_LEVEL_NOT_SUPPORTED.format(log_level), error=True)

    endpoint.log(logs=split_logs, log_level=log_level)


@endpoint_group.command()
@click.option('-s', '--slug', default=None, help=messages.ENDPOINT_SLUG)
@click.option('-st', '--start_time', default=None, help=messages.ENDPOINT_HELP_START_TIME)
@click.option('-et', '--end_time', default=None, help=messages.ENDPOINT_HELP_END_TIME)
@click.option('-o', '--offset', default=None, help=messages.ENDPOINT_HELP_OFFSET)
@click.option('-si', '--size', default=50, help=messages.ENDPOINT_HELP_BATCH_SIZE)
@click.option('-m', '--model', default=None, help=messages.ENDPOINT_HELP_MODEL_NUMBER)
@click.option('-ps', '--project-slug', help=messages.PROJECT_SLUG_HELP_TITLE, default=None, required=False)
@prepare_command()
def get_predictions(endpoint, logger, slug, start_time, end_time, offset, size, model, project_slug):
    """
        Get last 50 predictions of the endpoint
    """

    if endpoint is None:
        logger.log_and_echo(messages.ENDPOINT_DOES_NOT_EXIST, error=True)

    kwargs = {
        "size": size,
    }
    if start_time:
        kwargs['start_time'] = start_time
    if end_time:
        kwargs['end_time'] = end_time
    if offset:
        kwargs['offset'] = offset
    if model:
        kwargs['model'] = model

    res = endpoint.get_predictions(**kwargs)

    if res["total"] == 0:
        logger.log_and_echo(messages.ENDPOINT_NO_PREDICTIONS)
        return

    pretty_print_predictions(res["predictions"])
