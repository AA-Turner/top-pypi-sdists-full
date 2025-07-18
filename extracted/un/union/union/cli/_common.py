import typing
from typing import Tuple

import grpc
import rich_click as click
from flytekit.configuration import PlatformConfig

from union._config import _get_authenticated_channel, _get_organization
from union._interceptor import intercept_channel_with_org


def _get_channel_with_org(platform_config: PlatformConfig) -> Tuple[grpc.Channel, str]:
    """Construct authenticated channel that injects the org."""
    channel = _get_authenticated_channel(platform_config)

    org = _get_organization(platform_config, channel)
    channel = intercept_channel_with_org(org, channel)
    return channel, org


def _validate_key_value_pairs(ctx, param, values) -> typing.Dict[str, str]:
    """
    Validate key value pairs, parses given values into a dictionary and validates that it is of type key=value.
    """
    if not values:
        return {}
    result = {}
    for value in values:
        if "=" not in value:
            raise click.BadParameter(f"Invalid key value pair: {value}")
        key, v = value.split("=", 1)
        result[key] = v
    return result


def _common_options() -> typing.List[click.Option]:
    return [
        click.Option(
            param_decls=["-p", "--project"],
            required=False,
            type=str,
            default=None,
            help="Project to operate on",
            show_default=True,
        ),
        click.Option(
            param_decls=["-d", "--domain"],
            required=False,
            type=str,
            default="development",
            help="Domain to operate on",
            show_default=True,
        ),
    ]


class InvokeBaseMixin:
    def invoke(self, ctx):
        try:
            return super().invoke(ctx)
        except grpc.RpcError as e:
            raise click.ClickException(f"Error invoking command: {e.details()}") from e
        except Exception as e:
            raise click.ClickException(f"Error invoking command: {e}") from e


class CommandBase(InvokeBaseMixin, click.RichCommand):
    def __init__(self, *args, **kwargs):
        if "params" not in kwargs:
            kwargs["params"] = []
        kwargs["params"].extend(_common_options())
        super().__init__(*args, **kwargs)


class GroupBase(InvokeBaseMixin, click.RichGroup):
    def __init__(self, *args, **kwargs):
        if "params" not in kwargs:
            kwargs["params"] = []
        kwargs["params"].extend(_common_options())
        super().__init__(*args, **kwargs)
