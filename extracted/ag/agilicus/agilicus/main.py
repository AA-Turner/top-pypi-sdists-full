from agilicus.output.json import output_json, output_json_to_file, convert_to_json
from agilicus.output.table import output_entry
from agilicus.output.table import make_columns
from agilicus.output.table import format_table
from colorama import Fore
import configparser
import json
import requests
import sys
from datetime import date, datetime
from urllib.parse import urlparse
from click_shell import shell
from appdirs import user_data_dir

import click
import click_extension
import os
from prettytable import PrettyTable, TableStyle
from colorama import init
from agilicus.agilicus_api import ApiException
from . import (
    apps,
    audits,
    audit_destinations,
    challenges,
    context,
    credentials,
    custom_types,
    catalogues,
    csv_rules,
    demo,
    desktops,
    env_config,
    file_shares,
    files,
    gateway,
    input_helpers,
    issuers,
    logs,
    metrics,
    orgs,
    permissions,
    regions,
    scopes,
    tokens,
    admin,
    users,
    whoami,
    service_token,
    connectors,
    resources,
    garbage_collection,
    csr,
    certificate,
    forwarders,
    billing,
    launchers,
    lookups,
    ssh,
    transfers,
    feature_tags,
)

from .messages import messages, messages_main
from . import databases

from .input_helpers import (
    SubObjectInt,
    SubObjectString,
    pop_item_if_none,
    get_org_from_input_or_ctx,
    get_user_id_from_input_or_ctx,
)

from .output.console import output_formatted

from .trusted_certs import trusted_certs_main
from .hosts import hosts_main
from .labels import labels_main
from .rules import rules_main
from .products import products_main
from .features import features_main
from .policy import policy_main
from .features.features import format_features
from .credentials_commands import credentials_main
from .files_pkg import files_main
from .policy_config import policy_config_main
from .licensing import licensing_main
from .licensing.licenses import add_license_to_billing_sub

from .version import __version__

search_direction_values = ["forwards", "backwards"]
sort_order_values = ["ascending", "descending"]


class Config:
    """The config in this example only holds aliases."""

    def __init__(self):
        self.path = os.getcwd()
        self.aliases = {}

    def add_alias(self, alias, cmd):
        self.aliases.update({alias: cmd})

    def read_config(self, filename):
        parser = configparser.RawConfigParser()
        parser.read([filename])
        try:
            self.aliases.update(parser.items("aliases"))
        except configparser.NoSectionError:
            pass

    def write_config(self, filename):
        parser = configparser.RawConfigParser()
        parser.add_section("aliases")
        for key, value in self.aliases.items():
            parser.set("aliases", key, value)
        with open(filename, "wb") as file:
            parser.write(file)


pass_config = click.make_pass_decorator(Config, ensure=True)


class AliasedGroup(click.Group):
    """This subclass of a group supports looking up aliases in a config
    file and with a bit of magic.
    """

    def get_command(self, ctx, cmd_name):
        # Step one: bulitin commands as normal
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv

        # Step two: find the config object and ensure it's there.  This
        # will create the config object is missing.
        cfg = ctx.ensure_object(Config)

        # Step three: look up an explicit command alias in the config
        if cmd_name in cfg.aliases:
            actual_cmd = cfg.aliases[cmd_name]
            return click.Group.get_command(self, ctx, actual_cmd)
        return None

    def resolve_command(self, ctx, args):
        # always return the command's name, not the alias
        _, cmd, args = super().resolve_command(ctx, args)
        return cmd.name, cmd, args


def read_config(ctx, param, value):
    """Callback that is used whenever --config is passed.  We use this to
    always load the correct config.  This means that the config is loaded
    even if the group itself never executes so our aliases stay always
    available.
    """
    cfg = ctx.ensure_object(Config)
    if value is None:
        value = os.path.join(os.path.dirname(__file__), "aliases.ini")
    cfg.read_config(value)
    return value


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def prompt(ctx):
    issuer_host = urlparse(context.get_issuer(ctx)).netloc
    org = context.get_org(ctx)

    if not org:
        prefix = "auth."
        prompt = issuer_host
        if prompt.startswith(prefix):
            prompt = prompt[len(prefix) :]  # noqa
    else:
        prompt = org.get("subdomain")

    if context.get_value(ctx, "NO_PROMPT_COLOUR"):
        return f"{prompt}$ "
    return f"{Fore.BLUE}{prompt}$ {Fore.RESET}"


def connector_completion(ctx, args, incomplete):
    _connectors = connectors.query(ctx)
    results = []
    for _connector in _connectors:
        if incomplete in _connector["spec"]["name"]:
            results.append(_connector["spec"]["name"])
    return results


def app_completion(ctx, args, incomplete):
    _apps = apps.query(ctx)
    results = []
    for _app in _apps:
        if incomplete in _app["name"]:
            results.append(_app["name"])
    return results


def env_completion(ctx, args, incomplete):
    _envs = apps.env_query(ctx, None, args.pop())
    results = []
    for _env in _envs:
        if incomplete in _env["name"]:
            results.append(_env["name"])
    return results


def user_completion(ctx, args, incomplete):
    _users = users.query(ctx)["users"]
    results = []
    for _user in _users:
        results.append(str(_user["email"]))
    return results


def sub_org_completion(ctx, args, incomplete):
    suborgs = orgs.query_suborgs(ctx)
    results = []
    for suborg in suborgs:
        if incomplete in suborg["organisation"]:
            results.append(suborg["organisation"])
    return results


def get_user_id_from_email(ctx, email, org_id=None, type=users.USER_TYPES):
    _users = users.query(ctx, email=email, org_id=org_id, type=type).users
    if len(_users) == 1:
        return _users[0]
    return {}


def get_user_from_email_or_id(ctx, user_id_or_email=None, org_id=None, **kwargs):
    """If an email address, tries to map that to a user id. If that fails,
    assumes the input is a user id
    """
    to_check = input_helpers.get_user_id_from_input_or_ctx(ctx, user_id=user_id_or_email)
    _user = None
    if "@" in to_check:
        _user = get_user_id_from_email(ctx, email=to_check, org_id=org_id)
    if not _user:
        _user = users.get_user(ctx, to_check, org_id=org_id)

    return _user


def user_id_or_id_from_email(ctx, user_id_or_email=None, org_id=None, **kwargs):
    _user = get_user_from_email_or_id(ctx, user_id_or_email, org_id)
    if not _user:
        return None

    return _user["id"]


def get_org_id_by_name_or_use_given(org_by_name, org_id=None, org_name=None):
    if not org_id and org_name:
        if org_name in org_by_name:
            org_id = org_by_name[org_name]["id"]
        else:
            raise Exception("No such organisation found: {}".format(org_name))

    return org_id


def get_connector_id_from_id_or_name(ctx, connector_id_or_name, org_id=None, **kwargs):
    if len(connector_id_or_name) == 22:
        return connector_id_or_name
    result = connectors.query(ctx, name=connector_id_or_name)
    if len(result) == 1:
        return result[0]["metadata"]["id"]
    return None


def get_org_id(ctx, org_name=None, org_id=None):
    _, org_by_name = orgs.get_org_by_dictionary(ctx, org_id)
    return get_org_id_by_name_or_use_given(org_by_name, org_id=org_id, org_name=org_name)


# @click.group(cls=AliasedGroup)
@shell(prompt=prompt)
@click.option("--token", default=None)
@click.option(
    "--authentication-document", type=click_extension.JSONFile("r"), default=None
)
@click.option("--api", default=context.API_DEFAULT)
@click.option("--cacert", default=context.CACERT_DEFAULT)
@click.option("--client-id", default=context.CLIENT_ID_DEFAULT)
@click.option("--issuer", default=context.ISSUER_DEFAULT)
@click.option(
    "--auth-local-webserver/--noauth-local-webserver",
    "--auth_local_webserver/--noauth_local_webserver",
    default=True,
)
@click.option("--org-id", default=context.ORG_ID_DEFAULT)
@click.option("--header", default=context.HEADER_DEFAULT, type=bool)
@click.option("--scope", default=scopes.get_default_scopes(), multiple=True)
@click.option("--multiorg-scope", is_flag=True)
@click.option("--admin", is_flag=True)
@click.option("--refresh", is_flag=True)
@click.option("--output-format", default="console", type=str)
@click.option("--output-headers", default=None, is_flag=True)
@click.option("--no-prompt-colour", is_flag=True, default=None)
@click.option(
    "--config",
    type=click.Path(exists=True, dir_okay=False),
    callback=read_config,
    expose_value=False,
    help="The config file to use instead of the default.",
)
@click.option("--org-from-token-fallback", default=True)
@click.pass_context
def cli(
    ctx,
    token,
    api,
    cacert,
    client_id,
    issuer,
    auth_local_webserver,
    org_id,
    header,
    scope,
    multiorg_scope,
    admin,
    refresh,
    authentication_document,
    output_format,
    output_headers,
    no_prompt_colour,
    org_from_token_fallback,
):
    init(autoreset=True)
    ctx.ensure_object(dict)
    ctx.obj["TOKEN"] = token
    ctx.obj["API"] = api
    ctx.obj["CACERT"] = cacert
    ctx.obj["CLIENT_ID"] = client_id
    ctx.obj["ISSUER"] = issuer
    ctx.obj["AUTH_LOCAL_WEBSERVER"] = auth_local_webserver
    ctx.obj["ORG_ID"] = org_id
    ctx.obj["HEADER"] = header
    ctx.obj["NO_PROMPT_COLOUR"] = no_prompt_colour
    ctx.obj[context.ORG_FROM_TOKEN_FALLBACK] = org_from_token_fallback

    scope_list = list(scope)

    if admin:
        # Extend the provided scopes (either default or chosen by user) with the admin
        # scopes
        ctx.obj["CLIENT_ID"] = context.CLIENT_ID_ADMIN_DEFAULT
        scope_list.extend(scopes.get_admin_scopes())

    if multiorg_scope:
        scope_list.append("urn:agilicus:token_payload:multiorg:true")

    ctx.obj["SCOPES"] = scope_list
    ctx.obj["ADMIN_MODE"] = admin
    ctx.obj["output_format"] = output_format
    ctx.obj["output_headers"] = output_headers
    ctx.obj["CONFIG"] = context.get_api_config()
    ctx.obj["BILLING_API_KEY"] = os.getenv("BILLING_API_KEY", None)

    if authentication_document:
        context.save_refreshable_token(
            ctx, tokens.RefreshableServiceToken(ctx, authentication_document, scope_list)
        )
    else:
        context.save_refreshable_token(ctx, tokens.RefreshableAccessToken())

    if not org_id:
        # this is optional, used primarily for the prompt
        try:
            if not token:
                token = context.get_token(ctx)
                org_id = context.get_org_id(ctx, token)
        except Exception as exc:
            print("Exception in get_token: ", exc)
            pass

    if org_id:
        org = orgs.get(ctx, org_id)
        ctx.obj["ORGANISATION"] = org
    context.save(ctx)
    return None


@cli.command(name="list-orphaned-resources")
@click.option("--applications/--exclude-applications", default=True)
@click.option("--issuers/--exclude-issuers", default=True)
@click.option("--users/--exclude-users", default=True)
@click.option("--resources/--exclude-resources", default=True)
@click.option("--connectors/--exclude-connectors", default=True)
@click.option("--mark-connectors-deleted", default=False)
@click.option("--org-id", default=None, help="Show garbage for a specific org-id")
@click.option("--dry-run", is_flag=True, default=False)
@click.option(
    "--only-org-enabled",
    default=False,
    is_flag=True,
    help="find only resources that are not attached to an active org",
)
@click.pass_context
def list_orphaned_resources(ctx, **kwargs):
    result_table = garbage_collection.get_all_orphaned_resources(ctx, **kwargs)
    garbage_collection.output_orphaned_resources(ctx, result_table)


@cli.command(name="use")
@click.pass_context
@click.argument("organisation", default=None)
@click.option("--org-id", default="")
def use(ctx, org_id, organisation):
    org_list = []
    for org in get_saved_orgs():
        if not org.get("organisation"):
            continue
        if organisation.lower() in org.get("organisation").lower():
            org_list.append(org)
        elif organisation == org.get("id"):
            # using a specific org.
            org_list.append(org)
            break

    if not org_list:
        for org in get_saved_orgs():
            if not org.get("subdomain"):
                continue
            if organisation.lower() in org.get("subdomain").lower():
                org_list.append(org)

    if not org_list:
        print(f"no organisation named {organisation} found")
        return

    if len(org_list) > 1:
        print("multiple orgs found:")
        for org in org_list:
            print(
                f"Organisation: {org.get('organisation')} "
                f"ID: {org.get('id')} "
                f"Subdomain: {org.get('subdomain')}"
            )
        return

    switch_org(org_list[0])


def get_saved_orgs():
    orgs_file = get_saved_orgs_path()
    if not os.path.isfile(orgs_file):
        return []
    with open(orgs_file, "r") as f:
        return json.load(f)


def get_data_dir():
    data_dir = user_data_dir("agilicus-cli", "agilicus")
    if not os.path.isdir(data_dir):
        os.makedirs(data_dir, exist_ok=True)
    return data_dir


def get_saved_orgs_path():
    return os.path.join(get_data_dir(), "saved-orgs")


@cli.command()
@click.option("--org-id", default="")
@click.pass_context
def save_orgs(ctx, org_id=None):
    org_list = orgs.query(ctx, org_id=org_id, enabled=True)
    org_list = [
        {
            "id": org.get("id"),
            "subdomain": org.get("subdomain"),
            "organisation": org.get("organisation"),
        }
        for org in org_list
    ]
    with open(get_saved_orgs_path(), "w") as f:
        json.dump(org_list, f, default=str)


def output_tokens_list(ctx, tokens_list):
    if ctx.obj["output_format"] == "json":
        return output_json(ctx, tokens_list)
    table = PrettyTable(
        [
            "jti",
            "roles",
            "iat",
            "exp",
            "aud",
            "user",
            "session",
            "revoked",
            "scopes",
            "updated",
            "masquerading",
        ]
    )
    for token in tokens_list:
        table.add_row(
            [
                token["jti"],
                json.dumps(token["roles"], indent=2),
                token["iat"],
                token["exp"],
                json.dumps(token["aud"], indent=2),
                token["sub"],
                token["session"],
                token["revoked"],
                json.dumps(token["scopes"], indent=2),
                token["updated"],
                token.get("masquerading", "---"),
            ]
        )
    table.align = "l"
    print(table)


@cli.command(name="delete-credentials")
@click.pass_context
def _delete_credentials(ctx, **kwargs):
    credentials.delete_credentials_with_ctx(ctx)


@cli.command(name="list-tokens")
@click.option("--limit", default=None)
@click.option("--expired-from", default=None)
@click.option("--expired-to", default=None)
@click.option("--issued-from", default=None)
@click.option("--issued-to", default=None)
@click.option("--org-id", default=None)
@click.option("--jti", default=None)
@click.option("--sub", default=None)
@click.option("--session", default=None)
@click.pass_context
def list_tokens(ctx, org_id, **kwargs):
    output_tokens_list(
        ctx, json.loads(tokens.query_tokens(ctx, org_id=org_id, **kwargs))["tokens"]
    )


def output_gw_audit_list(ctx, audit_list):
    if ctx.obj["output_format"] == "json":
        return output_json(ctx, audit_list)
    table = PrettyTable(["time", "authority", "token_id"])
    for entry in audit_list:
        table.add_row([entry["time"], entry["authority"], entry["token_id"]])
    table.align = "l"
    print(table)


@cli.command(name="gateway-audit")
@click.option("--limit", default=None)
@click.option("--token-id", default=None)
def gateway_audit(ctx, **kwargs):
    output_gw_audit_list(ctx, json.loads(gateway.query_audit(**kwargs)))


def format_signup_as_text(records):
    table = PrettyTable(
        [
            "time",
            "first_name",
            "last_name",
            "user_id",
            "email",
            "ip",
            "org_name",
            "org_id",
            "country",
            "city",
        ]
    )
    for record in records:
        table.add_row(
            [
                record["time"].strftime("%Y-%m-%d %H:%M:%S %z"),
                record["first_name"],
                record["last_name"],
                record["user_id"],
                record["email"],
                record["ip"],
                record["org_name"],
                record["org_id"],
                record["country"],
                record["city"],
            ]
        )
    table.align = "l"
    return table


@cli.command(name="list-signups")
@click.option("--org-id", default="WWcWgenXrv9KUdfH9ipaYF")
@click.option("--dt-from", default=None)
@click.option("--dt-to", default=None)
@click.option("--user-id", default=None)
@click.option("--action", default="CREATE")
@click.option("--target-id", default=None)
@click.option("--token-id", default=None)
@click.option("--api-name", default=None)
@click.option("--target-resource-type", default="orgs")
@click.option("--output-format", type=click.Choice(["json"]), default=None)
@click.pass_context
def list_signups(ctx, **kwargs):
    output_format = kwargs.pop("output_format", "")
    records = audits.query(ctx, **kwargs)
    org_id = kwargs.pop("org_id", "")
    _users = {}
    _orgs = {}
    _ips = {}
    _output = []
    for record in records:
        if record.source_ip not in _ips:
            try:
                _ips[record.source_ip] = {}
                resp = requests.get(
                    f"https://api.agilicus.com/v1/ip2geo?ip={record.source_ip}"
                )
                if resp.status_code == 200:
                    _ips[record.source_ip] = json.loads(resp.content.decode("utf-8"))
            except Exception:
                pass
            _ips[record.source_ip].setdefault("country", "Unknown")
            _ips[record.source_ip].setdefault("city", "Unknown")
        if record.user_id not in _users:
            _user = users.get_user(ctx, record.user_id, org_id=org_id)
            _users[record.user_id] = _user.to_dict()
        if record.target_id not in _orgs:
            try:
                _org = None
                _org = orgs.get_raw(ctx, record.target_id).to_dict()
            except ApiException as exc:
                if exc.status != 404:
                    raise
            finally:
                if _org is None:
                    _org = {"organisation": "not found"}
                _orgs[record.target_id] = _org
        output_record = {
            "time": record.time,
            "first_name": _users[record.user_id]["first_name"],
            "last_name": _users[record.user_id].get("last_name"),
            "user_id": record.user_id,
            "email": _users[record.user_id]["email"],
            "ip": record.source_ip,
            "org_name": _orgs[record.target_id]["organisation"],
            "org_id": record.target_id,
            "country": _ips[record.source_ip]["country"],
            "city": _ips[record.source_ip]["city"],
        }
        _output.append(output_record)
    if output_format == "json":
        print(json.dumps(_output, default=str))
    else:
        print(format_signup_as_text(_output))


@cli.command(name="list-audit-records")
@click.option("--limit", type=int, default=50)
@click.option("--org-id", default=None)
@click.option("--dt-from", default=None)
@click.option("--dt-to", default=None)
@click.option("--user-id", default=None)
@click.option("--action", default=None)
@click.option("--target-id", default=None)
@click.option("--token-id", default=None)
@click.option("--api-name", default=None)
@click.option("--target-resource-type", default=None)
@click.option("--output-format", type=click.Choice(["json"]), default=None)
@click.option("--attribute-type", default=None)
@click.option("--attribute-id", default=None)
@click.option("--attribute-org-id", default=None)
@click.option("--show-column", multiple=True, default=None)
@click.pass_context
def list_audit_records(ctx, show_column, **kwargs):
    output_format = kwargs.pop("output_format", "")
    records = audits.query(ctx, **kwargs)
    if output_format == "json":
        records = [record.to_dict() for record in records]
        print(json.dumps(records, default=str))
    else:
        print(
            audits.format_audit_list_as_text(
                ctx, records, show_columns=list(show_column)
            )
        )


@cli.command(name="list-auth-audit-records")
@click.option("--limit", type=int, default=None)
@click.option("--org-id", default=None)
@click.option("--dt-from", default=None)
@click.option("--dt-to", default=None)
@click.option("--user-id", default=None)
@click.option("--session-id", default=None)
@click.option("--trace-id", default=None)
@click.option("--upstream-user-id", default=None)
@click.option("--upstream-idp", default=None)
@click.option("--login-org-id", default=None)
@click.option("--source-ip", default=None)
@click.option("--client-id", default=None)
@click.option("--event", default=None)
@click.option("--stage", default=None)
@click.option("--request-id", default=None)
@click.option("--map-email", is_flag=True, default=False)
@click.pass_context
def list_auth_audit_records(ctx, **kwargs):
    records = audits.query_auth_audits(ctx, **kwargs)
    print(audits.format_auth_audit_list_as_text(ctx, records))


@cli.command(name="list-users")
@click.option("--organisation", default=None)
@click.option("--org-id", default=None)
@click.option("--email", default=None)
@click.option("--previous-email", default="")
@click.option("--limit", type=int, default=None)
@click.option(
    "--status", multiple=True, type=click.Choice(users.STATUS_OPTIONS), default=None
)
@click.option(
    "--search-direction",
    default=None,
    type=click.Choice(search_direction_values),
)
@click.option("--has-roles", type=bool, default=None)
@click.option("--has-resource-roles", type=bool, default=None)
@click.option("--prefix-email-search", default=None)
@click.option("--first-name", default=None)
@click.option("--last-name", default=None)
@click.option("--user-id", default=None)
@click.option("--search-param", multiple=True, default=None)
@click.option("--allow-partial-match", is_flag=True, default=None)
@click.option("--type", multiple=True, default=None)
@click.option("--upstream-idp-id", default=None)
@click.option("--upstream-user-id", default=None)
@click.option("--issuer", default=None)
@click.option("--has-application-permissions", default=None)
@click.option("--show-columns", type=str, default=None)
@click.option("--reset-columns", is_flag=True, default=False)
@click.option("--has-resource-or-application-roles", is_flag=True, default=None)
@click.pass_context
def list_users(ctx, organisation, org_id, show_columns, reset_columns, **kwargs):
    # get all orgs
    kwargs["search_params"] = kwargs.pop("search_param", None)

    results = users.query(ctx, org_id, **kwargs).users
    columns = make_columns(
        ctx,
        results,
        """
          - id
          - first_name
          - last_name
          - email
          - org_id
          - status
          - created
          - updated
        """,
        show=show_columns,
        clear=reset_columns,
    )
    print(format_table(ctx, results, columns))


@cli.command(name="list-user-orgs")
@click.option("--user-id", default=None)
@click.option("--org-id", default=None)
@click.option("--issuer", default=None)
@click.option("--enabled", type=bool, default=None)
@click.pass_context
def list_user_orgs(ctx, **kwargs):
    results = users.list_user_orgs(ctx, **kwargs)
    print(users.format_user_orgs(ctx, results))


@cli.command(name="show-user")
@click.argument("email_or_id", shell_complete=user_completion)
@click.option("--org-id", default=None)
@click.pass_context
def show_user(ctx, email_or_id, **kwargs):
    _user = get_user_from_email_or_id(ctx, email_or_id, **kwargs)
    output_entry(ctx, _user.to_dict())


@cli.command(name="add-user")
@click.argument("first-name")
@click.argument("last-name")
@click.argument("email")
@click.argument("org-id")
@click.option("--external-id", default=None)
@click.option("--enabled", type=bool, default=None)
@click.option("--status", type=click.Choice(users.STATUS_OPTIONS), default=None)
@click.option("--description", type=str, default=None)
@click.pass_context
def add_user(ctx, first_name, last_name, email, org_id, **kwargs):
    output_entry(
        ctx, users.add_user(ctx, first_name, last_name, email, org_id, **kwargs)
    )


@cli.command(name="update-user")
@click.argument("email_or_id", shell_complete=user_completion)
@click.option("--email", default=None)
@click.option("--org-id", default=None)
@click.option("--first-name", default=None)
@click.option("--last-name", default=None)
@click.option("--external-id", default=None)
@click.option("--auto-created", type=bool, default=None)
@click.option("--enabled", type=bool, default=None)
@click.option("--cascade", type=bool, default=None)
@click.option("--status", type=click.Choice(users.STATUS_OPTIONS), default=None)
@click.option("--description", type=str, default=None)
@click.option("--attribute", type=(str, str), multiple=True, default=None)
@click.option("--remove-attribute", type=str, multiple=True, default=None)
@click.option("--disabled-at-time", default=None)
@click.pass_context
def update_user(ctx, email_or_id, org_id=None, **kwargs):
    _user = get_user_from_email_or_id(ctx, email_or_id, org_id=org_id)
    output_entry(
        ctx, users.update_user_with_user(ctx, _user.to_dict(), **kwargs).to_dict()
    )


@cli.command(name="delete-user")
@click.argument("email", shell_complete=user_completion)
@click.option("--org-id", default=None)
@click.pass_context
def delete_user(ctx, email, org_id):
    _user = get_user_from_email_or_id(ctx, email, org_id=org_id)
    users.delete_user(ctx, _user["id"], org_id=org_id)


@cli.command(name="add-user-role")
@click.argument("email_or_id", shell_complete=user_completion)
@click.argument("application", shell_complete=app_completion)
@click.option("--role", multiple=True)
@click.option("--org-id", default=None)
@click.option("--update", default=False, is_flag=True)
@click.pass_context
def add_user_role(ctx, email_or_id, application, role, org_id, update):
    _user = get_user_from_email_or_id(ctx, email_or_id, org_id=org_id)
    roles = []
    for _role in role:
        roles.append(_role)
    users.add_user_role(
        ctx, _user["id"], application, roles, org_id=org_id, update=update
    )
    output_entry(ctx, users.get_user(ctx, _user["id"], org_id=org_id).to_dict())


@cli.command(name="list-user-roles")
@click.argument("email", shell_complete=user_completion)
@click.option("--org-id", default=None)
@click.pass_context
def list_user_role(ctx, email, org_id):
    _user = get_user_id_from_email(ctx, email, org_id)
    if _user:
        roles = json.loads(users.list_user_roles(ctx, _user["id"], org_id))
        table = PrettyTable(["application/service", "roles"])
        table.align = "l"
        for app, rolelist in roles.items():
            table.add_row([app, rolelist])
        print(table)
    else:
        print(f"lookup of {email} not found")


def output_list_orgs(ctx, orgs_list):
    if ctx.obj["output_format"] == "json":
        return output_json(ctx, orgs_list)
    table = PrettyTable(
        ["id", "Organisation", "Created", "State", "Contact", "Issuer", "Subdomain"]
    )
    for entry in orgs_list:
        subdomain = entry.get("subdomain", None)
        try:
            created = entry["created"].isoformat()[0:19]
        except Exception:
            created = entry["created"]
        if "subdomain" not in entry:
            subdomain = None
        table.add_row(
            [
                entry["id"],
                entry["organisation"],
                created,
                entry.get("admin_state"),
                entry.get("contact_email"),
                entry.get("issuer"),
                subdomain,
            ]
        )
    table.align = "l"
    print(table)


def output_list_groups(ctx, groups_list, hide_members):
    if ctx.obj["output_format"] == "json":
        return output_json(ctx, groups_list)
    table = PrettyTable(["id", "Email", "members"])
    for entry in groups_list:
        _members = []
        if not hide_members:
            for _member in entry["members"]:
                _members.append(_member["email"])
        table.add_row(
            [
                entry["id"],
                entry["email"],
                "\n".join(_members),
            ]
        )
    table.align = "l"
    print(table)


@cli.command(name="list-groups")
@click.option("--organisation", default=None)
@click.option("--org-id", default=None)
@click.option("--type", multiple=True, default=["group"])
@click.option("--limit", default=500)
@click.option("--previous-email", default=None)
@click.option("--prefix-email-search", default="")
@click.option("--hide-members", type=bool, default=None)
@click.option(
    "--search-direction",
    default="forwards",
    type=click.Choice(search_direction_values),
)
@click.option("--first-name", default=None)
@click.option("--last-name", default=None)
@click.option("--search-param", multiple=True, default=None)
@click.option("--allow-partial-match", is_flag=True, default=False)
@click.pass_context
def list_groups(ctx, organisation, org_id, type, **kwargs):
    kwargs["search_params"] = kwargs.pop("search_param", None)
    hide_members = kwargs.pop("hide_members", False)
    # get all orgs
    org_by_id, org_by_name = orgs.get_org_by_dictionary(ctx, org_id)

    org_id = get_org_id_by_name_or_use_given(
        org_by_name, org_name=organisation, org_id=org_id
    )
    users_groups = users.query_groups(ctx, org_id, type=list(type), **kwargs)
    output_list_groups(ctx, users_groups["groups"], hide_members)


@cli.command(name="list-sysgroups")
@click.option("--organisation", default=None)
@click.option("--org-id", default=None)
@click.option("--hide-members", type=bool, default=None)
@click.pass_context
def list_sysgroups(ctx, organisation, org_id, **kwargs):
    hide_members = kwargs.pop("hide_members", False)
    # get all orgs
    org_by_id, org_by_name = orgs.get_org_by_dictionary(ctx, org_id)
    org_id = get_org_id_by_name_or_use_given(
        org_by_name, org_name=organisation, org_id=org_id
    )
    users_groups = users.query_groups(ctx, org_id, type=["sysgroup"], **kwargs)
    output_list_groups(ctx, users_groups["groups"], hide_members)


@cli.command(name="add-group")
@click.argument("first-name")
@click.option("--org-id")
@click.option("--type", default="group")
@click.option("--cascade", is_flag=True, default=None)
@click.pass_context
def add_group(ctx, **kwargs):
    output_entry(ctx, users.add_group(ctx, **kwargs))


@cli.command(name="show-group")
@click.argument("group-id")
@click.option("--org-id")
@click.pass_context
def show_group(ctx, group_id, **kwargs):
    output_entry(ctx, users.get_group(ctx, group_id, **kwargs))


@cli.command(name="add-group-member")
@click.argument("group-id", default=None)
@click.option("--org-id", default=None)
@click.option("--member-org-id", default=None)
@click.option("--member", multiple=True)
@click.option("--email", multiple=True)
@click.pass_context
def add_group_member(ctx, **kwargs):
    users.add_group_member(ctx, **kwargs)


@cli.command(name="delete-group-member")
@click.argument("group-id", default=None)
@click.option("--member", multiple=True)
@click.option("--org-id", default=None)
@click.pass_context
def delete_group_member(ctx, group_id, org_id, member):
    users.delete_group_member(ctx, group_id, member, org_id)


@cli.command(name="delete-group")
@click.argument("group-id", default=None)
@click.pass_context
def delete_group(ctx, group_id):
    users.delete_user(ctx, group_id, type="group")


@cli.command(name="list-useful-orgs")
@click.pass_context
def list_useful_orgs_(ctx, **kwargs):
    top_orgs = [
        "5QZ9wCU3xwHs4XcKAcGghL",
        "vLQPrCAy2v8UKWSmYvgGee",
        "XpRyFkb2ndrohCkYLUZpz8",
        "WWcWgenXrv9KUdfH9ipaYF",
    ]
    kwargs["enabled"] = True
    kwargs["org_id"] = ""
    orgs_list = orgs.query(ctx, **kwargs)
    result = []
    for org in orgs_list:
        if org["id"] not in top_orgs:
            org["organisation"] = f" - {org['organisation']}"
        result.append(org)
    output_list_orgs(ctx, result)


@cli.command(name="list-orgs")
@click.option("--org-id", default=None)
@click.option("--issuer", default=None)
@click.option("--name", default=None)
@click.option("--billing_account_id", default=None)
@click.option("--shard", default=None)
@click.option("--cluster", default=None)
@click.option("--subdomain", default=None)
@click.option(
    "--created-since", default=None, type=input_helpers.HumanReadableDateType()
)
@click.option("--updated-since", default=None, type=click.DateTime())
@click.option("--list-children", default=True, type=bool)
@click.option("--enabled", default=None, type=bool)
@click.option("--page-at-id", default="")
@click.option("--suborg-updated", default=False, type=bool)
@click.option("--get-system-options", default=False)
@click.option("--point-of-presence-name-list", multiple=True)
@click.option(
    "--page-size",
    type=int,
    default=100,
    help="number of items in each pagination, useful ONLY when page-at-id is set",
)
@click.option("--limit", type=int, default=None)
@click.pass_context
def list_orgs(ctx, **kwargs):
    output_list_orgs(ctx, orgs.query(ctx, **kwargs))


@cli.command(name="list-orgs-without-billing")
@click.option("--enabled", type=bool, default=True)
@click.pass_context
def list_orgs_without_billing(ctx, **kwargs):
    print(orgs.query_no_billing(ctx, **kwargs))


@cli.command(name="list-sub-orgs")
@click.option("--org-id", default=None)
@click.pass_context
def list_sub_orgs(ctx, **kwargs):
    output_list_orgs(ctx, orgs.query_suborgs(ctx, **kwargs))


@cli.command(name="reconcile-sub-org-issuer")
@click.option("--org-id", default=None)
@click.option("--sub-org-id", required=True)
@click.option("--own-issuer", type=bool, required=True)
@click.pass_context
def reconcile_sub_org_issuer(ctx, **kwargs):
    output_entry(ctx, orgs.reconcile_sub_org_issuer(ctx, **kwargs).to_dict())


@cli.command(name="show-org")
@click.argument("org-id", default=None, required=False)
@click.option("--get-system-options", type=bool, default=None)
@click.pass_context
def show_org(ctx, org_id, **kwargs):
    output_entry(ctx, orgs.get(ctx, org_id, **kwargs))


@cli.command(name="show-customer")
@click.argument("org-id", default=None, required=False)
@click.pass_context
def show_customer(ctx, org_id, **kwargs):
    org = orgs.get_raw(ctx, org_id, **kwargs)
    account = billing.get_billing_account(
        ctx, billing_account_id=org.billing_account_id, get_customer_data=True
    )
    output_entry(ctx, account.to_dict()["status"].get("customer"))


@cli.command(name="show-org-billing-account")
@click.option("--org-id", default=None)
@click.pass_context
def show_org_billing_account(ctx, org_id, **kwargs):
    output_entry(ctx, orgs.get_org_billing_account(ctx, org_id, **kwargs).to_dict())


@cli.command(name="create-billing-account-portal-link")
@click.option("--org-id", default=None)
@click.option("--return-uri", required=True)
@click.pass_context
def create_portal_link(ctx, **kwargs):
    output_entry(ctx, orgs.create_portal_link(ctx, **kwargs).to_dict())


@cli.command(name="update-org")
@click.argument("org_id", default=None)
@click.option("--organisation", default=None)
@click.option("--auto-create", type=bool, default=None)
@click.option("--issuer", default=None)
@click.option("--issuer-id", default=None)
@click.option("--contact-id", default=None)
@click.option("--subdomain", default=None)
@click.option("--external-id", default=None)
@click.option("--point-of-presence-id", default=None)
@click.option(
    "--admin-state",
    type=click.Choice(["active", "suspended", "disabled", "deleted"]),
    default=None,
)
@click.option("--trust-on-first-use-duration", type=int, default=None)
@click.option("--name-slug", default=None)
@click.option("--cluster", default=None)
@click.option("--shard", default=None)
@click.option("--disable-user-requests", type=bool, default=None)
@click.option("--ruleset-bundle-id", default=None)
@click.option("--region-id", default=None)
@click.pass_context
def update_org(
    ctx,
    org_id,
    auto_create,
    issuer,
    issuer_id,
    contact_id,
    subdomain,
    external_id,
    **kwargs,
):
    orgs.update(
        ctx,
        org_id,
        auto_create=auto_create,
        issuer=issuer,
        issuer_id=issuer_id,
        contact_id=contact_id,
        subdomain=subdomain,
        external_id=external_id,
        **kwargs,
    )
    output_entry(ctx, orgs.get(ctx, org_id))


@cli.command(name="reconcile-org-default-policy")
@click.option("--org-id", default=None)
@click.option("--all-orgs", is_flag=True, default=False)
@click.option("--limit", type=int, default=100)
@click.pass_context
def reconcile_org_default_policy(
    ctx,
    **kwargs,
):
    results = orgs.reconcile_org_policy(
        ctx,
        **kwargs,
    )
    print(orgs.format_reconcile_org_policy_results(ctx, results))


@cli.command(name="set-feature")
@click.argument("feature")
@click.argument("enabled", type=bool)
@click.option("--org-id", default=None)
@click.option("--setting", default="")
@click.pass_context
def set_feature(ctx, feature, enabled, **kwargs):
    result = orgs.set_feature(ctx, feature=feature, enabled=enabled, **kwargs)
    output_entry(ctx, result)


@cli.command(name="remove-feature")
@click.argument("feature")
@click.option("--org-id", default=None)
@click.pass_context
def remove_feature(ctx, feature, **kwargs):
    result = orgs.remove_feature(ctx, feature=feature, **kwargs)
    output_entry(ctx, result)


@cli.command(name="update-system-options")
@click.argument("org-id")
@click.option("--allowed-domains", multiple=True)
@click.option(
    "--license-constraints",
    type=click_extension.JSONFile("r"),
    help="a constraints file; - for stdin",
)
@click.option(
    "--constraint-vars",
    type=click_extension.JSONFile("r"),
    help="a constraint variables file; - for stdin",
)
@click.option(
    "--replace-constraints",
    type=bool,
    is_flag=True,
)
@click.option(
    "--replace-vars",
    type=bool,
    is_flag=True,
)
@click.pass_context
def update_system_options(ctx, org_id, **kwargs):
    result = orgs.replace_system_options(ctx, org_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="get-system-options")
@click.argument("org-id")
@click.pass_context
def get_system_options(ctx, org_id):
    result = orgs.get_system_options(ctx, org_id)
    output_entry(ctx, result.to_dict())


@cli.command(name="add-org")
@click.argument("organisation")
@click.argument("subdomain")
@click.option("--issuer", default=None)
@click.option("--issuer-id", default=None)
@click.option("--auto-create", type=bool, default=True)
@click.option("--contact-id", default=None)
@click.option("--subdomain", default=None)
@click.option("--parent-id", default=None)
@click.option(
    "--admin-state",
    type=click.Choice(["active", "suspended", "disabled", "deleted"]),
    default=None,
)
@click.option("--cluster", default=None)
@click.option("--region-id", default=None)
@click.option("--billing-account-id", default=None)
@click.option("--product-label-override", default=None)
@click.option("--shard", default=None)
@click.pass_context
def add_org(ctx, **kwargs):
    output_entry(
        ctx,
        orgs.add(
            ctx,
            **kwargs,
        ),
    )


@cli.command(name="fixup-org")
@click.argument("org-id")
@click.option("--product-label-override", default=None)
@click.pass_context
def fixup_org(ctx, **kwargs):
    output_entry(
        ctx,
        orgs.fixup(
            ctx,
            **kwargs,
        ),
    )


@cli.command(name="add-sub-org")
@click.argument("organisation")
@click.option("--auto-create", type=bool, default=True)
@click.option("--contact-id", default=None)
@click.option("--subdomain", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def add_sub_org(ctx, organisation, contact_id, auto_create, subdomain, org_id, **kwargs):
    output_entry(
        ctx,
        orgs.add_suborg(
            ctx, organisation, contact_id, auto_create, subdomain, org_id, **kwargs
        ),
    )


@cli.command(name="delete-sub-org")
@click.argument("org-id")
@click.pass_context
def delete_sub_org(ctx, org_id):
    orgs.delete_suborg(ctx, org_id)


@cli.command(name="delete-org")
@click.argument("org-id", default=None)
@click.pass_context
def delete_org(ctx, org_id, **kwargs):
    orgs.delete(ctx, org_id, **kwargs)


@cli.command(name="list-domains")
@click.option("--org-id", default=None)
@click.pass_context
def list_domains(ctx, **kwargs):
    table = PrettyTable(["domain"])
    domains = orgs.list_domains(ctx, **kwargs)
    for domain in domains:
        table.add_row([domain])
    table.align = "l"
    print(table)


def output_list_apps(ctx, orgs_by_id, apps_list):
    if ctx.obj["output_format"] == "json":
        apps_list = [x.to_dict() for x in apps_list]
        return output_json(ctx, apps_list)
    table = PrettyTable(["id", "Application", "Organisation"])
    for entry in apps_list:

        org_name = "none"
        org_id = getattr(entry, "org_id", None)
        if org_id and org_id in orgs_by_id:
            org_name = orgs_by_id[org_id]["organisation"]

        table.add_row([entry.id, entry.name, org_name])
    table.align = "l"
    print(table)


@cli.command(name="list-applications")
@click.option("--organisation", default=None)
@click.option("--org-id", default=None)
@click.option("--resource-id", default=None)
@click.option("--updated_since", default=None)
@click.option("--maintained/--no-maintained", default=None, is_flag=True)
@click.option("--owned/--no-owned", default=None, is_flag=True)
@click.option("--assigned/--no-assigned", default=None, is_flag=True)
@click.option(
    "--include-migrated-environments/--exclude-migrated-environments",
    default=None,
    is_flag=True,
)
@click.pass_context
def list_applications(ctx, organisation, org_id, **kwargs):
    # get all orgs
    org_by_id, org_by_name = orgs.get_org_by_dictionary(ctx, org_id)
    org_id = get_org_id_by_name_or_use_given(
        org_by_name, org_name=organisation, org_id=org_id
    )

    output_list_apps(ctx, org_by_id, apps.query(ctx, org_id, **kwargs))


@cli.command(name="list-environments")
@click.argument("application", shell_complete=app_completion)
@click.option("--organisation", default=None)
@click.option("--org-id", default=None)
@click.option("--filter", default=None)
@click.pass_context
def list_environments(ctx, organisation, org_id, filter, **kwargs):
    org_by_id, org_by_name = orgs.get_org_by_dictionary(ctx, org_id)
    if not org_id and organisation:
        if organisation in org_by_name:
            org_id = org_by_name[organisation]["id"]
        else:
            Exception("No such organisation found: {}".format(organisation))
    data = []
    table = PrettyTable(
        ["Name", "Assignments", "Services"],
        header=context.header(ctx),
        border=context.header(ctx),
    )
    for env in apps.env_query(ctx, org_id, **kwargs):
        _services = []
        app_services = env.get("application_services", [])
        if app_services is not None:
            for service in app_services:
                _services.append(service["name"])
        data.append(env)
        table.add_row([env["name"], env.get("assignments", None), _services])
    table.align = "l"
    if ctx.obj["output_format"] == "json":
        return output_json(ctx, data)
    if filter:
        print(table.get_string(fields=filter.split(",")))
    else:
        print(table)


@cli.command(name="list-application-services")
@click.option("--org-id", default=None)
@click.option("--updated-since", default=None, type=click.DateTime())
@click.option(
    "--protocol-type", default=None, type=click.Choice(["ip", "fileshare", "ssh"])
)
@click.option(
    "--protocol-type-list", multiple=True, type=click.Choice(["ip", "fileshare", "ssh"])
)
@click.option("--hostname", default=None)
@click.option("--port", type=int, default=None)
@click.option("--name", default=None)
@click.option("--hostname_or_service_name", default=None)
@click.option("--external_hostname_or_service", default=None)
@click.option("--show-status", is_flag=True, default=False)
@click.pass_context
def list_application_services(ctx, protocol_type_list, **kwargs):
    services = apps.get_application_services(
        ctx, protocol_type_list=list(protocol_type_list), **kwargs
    )
    print(apps.format_application_services(ctx, services))


@cli.command(name="add-application-service")
@click.argument("name", default=None)
@click.argument("hostname", default=None)
@click.argument("port", type=int, default=None)
@click.option("--org-id", default=None)
@click.option("--ipv4-addresses", default=None)
@click.option("--name-resolution", default=None)
@click.option("--protocol", default=None)
@click.option("--tls-enabled/--tls-disabled", is_flag=True, default=None)
@click.option("--tls-verify/--tls-no-verify", is_flag=True, default=None)
@click.option("--connector-id", default=None)
@click.option("--connector-instance-id", default=None)
@click.option("--learning-mode", type=bool, default=None)
@click.option("--learning-mode-expiry", type=click.DateTime(), default=None)
@click.option("--diagnostic-mode", type=bool, default=None)
@click.pass_context
def add_application_service(ctx, name, hostname, port, org_id, **kwargs):
    output_entry(
        ctx,
        apps.add_application_service(
            ctx, name, hostname, port, org_id=org_id, **kwargs
        ).to_dict(),
    )


@cli.command(name="set-http-config")
@click.argument("service-id", default=None)
@click.option("--set-token-cookie", is_flag=True)
@click.option("--rewrite-hostname", is_flag=True)
@click.option("--rewrite-hostname-with-port", is_flag=True)
@click.option("--rewrite-hostname-override", default="")
@click.option("--org-id", default=None)
@click.pass_context
def set_http_config(ctx, *args, **kwargs):
    output_entry(
        ctx,
        apps.set_http_config(
            ctx,
            *args,
            **kwargs,
        ).to_dict(),
    )


@cli.command(name="add-js-injection")
@click.argument("service-id", default=None)
@click.option("--inject-script", type=click.Path(exists=True))
@click.option("--inject-preset", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def add_js_injection(ctx, *args, **kwargs):
    output_entry(
        ctx,
        apps.add_js_injection(
            ctx,
            *args,
            **kwargs,
        ).to_dict(),
    )


@cli.command(name="delete-js-injection")
@click.argument("service-id", default=None)
@click.argument("index", type=int)
@click.option("--org-id", default=None)
@click.pass_context
def delete_js_injection(ctx, *args, **kwargs):
    output_entry(
        ctx,
        apps.delete_js_injection(
            ctx,
            *args,
            **kwargs,
        ).to_dict(),
    )


@cli.command(name="update-application-service")
@click.argument("id", default=None)
@click.option("--name", default=None)
@click.option("--hostname", default=None)
@click.option("--port", type=int, default=None)
@click.option("--org-id", default=None)
@click.option("--ipv4-addresses", default=None)
@click.option("--name-resolution", default=None)
@click.option(
    "--service-type",
    type=click.Choice(["vpn", "agent", "internet", "ipsec"]),
    default=None,
)
@click.option("--protocol", default=None)
@click.option("--connector-id", default=None)
@click.option("--connector-instance-id", default=None)
@click.option("--tls-enabled/--tls-disabled", is_flag=True, default=None)
@click.option("--tls-verify/--tls-no-verify", is_flag=True, default=None)
@click.option("--disable-http2", type=bool, default=None)
@click.option("--expose-as-hostname", type=bool, default=None)
@click.option("--learning-mode", type=bool, default=None)
@click.option("--learning-mode-expiry", type=click.DateTime(), default=None)
@click.option("--diagnostic-mode", type=bool, default=None)
@click.option(
    "--port-range", type=str, default=None, help="comma seperated list of port ranges"
)
@click.option("--source-port-override", default=None)
@click.option("--source-address-override", default=None)
@click.option("--dynamic-source-port-override", type=bool, default=None)
@click.option("--set-token-cookie", type=bool, default=None)
@click.pass_context
def update_application_service(ctx, id, **kwargs):
    output_entry(ctx, apps.update_application_service(ctx, id, **kwargs))


@cli.command(name="create-application-service-token")
@click.argument("id", default=None)
# @click.option("--duration-seconds", type=int, default=3600)
@click.option("--org_id", type=int, default=None)
@click.pass_context
def create_application_service_token(ctx, id, **kwargs):
    output_entry(ctx, apps.create_application_service_token(ctx, id, **kwargs).to_dict())


@cli.command(name="add-application-service-assignment")
@click.argument("app-service-name", default=None)
@click.argument("app", default=None)
@click.argument("environment-name", default=None)
@click.option("--org-id", default=None)
@click.option(
    "--expose-type",
    default="not_exposed",
    type=click.Choice(["not_exposed", "application", "path_prefix", "hostname"]),
)
@click.option("--expose-as-hostname", default=None)
@click.option(
    "--connection-mapping",
    default="default",
    type=click.Choice(apps.CONNECTION_MAPPING_OPTS),
)
@click.pass_context
def add_application_service_assignment(ctx, **kwargs):
    output_entry(ctx, apps.add_application_service_assignment(ctx, **kwargs))


@cli.command(name="update-application-service-assignment")
@click.argument("app-service-name", default=None)
@click.argument("app", default=None)
@click.argument("environment-name", default=None)
@click.option("--org-id", default=None)
@click.option(
    "--expose-type",
    default=None,
    type=click.Choice(["not_exposed", "application", "path_prefix", "hostname"]),
)
@click.option("--expose-as-hostname", default=None)
@click.option("--expose-as-hostname-list-json", default=None)
@click.option(
    "--connection-mapping",
    default="default",
    type=click.Choice(apps.CONNECTION_MAPPING_OPTS),
)
@click.pass_context
def update_application_service_assignment(ctx, **kwargs):
    kwargs["expose_as_hostname_list"] = None
    hostname_list_json = kwargs.get("expose_as_hostname_list_json")
    if hostname_list_json is not None:
        kwargs["expose_as_hostname_list"] = json.loads(hostname_list_json)
    output_entry(ctx, apps.update_application_service_assignment(ctx, **kwargs))


@cli.command(name="delete-application-service-assignment")
@click.argument("app-service-name", default=None)
@click.argument("app", default=None)
@click.argument("environment-name", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_application_service_assignment(ctx, **kwargs):
    apps.delete_application_service_assignment(ctx, **kwargs)


@cli.command(name="show-application-service")
@click.argument("id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def show_application_service(ctx, id, org_id, **kwargs):
    output_entry(
        ctx, apps.get_application_service(ctx, id, org_id=org_id, **kwargs).to_dict()
    )


@cli.command(name="delete-application-service")
@click.argument("name", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_application_service(ctx, name, org_id, **kwargs):
    print(apps.delete_application_service(ctx, name, org_id=org_id, **kwargs))


def output_environment_entries(ctx, entry):
    if ctx.obj["output_format"] == "json":
        return output_json(ctx, entry)
    table = PrettyTable(["field", "value"])
    for k, v in list(entry.items()):
        table.add_row([k, v])
    table.align = "l"
    print(table)


@cli.command(name="show-environment")
@click.argument("application", shell_complete=app_completion)
@click.argument("env-name", shell_complete=env_completion)
@click.option("--org-id", default=None)
@click.pass_context
def show_environment(ctx, application, env_name, org_id, **kwargs):
    output_environment_entries(
        ctx, apps.get_env(ctx, application, env_name, org_id, **kwargs)
    )


@cli.command(name="delete-environment")
@click.argument("app", shell_complete=app_completion)
@click.argument("env-name", shell_complete=env_completion)
@click.option("--org-id", default=None)
@click.pass_context
def delete_environment(ctx, app, **kwargs):
    _app = _get_app(ctx, app, **kwargs)
    if _app:
        _env = [env for env in _app["environments"] if env["name"] == kwargs["env_name"]]
        if click.confirm(
            "Do you want to delete this environment?:\n"
            f"{json.dumps(_env, indent=4, sort_keys=True)}"
        ):
            resp = apps.delete_environment(ctx, app_id=_app["id"], **kwargs)
            click.echo(resp)
    else:
        click.echo(f"app {app} not found")


@cli.command(name="update-environment")
@click.argument("app", shell_complete=app_completion)
@click.argument("env_name", shell_complete=env_completion)
@click.option("--org-id", default=None)
@click.option("--version-tag", default=None)
@click.option("--serverless-image", default=None)
@click.option("--config-mount-path", default=None)
@click.option("--config-as-mount", help="json string", default=None)
@click.option("--config-as-env", help="json string", default=None)
@click.option("--secrets-mount-path", default=None)
@click.option("--secrets-as-mount", default=None)
@click.option("--secrets-as-env", default=None)
@click.option("--domain-aliases", default=None, multiple=True)
@click.option("--clear-aliases", is_flag=True)
@click.option("--name-slug", default=None)
@click.option(
    "--proxy-location", default=None, type=click.Choice(["in_cloud", "on_site"])
)
@click.option(
    "--application-configs-data",
    help="A json formatted string that contains the application's configurations.",
    default=None,
)
@click.option(
    "--application-configs-file",
    help="A json file that contains the application's configurations.",
    type=click_extension.JSONFile("r"),
)
@click.pass_context
def update_environment(
    ctx,
    app,
    env_name,
    org_id,
    version_tag,
    config_mount_path,
    config_as_mount,
    config_as_env,
    secrets_mount_path,
    secrets_as_mount,
    secrets_as_env,
    serverless_image,
    application_configs_data,
    application_configs_file,
    domain_aliases,
    **kwargs,
):

    if not application_configs_data and not application_configs_file:
        application_configs = None
    else:
        if application_configs_file:
            if application_configs_data:
                print(
                    """Both application_configs_file and application_configs_data \
are set. Will use application_configs_file as application_configs"""
                )
            application_configs = application_configs_file
            if "application_configs" in application_configs_file:
                application_configs = application_configs_file["application_configs"]
        else:
            application_configs = json.loads(application_configs_data)

    _app = _get_app(ctx, app, org_id=org_id)
    if _app:
        apps.update_env(
            ctx,
            _app["id"],
            env_name,
            org_id,
            version_tag,
            config_mount_path,
            config_as_mount,
            config_as_env,
            secrets_mount_path,
            secrets_as_mount,
            secrets_as_env,
            serverless_image,
            application_configs,
            list(domain_aliases),
            **kwargs,
        )


@cli.command(name="set-env-runtime-status")
@click.argument("app", shell_complete=app_completion)
@click.argument("env-name", shell_complete=env_completion)
@click.option("--org-id", default=None)
@click.option("--overall-status", default=None)
@click.option("--running-replicas", default=None)
@click.option("--error-message", default=None)
@click.option("--restarts", help="json string", default=None)
@click.option("--cpu", help="json string", default=None)
@click.option("--memory", default=None)
@click.option("--running-image", default=None)
@click.option("--running-hash", default=None)
@click.pass_context
def update_environment_status(
    ctx,
    app,
    env_name,
    org_id,
    **kwargs,
):
    _app = _get_app(ctx, app, org_id=org_id)
    _env = [env for env in _app["environments"] if env["name"] == env_name][0]
    if _app:
        status = apps.update_env_runtime_status(
            ctx,
            _app["id"],
            env_name,
            _env["maintenance_org_id"],
            **kwargs,
        )
        click.echo(status)


@cli.command(name="get-env-status")
@click.argument("app", shell_complete=app_completion)
@click.argument("env-name", shell_complete=env_completion)
@click.option("--org-id", default=None)
@click.option("--organisation", default=None)
@click.pass_context
def get_environment_status(
    ctx,
    app,
    env_name,
    org_id,
    organisation,
    **kwargs,
):
    org_id = get_org_id(ctx, org_name=organisation, org_id=org_id)
    _app = _get_app(ctx, app, org_id=org_id)
    _env = [env for env in _app["environments"] if env["name"] == env_name][0]
    output_entry(ctx, _env["status"])


@cli.command(name="delete-application")
@click.argument("app", shell_complete=app_completion)
@click.option("--org-id", default=None)
@click.pass_context
def delete_application(ctx, app, **kwargs):
    _app = _get_app(ctx, app, **kwargs)
    if _app:
        if click.confirm(
            "Do you want to delete this app?:" f"\n{convert_to_json(ctx, _app)}"
        ):
            kwargs.setdefault(_app["org_id"])
            resp = apps.delete(ctx, _app["id"], **kwargs)
            click.echo(resp)


@cli.command(name="add-application")
@click.argument("name")
@click.argument("org-id")
@click.argument("category")
@click.option("--published", type=click.Choice(["no", "public"]), default=None)
@click.option("--default-role-id", default=None)
@click.option("--icon-url", default=None)
@click.option("--location", type=click.Choice(["hosted", "external"]), default=None)
@click.option("--service-account-required", is_flag=True, default=None)
@click.option("--name-slug", default=None)
@click.pass_context
def add_application(ctx, name, org_id, category, **kwargs):
    output_entry(ctx, json.loads(apps.add(ctx, name, org_id, category, **kwargs)))


@cli.command(name="assign-application")
@click.argument("env-name")
@click.argument("app-id")
@click.argument("org-id")
@click.argument("assigned-org-id")
@click.option("--admin-org-id", default=None)
@click.pass_context
def assign_application(ctx, env_name, app_id, org_id, assigned_org_id, admin_org_id):
    output_entry(
        ctx,
        json.loads(
            apps.update_assignment(
                ctx,
                env_name,
                app_id,
                org_id,
                assigned_org_id,
                admin_org_id=admin_org_id,
            )
        ),
    )


@cli.command(name="unassign-application")
@click.argument("env-name")
@click.argument("app-id")
@click.argument("org-id")
@click.argument("assigned-org-id")
@click.pass_context
def unassign_application(ctx, env_name, app_id, org_id, assigned_org_id):
    output_entry(
        ctx,
        json.loads(
            apps.update_assignment(
                ctx, env_name, app_id, org_id, assigned_org_id, unassign=True
            )
        ),
    )


def _get_app(ctx, app, app_id=None, org_id=None, **kwargs):
    _app = apps.get_app(ctx, org_id, app, **kwargs)
    if _app:
        return _app
    else:
        print(f"Application '{app}' not found")


@cli.command(name="show-application")
@click.argument("app", shell_complete=app_completion)
@click.option("--org-id", default=None)
@click.option("--include-migrated-environments", default=True)
@click.pass_context
def show_application(ctx, app, **kwargs):
    _app = _get_app(ctx, app, **kwargs)
    if _app:
        output_entry(ctx, _app)


@cli.command(name="update-application")
@click.argument("app", shell_complete=app_completion)
@click.option("--image", default=None)
@click.option("--port", type=int, default=None)
@click.option("--org-id", default=None)
@click.option("--published", type=click.Choice(["no", "public"]), default=None)
@click.option("--default-role-id", default=None)
@click.option("--icon-url", default=None)
@click.option("--location", type=click.Choice(["hosted", "external"]), default=None)
@click.option("--service-account-id", default=None)
@click.option("--service-account-required/--no-service-account-required", default=None)
@click.option("--name-slug", default=None)
@click.option("--admin-state", type=click.Choice(["active", "disabled"]), default=None)
@click.option("--description", default=None)
@click.pass_context
def update_application(ctx, app, org_id, **kwargs):
    _app = _get_app(ctx, app, org_id=org_id)
    if _app:
        apps.update_application(ctx, _app["id"], org_id, **kwargs)
        output_entry(ctx, json.loads(apps.get(ctx, _app["id"], org_id=org_id)))


@cli.command(name="add-role")
@click.argument("app", shell_complete=app_completion)
@click.argument("role-name")
@click.pass_context
def add_role(ctx, app, role_name):
    _app = _get_app(ctx, app)
    if _app:
        apps.add_role(ctx, _app["id"], role_name)
        output_entry(ctx, json.loads(apps.get(ctx, _app["id"])))


@cli.command(name="rules-from-csv")
@click.argument("app", shell_complete=app_completion)
@click.argument("role-name")
@click.option("--file-name", default="-")
@click.option("--org-id", default=None)
@click.option("--hostname", default=None)
@click.pass_context
def rules_from_csv(ctx, app, role_name, file_name, org_id, hostname):
    _app = _get_app(ctx, app, org_id=org_id)
    if _app:
        result = csv_rules.add_rules_to_app(
            ctx, _app["id"], role_name, file_name, org_id, hostname
        )
        output_entry(ctx, result)


@cli.command(name="add-definition")
@click.argument("app", shell_complete=app_completion)
@click.argument("key")
@click.argument("json-path")
@click.pass_context
def add_definition(ctx, app, key, json_path):
    _app = _get_app(ctx, app)
    if _app:
        apps.add_definition(ctx, _app["id"], key, json_path)
        output_entry(ctx, json.loads(apps.get(ctx, _app["id"])))


@cli.command(name="add-rule")
@click.argument("app", shell_complete=app_completion)
@click.argument("role-name")
@click.argument("method")
@click.argument("path-regex")
@click.option("--query-param", "-q", type=click.Tuple([str, str, str]), multiple=True)
@click.option("--json-pointer", "-j", type=click.Tuple([str, str]), multiple=True)
@click.option("--rule-name", default=None)
@click.option("--host", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def add_rule(
    ctx,
    app,
    role_name,
    method,
    path_regex,
    query_param,
    json_pointer,
    **kwargs,
):
    apps.add_rule(
        ctx,
        app,
        role_name,
        method,
        path_regex,
        query_param,
        json_pointer,
        **kwargs,
    )


@cli.command(name="list-rules")
@click.argument("app", shell_complete=app_completion)
@click.option("--org-id", default=None)
@click.pass_context
def list_rules(ctx, **kwargs):
    table = PrettyTable(
        ["role", "name", "host", "method", "path", "query_param", "json_body"]
    )
    for role in apps.get_roles(ctx, **kwargs):
        for rule in role.get("rules", []):
            body = rule.get("body", {})
            json_body = None
            if body:
                json_body = body.get("json", None)
            table.add_row(
                [
                    role["name"],
                    rule["name"],
                    rule.get("host", ""),
                    rule["method"],
                    rule["path"],
                    rule.get("query_parameters", None),
                    json_body,
                ]
            )
    table.align = "l"
    print(table)


# Rows is a list of dictonaries with the same keys
def _format_subtable_objs(rows):
    if rows is None:
        return None
    return _format_subtable([row.to_dict() for row in rows])


def _format_subtable(rows):
    if not rows:
        return None

    column_names = [k for k, _ in rows[0].items()]
    table = PrettyTable(column_names)
    table.align = "l"
    for row in rows:  # dict
        values = [v for _, v in row.items()]
        table.add_row(values)
    return table


@cli.command(name="list-mfa-challenge-methods")
@click.argument("user-id", default=None, required=False)
@click.option("--challenge-type", default=None)
@click.option("--method-status", type=bool, default=None)
@click.option("--method-origin", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_mfa_challenge_methods(ctx, user_id, **kwargs):
    if user_id is None:
        user_id = tokens.introspect_self(ctx).to_dict().get("sub")

    methods = users.list_mfa_challenge_methods(ctx, user_id, **kwargs)
    table = PrettyTable(
        ["ID", "nickname", "challenge_type", "priority", "endpoint", "origin", "enabled"]
    )
    for method in methods:
        md = method.metadata
        spec = method.spec
        table.add_row(
            [
                md.id,
                spec.nickname,
                spec.challenge_type,
                spec.priority,
                spec.endpoint,
                spec.origin,
                spec.enabled,
            ]
        )
    table.align = "l"
    print(table)


@cli.command(name="add-mfa-challenge-method")
@click.argument("user-id", default=None)
@click.option(
    "--challenge-type",
    type=click.Choice(["web_push", "totp", "webauthn"]),
    default=None,
)
@click.option("--priority", type=int, default=1)
@click.option("--endpoint", default="")
@click.option("--nickname", default=None)
@click.option("--origin", default=None)
@click.option("--enabled/--disabled", default=None)
@click.pass_context
def add_mfa_challenge_method(ctx, user_id, **kwargs):
    result = users.add_mfa_challenge_method(ctx, user_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-mfa-challenge-method")
@click.argument("user-id", default=None)
@click.argument("challenge-method-id", default=None)
@click.pass_context
def show_mfa_challenge_method(ctx, user_id, challenge_method_id, **kwargs):
    result = users.show_mfa_challenge_method(ctx, user_id, challenge_method_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-mfa-challenge-method")
@click.argument("user-id", default=None)
@click.argument("challenge-method-id", default=None)
@click.pass_context
def delete_mfa_challenge_method(ctx, user_id, challenge_method_id, **kwargs):
    users.delete_mfa_challenge_method(ctx, user_id, challenge_method_id, **kwargs)


@cli.command(name="reset-user-mfa-challenge-methods")
@click.argument("user-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def reset_user_mfa_challenge_methods(ctx, user_id, **kwargs):
    users.reset_user_mfa_challenge_methods(ctx, user_id, **kwargs)


@cli.command(name="reset-user-identity")
@click.argument("user-id", default=None)
@click.option("--identifier", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def reset_user_identity(ctx, user_id, **kwargs):
    result = users.reset_user_identity(ctx, user_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="update-mfa-challenge-method")
@click.argument("user-id", default=None)
@click.argument("challenge-method-id", default=None)
@click.option("--challenge-type", type=click.Choice(["web_push"]), default=None)
@click.option("--priority", type=int, default=None)
@click.option("--endpoint", default=None)
@click.option("--nickname", default=None)
@click.option("--origin", default=None)
@click.option("--enabled/--disabled", default=None)
@click.pass_context
def update_mfa_challenge_method(ctx, user_id, challenge_method_id, **kwargs):
    result = users.update_mfa_challenge_method(
        ctx, user_id, challenge_method_id, **kwargs
    )
    output_entry(ctx, result)


@cli.command(name="list-app-rules")
@click.argument("app-id", default=None)
@click.option("--org-id", default=None)
@click.option("--scope", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_app_rules(ctx, app_id, **kwargs):
    app_rules = apps.list_app_rules(ctx, app_id, **kwargs)
    table = PrettyTable(
        [
            "app_id",
            "rule_id",
            "org_id",
            "scope",
            "rule_type",
            "methods",
            "path",
            "query_param",
            "json_body",
        ]
    )
    for rule in app_rules:
        spec = rule.spec
        cond = spec.condition
        body_json = None
        if cond.body:
            body_json = cond.body.json
        table.add_row(
            [
                spec.app_id,
                rule.metadata.id,
                spec.org_id,
                spec.scope,
                cond.rule_type,
                cond.methods,
                cond.path_regex,
                _format_subtable_objs(cond.query_parameters),
                _format_subtable_objs(body_json),
            ]
        )

    table.align = "l"
    print(table)


@cli.command(name="list-combined-rules")
@click.option("--org-id", default=None)
@click.option("--scopes", multiple=True, default=None)
@click.option("--assigned", is_flag=True)
@click.option("--app-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_combined_rules(ctx, **kwargs):
    rules = apps.list_combined_rules(ctx, **kwargs)
    table = PrettyTable(["app_id", "role_id", "role_name", "org_id", "scope", "rules"])
    for rule in rules:
        status = rule.status

        # the rules didn't always have the data needed. can't have columns missing,
        # so set some defaults.
        sub_data = []
        for sub_rule in status.rules:
            if sub_rule.spec.condition is not None:
                sub = sub_rule.spec.condition.to_dict()
                new_dict = {}
                new_dict["rule_type"] = sub.get("rule_type")
                new_dict["body"] = sub.get("body", {})
                new_dict["methods"] = sub.get("methods", [])
                new_dict["path_regex"] = sub.get("path_regex", "")
                new_dict["query_parameters"] = sub.get("query_parameters", [])
                sub_data.append(new_dict)
        table.add_row(
            [
                status.app_id,
                status.role_id,
                status.role_name,
                status.org_id,
                status.scope,
                _format_subtable(sub_data),
            ]
        )

    table.align = "l"
    print(table)


@cli.command(name="list-combined-resource-rules")
@click.option("--org-id", default=None)
@click.option("--scopes", multiple=True, default=None)
@click.option("--assigned", is_flag=True)
@click.option("--resource-id", default=None)
@click.option("--resource-type", default=None, type=resources.resource_type_enum)
@click.option("--limit", default=500)
@click.pass_context
def list_combined_resource_rules(ctx, **kwargs):
    rules = resources.list_combined_resource_rules(ctx, **kwargs)
    print(resources.format_combined_resource_rules_as_text(ctx, rules))


@cli.command(name="add-http-rule")
@click.argument("app-id")
@click.argument("path-regex")
@click.argument("methods", nargs=-1)
@click.option("--rule-type", default="HttpRule")
@click.option("--comments", default=None)
@click.option("--org-id", default=None)
@click.option("--rule-scope", default=None)
@click.pass_context
def add_http_rule(ctx, app_id, **kwargs):
    result = apps.add_http_rule(ctx, app_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-rule-v2")
@click.argument("app-id")
@click.argument("rule-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_rule_v2(ctx, app_id, rule_id, **kwargs):
    result = apps.show_rule_v2(ctx, app_id, rule_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-rule-v2")
@click.argument("app-id")
@click.argument("rule-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_rule_v2(ctx, app_id, rule_id, **kwargs):
    apps.delete_rule_v2(ctx, app_id, rule_id, **kwargs)


@cli.command(name="update-http-rule")
@click.argument("app-id")
@click.argument("rule-id")
@click.option("--path-regex", default=None)
@click.option("--rule-type", default="HttpRule")
@click.option("--comments", default=None)
@click.option("--org-id", default=None)
@click.option("--rule-scope", default=None)
@click.pass_context
def update_http_rule(ctx, app_id, rule_id, rule_scope, **kwargs):
    result = apps.update_http_rule(ctx, app_id, rule_id, scope=rule_scope, **kwargs)
    output_entry(ctx, result)


@cli.command(name="update-http-rule-methods")
@click.argument("app-id")
@click.argument("rule-id")
@click.option("--methods", multiple=True, default=[])
@click.option("--org-id", default=None)
@click.pass_context
def update_http_rule_methods(ctx, app_id, rule_id, methods, **kwargs):
    result = apps.update_http_rule(ctx, app_id, rule_id, methods=methods, **kwargs)
    output_entry(ctx, result)


@cli.command(name="update-http-rule-query-params")
@click.argument("app-id")
@click.argument("rule-id")
@click.option(
    "--query-param",
    "-q",
    type=click.Tuple([str, str, str]),
    multiple=True,
    default=[],
    help="A tuple of strings representing the query parameter name"
    ", match value, and type (exact, regex)",
)
@click.option("--org-id", default=None)
@click.pass_context
def update_http_rule_query_params(ctx, app_id, rule_id, query_param, **kwargs):
    result = apps.update_http_rule(
        ctx, app_id, rule_id, query_params=query_param, **kwargs
    )
    output_entry(ctx, result)


@cli.command(name="update-http-rule-body-params")
@click.argument("app-id")
@click.argument("rule-id")
@click.option(
    "--body_param",
    "-bp",
    type=click.Tuple([str, str, str, str]),
    multiple=True,
    help="A tuple of strings representing the name, value to match against, match type, and json pointer path",  # noqa
)
@click.option("--org-id", default=None)
@click.pass_context
def update_http_rule_body_params(ctx, app_id, rule_id, body_param, **kwargs):
    result = apps.update_http_rule(
        ctx, app_id, rule_id, body_params=body_param, **kwargs
    )
    output_entry(ctx, result)


@cli.command(name="list-roles")
@click.argument("app-id", default=None)
@click.option("--org-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_roles(ctx, app_id, **kwargs):
    roles = apps.list_roles(ctx, app_id, **kwargs)
    table = PrettyTable(["app_id", "role_id", "name", "org_id", "included_roles"])
    for role in roles:
        spec = role.spec
        table.add_row(
            [
                spec.app_id,
                role.metadata.id,
                spec.name,
                spec.org_id,
                _format_subtable_objs(spec.included),
            ]
        )

    table.align = "l"
    print(table)


@cli.command(name="add-role-v2")
@click.argument("app-id", default=None)
@click.argument("name", default=None)
@click.option("--org-id", default=None)
@click.option("--comments", default=None)
@click.option("--included", multiple=True)
@click.pass_context
def add_role_v2(ctx, app_id, name, **kwargs):
    result = apps.add_role_v2(ctx, app_id, name, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-role-v2")
@click.argument("app-id", default=None)
@click.argument("role-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def show_role(ctx, app_id, role_id, **kwargs):
    result = apps.show_role_v2(ctx, app_id, role_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-role-v2")
@click.argument("app-id", default=None)
@click.argument("role-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_role(ctx, app_id, role_id, **kwargs):
    apps.delete_role_v2(ctx, app_id, role_id, **kwargs)


@cli.command(name="update-role-v2")
@click.argument("app-id", default=None)
@click.argument("role-id", default=None)
@click.option("--name", default=None)
@click.option("--comments", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def update_role(ctx, app_id, role_id, **kwargs):
    result = apps.update_role_v2(ctx, app_id, role_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="update-role-includes")
@click.argument("app-id", default=None)
@click.argument("role-id", default=None)
@click.option("--included", multiple=True, default=[])
@click.pass_context
def update_role_includes(ctx, app_id, role_id, included, **kwargs):
    result = apps.update_role_v2(ctx, app_id, role_id, included=included, **kwargs)
    output_entry(ctx, result)


@cli.command(name="list-roles-to-rules")
@click.argument("app-id", default=None)
@click.option("--org-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_roles_to_rules(ctx, app_id, **kwargs):
    roles = apps.list_roles_to_rules(ctx, app_id, **kwargs)
    table = PrettyTable(["role_to_rule_id", "role_id", "rule_id", "org_id", "included"])
    for role in roles:
        spec = role.spec
        table.add_row(
            [role.metadata.id, spec.role_id, spec.rule_id, spec.org_id, spec.included]
        )

    table.align = "l"
    print(table)


@cli.command(name="add-role-to-rule")
@click.argument("app-id", default=None)
@click.argument("role-id", default=None)
@click.argument("rule-id", default=None)
@click.option("--org-id", default=None)
@click.option("--included/--excluded", default=True)
@click.pass_context
def add_role_to_rule(ctx, app_id, role_id, rule_id, **kwargs):
    result = apps.add_role_to_rule(ctx, app_id, role_id, rule_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-role-to-rule")
@click.argument("app-id", default=None)
@click.argument("role-to-rule-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def show_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs):
    result = apps.show_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-role-to-rule")
@click.argument("app-id", default=None)
@click.argument("role-to-rule-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs):
    apps.delete_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs)


@cli.command(name="update-role-to-rule")
@click.argument("app-id", default=None)
@click.argument("role-to-rule-id", default=None)
@click.option("--org-id", default=None)
@click.option("--included/--excluded", default=True)
@click.pass_context
def update_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs):
    result = apps.update_role_to_rule(ctx, app_id, role_to_rule_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-rule")
@click.argument("app", shell_complete=app_completion)
@click.argument("role-name")
@click.argument("rule-name")
@click.option("--org-id", default=None)
@click.pass_context
def delete_rule(ctx, **kwargs):
    apps.delete_rule(ctx, **kwargs)


@cli.command(name="whoami")
@click.option("--refresh/--no-refresh", default=False)
@click.pass_context
def get_whoami(ctx, refresh=None, **kwargs):
    whoami.whoami_id(ctx, refresh, **kwargs)
    output_entry(ctx, tokens.introspect_self(ctx).to_dict())


@cli.command(name="show-token-introspection")
@click.option("--refresh", default=False)
@click.option("--token", default=None)
@click.option("--exclude-roles", default=False, type=bool)
@click.option("--include-suborgs", default=False, type=bool)
@click.option("--support-http-matchers", default=True, type=bool)
@click.option("--target-domain", default=None)
@click.option("--no-cache", is_flag=True, default=False)
@click.pass_context
def show_token_introspection(
    ctx,
    refresh=None,
    token=None,
    exclude_roles=False,
    include_suborgs=False,
    no_cache=False,
    **kwargs,
):
    """
    Introspects the user's permissions as provided by the current access token.
    Introspect a different token by passing in the unencoded JWT using --token.
    """
    my_token = token
    if not my_token:
        my_token = whoami.whoami(ctx, refresh, **kwargs)
    result = tokens.get_introspect(
        ctx,
        my_token,
        exclude_roles=exclude_roles,
        include_suborgs=include_suborgs,
        no_cache=no_cache,
        **kwargs,
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="get-token")
@click.pass_context
def get_token(ctx, **kwargs):
    token = whoami.whoami(ctx, False, **kwargs)
    if not token:
        print("No token found", file=sys.stderr)
        sys.exit(1)

    print(token)


@cli.command(name="create-token")
@click.option("--user-id", default=None, required=False)
@click.option("--org-id", default=None, required=False)
@click.option("--role", "-r", type=click.Tuple([str, str]), multiple=True)
@click.option("--duration", type=int, default=3600)
@click.option("--aud", type=str, multiple=True)
@click.option("--scope", type=str, multiple=True)
@click.option("--inherit-session", type=bool, default=False)
@click.option("--create-refresh-token", is_flag=True)
@click.option("--get-user", is_flag=True)
@click.pass_context
def create_token(
    ctx, user_id, org_id, role, duration, aud, scope, inherit_session, **kwargs
):
    if user_id is None:
        user_id = tokens.introspect_self(ctx).to_dict().get("sub")
    org_id = get_org_from_input_or_ctx(ctx, org_id)
    roles = {endpoint: role_name for endpoint, role_name in role}
    result = tokens.create_token(
        ctx,
        user_id,
        roles,
        duration,
        list(aud),
        org_id=org_id,
        scopes=scope,
        inherit_session=inherit_session,
        **kwargs,
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="bulk-revoke-tokens")
@click.argument("user-id")
@click.option("--org-id", type=str, default=None)
@click.option("--session-id", type=str, default=None)
@click.pass_context
def bulk_revoke_token(ctx, user_id, **kwargs):
    output_entry(ctx, tokens.bulk_revoke_token(ctx, user_id, **kwargs))


@cli.command(name="bulk-revoke-sessions")
@click.argument("user-id")
@click.option("--org-id", type=str, default=None)
@click.option("--session-id", type=str, default=None)
@click.option("--tokens-only", is_flag=True)
@click.pass_context
def bulk_revoke_sessions(ctx, user_id, **kwargs):
    output_entry(ctx, tokens.bulk_revoke_sessions(ctx, user_id, **kwargs))


@cli.command(name="bulk-delete-sessions")
@click.argument("user-id")
@click.option("--org-id", type=str, default=None)
@click.pass_context
def bulk_delete_sessions(ctx, user_id, **kwargs):
    output_entry(ctx, tokens.bulk_delete_sessions(ctx, user_id, **kwargs))


@cli.command(name="create-service-token")
@click.option(
    "--authentication-document", type=click_extension.JSONFile("r"), default=None
)
@click.option("--scope", type=str, multiple=True)
@click.option("--client-id", default=None)
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--auth-issuer-url", default=None)
@click.option("--expiry", default=None)
@click.option("--access-token", default=None)
@click.pass_context
def create_service_token(
    ctx, authentication_document, access_token, client_id, **kwargs
):
    if authentication_document:
        token = tokens.create_service_token(
            auth_doc=authentication_document, ctx=ctx, **kwargs
        )
        print(token)
    else:
        if not access_token:
            access_token = context.get_token(ctx)
        token = service_token.Token(
            access_token=access_token,
            cacert=context.get_cacert(ctx),
            api_host=context.get_api(ctx),
            client_id=context.get_client_id(ctx),
            **kwargs,
        )
        print(token.get())


@cli.command(name="list-files")
@click.option("--org-id", default=None)
@click.option("--tag", default=None)
@click.option("--file-association-id", default=None)
@click.option(
    "--oper-status", default=None, type=click.Choice(files.OPER_STATUS_OPTIONS)
)
@click.option("--has-been-associated", default=None, type=bool)
@click.pass_context
def list_files(ctx, oper_status, **kwargs):
    _files = files.query(ctx, object_oper_status=oper_status, **kwargs)
    table = PrettyTable(
        ["id", "name", "tag", "label", "created", "last_accessed", "size", "visibility"]
    )
    table.align = "l"
    for _file in _files:
        _file["tag"] = _file["tag"] if "tag" in _file else ""
        _file["label"] = _file["label"] if "label" in _file else ""
        table.add_row(
            [
                _file["id"],
                _file["name"],
                _file["tag"],
                _file["label"],
                _file["created"],
                _file["last_access"],
                _file.get("size", None),
                _file["visibility"],
            ]
        )
    print(table)


@cli.command(name="upload-file")
@click.argument("filename", type=click.Path(exists=True))
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.option("--label", default=None)
@click.option("--tag", default=None)
@click.option("--region", default=None)
@click.option("--visibility", type=click.Choice(["public", "private"]), default=None)
@click.pass_context
def upload_file(ctx, **kwargs):
    output_entry(ctx, files.upload(ctx, **kwargs))


@cli.command(name="reupload-file")
@click.argument("file-id")
@click.option("--filename", type=click.Path(exists=True), required=True)
@click.option("--org-id", default=None)
@click.pass_context
def reupload_file(ctx, **kwargs):
    output_entry(ctx, files.reupload(ctx, **kwargs))


@cli.command(name="download-file")
@click.argument("file-id")
@click.option("--org-id", default=None)
@click.option("--destination", default=None)
@click.pass_context
def download_file(ctx, **kwargs):
    files.download(ctx, **kwargs)


@cli.command(name="delete-file")
@click.argument("file-ids", nargs=-1)
@click.option("--org-id", default=None)
@click.pass_context
def delete_file(ctx, file_ids, **kwargs):
    for file_id in file_ids:
        files.delete(ctx, file_id=file_id, **kwargs)


@cli.command(name="show-file")
@click.argument("file-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def show_file(ctx, **kwargs):
    output_entry(ctx, files.get(ctx, **kwargs))


@cli.command(name="list-file-associations")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--file-id", default=None)
@click.option("--object-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_file_associations(ctx, name=None, **kwargs):
    file_associations = files.list_file_associations(ctx, name=name, **kwargs)
    table = files.format_file_associations(ctx, file_associations)
    print(table)


@cli.command(name="add-file-association")
@click.option("--org-id", default=None)
@click.option("--file-id", required=True)
@click.option("--object-id", required=True)
@click.pass_context
def add_file_association(ctx, **kwargs):
    result = files.add_file_association(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-file-association")
@click.argument("association-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_file_association(ctx, association_id, **kwargs):
    result = files.show_file_association(ctx, association_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-file-association")
@click.argument("association-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_file_association(ctx, association_id, **kwargs):
    files.delete_file_association(ctx, association_id, **kwargs)


@cli.command(
    name="clear-file-associations",
    help=(
        "clears file associations, marking any files now with none as ready for garbage"
        " collection"
    ),
)
@click.option(
    "--object-id", default=None, help="clear up associations related to this object"
)
@click.option("--org-id", default=None)
@click.pass_context
def clear_file_association(ctx, object_id, org_id, **kwargs):
    if object_id is None and org_id is None:
        raise click.UsageError(
            'Specify an org-id or object-id. "" will clear all objects'
        )

    result = files.clear_file_associations(
        ctx, object_id=object_id, org_id=org_id, **kwargs
    )
    table = files.format_cleared_associations(ctx, result)
    print(table)


@cli.command(name="list-config")
@click.argument("application", shell_complete=app_completion)
@click.argument("env-name", shell_complete=env_completion)
@click.option("--org-id", default=None)
@click.pass_context
def list_config(ctx, **kwargs):
    configs = env_config.query(ctx, **kwargs)

    table = PrettyTable(
        [
            "id",
            "config_type",
            "host",
            "src_mount",
            "domain",
            "share",
            "username",
            "password",
            "dest_mount",
            "file_store_uri",
        ]
    )
    table.align = "l"
    for config in configs:
        table.add_row(
            [
                config.id,
                config.config_type,
                config.mount_hostname,
                config.mount_src_path,
                config.mount_domain,
                config.mount_share,
                config.mount_username,
                config.mount_password,
                config.mount_path,
                config.file_store_uri,
            ]
        )
    print(table)


@cli.command(name="add-config")
@click.argument("application", shell_complete=app_completion)
@click.argument("env-name", shell_complete=env_completion)
@click.option("--org-id", default=None)
@click.option("--filename", default=None)
@click.option(
    "--config_type",
    type=click.Choice(
        [
            "configmap_mount",
            "configmap_env",
            "secret_mount",
            "secret_env",
            "mount_smb",
            "mount_tmpdir",
            "file_mount",
        ]
    ),
    prompt=True,
)
@click.option("--mount-path", default=None, prompt=True)
@click.option("--mount-src-path", default=None)
@click.option("--username", default=None)
@click.option("--hostname", default=None)
@click.option("--password", default=None)
@click.option("--share", default=None)
@click.option("--domain", default=None)
@click.option("--file-store-uri", default=None)
@click.pass_context
def add_config(ctx, **kwargs):
    output_entry(ctx, env_config.add(ctx, **kwargs).to_dict())


@cli.command(name="update-config")
@click.argument("application", shell_complete=app_completion)
@click.argument("env-name", shell_complete=env_completion)
@click.argument("id", default=None)
@click.option("--org-id", default=None)
@click.option(
    "--config_type",
    type=click.Choice(
        [
            "configmap_mount",
            "configmap_env",
            "secret_mount",
            "secret_env",
            "file_mount",
        ]
    ),
)
@click.option("--mount-path", default=None)
@click.option("--mount-src-path", default=None)
@click.option("--username", default=None)
@click.option("--password", default=None)
@click.option("--share", default=None)
@click.option("--domain", default=None)
@click.option("--file-store-uri", default=None)
@click.pass_context
def update_config(ctx, **kwargs):
    output_entry(ctx, env_config.update(ctx, **kwargs).to_dict())


@cli.command(name="delete-config")
@click.argument("application", shell_complete=app_completion)
@click.argument("env-name", shell_complete=env_completion)
@click.argument("id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_config(ctx, **kwargs):
    env_config.delete(ctx, **kwargs)


@cli.command(name="list-env-vars")
@click.argument("application", shell_complete=app_completion)
@click.argument("env-name", shell_complete=env_completion)
@click.option("--org-id", default=None)
@click.option("--secret", default=True)
@click.pass_context
def list_env_vars(ctx, **kwargs):
    envVar = env_config.EnvVarConfigObj(ctx, **kwargs)
    new_envs = envVar.get_env_list()

    output = env_config.format_env_vars_as_text(ctx, new_envs)
    print(output)


@cli.command(name="add-env-var")
@click.argument("application", shell_complete=app_completion)
@click.argument("env-name", shell_complete=env_completion)
@click.argument("env-config-name", default=None)
@click.argument("env-config-value", default=None)
@click.option("--org-id", default=None)
@click.option("--secret", default=True)
@click.pass_context
def add_env_var(ctx, env_config_name, env_config_value, **kwargs):
    envVar = env_config.EnvVarConfigObj(ctx, **kwargs)
    envVar.add_env_var(env_config_name, env_config_value)


@cli.command(name="delete-env-var")
@click.argument("application", shell_complete=app_completion)
@click.argument("env-name", shell_complete=env_completion)
@click.argument("env-var-name", default=None)
@click.option("--org-id", default=None)
@click.option("--secret", default=True)
@click.pass_context
def delete_env_var(ctx, env_var_name, **kwargs):
    envVar = env_config.EnvVarConfigObj(ctx, **kwargs)
    envVar.del_env_var(env_var_name)


@cli.command(name="update-env-var")
@click.argument("application", shell_complete=app_completion)
@click.argument("env-name", shell_complete=env_completion)
@click.argument("env-config-name", default=None)
@click.argument("env-config-value", default=None)
@click.option("--secret", default=True)
@click.pass_context
def update_env_var(ctx, env_config_name, env_config_value, **kwargs):
    envVar = env_config.EnvVarConfigObj(ctx, **kwargs)
    envVar.update_env_var(env_config_name, env_config_value)


@cli.command(name="get-logs")
@click.argument("org-id", default=None)
@click.option("--sub-org-id", default=None)
@click.option("--sub", default=None)
@click.option("--app", default=None)
@click.option("--dt-from", default=None)
@click.option("--dt-to", default=None)
@click.option("--dt-sort", default="asc")
@click.option("--limit", default=None)
@click.pass_context
def get_logs(ctx, **kwargs):
    _logs = logs.get(ctx, **kwargs)
    print(_logs)


@cli.command(name="get-top-users")
@click.argument("org-id", default=None)
@click.option("--dt-from", default=None)
@click.option("--dt-to", default=None)
@click.option("--app-id", default=None)
@click.option("--resource-id", default=None)
@click.option("--resource-name", default=None)
@click.option("--resource-type", default=None, type=resources.resource_type_enum)
@click.option("--sub-org-id", default=None)
@click.option("--interval", default=None)
@click.option("--limit", default=None)
@click.pass_context
def get_top_users(ctx, **kwargs):
    _metrics = metrics.query_top(ctx, **kwargs)
    table = PrettyTable(["user_id", "email", "count"])
    table.align = "l"
    if _metrics is not None:
        for _metric in _metrics:
            table.add_row([_metric.user_id, _metric.email, _metric.count])
    print(table)


@cli.command(name="get-active-users")
@click.argument("org-id", default=None)
@click.option("--dt-from", default=None)
@click.option("--dt-to", default=None)
@click.option("--app-id", default=None)
@click.option("--resource-id", default=None)
@click.option("--resource-name", default=None)
@click.option("--resource-type", default=None, type=resources.resource_type_enum)
@click.option("--sub-org-id", default=None)
@click.option("--interval", default=None)
@click.pass_context
def get_active_users(ctx, **kwargs):
    _metrics = metrics.query_active(ctx, **kwargs)
    table = PrettyTable(["time", "metric"])
    table.align = "l"
    if _metrics is not None:
        for _metric in _metrics:
            table.add_row([_metric.time, _metric.metric])
    print(table)


def _format_catalogue_entries_subtable(entries):
    table = PrettyTable(["name", "tag", "content"])
    table.align = "l"
    if entries:
        for entry in entries:
            table.add_row([entry.name, entry.tag, entry.content])
    return table


@cli.command(name="list-catalogues")
@click.option("--catalogue-category", default=None)
@click.option("--limit", default=25, type=int)
@click.pass_context
def list_catalogues(ctx, **kwargs):
    pop_item_if_none(kwargs, "catalogue_category")
    cats = catalogues.query(ctx, **kwargs)
    if ctx.obj["output_format"] == "json":
        cats_list = [x.to_dict() for x in cats]
        return output_json(ctx, cats_list)
    table = PrettyTable(["id", "category", "entries summary"])
    table.align = "l"
    for cat in cats:
        table.add_row(
            [
                cat.id,
                cat.category,
                _format_catalogue_entries_subtable(cat.catalogue_entries),
            ]
        )
    print(table)


@cli.command(name="show-catalogue")
@click.argument("catalogue-id", default=None)
@click.pass_context
def show_catalogue(ctx, **kwargs):
    output_entry(ctx, catalogues.show(ctx, **kwargs))


@cli.command(name="add-catalogue")
@click.argument("category", default=None)
@click.pass_context
def add_catalogue(ctx, **kwargs):
    output_entry(ctx, catalogues.add(ctx, **kwargs))


@cli.command(name="update-catalogue")
@click.argument("catalogue-id", default=None)
@click.option("--category", default=None)
@click.pass_context
def update_catalogue(ctx, **kwargs):
    output_entry(ctx, catalogues.update(ctx, **kwargs))


@cli.command(name="delete-catalogue")
@click.argument("catalogue-id", default=None)
@click.pass_context
def delete_catalogue(ctx, **kwargs):
    catalogues.delete(ctx, **kwargs)


@cli.command(name="list-catalogue-entries")
@click.option("--catalogue-id", default=None)
@click.option("--catalogue-category", default=None)
@click.option("--catalogue-entry-name", default=None)
@click.option("--limit", default=50, type=int)
@click.pass_context
def list_catalogue_entries(ctx, **kwargs):
    catalogue_id = kwargs.pop("catalogue_id", None)
    entries = catalogues.query_entries(ctx, catalogue_id=catalogue_id, **kwargs)
    if ctx.obj["output_format"] == "json":
        entries_list = [x.to_dict() for x in entries]
        return output_json(ctx, entries_list)
    table = PrettyTable(
        [
            "id",
            "catalogue_id",
            "category",
            "name",
            "content",
            "tag",
            "short desc",
            "long desc",
        ]
    )
    table.align = "l"
    for entry in entries:
        table.add_row(
            [
                entry.id,
                entry.catalogue_id,
                entry.catalogue_category,
                entry.name,
                entry.content,
                entry.tag,
                entry.short_description,
                entry.long_description,
            ]
        )
    print(table)


@cli.command(name="show-catalogue-entry")
@click.argument("catalogue-id", default=None)
@click.argument("entry-id", default=None)
@click.pass_context
def show_catalogue_entry(ctx, **kwargs):
    output_entry(ctx, catalogues.show_entry(ctx, **kwargs))


@cli.command(name="add-catalogue-entry")
@click.argument("catalogue-id", default=None)
@click.argument("name", default=None)
@click.option("--content", default=None)
@click.option("--tag", default=None)
@click.option("--short-description", default=None)
@click.option("--long-description", default=None)
@click.option(
    "--content-file",
    help="A file that contains the catalogue_content",
    type=click_extension.File("r"),
)
@click.pass_context
def add_catalogue_entry(ctx, content_file, content, **kwargs):
    if content_file:
        if content:
            print("Both content and content_file are set. Using content_file")

        content = content_file.read()

    output_entry(ctx, catalogues.add_entry(ctx, content=content, **kwargs))


@cli.command(name="update-catalogue-entry")
@click.argument("catalogue_id", default=None)
@click.argument("entry_id", default=None)
@click.option("--name", default=None)
@click.option("--content", default=None)
@click.option("--tag", default=None)
@click.option("--short-description", default=None)
@click.option("--long-description", default=None)
@click.option(
    "--content-file",
    help="A file that contains the catalogue_content",
    type=click_extension.File("r"),
)
@click.pass_context
def update_catalogue_entry(ctx, content_file, content, **kwargs):

    if content_file:
        if content:
            print("Both content and content_file are set. Using content_file")

        content = content_file.read()

    output_entry(ctx, catalogues.update_entry(ctx, content=content, **kwargs))


@cli.command(name="delete-catalogue-entry")
@click.argument("catalogue-id", default=None)
@click.argument("entry-id", default=None)
@click.pass_context
def delete_catalogue_entry(ctx, **kwargs):
    catalogues.delete_entry(ctx, **kwargs)


def _format_flat_list(items):
    return [item for item in items]


@cli.command(name="list-issuer-roots")
@click.option("--issuer", default=None)
@click.option("--summarize-collection", type=bool, default=True)
@click.option("--limit", default=None, type=int)
@click.pass_context
def list_issuer_roots(ctx, **kwargs):
    results = issuers.list_issuer_roots(ctx, **kwargs)
    columns = make_columns(
        ctx,
        results,
        """
          - id
          - issuer
          - org_id
        """,
    )
    print(format_table(ctx, results, columns))


@cli.command(name="list-issuers")
@click.option("--org-id", default=None)
@click.option("--summarize-collection", type=bool, default=True)
@click.option("--limit", default=None, type=int)
@click.option("--show-deleted", is_flag=True, default=None)
@click.pass_context
def list_issuers(ctx, **kwargs):
    _issuers = issuers.query(ctx, **kwargs)
    if ctx.obj["output_format"] == "json":
        iss = []
        for issuer in _issuers:
            issx = {}
            issx["enabled"] = issuer.enabled
            issx["id"] = issuer.id
            issx["local_auth_upstreams"] = issuer.local_auth_upstreams
            managed_upstreams = []
            for mui in issuer.managed_upstreams:
                mu = {}
                mu["enabled"] = mui.enabled
                mu["name"] = mui.name
                managed_upstreams.append(mu)
            issx["managed_upstreams"] = managed_upstreams
            issx["name_slug"] = issuer.name_slug
            issx["oidc_upstreams"] = issuer.oidc_upstreams
            issx["org_id"] = issuer.org_id
            issx["theme_file_id"] = issuer.theme_file_id
            issx["upstream_redirect_uri"] = issuer.upstream_redirect_uri
            issx["service_account_id"] = issuer.service_account_id
            clients = []
            for client in issuer.clients:
                cl = {}
                cl["attributes"] = client.attributes
                cl["id"] = client.id
                cl["mfa_challenge"] = client.mfa_challenge
                cl["name"] = client.name
                cl["org_id"] = client.org_id
                cl["organisation_scope"] = client.organisation_scope
                cl["redirects"] = client.redirects
                cl["restricted_organisations"] = client.restricted_organisations
                cl["saml_metadata_file"] = client.saml_metadata_file
                cl["secret"] = client.secret
                cl["single_sign_on"] = client.single_sign_on
                clients.append(cl)
            issx["clients"] = clients
            iss.append(issx)
        return output_json(ctx, iss)
    table = PrettyTable(
        [
            "issuer-id",
            "issuer",
            "enabled",
            "service_account_id",
            "client-id",
            "client",
            "org",
            "secret",
            "application",
            "organisation_scope",
            "redirects",
            "restricted_organisations",
        ]
    )
    table.align = "l"
    for issuer in _issuers:
        if len(issuer.clients):
            for client in issuer.clients:
                table.add_row(
                    [
                        issuer.id,
                        issuer.issuer,
                        issuer.enabled,
                        issuer.service_account_id,
                        client.id,
                        client.name,
                        client.org_id,
                        client.secret,
                        client.application,
                        client.organisation_scope,
                        _format_flat_list(client.redirects),
                        _format_flat_list(client.restricted_organisations),
                    ]
                )
        else:
            table.add_row(
                [
                    issuer.id,
                    issuer.issuer,
                    issuer.enabled,
                    issuer.service_account_id,
                    "-",
                    "-",
                    issuer.org_id,
                    "-",
                    "-",
                    "-",
                    "-",
                    "-",
                ]
            )
    print(table)


@cli.command(name="show-issuer")
@click.argument("issuer-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def show_issuer(ctx, **kwargs):
    output_entry(ctx, issuers.show(ctx, **kwargs))


@cli.command(name="show-wellknown-issuer-info")
@click.argument("issuer-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def show_well_known_issuer_info(ctx, **kwargs):
    output_entry(ctx, issuers.show_well_known(ctx, **kwargs))


@cli.command(name="list-issuer-upstreams")
@click.argument("issuer-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def list_issuer_upstreams(ctx, issuer_id, **kwargs):
    result = issuers.list_issuer_upstreams(ctx, issuer_id, **kwargs)
    print(issuers.format_issuer_upstreams(ctx, result))


@cli.command(name="list-all-issuer-upstreams")
@click.option("--upstream-type", default=None)
@click.option("--org-id", default=None)
@click.option(
    "--admin-status",
    default=None,
    type=click.Choice(["active", "disabled", "testing", "deleted"]),
)
@click.pass_context
def list_all_issuer_upstreams(ctx, **kwargs):
    result = issuers.list_all_issuer_upstreams(ctx, **kwargs)
    print(issuers.format_all_issuer_upstreams(ctx, result))


@cli.command(name="update-local-issuer-upstream")
@click.argument("issuer-id")
@click.argument("name", default=None)
@click.option("--org-id", default=None)
@click.option(
    "--admin-status",
    default=None,
    type=click.Choice(["active", "disabled", "testing", "deleted"]),
)
@click.pass_context
def update_issuer_upstream(ctx, *args, **kwargs):
    issuers.update_local_upstream(ctx, *args, **kwargs)


@cli.command(name="list-wellknown-issuer-info")
@click.option("--org-id", default=None)
@click.option("--issuer-id", default=None)
@click.pass_context
def list_well_known_issuer_info(ctx, **kwargs):
    result = issuers.list_well_known(ctx, **kwargs)
    print(issuers.format_well_known_issuer_info(ctx, result))


@cli.command(name="add-issuer")
@click.argument("issuer", default=None)
@click.argument("org-id", type=str, default=None)
@click.option("--parent-issuer", default=None)
@click.option("--upstream-redirect-uri", default=None)
@click.pass_context
def add_issuer(ctx, **kwargs):
    output_entry(ctx, issuers.add(ctx, **kwargs))


@cli.command(name="update-issuer-root")
@click.argument("issuer_id", default=None)
@click.option("--issuer", default=None)
@click.option("--org-id", default=None)
@click.option("--theme-file-id", type=str, default=None)
@click.option("--upstream-redirect-uri", default=None)
@click.option("--saml-state-encryption-key", default=None)
@click.option("--enabled/--disabled", default=None)
@click.option(
    "--admin-status",
    default=None,
    type=click.Choice(["active", "disabled", "testing", "deleted"]),
)
@click.option("--parent-issuer", default=None)
@click.pass_context
def update_issuer_root(ctx, issuer_id, **kwargs):
    output_entry(ctx, issuers.update_root(ctx, issuer_id, **kwargs))


@cli.command(name="update-issuer")
@click.argument("issuer-id", default=None)
@click.option("--theme-file-id", default=None)
@click.option("--org-id", default=None)
@click.option("--saml-state-encryption-key", default=None)
@click.option("--enabled/--disabled", default=None)
@click.option("--parent-issuer", default=None)
@click.pass_context
def update_issuer_extension(ctx, issuer_id, **kwargs):
    output_entry(ctx, issuers.update_extension(ctx, issuer_id, **kwargs))


@cli.command(name="reset-issuer-service-account")
@click.argument("issuer-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def reset_issuer_service_account(ctx, issuer_id, **kwargs):
    output_entry(ctx, issuers.reset_service_account(ctx, issuer_id, **kwargs))


@cli.command(name="delete-issuer")
@click.argument("issuer-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_issuer(ctx, **kwargs):
    issuers.delete(ctx, **kwargs)


@cli.command(name="list-clients")
@click.option("--org-id", default=None)
@click.option("--limit", default=None, type=int)
@click.option("--summarize-collection", default=True, type=bool)
@click.pass_context
def list_clients(ctx, **kwargs):
    _clients = issuers.query_clients(ctx, **kwargs)
    table = PrettyTable(
        [
            "id",
            "issuer_id",
            "org_id",
            "name",
            "secret",
            "application",
            "organisation_scope",
            "mfa_challenge",
            "single_sign_on",
            "redirects",
            "restricted_organisations",
        ]
    )
    table.align = "l"
    for client in _clients:
        table.add_row(
            [
                client.id,
                client.issuer_id,
                client.org_id,
                client.name,
                client.secret,
                client.application,
                client.organisation_scope,
                client.mfa_challenge,
                client.single_sign_on,
                _format_flat_list(client.redirects),
                _format_flat_list(client.restricted_organisations),
            ]
        )
    print(table)


@cli.command(name="show-client")
@click.argument("client-id", default=None)
@click.option("--org-id", default=None)
@click.option("--summarize-collection", default=True, type=bool)
@click.pass_context
def show_client(ctx, **kwargs):
    output_entry(ctx, issuers.show_client(ctx, **kwargs))


@cli.command(name="add-client")
@click.argument("issuer-id", default=None)
@click.argument("name", default=None)
@click.option("--secret", default=None)
@click.option("--application", default=None)
@click.option("--org-id", default=None)
@click.option(
    "--organisation-scope",
    default=None,
    type=click.Choice(["any", "here_and_down", "here_only"]),
)
@click.option(
    "--mfa-challenge",
    default=None,
    type=click.Choice(["always", "trust_upstream", "user_preference"]),
)
@click.option(
    "--single-sign-on",
    default=None,
    type=click.Choice(["never", "user_preference"]),
)
@click.option("--redirect-url", default=None, multiple=True)
@click.option("--restricted-org-id", default=None, multiple=True)
@click.option("--metadata-file", default=None)
@click.option("--metadata-text", default=None)
@click.pass_context
def add_client(ctx, redirect_url, restricted_org_id, **kwargs):
    output_entry(
        ctx,
        issuers.add_client(
            ctx,
            restricted_organisations=list(restricted_org_id),
            redirects=list(redirect_url),
            **kwargs,
        ),
    )


@cli.command(name="update-client")
@click.argument("client-id", default=None)
@click.option("--name", default=None)
@click.option("--secret", default=None)
@click.option("--application", default=None)
@click.option("--org-id", default=None)
@click.option("--issuer-id", default=None)
@click.option(
    "--organisation-scope",
    default=None,
    type=click.Choice(["any", "here_and_down", "here_only"]),
)
@click.option(
    "--mfa-challenge",
    default=None,
    type=click.Choice(["always", "trust_upstream", "user_preference"]),
)
@click.option(
    "--single-sign-on",
    default=None,
    type=click.Choice(["never", "user_preference"]),
)
@click.option("--metadata-file", default=None)
@click.option("--metadata-text", default=None)
@click.option("--id-mapping", default=None, multiple=True)
@click.option("--saml-scopes", default=None, multiple=True)
@click.option("--redirect-url", default=None, multiple=True)
@click.pass_context
def update_client(ctx, redirect_url, **kwargs):
    output_entry(
        ctx,
        issuers.update_client(
            ctx,
            redirects=list(redirect_url),
            **kwargs,
        ),
    )


@cli.command(name="delete-client")
@click.argument("client-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_client(ctx, **kwargs):
    issuers.delete_client(ctx, **kwargs)


@cli.command(name="add-redirect")
@click.argument("client-id", default=None)
@click.argument("redirect-url", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def add_redirect(ctx, **kwargs):
    output_entry(ctx, issuers.add_redirect(ctx, **kwargs))


@cli.command(name="delete-redirect")
@click.argument("client-id", default=None)
@click.argument("redirect-url", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_redirect(ctx, **kwargs):
    output_entry(ctx, issuers.delete_redirect(ctx, **kwargs))


@cli.command(name="replace-redirects")
@click.argument("client-id", default=None)
@click.option("--redirect-url", default=None, multiple=True)
@click.option("--org-id", default=None)
@click.pass_context
def replace_redirets(ctx, redirect_url=None, **kwargs):
    output_entry(ctx, issuers.update_client(ctx, redirects=redirect_url, **kwargs))


@cli.command(name="add-restricted-org")
@click.argument("client-id", default=None)
@click.argument("restricted-org-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def add_restricted_org(ctx, **kwargs):
    output_entry(ctx, issuers.add_restricted_organisation(ctx, **kwargs))


@cli.command(name="delete-restricted-org")
@click.argument("client-id", default=None)
@click.argument("restricted-org-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_restricted_org(ctx, **kwargs):
    output_entry(ctx, issuers.delete_restricted_organisation(ctx, **kwargs))


@cli.command(name="replace-restricted-orgs")
@click.argument("client-id", default=None)
@click.option("--restricted-org-id", default=None, multiple=True)
@click.option("--org-id", default=None)
@click.pass_context
def replace_restricted_orgs(ctx, restricted_org_id, **kwargs):
    output_entry(
        ctx,
        issuers.update_client(ctx, restricted_organisations=restricted_org_id, **kwargs),
    )


@cli.command(name="set-attribute-mapping")
@click.argument("client-id", default=None)
@click.argument("attribute-name", default=None)
@click.argument("attribute-path", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def set_attribute_mapping(ctx, client_id, attribute_name, attribute_path, **kwargs):
    result = issuers.set_attribute_mapping(
        ctx,
        client_id,
        attribute_name,
        attribute_path,
        **kwargs,
    )

    print(issuers.format_attributes(ctx, result))


@cli.command(name="delete-attribute-mapping")
@click.argument("client-id", default=None)
@click.argument("attribute-name", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_attribute_mapping(ctx, client_id, attribute_name, **kwargs):
    result = issuers.delete_attribute_mapping(
        ctx,
        client_id,
        attribute_name,
        **kwargs,
    )

    print(issuers.format_attributes(ctx, result))


@cli.command(name="list-managed-upstream-providers")
@click.argument("issuer-id", default=None)
@click.pass_context
def list_managed_upstream_providers(ctx, issuer_id=None, **kwargs):
    issuer = issuers.show(ctx, issuer_id, **kwargs)
    upstreams = issuer.get("managed_upstreams", [])
    table = PrettyTable(["Name", "enabled"])
    table.align = "l"
    for upstream in upstreams:
        table.add_row([upstream["name"], upstream["enabled"]])
    print(table)


@cli.command(name="update-managed-upstream-provider")
@click.argument("issuer-id", default=None)
@click.argument("name", default=None)
@click.option("--prompt-select-account", is_flag=True, default=None)
@click.option("--org-id", default=None)
@click.option("--enabled", type=bool, default=None)
@click.pass_context
def update_managed_upstream_provider(
    ctx, issuer_id=None, name=None, enabled=None, **kwargs
):
    issuer = issuers.update_managed_upstreams(ctx, issuer_id, name, enabled, **kwargs)
    if issuer:
        output_entry(ctx, issuer)


@cli.command(name="list-oidc-upstream-providers")
@click.argument("issuer-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def list_oidc_upstream_providers(ctx, issuer_id=None, **kwargs):
    issuer = issuers.show(ctx, issuer_id, **kwargs)
    upstreams = issuer.get("oidc_upstreams", [])
    table = PrettyTable(
        [
            "name",
            "issuer",
            "icon",
            "client_id",
            "client_secret",
            "issuer_external_host",
            "username_key",
            "user_id_key",
            "email_key",
            "email_verification_required",
            "request_user_info",
            "auto_create_status",
            "prompt_mode",
        ]
    )
    table.align = "l"
    for upstream in upstreams:
        table.add_row(
            [
                upstream["name"],
                upstream["issuer"],
                upstream["icon"],
                upstream["client_id"],
                upstream["client_secret"],
                upstream.get("issuer_external_host"),
                upstream.get("username_key"),
                upstream.get("user_id_key"),
                upstream.get("email_key"),
                upstream.get("email_verification_required"),
                upstream.get("request_user_info"),
                upstream.get("auto_create_status", "---"),
                upstream.get("prompt_mode"),
            ]
        )
    print(table)


@cli.command(name="update-oidc-upstream-provider")
@click.argument("issuer-id", default=None)
@click.argument("name", default=None)
@click.option("--icon", default=None)
@click.option("--issuer", default=None)
@click.option("--client-id", default=None)
@click.option("--client-secret", default=None)
@click.option("--issuer-external_host", default=None)
@click.option("--username-key", default=None)
@click.option("--user-id-key", default=None)
@click.option("--email-key", default=None)
@click.option("--email-verification-required", type=bool, default=None)
@click.option("--request-user-info", type=bool, default=None)
@click.option(
    "--auto-create-status", type=click.Choice(users.STATUS_OPTIONS), default=None
)
@click.option("--org-id", default=None)
@click.option("--prompt-mode", default=None, type=click.Choice(("auto", "disabled")))
@click.option("--oidc-flavor", type=click.Choice(["oidc", "microsoft"]), default="oidc")
@click.option(
    "--client-authorization-type", type=click.Choice(["federated-credential", ""])
)
@click.pass_context
def update_oidc_upstream_provider(
    ctx,
    issuer_id=None,
    name=None,
    icon=None,
    issuer=None,
    client_id=None,
    client_secret=None,
    issuer_external_host=None,
    username_key=None,
    user_id_key=None,
    email_key=None,
    email_verification_required=None,
    request_user_info=None,
    auto_create_status=None,
    prompt_mode=None,
    **kwargs,
):
    issuer = issuers.update_oidc_upstreams(
        ctx,
        issuer_id,
        name,
        icon,
        issuer,
        client_id,
        client_secret,
        issuer_external_host,
        username_key,
        user_id_key,
        email_key,
        email_verification_required,
        request_user_info,
        auto_create_status,
        prompt_mode=prompt_mode,
        **kwargs,
    )
    if issuer:
        output_entry(ctx, issuer)


@cli.command(name="add-oidc-upstream-provider")
@click.argument("issuer-id", default=None)
@click.argument("name", default=None)
@click.option("--issuer", default=None)
@click.option("--icon", default=None)
@click.option("--client-id", default=None)
@click.option("--client-secret", default=None)
@click.option("--issuer-external-host", default=None)
@click.option("--username-key", default=None)
@click.option("--user-id-key", default=None)
@click.option("--email-key", default=None)
@click.option("--email-verification-required", type=bool, default=None)
@click.option("--request-user-info", type=bool, default=None)
@click.option(
    "--auto-create-status", type=click.Choice(users.STATUS_OPTIONS), default=None
)
@click.option("--oidc-flavor", type=click.Choice(["oidc", "microsoft"]), default="oidc")
@click.option("--org-id", type=str, default=None)
@click.pass_context
def add_oidc_upstream_provider(
    ctx,
    issuer_id=None,
    name=None,
    icon=None,
    issuer=None,
    client_id=None,
    client_secret=None,
    issuer_external_host=None,
    username_key=None,
    user_id_key=None,
    email_key=None,
    email_verification_required=None,
    request_user_info=None,
    auto_create_status=None,
    **kwargs,
):
    issuer = issuers.add_oidc_upstreams(
        ctx,
        issuer_id,
        name,
        icon,
        issuer,
        client_id,
        client_secret,
        issuer_external_host,
        username_key,
        user_id_key,
        email_key,
        email_verification_required,
        request_user_info,
        auto_create_status,
        **kwargs,
    )
    if issuer:
        output_entry(ctx, issuer)


@cli.command(name="delete-oidc-upstream-provider")
@click.argument("issuer-id", default=None)
@click.argument("name", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_oidc_upstream_provider(ctx, issuer_id=None, name=None, **kwargs):
    issuers.delete_oidc_upstreams(ctx, issuer_id, name, **kwargs)


@cli.command(name="list-local-auth-upstream-providers")
@click.argument("issuer-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def list_local_auth_upstreams(ctx, issuer_id, **kwargs):
    issuer = issuers.show(ctx, issuer_id, **kwargs)
    upstreams = issuer.get("local_auth_upstreams", [])
    print(issuers.format_local_auth_upstreams(ctx, upstreams))


@cli.command(name="update-local-auth-upstream-provider")
@click.argument("issuer-id", default=None)
@click.argument("name", default=None)
@click.option("--upstream-id", default=None)
@click.option("--icon", default=None)
@click.option("--issuer", default=None)
@click.option(
    "--auto-create-status", type=click.Choice(users.STATUS_OPTIONS), default=None
)
@click.option("--upstream-domain-name", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def update_local_auth_upstream_provider(
    ctx,
    issuer_id,
    name,
    **kwargs,
):
    issuer = issuers.update_local_auth_upstream(
        ctx,
        issuer_id,
        name,
        **kwargs,
    )
    if issuer:
        output_entry(ctx, issuer)


@cli.command(name="add-local-auth-upstream-provider")
@click.argument("issuer-id", default=None)
@click.argument("name", default=None)
@click.option("--upstream-id", default=None)
@click.option("--issuer", default=None)
@click.option("--icon", default=None)
@click.option(
    "--auto-create-status", type=click.Choice(users.STATUS_OPTIONS), default="default"
)
@click.option("--upstream-domain-name", default=None)
@click.option("--org-id", type=str, default=None)
@click.pass_context
def add_local_auth_upstream_provider(
    ctx,
    issuer_id,
    name,
    **kwargs,
):
    issuer = issuers.add_local_auth_upstream(
        ctx,
        issuer_id,
        name,
        **kwargs,
    )

    if issuer:
        output_entry(ctx, issuer)


@cli.command(name="delete-local-auth-upstream-provider")
@click.argument("issuer-id", default=None)
@click.argument("name", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_local_auth_upstream_provider(ctx, issuer_id=None, name=None, **kwargs):
    issuers.delete_local_auth_upstream(ctx, issuer_id, name, **kwargs)


def _format_roles(roles):
    table = PrettyTable(["application", "roles"])
    table.align = "l"
    roles_as_dict = roles.to_dict()
    for k, v in roles_as_dict.items():
        table.add_row([k, v])
    return table


@cli.command(name="list-application-upstream-providers")
@click.argument("issuer-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def list_application_upstreams(ctx, issuer_id, **kwargs):
    issuer = issuers.show(ctx, issuer_id, **kwargs)
    upstreams = issuer.get("application_upstreams", [])
    print(issuers.format_application_upstreams(ctx, upstreams))


@cli.command(name="update-application-upstream-provider")
@click.argument("issuer-id", default=None)
@click.argument("name", default=None)
@click.option("--icon", default=None)
@click.option("--issuer", default=None)
@click.option("--successful-response-code", type=int, default=None)
@click.option("--username-field", default=None)
@click.option("--password-field", default=None)
@click.option("--expected-cookies", multiple=True, default=None)
@click.option("--clear-cookies", is_flag=True, default=None)
@click.option(
    "--auto-create-status", type=click.Choice(users.STATUS_OPTIONS), default=None
)
@click.option("--org-id", default=None)
@click.pass_context
def update_application_upstream_provider(
    ctx,
    issuer_id,
    name,
    **kwargs,
):
    issuer = issuers.update_application_upstream(
        ctx,
        issuer_id,
        name,
        **kwargs,
    )
    if issuer:
        output_entry(ctx, issuer)


@cli.command(name="add-application-upstream-provider")
@click.argument("issuer-id", default=None)
@click.argument("name", default=None)
@click.argument("successful-response-code", type=int, default=None)
@click.option("--issuer", default=None)
@click.option("--icon", default=None)
@click.option("--username-field", default=None)
@click.option("--password-field", default=None)
@click.option("--expected-cookies", multiple=True, default=None)
@click.option(
    "--auto-create-status", type=click.Choice(users.STATUS_OPTIONS), default=None
)
@click.option("--org-id", type=str, default=None)
@click.pass_context
def add_application_upstream_provider(
    ctx,
    issuer_id,
    name,
    successful_response_code,
    **kwargs,
):
    issuer = issuers.add_application_upstream(
        ctx,
        issuer_id,
        name,
        successful_response_code,
        **kwargs,
    )

    if issuer:
        output_entry(ctx, issuer)


@cli.command(name="delete-application-upstream-provider")
@click.argument("issuer-id", default=None)
@click.argument("name", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_application_upstream_provider(ctx, issuer_id=None, name=None, **kwargs):
    issuers.delete_application_upstream(ctx, issuer_id, name, **kwargs)


@cli.command(name="list-elevated-permissions")
@click.option("--user-id", default=None, required=False)
@click.option("--limit", default=25, type=int)
@click.pass_context
def list_elevated_permissions(ctx, user_id=None, **kwargs):
    if user_id is None:
        user_id = tokens.introspect_self(ctx).to_dict().get("sub")
    perms = permissions.query(ctx, user_id=user_id, **kwargs)
    table = PrettyTable(["user_id", "roles"])
    table.align = "l"
    for user_roles in perms:
        table.add_row(
            [
                user_roles.user_id,
                _format_roles(user_roles.roles),
            ]
        )
    print(table)


def _show_elevated_permissions(ctx, user_id, **kwargs):
    perms = permissions.show(ctx, user_id, **kwargs)
    output_entry(ctx, perms.to_dict())


@cli.command(name="show-elevated-permissions")
@click.argument("user-id")
@click.pass_context
def show_elevated_permissions(ctx, user_id, **kwargs):
    _show_elevated_permissions(ctx, user_id, **kwargs)


@cli.command(name="add-elevated-permissions")
@click.argument("user-id")
@click.argument("application")
@click.argument("name")
@click.pass_context
def add_elevated_permissions(ctx, user_id, application, name, **kwargs):
    permissions.add(ctx, user_id, application, name, **kwargs)
    _show_elevated_permissions(ctx, user_id, **kwargs)


@cli.command(name="delete-elevated-permissions")
@click.argument("user-id")
@click.argument("application")
@click.argument("name")
@click.pass_context
def delete_elevated_permissions(ctx, user_id, application, name, **kwargs):
    permissions.delete(ctx, user_id, application, name, **kwargs)
    _show_elevated_permissions(ctx, user_id, **kwargs)


@cli.command(name="clear-elevated-permissions")
@click.argument("user-id")
@click.pass_context
def clear_elevated_permissions(ctx, user_id, **kwargs):
    permissions.clear(ctx, user_id, **kwargs)
    _show_elevated_permissions(ctx, user_id, **kwargs)


@cli.command(name="create-challenge")
@click.argument("user-id")
@click.option("--response-uri")
@click.option("--origin")
@click.option(
    "--challenge-type",
    type=click.Choice(challenges.CHALLENGE_TYPES),
    multiple=True,
)
@click.option("--timeout-seconds", type=int, default=None)
@click.option("--send-now", is_flag=True)
@click.option(
    "--challenge-endpoint",
    type=click.Tuple([str, click.Choice(["web_push", "totp", "webauthn"])]),
    multiple=True,
    help="A pair of strings representing the endpoint id, and endpoint type",
)
@click.option(
    "--answer-data",
    type=click_extension.JSONFile("r"),
    help="a JSON object to return when the challenge is answered",
)
@click.pass_context
def create_challenge(ctx, user_id, challenge_type, origin, **kwargs):
    challenge = challenges.create_challenge(
        ctx, user_id, challenge_types=challenge_type, origin=origin, **kwargs
    )
    output_entry(ctx, challenge.to_dict())


@cli.command(name="get-challenge")
@click.argument("challenge-id")
@click.pass_context
def get_challenge(ctx, challenge_id, **kwargs):
    challenge = challenges.get_challenge(ctx, challenge_id, **kwargs)
    output_entry(ctx, challenge.to_dict())


@cli.command(name="answer-challenge")
@click.argument("challenge-id")
@click.argument("challenge-answer")
@click.argument("allowed", type=bool)
@click.argument("challenge-type", type=click.Choice(challenges.CHALLENGE_TYPES))
@click.option("--user-id")
@click.pass_context
def answer_challenge(
    ctx, challenge_id, challenge_answer, user_id, allowed, challenge_type, **kwargs
):
    challenge = challenges.get_challenge_answer(
        ctx, challenge_id, challenge_answer, user_id, allowed, challenge_type, **kwargs
    )
    output_entry(ctx, challenge.to_dict())


@cli.command(name="delete-challenge")
@click.argument("challenge-id")
@click.pass_context
def delete_challenge(ctx, challenge_id, **kwargs):
    challenges.delete_challenge(ctx, challenge_id, **kwargs)


@cli.command(name="replace-challenge")
@click.argument("challenge-id")
@click.option("--send-now", is_flag=True)
@click.pass_context
def replace_challenge(ctx, challenge_id, **kwargs):
    challenge = challenges.replace_challenge(ctx, challenge_id, **kwargs)
    output_entry(ctx, challenge.to_dict())


@cli.command(name="create-challenge-enrollment")
@click.argument("user-id")
@click.pass_context
def create_challenge_enrollment(ctx, user_id, **kwargs):
    challenge_enrollment = challenges.create_challenge_enrollment(ctx, user_id, **kwargs)
    output_entry(ctx, challenge_enrollment.to_dict())


@cli.command(name="get-challenge-enrollment")
@click.argument("enrollment-id")
@click.option("--user-id")
@click.pass_context
def get_challenge_enrollment(ctx, enrollment_id, **kwargs):
    challenge_enrollment = challenges.get_challenge_enrollment(
        ctx, enrollment_id, **kwargs
    )
    output_entry(ctx, challenge_enrollment.to_dict())


@cli.command(name="delete-challenge-enrollment")
@click.argument("enrollment-id")
@click.option("--user-id")
@click.pass_context
def delete_challenge_enrollment(ctx, enrollment_id, **kwargs):
    challenges.delete_challenge_enrollment(ctx, enrollment_id, **kwargs)


@cli.command(name="update-challenge-enrollment")
@click.argument("enrollment_id")
@click.argument("user-id")
@click.argument("answer")
@click.pass_context
def update_challenge_enrollment(ctx, enrollment_id, user_id, answer, **kwargs):
    result = challenges.update_challenge_enrollment(
        ctx, enrollment_id, user_id, answer, **kwargs
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="list-combined-user-details")
@click.option("--organisation", default=None)
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--email", default=None)
@click.option("--previous-email", default=None)
@click.option("--limit", type=int, default=None)
@click.option("--mfa-enrolled", type=bool, default=None)
@click.option("--auto-created", type=bool, default=None)
@click.option(
    "--status", multiple=True, type=click.Choice(users.STATUS_OPTIONS), default=None
)
@click.option(
    "--search-direction",
    default="forwards",
    type=click.Choice(search_direction_values),
)
@click.option("--prefix-email-search", default="")
@click.option("--first-name", default=None)
@click.option("--last-name", default=None)
@click.option("--search-param", multiple=True, default=None)
@click.option("--allow-partial-match", is_flag=True, default=False)
@click.pass_context
def list_combined_user_details(ctx, organisation, org_id, **kwargs):
    # get all orgs
    kwargs["search_params"] = kwargs.pop("search_param", None)
    org_by_id, org_by_name = orgs.get_org_by_dictionary(ctx, org_id)
    org_id = get_org_id(ctx, org_name=organisation, org_id=org_id)

    results = users.list_combined_user_details(ctx, org_id=org_id, **kwargs)
    print(users.format_combined_user_details_as_text(ctx, results))


@cli.command(name="list-totp-enrollments")
@click.option("--user-id", default=None)
@click.option("--limit", type=int, default=500)
@click.pass_context
def list_totp_enrollments(ctx, **kwargs):
    results = challenges.list_totp_enrollments(ctx, **kwargs)
    print(challenges.format_totp_enrollments(ctx, results))


@cli.command(name="list-webauthn-enrollments")
@click.option("--user-id", default=None, required=False)
@click.option("--limit", type=int, default=500)
@click.pass_context
def list_webauthn_enrollments(ctx, user_id, **kwargs):
    if user_id is None:
        user_id = tokens.introspect_self(ctx).to_dict().get("sub")
    results = challenges.list_webauthn_enrollments(ctx, user_id=user_id, **kwargs)
    print(challenges.format_webauthn_enrollments(ctx, results))


@cli.command(name="get-message-endpoint")
@click.argument("message-endpoint-id")
@click.option("--user-id", default=None)
@click.pass_context
def get_message_endpoint(ctx, **kwargs):
    result = messages.get_message_endpoint(ctx, **kwargs)
    print(result)


@cli.command(name="update-message-endpoint")
@click.argument("message-endpoint-id")
@click.option("--user-id", default=None)
@click.option("--enabled", type=bool, default=None)
@click.pass_context
def update_message_endpoint(ctx, **kwargs):
    result = messages.update_message_endpoint(ctx, **kwargs)
    print(result)


@cli.command(name="list-message-endpoints")
@click.option("--user-id", default=None)
@click.option("--limit", type=int, default=500)
@click.pass_context
def list_message_endpoints(ctx, **kwargs):
    results = messages.list_message_endpoints(ctx, **kwargs)
    print(messages.format_message_endpoints(ctx, results))


@cli.command(name="delete-message-endpoint")
@click.argument("message-endpoint-id")
@click.option("--user-id")
@click.pass_context
def delete_message_endpoint(ctx, message_endpoint_id, **kwargs):
    messages.delete_message_endpoint(ctx, message_endpoint_id, **kwargs)


@cli.command(name="send-message")
@click.option("--text", type=str, required=True)
@click.option("--context", type=str)
@click.option("--user-id", default=None)
@click.option("--org-id", default=None)
@click.option("--message-class", default=None)
@click.option("--message-type", default=None)
@click.option("--sub-header", default=None)
@click.option("--title", default=None)
@click.option("--expiry", type=custom_types.DateTime(), default=None)
@click.option("--approve-uri", default=None)
@click.option("--reject-uri", default=None)
@click.option("--tag", type=str, default=None, help="the tag name of a message")
@click.pass_context
def send_message(ctx, **kwargs):
    messages.send_message(ctx, **kwargs)


@cli.command(name="bulk-delete-messages")
@click.option("--tag", type=str, default=None, help="the tag name of a message")
@click.option("--org-id", default=None)
@click.option("--delete-expired", type=bool, is_flag=True, default=None)
@click.option("--limit", type=int, default=None)
@click.pass_context
def bulk_delete_messages(ctx, **kwargs):
    result = messages.bulk_delete_messages(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-inbox-items")
@click.option("--user-id", default=None)
@click.option("--org-id", default=None)
@click.option("--limit", type=int, default=500)
@click.option("--message-class", default=None)
@click.option("--message-class-list", multiple=True, default=None)
@click.option("--message-type", default=None)
@click.option("--expired", type=bool, default=None)
@click.option("--unread", type=bool, default=None)
@click.pass_context
def list_inbox_items(ctx, **kwargs):
    results = messages.list_inbox_items(ctx, **kwargs)
    print(messages.format_inbox_items_response(ctx, results))


@cli.command(name="update-inbox-item")
@click.option("--user-id", default=None)
@click.option("--inbox-item-id", required=True)
@click.option("--has-been-read", type=bool, default=None)
@click.pass_context
def update_inbox_item(ctx, **kwargs):
    result = messages.update_inbox_item(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-upstream-user-identities")
@click.option("--user-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_upstream_user_identities(ctx, user_id, **kwargs):
    ids = users.list_upstream_user_identities(ctx, user_id, **kwargs)
    table = users.format_upstream_user_identities_as_text(ctx, ids)
    print(table)


@cli.command(name="update-user-identity")
@click.argument("user-id", default=None)
@click.option("--first-name", default=None)
@click.option("--last-name", default=None)
@click.option("--primary-email", default=None)
@click.pass_context
def update_user_identity(ctx, user_id, **kwargs):
    result = users.update_user_identity(ctx, user_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="add-upstream-user-identity")
@click.argument("upstream-user-id")
@click.argument("upstream-idp-id")
@click.option("--user-id", default=None)
@click.pass_context
def add_upstream_user_identity(ctx, user_id, **kwargs):
    """
    Adds an identity to a user. Use this to give a user another method by which
    to log in. The upstream user id should be the id of the user in the upstream.
    This is often some form of unique ID distinct from the user's email address.
    """
    result = users.add_upstream_user_identity(ctx, user_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="update-upstream-user-identity")
@click.argument("upstream-user-identity-id")
@click.option("--upstream-user-id", default=None)
@click.option("--upstream-idp-id", default=None)
@click.option("--user-id", default=None)
@click.pass_context
def update_upstream_user_identity(ctx, upstream_user_identity_id, user_id, **kwargs):
    result = users.update_upstream_user_identity(
        ctx, upstream_user_identity_id, user_id, **kwargs
    )
    output_entry(ctx, result)


@cli.command(name="show-upstream-user-identity")
@click.argument("upstream-user-identity-id")
@click.option("--user-id", default=None)
@click.pass_context
def show_upstream_user_identity(ctx, user_id, upstream_user_identity_id, **kwargs):
    result = users.show_upstream_user_identity(
        ctx, upstream_user_identity_id, user_id, **kwargs
    )
    output_entry(ctx, result)


@cli.command(name="delete-upstream-user-identity")
@click.argument("upstream-user-identity-id")
@click.option("--user-id", default=None)
@click.pass_context
def delete_upstream_user_identity(ctx, user_id, upstream_user_identity_id, **kwargs):
    users.delete_upstream_user_identity(
        ctx, upstream_user_identity_id, user_id, **kwargs
    )


@cli.command(name="list-user-requests")
@click.option("--user-id", default=None)
@click.option("--org-id", default=None)
@click.option("--request-type", default=None)
@click.option("--request-state", default=None)
@click.option("--limit", default=500)
@click.option("--expired", type=bool, default=None)
@click.pass_context
def list_user_requests(ctx, **kwargs):
    ids = users.list_user_requests(ctx, **kwargs)
    table = users.format_user_requests_as_text(ctx, ids)
    print(table)


@cli.command(name="add-user-request")
@click.argument("user-id")
@click.argument("org-id")
@click.argument("requested-resource")
@click.argument(
    "requested-resource-type",
    type=resources.permissioned_resource_type_enum,
)
@click.option("--request-information", default=None)
@click.option("--requested-sub-resource", type=str, default=None)
@click.option("--expiry-date", type=custom_types.DateTime(), default=None)
@click.option("--from-date", type=custom_types.DateTime(), default=None)
@click.option("--to-date", type=custom_types.DateTime(), default=None)
@click.pass_context
def add_user_request(
    ctx, user_id, org_id, requested_resource, requested_resource_type, **kwargs
):
    result = users.add_user_request(
        ctx, user_id, org_id, requested_resource, requested_resource_type, **kwargs
    )
    output_entry(ctx, result)


@cli.command(name="update-user-request")
@click.argument("user-request-id")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--requested-resource", default=None)
@click.option("--requested-sub-resource", type=str, default=None)
@click.option(
    "--requested-resource-type",
    type=resources.permissioned_resource_type_enum,
    default=None,
)
@click.option("--request-information", default=None)
@click.option("--response-information", default=None)
@click.pass_context
def update_user_request(ctx, user_request_id, **kwargs):
    result = users.update_user_request(ctx, user_request_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="action-user-request")
@click.argument("user-request-id")
@click.argument("state", type=click.Choice(["approved", "declined"]))
@click.option("--org-id", default=None)
@click.option("--requested-resource", default=None)
@click.option(
    "--requested-resource-type",
    type=resources.permissioned_resource_type_enum,
    default=None,
)
@click.option("--request-information", default=None)
@click.pass_context
def action_user_request(ctx, user_request_id, state, **kwargs):
    result = users.action_user_request(ctx, user_request_id, state, **kwargs)
    output_entry(ctx, result)


@cli.command(name="bulk-action-user-request")
@click.option("--user-id", default=None, required=True)
@click.option("--org-id", default=None)
@click.option("--state", default=None, type=click.Choice(["approved", "declined"]))
@click.option("--user-status", default=None, type=click.Choice(users.STATUS_OPTIONS))
@click.option("--reset-user", type=bool, default=False)
@click.pass_context
def bulk_action_user_request(ctx, user_id, state, **kwargs):
    result = users.bulk_action_user_request(ctx, user_id, state, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-user-request")
@click.argument("user-request-id")
@click.option("--user-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def show_user_request(ctx, user_request_id, **kwargs):
    result = users.show_user_request(ctx, user_request_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-user-request")
@click.argument("user-request-id")
@click.option("--user-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_user_request(ctx, user_request_id, **kwargs):
    users.delete_user_request(ctx, user_request_id, **kwargs)


@cli.command(name="list-access-requests")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--request-type", default=None)
@click.option("--request-state", default=None)
@click.option("--limit", default=500)
@click.option("--email", default=None)
@click.option(
    "--search-direction",
    default="forwards",
    type=click.Choice(search_direction_values),
)
@click.pass_context
def list_access_requests(ctx, org_id, **kwargs):
    requests_list = users.list_access_requests(ctx, org_id, **kwargs)
    table = PrettyTable(
        [
            "id",
            "email",
            "org_id",
            "user_status",
            "user_requests",
        ]
    )
    for entry in requests_list:
        table.add_row(
            [
                entry.metadata.id,
                entry.status.user.email,
                entry.status.user.org_id,
                entry.status.user.status,
                entry.status.user_requests,
            ]
        )
    table.align = "l"
    print(table)


@cli.command(name="version")
@click.pass_context
def version(ctx):
    print(__version__)


@cli.command(name="upload-upstream-user-identity-list")
@click.argument("org-id")
@click.argument("upstream-user-idp-id")
@click.argument("email-to-id-mapping")
@click.pass_context
def upload_upstream_user_identity_list(
    ctx, org_id, upstream_user_idp_id, email_to_id_mapping
):
    """
    Updates the upstream identity for many users. This command takes a csv file as
    input as the email-to-id-mapping argument. If the argument is '-', the file will
    be read from stdin. The file must be csv formatted, containing a mapping between
    email address and upstream user id. The file must start with a header with
    "email" and "upstream_user_id" for the two columns.

    Example:

    "email","upstream_user_id"

    "foo@example.com","1234-4567"

    "bar@example.com","5023-1235"
    """
    users.upload_upstream_user_identity_list(
        ctx, org_id, upstream_user_idp_id, email_to_id_mapping
    )


@cli.command(
    name="list-user-application-access-info",
    help="list a user's application access info",
)
@click.option("--user", default=None)
@click.option("--org-id", default=None)
@click.option("--resource-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_user_application_access_info(ctx, user, org_id, **kwargs):
    user_id = user_id_or_id_from_email(ctx, user_id_or_email=user, org_id=org_id)
    info = users.list_user_application_access_info(ctx, user_id, org_id=org_id, **kwargs)
    table = users.format_user_application_access_info_as_text(ctx, info)
    print(table)


@cli.command(name="list-user-fileshare-access-info")
@click.option("--user", default=None)
@click.option("--org-id", default=None)
@click.option("--resource-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_user_fileshare_access_info(ctx, user, org_id, **kwargs):
    user_id = user_id_or_id_from_email(ctx, user_id_or_email=user, org_id=org_id)
    info = users.list_user_fileshare_access_info(ctx, user_id, org_id=org_id, **kwargs)
    table = users.format_user_fileshare_access_info_as_text(ctx, info)
    print(table)


@cli.command(name="list-user-desktop-access-info")
@click.option("--user", default=None)
@click.option("--org-id", default=None)
@click.option("--desktop-type", default=None)
@click.option("--resource-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_user_desktop_access_info(ctx, user, org_id, **kwargs):
    user_id = user_id_or_id_from_email(ctx, user_id_or_email=user, org_id=org_id)
    info = users.list_user_desktop_access_info(ctx, user_id, org_id=org_id, **kwargs)
    table = users.format_user_desktop_access_info_as_text(ctx, info)
    print(table)


@cli.command(name="list-user-resource-access-info")
@click.option("--user", default=None)
@click.option("--org-id", default=None)
@click.option("--resource-id", default=None)
@click.option("--include_all_resource_type", type=bool, default=True)
@click.option(
    "--resource-type",
    default=None,
    type=click.Choice(
        ["application", "application_service", "fileshare", "desktop", "database"]
    ),
)
@click.option("--limit", default=500)
@click.pass_context
def list_user_resource_access_info(ctx, user, org_id, **kwargs):
    user_id = user_id_or_id_from_email(ctx, user_id_or_email=user, org_id=org_id)
    info = users.list_user_resource_access_info(ctx, user_id, org_id=org_id, **kwargs)
    table = users.format_user_resource_access_info_as_text(ctx, info)
    print(table)


@cli.command(name="list-application-summaries")
@click.option("--org-id", default=None)
@click.option("--assigned-org-id", multiple=True, default=None)
@click.option("--resource-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_application_summaries(ctx, org_id, assigned_org_id, **kwargs):
    summaries = apps.list_application_summaries(
        ctx, org_id=org_id, assigned_org_ids=assigned_org_id, **kwargs
    )
    table = apps.format_application_summaries_as_text(ctx, summaries)
    print(table)


@cli.command(name="list-auth-policies")
@click.option("--org-id", default=None)
@click.option("--issuer-id", default=None)
@click.option("--policy-name", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_auth_policies(ctx, **kwargs):
    pop_item_if_none(kwargs)
    policies = issuers.list_auth_policies(ctx, **kwargs)
    print(issuers.format_policy_table(ctx, policies))


@cli.command(name="list-auth-policy-rules")
@click.option("--org-id", default=None)
@click.option("--limit", default=500)
@click.option("--policy-name", default=None)
@click.pass_context
def list_auth_policy_rules(ctx, **kwargs):
    pop_item_if_none(kwargs)
    policies = issuers.list_auth_policies(ctx, **kwargs)
    print("Policy Rules")
    print(issuers.format_policy_rules_table(ctx, policies))
    print("Policy Groups")
    print(issuers.format_policy_groups_table(ctx, policies))


@cli.command(name="add-auth-policy")
@click.argument("issuer_id")
@click.argument(
    "default-action",
    type=click.Choice(
        ["do_mfa", "authenticate", "deny_login", "allow_login", "dont_mfa"]
    ),
)
@click.argument(
    "supported-mfa-methods",
    type=click.Choice(["web_push", "totp", "webauthn"]),
    nargs=-1,
)
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.pass_context
def add_auth_policy(ctx, issuer_id, default_action, supported_mfa_methods, **kwargs):
    pop_item_if_none(kwargs)
    result = issuers.add_auth_policy(
        ctx, issuer_id, default_action, supported_mfa_methods, **kwargs
    )
    output_entry(ctx, result)


@cli.command(name="set-issuer-auth-policy-to-default")
@click.argument("issuer-id")
@click.option("--org-id", default=None)
@click.pass_context
def reset_auth_policy(ctx, issuer_id, **kwargs):
    result = issuers.reset_auth_policy(ctx, issuer_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="update-auth-policy")
@click.argument("policy-id")
@click.option(
    "--default-action",
    type=click.Choice(
        ["do_mfa", "authenticate", "deny_login", "allow_login", "dont_mfa"]
    ),
)
@click.option("--issuer-id", default=None)
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.option(
    "--supported-mfa-methods",
    type=click.Choice(["web_push", "totp", "webauthn"]),
    multiple=True,
)
@click.pass_context
def update_auth_policy(ctx, policy_id, **kwargs):
    pop_item_if_none(kwargs)
    result = issuers.update_auth_policy(ctx, policy_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-auth-policy")
@click.argument("policy-id")
@click.option("--org-id", default=None)
@click.option("--formatted", default=None, is_flag=True)
@click.pass_context
def get_auth_policy(ctx, policy_id, formatted, **kwargs):
    result = issuers.get_auth_policy(ctx, policy_id, formatted, **kwargs)
    if not formatted:
        output_entry(ctx, result)
    else:
        print(result)


@cli.command(name="delete-auth-policy")
@click.argument("policy-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_auth_policy(ctx, policy_id, **kwargs):
    issuers.delete_auth_policy(ctx, policy_id, **kwargs)


@cli.command(name="add-auth-policy-rule")
@click.argument("policy-id")
@click.argument("action")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def add_auth_policy_rule(ctx, policy_id, action, **kwargs):
    pop_item_if_none(kwargs)
    result = issuers.add_auth_policy_rule(ctx, policy_id, action, **kwargs)
    output_entry(ctx, result)


@cli.command(name="update-auth-policy-rule")
@click.argument("policy-id")
@click.argument("policy-rule-id")
@click.option("--action")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def update_auth_policy_rule(ctx, policy_id, policy_rule_id, **kwargs):
    pop_item_if_none(kwargs)
    result = issuers.update_auth_policy_rule(ctx, policy_id, policy_rule_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="set-auth-policy")
@click.argument("issuer-id")
@click.option(
    "--policy-data",
    default=None,
    help="A json formatted string that contains a policy spec.",
)
@click.option(
    "--policy-file",
    default=None,
    help="A json file that contains a policy spec.",
    type=click_extension.JSONFile("r"),
)
@click.option("--org-id", default=None)
@click.pass_context
def set_auth_policy(ctx, issuer_id, policy_data, policy_file, org_id, **kwargs):
    if policy_file:
        if policy_data:
            print("only specify policy data or policy spec")
        else:
            policy = policy_file
    else:
        policy = json.loads(policy_data)

    result = issuers.set_auth_policy(ctx, issuer_id, policy, org_id, **kwargs)
    output_entry(ctx, result)


def convert_condition_value(value_type, value):
    if value_type == "bool":
        str_val = value[0]
        if str_val.lower() == "true":
            return json.dumps(True)
        elif str_val.lower() == "false":
            return json.dumps(False)
        raise ValueError
    if value_type == "int":
        return json.dumps(int(value[0]))
    if value_type == "str":
        return json.dumps(str(value[0]))
    if value_type == "list":
        return json.dumps(list(value))
    raise ValueError(f"value_type {value_type} not known")


@cli.command(name="add-auth-policy-conditions")
@click.argument("policy-id")
@click.argument("policy-rule-id")
@click.argument("condition-type")
@click.argument(
    "condition-value-type", type=click.Choice(["bool", "int", "str", "list"])
)
@click.argument("condition-value", nargs=-1)
@click.option("--operator", default=None)
@click.option("--field", default=None)
@click.option("--input-is-list", default=None, type=bool)
@click.option("--org-id", default=None)
@click.pass_context
def add_auth_policy_condition(
    ctx,
    policy_id,
    policy_rule_id,
    condition_type,
    condition_value_type,
    condition_value,
    **kwargs,
):
    value = convert_condition_value(condition_value_type, condition_value)
    result = issuers.add_auth_policy_condition(
        ctx, policy_id, policy_rule_id, condition_type, value=value, **kwargs
    )
    output_entry(ctx, result)


@cli.command(name="delete-auth-policy-conditions")
@click.argument("policy-id")
@click.argument("policy-rule-id")
@click.argument("condition-type")
@click.option("--org-id", default=None)
@click.pass_context
def delete_auth_policy_condition(ctx, policy_id, policy_rule_id, **kwargs):
    issuers.delete_auth_policy_condition(ctx, policy_id, policy_rule_id, **kwargs)


@cli.command(name="show-auth-policy-rule")
@click.argument("policy-id")
@click.argument("policy-rule-id")
@click.pass_context
def get_auth_policy_rule(ctx, policy_id, policy_rule_id, **kwargs):
    result = issuers.get_auth_policy_rule(ctx, policy_id, policy_rule_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-auth-policy-rule")
@click.argument("policy-id")
@click.argument("policy-rule-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_auth_policy_rule(ctx, policy_id, policy_rule_id, **kwargs):
    issuers.delete_auth_policy_rule(ctx, policy_id, policy_rule_id, **kwargs)


@cli.command(name="add-auth-policy-group")
@click.argument("policy-id")
@click.option("--name")
@click.option("--rule-id", multiple=True, default=[])
@click.option("--org-id", default=None)
@click.option(
    "--insertion-index",
    type=int,
    help="""The index to insert this group at.
         If not set the group will be added to the end""",
    default=None,
)
@click.pass_context
def add_auth_policy_group(
    ctx,
    policy_id,
    **kwargs,
):
    kwargs["rule_ids"] = kwargs.pop("rule_id", [])
    result = issuers.add_auth_policy_group(ctx, policy_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-auth-policy-group")
@click.argument("policy-id")
@click.argument("policy-group-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_auth_policy_group(ctx, policy_id, policy_group_id, **kwargs):
    issuers.delete_auth_policy_group(ctx, policy_id, policy_group_id, **kwargs)


@cli.command(name="list-user-metadata")
@click.option("--user-id", default=None)
@click.option("--org-id", default=None)
@click.option("--data-type", default=None)
@click.option("--app-id", default=None)
@click.option("--recursive", default=None, type=bool)
@click.option("--limit", default=500)
@click.pass_context
def list_user_metadata(ctx, **kwargs):
    ids = users.list_user_metadata(ctx, **kwargs)
    table = users.format_user_metadata_as_text(ctx, ids)
    print(table)


@cli.command(name="add-user-metadata")
@click.argument("user-id")
@click.argument("org-id")
@click.argument(
    "data-type",
    type=click.Choice(
        ["mfa_enrollment_expiry", "user_app_data", "user_org_data", "json"]
    ),
)
@click.argument("data")
@click.option(
    "--app-id",
    default=None,
    help="excluding the app_id will be interpretted as an organisation level metadata setting",  # noqa
)
@click.option("--name", default=None)
@click.pass_context
def add_user_metadata(ctx, user_id, org_id, data_type, data, **kwargs):
    result = users.add_user_metadata(ctx, user_id, org_id, data_type, data, **kwargs)
    output_entry(ctx, result)


@cli.command(name="update-user-metadata")
@click.argument("user-metadata-id")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option(
    "--data_type",
    type=click.Choice(
        ["mfa_enrollment_expiry", "user_app_data", "user_org_data", "json"]
    ),
)
@click.option("--data")
@click.option("--app-id", default=None)
@click.option("--name", default=None)
@click.pass_context
def update_user_metadata(ctx, user_metadata_id, **kwargs):
    result = users.update_user_metadata(ctx, user_metadata_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-user-metadata")
@click.argument("user-metadata-id")
@click.option("--user-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def show_user_metadata(ctx, user_metadata_id, **kwargs):
    result = users.show_user_metadata(ctx, user_metadata_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-user-metadata")
@click.argument("user-metadata-id")
@click.option("--user-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_user_metadata(ctx, user_metadata_id, **kwargs):
    users.delete_user_metadata(ctx, user_metadata_id, **kwargs)


@cli.command(name="bulk-set-metadata")
@click.argument("org-id")
@click.argument(
    "data-type",
    type=click.Choice(
        ["mfa_enrollment_expiry", "user_app_data", "user_org_data", "json"]
    ),
)
@click.argument("data")
@click.option("--app-id", default=None)
@click.option("--name", default=None)
@click.pass_context
def bulk_set_user_metadata(ctx, org_id, data_type, data, **kwargs):
    users.bulk_set_user_metadata(ctx, org_id, data_type, data, **kwargs)


@cli.command(name="list-secure-agent")
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_secure_agents(ctx, **kwargs):
    ids = apps.list_secure_agents(ctx, **kwargs)
    table = apps.format_secure_agent_as_text(ctx, ids)
    print(table)


@cli.command(name="add-secure-agent")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--application-service-ids", multiple=True, default=None)
@click.pass_context
def add_secure_agent(ctx, **kwargs):
    result = apps.add_secure_agent(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(name="set-connector-to-agent")
@click.argument("agent-id")
@click.option("--connection-uri", default=None)
@click.option("--org-id", default=None)
@click.option("--max_number_connections", type=int, default=None)
@click.pass_context
def set_connector_to_agent(ctx, agent_id, connection_uri, **kwargs):
    # This is temporary until we have other ways of referencing connectors
    if not connection_uri:
        print("connection_uri required")
        return
    result = apps.set_connector_to_agent(ctx, agent_id, connection_uri, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-connector-from-agent")
@click.argument("agent-id")
@click.option("--connection-uri", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def delete_connector_from_agent(ctx, agent_id, connection_uri, **kwargs):
    # This is temporary until we have other ways of referencing connectors
    if not connection_uri:
        print("connection_uri required")
        return
    result = apps.delete_connector_from_agent(ctx, agent_id, connection_uri, **kwargs)
    output_entry(ctx, result)


@cli.command(name="update-secure-agent")
@click.argument("secure-agent-id")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--application_service_ids", multiple=True, default=None)
@click.pass_context
def update_secure_agent(ctx, secure_agent_id, **kwargs):
    result = apps.update_secure_agent(ctx, secure_agent_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-secure-agent")
@click.argument("secure-agent-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_secure_agent(ctx, secure_agent_id, **kwargs):
    result = apps.show_secure_agent(ctx, secure_agent_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-secure-agent")
@click.argument("secure-agent-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_secure_agent(ctx, secure_agent_id, **kwargs):
    apps.delete_secure_agent(ctx, secure_agent_id, **kwargs)


@cli.command(name="list-authentication-documents")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_authentication_documents(ctx, **kwargs):
    ids = tokens.list_authentication_documents(ctx, **kwargs)
    table = tokens.format_authentication_document_as_text(ctx, ids)
    print(table)


@cli.command(name="add-authentication-document")
@click.option("--org-id", default=None)
@click.option("--user-id", required=True)
@click.option("--auth-issuer-url", required=True)
@click.option("--expiry", default=None)
@click.option("--outfile", default=None)
@click.pass_context
def add_authentication_document(ctx, outfile, **kwargs):
    result = tokens.add_authentication_document(ctx, **kwargs)
    if outfile:
        output_json_to_file(ctx, result, outfile)
    else:
        output_entry(ctx, result)


@cli.command(name="show-authentication-document")
@click.argument("document-id")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.pass_context
def show_authentication_document(ctx, document_id, **kwargs):
    result = tokens.show_authentication_document(ctx, document_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-authentication-document")
@click.argument("document-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_authentication_document(ctx, document_id, **kwargs):
    tokens.delete_authentication_document(ctx, document_id, **kwargs)


@cli.command(name="validate-identity-assertion")
@click.argument("document-id")
@click.argument("token", default=None)
@click.pass_context
def validate_identity_assertion(ctx, document_id, token, **kwargs):
    result = tokens.validate_identity_assertion(ctx, document_id, token, **kwargs)
    output_entry(ctx, result)


@cli.command(name="list-service-accounts")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_service_accounts(ctx, **kwargs):
    ids = users.list_service_accounts(ctx, **kwargs)
    table = users.format_service_account_as_text(ctx, ids)
    print(table)


@cli.command(name="add-service-account")
@click.argument("org-id")
@click.argument("name")
@click.option("--enabled/--disabled", default=None)
@click.option("--allowed_sub_org", multiple=True, default=None)
@click.option("--description", type=str, default=None)
@click.pass_context
def add_service_account(ctx, org_id, name, **kwargs):
    kwargs["allowed_sub_orgs"] = kwargs.pop("allowed_sub_org", [])
    result = users.add_service_account(ctx, org_id, name, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-service-account")
@click.argument("service-account-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_service_account(ctx, service_account_id, **kwargs):
    result = users.show_service_account(ctx, service_account_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-service-account")
@click.argument("service-account-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_service_account(ctx, service_account_id, **kwargs):
    users.delete_service_account(ctx, service_account_id, **kwargs)


@cli.command(name="update-service-account")
@click.argument("service-account-id")
@click.option("--name", default=None)
@click.option("--enabled/--disabled", default=None)
@click.option("--allowed_sub_org", multiple=True, default=None)
@click.option("--description", type=str, default=None)
@click.option("--org-id", type=str, default=None)
@click.pass_context
def update_service_account(ctx, service_account_id, **kwargs):
    kwargs["allowed_sub_orgs"] = kwargs.pop("allowed_sub_org", None)
    users.update_service_account(ctx, service_account_id, **kwargs)


@cli.command(name="add-api-key")
@click.option("--duration-seconds", type=int, default=None)
@click.option("--scope", type=str, multiple=True)
@click.option("--user-id", type=str, default=None)
@click.option("--session", type=str, default=None)
@click.option("--org-id", type=str, default=None)
@click.option("--label", type=str, default=None)
@click.option("--name", type=str, default=None)
@click.pass_context
def add_api_key(ctx, duration_seconds, scope, **kwargs):
    api_key = tokens.add_api_key(ctx, duration=duration_seconds, scopes=scope, **kwargs)
    output_entry(ctx, api_key.to_dict())


@cli.command(name="delete-api-key")
@click.argument("api_key_id")
@click.option("--user-id", type=str, default=None)
@click.pass_context
def delete_api_key(ctx, api_key_id, **kwargs):
    tokens.delete_api_key(ctx, api_key_id, **kwargs)


@cli.command(name="get-api-key")
@click.argument("api_key_id")
@click.option("--user-id", type=str, default=None)
@click.option("--org-id", type=str, default=None)
@click.pass_context
def get_api_key(ctx, api_key_id, **kwargs):
    api_key = tokens.get_api_key(ctx, api_key_id, **kwargs)
    output_entry(ctx, api_key.to_dict())


@cli.command(name="replace-api-key")
@click.argument("api_key_id")
@click.option("--user-id", type=str, default=None)
@click.option("--org-id", type=str, default=None)
@click.option("--expiry", type=click.DateTime(), default=None)
@click.pass_context
def replace_api_key(ctx, api_key_id, **kwargs):
    api_key = tokens.replace_api_key(ctx, api_key_id, **kwargs)
    output_entry(ctx, api_key.to_dict())


@cli.command(name="list-api-keys")
@click.option("--user-id", type=str, default=None)
@click.option("--org-id", type=str, default=None)
@click.option("--org-id", type=str, default=None)
@click.option("--label", type=str, default=None)
@click.option("--limit", type=int, default=None)
@click.option("--scope", multiple=True, default=None)
@click.option("--valid-at", type=str, default=None)
@click.option("--sort-order", type=click.Choice(sort_order_values), default=None)
@click.option("--next-created-date", type=str, default=None)
@click.option(
    "--search-direction", type=click.Choice(search_direction_values), default=None
)
@click.option(
    "--oper-status",
    type=click.Choice(tokens.api_key_oper_statuses),
    multiple=True,
    default=None,
)
@click.option(
    "--not-oper-status",
    type=click.Choice(tokens.api_key_oper_statuses),
    multiple=True,
    default=None,
)
@click.pass_context
def list_api_keys(ctx, scope, **kwargs):
    api_keys_resp = tokens.list_api_keys(ctx, scopes=list(scope), **kwargs)
    if context.output_json(ctx):
        output_formatted(ctx, api_keys_resp.to_dict())
        return

    table = tokens.format_api_keys_as_text(ctx, api_keys_resp.api_keys)
    print(table)

    if api_keys_resp.page_at_created_date is not None:
        del api_keys_resp["api_keys"]
        page_details = api_keys_resp.to_dict()
        output_entry(ctx, page_details)


@cli.command(name="clean-api-keys")
@click.option("--user-id", type=str, default=None)
@click.option("--org-id", type=str, default=None)
@click.option("--expires-at", type=custom_types.DateTime(), default=None)
@click.option("--no-expiry", is_flag=True, default=None)
@click.option("--older-than", type=custom_types.DateTime(), default=None)
@click.pass_context
def clear_api_keys(ctx, **kwargs):
    api_keys = tokens.clean_api_keys(ctx, **kwargs)
    if context.output_json(ctx):
        output_formatted(ctx, api_keys)
        return

    table = tokens.format_api_keys_as_text(ctx, api_keys)
    print(table)


@cli.command(name="show-api-key-introspection")
@click.argument("email")
@click.argument("api_key")
@click.option("--include_suborgs", default=False, type=bool)
@click.option("--support-http-matchers", default=True, type=bool)
@click.pass_context
def show_api_key_introspection(ctx, email, api_key, include_suborgs=False, **kwargs):
    result = tokens.get_api_key_introspect(
        ctx, email, api_key, include_suborgs=include_suborgs, **kwargs
    )
    output_entry(ctx, result.to_dict())


@cli.command(help="list all connectors")
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.option("--limit", default=None)
@click.option("--show-stats", type=bool, default=True)
@click.option("--no-down", is_flag=True, type=bool, default=False)
@click.option("--page-at-id", default=None)
@click.option("--page-size", default=500, type=int)
@click.option("--filter-os-version", default=None)
@click.option(
    "--sort-by",
    type=click.Choice(["metadata.created", "status.operational_status.status"]),
    multiple=True,
    default=None,
)
@click.option(
    "--not-version",
    default=None,
    help="show connectors that are not running the specified version",
)
@click.option(
    "--only-version",
    default=None,
    help="show connectors that are running the specified version",
)
@click.pass_context
def list_connectors(ctx, **kwargs):
    results = connectors.query(ctx, **kwargs)
    table = connectors.format_connectors_as_text(
        ctx, results, skip_sub_table=False, **kwargs
    )
    print(table)


@cli.command(name="show-connector")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_connector(ctx, **kwargs):
    result = connectors.get(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="update-connector")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.option(
    "--admin-status",
    default=None,
    type=click.Choice(["active", "disabled", "testing", "deleted"]),
)
@click.option(
    "--trap-disabled",
    default=None,
    type=bool,
)
@click.pass_context
def update_connector(ctx, **kwargs):
    result = connectors.update(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="configure-connector-stats-publishing")
@click.option("--org-id", default=None)
@click.option(
    "--connector-id",
    type=str,
    multiple=True,
    required=True,
    help="list of connectors to configure",
)
@click.option(
    "--publish-period-s", type=int, default=30, help="how frequently to publish"
)
@click.option("--net-summary-duration-s", type=int, default=None)
@click.option("--http-summary-duration-s", type=int, default=None)
@click.option("--net-detailed-duration-s", type=int, default=None)
@click.option("--http-detailed-duration-s", type=int, default=None)
@click.option("--share-summary-duration-s", type=int, default=None)
@click.option("--share-detailed-duration-s", type=int, default=None)
@click.pass_context
def configure_connector_stats_publishing(ctx, **kwargs):
    result = connectors.configure_stats_publishing(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-connector-transfers")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_connector_transfers(ctx, *args, **kwargs):
    results = transfers.query_connector(ctx, *args, **kwargs)
    table = transfers.format(ctx, results)
    print(table)


@cli.command(name="new-connector-transfer")
@click.argument("connector-id")
@click.pass_context
def new__connector_transfer(ctx, *args, **kwargs):
    result = transfers.new_transfer(ctx, *args, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-agent-connector-instance")
@click.argument("connector-id")
@click.argument("connector_instance_id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_agent_connector_instance(ctx, **kwargs):
    connectors.delete_agent_connector_instance(ctx, **kwargs)


@cli.command(name="list-agent-connectors")
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.option("--limit", default=500)
@click.option(
    "--column-format", default="newformat", type=click.Choice(["oldformat", "newformat"])
)
@click.option("--filter-not-has-version", default=None)
@click.option("--output-msfriendly", is_flag=True, default=False)
@click.option(
    "--sort-by",
    type=click.Choice(["version", "status", "uptime", "org", "last_seen", "os_version"]),
    default="version",
)
@click.option("--reverse-sort", is_flag=True, default=False)
@click.option("--page-at-id", default=None)
@click.option("--show-stats", default=None, type=bool)
@click.pass_context
def list_agent_connectors(
    ctx, output_msfriendly=False, sort_by=None, reverse_sort=False, **kwargs
):
    results = connectors.query_agents(ctx, **kwargs)
    table = connectors.format_agents_as_text(ctx, results, **kwargs)
    if output_msfriendly:
        table.set_style(TableStyle.MSWORD_FRIENDLY)
    if sort_by is not None and ctx.obj["output_format"] != "json":
        print(table.get_string(sortby=sort_by, reversesort=reverse_sort))
    else:
        print(table)


@cli.command(name="list-connector-instances")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.pass_context
def list_agent_connectors_instances(
    ctx,
    **kwargs,
):
    results = connectors.query_agent_instances(ctx, **kwargs)
    table = connectors.format_agent_instances(ctx, results, **kwargs)
    print(table)


@cli.command(name="show-connector-instance")
@click.argument("connector-id")
@click.argument("connector-instance-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_connector_instance(
    ctx,
    *args,
    **kwargs,
):
    result = connectors.get_instance(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="add-agent-connector")
@click.argument("name")
@click.option("--org-id", default=None)
@click.option("--connection-uri", default=None)
@click.option("--max_number-connections", type=int, default=None)
@click.option("--point-of-presence-tag", multiple=True, default=None)
@click.option("--service-account-required", default=True, is_flag=True)
@click.option(
    "--local-authentication-enabled/--local-authentication-disabled", default=None
)
@click.option(
    "--proxy-tunnel-termination",
    default=None,
    type=click.Choice(connectors.TUNNEL_TERMINATION_TYPES),
)
@click.pass_context
def add_agent_connector(ctx, **kwargs):
    result = connectors.add_agent(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(
    name="add-agent-connector-local-bind",
    help="""
Adds a local bind to the agent so that it can serve local content without needing to
proxy through the Agilicus cloud.
""",
)
@click.argument("connector-id")
@click.option(
    "--bind-host", default=None, help="An IP or hostname. Leave empty for all."
)
@click.option("--bind-port", type=int, required=True)
@click.option("--org-id", default=None)
@click.option("--revocation-proxy", is_flag=True, default=False)
@click.pass_context
def add_agent_connector_local_bind(ctx, **kwargs):
    result = connectors.add_agent_local_bind(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-agent-connector-local-bind")
@click.argument("connector-id")
@click.option("--bind-host", default=None)
@click.option("--bind-port", type=int)
@click.option("--org-id", default=None)
@click.option("--revocation-proxy", is_flag=True, default=False)
@click.pass_context
def delete_agent_connector_local_bind(ctx, **kwargs):
    result = connectors.delete_agent_local_bind(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(
    name="add-agent-connector-egress-gateway",
    help="""
Adds a local bind to the agent so that it can serve as an egress gateway to another
connector.
""",
)
@click.argument("connector-id")
@click.option(
    "--bind-host", default=None, help="An IP or hostname. Leave empty for all."
)
@click.option("--bind-port", type=int, required=True)
@click.option("--org-id", default=None)
@click.pass_context
def add_agent_connector_egress_gateway(ctx, **kwargs):
    result = connectors.add_agent_egress_gateway(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-agent-connector-egress-gateway")
@click.argument("connector-id")
@click.option("--bind-host", default=None)
@click.option("--bind-port", type=int)
@click.option("--org-id", default=None)
@click.pass_context
def delete_agent_connector_egress_gateway(ctx, **kwargs):
    result = connectors.delete_agent_egress_gateway(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-agent-connector")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_agent_connector(ctx, connector_id, **kwargs):
    result = connectors.get_agent(ctx, connector_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-agent-connector-info")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.option("--allow-list", is_flag=True, default=True)
@click.option("--service-forwarders", is_flag=True, default=True)
@click.option("--authz-public-key", is_flag=True, default=True)
@click.option("--instance-id", default=None)
@click.pass_context
def show_agent_connector_info(ctx, connector_id, **kwargs):
    result = connectors.get_agent_info(ctx, connector_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="update-agent-connector")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.option("--connection-uri", default=None)
@click.option("--max-number-connections", type=int, default=None)
@click.option("--name-slug", type=str, default=None)
@click.option("--point-of-presence-tag", multiple=True, default=None)
@click.option("--clear-point-of-presence-tags", is_flag=True, default=False)
@click.option("--service-account-required/--service-account-not-required", default=True)
@click.option(
    "--local-authentication-enabled/--local-authentication-disabled", default=None
)
@click.option(
    "--proxy-tunnel-termination",
    default=None,
    type=click.Choice(connectors.TUNNEL_TERMINATION_TYPES),
)
@click.option(
    "--dynamic-routes-enabled",
    default=None,
    type=custom_types.TernaryParamType(),
)
@click.option(
    "--on-demand-routes-enabled",
    default=None,
    type=custom_types.TernaryParamType(),
)
@click.option("--admin-status", default=None)
@click.option("--revocation-proxy-trusted-cert-bundle-id", default=None)
@click.option("--revocation-proxy-rules-bundle-id", default=None)
@click.option(
    "--trap-disabled",
    default=None,
    type=bool,
)
@click.pass_context
def update_agent_connector(ctx, connector_id, **kwargs):
    result = connectors.replace_agent(ctx, connector_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="update-agent-connector-auth-info")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.option("--local-authentication-public-key", default=None)
@click.pass_context
def update_agent_connector_auth_info(ctx, connector_id, **kwargs):
    result = connectors.replace_agent_auth_info(ctx, connector_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-agent-connector")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_agent_connector(ctx, connector_id, **kwargs):
    connectors.delete_agent(ctx, connector_id, **kwargs)


@cli.command(name="set-agent-connector-stats")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.option(
    "--overall-status",
    type=click.Choice(["good", "warn", "down", "stale"]),
    required=True,
)
@click.option("--os-version", default=None, type=SubObjectString("system"))
@click.option("--os-uptime", default=None, type=SubObjectInt("system"))
@click.option("--agent-uptime", default=0, type=SubObjectInt("system"))
@click.option("--agent-version", default="", type=SubObjectString("system"))
@click.option("--active-connections", default=0, type=SubObjectInt("transport"))
@click.option("--target-number-connections", default=0, type=SubObjectInt("transport"))
@click.option("--connection-start-count", default=0, type=SubObjectInt("transport"))
@click.option("--connection-stop-count", default=0, type=SubObjectInt("transport"))
@click.pass_context
def set_agent_connector_stats(
    ctx,
    connector_id,
    org_id,
    overall_status,
    **kwargs,
):
    result = connectors.set_agent_connector_stats(
        ctx, connector_id, org_id, overall_status, **kwargs
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="get-agent-connector-stats")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.pass_context
def get_agent_connector_stats(
    ctx,
    connector_id,
    org_id,
    **kwargs,
):
    result = connectors.get_agent_connector_stats(ctx, connector_id, org_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-agent-connector-stats")
@click.argument("connector-id-or-name", shell_complete=connector_completion)
@click.option("--org-id", default=None)
@click.pass_context
def show_agent_connector_stats(
    ctx,
    connector_id_or_name,
    **kwargs,
):
    connector_id = get_connector_id_from_id_or_name(ctx, connector_id_or_name)
    if not connector_id:
        print(f"failed to find connector for name {connector_id_or_name}")
        return
    connectors.show_agent_connector_stats(ctx, connector_id, **kwargs)


@cli.command(name="show-agent-connector-dynamic-stats")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.option("--collected-since", type=click.DateTime(), default=None)
@click.option("--detailed", is_flag=True, default=False)
@click.option("--breakdown", is_flag=True, default=False)
# @click.option("--watch", is_flag=True, default=False)
# @click.option("--watch-period", type=int, default=15)
@click.pass_context
def show_agent_connector_dynamic_stats(
    ctx,
    connector_id,
    **kwargs,
):
    connectors.show_agent_connector_dynamic_stats(ctx, connector_id, **kwargs)


@cli.command(name="list-connector-dynamic-stats")
@click.option("--connector-id", required=True, multiple=True)
@click.option("--org-id", default=None)
@click.option("--collected-since", type=click.DateTime(), default=None)
@click.option("--detailed", is_flag=True, default=False)
@click.option("--breakdown", is_flag=True, default=False)
@click.pass_context
def list_agent_connector_dynamic_stats(
    ctx,
    connector_id,
    **kwargs,
):
    connectors.list_connector_dynamic_stats(ctx, connector_id, **kwargs)


@cli.command(name="list-connector-static-stats")
@click.option("--connector-id", required=True, multiple=True)
@click.option("--org-id", default=None)
@click.pass_context
def list_agent_connector_static_stats(
    ctx,
    connector_id,
    **kwargs,
):
    result = connectors.list_connector_static_stats(ctx, connector_id, **kwargs)
    print(connectors.format_static_stats_as_text(ctx, result))


@cli.command(name="add-agent-connector-csr")
@click.argument("connector-id")
@click.argument("request", type=click.Path(exists=True))
@click.option("--org-id", default=None)
@click.option(
    "--target-issuer", default=None, type=click.Choice(csr.TARGET_ISSUER_VALUES)
)
@click.pass_context
def add_agent_connector_csr(ctx, **kwargs):
    result = csr.add_agent_csr(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="add-csr")
@click.argument("request", type=click.Path(exists=True))
@click.option("--org-id", default=None)
@click.option("--uid", default=None)
@click.option("--private-key-id", default=None)
@click.option(
    "--target-issuer", default=None, type=click.Choice(csr.TARGET_ISSUER_VALUES)
)
@click.pass_context
def add_csr(ctx, **kwargs):
    result = csr.add_csr(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-agent-connector-csr")
@click.argument("connector-id")
@click.argument("csr-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_agent_connector_csr(ctx, **kwargs):
    result = csr.get_agent_csr(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-agent-connector-csr")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.option("--not-valid-after", default=None)
@click.option("--reason", default=None, type=click.Choice(csr.ReasonEnum.values()))
@click.option("--private-key-id", default=None)
@click.option("--limit-csr-certificates", type=int, default=None)
@click.option(
    "--target-issuer",
    multiple=True,
    default=None,
    type=click.Choice(csr.TARGET_ISSUER_VALUES),
)
@click.pass_context
def list_agent_connector_csr(ctx, **kwargs):
    results = csr.list_agent_csr(ctx, **kwargs)
    print(csr.format_csr_as_text(ctx, results))


@cli.command(name="reissue-csr")
@click.argument("csr-id")
@click.option("--org-id", default=None)
@click.option("--old-not-after", required=True, type=click.DateTime())
@click.pass_context
def reissue_csr(ctx, **kwargs):
    result = csr.reissue_csr(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-file-share-services")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.option("--updated-since", default=None, type=click.DateTime())
@click.option("--resource-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_file_share_services(ctx, name=None, **kwargs):
    shares = file_shares.list_file_share_services(ctx, name=name, **kwargs)
    table = file_shares.format_file_share_services_as_text(ctx, shares)
    print(table)


@cli.command(name="add-file-share-service")
@click.option("--name", default=None, required=True)
@click.option("--share-name", default=None)
@click.option("--local-path", default=None, required=True)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None, required=True)
@click.option("--base-domain", default=None)
@click.option("--end-to-end-tls", default=None, type=bool)
@click.option("--share-index", default=None, type=int)
@click.option("--windows-drive", default=None, type=str)
@click.option("--linux-path", default=None, type=int)
@click.option("--mac-path", default=None, type=int)
@click.option("--tags", default=None, type=int, multiple=True)
@click.option("--file_level-access-permissions", default=None, type=bool)
@click.option("--sub-path", default=None, type=str)
@click.pass_context
def add_file_share_service(ctx, name, share_name, end_to_end_tls, base_domain, **kwargs):
    if share_name is None:
        share_name = name

    kwargs["transport_end_to_end_tls"] = end_to_end_tls
    kwargs["transport_base_domain"] = base_domain
    result = file_shares.add_file_share_service(
        ctx, name=name, share_name=share_name, **kwargs
    )
    output_entry(ctx, result)


@cli.command(name="update-file-share-service")
@click.argument("file-share-service-id")
@click.option("--name", default=None)
@click.option("--share-name", default=None)
@click.option("--local-path", default=None)
@click.option("--org-id", default=None)
@click.option("--base-domain", default=None)
@click.option("--end-to-end-tls", default=None, type=bool)
@click.option("--share-index", default=None, type=int)
@click.option("--name-slug", default=None)
@click.option("--file-level-access-permissions", default=None, type=bool)
@click.option("--published", type=click.Choice(["no", "public"]), default=None)
@click.option("--sub-path", default=None, type=str)
@click.pass_context
def update_file_share_service(
    ctx, file_share_service_id, end_to_end_tls, base_domain, published, **kwargs
):
    kwargs["transport_end_to_end_tls"] = end_to_end_tls
    kwargs["transport_base_domain"] = base_domain
    result = file_shares.update_file_share_service(
        ctx, file_share_service_id, published, **kwargs
    )
    output_entry(ctx, result)


@cli.command(name="show-file-share-service")
@click.argument("file-share-service-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_file_share_service(ctx, file_share_service_id, **kwargs):
    result = file_shares.show_file_share_service(ctx, file_share_service_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-file-share-service")
@click.argument("file-share-service-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_file_share_service(ctx, file_share_service_id, **kwargs):
    file_shares.delete_file_share_service(ctx, file_share_service_id, **kwargs)


@cli.command(name="list-desktop-resources")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--name-slug", default=None)
@click.option("--desktop-type", default=None, type=str)
@click.option("--updated-since", default=None, type=click.DateTime())
@click.option("--has-remote-app", type=bool, default=None)
@click.option("--resource-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_desktop_resources(ctx, name=None, **kwargs):
    resources = desktops.list_desktop_resources(ctx, name=name, **kwargs)
    table = desktops.format_desktops_as_text(ctx, resources)
    print(table)


def vnc_pw_valid(ctx, param, value):
    if value and len(value) > 256:
        raise click.BadParameter(
            "username/password length must be less than or equal to 256 chars."
        )
    return value


@cli.command(name="add-desktop-resource")
@click.option("--name", default=None, required=True)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.option("--address", default=None, required=True)
@click.option("--desktop-type", default="rdp", type=str)
@click.option("--disable-gateway", default=None, type=bool)
@click.option(
    "--read-write-password",
    default=None,
    type=str,
    help="password for read-write access to desktop",
    callback=vnc_pw_valid,
)
@click.option(
    "--read-write-username",
    default=None,
    type=str,
    help="username for read-write access to desktop",
    callback=vnc_pw_valid,
)
@click.option(
    "--read-only-password",
    default=None,
    type=str,
    help="password for read-only access to desktop",
    callback=vnc_pw_valid,
)
@click.option(
    "--read-only-username",
    default=None,
    type=str,
    help="username for read-only access to desktop",
    callback=vnc_pw_valid,
)
@click.option(
    "--extra-configs",
    default=None,
    type=str,
    help="extra configs for rdp desktops",
    multiple=True,
)
@click.pass_context
def add_desktop_resource(ctx, name, **kwargs):
    if kwargs.get("extra_configs", None) is not None:
        kwargs["extra_configs"] = list(kwargs["extra_configs"])
    result = desktops.add_desktop_resource(ctx, name=name, **kwargs)
    output_entry(ctx, result)


@cli.command(name="update-desktop-resource")
@click.argument("desktop-resource-id")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.option("--address", default=None)
@click.option("--session-type", default=None)
@click.option("--desktop-type", default=None, type=str)
@click.option("--disable-gateway", default=None, type=bool)
@click.option(
    "--read-write-password",
    default=None,
    type=str,
    help="password for read-write access to desktop",
    callback=vnc_pw_valid,
)
@click.option(
    "--read-write-username",
    default=None,
    type=str,
    help="username for read-write access to desktop",
    callback=vnc_pw_valid,
)
@click.option(
    "--read-only-password",
    default=None,
    type=str,
    help="password for read-only access to desktop",
    callback=vnc_pw_valid,
)
@click.option(
    "--read-only-username",
    default=None,
    type=str,
    help="username for read-only access to desktop",
    callback=vnc_pw_valid,
)
@click.option("--published", type=click.Choice(["no", "public"]), default=None)
@click.option(
    "--extra-configs",
    default=None,
    type=str,
    help="extra configs for rdp desktops",
    multiple=True,
)
@click.option(
    "--remove-extra-configs",
    default=None,
    type=bool,
    help="remove extra configs for rdp desktops",
)
@click.pass_context
def update_desktop_resource(ctx, desktop_resource_id, **kwargs):
    if kwargs.get("extra_configs", None) is not None:
        kwargs["extra_configs"] = list(kwargs["extra_configs"])
    if kwargs.get("remove_extra_configs", None):
        kwargs["extra_configs"] = []
    result = desktops.update_desktop_resource(ctx, desktop_resource_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-desktop-resource")
@click.argument("desktop-resource-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_desktop_resource(ctx, desktop_resource_id, **kwargs):
    result = desktops.show_desktop_resource(ctx, desktop_resource_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-desktop-resource")
@click.argument("desktop-resource-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_desktop_resource(ctx, desktop_resource_id, **kwargs):
    desktops.delete_desktop_resource(ctx, desktop_resource_id, **kwargs)


@cli.command(name="create-desktop-client-config")
@click.argument("desktop-resource-id")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--config-override", default=None, type=click_extension.File("r"))
@click.option("--as-text/--as-base64", default=False, is_flag=True)
@click.option("--raw", default=False, is_flag=True)
@click.pass_context
def create_desktop_client_config(ctx, desktop_resource_id, config_override, **kwargs):
    config_items = None
    if config_override is not None:
        config_items = desktops.parse_config_override_input(
            config_override.read(), config_override.name
        )
    result = desktops.create_desktop_client_config(
        ctx, desktop_resource_id, config_items=config_items, **kwargs
    )
    print(result)


@cli.command(name="create-desktop-server-config")
@click.argument("desktop-resource-id")
@click.option("--org-id", default=None)
@click.option("--as-text/--as-base64", default=False, is_flag=True)
@click.option("--raw", default=False, is_flag=True)
@click.pass_context
def create_desktop_server_config(ctx, desktop_resource_id, **kwargs):
    result = desktops.create_desktop_server_config(ctx, desktop_resource_id, **kwargs)
    print(result)


@cli.command(name="set-desktop-config-override")
@click.option("--config-override", required=True, type=click_extension.File("r"))
@click.option("--desktop-id", default=None)
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.pass_context
def set_desktop_config_override(ctx, config_override, **kwargs):
    config_items = desktops.parse_config_override_input(
        config_override.read(), config_override.name
    )
    result = desktops.set_desktop_config_override(ctx, config_items, **kwargs)
    output_entry(ctx, result)


@cli.command(name="list-resource-permissions")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--resource-role-name", default=None)
@click.option("--resource-id", default=None)
@click.option("--resource-type", default=None, type=resources.resource_type_enum)
@click.option("--limit", default=500)
@click.option("--rendered", default=False, is_flag=True)
@click.pass_context
def list_resource_permissions(ctx, rendered, **kwargs):
    if not rendered:
        roles = resources.query_permissions(ctx, **kwargs)
    else:
        roles = resources.render_permissions(ctx, **kwargs)
    table = resources.format_permissions(ctx, roles)
    print(table)


@cli.command(name="add-resource-permission")
@click.argument("user_id")
@click.argument("resource-type", type=resources.resource_type_enum)
@click.argument("resource-role-name")
@click.argument("resource-id")
@click.option("--org-id", default=None)
@click.pass_context
def add_resource_permission(ctx, **kwargs):
    result = resources.add_permission(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-resource-permission")
@click.argument("id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_resource_permission(ctx, **kwargs):
    resources.delete_permission(ctx, **kwargs)


@cli.command(name="bulk-delete-resource-permissions")
@click.option("--resource-id")
@click.option("--resource-type", type=resources.resource_type_enum)
@click.option("--org-id", default=None)
@click.pass_context
def bulk_delete_resource_permission(ctx, **kwargs):
    resources.bulk_delete_permission(ctx, **kwargs)


@cli.command(name="list-resources")
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.option("--resource-id", default=None)
@click.option("--expand-resource-members", is_flag=True, default=None)
@click.option(
    "--resource-type",
    default=None,
    type=resources.resource_type_enum,
)
@click.option(
    "--exclude-resource-type",
    default=None,
    multiple=True,
    type=resources.resource_type_enum,
)
@click.option("--page-at-id", default=None)
@click.option("--limit", default=500)
@click.option("--show-columns", type=str, default=None)
@click.option("--reset-columns", is_flag=True, default=False)
@click.option("--show-stats", is_flag=True, default=None)
@click.pass_context
def list_resources(ctx, reset_columns=None, show_columns=None, **kwargs):
    """Lists generic resources, which can be filtered by type, organisation, etc."""
    if kwargs["name"] is None:
        kwargs.pop("name")
    if show_columns and "resource_urls" in show_columns:
        kwargs["resource_urls"] = True
    results = resources.query_resources(ctx, **kwargs)
    table = resources.format_resources(
        ctx, results, show_columns=show_columns, reset_columns=reset_columns
    )
    print(table)


@cli.command(name="create-resource-group")
@click.argument("name")
@click.option("--org-id", default=None)
@click.option("--resource-member", multiple=True, type=str)
@click.pass_context
def create_resource_group(ctx, resource_member, **kwargs):
    result = resources.create_resource_group(
        ctx, resource_members=list(resource_member), **kwargs
    )
    print(result)
    output_entry(ctx, result)


@cli.command(name="delete-resource")
@click.argument("id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_resource(ctx, **kwargs):
    resources.delete_resource(ctx, **kwargs)


@cli.command(name="show-resource")
@click.argument("id")
@click.option("--org-id", default=None)
@click.option("--resource-urls", type=bool, default=None)
@click.pass_context
def show_resource(ctx, **kwargs):
    output_entry(ctx, resources.get_resource(ctx, **kwargs))


@cli.command(name="list-resource-groups")
@click.option("--org-id", default=None)
@click.pass_context
def list_resource_groups(ctx, **kwargs):
    results = resources.list_resource_groups(ctx, **kwargs)
    columns = make_columns(
        ctx,
        results,
        """
          - id
          - resource_type
          - org_id
          - resource_members:
            - id
            - resource_type
        """,
    )
    print(format_table(ctx, results, columns))


@cli.command(name="update-resource")
@click.argument("id")
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.option("--bundle-id", default=None)
@click.option("--resource-member", multiple=True, type=str)
@click.option("--remove-resource-member", multiple=True, type=str)
@click.option(
    "--rules-config-file",
    help="A json file that contains the resource's rule configuration.",
    type=click_extension.JSONFile("r"),
)
@click.option(
    "--roles-config-file",
    help="A json file that contains the resource's role configuration.",
    type=click_extension.JSONFile("r"),
)
@click.option("--published", type=click.Choice(["no", "public"]), default=None)
@click.option(
    "--hide", type=click.Choice(["no", "all", "desktop", "profile"]), default=None
)
@click.pass_context
def update_resource(ctx, id, resource_member, remove_resource_member, **kwargs):
    result = resources.update_resource(
        ctx,
        id,
        resource_members=list(resource_member),
        remove_resource_members=list(remove_resource_member),
        **kwargs,
    )
    output_entry(ctx, result)


@cli.command(name="reconcile-default-policy")
@click.argument("resource-id")
@click.pass_context
def reconcile_default_policy(ctx, **kwargs):
    result = resources.reconcile_default_policy(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-org-user-roles")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--limit", default=500)
@click.option("--offset", default=0)
@click.option("--paginate", is_flag=True, default=False)
@click.pass_context
def list_org_user_roles(ctx, **kwargs):
    roles = users.list_org_user_roles(ctx, **kwargs)
    table = users.format_org_user_roles(ctx, roles)
    print(table)


@cli.command(name="list-ipsec-connectors")
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_ipsec_connectors(ctx, **kwargs):
    results = connectors.query_ipsec(ctx, **kwargs)
    table = PrettyTable(
        [
            "id",
            "name",
            "org_id",
            "connections",
            "application_services",
        ]
    )
    for entry in results.ipsec_connectors:
        table.add_row(
            [
                entry.metadata.id,
                entry.spec.name,
                entry.spec.org_id,
                [connection.name for connection in entry.spec.connections],
                entry.status.application_services,
            ]
        )
    table.align = "l"
    print(table)


@cli.command(name="add-ipsec-connector")
@click.argument("name")
@click.option("--org-id", default=None)
@click.pass_context
def add_ipsec_connector(ctx, **kwargs):
    result = connectors.add_ipsec(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="add-ipsec-connection")
@click.argument("connector_id")
@click.argument("name")
@click.option("--remote-ipv4-address")
@click.option("--org-id", default=None)
@click.option("--inherit-from")
@click.option("--ike-version", type=click.Choice(["ikev1", "ikev2"]))
@click.option("--local-ipv4-block")
@click.option("--remote-healthcheck-ipv4-address")
@click.option("--remote-ipv4-block", multiple=True, type=str)
@click.option(
    "--ike-authentication-type",
    type=click.Choice(["ike_preshared_key", "certificate"]),
    default=None,
)
@click.option("--ike-preshared-key")
@click.option("--ike-chain-of-trust-certificates-filename", type=click.Path(exists=True))
@click.option("--ike-remote-identity")
@click.option(
    "--ike-cipher-encryption-algorithm", type=click.Choice(["aes128", "aes256"])
)
@click.option(
    "--ike-cipher-integrity-algorithm", type=click.Choice(["sha256", "sha384", "sha512"])
)
@click.option(
    "--ike-cipher-diffie-hellman-group",
    type=click.Choice(["ecp256", "ecp384", "ecp512"]),
)
@click.option(
    "--esp-cipher-encryption-algorithm", type=click.Choice(["aes128", "aes256"])
)
@click.option(
    "--esp-cipher-integrity-algorithm", type=click.Choice(["sha256", "sha384", "sha512"])
)
@click.option(
    "--esp-cipher-diffie-hellman-group",
    type=click.Choice(["ecp256", "ecp384", "ecp512"]),
)
@click.option("--esp-lifetime", type=int)
@click.option("--ike-lifetime", type=int)
@click.option("--ike-rekey", type=bool)
@click.option("--ike-reauth", type=bool)
@click.option("--use-cert-hash", type=bool)
@click.option("--remote-certificate-uribase", type=str)
@click.option("--local-certificate-uribase", type=str)
@click.pass_context
def add_ipsec_connection(ctx, **kwargs):
    result = connectors.add_or_update_ipsec_connection(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="update-ipsec-connection")
@click.argument("connector_id")
@click.argument("name")
@click.option("--remote-ipv4-address")
@click.option("--org-id", default=None)
@click.option("--inherit-from")
@click.option("--ike-version", type=click.Choice(["ikev1", "ikev2"]))
@click.option("--local-ipv4-block")
@click.option("--remote-healthcheck-ipv4-address")
@click.option("--remote-ipv4-block", multiple=True, type=str)
@click.option(
    "--ike-authentication-type",
    type=click.Choice(["ike_preshared_key", "certificate"]),
    default=None,
)
@click.option("--ike-preshared-key")
@click.option("--ike-chain-of-trust-certificates-filename", type=click.Path(exists=True))
@click.option("--ike-remote-identity")
@click.option(
    "--ike-cipher-encryption-algorithm", type=click.Choice(["aes128", "aes256"])
)
@click.option(
    "--ike-cipher-integrity-algorithm", type=click.Choice(["sha256", "sha384", "sha512"])
)
@click.option(
    "--ike-cipher-diffie-hellman-group",
    type=click.Choice(["ecp256", "ecp384", "ecp512"]),
)
@click.option(
    "--esp-cipher-encryption-algorithm", type=click.Choice(["aes128", "aes256"])
)
@click.option(
    "--esp-cipher-integrity-algorithm", type=click.Choice(["sha256", "sha384", "sha512"])
)
@click.option(
    "--esp-cipher-diffie-hellman-group",
    type=click.Choice(["ecp256", "ecp384", "ecp512"]),
)
@click.option("--esp-lifetime", type=int)
@click.option("--ike-lifetime", type=int)
@click.option("--ike-rekey", type=bool)
@click.option("--ike-reauth", type=bool)
@click.option("--use-cert-hash", type=bool)
@click.option("--remote-certificate-uribase", type=str)
@click.option("--local-certificate-uribase", type=str)
@click.pass_context
def update_ipsec_connection(ctx, **kwargs):
    result = connectors.add_or_update_ipsec_connection(
        ctx, update_connection=True, **kwargs
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-ipsec-connection")
@click.argument("connector_id")
@click.argument("name")
@click.pass_context
def delete_ipsec_connection(ctx, **kwargs):
    result = connectors.delete_ipsec_connection(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-ipsec-connector")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_ipsec_connector(ctx, connector_id, **kwargs):
    result = connectors.get_ipsec(ctx, connector_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-ipsec-connection")
@click.argument("connector-id")
@click.argument("name")
@click.option("--org-id", default=None)
@click.pass_context
def show_ipsec_connection(ctx, connector_id, name, **kwargs):
    result = connectors.get_ipsec(ctx, connector_id, **kwargs)
    for connection in result.spec.connections:
        if connection.name == name:
            _dict = connection.to_dict()
            _spec = _dict.pop("spec")
            output_entry(ctx, _dict)
            output_entry(ctx, _spec)
            return


@cli.command(name="show-ipsec-connections")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.option("--render-inherit", is_flag=True, default=False)
@click.pass_context
def show_ipsec_connections(ctx, connector_id, render_inherit, **kwargs):
    if render_inherit is True:
        result = connectors.get_ipsec_info(ctx, connector_id, **kwargs)
    else:
        result = connectors.get_ipsec(ctx, connector_id, **kwargs)
    header = ["property"]
    rows = {}

    for connection in result.spec.connections:

        header.append(connection.name)
        _dict = connection.to_dict()
        _spec = _dict.pop("spec")

        for k, v in _spec.items():
            rows.setdefault(k, [])
            if v is not None:
                rows[k].append(v)
            else:
                rows[k].append("")
    table = PrettyTable(header)
    for k, v in rows.items():
        columns = [k]
        columns.extend(v)
        table.add_row(columns)
    table.align = "l"
    print(table)


@cli.command(name="show-ipsec-connector-info")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_ipsec_connector_info(ctx, connector_id, **kwargs):
    result = connectors.get_ipsec_info(ctx, connector_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="update-ipsec-connector")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.option("--name-slug", default=None)
@click.pass_context
def update_ipsec_connector(ctx, connector_id, **kwargs):
    result = connectors.replace_ipsec(ctx, connector_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-ipsec-connector")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_ipsec_connector(ctx, connector_id, **kwargs):
    connectors.delete_ipsec(ctx, connector_id, **kwargs)


@cli.command(name="list-csr")
@click.option("--org-id", default=None)
@click.option("--not-valid-after", default=None)
@click.option("--reason", type=click.Choice(csr.ReasonEnum.values()))
@click.option(
    "--target-issuer",
    multiple=True,
    type=click.Choice(csr.TARGET_ISSUER_VALUES),
    default=None,
)
@click.option("--limit-csr-certificates", type=int, default=None)
@click.option("--get-certificate-updates", is_flag=True, default=False)
@click.pass_context
def list_csr(ctx, **kwargs):
    results = csr.list_csr(ctx, **kwargs)
    print(csr.format_csr_as_text(ctx, results, **kwargs))


@cli.command(name="show-csr")
@click.argument("csr-id")
@click.option("--org-id", default=None)
@click.option("--limit-csr-certificates", type=int, default=None)
@click.option("--get-certificate-updates", is_flag=True, default=False)
@click.pass_context
def get_csr(ctx, **kwargs):
    result = csr.get_csr(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-csr")
@click.argument("csr-id", nargs=-1)
@click.option("--org-id", default=None)
@click.pass_context
def delete_csr(ctx, csr_id, **kwargs):
    for id in csr_id:
        csr.delete_csr(ctx, csr_id=id, **kwargs)


@cli.command(name="update-csr")
@click.argument("csr-id")
@click.option("--org-id", default=None)
@click.option("--uid", default=None)
@click.option("--private-key-id", default=None)
@click.pass_context
def update_csr(ctx, *args, **kwargs):
    csr.update_csr(ctx, *args, **kwargs)


@cli.command(name="list-certificates")
@click.option("--org-id", default=None)
@click.pass_context
def list_certificates(ctx, **kwargs):
    results = certificate.list_certificates(ctx, **kwargs)
    print(certificate.format_certificates_as_text(ctx, results))


@cli.command(name="show-certificate")
@click.argument("certificate-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_certificates(ctx, **kwargs):
    result = certificate.get_certificate(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-certificate")
@click.argument("certificate-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_certificate(ctx, **kwargs):
    certificate.delete_certificate(ctx, **kwargs)


@cli.command(name="add-certificate")
@click.argument("csr-id")
@click.option("--certificate", type=click.Path(exists=True))
@click.option("--org-id", default=None)
@click.option("--message", default="a default message")
@click.option("--reason", default="pending", type=click.Choice(csr.ReasonEnum.values()))
@click.pass_context
def add_certificates(ctx, **kwargs):
    result = certificate.add_certificate(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-root-certificates")
@click.option("--org-id", default=None)
@click.pass_context
def list_root_certificates(ctx, **kwargs):
    results = certificate.list_root_certificates(ctx, **kwargs)
    print(certificate.format_root_certificates_as_text(ctx, results))


@cli.command(name="list-sessions")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--revoked/--not-revoked", default=None)
@click.option("--limit", default=500)
@click.option("--show-columns", type=str, default=None)
@click.option("--reset-columns", is_flag=True, default=False)
@click.pass_context
def list_sessions(ctx, show_columns, reset_columns, **kwargs):
    results = tokens.list_sessions(ctx, **kwargs)
    columns = make_columns(
        ctx,
        results,
        """
          - metadata.id
          - metadata.created
          - spec.user_id
          - spec.revoked
        """,
        show=show_columns,
        clear=reset_columns,
    )
    print(format_table(ctx, results, columns))


@cli.command(name="add-session")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--number-of-failed-multi-factor-challenges", type=int, default=None)
@click.option("--number-of-logins", type=int, default=None)
@click.option("--revoked/--not-revoked", default=None)
@click.pass_context
def add_session(ctx, **kwargs):
    result = tokens.add_session(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-session")
@click.argument("session-id")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.pass_context
def show_session(ctx, session_id, **kwargs):
    result = tokens.get_session(ctx, session_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-session")
@click.argument("session-id")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.pass_context
def delete_session(ctx, session_id, **kwargs):
    tokens.delete_session(ctx, session_id, **kwargs)


@cli.command(name="update-session")
@click.argument("session-id")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--number-of-failed-multi-factor-challenges", type=int, default=None)
@click.option("--number-of-logins", type=int, default=None)
@click.option("--revoked/--not-revoked", default=None)
@click.pass_context
def update_session(ctx, session_id, **kwargs):
    result = tokens.update_session(ctx, session_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-forwarder")
@click.argument("id")
@click.option("--org-id", default=None)
@click.pass_context
def show_forwarder(ctx, **kwargs):
    result = forwarders.get(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-forwarder")
@click.argument("id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_forwarder(ctx, **kwargs):
    forwarders.delete(ctx, **kwargs)


@cli.command(name="add-forwarder")
@click.argument("name")
@click.argument("port", type=int)
@click.argument("connector-id")
@click.argument("application-service-id")
@click.option("--org-id", default=None)
@click.option("--bind-address", default="localhost")
@click.option("--protocol", default="tcp")
@click.pass_context
def add_forwarder(ctx, **kwargs):
    result = forwarders.add(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-forwarders")
@click.option("--org-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_forwarders(ctx, **kwargs):
    ids = forwarders.query(ctx, **kwargs)
    table = forwarders.format_forwarders_as_text(ctx, ids)
    print(table)


@cli.command(name="update-forwarder")
@click.argument("id")
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.option("--port", type=int, default=None)
@click.option("--connector-id", default=None)
@click.option("--application-service-id", default=None)
@click.option("--bind-address", default=None)
@click.option("--protocol", default=None)
@click.pass_context
def update_forwarder(ctx, id, **kwargs):
    result = forwarders.replace(ctx, id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-resource-roles")
@click.option("--resource-type", default=None, type=resources.resource_type_enum)
@click.option("--org-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_resource_roles(ctx, **kwargs):
    roles = resources.query_roles(ctx, **kwargs)
    table = resources.format_roles(ctx, roles)
    print(table)


@cli.command(name="list-upstream-group-mappings")
@click.argument("issuer-id")
@click.option("--org-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_upstream_group_mappings(ctx, issuer_id, **kwargs):
    ids = issuers.list_upstream_group_mappings(ctx, issuer_id, **kwargs)
    table = issuers.format_upstream_group_mappings_table(ctx, ids)
    print(table)


@cli.command(name="add-upstream-group-mapping")
@click.argument("issuer-id")
@click.argument("upstream-issuer")
@click.option("--org-id", default=None)
@click.pass_context
def add_upstream_group_mapping(ctx, issuer_id, upstream_issuer, **kwargs):
    result = issuers.add_upstream_group_mapping(
        ctx, issuer_id, upstream_issuer, **kwargs
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="show-upstream-group-mapping")
@click.argument("issuer-id")
@click.argument("upstream-group-mapping-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_upstream_group_mapping(ctx, issuer_id, upstream_group_mapping_id, **kwargs):
    result = issuers.get_upstream_group_mapping(
        ctx, issuer_id, upstream_group_mapping_id, **kwargs
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-upstream-group-mapping")
@click.argument("issuer-id")
@click.argument("upstream-group-mapping-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_upstream_group_mapping(ctx, issuer_id, upstream_group_mapping_id, **kwargs):
    issuers.delete_upstream_group_mapping(
        ctx, issuer_id, upstream_group_mapping_id, **kwargs
    )


@cli.command(name="update-upstream-group-mapping")
@click.argument("issuer-id")
@click.argument("upstream-group-mapping-id")
@click.option("--upstream-issuer", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def update_upstream_group_mapping(ctx, issuer_id, upstream_group_mapping_id, **kwargs):
    result = issuers.update_upstream_group_mapping(
        ctx, issuer_id, upstream_group_mapping_id, **kwargs
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="add-upstream-group-mapping-entry")
@click.argument("issuer-id")
@click.argument("upstream-group-mapping-id")
@click.argument("upstream-group-name")
@click.argument("agilicus-group-name")
@click.argument("priority", type=int)
@click.option("--group-org-id", default=None)
@click.option("--upstream-name-is-a-guid", default=None, type=bool)
@click.option("--org-id", default=None)
@click.pass_context
def add_upstream_group_mapping_entry(
    ctx,
    issuer_id,
    upstream_group_mapping_id,
    upstream_group_name,
    agilicus_group_name,
    priority,
    **kwargs,
):
    result = issuers.add_upstream_group_mapping_entry(
        ctx,
        issuer_id,
        upstream_group_mapping_id,
        upstream_group_name,
        agilicus_group_name,
        priority,
        **kwargs,
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-upstream-group-mapping-entry")
@click.argument("issuer-id")
@click.argument("upstream-group-mapping-id")
@click.argument("upstream-group-name")
@click.option("--org-id", default=None)
@click.pass_context
def delete_upstream_group_mapping_entry(
    ctx, issuer_id, upstream_group_mapping_id, upstream_group_name, **kwargs
):
    result = issuers.delete_upstream_group_mapping_entry(
        ctx, issuer_id, upstream_group_mapping_id, upstream_group_name, **kwargs
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="add-upstream-group-mapping-excluded-group")
@click.argument("issuer-id")
@click.argument("upstream-group-mapping-id")
@click.argument("upstream-group-name")
@click.option("--upstream-name-is-a-guid", default=None, type=bool)
@click.option("--org-id", default=None)
@click.pass_context
def add_upstream_excluded_group(
    ctx,
    issuer_id,
    upstream_group_mapping_id,
    upstream_group_name,
    **kwargs,
):
    result = issuers.add_upstream_excluded_group(
        ctx,
        issuer_id,
        upstream_group_mapping_id,
        upstream_group_name,
        **kwargs,
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-upstream-group-mapping-excluded-group")
@click.argument("issuer-id")
@click.argument("upstream-group-mapping-id")
@click.argument("upstream-group-name")
@click.option("--org-id", default=None)
@click.pass_context
def delete_upstream_excluded_group(
    ctx, issuer_id, upstream_group_mapping_id, upstream_group_name, **kwargs
):
    result = issuers.delete_upstream_excluded_group(
        ctx, issuer_id, upstream_group_mapping_id, upstream_group_name, **kwargs
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="simulate-upstream-group-reconcile")
@click.argument("issuer-id")
@click.argument("upstream-group-mapping-id")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--group-names-from-upstream", multiple=True)
@click.option("--group-guids-from-upstream", multiple=True)
@click.pass_context
def simulate_upstream_group_reconcile(
    ctx, issuer_id, upstream_group_mapping_id, **kwargs
):
    """Simulates the behaviour of a group reconciliation policy"""
    mapping = issuers.get_upstream_group_mapping(
        ctx, issuer_id, upstream_group_mapping_id, **kwargs
    )
    if not mapping:
        print("Unable to find specified issuer mapping")
        return
    output_entry(ctx, users.simulate_upstream_group_reconcile(ctx, mapping, **kwargs))


@cli.command(name="run-upstream-group-reconcile")
@click.argument("issuer-id")
@click.argument("upstream-group-mapping-id")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--group-names-from-upstream", multiple=True)
@click.option("--group-guids-from-upstream", multiple=True)
@click.pass_context
def run_upstream_group_reconcile(ctx, issuer_id, upstream_group_mapping_id, **kwargs):
    mapping = issuers.get_upstream_group_mapping(
        ctx, issuer_id, upstream_group_mapping_id, **kwargs
    )
    if not mapping:
        print("Unable to find specified issuer mapping")
        return
    output_entry(ctx, users.run_upstream_group_reconcile(ctx, mapping, **kwargs))


@cli.command(name="show-application-api-usage-metrics")
@click.option("--org-id", default=None)
@click.pass_context
def show_application_api_usage_metrics(ctx, **kwargs):
    result = apps.show_application_api_usage_metrics(ctx, **kwargs)
    table = apps.format_usage_metrics(ctx, result)
    print(table)


@cli.command(name="show-application-usage-metrics")
@click.option("--org-id", default=None)
@click.pass_context
def show_application_usage_metrics(ctx, **kwargs):
    result = apps.show_application_usage_metrics(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-application-service-usage-metrics")
@click.option("--org-id", default=None)
@click.pass_context
def show_application_service_usage_metrics(ctx, **kwargs):
    result = apps.show_application_service_usage_metrics(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-file-share-usage-metrics")
@click.option("--org-id", default=None)
@click.pass_context
def show_file_share_usage_metrics(ctx, **kwargs):
    result = apps.show_file_share_usage_metrics(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-org-usage-metrics")
@click.option("--org-id", default=None)
@click.pass_context
def show_org_usage_metrics(ctx, **kwargs):
    result = users.show_org_usage_metrics(ctx, **kwargs)
    table = apps.format_usage_metrics(ctx, result)
    print(table)


@cli.command(name="show-connector-usage-metrics")
@click.option("--org-id", multiple=True, default=None)
@click.pass_context
def show_connectors_usage_metrics(ctx, org_id, **kwargs):
    result = connectors.show_connectors_usage_metrics(
        ctx, org_ids=list(org_id), **kwargs
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="list-upstream-aliases")
@click.argument("issuer-id")
@click.option("--org-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_upstream_aliases(ctx, issuer_id, **kwargs):
    ids = issuers.list_upstream_aliases(ctx, issuer_id, **kwargs)
    table = issuers.format_upstream_aliases_table(ctx, ids)
    print(table)


@cli.command(name="add-upstream-alias")
@click.argument("issuer-id")
@click.argument("client-id")
@click.option("--org-id", default=None)
@click.pass_context
def add_upstream_alias(ctx, issuer_id, client_id, **kwargs):
    result = issuers.add_upstream_alias(ctx, issuer_id, client_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-upstream-alias")
@click.argument("issuer-id")
@click.argument("upstream-alias-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_upstream_alias(ctx, issuer_id, upstream_alias_id, **kwargs):
    result = issuers.get_upstream_alias(ctx, issuer_id, upstream_alias_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-upstream-alias")
@click.argument("issuer-id")
@click.argument("upstream-alias-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_upstream_alias(ctx, issuer_id, upstream_alias_id, **kwargs):
    issuers.delete_upstream_alias(ctx, issuer_id, upstream_alias_id, **kwargs)


@cli.command(name="update-upstream-alias")
@click.argument("issuer-id")
@click.argument("upstream-alias-id")
@click.option("--client-id", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def update_upstream_alias(ctx, issuer_id, upstream_alias_id, **kwargs):
    result = issuers.update_upstream_alias(ctx, issuer_id, upstream_alias_id, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="add-upstream-alias-mapping")
@click.argument("issuer-id")
@click.argument("upstream-alias-id")
@click.argument("upstream-provider-name")
@click.option("--aliased-upstream-provider-names", multiple=True, default=[])
@click.option("--org-id", default=None)
@click.pass_context
def add_upstream_alias_mapping(
    ctx,
    issuer_id,
    upstream_alias_id,
    upstream_provider_name,
    **kwargs,
):
    result = issuers.add_upstream_alias_mapping(
        ctx,
        issuer_id,
        upstream_alias_id,
        upstream_provider_name,
        **kwargs,
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-upstream-alias-mapping")
@click.argument("issuer-id")
@click.argument("upstream-alias-id")
@click.argument("upstream-provider-name")
@click.option("--org-id", default=None)
@click.pass_context
def delete_upstream_alias_mapping(
    ctx, issuer_id, upstream_alias_id, upstream_provider_name, **kwargs
):
    result = issuers.delete_upstream_alias_mapping(
        ctx, issuer_id, upstream_alias_id, upstream_provider_name, **kwargs
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="list-billing-accounts")
@click.option("--org-id", default=None)
@click.option("--get-customer-data", is_flag=True, default=False)
@click.option("--get-subscription-data", is_flag=True, default=False)
@click.option("--get-usage-metrics", is_flag=True, default=False)
@click.option("--limit", default=500, type=int)
@click.option("--page-at-id", default="")
@click.option("--page-size", default=100, type=int)
@click.option("--active-orgs-since", default=None, type=click.DateTime())
@click.pass_context
def list_billing_accounts(ctx, **kwargs):
    accounts = billing.list_accounts(ctx, **kwargs)
    table = billing.format_accounts(ctx, accounts, **kwargs)
    print(table)


@cli.command(name="list-billing-subscriptions")
@click.option("--org-id", default=None)
@click.option("--billing-account-id", default=None)
@click.option("--limit", default=None, type=int)
@click.option("--page-at-id", default="")
@click.option("--page-size", default=100, type=int)
@click.option("--get-subscription-data", is_flag=True, default=False)
@click.option("--get-usage-metrics", is_flag=True, default=False)
@click.option("--get-stripe-status", is_flag=True, default=False)
@click.option("--has-cancel-detail", is_flag=True, default=None)
@click.option("--active-orgs-since", default=None, type=click.DateTime())
@click.option("--filter", type=click.Choice(billing.BILLING_SUBSCRIPTIONS_FILTER_TYPES))
@click.pass_context
def list_billing_subscriptions(ctx, get_stripe_status=False, **kwargs):
    if get_stripe_status:
        # for stripe status, we need subscription_data
        kwargs["get_subscription_data"] = True
    results = billing.list_subscriptions(ctx, **kwargs)
    table = billing.format_subscriptions(
        ctx, results, get_stripe_status=get_stripe_status, **kwargs
    )
    print(table)


@cli.command(name="add-subscription-balance-transaction")
@click.argument("billing-subscription-id")
@click.option(
    "--amount",
    default=None,
    type=float,
    help="Amount in the currency of the subscription",
)
@click.option("--description", default=None)
@click.option(
    "--adjustment-type", type=click.Choice(["credit", "debit"]), default="credit"
)
@click.pass_context
def add_subscription_balance_transaction(ctx, *args, **kwargs):
    result = billing.add_subscription_balance_transaction(ctx, *args, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-subscription-balance-transactions")
@click.argument("billing-subscription-id")
@click.option("--limit", default=None, type=int)
@click.pass_context
def list_subscription_balance_transactions(ctx, *args, **kwargs):
    result = billing.list_subscription_balance_transactions(ctx, *args, **kwargs)
    table = billing.format_balance_transactions(ctx, result.data)
    print(table)


@cli.command(name="list-customer-balance-transactions")
@click.argument("billing-id")
@click.option("--limit", default=None, type=int)
@click.pass_context
def list_customer_balance_transactions(ctx, *args, **kwargs):
    result = billing.list_customer_balance_transactions(ctx, *args, **kwargs)
    table = billing.format_balance_transactions(ctx, result.data)
    print(table)


@cli.command(name="add-billing-subscription")
@click.argument("billing-account-id", default=None)
@click.option("--subscription-id", default=None)
@click.pass_context
def add_billing_subscription(ctx, *args, **kwargs):
    result = billing.add_subscription(ctx, *args, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-billing-subscription")
@click.argument("billing-subscription-id", default=None)
@click.pass_context
def delete_billing_subscription(ctx, *args, **kwargs):
    billing.delete_subscription(ctx, *args, **kwargs)


@cli.command(name="migrate-billing-subscriptions")
@click.option("--billing-account-id", default=None)
@click.option("--commit", is_flag=True, default=None)
@click.pass_context
def migrate_billing_subscriptions(ctx, *args, **kwargs):
    billing.migrate_billing_subscriptions(ctx, *args, **kwargs)


@cli.command(name="reconcile-billing-subscriptions")
@click.option("--billing-account-id", default=None)
@click.option("--push-to-prometheus", type=bool, default=False)
@click.option("--orgs-enabled-since-days", type=int, default=2)
@click.pass_context
def reconcile_billing_subscriptions(ctx, *args, **kwargs):
    billing.reconcile_billing_subscriptions(ctx, *args, **kwargs)


@cli.command(name="add-billing-account")
@click.argument("customer-id")
@click.option("--org-id", default=None, multiple=True)
@click.option("--product-id", default=None, multiple=True)
@click.option("--dev-mode", is_flag=True, default=None)
@click.pass_context
def add_billing_accounts(ctx, org_id, **kwargs):
    account = billing.add_billing_account(ctx, org_ids=list(org_id), **kwargs)
    output_entry(ctx, account.to_dict())


@cli.command(name="delete-billing-account")
@click.argument("billing-account-id")
@click.pass_context
def delete_billing_account(ctx, **kwargs):
    billing.delete_billing_account(ctx, **kwargs)


@cli.command(name="update-billing-account")
@click.argument("billing-account-id")
@click.option("--customer-id", default=None)
@click.option("--product-id", default=None)
@click.option("--dev-mode/--prod-mode", is_flag=True, default=None)
@click.option(
    "--license-constraints",
    type=click_extension.JSONFile("r"),
    help="a constraints file; - for stdin",
)
@click.option(
    "--constraint-vars",
    type=click_extension.JSONFile("r"),
    help="a constraint variables file; - for stdin",
)
@click.option(
    "--replace-constraints",
    type=bool,
    is_flag=True,
)
@click.option(
    "--replace-vars",
    type=bool,
    is_flag=True,
)
@click.pass_context
def update_billing_account(ctx, **kwargs):
    account = billing.replace_billing_account(ctx, **kwargs)
    output_entry(ctx, account.to_dict())


@cli.command(name="add-org-to-billing-account")
@click.argument("billing-account-id")
@click.argument("org-id")
@click.pass_context
def add_org_to_billing_account(ctx, **kwargs):
    account = billing.add_org(ctx, **kwargs)
    output_entry(ctx, account.to_dict())


@cli.command(name="remove-org-from-billing-account")
@click.argument("billing-account-id")
@click.argument("org-id")
@click.pass_context
def remove_org_to_billing_account(ctx, **kwargs):
    billing.remove_org(ctx, **kwargs)


@cli.command(name="add-org-to-subscription")
@click.argument("billing-subscription-id")
@click.argument("org-id")
@click.pass_context
def add_org_to_subscription(ctx, *args, **kwargs):
    account = billing.add_org_to_subscription(ctx, *args, **kwargs)
    output_entry(ctx, account.to_dict())


@cli.command(name="remove-org-from-subscription")
@click.argument("billing-subscription-id")
@click.argument("org-id")
@click.pass_context
def remove_org_from_subscription(ctx, *args, **kwargs):
    billing.remove_org_from_subscription(ctx, *args, **kwargs)


@cli.command(name="show-billing-account")
@click.argument("billing-account-id")
@click.option("--get-customer-data", is_flag=True, default=False)
@click.option("--get-subscription-data", is_flag=True, default=False)
@click.option("--get-usage-metrics", is_flag=True, default=False)
@click.option("--org-id", default=None)
@click.pass_context
def show_billing_accounts(ctx, **kwargs):
    account = billing.get_billing_account(ctx, **kwargs)
    output_entry(ctx, account.to_dict())


def override_replace(
    metric, usage_override, usage_min, usage_max, usage_step, group_by_org
):
    if usage_override is None:
        usage_override = []
    usage_min = None if usage_min is None else int(usage_min)
    usage_max = None if usage_max is None else int(usage_max)
    usage_step = None if usage_step is None else int(usage_step)
    for idx, x in enumerate(usage_override):
        if x["metric"] == metric:
            usage_override.remove(x)
    if usage_min is not None or usage_max or usage_step is not None:
        rec = {"metric": metric}
        if usage_min is not None:
            rec["min_quantity"] = usage_min
        if usage_max is not None:
            rec["max_quantity"] = usage_max
        if usage_step is not None:
            rec["step_size"] = usage_step
        if group_by_org:
            rec["group_by_org"] = group_by_org
        usage_override.append(rec)
    return usage_override


@cli.command(name="update-subscription")
@click.argument("billing-subscription-id", required=True)
@click.option("--usage-override")
@click.option("--remove-usage-metric-name", default=None, multiple=True)
@click.option("--usage-metric-name", default=None, multiple=True)
@click.option("--usage-metric-min", default=None, multiple=True)
@click.option("--usage-metric-max", default=None, multiple=True)
@click.option("--usage-metric-step", default=None, multiple=True)
@click.option("--usage-group-by-org", default=None, multiple=True)
@click.option("--subscription-id", default=None)
@click.option("--billing-account-id", default=None)
@click.option("--feature-id", default=None, multiple=True)
@click.option("--remove-feature-id", default=None, multiple=True)
@click.option("--product-id", default=None)
@click.option("--subscription-reconcile", default=None)
@click.option("--trial-period", type=int, default=None)
@click.option("--dev-mode", is_flag=True, default=None)
@click.option("--license-id", default=None)
@click.option("--add-license", is_flag=True)
@click.option(
    "--product-table-version",
    type=str,
    default=None,
    help="when adding license, override a table version",
)
@click.option(
    "--product-name",
    type=str,
    default=None,
    help="when adding license, override a product name",
)
@click.pass_context
def update_subscription(
    ctx,
    subscription_id,
    billing_account_id=None,
    feature_id=None,
    remove_feature_id=None,
    product_id=None,
    subscription_reconcile=None,
    dev_mode=None,
    license_id=None,
    add_license=None,
    product_table_version=None,
    product_name=None,
    **kwargs,
):
    """Update the min/max overrides in a customer subscription."""
    bsub = billing.get_billing_subscription(ctx, kwargs["billing_subscription_id"])
    usage_override = bsub.spec.usage_override

    mins = list(kwargs["usage_metric_min"])
    maxs = list(kwargs["usage_metric_max"])
    steps = list(kwargs["usage_metric_step"])
    group_by_org = list(kwargs["usage_group_by_org"])

    for metric in kwargs["remove_usage_metric_name"]:
        for idx, x in enumerate(usage_override):
            if x["metric"] == metric:
                usage_override.remove(x)

    for metric in kwargs["usage_metric_name"]:
        usage_min = mins.pop(0) if len(mins) > 0 else None
        usage_max = maxs.pop(0) if len(maxs) > 0 else None
        usage_step = steps.pop(0) if len(steps) > 0 else None
        group_by_org = (
            group_by_org.pop(0) if group_by_org and len(group_by_org) > 0 else None
        )
        usage_override = override_replace(
            metric, usage_override, usage_min, usage_max, usage_step, group_by_org
        )

    bsub.spec.usage_override = usage_override

    if subscription_id is not None:
        if subscription_id:
            bsub.spec.subscription_id = subscription_id
        else:
            bsub.spec.subscription_id = None

    if billing_account_id:
        bsub.spec.billing_account_id = billing_account_id

    if feature_id is not None:
        for feature_id in feature_id:
            bsub.spec.feature_overrides.append(feature_id)

    if remove_feature_id is not None:
        old_features = bsub.spec.feature_overrides
        bsub.spec.feature_overrides = []
        for feature_id in old_features:
            if feature_id in remove_feature_id:
                # needs to be removed.
                continue
            bsub.spec.feature_overrides.append(feature_id)
    if product_id is not None:
        bsub.spec.product_id = product_id

    if dev_mode is not None:
        bsub.spec.dev_mode = dev_mode
    if license_id is not None:
        bsub.spec.license_id = license_id

    params = {}
    if subscription_reconcile is not None:
        params["subscription_reconcile"] = subscription_reconcile

    if add_license:
        add_license_to_billing_sub(ctx, bsub, product_name, product_table_version)

    sub = billing.update_subscription(
        ctx,
        billing_subscription_id=kwargs["billing_subscription_id"],
        subscription=bsub,
        **params,
    )
    output_entry(ctx, sub.to_dict())


@cli.command(name="show-billing-subscription")
@click.argument("billing-subscription-id")
@click.option("--get-customer-data", is_flag=True, default=False)
@click.option("--get-subscription-data", is_flag=True, default=False)
@click.pass_context
def show_billing_account(ctx, *args, **kwargs):
    account = billing.get_billing_subscription(ctx, *args, **kwargs)
    output_entry(ctx, account.to_dict())


@cli.command(name="cancel-billing-subscription")
@click.option("--billing-subscription-id", default=None)
@click.option("--org-id", default=None)
@click.option("--immediately", type=bool, default=None)
@click.option("--cancel-at-period-end", type=bool, default=None)
@click.option("--cancel-at", default=None, type=click.DateTime())
@click.option("--comment", default=None)
@click.option("--feedback", default=None)
@click.pass_context
def cancel_billing_subscription(ctx, org_id, billing_subscription_id, *args, **kwargs):
    if not org_id and not billing_subscription_id:
        print("require org-id or billing-subscription-id")
        sys.exit(1)

    if org_id and billing_subscription_id:
        print("require only org-id or billing-subscription-id")
        sys.exit(1)

    account = billing.cancel_billing_subscription(
        ctx, org_id=org_id, billing_subscription_id=billing_subscription_id, **kwargs
    )
    output_entry(ctx, account.to_dict())


@cli.command(name="new-billing-subscription")
@click.argument("billing-subscription-id")
@click.option("--description", default=None)
@click.option("--trial-period", type=int, default=None)
@click.pass_context
def new_billing_subscription(ctx, *args, **kwargs):
    account = billing.new_billing_subscription(ctx, *args, **kwargs)
    output_entry(ctx, account.to_dict())


@cli.command(name="list-billing-account-usage-records")
@click.argument("billing-account-id")
@click.pass_context
def list_billing_account_account_usage_records(ctx, **kwargs):
    records = billing.get_usage_records(ctx, **kwargs)
    table = billing.format_usage_records(ctx, records.usage_records)
    print(table)


@cli.command(name="create-billing-account-usage-record")
@click.option("--billing-account-id", default=None)
@click.option("--all-accounts", is_flag=True, default=None)
@click.option("--dry-run", is_flag=True, default=False)
@click.option("--push-to-prometheus-on-success", type=bool, default=False)
@click.option("--orgs-enabled-since-days", type=int, default=2)
@click.pass_context
def create_billing_account_account_usage_record(ctx, **kwargs):
    billing.create_usage_record(ctx, **kwargs)


@cli.command(name="list-subscription-features")
@click.argument("billing-subscription-id")
@click.pass_context
def list_subscription_features(ctx, **kwargs):
    results = billing.list_subscription_features(ctx, **kwargs)
    print(format_features(ctx, results))


@cli.command(name="create-billing-checkout-session")
@click.option("--org-id", default=None)
@click.option("--ui-mode", default=None)
@click.option("--return-url", default=None)
@click.option("--success-url", default=None)
@click.option("--custom-text", default=None)
@click.pass_context
def create_billing_checkout_session(ctx, *args, **kwargs):
    result = billing.create_billing_checkout_session(ctx, *args, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-billing-checkout-sessions")
@click.argument("billing-account-id", default=None)
@click.option("--checkout-session-status", default=None)
@click.pass_context
def list_billing_checkout_sessions(ctx, *args, **kwargs):
    result = billing.list_billing_checkout_sessions(ctx, *args, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-launcher")
@click.argument("id")
@click.option("--org-id", default=None)
@click.option("--expand-resource-members", is_flag=True, default=False)
@click.pass_context
def show_launcher(ctx, **kwargs):
    result = launchers.get(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-launcher")
@click.argument("id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_launcher(ctx, **kwargs):
    launchers.delete(ctx, **kwargs)


@cli.command(name="add-launcher")
@click.argument("name")
@click.option("--org-id", default=None)
@click.option("--resource-member", multiple=True, type=str)
@click.option("--command-path", default=None)
@click.option("--command-arguments", default=None)
@click.option(
    "--start-in", default=None, help="the directory in which the application is launched"
)
@click.option(
    "--do-intercept",
    type=bool,
    default=None,
    help="set this if you can't change dns settings",
)
@click.option("--hide-console", type=bool, default=None)
@click.option("--disable-http-proxy", type=bool, default=None)
@click.option("--learning-mode", type=bool, default=None)
@click.option("--learning-mode-expiry", type=click.DateTime(), default=None)
@click.option("--diagnostic-mode", type=bool, default=None)
@click.option("--wait-for-all-descendants", type=bool, default=None)
@click.pass_context
def add_launcher(ctx, resource_member, **kwargs):
    result = launchers.add(ctx, resource_members=list(resource_member), **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-launchers")
@click.option("--org-id", default=None)
@click.option("--limit", default=500)
@click.option("--resource-id", default=None)
@click.option("--expand-resource-members", is_flag=True, default=False)
@click.pass_context
def list_launchers(ctx, **kwargs):
    ids = launchers.query(ctx, **kwargs)
    table = launchers.format_launchers(ctx, ids)
    print(table)


@cli.command(name="update-launcher")
@click.argument("id")
@click.option("--org-id", default=None)
@click.option("--name", default=None)
@click.option("--resource-member", multiple=True, type=str)
@click.option("--remove-resource-member", multiple=True, type=str)
@click.option("--command-path", default=None)
@click.option("--command-arguments", default=None)
@click.option("--start-in", default=None)
@click.option("--do-intercept", type=bool, default=None)
@click.option("--hide-console", type=bool, default=None)
@click.option("--disable-http-proxy", type=bool, default=None)
@click.option("--application-id", multiple=True, type=str)
@click.option("--remove-application-id", multiple=True, type=str)
@click.option("--learning-mode", type=bool, default=None)
@click.option("--learning-mode-expiry", type=click.DateTime(), default=None)
@click.option("--run-as-admin", type=bool, default=None)
@click.option("--fork-then-attach", type=bool, default=None)
@click.option("--end-existing-if-running", type=bool, default=None)
@click.option("--diagnostic-mode", type=bool, default=None)
@click.option("--wait-for-all-descendants", type=bool, default=None)
@click.pass_context
def update_launcher(
    ctx,
    id,
    resource_member,
    remove_resource_member,
    application_id,
    remove_application_id,
    **kwargs,
):
    result = launchers.replace(
        ctx,
        id,
        resource_members=list(resource_member),
        remove_resource_members=list(remove_resource_member),
        application_ids=list(application_id),
        remove_application_ids=list(remove_application_id),
        **kwargs,
    )
    output_entry(ctx, result)


@cli.command(name="add-launcher-interceptor-rule")
@click.argument("id")
@click.option("--org-id", default=None)
@click.option("--allow-name-exact", multiple=True, type=str)
@click.option("--allow-value-regex", multiple=True, type=str)
@click.option("--disallow-name-exact", multiple=True, type=str)
@click.option("--disallow-value-regex", multiple=True, type=str)
@click.pass_context
def add_launcher_interceptor_rule(
    ctx,
    id,
    allow_name_exact,
    allow_value_regex,
    disallow_name_exact,
    disallow_value_regex,
    **kwargs,
):
    result = launchers.add_interceptor_rule(
        ctx,
        id,
        allow_name_exact_list=list(allow_name_exact),
        allow_value_regex_list=list(allow_value_regex),
        disallow_name_exact_list=list(disallow_name_exact),
        disallow_value_regex_list=list(disallow_value_regex),
        **kwargs,
    )
    output_entry(ctx, result)


@cli.command(name="remove-launcher-interceptor-rule")
@click.argument("id")
@click.option("--org-id", default=None)
@click.option("--allow-name-exact", multiple=True, type=str)
@click.option("--allow-value-regex", multiple=True, type=str)
@click.option("--disallow-name-exact", multiple=True, type=str)
@click.option("--disallow-value-regex", multiple=True, type=str)
@click.pass_context
def remove_launcher_interceptor_rule(
    ctx,
    id,
    allow_name_exact,
    allow_value_regex,
    disallow_name_exact,
    disallow_value_regex,
    **kwargs,
):
    result = launchers.remove_interceptor_rule(
        ctx,
        id,
        allow_name_exact_list=list(allow_name_exact),
        allow_value_regex_list=list(allow_value_regex),
        disallow_name_exact_list=list(disallow_name_exact),
        disallow_value_regex_list=list(disallow_value_regex),
        **kwargs,
    )
    output_entry(ctx, result)


@cli.command(name="add-launcher-interceptor-extra-process")
@click.argument("id")
@click.argument("program-name", type=str)
@click.option("--org-id", default=None)
@click.option("--name-regex-flag", type=bool, default=False)
@click.option("--start-if-not-running", type=bool, default=False)
@click.option("--exit-when-ending", type=bool, default=True)
@click.option("--attach-if-already-running", type=bool, default=False)
@click.option("--fork-then-attach", type=bool, default=False)
@click.option("--command-arguments", type=str)
@click.option("--start-in", type=str)
@click.option("--match-arguments", type=bool)
@click.option("--wait-for-exit", type=bool)
@click.pass_context
def add_launcher_interceptor_extra_process(
    ctx,
    id,
    program_name,
    **kwargs,
):
    result = launchers.add_interceptor_extra_process(
        ctx,
        id,
        program_name,
        **kwargs,
    )
    output_entry(ctx, result)


@cli.command(name="remove-launcher-interceptor-extra-process")
@click.argument("id")
@click.argument("program-name", type=str)
@click.option("--org-id", default=None)
@click.pass_context
def remove_launcher_extra_process(
    ctx,
    id,
    program_name,
    **kwargs,
):
    result = launchers.remove_interceptor_extra_process(
        ctx,
        id,
        program_name,
        **kwargs,
    )
    output_entry(ctx, result)


@cli.command(name="list-audit-destinations")
@click.option("--name", default=None, help="search by name")
@click.option("--org-id", default=None, help="search by org_id. Defaults to current org")
@click.option(
    "--destination-type",
    default=None,
    type=click.Choice(audit_destinations.DESTINATION_TYPES),
)
@click.option("--limit", default=500)
@click.pass_context
def list_audit_destinations(ctx, name=None, **kwargs):
    resources = audit_destinations.list_audit_destinations(ctx, name=name, **kwargs)
    table = audit_destinations.format_audit_destinations_as_text(ctx, resources)
    print(table)


@cli.command(name="add-audit-destination")
@click.option("--name", default=None, required=True)
@click.option("--org-id", default=None)
@click.option(
    "--destination-type",
    default=None,
    required=True,
    type=click.Choice(audit_destinations.DESTINATION_TYPES),
)
@click.option("--comment", default="")
@click.option("--location", required=True)
@click.option("--enabled", default=True, type=bool)
@click.option(
    "--authentication-type",
    default=None,
    type=click.Choice(audit_destinations.AUTH_TYPES),
)
@click.option("--username", default=None, type=str)
@click.option("--password", default=None, type=str)
@click.option("--bearer-token", default=None, type=str)
@click.pass_context
def add_audit_destination(ctx, **kwargs):
    result = audit_destinations.add_audit_destination(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(name="update-audit-destination")
@click.argument("destination-id")
@click.option("--name", default=None, help="update by name")
@click.option("--org-id", default=None)
@click.option(
    "--destination-type",
    default=None,
    type=click.Choice(audit_destinations.DESTINATION_TYPES),
)
@click.option("--comment", default=None)
@click.option("--location", default=None)
@click.option("--enabled", default=None, type=bool)
@click.option(
    "--authentication-type",
    default=None,
    type=click.Choice(audit_destinations.AUTH_TYPES),
)
@click.option("--username", default=None, type=str)
@click.option("--password", default=None, type=str)
@click.option("--token", default=None, type=str)
@click.pass_context
def update_audit_destination(ctx, destination_id, **kwargs):
    result = audit_destinations.update_audit_destination(ctx, destination_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-audit-destination")
@click.argument("destination-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_audit_destination(ctx, destination_id, **kwargs):
    result = audit_destinations.show_audit_destination(ctx, destination_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-audit-destination")
@click.argument("destination-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_audit_destination(ctx, destination_id, **kwargs):
    audit_destinations.delete_audit_destination(ctx, destination_id, **kwargs)


@cli.command(name="add-audit-destination-filter")
@click.argument("destination-id")
@click.option("--org-id", default=None)
@click.option(
    "--filter-type", required=True, type=click.Choice(audit_destinations.FILTER_TYPES)
)
@click.option("--value", multiple=True, default=None)
@click.pass_context
def add_audit_destination_filter(ctx, **kwargs):
    result = audit_destinations.add_audit_destination_filter(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(
    name="delete-audit-destination-filter",
    help=(
        "delete a filter of a given type. If value is not provided, deletes all of that"
        " type"
    ),
)
@click.argument("destination-id")
@click.option("--org-id", default=None)
@click.option(
    "--filter-type", required=True, type=click.Choice(audit_destinations.FILTER_TYPES)
)
@click.option("--value", multiple=True, default=None, required=False)
@click.pass_context
def delete_audit_destination_filter(ctx, **kwargs):
    result = audit_destinations.delete_audit_destination_filter(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(name="lookup")
@click.option("--org-id", default=None)
@click.argument("guid")
@click.pass_context
def lookup(ctx, **kwargs):
    result = lookups.lookup(ctx, **kwargs)
    # return result
    output_entry(ctx, result.to_dict())


@cli.command(name="bulk_lookup")
@click.option("--org-id", default=None)
@click.argument("guids", nargs=-1)
@click.pass_context
def bulk_lookup(ctx, guids, **kwargs):
    result = lookups.bulk_lookup(ctx, list(guids), **kwargs)
    print(result.to_dict()["guid_to_name_list"])

    table = PrettyTable(
        [
            "guid",
            "guid_type",
            "name",
            "org_id",
            "uri",
        ]
    )
    for record in result.guid_to_name_list:
        table.add_row(
            [record.guid, record.guid_type, record.name, record.org_id, record.uri]
        )
    table.align = "l"
    print(table)


@cli.command(name="watch-orgs")
@click.option("--routing-key", default=None)
@click.option("--org-id", default=None)
@click.pass_context
def watch_orgs(ctx, **kwargs):
    # Late import since stomp.py might not be installed, which amq might use
    from . import amq

    amq.subscribe(ctx, "orgs", **kwargs)


@cli.command(name="watch-updates")
@click.option("--org-id", default=None)
@click.option("--queue-override", default=None)
@click.pass_context
def watch_updates(ctx, **kwargs):
    # Late import since stomp.py might not be installed, which amq might use
    from . import amq

    amq.subscribe(ctx, "updates", **kwargs)


@cli.command(name="watch-audits")
@click.option("--org-id", default=None)
@click.option("--queue-override", default=None)
@click.option("--routing-key", default="#")
@click.pass_context
def watch_audits(ctx, **kwargs):
    # Late import since stomp.py might not be installed, which amq might use
    from . import amq

    amq.subscribe(ctx, "audits", **kwargs)


@cli.command(name="watch-issuers")
@click.option("--org-id", default=None)
@click.option("--routing-key", default=None)
@click.pass_context
def watch_issuers(ctx, **kwargs):
    # Late import since stomp.py might not be installed, which amq might use
    from . import amq

    amq.subscribe(ctx, "issuers", **kwargs)


@cli.command(name="update-application-configs")
@click.argument("app")
@click.argument("env_name")
@click.option("--org-id", default=None)
@click.option("--additional-include-user-context-headers", type=bool, default=None)
@click.option("--security-http-cors-allow-resource-origins", type=bool)
@click.option("--security-http-cors-enabled", type=bool)
@click.option(
    "--security-http-cors-mode",
    type=click.Choice(["overwrite", "clear"]),
    default="overwrite",
)
@click.option(
    "--security-http-cors-origin-matching", type=click.Choice(["me", "wildcard", "list"])
)
@click.option("--security-http-cors-allow-origins", multiple=True)
@click.option("--security-http-cors-allow-methods", multiple=True)
@click.option("--security-http-cors-allow-headers", multiple=True)
@click.option("--security-http-cors-allow-headers", multiple=True)
@click.option("--security-http-cors-expose-headers", multiple=True)
@click.option("--security-http-cors-max-age-seconds")
@click.option("--security-http-cors-allow-credentials", type=bool)
@click.option("--oidc_config-auth-enabled", type=bool)
@click.option("--oidc-config-auth-issuer", default=None)
@click.option("--oidc-config-auth-redirect-after-signin-path", default=None)
@click.option("--oidc-config-auth-redirect-subpath", default=None)
@click.option("--oidc_config_recursive_replace", default=None, type=bool)
@click.option("--oidc-config-domain-path-replacement", default=None, type=bool)
@click.option("--oidc-config-rewrite-set-cookie", default=None, type=bool)
@click.option("--oidc-config-rewrite-cookie", default=None, type=bool)
@click.option(
    "--oidc-proxy-header-response-replace",
    nargs=2,
    type=click.Tuple([str, str]),
    multiple=True,
    default=(),
    help="A tuple of two strings representing the old_name and new_name to be "
    "replaced in the response header",
)
@click.option(
    "--oidc-proxy-header-request-replace",
    nargs=2,
    type=click.Tuple([str, str]),
    multiple=True,
    default=(),
    help="A tuple of two strings representing the old_name and new_name to be "
    "replaced in the request header",
)
@click.option("--authentication-config-application-handles-authentication", type=bool)
@click.option(
    "--authentication-config-upstream-ntlm-passthrough", type=bool, default=None
)
@click.option("--client-injection-enabled", type=bool, default=None)
@click.option("--client-injection-version", default=None)
@click.pass_context
def update_application_configs(
    ctx,
    app,
    env_name,
    org_id,
    security_http_cors_allow_origins=None,
    security_http_cors_allow_methods=None,
    security_http_cors_allow_headers=None,
    security_http_cors_expose_headers=None,
    oidc_proxy_header_response_replace=None,
    oidc_proxy_header_request_replace=None,
    **kwargs,
):
    _env = apps.get_env(ctx, app, env_name, org_id)
    _app = _get_app(ctx, app, org_id=org_id)
    if _env and _app:
        application_configs = _env.get("application_configs", {})
        apps.update_application_configs(
            application_configs,
            security_http_cors_allow_origins=list(security_http_cors_allow_origins),
            security_http_cors_allow_methods=list(security_http_cors_allow_methods),
            security_http_cors_allow_headers=list(security_http_cors_allow_headers),
            security_http_cors_expose_headers=list(security_http_cors_expose_headers),
            oidc_proxy_header_response_replace=list(oidc_proxy_header_response_replace),
            oidc_proxy_header_request_replace=list(oidc_proxy_header_request_replace),
            **kwargs,
        )
        apps.update_env(
            ctx,
            _app["id"],
            env_name,
            org_id,
            application_configs=application_configs,
        )


@cli.command(name="list-feature-tags")
@click.option("--name", default=None)
@click.option("--page-at-name", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_feature_tags(ctx, **kwargs):
    ids = feature_tags.list_feature_tags(ctx, **kwargs)
    table = feature_tags.format_feature_tags_as_text(ctx, ids)
    print(table)


@cli.command(name="add-feature-tag")
@click.argument("name")
@click.pass_context
def add_feature_tag(ctx, **kwargs):
    result = feature_tags.add_feature_tag(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="show-feature-tag")
@click.argument("name")
@click.pass_context
def show_feature_tag(ctx, name):
    result = feature_tags.show_feature_tag(ctx, name=name)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-feature-tag")
@click.argument("name")
@click.pass_context
def delete_feature_tag(ctx, name):
    feature_tags.delete_feature_tag(ctx, name=name)


@cli.command(name="list-point-of-presences")
@click.option("--name", default=None)
@click.option("--page-at-name", default=None)
@click.option("--includes-all-tag", multiple=True)
@click.option("--includes-any-tag", multiple=True)
@click.option("--excludes-all-tag", multiple=True)
@click.option("--excludes-any-tag", multiple=True)
@click.option("--cluster-name", default=None)
@click.option("--org-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_point_of_presences(ctx, **kwargs):
    ids = regions.list_point_of_presences(ctx, **kwargs)
    table = regions.format_point_of_presences_as_text(ctx, ids)
    print(table)


@cli.command(name="add-point-of-presence")
@click.argument("name")
@click.option("--tag", multiple=True, help="tags attracted to this point of presence")
@click.option("--domain", multiple=True)
@click.pass_context
def add_point_of_presence(ctx, **kwargs):
    result = regions.add_point_of_presence(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="update-point-of-presence")
@click.argument("point-of-presence-id")
@click.option("--name", default=None)
@click.option("--tag", multiple=True, help="tags attracted to this point of presence")
@click.option("--domain", multiple=True)
@click.option("--master-cluster-id", default=None)
@click.option("--add-cluster-id", multiple=True)
@click.option("--remove-cluster-id", multiple=True)
@click.option("--org-domain", multiple=True)
@click.option("--public", type=bool, default=None)
@click.option("--restrict-by-user-id", type=bool, default=None)
@click.option("--add-permitted-user-id", multiple=True)
@click.option("--remove-permitted-user-id", multiple=True)
@click.option(
    "--overwrite-tags",
    is_flag=True,
    help="overwrites the tags rather than adding to them",
)
@click.option(
    "--overwrite-domains",
    is_flag=True,
    help="overwrites the domains rather than adding to them",
)
@click.option("--requests-enabled", type=bool, default=None)
@click.option("--routing-ces", default=None)
@click.pass_context
def update_point_of_presence(
    ctx, point_of_presence_id, add_cluster_id, remove_cluster_id, **kwargs
):
    result = regions.update_point_of_presence(
        ctx,
        pop_id=point_of_presence_id,
        add_cluster_ids=list(add_cluster_id),
        remove_cluster_ids=list(remove_cluster_id),
        **kwargs,
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="show-point-of-presence")
@click.argument("point-of-presence-id")
@click.pass_context
def show_point_of_presence(ctx, point_of_presence_id):
    result = regions.show_point_of_presence(ctx, pop_id=point_of_presence_id)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-point-of-presence")
@click.argument("point-of-presence-id")
@click.pass_context
def delete_point_of_presence(ctx, point_of_presence_id):
    regions.delete_point_of_presence(ctx, pop_id=point_of_presence_id)


@cli.command(name="list-clusters")
@click.option("--limit", default=500)
@click.pass_context
def list_clusters(ctx, **kwargs):
    results = regions.list_clusters(ctx, **kwargs)
    columns = make_columns(
        ctx,
        results,
        """
          - metadata.id
          - spec.name
          - spec.domain
          - spec.config
        """,
    )
    print(format_table(ctx, results, columns))


@cli.command(name="add-cluster")
@click.argument("name")
@click.option("--domain", default=None)
@click.option("--ip-address", type=str, multiple=True)
@click.option("--description", default=None)
@click.pass_context
def add_cluster(ctx, ip_address, **kwargs):
    result = regions.add_cluster(ctx, ip_addresses=list(ip_address), **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-cluster")
@click.argument("cluster_id")
@click.pass_context
def delete_cluster(ctx, *args, **kwargs):
    regions.delete_cluster(ctx, *args, **kwargs)


@cli.command(name="update-cluster")
@click.argument("cluster_id")
@click.option("--name", default=None)
@click.option("--domain", default=None)
@click.option("--add-ip-address", type=str, multiple=True)
@click.option("--remove-ip-address", type=str, multiple=True)
@click.option("--description", default=None)
@click.pass_context
def update_cluster(ctx, add_ip_address, remove_ip_address, *args, **kwargs):
    regions.update_cluster(
        ctx,
        *args,
        remove_ip_addresses=list(remove_ip_address),
        add_ip_addresses=list(add_ip_address),
        **kwargs,
    )


@cli.command(name="list-regions")
@click.option("--limit", default=500)
@click.pass_context
def list_regions(ctx, **kwargs):
    results = regions.list_regions(ctx, **kwargs)
    columns = make_columns(
        ctx,
        results,
        """
          - metadata.id(newname=id)
          - spec.name(newname=name)
          - spec.master_pop_id(newname=master)
          - spec.routing(newname=routing)
          - status.pops:
            - metadata.id(newname=id)
            - spec.name(newname=name)
            - spec.routing(newname=routing)
        """,
    )
    print(format_table(ctx, results, columns))


@cli.command(name="add-region")
@click.argument("name")
@click.option("--domain", multiple=True)
@click.pass_context
def add_region(ctx, **kwargs):
    result = regions.add_region(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="update-region")
@click.argument("region-id")
@click.option("--name", default=None)
@click.option("--domain", multiple=True)
@click.option("--org-domain", multiple=True)
@click.option("--master-pop-id", default=None)
@click.option("--add-pop-id", multiple=True)
@click.option("--remove-pop-id", multiple=True)
@click.option("--requests-enabled", type=bool, default=None)
@click.option("--public", type=bool, default=None)
@click.option("--restrict-by-user-id", type=bool, default=None)
@click.option("--add-permitted-user-id", multiple=True)
@click.option("--remove-permitted-user-id", multiple=True)
@click.option("--routing-ces", default=None)
@click.option(
    "--overwrite-domains",
    is_flag=True,
    help="overwrites the domains rather than adding to them",
)
@click.pass_context
def update_region(ctx, region_id, add_pop_id, remove_pop_id, **kwargs):
    result = regions.update_region(
        ctx,
        region_id=region_id,
        add_pop_ids=list(add_pop_id),
        remove_pop_ids=list(remove_pop_id),
        **kwargs,
    )
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-region")
@click.argument("region_id")
@click.pass_context
def delete_region(ctx, *args, **kwargs):
    regions.delete_region(ctx, *args, **kwargs)


@cli.command(name="routing-request")
@click.option("--ip-address", multiple=True, default=None)
@click.pass_context
def routing_request(ctx, *args, **kwargs):
    output_entry(ctx, regions.routing_request(ctx, *args, **kwargs).to_dict())


@cli.command(name="build-agilicus-locations")
@click.option("--fail-on-domain-lookup-failure", default=True)
@click.pass_context
def build_agilicus_locations(ctx, *args, **kwargs):
    regions.build_agilicus_locations(ctx, *args, **kwargs)


@cli.command(name="list-connector-queues")
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.pass_context
def list_connector_queues(ctx, **kwargs):
    results = connectors.get_connector_queues(ctx, **kwargs)
    table = connectors.format_queues(ctx, results)
    print(table)


@cli.command(name="add-connector-queue")
@click.argument("connector-id")
@click.argument("instance-name")
@click.option("--org-id", default=None)
@click.option("--queue-ttl", type=int, default=None)
@click.option("--dynamic_routes_enabled", type=bool, default=None)
@click.pass_context
def add_connector_queue(ctx, **kwargs):
    result = connectors.add_connector_queue(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-connector-queue")
@click.argument("connector-id")
@click.argument("queue-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_connector_queue(ctx, **kwargs):
    connectors.delete_connector_queue(ctx, **kwargs)


@cli.command(name="get-connector-stats-config")
@click.option("--org-id", default=None)
@click.option("--connector-id", required=True, default=None)
@click.pass_context
def get_connector_stats_config(ctx, **kwargs):
    result = connectors.get_connector_stats_config(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-ssh-resources")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--name-slug", default=None)
@click.option("--updated-since", default=None, type=click.DateTime())
@click.option("--resource-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_ssh_resources(ctx, name=None, **kwargs):
    resources = ssh.list_ssh_resources(ctx, name=name, **kwargs)
    table = ssh.format_ssh_as_text(ctx, resources)
    print(table)


@cli.command(name="add-ssh-resource")
@click.option("--name", default=None, required=True)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.option("--address", default=None, required=True)
@click.option("--port", type=int, default=None)
@click.pass_context
def add_ssh_resource(ctx, name, port, **kwargs):
    result = ssh.add_ssh_resource(ctx, name=name, port=port, **kwargs)
    output_entry(ctx, result)


@cli.command(name="update-ssh-resource")
@click.argument("ssh-resource-id")
@click.option("--name", default=None)
@click.option("--org-id", default=None)
@click.option("--connector-id", default=None)
@click.option("--address", default=None)
@click.option("--port", type=int, default=None)
@click.option("--username", default=None)
@click.option("--published", type=click.Choice(["no", "public"]), default=None)
@click.pass_context
def update_ssh_resource(ctx, ssh_resource_id, port, published, **kwargs):
    result = ssh.update_ssh_resource(ctx, ssh_resource_id, port, published, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-ssh-resource")
@click.argument("ssh-resource-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_ssh_resource(ctx, ssh_resource_id, **kwargs):
    result = ssh.show_ssh_resource(ctx, ssh_resource_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-ssh-resource")
@click.argument("ssh-resource-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_ssh_resource(ctx, ssh_resource_id, **kwargs):
    ssh.delete_ssh_resource(ctx, ssh_resource_id, **kwargs)


@cli.command(name="list-user-ssh-access-info")
@click.option("--user", default=None)
@click.option("--org-id", default=None)
@click.option("--resource-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_user_ssh_access_info(ctx, user, org_id, **kwargs):
    user_id = user_id_or_id_from_email(ctx, user_id_or_email=user, org_id=org_id)
    info = users.list_user_ssh_access_info(ctx, user_id, org_id=org_id, **kwargs)
    table = users.format_user_ssh_access_info_as_text(ctx, info)
    print(table)


@cli.command(name="list-user-launcher-access-info")
@click.option("--user", default=None)
@click.option("--org-id", default=None)
@click.option("--resource-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_user_launcher_access_info(ctx, user, org_id, **kwargs):
    user_id = user_id_or_id_from_email(ctx, user_id_or_email=user, org_id=org_id)
    info = users.list_user_launcher_access_info(ctx, user_id, org_id=org_id, **kwargs)
    table = users.format_user_launcher_access_info_as_text(ctx, info)
    print(table)


@cli.command(name="add-remote-app")
@click.option("--desktop-id", required=True)
@click.option("--command-path", required=True)
@click.option("--org-id", default=None)
@click.option("--command-arguments", default=None)
@click.option("--working-directory", default=None)
@click.option("--expand-command-line-with-local", type=bool, default=None)
@click.option("--expand-working-directory-with-local", type=bool, default=None)
@click.option("--file-to-open", default=None)
@click.pass_context
def add_remote_app(ctx, **kwargs):
    result = desktops.add_remote_app(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(name="get-user-access-info")
@click.argument("user-id", default=None, required=False)
@click.argument("org-id", default=None, required=False)
@click.option(
    "--if-none-match", default=None, help="use sha256 of last fetched to short-circuit"
)
@click.pass_context
def get_user_access_info(ctx, user_id, org_id, **kwargs):
    user_id = get_user_id_from_input_or_ctx(ctx, org_id)
    org_id = get_org_from_input_or_ctx(ctx, org_id)
    result, _, headers = users.get_user_ssh_access_info(
        ctx, user_id, org_id=org_id, **kwargs
    )
    output_entry(ctx, result.to_dict(), headers)


@cli.command(name="update-remote-app")
@click.option("--desktop-id", required=True)
@click.option("--command-path", default=None)
@click.option("--org-id", default=None)
@click.option("--command-arguments", default=None)
@click.option("--working-directory", default=None)
@click.option("--expand-command-line-with-local", type=bool, default=None)
@click.option("--expand-working-directory-with-local", type=bool, default=None)
@click.option("--file-to-open", default=None)
@click.pass_context
def update_remote_app(ctx, **kwargs):
    result = desktops.update_remote_app(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(name="add-display-info-icon", help="Add an icon to a resource")
@click.option("--resource-id", required=True)
@click.option("--org-id", default=None)
@click.option("--uri", required=True)
@click.option("--purpose", multiple=True, default=None)
@click.option("--height-px", type=int, default=None)
@click.option("--width-px", type=int, default=None)
@click.pass_context
def add_display_info_icon(ctx, **kwargs):
    result = resources.add_display_info_icon(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-display-info-icon")
@click.option("--resource-id", required=True)
@click.option("--org-id", default=None)
@click.option("--uri", required=True)
@click.pass_context
def delete_display_info_icon(ctx, **kwargs):
    result = resources.delete_display_info_icon(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-remote-app")
@click.option("--desktop-id", required=True)
@click.option("--org-id", default=None)
@click.pass_context
def delete_remote_app(ctx, **kwargs):
    result = desktops.clear_remote_app(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(name="create-one-time-use-challenge")
@click.option("--user-id", default=None)
@click.option("--actor-id", multiple=True, default=None)
@click.option("--org-id", default=None)
@click.option("--action-url", required=True)
@click.option("--action-method", required=True)
@click.option("--approve-action-body", default=None)
@click.option("--decline-action-body", default=None)
@click.option("--action-content-type", default=None)
@click.option("--scope", multiple=True, default=None)
@click.option("--timeout-seconds", type=int, required=True, default=600)
@click.pass_context
def create_one_time_use_challenge(ctx, **kwargs):
    result = challenges.create_one_time_use_challenge(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="create-user-data-token")
@click.option("--user-data", type=str, default=None, help="json string of user data")
@click.option("--aud", type=str, multiple=True)
@click.option(
    "--duration", type=int, default=3600, help="duration of signed user token in seconds"
)
@click.pass_context
def create_user_data_token(ctx, aud=None, **kwargs):
    result = tokens.create_user_data_token(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="admin-set-subscription-info")
@click.option("--org-id", default=context.ORG_ID_DEFAULT, required=True)
@click.option("--min-user", default=None)
@click.option("--max-user", default=None)
@click.option("--step-user", default=None)
@click.option("--min-connector", default=None)
@click.option("--max-connector", default=None)
@click.option("--step-connector", default=None)
@click.pass_context
def admin_set_subscription_info(ctx, **kwargs):
    """Administrative use, change parameters of subscription."""
    admin.set_subscription_info(ctx, **kwargs)


@cli.command(name="admin-org-status")
@click.option("--org-id", default=None, required=False)
@click.option("--email", default=None)
@click.option("--markdown/--no-markdown", default=False, required=False)
@click.pass_context
def admin_status(ctx, **kwargs):
    """Show the status of an org, either by org-id, or, email of owner."""
    admin.status(ctx, **kwargs)


@cli.command(name="admin-all-org-status")
@click.option("--parent-org-id", default="WWcWgenXrv9KUdfH9ipaYF", required=False)
@click.pass_context
def admin_all_org_status(ctx, **kwargs):
    """Show the status of all orgs with the given parent."""
    admin.all_org_status(ctx, **kwargs)


@cli.command(name="delete-demo")
@click.option("--org-id", default=context.ORG_ID_DEFAULT, required=True)
@click.pass_context
def delete_demo(ctx, **kwargs):
    """Delete a demo-setup (if in present)."""
    demo.delete(ctx, **kwargs)


@cli.command()
@click.option("--limit", type=int, default=None)
@click.option("--org-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--email", default=None)
@click.option("--user-id", default=None)
@click.option("--allow-partial-match", is_flag=True, default=False)
@click.option("--type", multiple=True, type=click.Choice(users.USER_TYPES), default=None)
@click.pass_context
def list_user_guids(ctx, type, **kwargs):
    results = users.list_user_guids(ctx, type=list(type), **kwargs)
    columns = make_columns(
        ctx,
        results,
        """
          - guid
          - name
        """,
    )
    print(format_table(ctx, results, columns))


@cli.command()
@click.pass_context
@click.option("--org-id", default=None)
@click.option("--n", default=10, type=int)
def show_top_connectors(ctx, **kwargs):
    metrics.show_top_connectors(ctx, **kwargs)


@cli.command()
@click.option("--limit", type=int, default=None)
@click.option("--org-id", default=None)
@click.option("--page-at-id", default=None)
@click.option("--inner-connector-id", default=None)
@click.option("--outer-connector-id", default=None)
@click.pass_context
def list_connector_proxies(ctx, **kwargs):
    results = connectors.list_connector_proxies(ctx, **kwargs)
    columns = make_columns(
        ctx,
        results,
        """
          - metadata.id
          - spec.inner_connector_id
          - spec.outer_connector_id
          - spec.local_bind
        """,
    )
    print(format_table(ctx, results, columns))


@cli.command()
@click.argument("inner_connector_id")
@click.argument("outer_connector_id")
@click.option(
    "--bind-host", default=None, help="An IP or hostname. Leave empty for all."
)
@click.option("--bind-port", type=int)
@click.option("--org-id", default=None)
@click.pass_context
def add_connector_proxy(ctx, **kwargs):
    output_entry(
        ctx,
        connectors.add_connector_proxy(ctx, **kwargs).to_dict(),
    )


@cli.command()
@click.argument("id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_connector_proxy(ctx, **kwargs):
    connectors.delete_connector_proxy(ctx, **kwargs)


@cli.command()
@click.pass_context
@click.option("--token", default=None)
@click.option("--open-profile", is_flag=True, default=None)
@click.option("--profile-uri", default=None)
@click.option("--description", default=None)
@click.option("--webpush", is_flag=True, default=None)
def create_session_challenge(ctx, token, **kwargs):
    result = tokens.create_session_challenge(ctx, token=token, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command()
@click.pass_context
@click.option("--token", default=None)
def update_session_challenge(ctx, token, **kwargs):
    result = tokens.update_session_challenge(ctx, token=token)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-org-pops")
@click.option("--org-id", default=None)
@click.pass_context
def list_org_pops(ctx, **kwargs):
    result = orgs.list_org_pops(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(name="add-org-pop")
@click.argument("pop")
@click.option("--org-id", default=None)
@click.pass_context
def add_org_pop(ctx, **kwargs):
    result = orgs.add_org_pop(ctx, **kwargs)
    output_entry(ctx, result)


@cli.command(name="remove-org-pop")
@click.argument("pop")
@click.option("--org-id", default=None)
@click.pass_context
def remove_org_pop(ctx, **kwargs):
    result = orgs.remove_org_pop(ctx, **kwargs)
    output_entry(ctx, result)


def switch_org(org):
    ctx = click.get_current_context()
    ctx.obj["ORG_ID"] = org.get("id")
    context.save_refreshable_token(ctx, tokens.RefreshableAccessToken())

    ctx.obj["ORGANISATION"] = orgs.get(ctx, org.get("id"))
    context.save(ctx)


@cli.command(name="list-connector-services")
@click.argument("connector-id")
@click.option("--org-id", default=None)
@click.pass_context
def list_connector_services(ctx, *args, **kwargs):
    results = connectors.query_services(ctx, *args, **kwargs)
    columns = make_columns(
        ctx,
        results,
        """
          - spec.org_id(newname=org_id)
          - spec.connector_id(newname=connector_id)
          - spec.service(newname=service)
          - status.application_service
        """,
    )
    print(format_table(ctx, results, columns))


@cli.command(name="add-connector-service")
@click.argument("connector-id")
@click.argument("service")
@click.option("--org-id", default=None)
@click.pass_context
def add_connector_services(ctx, *args, **kwargs):
    result = connectors.add_service(ctx, *args, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="delete-connector-service")
@click.argument("connector-id")
@click.argument("service")
@click.option("--org-id", default=None)
@click.pass_context
def delete_connector_services(ctx, *args, **kwargs):
    connectors.delete_service(ctx, *args, **kwargs)


@cli.command(name="list-support-requests")
@click.option("--org-id", default=None)
@click.option("--user-id", default=None)
@click.option("--supporting-user-org-id", default=None)
@click.option("--expired", default=None, type=bool)
@click.option("--limit", default=500)
@click.pass_context
def list_support_requests(ctx, **kwargs):
    ids = users.list_support_requests(ctx, **kwargs)
    table = users.format_support_request_as_text(ctx, ids)
    print(table)


@cli.command(name="create-support-request")
@click.option("--org-id", type=str, default=None)
@click.option("--supporting-user-email", type=str)
@click.option("--supporting-user-org-id", type=str)
@click.option("--expiry", type=click.DateTime(), default=None)
@click.option("--viewer-only-permissions", default=False, type=bool)
@click.pass_context
def create_support_request(ctx, org_id, **kwargs):
    result = users.create_support_request(ctx, org_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="show-support-request")
@click.argument("support-request-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_support_request(ctx, support_request_id, **kwargs):
    result = users.show_support_request(ctx, support_request_id, **kwargs)
    output_entry(ctx, result)


@cli.command(name="delete-support-request")
@click.argument("support-request-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_support_request(ctx, support_request_id, **kwargs):
    users.delete_support_request(ctx, support_request_id, **kwargs)


@cli.command(name="update-support-request")
@click.argument("support-request-id")
@click.option("--expiry", type=click.DateTime(), default=None)
@click.pass_context
def update_support_request(ctx, support_request_id, **kwargs):
    users.update_support_request(ctx, support_request_id, **kwargs)


@cli.command(name="create-support-request-message")
@click.argument("target-user-id", type=str)
@click.argument("target-org-id", type=str)
@click.option(
    "--duration", type=int, default=86400, help="duration of support request in seconds"
)
@click.pass_context
def create_support_request_message(
    ctx, target_user_id, target_org_id, duration, **kwargs
):
    users.create_support_request_message(
        ctx, target_user_id, target_org_id, duration, **kwargs
    )


@cli.command(name="create-support-request-acknowledgement")
@click.argument("org-id", type=str)
@click.argument("supporting-user-id", type=str)
@click.argument("support-request-id", type=str)
@click.pass_context
def create_support_request_acknowledgement(
    ctx, org_id, supporting_user_id, support_request_id, **kwargs
):
    """
    Adds an acknowledgment for support request SUPPORT_REQUEST_ID.

    ORG_ID is the supportting user's organization.
    """
    result = users.create_support_request_acknowledgement(
        ctx, org_id, supporting_user_id, support_request_id, **kwargs
    )
    output_entry(ctx, result)


@cli.command(name="show-support-request-acknowledgement")
@click.argument("support-request-acknowledgement-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_support_request_acknowledgement(
    ctx, support_request_acknowledgement_id, **kwargs
):
    result = users.show_support_request_acknowledgement(
        ctx, support_request_acknowledgement_id, **kwargs
    )
    output_entry(ctx, result)


@cli.command(name="list-support-request-acknowledgements")
@click.option("--org-id", type=str, default=None, help="org id of the supporting user")
@click.option("--support-request-id", default=None)
@click.option("--expired", default=None, type=bool)
@click.option("--limit", default=500)
@click.pass_context
def list_support_request_acknowledgements(ctx, **kwargs):
    ids = users.list_support_request_acknowledgements(ctx, **kwargs)
    table = users.format_support_request_acknowledgement_as_text(ctx, ids)
    print(table)


@cli.command(name="delete-support-request-acknowledgement")
@click.argument("support-request-acknowledgement-id")
@click.pass_context
def delete_support_request_acknowledgement(
    ctx, support_request_acknowledgement_id, **kwargs
):
    users.delete_support_request_acknowledgement(
        ctx, support_request_acknowledgement_id, **kwargs
    )


@cli.command(name="add-fake-oidc-issuer")
@click.argument("issuer-id")
@click.option("--org-id", default=None)
@click.pass_context
def add_fake_oidc_issuer(ctx, *args, **kwargs):
    result = issuers.add_fake_upstream(ctx, *args, **kwargs)
    output_entry(ctx, result)


@cli.command(name="list-certificate-trackers")
@click.option("--org-id", default=None)
@click.option("--show-columns", type=str, default=None)
@click.option("--reset-columns", is_flag=True, default=False)
@click.option("--limit", default=500)
@click.pass_context
def list_certificate_trackers(ctx, show_columns, reset_columns, **kwargs):
    results = certificate.list_certificate_trackers(ctx, **kwargs)
    columns = make_columns(
        ctx,
        results,
        """
          - metadata.id(newname=id)
          - spec.org_id(newname=org_id)
          - spec.config(newname=config)
          - status.certificates:
            - metadata.id(newname=id)
            - status.not_before(newname=not_before)
        """,
        show=show_columns,
        clear=reset_columns,
    )
    print(format_table(ctx, results, columns))


@cli.command(name="delete-certificate-tracker")
@click.argument("certificate-tracker-id")
@click.option("--org-id", default=None)
@click.pass_context
def delete_certificate_tracker(ctx, **kwargs):
    certificate.delete_certificate_tracker(ctx, **kwargs)


@cli.command(name="show-certificate-tracker")
@click.argument("certificate-tracker-id")
@click.option("--org-id", default=None)
@click.pass_context
def show_certificate_tracker(ctx, **kwargs):
    result = certificate.get_certificate_tracker(ctx, **kwargs)
    output_entry(ctx, result.to_dict())


@cli.command(name="list-regional-locations")
@click.option("--location-name-list", multiple=True, default=None)
@click.option("--subdomain", default=None)
@click.option("--org-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_regional_locations(ctx, **kwargs):
    locations = regions.list_regional_locations(ctx, **kwargs).regional_locations
    columns = make_columns(
        ctx,
        locations,
        """
          - name
          - location_type
          - org_domains
          - cname_domain_forwards
          - firewall_rules:
            - name
            - action
            - domains
            - subnets
            - ports
        """,
    )
    print(format_table(ctx, locations, columns))


@cli.command(name="list-org-upstream-user-identities")
@click.option("--org-id", default=None)
@click.option("--limit", default=500)
@click.pass_context
def list_org_upstream_user_identities(ctx, **kwargs):
    org_upstreams = users.list_org_upstream_user_identities(ctx, **kwargs)
    columns = make_columns(
        ctx,
        org_upstreams,
        """
          - metadata.id(newname=id)
          - spec.user_id(newname=user_id)
          - spec.org_id(newname=org_id)
          - spec.last_login(newname=last_login)
          - status.upstream_user_identity.spec.upstream_idp_id(newname=upstream_idp_id)
          - status.upstream_user_identity.spec.upstream_user_id(newname=upstream_user_id)
        """,
    )
    print(format_table(ctx, org_upstreams, columns))


def main():
    trusted_certs_main.add_commands(cli)
    hosts_main.add_commands(cli)
    labels_main.add_commands(cli)
    rules_main.add_commands(cli)
    policy_main.add_commands(cli)
    products_main.add_commands(cli)
    credentials_main.add_commands(cli)
    features_main.add_commands(cli)
    files_main.add_commands(cli)
    policy_config_main.add_commands(cli)
    messages_main.add_commands(cli)
    databases.add_commands(cli)
    licensing_main.add_commands(cli)

    cli(auto_envvar_prefix="AGILICUS")


if __name__ == "__main__":
    main()
