import click
from aheadworks_composer_manager.model.extension import Extension
import requests
import os
import json

class ApiError(click.ClickException):
    pass

def api_call(ctx, method, endpoint, *args, **kwargs):
    headers = {'Content-Type': 'application/json',
               'Authorization': 'Bearer {0}'.format(ctx.obj['REPO_TOKEN'])}

    req = requests.Request(method, ctx.obj['REPO_FULL_URL'] + endpoint, headers=headers, *args, **kwargs)
    prepared = req.prepare()

    if ctx.obj['PRINT_REQUESTS']:
        click.echo("[DEBUG] >>> ({method}) {req.url} {req.body}".format(method=method.upper(), req=prepared, args=args, kwargs=kwargs))

    s = requests.Session()
    resp = s.send(prepared)

    if ctx.obj['PRINT_REQUESTS']:
        click.echo("[DEBUG] <<< (HTTP {resp.status_code}) {resp.text}".format(resp=resp))

    try:
        res = resp.json()
        if 'error' in res:
            raise ApiError(res['error'])
        return res
    except json.decoder.JSONDecodeError as e:
        if resp.text:
            raise ApiError("{}\n{}".format(e, resp.text))
        return {}


@click.group()
@click.pass_context
@click.option('--repo-url', envvar="REPO_URL", required=True)
@click.option('--repo-login', envvar="REPO_LOGIN", required=True)
@click.option('--repo-token', envvar="REPO_TOKEN", required=True)
@click.option('-p','--print-requests', is_flag=True, help="Verbosely print API requests")
def cli(ctx, repo_url, repo_login, repo_token, print_requests):
    ctx.obj = {}
    ctx.obj['REPO_FULL_URL'] = 'https://' + repo_login + '@' + repo_url
    ctx.obj['REPO_URL'] = repo_url
    ctx.obj['REPO_LOGIN'] = repo_login
    ctx.obj['REPO_TOKEN'] = repo_token
    ctx.obj['PRINT_REQUESTS'] = print_requests


@cli.command()
@click.pass_context
def get_packages(ctx):
    result = api_call(ctx, 'get', '/packages')
    click.echo(result)


@cli.command()
@click.pass_context
@click.argument('name')
def find_package(ctx, name):
    result = api_call(ctx, 'get', '/packages', params={'name': name})
    click.echo(result)


@cli.command()
@click.pass_context
@click.argument('name')
@click.argument('description', required=True)
def create_package(ctx, name, description):
    data = {
        'name': name,
        'description': description
    }
    result = api_call(ctx, 'post', '/packages', json=data)
    click.echo(result)


@cli.command()
@click.pass_context
@click.argument('package_zip', type=click.Path(exists=True, dir_okay=False))
@click.option('--status', default=1)
@click.option('--filename', required=False, help="Specify if filename is different at server")
def send_package(ctx, package_zip, status, filename):

    with Extension(package_zip) as e:
        create_package_data = {
            "name": e.meta.name,
            "description": e.meta.description,
            "status": 1
        }

        create_version_data = {
            'name': e.meta.version,
            'package': e.meta.name,
            'status': status,
            'filename': os.path.basename(filename or package_zip)
        }


        package_exists = api_call(ctx, 'get', '/packages', params={'name': e.meta.name})
        if len(package_exists):
            res = api_call(ctx, 'put', '/packages/%s' % package_exists[0]["id"], json=create_package_data)
        else:
            res = api_call(ctx, 'post', '/packages', json=create_package_data)

        version_exists = api_call(ctx, 'get', '/versions', params={'package': e.meta.name, 'name': e.meta.version})

        if len(version_exists):
            res = api_call(ctx, 'put', '/versions/%s' % version_exists[0]['id'], json=create_version_data)
            click.echo("Updated version {v[name]}".format(v=create_version_data))
        else:
            res = api_call(ctx, 'post', '/versions', json=create_version_data)
            click.echo("Created version {v[name]}".format(v=create_version_data))


@cli.command()
@click.pass_context
@click.argument('email', required=True)
@click.argument('public_key', required=True)
@click.argument('private_key', required=True)
def create_consumer(ctx, email, public_key, private_key):
    api_call(ctx, 'get', '/consumers')
    res = api_call(ctx, 'post', '/consumers', json={'email': email, 'public_key': public_key, 'private_key': private_key})
    click.echo("Created consumer #{res[id]} for email {res[email]}, pubkey {res[public_key]}".format(res=res))

@cli.command()
@click.pass_context
@click.argument('email', required=True)
@click.argument('public_key', required=True)
@click.argument('private_key', required=True)
def set_key(ctx, email, public_key, private_key):

    """Get consumer key(s)"""
    params = {'email': email}
    consumers = api_call(ctx, 'get', '/consumers', params=params)

    for c in consumers:
        cid = c['id']
        rq = {
            'email': email,
            'public_key': public_key,
            'private_key': private_key,
            'source': c['source'],
            'reference': c['reference']
        }
        res = api_call(ctx, 'put', '/consumers/%s' % cid,
                       json=rq)
        click.echo("Updated consumer #%s" % cid)
        return
    click.echo("No consumer match for email %s" % email, err=True)


@cli.command()
@click.pass_context
@click.argument('email', nargs=-1)
@click.option('--format', required=False)
def find_consumer(ctx, email, format):
    """Get consumer key(s)"""
    params = {'email': email}
    consumers = api_call(ctx, 'get', '/consumers', params=params)
    if not format:
        click.echo(consumers)
        return

    for c in consumers:
        click.echo(format.format(**c))


@cli.command()
@click.pass_context
@click.argument('email', required=True)
@click.argument('public_key', required=False, default='')
def delete_consumer(ctx, email, public_key):
    """Delete consumer key(s)"""
    params = {'email': email}
    if public_key:
        params.update({'public_key': public_key})
    consumers = api_call(ctx, 'get', '/consumers', params=params)

    n = 0
    for c in consumers:
        api_call(ctx, 'delete', '/consumers/%s' % c['id'])
        n += 1

    click.echo("Deleted {n} keys".format(n=n))


@cli.command()
@click.pass_context
@click.argument('package', required=True)
@click.argument('consumer', required=True, nargs=-1)
@click.option('--version', required=False, default='*')
def grant(ctx, package, consumer, version):
    """Give access to package to consumers"""
    ids = []

    for c in consumer:
        if '@' in c:
            found_consumers = [x['id'] for x in api_call(ctx, 'get', '/consumers', params={'email': c})]
            if not len(found_consumers):
                click.echo("Can't find consumer {}, skipping".format(c), err=True)
        else:
            found_consumers = [c]

        ids += found_consumers

    for cid in ids:
        # Delete permission if exists
        try:
            permissions = [p['id'] for p in api_call(ctx, 'get', '/permissions', params={'consumer_id': cid, 'package': package, 'version': version})]
            aaa = [api_call(ctx, 'delete', '/permissions/%s' % x) for x in permissions]
        except ApiError as e:
            pass
        api_call(ctx, 'post', '/permissions', json={'consumer_id': cid, 'package': package, 'version': version})

@cli.command()
@click.pass_context
@click.argument('consumer', required=True, nargs=-1)
def get_permissions(ctx, consumer):
    """Give access to package to consumers"""
    ids = []

    for c in consumer:
        if '@' in c:
            found_consumers = [x['id'] for x in api_call(ctx, 'get', '/consumers', params={'email': c})]
            if not len(found_consumers):
                click.echo("Can't find consumer {}, skipping".format(c), err=True)
        else:
            found_consumers = [c]

        ids += found_consumers

    for cid in ids:
        # Delete permission if exists
        try:
            permissions = [p for p in api_call(ctx, 'get', '/permissions', params={'consumer_id': cid})]
            click.echo(permissions)
        except ApiError as e:
            pass

if __name__ == '__main__':
    cli()
