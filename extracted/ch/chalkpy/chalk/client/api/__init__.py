from __future__ import annotations

from typing import TYPE_CHECKING

from chalk.client.api.datasources import Datasource, DatasourceAPI, DatasourceTestResult, IntegrationKind

if TYPE_CHECKING:
    from chalk.client.client_grpc import StubRefresher

__all__ = [
    "APINamespace",
    "Datasource",
    "DatasourceAPI",
    "DatasourceTestResult",
    "IntegrationKind",
]


class APINamespace:
    """Namespace for Chalk management APIs accessible via ``client.api``."""

    def __init__(self, stub_refresher: "StubRefresher"):
        super().__init__()
        self._datasources = DatasourceAPI(stub_refresher)

    @property
    def datasources(self) -> DatasourceAPI:
        return self._datasources
