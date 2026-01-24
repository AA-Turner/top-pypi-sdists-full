# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Utilities for updating preflight hashes with information from requests

This module is primarily tested by framework tests.
"""

from dataclasses import replace
from contrast.utils.decorators import fail_loudly
from contrast.utils.digest_utils import Digest

from contrast_fireball import AssessFinding
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")


def _get_route_for_hash(context):
    """
    Get route to be used for hashing according to preflight spec:

        1. Route signature
        2. Normalized uri - the agents best attempt at normalizing the URI
           for path parameters. typically this involves a regex to abstract
           numeric or UUID path segments, but is not well defined. ideally,
           this case will phase out as route coverage expands, so the
           definition does not need to be consistent across agents so long
           as it is consistent within them.
        3. Raw uri
    """
    route = context.observed_route
    if route is not None and route.signature:
        return route.signature

    normalized_uri = context.request.get_normalized_uri()
    return normalized_uri or context.request.path_qs


def _get_verb_for_hash(context):
    route = context.observed_route
    if route is not None and route.verb:
        return route.verb

    return context.request.method


@fail_loudly("Failed to update preflight hashes")
def update_preflight_hashes(context):
    """
    Update preflight hashes for all findings with available route/request info

    @param context: Current request context
    """

    context.findings = [
        replace(finding, hash=finding_hash(finding, route_hash(context)))
        for finding in context.findings
    ]


def finding_hash(finding: AssessFinding, route_hash: str):
    hasher = Digest()
    hasher.update(str(finding.hash))
    hasher.update(route_hash)
    return hasher.crc32


def route_hash(context):
    hasher = Digest()
    hasher.update(_get_route_for_hash(context))
    hasher.update(_get_verb_for_hash(context))
    return hasher.finish()
