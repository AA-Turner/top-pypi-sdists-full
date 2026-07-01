from __future__ import annotations

import grpc
import logging

from dbt_state.auth.sso import SsoAuth


logger = logging.getLogger(__name__)


class GrpcAuthPlugin(grpc.AuthMetadataPlugin):
    def __init__(self, sso: SsoAuth) -> None:
        self._sso: SsoAuth = sso

    def __call__(
        self,
        context: grpc.AuthMetadataContext,
        callback: grpc.AuthMetadataPluginCallback,
    ) -> None:
        try:
            token = self._sso.id_token(login=True)
            callback((("authorization", f"Bearer {token}"),), None)
        except Exception as e:
            logger.error(f"Failed to get authentication token for gRPC call: {e}")
            callback(tuple(), None)
