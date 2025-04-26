import datetime
from datetime import timedelta
import agilicus
from prettytable import PrettyTable
from operator import attrgetter
from . import get_many_entries

import agilicus_api.exceptions
import dateutil.tz
import operator
from colorama import Fore
import re
from typing import Optional
from urllib.parse import urlparse

from . import context
from . import output
from . import regions
from .input_helpers import get_org_from_input_or_ctx
from .input_helpers import strip_none
from agilicus import input_helpers
from .orgs import get_org_by_dictionary
from . import create_or_update
from .custom_types import Ternary

from .output.table import (
    spec_column,
    status_column,
    format_table,
    column,
    metadata_column,
    subtable,
)

TUNNEL_TERMINATION_TYPES = ["tcp", "inproc"]


def _filter_version(connector, not_version=None, only_version=None):
    if not not_version and not only_version:
        return False

    filter_out = True
    for instance in connector["status"].get("instances", []):
        try:
            v = _get_version(instance, "")
            if not_version and v != not_version:
                filter_out = False
            if only_version and v == only_version:
                filter_out = False
        except Exception:
            pass
    return filter_out


def _filter_os_version(connector, os_version_regex):
    if not os_version_regex:
        return False

    filter_out = True
    for instance in connector["status"].get("instances", []):
        try:
            if os_version_regex.match(_get_os_version(instance, "")):
                filter_out = False
        except Exception:
            pass
    return filter_out


def do_filter(
    ctx,
    no_down,
    connectors,
    not_version=None,
    only_version=None,
    sort_by=None,
    filter_os_version=None,
    **kwargs,
):
    if sort_by:
        connectors = sorted(connectors, key=lambda k: (operator.attrgetter(*sort_by)(k)))

    os_version_regex = None
    if filter_os_version:
        os_version_regex = re.compile(filter_os_version)
    filtered_connectors = []
    for connector in connectors:
        if _filter_version(connector, not_version, only_version):
            continue
        if _filter_os_version(connector, os_version_regex):
            continue
        if not no_down:
            filtered_connectors.append(connector)
        elif connector["status"]["operational_status"]["status"] != "down":
            filtered_connectors.append(connector)
    return filtered_connectors


def query(
    ctx,
    no_down=False,
    not_version=None,
    only_version=None,
    sort_by=None,
    page_at_id=None,
    page_size=500,
    filter_os_version=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    params = {}
    params["org_id"] = org_id
    if page_at_id is None:
        page_at_id = ""
    input_helpers.update_if_not_none(params, kwargs)
    query_results = get_many_entries(
        apiclient.connectors_api.list_connector,
        "connectors",
        maximum=kwargs.get("limit", None),
        page_size=page_size,
        page_at_id=page_at_id,
        **params,
    )
    return do_filter(
        ctx,
        no_down,
        query_results,
        only_version=only_version,
        not_version=not_version,
        sort_by=sort_by,
        filter_os_version=filter_os_version,
        **kwargs,
    )


def get(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    params = kwargs
    params["org_id"] = org_id
    input_helpers.update_if_not_none(params, kwargs)
    return apiclient.connectors_api.get_connector(connector_id, **params)


def get_instance(ctx, connector_id, connector_instance_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    params = kwargs
    params["org_id"] = org_id
    input_helpers.update_if_not_none(params, kwargs)
    return apiclient.connectors_api.get_instance(
        connector_id, connector_instance_id, **params
    )


def query_agents(ctx, column_format=None, filter_not_has_version=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    if column_format == "newformat":
        kwargs["show_stats"] = True

    if org_id:
        kwargs["org_id"] = org_id
    query_results = apiclient.connectors_api.list_agent_connector(
        **strip_none(kwargs)
    ).agent_connectors
    return query_results


def query_agent_instances(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    if org_id:
        kwargs["org_id"] = org_id
    return apiclient.connectors_api.list_instances(
        connector_id, **strip_none(kwargs)
    ).agent_connector_instances


def format_agent_instances(ctx, instances, **kwargs):
    columns = [
        metadata_column("id"),
        spec_column("org_id"),
        status_column("instance_number"),
        status_column("name"),
        status_column("service_account_id"),
        column("status", newname="status", getter=_get_oper_status, optional=True),
    ]

    return format_table(ctx, instances, columns)


def _instances_table():
    instance_columns = [
        status_column("instance_number"),
        column(
            "overall_status",
            newname="overall_status",
            getter=_get_oper_status(attrgetter("status.operational_status")),
            optional=True,
        ),
        column("status.stats.overall_status_info", newname="status_info", optional=True),
        column("hostname", getter=_get_hostname, optional=True),
        column("os_version", getter=_get_os_version, optional=True),
        column("version", getter=_get_version, optional=True),
        column(
            "stats",
            newname="last_status_change",
            getter=_get_oper_status_change,
            optional=True,
        ),
    ]
    return instance_columns


def format_connectors_as_text(
    ctx, connectors, sort_by=None, skip_sub_table=False, **kwargs
):
    instance_columns = _instances_table()
    columns = [
        metadata_column("id"),
        spec_column("name"),
        column(
            "stats",
            newname="last_status_change",
            getter=_get_oper_status_change,
            optional=True,
        ),
    ]
    if "metadata.created" in sort_by:
        columns.append(metadata_column("created"))

    if not get_org_from_input_or_ctx(ctx, **kwargs):
        columns.append(spec_column("org_id"))
        org_dictionary = get_org_by_dictionary(ctx, "")
        for connector in connectors:
            org = org_dictionary[0].get(connector.spec.org_id, {})
            connector.spec["organisation"] = org.get("organisation")
        columns.append(spec_column("organisation"))

    columns.append(
        column(
            "status",
            newname="status",
            getter=_get_oper_status(attrgetter("status.operational_status")),
            optional=True,
        )
    )
    if skip_sub_table is False:
        columns.append(
            subtable(ctx, "instances", instance_columns, subobject_name="status")
        )

    return format_table(ctx, connectors, columns)


windows_ver_regex = """^.*[\\s]+([\\d]+\\.[\\d]+\\.[\\d]+).*$"""
windows_ver = re.compile(windows_ver_regex)


def _truncate_os(os_ver: str):
    if not os_ver:
        return os_ver

    if os_ver.upper().startswith("MICROSOFT WINDOWS"):
        ver_num = windows_ver.findall(os_ver)
        if ver_num:
            return "Windows " + ver_num[0]

    return os_ver[0:20]


def _shorten(data, limit=20):
    if data:
        val = data[:limit] + (".." if len(data) > limit else "")
        return val.strip()


def _remove_utc(datetime_obj):
    return str(datetime_obj.replace(microsecond=0)).split("+")[0]


def _get_status(record):
    status = record.get("status")
    if not status:
        return
    return status.to_dict()


def _get_connection_uri(record, key):
    if "connection_uri" in record["spec"]:
        parsed_uri = urlparse(record["spec"]["connection_uri"])
        return parsed_uri.netloc
    return None


def _get_oper_status(operstatus_getter):
    def getit(record, key):
        status = operstatus_getter(record)["status"]
        if status == "down":
            return f"{Fore.LIGHTRED_EX}{status}{Fore.RESET}"
        elif status == "degraded":
            return f"{Fore.LIGHTYELLOW_EX}{status}{Fore.RESET}"
        elif status == "warn":
            return f"{Fore.LIGHTYELLOW_EX}{status}{Fore.RESET}"
        elif status == "good":
            return f"{Fore.LIGHTGREEN_EX}{status}{Fore.RESET}"
        return status

    return getit


def _get_hostname(record, key):
    return _shorten(_get_stats(record)["system"]["hostname"])


def _get_version(record, key):
    system = _get_stats(record)["system"]
    if "agent_version" in system:
        return _shorten(system["agent_version"], 16)
    elif "version" in system:
        return _shorten(system["version"], 16)


def _get_os_version(record, key):
    return _truncate_os(_get_stats(record)["system"]["os_version"])


def _get_oper_status_change(record, key):
    return _remove_utc(
        _get_status(record)["operational_status"].get("status_change_time")
    )


def _get_stats(record, key=None):
    status = record.get("status")
    if not status:
        return
    return status.to_dict()["stats"]


def format_agents_with_version(  # noqa
    ctx, agents, column_format=None, filter_not_has_version=None, **kwargs
):
    org_by_id = dict()
    try:
        org_by_id, _ = get_org_by_dictionary(ctx, "")
    except agilicus_api.exceptions.ForbiddenException:
        # Fall back on getting just our own
        org_by_id, _ = get_org_by_dictionary(ctx, None)

    def _get_hostname(record, key):
        return _shorten(_get_stats(record)["system"]["hostname"])

    def _get_agent_uptime(record, key):
        secs = _get_stats(record)["system"]["agent_uptime"]
        sec = timedelta(seconds=secs)
        d = datetime.datetime(1, 1, 1) + sec
        return f"{d.day - 1}:{d.hour}:{d.minute}:{d.second}"

    def _get_collection_time(record, key):
        return _remove_utc(_get_stats(record)["metadata"]["collection_time"])

    def _get_overall_status(record, key):
        return _get_stats(record)["overall_status"]

    def _get_org(record):
        spec = record.get("spec").to_dict()
        org_id = spec.get("org_id")
        return org_by_id.get(org_id, org_id)

    def _get_org_name(record, keys):
        return _get_org(record).get("organisation")

    def _get_org_contact(record, keys):
        return _get_org(record).get("contact_email")

    def _row_filter(record):
        if not filter_not_has_version:
            return True
        try:
            version = _get_version(record, None)
            if version != filter_not_has_version:
                return True
        except Exception:
            pass
        return False

    columns = [
        metadata_column("id"),
        spec_column("name"),
        column("stats", newname="version", getter=_get_version, optional=True),
        column("stats", newname="uptime", getter=_get_agent_uptime, optional=True),
        column("stats", newname="os_version", getter=_get_os_version, optional=True),
        column("stats", newname="last_seen", getter=_get_collection_time, optional=True),
        column("stats", newname="status", getter=_get_oper_status, optional=True),
        column(
            "stats",
            newname="last_status_change",
            getter=_get_oper_status_change,
            optional=True,
        ),
        column("stats", newname="hostname", getter=_get_hostname, optional=True),
        column("spec", newname="org", getter=_get_org_name, optional=True),
        column("spec", newname="contact", getter=_get_org_contact, optional=True),
    ]

    return format_table(
        ctx, agents, columns, getter=operator.itemgetter, row_filter=_row_filter
    )


def format_agents_as_text(ctx, agents, column_format=None, **kwargs):
    if column_format == "newformat":
        return format_agents_with_version(ctx, agents, **kwargs)

    app_service_columns = [
        column("id"),
        column("hostname"),
        column("port"),
        column("protocol"),
        column("service_type"),
    ]
    columns = [
        metadata_column("id"),
        spec_column("name"),
        spec_column("org_id"),
        spec_column("connection_uri"),
        spec_column("max_number_connections"),
        spec_column("local_authentication_enabled"),
        subtable(
            ctx, "application_services", app_service_columns, subobject_name="status"
        ),
    ]

    return format_table(ctx, agents, columns)


def add_agent(ctx, point_of_presence_tag=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)

    spec = agilicus.AgentConnectorSpec(org_id=org_id, **kwargs)
    if point_of_presence_tag:
        spec.connector_cloud_routing = agilicus.ConnectorCloudRouting(
            point_of_presence_tags=regions.tag_list_to_tag_names(point_of_presence_tag)
        )

    connector = agilicus.AgentConnector(spec=spec)
    return create_or_update(
        connector,
        lambda obj: apiclient.connectors_api.create_agent_connector(obj),
        lambda guid, obj: apiclient.connectors_api.replace_agent_connector(
            guid, agent_connector=obj
        ),
    )[0]


def get_agent(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    kwargs = strip_none(kwargs)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    if org_id:
        kwargs["org_id"] = org_id
    return apiclient.connectors_api.get_agent_connector(connector_id, **kwargs)


def delete_agent(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)
    return apiclient.connectors_api.delete_agent_connector(
        connector_id, org_id=org_id, **kwargs
    )


def get_agent_info(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)
    return apiclient.connectors_api.get_agent_info(connector_id, org_id=org_id, **kwargs)


def add_agent_local_bind(
    ctx,
    connector_id,
    bind_port,
    bind_host=None,
    revocation_proxy=False,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    connector = apiclient.connectors_api.get_agent_connector(connector_id, org_id=org_id)

    if revocation_proxy:
        routing = connector.spec.revocation_proxy
        if routing is None:
            routing = agilicus.AgentConnectorRouting(local_binds=[])
    else:
        routing = connector.spec.routing
        if routing is None:
            routing = agilicus.AgentConnectorRouting(local_binds=[])

    bind = agilicus.AgentConnectorLocalBind(bind_host=bind_host, bind_port=bind_port)
    routing.local_binds.append(bind)
    if revocation_proxy:
        connector.spec.revocation_proxy = routing
    else:
        connector.spec.routing = routing

    return _replace_agent(apiclient, connector_id=connector_id, connector=connector)


def delete_agent_local_bind(
    ctx,
    connector_id,
    bind_port=None,
    bind_host=None,
    revocation_proxy=False,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    connector = apiclient.connectors_api.get_agent_connector(connector_id, org_id=org_id)

    if revocation_proxy:
        routing = connector.spec.revocation_proxy
        if routing is None:
            return connector
    else:
        routing = connector.spec.routing
        if routing is None:
            return connector

    results = []
    for bind in routing.local_binds:
        if bind_port is not None and bind_port != bind.bind_port:
            results.append(bind)
            continue

        if bind_host is not None and bind_host != bind.bind_host:
            results.append(bind)
            continue

    routing.local_binds = results
    if revocation_proxy:
        connector.spec.revocation_proxy = routing
    else:
        connector.spec.routing = routing

    return _replace_agent(apiclient, connector_id=connector_id, connector=connector)


def add_agent_egress_gateway(
    ctx,
    connector_id,
    bind_port,
    bind_host=None,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    connector = apiclient.connectors_api.get_agent_connector(connector_id, org_id=org_id)

    gateway = connector.spec.egress_gateway
    if gateway is None:
        gateway = agilicus.EgressGateway(local_binds=[])

    bind = agilicus.AgentConnectorLocalBind(bind_host=bind_host, bind_port=bind_port)
    gateway.local_binds.append(bind)
    connector.spec.egress_gateway = gateway

    return _replace_agent(apiclient, connector_id=connector_id, connector=connector)


def delete_agent_egress_gateway(
    ctx,
    connector_id,
    bind_port=None,
    bind_host=None,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    connector = apiclient.connectors_api.get_agent_connector(connector_id, org_id=org_id)

    gateway = connector.spec.egress_gateway
    if gateway is None:
        return connector

    results = []
    for bind in gateway.local_binds:
        if bind_port is not None and bind_port != bind.bind_port:
            results.append(bind)
            continue

        if bind_host is not None and bind_host != bind.bind_host:
            results.append(bind)
            continue

    gateway.local_binds = results
    connector.spec.egress_gateway = gateway

    return _replace_agent(apiclient, connector_id=connector_id, connector=connector)


def _replace_agent(apiclient, connector_id, connector):

    # Clear out the status since it's unnecessary.
    del connector["status"]
    return apiclient.connectors_api.replace_agent_connector(
        connector_id, agent_connector=connector
    )


def replace_agent(
    ctx,
    connector_id,
    connection_uri=None,
    max_number_connections=None,
    name=None,
    service_account_required=None,
    local_authentication_enabled=None,
    name_slug=None,
    point_of_presence_tag=None,
    clear_point_of_presence_tags=False,
    proxy_tunnel_termination=None,
    dynamic_routes_enabled: Optional[Ternary] = None,
    on_demand_routes_enabled: Optional[Ternary] = None,
    admin_status=None,
    trap_disabled=None,
    revocation_proxy_trusted_cert_bundle_id=None,
    revocation_proxy_rules_bundle_id=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)

    connector = apiclient.connectors_api.get_agent_connector(
        connector_id, org_id=org_id, **kwargs
    )

    if connection_uri:
        connector.spec.connection_uri = connection_uri

    if max_number_connections:
        connector.spec.max_number_connections = max_number_connections

    if name:
        connector.spec.name = name

    if service_account_required is not None:
        connector.spec.service_account_required = service_account_required

    if local_authentication_enabled is not None:
        connector.spec.local_authentication_enabled = local_authentication_enabled

    if name_slug is not None:
        connector.spec.name_slug = name_slug

    if clear_point_of_presence_tags:
        point_of_presence_tag = []

    if point_of_presence_tag is not None:
        tags = regions.tag_list_to_tag_names(point_of_presence_tag)
        cloud_routing = connector.spec.connector_cloud_routing
        if not cloud_routing:
            cloud_routing = agilicus.ConnectorCloudRouting(point_of_presence_tags=tags)
        else:
            cloud_routing.point_of_presence_tags = tags

        connector.spec.cloud_routing = cloud_routing

    _update_tunneling(connector, dynamic_routes_enabled, on_demand_routes_enabled)

    if admin_status is not None:
        connector.spec.admin_status = admin_status

    if trap_disabled is not None:
        connector.spec.trap_disabled = trap_disabled

    if proxy_tunnel_termination is not None:
        connector.spec.proxy_tunnel_termination = proxy_tunnel_termination

    if revocation_proxy_trusted_cert_bundle_id is not None:
        connector.spec.revocation_proxy.trusted_cert_bundle = (
            revocation_proxy_trusted_cert_bundle_id
        )

    if revocation_proxy_rules_bundle_id is not None:
        connector.spec.revocation_proxy.rules_bundle = revocation_proxy_rules_bundle_id

    return _replace_agent(apiclient, connector_id=connector_id, connector=connector)


def _update_tunneling(connector, dynamic_routes_enabled, on_demand_routes_enabled):
    if dynamic_routes_enabled is None and on_demand_routes_enabled is None:
        return

    routing = connector.spec.routing
    if routing is None:
        routing = agilicus.AgentConnectorCloudRouting(local_binds=[])
    connector.spec.routing = routing
    tunneling = routing.tunneling
    if not tunneling:
        tunneling = agilicus.AgentConnectorTunneling()
        routing.tunneling = tunneling

    if dynamic_routes_enabled is not None:
        dynamic = dynamic_routes_enabled.to_bool_or_none()
        tunneling.dynamic_routes_enabled = dynamic

    if on_demand_routes_enabled is not None:
        on_demand = on_demand_routes_enabled.to_bool_or_none()
        tunneling.on_demand_routes_enabled = on_demand


def replace_agent_auth_info(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)

    info = agilicus.AgentLocalAuthInfo(**kwargs)
    return apiclient.connectors_api.replace_agent_connector_local_auth_info(
        connector_id, agent_local_auth_info=info
    )


def set_agent_connector_stats(ctx, connector_id, org_id, overall_status, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    system_objs = input_helpers.get_objects_by_location("system", kwargs)
    system = agilicus.AgentConnectorSystemStats(
        agent_connector_org_id=org_id, agent_connector_id=connector_id, **system_objs
    )
    transport_objs = input_helpers.get_objects_by_location("transport", kwargs)
    transport = agilicus.AgentConnectorTransportStats(**transport_objs)
    now = datetime.datetime.utcnow().replace(tzinfo=dateutil.tz.tzutc())
    metadata = agilicus.AgentConnectorStatsMetadata(collection_time=now)

    stats = agilicus.AgentConnectorStats(
        metadata=metadata,
        overall_status=overall_status,
        system=system,
        transport=transport,
    )

    return apiclient.connectors_api.create_agent_stats(connector_id, stats)


def get_agent_connector_stats(ctx, connector_id, org_id, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    return apiclient.connectors_api.get_agent_stats(
        connector_id, org_id=org_id, **kwargs
    )


def add_table_stats_rows(instancesStats, stat, value):
    if isinstance(value, dict):
        for nstat, nvalue in value.items():
            add_table_stats_rows(instancesStats, stat + ":" + nstat, nvalue)
    elif isinstance(value, list):
        for index, row in enumerate(value):
            try:
                if not isinstance(row, dict):
                    row = row.to_dict()
                for nstat, nvalue in row.items():
                    add_table_stats_rows(
                        instancesStats, stat + f"[{index}]:" + nstat, nvalue
                    )
            except Exception:
                pass
    else:
        instancesStats.setdefault(stat, []).append(value)


def show_agent_connector_stats(ctx, connector_id, **kwargs):
    headings = []
    headings.append("Statistic")
    results = query_agent_instances(ctx, connector_id, **kwargs)
    instance_stats = []
    for instance in results:
        instance_dict = instance.to_dict()
        stats = instance_dict.get("status", {}).get("stats", {})
        if not stats:
            continue

        for sub_key in ["sys_info", "perf_metrics"]:
            info = instance_dict.get("status", {}).get(sub_key, {})
            if info:
                stats.update({sub_key: info})

        instance_stats.append(stats)
        headings.append(instance.status.name)

    table = PrettyTable(headings)

    instancesStats = {}
    for stats in instance_stats:
        for stat, value in stats.items():
            add_table_stats_rows(instancesStats, stat, value)
    for stat, entries in instancesStats.items():
        row = []
        row.append(stat)
        row.extend(entries)
        table.add_row(row)
    table.align = "l"
    print(table)


def show_agent_connector_dynamic_stats(
    ctx, connector_id, org_id=None, detailed=False, breakdown=False, **kwargs
):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    stats = get_agent_connector_dynamic_stats(ctx, connector_id, org_id, **kwargs)
    if not context.output_console(ctx):
        output.output_formatted(ctx, stats.to_dict())
        return

    headings = []
    headings.append("Statistic")
    headings.append("Value")
    table = PrettyTable(headings)
    table.add_row(("last_updated", stats.metadata.collection_time))
    stat_rows = _collate_upstream_stats(ctx, stats.upstream_totals, detailed)
    to_add_breakdown = []
    if breakdown:
        to_add_breakdown = stats.upstream_breakdown

    for item in to_add_breakdown:
        prefix = [item.connector_instance_id, item.application_service_id]
        stat_rows.extend(
            _collate_upstream_stats(ctx, item.upstream_stats, detailed, prefix)
        )

    for stat, val in stat_rows:
        row = []
        row.append(stat)
        row.append(val)
        table.add_row(row)

    table.align = "l"
    print(table)


def list_connector_dynamic_stats(
    ctx, connector_ids, org_id=None, detailed=False, breakdown=False, **kwargs
):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    results = do_list_connector_stats(
        ctx, connector_ids, org_id, show_dynamic=True, **kwargs
    )
    if not context.output_console(ctx):
        output.output_formatted(ctx, results.to_dict()["dynamic_stats"])
        return

    headings = []
    headings.append("Statistic")
    headings.append("Value")
    table = PrettyTable(headings)
    for stats in results.dynamic_stats:
        base_prefix = [stats.connector_id]
        table.add_row((f"{base_prefix[0]}.last_updated", stats.metadata.collection_time))
        stat_rows = _collate_upstream_stats(
            ctx, stats.upstream_totals, detailed, base_prefix
        )
        to_add_breakdown = []
        if breakdown:
            to_add_breakdown = stats.upstream_breakdown

        for item in to_add_breakdown:
            prefix = base_prefix + [
                item.connector_instance_id,
                item.application_service_id,
            ]
            stat_rows.extend(
                _collate_upstream_stats(ctx, item.upstream_stats, detailed, prefix)
            )

        for stat, val in stat_rows:
            row = []
            row.append(stat)
            row.append(val)
            table.add_row(row)

    table.align = "l"
    print(table)


def list_connector_static_stats(ctx, connector_ids, org_id=None, **kwargs):
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    results = do_list_connector_stats(
        ctx, connector_ids, org_id, show_static=True, **kwargs
    )
    return results.static_stats


def format_static_stats_as_text(
    ctx,
    stats,
):
    instance_columns = _instances_table()
    columns = [
        column("connector_id"),
        column(
            "status",
            newname="status",
            getter=_get_oper_status(attrgetter("operational_status")),
            optional=True,
        ),
        subtable(ctx, "instances", instance_columns),
    ]

    return format_table(ctx, stats, columns)


def _collate_upstream_stats(ctx, upstream_stats, detailed, name_prefix=None):
    results = []
    upstream_stats = upstream_stats.to_dict()
    net_sum = upstream_stats.get("network_summary_stats")
    results.extend(_collate_stats_object(ctx, net_sum, name_prefix=name_prefix))
    http_sum = upstream_stats.get("http_summary_stats")
    results.extend(_collate_stats_object(ctx, http_sum, name_prefix=name_prefix))
    share_sum = upstream_stats.get("share_summary_stats")
    results.extend(_collate_stats_object(ctx, share_sum, name_prefix=name_prefix))

    if not detailed:
        return results

    net_sum = upstream_stats.get("network_detailed_stats")
    results.extend(_collate_stats_object(ctx, net_sum, name_prefix=name_prefix))
    http_sum = upstream_stats.get("http_detailed_stats")
    results.extend(_collate_stats_object(ctx, http_sum, name_prefix=name_prefix))
    share_sum = upstream_stats.get("share_detailed_stats")
    results.extend(_collate_stats_object(ctx, share_sum, name_prefix=name_prefix))
    return results


def _collate_stats_object(ctx, stats_obj, name_prefix=None):
    if not stats_obj:
        return []
    results = []
    if name_prefix is None:
        name_prefix = []
    for key, val in stats_obj.items():
        name = name_prefix + [key]
        if isinstance(val, dict):
            results.extend(_collate_stats_object(ctx, val, name))
            continue
        results.append((".".join(name), val))
    return results


def get_agent_connector_dynamic_stats(
    ctx, connector_id, org_id, collected_since: datetime.datetime, **kwargs
) -> agilicus_api.AgentConnectorDynamicStats:
    apiclient = context.get_apiclient_from_ctx(ctx)

    if collected_since is not None:
        collected_since = collected_since.replace(tzinfo=datetime.timezone.utc)
        kwargs["collected_since"] = collected_since
    results = apiclient.connectors_api.get_agent_connector_dynamic_stats(
        connector_id=connector_id, org_id=org_id, **kwargs
    )
    return results


def do_list_connector_stats(
    ctx,
    connector_ids,
    org_id,
    collected_since: Optional[datetime.datetime] = None,
    show_dynamic=False,
    show_static=False,
    **kwargs,
) -> agilicus_api.AgentConnectorDynamicStats:
    apiclient = context.get_apiclient_from_ctx(ctx)

    if collected_since is not None:
        collected_since = collected_since.replace(tzinfo=datetime.timezone.utc)
        kwargs["collected_since"] = collected_since

    results = apiclient.connectors_api.list_connector_stats(
        connector_id_list=connector_ids,
        org_id=org_id,
        show_dynamic=show_dynamic,
        show_static=show_static,
        **kwargs,
    )
    return results


def query_ipsec(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    kwargs["org_id"] = org_id
    kwargs = strip_none(kwargs)
    query_results = apiclient.connectors_api.list_ipsec_connector(**kwargs)
    return query_results


def add_ipsec(ctx, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)

    spec = agilicus.IpsecConnectorSpec(org_id=org_id, **kwargs)
    connector = agilicus.IpsecConnector(spec=spec)
    return apiclient.connectors_api.create_ipsec_connector(connector)


def add_or_update_ipsec_connection(
    ctx,
    connector_id,
    name,
    org_id=None,
    inherit_from=None,
    remote_ipv4_block=None,
    ike_chain_of_trust_certificates_filename=None,
    update_connection=False,
    **kwargs,
):

    kwargs = strip_none(kwargs)
    if ike_chain_of_trust_certificates_filename is not None:
        ike_chain_of_trust_certificates = open(
            ike_chain_of_trust_certificates_filename, "r"
        ).read()
        kwargs["ike_chain_of_trust_certificates"] = ike_chain_of_trust_certificates

    if remote_ipv4_block:
        remote_ipv4_ranges = []
        for block in remote_ipv4_block:
            remote_ipv4_ranges.append(
                agilicus.IpsecConnectionIpv4Block(ipv4_address_block=block)
            )
        kwargs["remote_ipv4_ranges"] = remote_ipv4_ranges

    connector = get_ipsec(ctx, connector_id, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    if update_connection:
        new_connections = []
        for _connection in connector.spec.connections:
            if _connection.name == name:
                # update the connection with the updated kwargs by just blasting the new
                # values in to it.
                for k, v in kwargs.items():
                    _connection.spec[k] = v
                connection = _connection
                if inherit_from is not None:
                    connection.inherit_from = inherit_from

            new_connections.append(_connection)
        connector.spec.connections = new_connections
    else:
        connection_spec = input_helpers.model_from_dict(
            agilicus.IpsecConnectionSpec, kwargs
        )
        connection = agilicus.IpsecConnection(name, spec=connection_spec)
        if inherit_from:
            connection.inherit_from = inherit_from
        connector.spec.connections.append(connection)

    return apiclient.connectors_api.replace_ipsec_connector(
        connector_id, ipsec_connector=connector
    )


def delete_ipsec_connection(ctx, connector_id, name, org_id=None, **kwargs):
    connector = get_ipsec(ctx, connector_id, org_id=org_id)
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)

    kwargs = strip_none(kwargs)
    update_connections = []
    for connection in connector.spec.connections:
        if connection.name != name:
            update_connections.append(connection)
    connector.spec.connections = update_connections

    return apiclient.connectors_api.replace_ipsec_connector(
        connector_id, ipsec_connector=connector
    )


def get_ipsec(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)
    return apiclient.connectors_api.get_ipsec_connector(
        connector_id, org_id=org_id, **kwargs
    )


def delete_ipsec(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)
    return apiclient.connectors_api.delete_ipsec_connector(
        connector_id, org_id=org_id, **kwargs
    )


def get_ipsec_info(ctx, connector_id, org_id=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)
    return apiclient.connectors_api.get_ipsec_connector_info(
        connector_id, org_id=org_id, **kwargs
    )


def replace_ipsec(
    ctx,
    connector_id,
    name=None,
    name_slug=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)

    connector = apiclient.connectors_api.get_ipsec_connector(
        connector_id, org_id=org_id, **kwargs
    )

    if name:
        connector.spec.name = name

    if name_slug:
        connector.spec.name_slug = name_slug

    return apiclient.connectors_api.replace_ipsec_connector(
        connector_id, ipsec_connector=connector
    )


def show_connectors_usage_metrics(ctx, org_ids, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    if not org_ids:
        raise Exception("require at least one org_id")
    return apiclient.connectors_api.get_connector_usage_metrics(org_ids=org_ids)


def format_queues(ctx, queues):
    columns = [
        metadata_column("id"),
        spec_column("connector_id"),
        spec_column("instance_name"),
        spec_column("org_id"),
        spec_column("queue_ttl"),
        status_column("queue_name"),
        status_column("expired"),
    ]

    return format_table(ctx, queues.queues, columns)


def get_connector_queues(ctx, connector_id=None, org_id=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    params = kwargs
    if org_id is None:
        params["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    input_helpers.update_if_not_none(params, kwargs)
    if connector_id is not None:
        return apiclient.connectors_api.get_connector_queues(connector_id, **params)
    else:
        return apiclient.connectors_api.get_queues(**params)


def add_connector_queue(
    ctx,
    connector_id=None,
    instance_name=None,
    queue_ttl=None,
    dynamic_routes_enabled=None,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    spec = agilicus_api.AgentConnectorQueueSpec(
        connector_id=connector_id, instance_name=instance_name, org_id=org_id
    )

    if queue_ttl is not None:
        spec.queue_ttl = queue_ttl

    if dynamic_routes_enabled is not None:
        spec.dynamic_routes_enabled = True
    queue = agilicus_api.AgentConnectorQueue(spec=spec)

    return apiclient.connectors_api.create_queue(connector_id, queue)


def delete_connector_queue(ctx, connector_id, queue_id, org_id=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    params = kwargs
    if org_id is None:
        params["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    input_helpers.update_if_not_none(params, kwargs)
    return apiclient.connectors_api.delete_connector_queue(
        connector_id, queue_id, **params
    )


def delete_agent_connector_instance(ctx, connector_id, connector_instance_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs.pop("org_id", None)
    kwargs = strip_none(kwargs)
    return apiclient.connectors_api.delete_instance(
        connector_id,
        connector_instance_id=connector_instance_id,
        org_id=org_id,
    )


def get_connector_stats_config(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    kwargs["org_id"] = get_org_from_input_or_ctx(ctx, **kwargs)
    return apiclient.connectors_api.get_stats_config(connector_id, **kwargs)


def configure_stats_publishing(
    ctx,
    org_id,
    connector_id,
    publish_period_s,
    net_summary_duration_s,
    http_summary_duration_s,
    net_detailed_duration_s,
    http_detailed_duration_s,
    share_summary_duration_s,
    share_detailed_duration_s,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, org_id=org_id)

    net = agilicus_api.StatsPublishingLevelConfig()
    http = agilicus_api.StatsPublishingLevelConfig()
    share = agilicus_api.StatsPublishingLevelConfig()

    if net_summary_duration_s:
        net.summary_duration_seconds = net_summary_duration_s
    if net_detailed_duration_s:
        net.detailed_duration_seconds = net_detailed_duration_s
    if http_summary_duration_s:
        http.summary_duration_seconds = http_summary_duration_s
    if http_detailed_duration_s:
        http.detailed_duration_seconds = http_detailed_duration_s
    if share_summary_duration_s:
        share.summary_duration_seconds = share_summary_duration_s
    if share_detailed_duration_s:
        share.detailed_duration_seconds = share_detailed_duration_s

    cfg = agilicus_api.StatsPublishingConfig(
        upstream_network_publishing=net,
        upstream_http_publishing=http,
        upstream_share_publishing=share,
        publish_period_seconds=publish_period_s,
    )
    req = agilicus_api.ConfigureConnectorStatsPublishingRequest(
        org_id, connector_ids=list(connector_id), stats_publishing_config=cfg
    )
    return apiclient.connectors_api.create_configure_publishing_request(req)


def format_for_gc(ctx, connectors):
    columns = [
        metadata_column("id"),
        spec_column("org_id", "org id"),
        spec_column("name"),
    ]
    return format_table(ctx, connectors, columns)


def list_connector_proxies(
    ctx,
    page_at_id=None,
    page_size=500,
    **kwargs,
):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    params = {}
    params["org_id"] = org_id
    if page_at_id is None:
        page_at_id = ""
    input_helpers.update_if_not_none(params, kwargs)
    return get_many_entries(
        apiclient.connectors_api.list_proxies,
        "connector_proxies",
        maximum=kwargs.get("limit", None),
        page_size=page_size,
        page_at_id=page_at_id,
        **params,
    )


def add_connector_proxy(ctx, bind_host=None, bind_port=None, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    spec = agilicus.AgentConnectorProxySpec(org_id=org_id, **kwargs)

    if bind_port or bind_host:
        local_bind = agilicus_api.AgentConnectorLocalBind(
            bind_host=bind_host,
            bind_port=bind_port,
        )
        spec.local_bind = local_bind

    return apiclient.connectors_api.create_connector_proxy(
        agilicus.AgentConnectorProxy(spec),
    )


def delete_connector_proxy(ctx, id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)

    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs = strip_none(kwargs)

    return apiclient.connectors_api.delete_proxy(
        id,
        org_id=org_id,
    )


def query_services(ctx, connector_id, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    kwargs["org_id"] = org_id
    kwargs = strip_none(kwargs)
    return apiclient.connectors_api.list_services(connector_id, **kwargs).services


def add_service(ctx, connector_id, service, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)

    spec = agilicus.ConnectorServiceSpec(
        org_id=org_id,
        service=service,
        connector_id=connector_id,
    )
    connectorService = agilicus.ConnectorService(spec=spec)
    return apiclient.connectors_api.create_service(connector_id, connectorService)


def delete_service(ctx, connector_id, service, **kwargs):
    token = context.get_token(ctx)
    apiclient = context.get_apiclient(ctx, token)
    org_id = get_org_from_input_or_ctx(ctx, **kwargs)
    kwargs["org_id"] = org_id
    kwargs = strip_none(kwargs)
    return apiclient.connectors_api.delete_service(
        connector_id, connector_service=service, **kwargs
    )
