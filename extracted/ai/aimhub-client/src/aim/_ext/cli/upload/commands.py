import click
import shutil
import os
import requests

from aim import Repo
from aim._sdk.configs import get_aim_repo_name
from aim._sdk.utils import clean_repo_path
from aim._ext.cli.upload.utils import get_auth_headers


@click.command('upload')
@click.argument('url', required=True, type=str)
@click.option('--repo', required=False, default=os.getcwd(), type=click.Path(exists=True,
                                                                             file_okay=False,
                                                                             dir_okay=True,
                                                                             writable=True))
@click.option('--project-name', required=True, type=str)
@click.option('--cleanup', required=False, default=True, type=bool)
def upload(url, repo, project_name, cleanup):
    if not Repo.exists(repo):
        click.secho(f'\'{repo}\' is not a valid Aim Repo.', fg='yellow')
        exit(1)

    auth_headers = get_auth_headers(url)

    aim_repo_path = os.path.join(clean_repo_path(repo), get_aim_repo_name())
    upload_file = f'{project_name}.tar.bz2'

    click.echo(f'Creating archive \'{upload_file}\' for Aim Repo \'{repo}\'...')
    shutil.make_archive(project_name, 'bztar', aim_repo_path)

    click.echo(f'Archive created.')
    click.echo(f'Uploading archive \'{upload_file}\'...')
    with open(upload_file, 'rb') as stream:
        params = {'project_name': project_name}
        response = requests.post(f'{url}/api/projects/upload', data=stream, headers=auth_headers, params=params)
        if not response.ok:
            reason = response.json().get('message')
            click.secho(f'Failed to upload archive. Reason: {reason}', fg='yellow')
        else:
            click.echo(f'Upload complete.')
    if cleanup:
        os.remove(upload_file)
