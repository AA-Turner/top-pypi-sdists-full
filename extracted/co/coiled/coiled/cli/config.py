from typing import List

import click

from coiled.utils import save_config

from .utils import CONTEXT_SETTINGS


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument("key", nargs=1)
@click.argument("value", nargs=1)
@click.option("--type-infer/--no-type-infer", is_flag=True, default=True)
def config_set(key, value: str, type_infer: bool):
    """
    Set Dask config [key] to [value].

    Example usage:

    \b
        coiled config set account foo

    For `user`, `token`, `server`, and `account`, the `coiled` prefix will
    automatically be added, so this would set `coiled.account` to `foo`.


    Note: If you aren't careful you can create schema conflicts. For example,
    you'll get an error if you try to run

    \b
         coiled config set foo 1
         coiled config set foo.bar 2

    because you can't set sub-keys on an integer (i.e., 1 in this case).
    """
    if key in ("user", "token", "server", "account"):
        key = f"coiled.{key}"

    modified_value = value

    if type_infer:
        if value.isnumeric():
            modified_value = int(value)
        else:
            try:
                modified_value = float(value)
            except ValueError:
                pass

        if value in ("False", "false"):
            modified_value = False
        if value in ("True", "true"):
            modified_value = True

        if not isinstance(modified_value, str):
            print(
                f"Interpreting '{modified_value}' as [{type(modified_value).__name__}], "
                "use --no-type-infer if you want it stored as a string."
            )

    new_config = set_config_key({}, key.split("."), modified_value)
    _config, path = save_config(new_config)

    print(f"Updated [{key}] to [{modified_value}], config saved to {path}")


def set_config_key(existing: dict, key: List[str], val) -> dict:
    if not key:
        return existing
    head = key[0]
    if len(key) == 1:
        existing[head] = val
    else:
        if head not in existing:
            existing[head] = {}

        set_config_key(existing[head], key[1:], val)

    return existing


@click.group(name="config", context_settings=CONTEXT_SETTINGS)
def config():
    pass


config.add_command(config_set, "set")
