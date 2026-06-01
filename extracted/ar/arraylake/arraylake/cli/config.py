import io
from enum import StrEnum
from pathlib import Path

import typer
from rich import print_json
from rich.syntax import Syntax
from ruamel.yaml import YAML

from arraylake import config as config_obj
from arraylake.cli.utils import rich_console
from arraylake.config import user_config_file

app = typer.Typer(help="Manage configuration for arraylake")

yaml = YAML(typ="safe", pure=True)
yaml.default_flow_style = False


class ListOutputType(StrEnum):
    json = "json"
    yaml = "yaml"


def get_nested_map(obj, keys):
    o = obj
    for k in keys:
        if k not in o:
            o[k] = {}
        o = o[k]
    return o


def set_key(obj, key, value):
    if "." in key:
        pieces = key.split(".")
        assert len(pieces) > 1
        m = get_nested_map(obj, pieces[:-1])
        m[pieces[-1]] = value
    else:
        obj[key] = value


def get_key(obj, key):
    if "." in key:
        pieces = key.split(".")
        assert len(pieces) > 1
        m = get_nested_map(obj, pieces[:-1])
        return m[pieces[-1]]
    else:
        return obj[key]


def del_key(obj, key):
    if "." in key:
        pieces = key.split(".")
        assert len(pieces) > 1
        m = get_nested_map(obj, pieces[:-1])
        del m[pieces[-1]]
    else:
        del obj[key]


def get_user_config(path=user_config_file):
    try:
        with path.open(mode="r") as f:
            c = yaml.load(f)
            if c is None:
                c = {}
    except FileNotFoundError:
        c = {}
    return c


def write_user_config(c, path=user_config_file):
    with path.open(mode="w") as f:
        yaml.dump(c, f)


def print_yaml(c):
    buf = io.BytesIO()
    yaml.dump(c, buf)
    syntax = Syntax(buf.getvalue().decode(), "yaml", background_color="default", theme="default")
    rich_console.print(syntax)


@app.command(name="list")
def list_config(
    path: Path = typer.Option(None, help="Specific config file to list"),
    output: ListOutputType = typer.Option("yaml", help="Output formatting"),
):
    """**List** current Arraylake config settings

    If **path** is specified, only that part of the config will be printed.

    **Examples**

    - List arraylake config

        ```
        $ arraylake config list
        ```
    """
    if path:
        c = get_user_config(path=path)
    else:
        c = config_obj.config

    if output == "yaml":
        print_yaml(c)
    else:
        print_json(data=c)


@app.command()
def set(
    key: str = typer.Argument(..., help="key to set in config file"),
    value: str = typer.Argument(..., help="value to set in config file"),
    path: Path = typer.Option(user_config_file, help="Config file to update"),
):
    """**Set** Arraylake config value

    **Examples**

    - Set `service.uri` config value

        ```
        $ arraylake config set service.uri https://api.earthmover.io
        ```
    """
    c = get_user_config(path=path)

    set_key(c, key, value)

    # write back to file
    write_user_config(c, path=path)


@app.command()
def unset(
    key: str = typer.Argument(..., help="key to unset in config file"),
    path: Path = typer.Option(user_config_file, help="Config file to update"),
):
    """**Unset** Arraylake config value

    **Examples**

    - Unset `service.uri` config value

        ```
        $ arraylake config unset service.uri
        ```
    """
    c = get_user_config(path=path)

    del_key(c, key)

    # write back to file
    write_user_config(c, path=path)


@app.command()
def get(
    key: str = typer.Argument(..., help="key to get in config file"),
    path: Path = typer.Option(user_config_file, help="Config file to update"),
    output: ListOutputType = typer.Option("yaml", help="Output formatting"),
):
    """**Get** Arraylake config value

    **Examples**

    - Get `service.uri` config value

        ```
        $ arraylake config get service.uri
        ```
    """
    if path:
        c = get_user_config(path=path)
        data = get_key(c, key)
    else:
        data = config_obj.get(key)

    if output == "yaml":
        print_yaml(data)
    else:
        print_json(data)


@app.command()
def init(path: Path = typer.Option(user_config_file, help="Config file to initialize")):
    """**Initialize** Arraylake config

    This command will walk you through the steps to configure Arraylake.
    """

    c = get_user_config(path=path)

    # write back to file
    write_user_config(c, path=path)
    rich_console.print(f"✅ Config file updated at {path}")
