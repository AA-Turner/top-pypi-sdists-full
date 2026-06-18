# SPDX-FileCopyrightText: 2021-2022 TU Wien.
# SPDX-FileCopyrightText: 2021 CERN.
# SPDX-License-Identifier: MIT

"""Resolver and proxy for requests."""

from invenio_records_resources.references.registry import ResolverRegistryBase

from ..proxies import current_requests


class ResolverRegistry(ResolverRegistryBase):
    """Namespace for resolver functions."""

    @classmethod
    def get_registered_resolvers(cls):
        """Get all currently registered resolvers."""
        return iter(current_requests.entity_resolvers_registry)
