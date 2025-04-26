import os
from importlib.metadata import version
from textwrap import dedent

import rich
import rich_click as click
from flytekit.clis.sdk_in_container.constants import CTX_VERBOSE
from rich.panel import Panel

from union._config import _UNION_CONFIG, _get_config_obj, _get_organization


@click.command("info")
@click.pass_context
def info(ctx: click.Context):
    config_obj = _get_config_obj()
    endpoint = config_obj.platform.endpoint

    union_version = version("union")
    flytekit_version = version("flytekit")
    context = dedent(
        f"""\
    union is the CLI to interact with Union. Use the CLI to register, create and track task and workflow executions locally and remotely.

    Union Version    : {union_version}
    Flytekit Version : {flytekit_version}
    Union Endpoint   : {endpoint}"""  # noqa: E501
    )
    if _UNION_CONFIG.config_source:
        context += f"{os.linesep}Config Source    : {_UNION_CONFIG.config_source}"

    is_verbose = ctx.obj[CTX_VERBOSE] > 0
    if is_verbose:
        org = _get_organization(platform_config=config_obj.platform)
        union_suffixes = [".union.ai", ".unionai.cloud"]
        if org is None:
            org = endpoint
            for suffix in union_suffixes:
                if org.endswith(suffix):
                    org = org[: -len(suffix)]
                    break
        context += f"{os.linesep}Org              : {org}"

    rich.print(Panel(context, title="Union CLI Info", padding=(1, 1)))
