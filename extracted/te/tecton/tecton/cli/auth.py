import sys
from typing import Optional

import click

from tecton import conf
from tecton._internals.utils import cluster_url
from tecton.cli import cli_utils
from tecton.cli import printer
from tecton.cli.command import TectonCommand
from tecton.identities import credentials
from tecton.identities import okta


@click.command(requires_auth=False, cls=TectonCommand)
@click.argument("tecton_url", required=False)
@click.option(
    "--manual/--no-manual",
    default=False,
    help="Manually require user to open browser and paste login token. Needed when using the Tecton CLI in a headless environment.",
)
@click.option("--okta-session-token", default=None, hidden=True, required=False)
def login(tecton_url: Optional[str], manual: bool, okta_session_token: Optional[str]):
    """Log in and authenticate Tecton CLI.

    The Tecton URL may be optionally passed on the command line as TECTON_URL, otherwise you will be prompted.
    """
    host = cluster_url()

    if tecton_url is None:
        printer.safe_print("Enter configuration. Press enter to use current value")
        prompt = "Tecton Cluster URL [%s]: " % (host or "no current value. example: https://yourco.tecton.ai")
        new_host = input(prompt).strip()
        if new_host:
            host = new_host
    else:
        host = tecton_url

    if okta_session_token:
        auth_flow_type = okta.AuthFlowType.SESSION_TOKEN
    elif manual:
        auth_flow_type = okta.AuthFlowType.BROWSER_MANUAL
    else:
        auth_flow_type = okta.AuthFlowType.BROWSER_HANDS_FREE

    temp_result, auth_code = credentials._initiate_login_and_get_auth_code(
        host=host, auth_flow_type=auth_flow_type, okta_session_token=okta_session_token
    )
    credentials._complete_login_with_auth_code(temp_result, auth_code)
    printer.safe_print(f"✅ Updated configuration at {conf._LOCAL_TECTON_CONFIG_FILE}")


@click.command(requires_auth=False, cls=TectonCommand)
def logout():
    """Log out of current user session. This is a no-op if there is no logged in session."""
    conf.delete_okta_tokens()
    printer.safe_print("✅ Logged user out of session. Use `tecton login` to re-authenticate.")


@click.command(cls=TectonCommand)
def get_caller_identity():
    """
    Show the current User or API Key used to authenticate with Tecton.
    """
    _get_caller_identity_impl()


def _get_caller_identity_impl():
    try:
        profile = credentials.get_caller_identity()
    except Exception as e:
        print(e)
        sys.exit(1)

    if profile and isinstance(profile, okta.UserProfile):
        key_map = {"id": "ID", "email": "Email", "name": "Name"}
        cli_utils.pprint_attr_obj(key_map, profile, colwidth=16)
    else:
        service_account = {
            "Service Account ID": profile.id,
            "Secret Key": profile.obscured_key,
            "Name": profile.name,
            "Description": profile.description,
            "Created by": profile.created_by,
        }
        cli_utils.pprint_dict(service_account, colwidth=19)
