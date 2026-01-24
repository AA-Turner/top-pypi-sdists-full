import click
import functools
import os
import sys
from typing import Dict, List, Union, Optional, Callable
from click_aliases import ClickAliasedGroup

from nexuscli import exception
from nexuscli.cli import constants
from nexuscli.nexus_client import NexusClient
from nexuscli.nexus_config import NexusConfig
from texttable import Texttable


class AliasedGroup(ClickAliasedGroup):
    """
    Implements execution of the first partial match for a command. Fails with a
    message if there are no unique matches.

    See: https://click.palletsprojects.com/en/7.x/advanced/#command-aliases
    """
    def get_command(self, ctx, cmd_name):
        rv = ClickAliasedGroup.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx) if x.startswith(cmd_name)]
        if not matches:
            return None
        if len(matches) == 1:
            return ClickAliasedGroup.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


def with_nexus_client(click_command):
    @functools.wraps(click_command)
    @click.pass_context
    def command(ctx: click.Context, **kwargs):
        ctx.obj = get_client()
        return click_command(ctx, **kwargs)

    return command


def add_options(options):
    def _add_options(func):
        for option in reversed(options):
            func = option(func)
        return func
    return _add_options


def move_to_key(mydict, new_key, keys_to_move):
    if set(mydict.keys()).intersection(keys_to_move):
        mydict[new_key] = {}
        for k in keys_to_move:
            mydict[new_key][k] = mydict[k]
            del mydict[k]


def mapped_commands(command_map: dict):
    """
    TODO: document command_map format

    :param command_map:
    :return:
    """
    class CommandGroup(click.Group):
        def get_command(self, ctx, cmd_name):
            for real_command, aliases in command_map.items():
                if cmd_name in aliases:
                    return click.Group.get_command(self, ctx, real_command)
            return None

        def list_commands(self, ctx):
            return sorted([a for b in command_map.values() for a in b])

    return CommandGroup


def upcase_values(mydict: dict, keys=[]):
    for key in keys:
        value = mydict.get(key)
        if value is not None:
            mydict[key] = value.upper()


def rename_keys(mydict: dict, rename_map: dict):
    for current_name, new_name in rename_map.items():
        if mydict.get(current_name) is not None:
            mydict[new_name] = mydict[current_name]
            del mydict[current_name]


def _with_env_var_prefix(names) -> List[str]:
    return [f'{constants.ENV_VAR_PREFIX}_{x}' for x in names]


def _env_settings_into_kwargs(
        variables: List[str],
        kwargs: Dict[str, Union[bool, str]],
        transform_method: Optional[Callable] = None) -> None:
    def _without_prefix(name) -> str:
        return name[len(constants.ENV_VAR_PREFIX) + 1:].lower()

    for env_var in variables:
        if os.environ.get(env_var):
            if transform_method:
                kwargs[_without_prefix(env_var)] = transform_method(os.environ[env_var])
            else:
                kwargs[_without_prefix(env_var)] = os.environ[env_var]


def _get_login_from_env() -> List[str]:
    login_variables = _with_env_var_prefix(constants.NEXUS_OPTIONS_FOR_LOGIN)
    has_any_required_env_vars = any([x in os.environ for x in login_variables])
    has_all_required_env_vars = all([x in os.environ for x in login_variables])

    if has_any_required_env_vars:
        if has_all_required_env_vars:
            return login_variables
        else:
            errmsg = 'If any of these environment variables are set, then ALL must be set: ' \
                     f'{login_variables}'
            raise exception.NexusClientInvalidCredentials(errmsg)

    return []


def _get_client_kwargs() -> Optional[Dict[str, Union[bool, str]]]:
    config_kwargs: Dict[str, Union[bool, str]] = {}
    variables_to_set: List[str]
    bool_variables: List[str]

    def _str_to_bool(value: str) -> bool:
        return value.lower() in ('true', 't', 'yes', '1')

    variables_to_set = _with_env_var_prefix(constants.OPTIONAL_NEXUS_OPTIONS)
    variables_to_set += _get_login_from_env()
    bool_variables = _with_env_var_prefix(constants.BOOL_OPTIONAL_NEXUS_OPTIONS)

    _env_settings_into_kwargs(variables_to_set, config_kwargs)
    _env_settings_into_kwargs(bool_variables, config_kwargs, _str_to_bool)

    if config_kwargs:
        return config_kwargs
    else:
        return None


def get_client() -> NexusClient:
    """
    Returns a Nexus Client instance. Prints a warning if the configuration file doesn't exist.
    """
    maybe_config = _get_client_kwargs()
    if maybe_config:
        config = NexusConfig(**_get_client_kwargs())
        return NexusClient(config=config)

    config = NexusConfig()
    try:
        config.load()
    except FileNotFoundError:
        sys.stderr.write(
            'Warning: configuration not found; proceeding with defaults.\n'
            'To remove this warning, please run `nexus3 login`\n')

    return NexusClient(config=config)


def print_as_table(contents: List[Dict], fields: List) -> None:
    """
    Print json API output as a table

    :param contents: table contents
    :param fields: list of key names in contents elements to be added as columns to table
    """
    table = Texttable(max_width=constants.TTY_MAX_WIDTH)
    table.set_deco(Texttable.HEADER)
    table.set_header_align(['l'] * len(fields))
    table.header([x.title() for x in fields])
    table.add_rows([[item[x] for x in fields] for item in contents], header=False)

    print(table.draw())
