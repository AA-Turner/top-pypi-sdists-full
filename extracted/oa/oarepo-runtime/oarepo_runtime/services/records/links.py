#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Utility for rendering URI template links."""

from __future__ import annotations

from typing import Any, override

from invenio_records_resources.services.base.links import EndpointLink


def rdm_pagination_record_endpoint_links(endpoint: str, params: list[str] | None = None) -> dict[str, EndpointLink]:
    """Create pagination links (prev/self/next) from the same endpoint.

    These links are used on a record instance where we want to have a list of something,
    for example /records/<pid>/versions.

    Note: using RecordEndpointLink here is fragile as it normally expects
    a record as the first argument to vars, but here we pass pagination
    as the first argument to vars. Because pagination does not have pid_value
    attribute, the vars method will just skip adding pid_value to vars and
    the pid_value must be passed via params. This is done in invenio_rdm_records'
    service but not in invenio_drafts_resources service, where the parameter is
    called "id" instead of "pid_value". That is why this function is called rdm_...
    """
    params = [*(params or []), "pid_value"]

    class RecordEndpointLinkWithId(EndpointLink):
        @override
        @staticmethod
        def vars(obj: Any, vars: dict[str, Any]) -> None:
            pid_value = vars.pop("id", None)
            if pid_value is not None:
                vars["pid_value"] = pid_value

    return {
        "prev": RecordEndpointLinkWithId(
            endpoint,
            when=lambda pagination, _ctx: pagination.has_prev,
            vars=lambda pagination, _vars: _vars["args"].update({"page": pagination.prev_page.page}),
            params=params,
        ),
        "self": RecordEndpointLinkWithId(
            endpoint,
            params=params,
        ),
        "next": RecordEndpointLinkWithId(
            endpoint,
            when=lambda pagination, _ctx: pagination.has_next,
            vars=lambda pagination, _vars: _vars["args"].update({"page": pagination.next_page.page}),
            params=params,
        ),
    }


def pagination_endpoint_links_html(endpoint: str, params: list[str] | None = None) -> dict[str, EndpointLink]:
    """Create pagination links (prev/self/next) from the same endpoint."""
    return {
        "prev_html": EndpointLink(
            endpoint,
            when=lambda pagination, _ctx: pagination.has_prev,
            vars=lambda pagination, _vars: _vars["args"].update({"page": pagination.prev_page.page}),
            params=params,
        ),
        "self_html": EndpointLink(endpoint, params=params),
        "next_html": EndpointLink(
            endpoint,
            when=lambda pagination, _ctx: pagination.has_next,
            vars=lambda pagination, _vars: _vars["args"].update({"page": pagination.next_page.page}),
            params=params,
        ),
    }
