import click
import time
import os
import re
from springlabs_cc_ricardo.utils import createDjangoProject, createFlaskProject
from springlabs_cc_ricardo import __version__ as version


def validate_name(ctx, param, value):
    """
        Función que valida si nommbre del proyecto se encuentra en formato correcto
    """
    namesNoValid = ["api", "core", "graphql_api", "tests", "models_app"]
    validName = re.compile(
        r"^(?=.{4,25}$)(?![_])(?!.*[_]{2})[a-z0-9_]+(?<![_])$")
    if validName.search(value) == None:
        message = "The project name should only contain lowercase letters,numbers,underscores (4-25 characters)"
        raise click.BadParameter(message)
    if value in namesNoValid:
        raise click.BadParameter(
            f"The project name can't be called such as one of the following list {namesNoValid}")
    return value


def validate_database(ctx, param, value):
    """
        Función que valida que opciones de database sean adecuadas según el
        framework:
        Django  ->  (postgres, mysql)
        Flask   ->  (mongo)
    """
    db_accepted_flask = ["mongo", ]
    db_accepted_django = ["postgres", "mysql"]
    if ctx.params['framework'] == "Django":
        if value in db_accepted_django:
            return value
        else:
            message = f"invalid choice from framework Django: {value}"
            possibilities = db_accepted_django
    elif ctx.params['framework'] == "Flask":
        if value in db_accepted_flask:
            return value
        else:
            message = f"invalid choice from framework Flask: {value}"
            possibilities = db_accepted_flask

    raise click.NoSuchOption(
        option_name="option_name", message=message, possibilities=possibilities)


def validate_diseno(ctx, param, value):
    """
        Función que valida que opciones de diseño sean adecuadas según el
        framework:
        Django  ->  (logico, fisico)
        Flask   ->  (logico)
    """
    diseno_accepted_flask = ["logico", ]
    diseno_accepted_django = ['logico', 'fisico']

    if ctx.params['framework'] == "Django":
        if value in diseno_accepted_django:
            return value
        else:
            message = f"invalid design choice from framework Django: {value}"
            possibilities = diseno_accepted_django
    elif ctx.params['framework'] == "Flask":
        if value in diseno_accepted_flask:
            return value
        else:
            message = f"invalid design choice from framework Flask: {value}"
            possibilities = diseno_accepted_flask

    raise click.NoSuchOption(
        option_name="option_name", message=message, possibilities=possibilities)


@click.group(invoke_without_command=False)
@click.version_option(version=version, prog_name="Springlabs Django Manager(no es copia)", message="%(prog)s, v%(version)s")
@click.pass_context
def cli(ctx):
    """Springlabs Manager projects."""
    ctx.invoked_subcommand


@cli.command()
@click.option('-fw', '--framework',
              prompt='Framework a utilizar',
              default="Django",
              show_default=True,
              type=click.Choice(['Django', 'Flask'], case_sensitive=False),
              help='Python Framework to use')
@click.option('-db', '--database',
              prompt='Database a utilizar',
              default="postgres",
              show_default=True,
              type=click.Choice(
                  ['postgres', 'mysql', 'mongo'], case_sensitive=False),
              help='Database engine to use',
              callback=validate_database)
@click.option('-d', '--diseno',
              prompt='Diseño de database a utilizar',
              default="logico",
              show_default=True,
              type=click.Choice(
                  ['logico', 'fisico'], case_sensitive=False),
              help='Database design to use',
              callback=validate_diseno)
@click.option('-n', '--name',
              prompt='Project Name',
              help='Project Name',
              callback=validate_name)
def create_project(framework, database, name, diseno):
    """ Create a new Python project """
    if framework == "Django":
        message, result = createDjangoProject(
            name=name, database=database, design=diseno)
    elif framework == "Flask":
        message, result = createFlaskProject(
            name=name, database=database, design=diseno)
    if result == True:
        message = f"Se creó proyecto {framework}-{database}({diseno}) [{name}] correctamente"
        click.secho(message, fg='green')
    else:
        message = "Error: " + message
        click.secho(message, fg='red')


if __name__ == '__main__':
    cli()
