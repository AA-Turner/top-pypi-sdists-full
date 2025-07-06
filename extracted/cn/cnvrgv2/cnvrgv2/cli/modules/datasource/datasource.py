import click
from prettytable import PrettyTable

from cnvrgv2.cli.utils import messages
from cnvrgv2.cli.utils.decorators import prepare_command
from cnvrgv2.cli.utils.dict_param import DICT
from cnvrgv2.modules.datasource import StorageTypes


@click.group(name='datasource')
def datasource_group():
    pass


# TODO Rethink aws concrete parameters like bucket name and path

@datasource_group.command(name="create")
@click.option('-n', '--name', prompt=messages.DATASOURCE_NAME, help=messages.DATASOURCE_NAME_HELP)
@click.option('-t', '--type', type=click.Choice(StorageTypes), prompt=messages.DATASOURCE_TYPE,
              help=messages.DATASOURCE_TYPE_HELP)
@click.option('-bn', '--bucket-name', prompt=messages.DATASTORE_BUCKET, help=messages.DATASTORE_BUCKET_HELP)
@click.option('-c', '--credentials', type=DICT, prompt=messages.DATASOURCE_CREDENTIALS,
              help=messages.DATASOURCE_CREDENTIALS_HELP)
@click.option('-r', '--region', prompt=messages.DATASOURCE_REGION, help=messages.DATASOURCE_REGION_HELP)
@click.option('-d', '--description', prompt=messages.DATASOURCE_DESCRIPTION, help=messages.DATASOURCE_DESCRIPTION_HELP)
@click.option('-p', '--public', is_flag=True, prompt=messages.DATASOURCE_PUBLIC, help=messages.DATASOURCE_PUBLIC_HELP)
@click.option('-pa', '--path', prompt=messages.DATASOURCE_PATH, help=messages.DATASOURCE_PATH_HELP)
@click.option('-e', '--endpoint', prompt=messages.DATASOURCE_ENDPOINT, help=messages.DATASOURCE_ENDPOINT)
@click.option('-u', '--users', default=[], prompt=messages.DATASOURCE_USERS, help=messages.DATASOURCE_USERS_HELP)
@prepare_command()
def create_datasource(cnvrg, logger, name, storage_type, bucket_name, credentials, region, description, public, path,
                      endpoint, users):
    """
    @param users:
    @param endpoint:
    @param path:
    @param public:
    @param description:
    @param region:
    @param credentials:
    @param bucket_name:
    @param storage_type:
    @param name:
    @param cnvrg:
    @param logger:
    @param slug:
    @return:
    """
    try:
        ds = cnvrg.datasources.create(
            name=name,
            storage_type=storage_type,
            bucket_name=bucket_name,
            credentials=credentials,
            region=region,
            description=description,
            public=public,
            path=path,
            endpoint=endpoint,
            users=users
        )
        logger.log_and_echo(f"A new datasource with the slug: {ds.slug} created!")
    except Exception as e:
        logger.log_and_echo(f"Failed to create datasource. Error: {e}")


@datasource_group.command(name="delete-datasource")
@click.option('-s', '--slug', prompt=messages.DATASOURCE_SLUG_HELP, help=messages.DATASOURCE_SLUG)
@prepare_command()
def delete_datasource(cnvrg, logger, slug):
    """
    @param cnvrg:
    @param logger:
    @param slug:
    @return:
    """
    try:
        ds = cnvrg.datasources.get(slug)
        ds.delete()
    except Exception:
        logger.log_and_echo("Failed to delete datasource")


@datasource_group.command()
@click.option('-s', '--slug', prompt=messages.DATASOURCE_SLUG_HELP, help=messages.DATASOURCE_SLUG)
@click.option('-p', '--page-size', help=messages.DATASOURCE_PAGE_SIZE_HELP)
@click.option('-w', '--max-workers', help=messages.DATASOURCE_MAX_WORKERS_HELP)
@click.option('-f', "--force", is_flag=True, help=messages.DATASOURCE_FORCE)
@click.option('-i', '--skip-if-exists', is_flag=True, help=messages.DATASOURCE_IGNORE_FILE_ERROR)
@prepare_command()
def clone(cnvrg, logger, slug, page_size, max_workers, skip_if_exists, force):
    """
    @param cnvrg:
    @param logger:
    @param slug:
    @param page_size:
    @param max_workers:
    @param skip_if_exists:
    @param force:
    @return:
    """
    ds = cnvrg.datasources.get(slug)
    logger.log_and_echo('starting cloning datasource...')
    ds.clone(page_size=page_size, max_workers=max_workers, skip_if_exists=skip_if_exists, force=force)
    logger.log_and_echo('datasource cloned')


@datasource_group.command(name='list')
@click.option('-s', '--slug', prompt=messages.DATASOURCE_SLUG_HELP, help=messages.DATASOURCE_SLUG)
@prepare_command()
def list_command(cnvrg, slug):
    """
    @param cnvrg:
    @param slug:
    @return:
    """
    ds = cnvrg.datasources.get(slug)
    files = ds.list()
    table = PrettyTable()
    table.field_names = ["File name"]
    table.align["File name"] = 'l'
    for file in files:
        table.add_row([file])

    click.echo(table)
