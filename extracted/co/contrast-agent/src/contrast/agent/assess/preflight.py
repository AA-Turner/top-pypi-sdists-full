# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Utilities for computing preflight hashes from route and request information

This module is primarily tested by framework tests.
"""

from __future__ import annotations

import typing

from contrast.utils.digest_utils import Digest
from contrast_vendor import structlog as logging

logger = logging.getLogger("contrast")

if typing.TYPE_CHECKING:
    from contrast_fireball import AssessFinding, ObservedRoute

    from contrast.agent.context import WebContext


def _get_route_for_hash(web_context: WebContext, route: ObservedRoute):
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
    if route.signature:
        return route.signature

    normalized_uri = web_context.request.get_normalized_uri()
    return normalized_uri or web_context.request.path_qs


def _get_verb_for_hash(web_context: WebContext, route: ObservedRoute):
    if route.verb:
        return route.verb

    return web_context.request.method


def finding_hash(finding: AssessFinding, route_hash: str):
    hasher = Digest()
    hasher.update(str(finding.hash))
    hasher.update(route_hash)
    return hasher.crc32


def route_hash(web_context: WebContext, observed_route: ObservedRoute):
    hasher = Digest()
    hasher.update(_get_route_for_hash(web_context, observed_route))
    hasher.update(_get_verb_for_hash(web_context, observed_route))
    return hasher.finish()
