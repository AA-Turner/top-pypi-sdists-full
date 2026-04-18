from agilicus import agilicus_api
from agilicus.input_helpers import build_object_prefix


def get_oauth2_routing_auth(existing, properties, pop=False):
    return build_object_prefix(
        existing, properties, "oauth2_routing_", agilicus_api.Oauth2AuthRouting, pop=pop
    )


def get_oauth2_auth(existing, properties, pop=False):
    routing = get_oauth2_routing_auth(existing.get("routing", {}), properties, pop=True)

    result = build_object_prefix(
        existing, properties, "oauth2_", agilicus_api.Oauth2Auth, pop=pop
    )
    if result and routing:
        result.routing = routing
    return result
