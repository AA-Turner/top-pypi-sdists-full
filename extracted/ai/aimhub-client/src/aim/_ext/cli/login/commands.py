import os
import click
import requests


@click.command('login')
@click.argument('url', required=True, type=str)
@click.option('--email', prompt=True)
@click.option('--password', prompt=True, hide_input=True)
def login(url, email, password):
    """
        Login to remote Aimhub server
    """

    if url.endswith('/'):
        url = url[:-1]
    data = {'email': email, 'password': password}
    login_api = f'{url}/api/auth/ts/login/'
    response = requests.post(login_api, data=data)

    if response.status_code == 401:
        raise Exception('Incorrect email or password provided.')

    if response.status_code != 200:
        raise Exception(response.text)

    access_token = response.json().get('access_token')

    token_file_path = os.path.expanduser('~/.aimhub_user_token')

    with open(token_file_path, 'w+') as f:
        f.write(access_token)
