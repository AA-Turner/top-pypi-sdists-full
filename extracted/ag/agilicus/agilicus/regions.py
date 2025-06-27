from typing import List
import sys
import socket

import agilicus
import json

from . import context
from .input_helpers import strip_none
from .input_helpers import add_remove_uniq_list
from .output.table import (
    spec_column,
    format_table,
    metadata_column,
    status_column,
)


def list_point_of_presences(
    ctx, excludes_all_tag, excludes_any_tag, includes_all_tag, includes_any_tag, **kwargs
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    excludes_all_tags = tag_list_to_tag_names(excludes_all_tag)
    excludes_any_tags = tag_list_to_tag_names(excludes_any_tag)
    includes_all_tags = tag_list_to_tag_names(includes_all_tag)
    includes_any_tags = tag_list_to_tag_names(includes_any_tag)

    return apiclient.regions_api.list_point_of_presences(
        excludes_all_tag=excludes_all_tags,
        excludes_any_tag=excludes_any_tags,
        includes_all_tag=includes_all_tags,
        includes_any_tag=includes_any_tags,
        **strip_none(kwargs),
    ).point_of_presences


def add_point_of_presence(ctx, name, tag: List[str], domain=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)

    tags = []
    if tag:
        tags = tag_list_to_tag_names(tag)

    domains = []
    if domain:
        domains = [agilicus.Domain(d) for d in domain]

    routing = agilicus.PointOfPresenceRouting(domains=domains)
    pop_spec = agilicus.PointOfPresenceSpec(
        name=agilicus.FeatureTagName(name), tags=tags, routing=routing
    )
    pop = agilicus.PointOfPresence(spec=pop_spec)
    return apiclient.regions_api.add_point_of_presence(pop)


def update_point_of_presence(
    ctx,
    pop_id,
    tag: List[str],
    domain=None,
    overwrite_tags=False,
    overwrite_domains=False,
    name=None,
    add_cluster_ids=None,
    remove_cluster_ids=None,
    master_cluster_id=None,
    requests_enabled=None,
    org_domain=None,
    public=None,
    restrict_by_user_id=None,
    add_permitted_user_id=None,
    remove_permitted_user_id=None,
    routing_ces=None,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)

    original = apiclient.regions_api.get_point_of_presence(point_of_presence_id=pop_id)

    tags = []
    if tag:
        tags = tag_list_to_tag_names(tag)

    if not overwrite_tags:
        tags.extend(original.spec.tags)
        tags = tag_list_to_tag_names(list(set(str(tag) for tag in tags)))

    original.spec.tags = tags

    domains = []
    if domain:
        domains = [agilicus.Domain(d) for d in domain]

    org_domains = []
    if org_domain:
        org_domains = [agilicus.Domain(d) for d in org_domain]

    if not overwrite_domains:
        to_write = original.spec.routing.domains
        for domain in domains:
            if domain not in to_write:
                to_write.append(domain)
        domains = to_write

    original.spec.routing.domains = domains
    original.spec.routing.org_domains = org_domains
    if name is not None:
        original.spec.name = name

    if requests_enabled is not None:
        original.spec.routing.requests_enabled = requests_enabled

    if public is not None:
        original.spec.routing.public = public

    if restrict_by_user_id is not None:
        original.spec.routing.restrict_by_user_id = restrict_by_user_id

    if routing_ces is not None:
        original.spec.routing.ces = routing_ces

    original.spec.routing.permitted_user_ids = add_remove_uniq_list(
        original.spec.routing.permitted_user_ids,
        add_permitted_user_id,
        remove_permitted_user_id,
    )

    original.spec.cluster_ids = add_remove_uniq_list(
        original.spec.cluster_ids,
        add_cluster_ids,
        remove_cluster_ids,
    )
    if master_cluster_id is not None:
        original.spec.master_cluster_id = master_cluster_id

    return apiclient.regions_api.replace_point_of_presence(
        pop_id,
        point_of_presence=original,
    )


def show_point_of_presence(ctx, pop_id):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.regions_api.get_point_of_presence(point_of_presence_id=pop_id)


def delete_point_of_presence(ctx, pop_id):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.regions_api.delete_point_of_presence(point_of_presence_id=pop_id)


def format_point_of_presences_as_text(ctx, tags):
    columns = [
        metadata_column("id"),
        spec_column("name"),
        spec_column("tags"),
        spec_column("routing", "routing"),
        spec_column("master_cluster_id"),
        status_column("clusters"),
    ]

    return format_table(ctx, tags, columns)


def tag_list_to_tag_names(tags: List[str]) -> List[agilicus.FeatureTagName]:
    return [agilicus.FeatureTagName(tag_name) for tag_name in tags]


def add_cluster(ctx, name, ip_addresses=None, description=None, domain=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)

    config = agilicus.ClusterConfig()

    if ip_addresses:
        config.ip_addresses = ip_addresses

    if description:
        config.description = description

    spec = agilicus.ClusterSpec(
        name=agilicus.Domain(name),
        config=config,
    )

    if domain:
        spec.domain = agilicus.Domain(domain)

    cluster = agilicus.Cluster(spec=spec)
    return apiclient.regions_api.add_cluster(cluster)


def _update_list(ip_addresses):
    return {k: True for v, k in enumerate(ip_addresses)}


def update_cluster(
    ctx,
    cluster_id,
    name=None,
    domain=None,
    remove_ip_addresses=None,
    add_ip_addresses=None,
    description=None,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)
    cluster = apiclient.regions_api.get_cluster(cluster_id)

    config = cluster.spec.config
    if not config:
        cluster.spec.config = agilicus.ClusterConfig()
        config = cluster.spec.config

    config.ip_addresses = add_remove_uniq_list(
        config.ip_addresses,
        add_ip_addresses,
        remove_ip_addresses,
    )

    if description:
        config.description = description

    if name:
        cluster.spec.name = agilicus.Domain(name)

    if domain:
        cluster.spec.domain = agilicus.Domain(domain)

    return apiclient.regions_api.replace_cluster(cluster_id, cluster=cluster)


def delete_cluster(ctx, cluster_id):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.regions_api.delete_cluster(cluster_id)


def list_clusters(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)

    return apiclient.regions_api.list_clusters(
        **strip_none(kwargs),
    ).clusters


def list_regions(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)

    return apiclient.regions_api.list_regions(
        **strip_none(kwargs),
    ).regions


def add_region(ctx, name, domain=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)

    domains = []
    if domain:
        domains = [agilicus.Domain(d) for d in domain]

    routing = agilicus.RegionRouting(domains=domains)
    region_spec = agilicus.RegionSpec(name=name, routing=routing)
    region = agilicus.Region(spec=region_spec)
    return apiclient.regions_api.add_region(region)


def update_region(
    ctx,
    region_id,
    domain=None,
    overwrite_domains=False,
    name=None,
    add_pop_ids=None,
    remove_pop_ids=None,
    master_pop_id=None,
    requests_enabled=None,
    org_domain=None,
    public=None,
    restrict_by_user_id=None,
    add_permitted_user_id=None,
    remove_permitted_user_id=None,
    routing_ces=None,
    **kwargs,
):
    apiclient = context.get_apiclient_from_ctx(ctx)

    original = apiclient.regions_api.get_region(region_id=region_id)

    domains = []
    if domain:
        domains = [agilicus.Domain(d) for d in domain]

    org_domains = []
    if org_domain:
        org_domains = [agilicus.Domain(d) for d in org_domain]

    if not overwrite_domains:
        to_write = original.spec.routing.domains
        for domain in domains:
            if domain not in to_write:
                to_write.append(domain)
        domains = to_write

    original.spec.routing.domains = domains
    original.spec.routing.org_domains = org_domains
    if name is not None:
        original.spec.name = name

    if requests_enabled is not None:
        original.spec.routing.requests_enabled = requests_enabled

    if public is not None:
        original.spec.routing.public = public

    if restrict_by_user_id is not None:
        original.spec.routing.restrict_by_user_id = restrict_by_user_id

    if routing_ces is not None:
        original.spec.routing.ces = routing_ces

    original.spec.routing.permitted_user_ids = add_remove_uniq_list(
        original.spec.routing.permitted_user_ids,
        add_permitted_user_id,
        remove_permitted_user_id,
    )

    original.spec.pop_ids = add_remove_uniq_list(
        original.spec.pop_ids,
        add_pop_ids,
        remove_pop_ids,
    )
    if master_pop_id is not None:
        original.spec.master_pop_id = master_pop_id

    return apiclient.regions_api.replace_region(
        region_id,
        region=original,
    )


def delete_region(ctx, region_id):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.regions_api.delete_region(region_id=region_id)


def _filter_requests_enabled(objs):
    filtered = []
    for obj in objs:
        if obj.spec.routing and obj.spec.routing.public:
            filtered.append(obj)
    return filtered


def _add_rule(name, domains, ip_addresses, ports):
    return {
        "name": name,
        "domains": domains,
        "ip_addresses": ip_addresses,
        "ports": ports,
    }


def _get_ip_addresses(obj):
    ip_addresses = []
    clusters = []
    if obj.status.get("pops"):
        for pop in obj.status.pops:
            clusters = pop.status.clusters or []
    elif obj.status.get("clusters"):
        clusters = obj.status.clusters

    for cluster in clusters:
        ip_addresses.extend(cluster.spec.config.ip_addresses or [])
    return set(ip_addresses)


def _get_ip_addresses_by_name(
    domains, port, obj, fail_on_domain_lookup_failure=None, **kwargs
):
    ip_addresses = set()
    for domain in domains:
        try:
            for addr in socket.getaddrinfo(domain, port):
                ip_addresses.add(addr[4][0])
        except Exception:
            print(f"no lookup for domain {domain}", file=sys.stderr)
            if fail_on_domain_lookup_failure:
                sys.exit(1)

    if obj:
        ip_addresses = ip_addresses.union(_get_ip_addresses(obj))

    return list(ip_addresses)


def _add_location(location_type, obj, **kwargs):
    loc = {}
    loc["name"] = str(obj.spec.name)
    loc["location_type"] = location_type
    hosting = loc.setdefault("hosting", {})
    hosting["cname_domain_forwards"] = [
        str(domain) for domain in obj.spec.routing.domains or []
    ]
    hosting["org_domains"] = [
        str(domain) for domain in obj.spec.routing.org_domains or []
    ]
    rules = hosting.setdefault("firewall-rules", {})
    allow = rules.setdefault("allow", [])
    allow.append(
        _add_rule(
            "www",
            ["www.agilicus.com"],
            _get_ip_addresses_by_name(["www.agilicus.com"], 443, None, **kwargs),
            [443],
        )
    )
    allow.append(
        _add_rule(
            "noc",
            ["api.agilicus.com"],
            _get_ip_addresses_by_name(["api.agilicus.com"], 443, None, **kwargs),
            [443],
        )
    )

    domains = []
    for domain in obj.spec.routing.domains or []:
        domains.append(str(domain))
        domains.append(f"agent-server.{domain}")
        domains.append(f"desktops.{domain}")
        domains.append(f"ssh-gateway.{domain}")
    allow.append(
        _add_rule(
            "admin/dataplane",
            domains,
            _get_ip_addresses_by_name(domains, 443, obj, **kwargs),
            [443],
        )
    )
    return loc


def build_agilicus_locations(ctx, *args, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)

    regions = _filter_requests_enabled(apiclient.regions_api.list_regions().regions)
    pops = _filter_requests_enabled(
        apiclient.regions_api.list_point_of_presences().point_of_presences
    )

    top = {}
    locations = top.setdefault("agilicus_locations", [])
    for region in regions:
        locations.append(_add_location("region", region, **kwargs))

    for pop in pops:
        locations.append(_add_location("pop", pop, **kwargs))
    print(json.dumps(top))


def routing_request(ctx, *args, ip_address=None, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    ip_addresses = []
    if ip_address is not None:
        ip_addresses = list(ip_address)
    request = agilicus.RoutingRequest(ip_addresses=ip_addresses)
    return apiclient.regions_api.routing_request(request)


def list_regional_locations(ctx, **kwargs):
    apiclient = context.get_apiclient_from_ctx(ctx)
    return apiclient.regions_api.get_regional_locations(**strip_none(kwargs))
