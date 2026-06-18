# SPDX-FileCopyrightText: 2021-2022 TU Wien.
# SPDX-FileCopyrightText: 2021 CERN.
# SPDX-License-Identifier: MIT

"""Resolver and proxy for requests."""

from invenio_records_resources.references.entity_resolvers import (
    RecordPKProxy,
    RecordResolver,
)

from ..records.api import Request, RequestEvent
from ..services import RequestEventsServiceConfig, RequestsServiceConfig


class RequestResolver(RecordResolver):
    """Resolver for requests."""

    type_id = "request"

    def __init__(self):
        """Initialize the default record resolver."""
        super().__init__(
            record_cls=Request,
            service_id=RequestsServiceConfig.service_id,
            type_key=self.type_id,
            proxy_cls=RecordPKProxy,
        )

    def _reference_entity(self, entity):
        """Create a reference dict for the given request."""
        return {self.type_key: str(entity.id)}


class RequestEventResolver(RecordResolver):
    """Resolver for requests."""

    type_id = "request_event"

    def __init__(self):
        """Initialize the default record resolver."""
        super().__init__(
            record_cls=RequestEvent,
            service_id=RequestEventsServiceConfig.service_id,
            type_key=self.type_id,
            proxy_cls=RecordPKProxy,
        )

    def _reference_entity(self, entity):
        """Create a reference dict for the given request."""
        return {self.type_key: str(entity.id)}
