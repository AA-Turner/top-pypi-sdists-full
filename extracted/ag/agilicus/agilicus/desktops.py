import base64
import json

from . import context
from agilicus.agilicus_api import (
    ConfigFileFormat,
    CustomDesktopClientConfig,
    DesktopRemoteApp,
    DesktopResource,
    DesktopResourceSpec,
    DesktopClientConfiguration,
    DesktopClientConfigItem,
    DesktopConnectionInfo,
    DesktopServerConfiguration,
    VNCConnectionInfo,
    VNCPasswordAuthentication,
    UserMetadata,
    UserMetadataSpec,
)

from .input_helpers import build_updated_model
from .input_helpers import update_org_from_input_or_ctx
from .input_helpers import get_org_from_input_or_ctx
from .input_helpers import get_user_id_from_input_or_ctx
from .input_helpers import strip_none
from .output.table import (
    spec_column,
    format_table,
    metadata_column,
)
from .resource_helpers import map_resource_published


def list_desktop_resources(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    params = strip_none(kwargs)
    query_results = apiclient.app_services_api.list_desktop_resources(**params)
    return query_results.desktop_resources


def add_desktop_resource(
    ctx,
    read_write_password,
    read_only_password,
    read_write_username,
    read_only_username,
    disable_gateway,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    spec = DesktopResourceSpec(**strip_none(kwargs))
    model = DesktopResource(spec=spec)
    _update_connection_info(
        model,
        read_write_password=read_write_password,
        read_only_password=read_only_password,
        read_write_username=read_write_username,
        read_only_username=read_only_username,
        disable_gateway=disable_gateway,
    )
    return apiclient.app_services_api.create_desktop_resource(model).to_dict()


def _update_connection_info(
    model: DesktopResource,
    read_write_password=None,
    read_only_password=None,
    read_write_username=None,
    read_only_username=None,
    disable_gateway=None,
    **kwargs,
):
    if model.spec.desktop_type != "vnc":
        # nothing to do. Return the original
        return model.spec.connection_info

    conn_info = model.spec.connection_info or DesktopConnectionInfo()
    vnc_connection_info = conn_info.vnc_connection_info or VNCConnectionInfo()

    model.spec.connection_info = conn_info
    conn_info.vnc_connection_info = vnc_connection_info

    if disable_gateway is not None:
        vnc_connection_info.disable_gateway = disable_gateway

    if (
        read_write_password is None
        and read_only_password is None
        and read_write_username is None
        and read_only_username is None
    ):
        # nothing to do. Return the original
        return model.spec.connection_info

    password_auth = (
        vnc_connection_info.password_authentication_info or VNCPasswordAuthentication()
    )

    if read_write_password is not None:
        password_auth.read_write_password = read_write_password

    if read_only_password is not None:
        password_auth.read_only_password = read_only_password

    if read_write_username is not None:
        password_auth.read_write_username = read_write_username

    if read_only_username is not None:
        password_auth.read_only_username = read_only_username
    vnc_connection_info.password_authentication_info = password_auth
    return model.spec.connection_info


def _get_desktop_resource(ctx, apiclient, resource_id, **kwargs):
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.app_services_api.get_desktop_resource(resource_id, **kwargs)


def show_desktop_resource(ctx, resource_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return _get_desktop_resource(ctx, apiclient, resource_id, **kwargs).to_dict()


def delete_desktop_resource(ctx, resource_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    update_org_from_input_or_ctx(kwargs, ctx, **kwargs)
    return apiclient.app_services_api.delete_desktop_resource(resource_id, **kwargs)


def update_desktop_resource(
    ctx,
    resource_id,
    read_write_password,
    read_only_password,
    read_write_username,
    read_only_username,
    published,
    disable_gateway,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    get_args = {}
    update_org_from_input_or_ctx(get_args, ctx, **kwargs)
    mapping = _get_desktop_resource(ctx, apiclient, resource_id, **get_args)

    # This needs to run before the build_updated_model, because its check_type blows away
    # the types of nested objects, making them dicts.
    _update_connection_info(
        mapping,
        read_write_password=read_write_password,
        read_only_password=read_only_password,
        read_write_username=read_write_username,
        read_only_username=read_only_username,
        disable_gateway=disable_gateway,
    )

    # check_type=False works around nested types not deserializing correctly
    mapping.spec = build_updated_model(
        DesktopResourceSpec, mapping.spec, kwargs, check_type=False
    )
    mapping = map_resource_published(mapping, published)
    return apiclient.app_services_api.replace_desktop_resource(
        resource_id, desktop_resource=mapping
    ).to_dict()


def create_desktop_client_config(
    ctx, desktop_resource_id, as_text, raw, config_items, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["user_id"] = get_user_id_from_input_or_ctx(ctx, **kwargs)
    config = DesktopClientConfiguration(**strip_none(kwargs))
    if config_items:
        custom_config = CustomDesktopClientConfig(
            config_items=config_items,
        )
        config.custom_config = [custom_config]

    result = apiclient.app_services_api.create_client_configuration(
        desktop_resource_id, desktop_client_configuration=config
    )
    if raw:
        cfg = result.generated_config
    else:
        cfg = result.generated_config.configuration_file
    if as_text:
        return base64.b64decode(cfg).decode()
    return cfg


def create_desktop_server_config(ctx, desktop_resource_id, as_text, raw, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    config = DesktopServerConfiguration(
        configuration_file_format=ConfigFileFormat("win-reg"),
        **strip_none(kwargs),
    )

    result = apiclient.app_services_api.create_server_configuration(
        desktop_resource_id, desktop_server_configuration=config
    )
    if raw:
        cfg = result.generated_config
    else:
        cfg = result.generated_config.configuration_file
    if as_text:
        return base64.b64decode(cfg).decode()
    return cfg


def format_desktops_as_text(ctx, resources):
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        spec_column("name"),
        spec_column("address"),
        spec_column("desktop_type"),
        spec_column("session_type"),
        spec_column("connector_id"),
    ]

    return format_table(ctx, resources, columns)


def add_remote_app(ctx, desktop_id, command_path, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    get_args = {}
    update_org_from_input_or_ctx(get_args, ctx, **kwargs)
    desktop = _get_desktop_resource(ctx, apiclient, desktop_id, **get_args)
    spec = DesktopRemoteApp(command_path=command_path, **strip_none(kwargs))
    desktop.spec.remote_app = spec
    return apiclient.app_services_api.replace_desktop_resource(
        desktop_id, desktop_resource=desktop
    ).to_dict()


def update_remote_app(ctx, desktop_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    get_args = {}
    update_org_from_input_or_ctx(get_args, ctx, **kwargs)
    desktop = _get_desktop_resource(ctx, apiclient, desktop_id, **get_args)
    spec = desktop.spec.remote_app
    if spec is None:
        raise Exception("remote app not present. Please add one.")

    desktop.spec.remote_app = build_updated_model(DesktopRemoteApp, spec, kwargs)
    return apiclient.app_services_api.replace_desktop_resource(
        desktop_id, desktop_resource=desktop
    ).to_dict()


def clear_remote_app(ctx, desktop_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    get_args = {}
    update_org_from_input_or_ctx(get_args, ctx, **kwargs)
    desktop = _get_desktop_resource(ctx, apiclient, desktop_id, **get_args)
    spec = desktop.spec.remote_app
    if spec is None:
        return

    desktop.spec.remote_app = None
    return apiclient.app_services_api.replace_desktop_resource(
        desktop_id, desktop_resource=desktop
    ).to_dict()


_DESKTOP_OVERRIDE_NAME = "desktop-config-rdp-override"


def _get_existing_override(ctx, user_id, org_id, desktop_id):
    apiclient = context.get_apiclient_from_ctx(ctx)
    query_results = apiclient.user_api.list_user_metadata(user_id=user_id, org_id=org_id)
    results = query_results.user_metadata
    for result in results:
        spec = result.spec
        if spec.name == "desktop-config-rdp-override" and (
            desktop_id is None or desktop_id == result.spec.app_id
        ):
            return result
    return None


def set_desktop_config_override(ctx, config_items, desktop_id=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    user_id = get_user_id_from_input_or_ctx(ctx, **kwargs)
    custom_config = CustomDesktopClientConfig(
        config_items=config_items,
    )

    def to_json(obj):
        return json.dumps(apiclient.user_api.api_client.sanitize_for_serialization(obj))

    existing = _get_existing_override(ctx, user_id, org_id, desktop_id)
    if existing:
        existing.spec.data = to_json(custom_config)
        return apiclient.user_api.replace_user_metadata(
            existing.metadata.id, user_metadata=existing
        ).to_dict()
    spec = UserMetadataSpec(
        user_id=user_id,
        org_id=org_id,
        data_type="json",
        data=to_json(custom_config),
        name=_DESKTOP_OVERRIDE_NAME,
    )
    if desktop_id:
        spec.app_id = desktop_id
    model = UserMetadata(spec=spec)
    return apiclient.user_api.create_user_metadata(model).to_dict()


def parse_config_override_input(contents, name):
    if not name.endswith(".rdp"):
        raise ValueError("currently only RDP overrides are supported")

    lines = contents.splitlines()
    results = []
    for line in lines:
        if line.strip() == "":
            continue
        parts = line.split(":", 3)
        if len(parts) < 3:
            raise ValueError(
                f"invalid RDP file. Expect <option>:<type>:<value>. Got '{line}'"
            )

        results.append(
            DesktopClientConfigItem(
                key=parts[0],
                config_type=parts[1],
                value=parts[2],
                operation="set",
            )
        )

    return results
