import click
from . import credentials
from ..output.table import output_entry


@click.command(name="add-object-credential")
@click.option("--object-id", required=True)
@click.option("--object-type", required=True)
@click.option("--org-id", default=None)
@click.option("--priority", type=int, default=0)
@click.option("--purpose", required=True)
@click.option("--encrypt", default=True)
@click.option("--username", default=None)
@click.option("--password", default=None)
@click.option("--private-key", type=click.File("r"), default=None)
@click.option("--private-key-passphrase", default=None)
@click.pass_context
def cli_command_add_object_credential(
    ctx, private_key, username, password, encrypt, private_key_passphrase, **kwargs
):
    secrets = credentials.make_secrets(
        private_key=private_key,
        username=username,
        password=password,
        encrypt=encrypt,
        private_key_passphrase=private_key_passphrase,
    )

    output_entry(ctx, credentials.add_object_credentials(ctx, secrets=secrets, **kwargs))


@click.command(name="get-object-credential")
@click.option("--object-credential-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_get_object_credential(ctx, **kwargs):
    output_entry(ctx, credentials.get_object_credential(ctx, **kwargs).to_dict())


@click.command(name="delete-object-credential")
@click.option("--object-credential-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def cli_command_delete_object_credential(ctx, **kwargs):
    credentials.delete_object_credential(ctx, **kwargs)


@click.command(name="list-object-credentials")
@click.option("--org-id", default=None)
@click.option("--purpose", default=None)
@click.option("--object-type", default=None)
@click.option("--object-types", multiple=True, default=None)
@click.option("--object-id", default=None)
@click.option("--object-ids", multiple=True, default=None)
@click.option("--encryption-key-id", default=None)
@click.pass_context
def cli_command_list_object_credential(ctx, **kwargs):
    creds = credentials.list_object_credentials(ctx, **kwargs)
    print(credentials.format_object_credentials(ctx, creds))


@click.command(name="list-object-credentials-existence-info")
@click.option("--org-id", default=None)
@click.option("--purpose", default=None)
@click.option("--object-type", default=None)
@click.option("--object-types", multiple=True, default=None)
@click.option("--object-id", default=None)
@click.option("--object-ids", multiple=True, default=None)
@click.pass_context
def cli_command_list_object_credentials_existence_info(ctx, **kwargs):
    creds = credentials.list_existence_info(ctx, **kwargs)
    print(credentials.format_object_credential_existence_info(ctx, creds))


all_funcs = [func for func in dir() if "cli_command_" in func]


def add_commands(cli):
    glob = globals()
    for func in all_funcs:
        cli.add_command(glob[func])
